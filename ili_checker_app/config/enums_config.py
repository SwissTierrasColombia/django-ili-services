from enum import Enum


class QueryStatus(Enum):
    OK = 0
    NO_DATA = -1
    ERROR = 1


class ReportResultColor(Enum):
    SUCCESS = (124, 179, 66)
    WARN = (253, 216, 53)
    ERROR = (239, 83, 80)


class ReportMessageStatus(Enum):
    SUCCESS = "No hay errores"
    WARN = "No hay datos para validar"
    ERROR = "Se ha identificado {} {}"
    QUERY_ERROR = "La consulta ejecutada no es válida, consulte al administrador del sistema"
    EMPTY_RULES = ("Este modelo de datos no cuenta con reglas de calidad definidas para ser evaluadas. Sí considera "
                   "esto un error, puede consultar con el administrador del sistema.")


class TaskStatus(Enum):
    COMPLETED = 'Completado'
    IN_PROCESS = 'En proceso'
    PENDING = 'Pendiente'
    ERROR = 'Error'
