import smtplib
import ssl
from email.headerregistry import Address
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader

from app import envs

uri = envs.EMAIL_URI
port = envs.EMAIL_PORT
login = envs.EMAIL_LOGIN
password = envs.EMAIL_PASSWORD

context = ssl.create_default_context()


def get_template(template: str, **kwargs) -> str:
    file_loader = FileSystemLoader(searchpath=envs.ROOT_DIR)
    env = Environment(loader=file_loader)

    template = env.get_template(template)

    output = template.render(site_domain=envs.HOST_NAME, **kwargs)
    return output


def send_email(to: str, subject: str, content: str) -> None:
    if envs.ENVIRONMENT == "dev":
        return

    email = EmailMessage()
    email["From"] = Address(
        display_name="No Reply (Gamers' Plane)",
        username="no-reply",
        domain="gamersplane.com",
    )
    email["To"] = to
    email["Subject"] = subject
    email.set_content(content, subtype="html")

    with smtplib.SMTP_SSL(uri, port, context=context) as server:
        server.login(login, password)
        server.send_message(email)
