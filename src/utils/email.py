from flask_mail import Message

from ...model import mail
from ...config import cfg


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=cfg.MAIL_DEFAULT_SENDER,
    )
    mail.send(msg)