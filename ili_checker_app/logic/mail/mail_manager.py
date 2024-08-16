import smtplib
import ssl
import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from ili_checker_app.config.general_config import EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_SUBJECT, PORT, SMTP


class MailManager:
    """
        class to send email with attachment
    """
    HTML_EMAIL_TEMPLATE = f"""
    <html>
        <body>
            <div style="border: 1px solid #ccc; border-radius: 10px; width:60%; height: auto; margin: 0 auto; padding: 30px; font-family: Arial, Helvetica, sans-serif;">
                <div style="background-color: #007399; color: white; padding: 20px">
                    <h1 style="text-align: center;">
                        Ili-Ckecker-Col
                    </h1>
                </div>
                <div>
                    <p>¡Hola! Usuario,</p>
                    <p style="text-align: center;">Tu tarea #12312 ha finalizado exitosamente. <br> Adjunto encontraras el resultado del procesamiento.</p>
                    <div style="text-align: center; margin: 25px 0;">
                        <a href="#" style="border: 1px solid black; background-color: black; padding: 15px 10px; border-radius: 5px; text-decoration: none;color: white;">¿Validar otro XTF?</a>
                    </div>
                </div>

                <hr style="width: 75%; color: #ccc;">
                <div>
                    <div style="display: flex; justify-content: center; align-items: center; gap: 5px 5px;">
                        <small>Desarrollado por:</small>
                        <a href="https://ceicol.com/">
                            Ceicol
                        </a>
                    </div>
                    <div style="text-align: center">
                        <small>
                            © 2024 CEICOL. Todos los derechos reservados.
                        </small>
                    </div>
                </div>
            </div> 
        </body>
    </html>
    """

    def __init__(self, task_id: str, email_to: str | list[str], file_dir: str | bytes | None = None) -> None:
        self.task_id = task_id
        self.file_dir = file_dir
        self.email_to = email_to

    def email_is_valid(self):
        expressions = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"

        return re.match(expressions, self.email_to) is not None
    
    def send_mail(self):

        def attach_file_to_email(email_message: MIMEMultipart, filename: bytes):
            #Leer el archivo en modo binario

            with open(filename, "rb") as file:
                file_attachment = MIMEApplication(file.read())

            #Añadir una cabecera y un nombre a los adjuntos
            file_attachment.add_header(
                "Content-Disposition",
                f"Attachment; filename= {self.task_id}.pdf",
            )
            #Añadir el file al mensaje
            email_message.attach(file_attachment)

        if not self.email_is_valid():
            raise Exception("Email is not valid")
        
        email_from = EMAIL_USERNAME
        email_password = EMAIL_PASSWORD

        email_message = MIMEMultipart()
        email_message['From'] = email_from
        email_message['To'] = self.email_to
        email_message['Subject'] = EMAIL_SUBJECT

        email_message.attach(MIMEText(self.HTML_EMAIL_TEMPLATE, "html"))

        if self.file_dir:
            attach_file_to_email(email_message, self.file_dir)

        email_string = email_message.as_string()
        email_context = ssl.create_default_context()

        try:
            with smtplib.SMTP(SMTP, port=PORT) as server:
                server.starttls(context=email_context)
                server.login(user=email_from, password=email_password)
                server.sendmail(from_addr=email_from, to_addrs=self.email_to, msg=email_string)
            print("Email enviado")
        except Exception as e:
            raise Exception(f"Error al enviar el email: {e}")
