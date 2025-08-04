import os
import base64
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.send']



def get_email_service():
    creds = None
    token_path = 'token.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


# def get_latest_trainer_email(service, hr_email):
#     query = 'subject:("Training Request" OR "Session Request" OR "Trainer Proposal")'
#     results = service.users().messages().list(userId='me', labelIds=['INBOX'], q=query, maxResults=1).execute()
#     messages = results.get('messages', [])

#     if not messages:
#         return None, None

#     msg_id = messages[0]['id']
#     msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

#     headers = msg['payload'].get('headers', [])
    
#     # Extract sender email cleanly
#     from_header = next((h['value'] for h in headers if h['name'] == 'From'), None)
#     match = re.search(r'<(.+?)>', from_header)
#     from_email = match.group(1) if match else from_header

#     subject = next((h['value'] for h in headers if h['name'] == 'Subject'), None)

#     # Decode body
#     parts = msg['payload'].get('parts', [])
#     body = ""
#     if parts:
#         for part in parts:
#             if part['mimeType'] == 'text/plain':
#                 data = part['body']['data']
#                 body = base64.urlsafe_b64decode(data).decode('utf-8')
#                 break
#     else:
#         body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')

#     thread_id = msg.get('threadId')
#     message_id = next((h['value'] for h in headers if h['name'] == 'Message-ID'), None)
#     return from_email, body, thread_id, message_id

def get_latest_unprocessed_email(service, hr_email, label_name="EmailAnalyser/Processed"):
    query = f'-label:"{label_name}" subject:"Training Request"'
    results = service.users().messages().list(userId='me', q=query, labelIds=['INBOX'], maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        return None, None, None, None, None

    msg_id = messages[0]['id']
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

    headers = msg['payload'].get('headers', [])
    subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), None)
    from_email = next((h['value'] for h in headers if h['name'].lower() == 'from'), None)
    message_id = next((h['value'] for h in headers if h['name'].lower() == 'message-id'), None)
    thread_id = msg.get('threadId')

    # Decode message
    parts = msg['payload'].get('parts', [])
    body = ""
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
                break
    else:
        body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')

    return from_email, body, thread_id, message_id, msg_id


def create_label_if_not_exists(service, label_name="EmailAnalyser/Processed"):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    if any(l['name'] == label_name for l in labels):
        return
    label_body = {
        'name': label_name,
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show'
    }
    service.users().labels().create(userId='me', body=label_body).execute()

def mark_as_processed(service, msg_id, label_name="EmailAnalyser/Processed"):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    label_id = next((l['id'] for l in labels if l['name'] == label_name), None)
    if label_id:
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'addLabelIds': [label_id]}
        ).execute()


