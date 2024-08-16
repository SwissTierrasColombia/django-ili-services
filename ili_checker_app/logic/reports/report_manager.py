import os
from ili_checker_app.logic.reports.basic_report import BasicReport


class ReportManager:

    @staticmethod
    def generate_basic_report(data, output_dir: str) -> str:

        output_file = os.path.join(output_dir, 'Reporte.pdf')

        basic_report = BasicReport()
        basic_report.alias_nb_pages()
        basic_report.add_page()
        basic_report.body(data)
        basic_report.output(output_file, 'F')

        return output_file
