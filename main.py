from dotenv import load_dotenv
import os
import boto3
import requests
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from msal import ConfidentialClientApplication
from flask import Flask, request, jsonify



load_dotenv()

GMAIL_CREDENTIALS_FILE = os.getenv('GMAIL_CREDENTIALS_FILE')
MS_CLIENT_ID = os.getenv('MS_CLIENT_ID')
MS_CLIENT_SECRET = os.getenv('MS_CLIENT_SECRET')
MS_TENANT_ID = os.getenv('MS_TENANT_ID')
AWS_REGION = 'us-east-1'
AZURE_CHATGPT_API_KEY = os.getenv('AZURE_CHATGPT_API_KEY')
AZURE_CHATGPT_ENDPOINT = 'https://api.openai.azure.com/v1/completions'


ses_client = boto3.client('ses', region_name=AWS_REGION)

app = Flask(__name__)


def fetch_gmail_emails():
    creds = Credentials.from_authorized_user_file(GMAIL_CREDENTIALS_FILE)
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        msg_details = service.users().messages().get(userId='me', id=msg['id']).execute()
        emails.append({
            'id': msg['id'],
            'snippet': msg_details.get('snippet'),
            'subject': msg_details['payload']['headers'][0]['value']
        })
    return emails


def fetch_outlook_emails():
    app = ConfidentialClientApplication(MS_CLIENT_ID, authority=f"https://login.microsoftonline.com/{MS_TENANT_ID}",
                                        client_credential=MS_CLIENT_SECRET)
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    access_token = result['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://graph.microsoft.com/v1.0/me/messages', headers=headers)
    return response.json().get('value', [])


def generate_email_response(prompt):
    response = requests.post(
        AZURE_CHATGPT_ENDPOINT,
        headers={"Authorization": f"Bearer {AZURE_CHATGPT_API_KEY}"},
        json={"prompt": prompt, "max_tokens": 150}
    )
    return response.json().get('choices')[0].get('text')


def send_email(to_address, subject, body):
    response = ses_client.send_email(
        Source='hello@Vomychat.atlassoit.co',
        Destination={'ToAddresses': [to_address]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
    return response


def mark_as_not_spam(email_id):
    creds = Credentials.from_authorized_user_file(GMAIL_CREDENTIALS_FILE)
    service = build('gmail', 'v1', credentials=creds)
    service.users().messages().modify(
        userId='me',
        id=email_id,
        body={'removeLabelIds': ['SPAM']}
    ).execute()
    return f"Email {email_id} removed from spam."


@app.route('/fetch_emails', methods=['GET'])
def fetch_emails():
    gmail_emails = fetch_gmail_emails()
    outlook_emails = fetch_outlook_emails()
    return jsonify({'gmail': gmail_emails, 'outlook': outlook_emails})

@app.route('/generate_response', methods=['POST'])
def generate_response():
    data = request.json
    prompt = data.get('prompt')
    response = generate_email_response(prompt)
    return jsonify({'response': response})

@app.route('/send_email', methods=['POST'])
def send_email_endpoint():
    data = request.json
    to_address = data['to']
    subject = data['subject']
    body = data['body']
    response = send_email(to_address, subject, body)
    return jsonify({'status': 'Email sent', 'response': response})

@app.route('/remove_spam', methods=['POST'])
def remove_spam():
    data = request.json
    email_id = data['email_id']
    response = mark_as_not_spam(email_id)
    return jsonify({'status': response})

if __name__ == '__main__':
    app.run(debug=True)
