import os
import uuid
from django.core.files.uploadedfile import UploadedFile
from django.contrib.auth.models import User, AbstractBaseUser, AnonymousUser

from ili_checker_app.logic.receiver_file_manager import ReceiverFileManager
from ili_checker_app.logic.uploads.local_upload_manager import LocalUploadManager
from ili_checker_app.logic.quality_rule import QualityRule
from ili_checker_app.logic.reports.report_manager import ReportManager

from ili_checker_app.models import Tarea, Modelo, Regla
from ili_checker_app.serializer import ReglaSerializer, ModeloSerializer

from ili_checker_app.submodules.iliservices.core.ili2db import Ili2DB
from ili_checker_app.submodules.iliservices.db.pg_factory import PGFactory
from ili_checker_app.utils.interlis_utils import get_xtf_models
from ili_checker_app.submodules.iliservices.core.ilivalidator import IliValidator

from ili_checker_app.config.general_config import TAG_RESPONSE_SQL

from ili_checker_app.utils.utils import update_task_status
from ili_checker_app.config.enums_config import TaskStatus


class JobManager:
    def __init__(self, file: UploadedFile, request_user: AbstractBaseUser | AnonymousUser) -> None:
        self._file = file
        self._filename = None
        self._user = request_user
        self._job_id = uuid.uuid4().hex
        self._output_dir = None
        self._task_id = None
        self._temp_file_path = None
        self._local_file_path = None
        self._schema_name = "ili_" + self._job_id
        self._pg_params = {'schema': self._schema_name}
        self._ili2db = Ili2DB()
        self._pg_factory = PGFactory()
        self._db = self._pg_factory.get_db_connector(self._pg_params)
        self._models = list()

        self._ilivalidator = IliValidator()

    def receiver(self, size_file: int) -> str | bool:
        """
        Receiver bytes and save file in temp dir and return a directory or false if error exist
        """
        receiver_manager = ReceiverFileManager(self._file, size_file)
        file_path = receiver_manager.save_file()
        if os.path.isfile(file_path):
            self._filename = os.path.basename(file_path)
            self._temp_file_path = file_path
            return self._temp_file_path
        else:
            return False

    def save_file(self) -> str:
        """
        Save file in local storage directory
        """
        local_manager = LocalUploadManager(self._temp_file_path, self._job_id)
        self._output_dir = local_manager.save()
        self._local_file_path = os.path.join(self._output_dir, self._filename)
        return self._output_dir

    def create_task(self) -> int:
        """
        Create new task and return id
        """
        new_task = Tarea.objects.create(
            nombre=self._filename,
            productos="",
            directorio=self.save_file(),
            usuario=User.objects.get(username='Anonimo') if str(self._user) == 'AnonymousUser' else self._user
        )

        self._task_id = new_task.id
        update_task_status(self._task_id, TaskStatus.PENDING)
        # self.run()

        return self._task_id

    def validation_xtf(self) -> bool:
        """
        File XTF is validated
        """
        file = self._local_file_path
        output_dir = self._output_dir

        configuration = self._ilivalidator.get_ilivalidator_configuration(file, output_dir=output_dir)
        res_validation, msg_validation = self._ilivalidator.validate_xtf(configuration)

        if res_validation:
            self.run()
        else:
            update_task_status(self._task_id, TaskStatus.ERROR)

        return res_validation

    def validate_models(self) -> list:
        models = get_xtf_models(self._local_file_path)
        for item in models:
            self._models.append(item["name"])
        return self._models
    
    def import_schema(self) -> tuple[bool, str]:
        configuration = self._ili2db.get_import_schema_configuration(self._db, self._models, create_basket_col=True)
        res_schema_import, msg_schema_import = self._ili2db.import_schema(self._db, configuration)
        return res_schema_import, msg_schema_import
    
    def import_data(self) -> tuple[bool, str]:
        xtf_path = self._local_file_path
        configuration = self._ili2db.get_import_data_configuration(self._db, xtf_path)
        res_import_data, msg_import_data = self._ili2db.import_data(self._db, configuration)
        return res_import_data, msg_import_data
    
    def validate_quality_rule(self, query: str) -> int | None:
        """
        Executes the query associated with a quality rule and returns the total errors.
        """
        prepare_query = query.format(schema=self._schema_name)
        query_valid, value_query = self._db.execute_sql_query(prepare_query)
        if not query_valid:
            return None
        else:
            return value_query[0][TAG_RESPONSE_SQL]

    def get_models_and_rules(self) -> dict:
        try:
            data = dict()
            for model in self._models:
                rule_items = list()

                try:
                    model_items = Modelo.objects.get(iliname=model)
                    model_serializer = ModeloSerializer(model_items).data

                    rules = Regla.objects.filter(modelo=model_serializer.get('id'))
                    rules_serializer = ReglaSerializer(rules, many=True).data

                    update_task_status(self._task_id, TaskStatus.IN_PROCESS)

                    for rule in rules_serializer:
                        total_errors = self.validate_quality_rule(rule['query'])

                        rule = QualityRule(
                            name=rule['nombre'],
                            description=rule['descripcion'],
                            # El resultado se establece según los siguientes parametros:
                            # 0 = No hay errores
                            # -1 = No existen datos para validar
                            # 1 ó más = Total de errores
                            result=1 if total_errors is None else total_errors,
                            error=True if total_errors is None else False
                        ).return_dict()

                        rule_items.append(rule)

                    model_name = model_serializer['nombre']
                    data[model_name] = {
                        "iliname": model_serializer['iliname'],
                        "rules": rule_items
                    }

                except Modelo.DoesNotExist:
                    update_task_status(self._task_id, TaskStatus.ERROR)
                    rule_items.append({"error": f"El modelo {model} no esta registrado."})
                    data[model] = {
                        "iliname": "",
                        "rules": rule_items
                    }

                except Regla.DoesNotExist:
                    update_task_status(self._task_id, TaskStatus.ERROR)
                    rule_items.append({"error": f"El modelo {model_name} no tiene reglas de calidad asociadas."})
                    data[model_name] = {
                        "iliname": model_serializer['iliname'],
                        "rules": rule_items
                    }

            return data
        except Exception as e:
            update_task_status(self._task_id, TaskStatus.ERROR)
            raise Exception(str(e))

    def create_report(self) -> str:
        data = self.get_models_and_rules()
        report_path = ReportManager.generate_basic_report(data, self._output_dir)
        return report_path

    def run(self) -> str:
        # Validation model
        model = self.validate_models()
        if len(model) < 1:
            raise Exception('El modelo del XTF no es válido.')

        # open connection
        self._db.open_connection()

        # Import schema
        is_schema, msg = self.import_schema()
        if not is_schema:
            raise Exception('Error al importar schema. ' + msg)

        # Import data
        is_data, msg = self.import_data()
        if not is_data:
            raise Exception('Error al importar data. ' + msg)

        # close connection
        self._db.close_connection()

        # Create report PDF
        dir_pdf = self.create_report()
        if os.path.exists(dir_pdf):
            update_task_status(self._task_id, TaskStatus.COMPLETED)
            return self._task_id
        else:
            update_task_status(self._task_id, TaskStatus.ERROR)
            raise Exception('Ocurrio un error al generar el archivo pdf, archivo no encontrado')
