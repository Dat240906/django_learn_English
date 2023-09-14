import os
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText

# Thông tin xác thực OAuth2
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
creds = None

def refresh_token():
    global creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

# Kiểm tra xem đã có thông tin xác thực OAuth2 hay chưa
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# Nếu chưa có hoặc hết hạn, thì yêu cầu xác thực mới
if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    refresh_token()  # Làm mới token sau khi xác thực

# Tạo service Gmail
service = build('gmail', 'v1', credentials=creds)

# Tạo email
message = MIMEText("nd")
message['to'] = "umbalaavc16@gmail.com"
message['subject'] = "Exam-Relax"

# Gửi email
raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
body = {'raw': raw_message}
service.users().messages().send(userId='me', body=body).execute()
