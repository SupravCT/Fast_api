from fastapi_mail import FastMail,ConnectionConfig,MessageSchema
from src.config import settings

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)

mail=FastMail(config=mail_config)

mail.send_message(
    MessageSchema()
)

def create_message(recipents:list[str],
                   subject:str,
                   body:str,
                   subtype:str="html"):
    message=MessageSchema(
        recipents=recipents,
        subject=subject,
        body=body,
        subtype=subtype
        )