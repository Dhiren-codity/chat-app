import smtplib
import requests
from email.mime.text import MIMEText

class EmailService:
    def __init__(self):
        self.smtp_host = 'smtp.gmail.com'
        self.smtp_port = 587

    def send_notification(self, to, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'noreply@chatapp.com'
        msg['To'] = to

        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        server.starttls()
        server.send_message(msg)
        server.quit()

        return True

class PushService:
    def __init__(self):
        self.api_url = 'https://fcm.googleapis.com/fcm/send'

    def send(self, user_id, title, body):
        token = self.get_device_token(user_id)

        payload = {
            'to': token,
            'notification': {
                'title': title,
                'body': body
            }
        }

        response = requests.post(self.api_url, json=payload)
        return response.status_code == 200

    def get_device_token(self, user_id):
        from models import UserDevice
        device = UserDevice.query.filter_by(user_id=user_id).first()
        return device.fcm_token if device else None
