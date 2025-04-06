from flask_mail import Message
from flask import current_app
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail = current_app.extensions.get('mail')
        if mail:
            mail.send(msg)

def send_email(subject, recipients, body, sender=None):
    """
    Sends an email asynchronously.
    """
    app = current_app._get_current_object()
    sender = sender or app.config.get('MAIL_DEFAULT_SENDER')
    msg = Message(subject, sender=sender, recipients=recipients, body=body)
    Thread(target=send_async_email, args=(app, msg)).start()