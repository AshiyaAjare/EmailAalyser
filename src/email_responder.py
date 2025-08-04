from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

def send_email(service, to, subject, body_text, thread_id=None, message_id=None):
    message = MIMEText(body_text)
    message['to'] = to
    message['subject'] = subject

    if message_id:
        message['In-Reply-To'] = message_id
        message['References'] = message_id

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    send_message = {
        'raw': raw_message
    }
    
    if thread_id:
        send_message['threadId'] = thread_id

    sent = service.users().messages().send(
        userId="me", body=send_message).execute()

    print("📩 Replied to thread:", thread_id)
    return sent