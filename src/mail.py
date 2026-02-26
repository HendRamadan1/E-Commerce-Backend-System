from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType
from src.Config import config
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent


mail_config=ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD= config.MAIL_PASSWORD,
    MAIL_PORT=587,
    MAIL_FROM=config.MAIL_FROM,
    MAIL_SERVER= config.MAIL_SERVER,
    MAIL_FROM_NAME=config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR,'templetes') 
    

)

mail =FastMail(config=mail_config)
def create_message(recipients:list[str],body:str,subject:str,subtype:MessageType.html):
    message=MessageSchema(recipients=recipients,body=body,subject=subject,subtype=subtype)
    return message 
