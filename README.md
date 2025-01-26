# Email Control Program

## Purpose

The Email Control Program is designed to:

1. **Manage over 100k emails**: Read, reply, and send emails effectively across Gmail and Outlook.
2. **Automate Responses**: Use Azure OpenAI ChatGPT API to generate email replies.
3. **Send Emails**: Utilize AWS Simple Email Service (SES) for sending emails with good IP reputation management.
4. **Organize Emails**: Pull emails out of spam or promotional folders for better management.

---

## Prerequisites

### Technologies Used
1. **AWS SES**: For sending emails.
2. **Azure ChatGPT API**: For generating automated email responses.
3. **Google Gmail API**: For Gmail integration.
4. **Microsoft Graph API**: For Outlook integration.
5. **Flask**: For building the RESTful API endpoints.
6. **Python 3.9+**: Programming language.

### Required Credentials
You will need:

1. **AWS SES** credentials:
   - `AWS_REGION`
   - Access and secret keys.

2. **Azure ChatGPT API**:
   - `AZURE_CHATGPT_API_KEY`
   - Endpoint URL.

3. **Google Gmail API**:
   - A valid OAuth 2.0 credentials file (`credentials.json`).

4. **Microsoft Graph API**:
   - `MS_CLIENT_ID`
   - `MS_CLIENT_SECRET`
   - `MS_TENANT_ID`.

---

## Installation

### 1. Clone the Repository
Clone the code to your local system:
```bash
git clone <repository_url>
cd email_control_program
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root and add the following:
```env
GMAIL_CREDENTIALS_FILE=path/to/gmail/credentials.json
MS_CLIENT_ID=your-microsoft-client-id
MS_CLIENT_SECRET=your-microsoft-client-secret
MS_TENANT_ID=your-microsoft-tenant-id
AWS_REGION=us-east-1
AZURE_CHATGPT_API_KEY=your-azure-chatgpt-api-key
AZURE_CHATGPT_ENDPOINT=https://api.openai.azure.com/v1/completions
```

Replace the placeholders with your actual credentials.

### 5. Run the Application
Start the Flask app:
```bash
python app.py
```

The application will run on `http://127.0.0.1:5000`.

---

## API Endpoints

### 1. Fetch Emails
**GET /fetch_emails**
- Fetches emails from Gmail and Outlook.
- **Response**: List of emails.

### 2. Generate Email Response
**POST /generate_response**
- Input: JSON with the email's content as `prompt`.
- **Response**: AI-generated reply.

Example:
```json
{
  "prompt": "Hello, can you provide the latest update on the project?"
}
```

### 3. Send Email
**POST /send_email**
- Input: JSON with `to`, `subject`, and `body`.
- Sends an email via AWS SES.

Example:
```json
{
  "to": "recipient@example.com",
  "subject": "Status Update",
  "body": "Here is the update you requested."
}
```

### 4. Remove Email from Spam
**POST /remove_spam**
- Input: JSON with `email_id`.
- Removes an email from the Gmail spam folder.

Example:
```json
{
  "email_id": "12345abc"
}
```

---

## Features

1. **Scalable Email Management**:
   - Handles large-scale email operations.
2. **Automated Responses**:
   - Uses AI to craft replies, saving time and effort.
3. **Efficient Email Sending**:
   - Maintains good IP reputation with AWS SES.
4. **Organized Inbox**:
   - Moves emails out of spam to ensure no important email is missed.

---

## Security Notes
- Store sensitive credentials in environment variables.
- Limit access to your API endpoints by implementing authentication mechanisms.
- Regularly rotate API keys and credentials to minimize risks.

---

## Future Enhancements
1. Add OAuth authentication for secure user access.
2. Enable multi-language support for email replies.
3. Integrate additional email providers like Yahoo.

---

## Troubleshooting

### Common Issues
1. **Gmail API Authentication Error**:
   - Ensure `credentials.json` is properly configured.
   - Check Gmail API quota limits.

2. **AWS SES Email Not Delivered**:
   - Verify the email address is verified in AWS SES.
   - Check AWS SES sending limits.

3. **Azure ChatGPT API Issues**:
   - Ensure the API key is valid.
   - Confirm the endpoint URL is correct.

For further assistance, refer to the documentation of the respective APIs or raise an issue in the repository.

---

## License
This project is licensed under the [MIT License](LICENSE).

