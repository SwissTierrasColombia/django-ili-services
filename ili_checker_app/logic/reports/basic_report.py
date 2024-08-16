from fpdf import FPDF
from pathlib import Path
import os
from ili_checker_app.config.enums_config import (
    QueryStatus,
    ReportResultColor,
    ReportMessageStatus
)
from ili_checker_app.config.general_config import (
    NAME_LOGO_POSITION_LEFT,
    NAME_LOGO_POSITION_RIGHT
)


class BasicReport(FPDF):
    base_dir = Path(__file__).resolve().parent.parent.parent
    assets_dir = os.path.join(base_dir, 'assets')
    image_left_logo_dir = os.path.join(assets_dir, NAME_LOGO_POSITION_LEFT)
    image_right_logo_dir = os.path.join(assets_dir, NAME_LOGO_POSITION_RIGHT)
    image_check_dir = os.path.join(assets_dir, 'check.png')
    image_warn_dir = os.path.join(assets_dir, 'warn.png')
    image_error_dir = os.path.join(assets_dir, 'error.png')

    def reset_styles(self) -> None:
        self.set_draw_color(0, 0, 0)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)

    def draw_cell_with_status_error(
            self,
            pdf: FPDF,
            color: tuple,
            message_status: str,
            icon_status: str,
            width_page: float,
            margin_cell: float
    ):
        pos_y_initial = pdf.get_y()

        pdf.set_draw_color(0, 115, 153)
        pdf.set_fill_color(0, 115, 153)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(margin_cell, pdf.get_y() + 2)

        self.reset_styles()
        pdf.set_draw_color(192, 192, 192)
        pdf.set_text_color(*color)
        pdf.set_xy(margin_cell, pdf.get_y() + 1)
        pdf.image(icon_status, pdf.get_x(), pdf.get_y(), 5, 5)
        pdf.set_xy(margin_cell + 8, pdf.get_y())
        self.reset_styles()
        pdf.set_font('Arial', '', 8)
        pdf.multi_cell(width_page - 21, 5, message_status, 0, 'L')

        # Barra estado lateral
        pdf.set_draw_color(*color)
        pdf.set_fill_color(*color)
        pos_y_final = pdf.get_y()
        pdf.set_xy(pdf.get_x(), pos_y_initial)
        pdf.cell(3, (pos_y_final - pos_y_initial) + 2, '', 1, 0, 'C', 1)
        self.reset_styles()

        # Marco
        pdf.set_draw_color(0, 115, 153)
        pdf.set_line_width(0.3)
        pdf.set_xy(pdf.get_x() + 2, pos_y_initial)
        pdf.cell(0, (pos_y_final - pos_y_initial) + 2, '', 1, 1, 'L', 0)
        pdf.ln(5)
        pdf.set_line_width(0.2)

    def draw_cell(
            self,
            pdf: FPDF,
            rule: dict,
            color: list,
            message_status: str,
            icon_status: str,
            width_page: float,
            margin_cell: float
    ):
        pos_y_initial = pdf.get_y()

        pdf.set_draw_color(0, 115, 153)
        pdf.set_fill_color(0, 115, 153)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(margin_cell, pdf.get_y() + 2)
        pdf.multi_cell(width_page - 13, 5, f'Regla: {rule["nombre"]}', True, 'L', True)
        pdf.set_xy(margin_cell, pdf.get_y() + 1)

        self.reset_styles()
        pdf.set_draw_color(192, 192, 192)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(width_page - 13, 5, 'Descripción:', 'LTR', 1, 'L')
        pdf.set_font('Arial', '', 8)
        pdf.set_xy(margin_cell, pdf.get_y())
        pdf.multi_cell(width_page - 13, 5, rule['descripcion'].replace("\n", " ").strip(), 'LRB', 'L')

        pdf.set_text_color(*color)
        pdf.set_xy(margin_cell, pdf.get_y() + 1)
        pdf.image(icon_status, pdf.get_x(), pdf.get_y(), 5, 5)
        pdf.set_xy(margin_cell + 8, pdf.get_y())
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(width_page - 21, 5, message_status, 0, 1, 'L')

        # Barra estado lateral
        pdf.set_draw_color(*color)
        pdf.set_fill_color(*color)
        pos_y_final = pdf.get_y()
        pdf.set_xy(pdf.get_x(), pos_y_initial)
        pdf.cell(3, (pos_y_final - pos_y_initial) + 2, '', 1, 0, 'C', 1)
        self.reset_styles()

        # Marco
        pdf.set_draw_color(0, 115, 153)
        pdf.set_line_width(0.3)
        pdf.set_xy(pdf.get_x() + 2, pos_y_initial)
        pdf.cell(0, (pos_y_final - pos_y_initial) + 2, '', 1, 1, 'L', 0)
        pdf.ln(5)
        pdf.set_line_width(0.2)

    # Calcula el alto de la celda creando un pdf temporal
    def get_multicell_height(self, rule):
        pdf = FPDF()
        pdf.add_page()
        width_page = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.set_font('Arial', 'B', 10)

        pos_initial_y = pdf.get_y()
        margin_cell = pdf.get_x() + 10
        color = ReportResultColor.SUCCESS.value
        message_status = ReportMessageStatus.SUCCESS.value
        icon_status = self.image_check_dir

        self.draw_cell(pdf, rule, color, message_status, icon_status, width_page=width_page, margin_cell=margin_cell)

        height = pdf.get_y() - pos_initial_y
        return height

    def get_multicell_height_with_status_error(self, message_status=ReportMessageStatus.SUCCESS.value):
        pdf = FPDF()
        pdf.add_page()
        width_page = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.set_font('Arial', 'B', 10)

        pos_initial_y = pdf.get_y()
        margin_cell = pdf.get_x() + 10
        color = ReportResultColor.SUCCESS.value
        icon_status = self.image_check_dir

        self.draw_cell_with_status_error(pdf, color, message_status, icon_status, width_page=width_page,
                                         margin_cell=margin_cell)

        height = pdf.get_y() - pos_initial_y
        return height

    def create_draw_warning_cell(self, message: ReportMessageStatus):
        width_page = self.w - self.l_margin - self.r_margin
        margin_cell = self.get_x() + 10
        color_text_and_bar = ReportResultColor.WARN.value
        message_status = message
        icon_status = self.image_warn_dir

        height_cell = self.get_multicell_height_with_status_error(message_status)
        height_free = self.h - self.get_y() - 15

        if height_cell > height_free:
            self.add_page()

        self.draw_cell_with_status_error(
            self,
            color_text_and_bar,
            message_status,
            icon_status,
            width_page,
            margin_cell,
        )

    def header(self):
        # Logo
        if os.path.isfile(self.image_left_logo_dir):
            self.image(self.image_left_logo_dir, 10, 8, 33)
        if os.path.isfile(self.image_right_logo_dir):
            self.image(self.image_right_logo_dir, 165, 12, 30)

        # Arial bold 15
        self.set_font('Arial', 'B', 15)

        # create margen in page
        self.set_line_width(0.5)
        self.set_draw_color(0, 115, 153)
        self.rect(5, 5, 200, 287)

        # Title
        self.multi_cell(0, 8, 'Reporte de validación de reglas\n de calidad del archivo XTF', 1, 'C')
        # Line break
        self.ln(10)

    def body(self, data: dict[str, dict[str, list[dict]]]):
        list_models = list()
        for name_model in data:
            list_models.append(data[name_model].get('iliname'))

            self.set_font('Arial', '', 10)
            width_page = self.w - self.l_margin - self.r_margin
            models = ", ".join(list_models)
            self.multi_cell(width_page, 5,
                            f"El archivo XTF suministrado es válido y está conformado por los siguientes modelos: {models}.\nA continuación, se presentan el resultado de cada una de las reglas de calidad definidas para cada uno de los modelos.")
            self.ln()

        for model in data:
            name_iliname = data.get(model).get('iliname')
            rules = data.get(model).get('rules')

            self.set_font('Arial', 'B', 10)
            self.cell(width_page, 5, f'{model}', 0, 1, 'C', False)
            self.cell(width_page, 5, f'{name_iliname}', 0, 1, 'C', False)
            self.ln()

            if len(rules) > 0:
                for rule in rules:
                    if (
                        rule.get('error')
                        and rule.get('resultado') is None
                    ):
                        # Se crea una celda cuando existe un error.
                        self.create_draw_warning_cell(message=rule.get('error'))
                    else:
                        result_model: int = rule.get('resultado')
                        height_cell = self.get_multicell_height(rule)
                        height_free = self.h - self.get_y() - 15

                        if height_cell > height_free:
                            self.add_page()

                        margin_cell = self.get_x() + 10

                        if result_model == QueryStatus.OK.value:
                            color_text_and_bar = ReportResultColor.SUCCESS.value
                            message_status = ReportMessageStatus.SUCCESS.value
                            icon_status = self.image_check_dir
                        elif result_model == QueryStatus.NO_DATA.value:
                            color_text_and_bar = ReportResultColor.WARN.value
                            message_status = ReportMessageStatus.WARN.value
                            icon_status = self.image_warn_dir
                        else:
                            color_text_and_bar = ReportResultColor.ERROR.value

                            if rule.get('error'):
                                message_status = ReportMessageStatus.QUERY_ERROR.value
                            else:
                                message_status = ReportMessageStatus.ERROR.value.format(
                                    result_model,
                                    "errores" if result_model > 1 else "error"
                                )

                            icon_status = self.image_error_dir

                        self.draw_cell(
                            self,
                            rule,
                            color_text_and_bar,
                            message_status,
                            icon_status,
                            width_page,
                            margin_cell,
                        )
            else:
                # Si no existen reglas, se genera un mensaje de advertencia
                self.create_draw_warning_cell(ReportMessageStatus.EMPTY_RULES.value)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
