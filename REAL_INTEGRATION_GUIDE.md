# ContextBridge - Real Integration Setup Guide

This guide will help you set up **REAL** enterprise data integrations instead of using demo data.

---

## 🎯 Overview

ContextBridge can connect to your actual enterprise data sources:
- **Slack** - Team conversations and channels
- **Jira** - Project tickets and issues
- **Google Drive** - Documents and files
- **Gmail** - Email communications
- **Meeting Transcripts** - Video call transcripts

---

## 🚀 Quick Start

### Step 1: Disable Demo Mode

Edit your `.env` file:
```env
DEMO_MODE=false
```

### Step 2: Configure Your Integrations

Follow the sections below for each service you want to connect.

---

## 📱 Slack Integration

### Prerequisites
- Slack workspace admin access
- Ability to create Slack apps

### Setup Steps

1. **Create a Slack App**
   - Go to https://api.slack.com/apps
   - Click "Create New App" → "From scratch"
   - Name: "ContextBridge"
   - Select your workspace

2. **Add Bot Token Scopes**
   - Go to "OAuth & Permissions"
   - Add these Bot Token Scopes:
     - `channels:history` - Read public channel messages
     - `channels:read` - View basic channel info
     - `groups:history` - Read private channel messages
     - `groups:read` - View private channels
     - `users:read` - View user information
     - `users:read.email` - View user email addresses

3. **Install App to Workspace**
   - Click "Install to Workspace"
   - Authorize the app
   - Copy the "Bot User OAuth Token" (starts with `xoxb-`)

4. **Add to .env**
   ```env
   SLACK_BOT_TOKEN=xoxb-your-actual-token-here
   ```

5. **Invite Bot to Channels**
   - In Slack, go to each channel you want to monitor
   - Type `/invite @ContextBridge`

### Test Connection
```bash
python -c "from ingestion.slack_connector import SlackConnector; from config import settings; connector = SlackConnector(demo_mode=False, slack_token=settings.SLACK_BOT_TOKEN); print(connector.get_channels())"
```

---

## 🎫 Jira Integration

### Prerequisites
- Jira Cloud account
- Jira admin or project admin access

### Setup Steps

1. **Create API Token**
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Name: "ContextBridge"
   - Copy the token (you won't see it again!)

2. **Get Your Jira URL**
   - Your Jira URL format: `https://your-domain.atlassian.net`
   - Example: `https://acme-corp.atlassian.net`

3. **Add to .env**
   ```env
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=your-email@company.com
   JIRA_API_TOKEN=your-api-token-here
   ```

### Test Connection
```bash
python -c "from ingestion.jira_connector import JiraConnector; from config import settings; connector = JiraConnector(demo_mode=False, jira_url=settings.JIRA_URL, jira_email=settings.JIRA_EMAIL, jira_api_token=settings.JIRA_API_TOKEN); print(connector.get_projects())"
```

---

## 📁 Google Drive Integration

### Prerequisites
- Google Workspace account
- Access to Google Cloud Console

### Setup Steps

#### Option A: Service Account (Recommended for Production)

1. **Create Service Account**
   - Go to https://console.cloud.google.com/
   - Create a new project or select existing
   - Enable "Google Drive API"
   - Go to "Credentials" → "Create Credentials" → "Service Account"
   - Name: "ContextBridge Drive"
   - Grant role: "Viewer"

2. **Create Key**
   - Click on the service account
   - Go to "Keys" tab
   - "Add Key" → "Create new key" → "JSON"
   - Download the JSON file

3. **Share Drive Folders**
   - In Google Drive, share folders with the service account email
   - Service account email format: `contextbridge-drive@your-project.iam.gserviceaccount.com`
   - Give "Viewer" permission

4. **Add to .env**
   ```env
   GOOGLE_DRIVE_SERVICE_ACCOUNT_PATH=./credentials/drive_service_account.json
   ```

#### Option B: OAuth2 (For Personal Use)

1. **Create OAuth2 Credentials**
   - Go to https://console.cloud.google.com/
   - Enable "Google Drive API"
   - Go to "Credentials" → "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Download the JSON file

2. **Run OAuth Flow**
   ```bash
   python scripts/setup_google_oauth.py --service drive
   ```
   - This will open a browser for authorization
   - Credentials will be saved automatically

3. **Add to .env**
   ```env
   GOOGLE_DRIVE_CREDENTIALS_PATH=./credentials/drive_credentials.json
   ```

### Test Connection
```bash
python -c "from ingestion.drive_connector import DriveConnector; from config import settings; connector = DriveConnector(demo_mode=False, service_account_path=settings.GOOGLE_DRIVE_SERVICE_ACCOUNT_PATH); print(len(connector.fetch_documents(limit=5)))"
```

---

## 📧 Gmail Integration

### Prerequisites
- Gmail account
- Access to Google Cloud Console

### Setup Steps

Follow the same steps as Google Drive, but:
- Enable "Gmail API" instead of Drive API
- Use scope: `https://www.googleapis.com/auth/gmail.readonly`
- Share email access with service account (if using service account)

**Add to .env:**
```env
GMAIL_SERVICE_ACCOUNT_PATH=./credentials/gmail_service_account.json
# OR
GMAIL_CREDENTIALS_PATH=./credentials/gmail_credentials.json
```

### Test Connection
```bash
python -c "from ingestion.email_connector import EmailConnector; from config import settings; connector = EmailConnector(demo_mode=False, service_account_path=settings.GMAIL_SERVICE_ACCOUNT_PATH); print(len(connector.fetch_emails(limit=5)))"
```

---

## 🔐 Security Best Practices

### 1. Credentials Storage
- **NEVER** commit credentials to Git
- Store credentials in `./credentials/` folder (already in .gitignore)
- Use environment variables for sensitive data

### 2. Access Control
- Use service accounts with minimal permissions
- Grant "Viewer" or "Read-only" access only
- Regularly rotate API tokens

### 3. Data Privacy
- ContextBridge processes data locally
- No data is sent to external services except:
  - Google Gemini API (for knowledge extraction)
  - ChromaDB (local vector store)

### 4. Audit Logging
- All data ingestion is logged
- Check `logs/contextbridge.log` for activity
- Monitor API usage in respective platforms

---

## 📊 Usage Examples

### Ingest from All Sources
```python
from config import settings
from ingestion.slack_connector import SlackConnector
from ingestion.jira_connector import JiraConnector
from ingestion.drive_connector import DriveConnector
from ingestion.email_connector import EmailConnector

# Initialize connectors
slack = SlackConnector(demo_mode=False, slack_token=settings.SLACK_BOT_TOKEN)
jira = JiraConnector(
    demo_mode=False,
    jira_url=settings.JIRA_URL,
    jira_email=settings.JIRA_EMAIL,
    jira_api_token=settings.JIRA_API_TOKEN
)
drive = DriveConnector(
    demo_mode=False,
    service_account_path=settings.GOOGLE_DRIVE_SERVICE_ACCOUNT_PATH
)
gmail = EmailConnector(
    demo_mode=False,
    service_account_path=settings.GMAIL_SERVICE_ACCOUNT_PATH
)

# Fetch data
slack_messages = slack.fetch_messages(limit=100)
jira_tickets = jira.fetch_tickets(limit=50)
drive_docs = drive.fetch_documents(limit=50)
emails = gmail.fetch_emails(limit=50)

print(f"Fetched: {len(slack_messages)} Slack messages")
print(f"Fetched: {len(jira_tickets)} Jira tickets")
print(f"Fetched: {len(drive_docs)} Drive documents")
print(f"Fetched: {len(emails)} emails")
```

### Ingest via API
```bash
# Ingest Slack messages
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "slack",
    "channel": "engineering",
    "limit": 100
  }'

# Ingest Jira tickets
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "jira",
    "project": "ENG",
    "limit": 50
  }'
```

---

## 🐛 Troubleshooting

### Slack Issues

**Error: "not_authed" or "invalid_auth"**
- Check your `SLACK_BOT_TOKEN` is correct
- Ensure token starts with `xoxb-`
- Verify app is installed to workspace

**Error: "channel_not_found"**
- Invite the bot to the channel: `/invite @ContextBridge`
- Check channel name is correct

### Jira Issues

**Error: "Unauthorized"**
- Verify `JIRA_EMAIL` matches the account that created the API token
- Check `JIRA_API_TOKEN` is correct
- Ensure `JIRA_URL` format is correct

**Error: "Project not found"**
- Check project key is correct (e.g., "ENG", not "Engineering")
- Verify you have access to the project

### Google Drive/Gmail Issues

**Error: "Insufficient permissions"**
- Check service account has access to folders/emails
- Verify API is enabled in Google Cloud Console
- Ensure correct scopes are granted

**Error: "File not found"**
- Service account must be explicitly shared the folder
- Check folder ID or name is correct

---

## 📈 Performance Tips

### 1. Batch Processing
- Fetch data in batches (100-500 items)
- Use pagination for large datasets
- Process during off-peak hours

### 2. Rate Limiting
- Slack: 1 request per second
- Jira: 10 requests per second (Cloud)
- Google APIs: 100 requests per 100 seconds

### 3. Caching
- ContextBridge caches processed knowledge
- Re-ingestion only processes new/updated items
- Use incremental sync for large datasets

---

## 🎯 Next Steps

1. **Test Each Integration** - Verify connections work
2. **Initial Ingestion** - Load historical data
3. **Schedule Sync** - Set up periodic data refresh
4. **Monitor Logs** - Check for errors and performance
5. **Optimize** - Adjust batch sizes and frequency

---

## 📞 Support

For issues or questions:
- Check logs: `logs/contextbridge.log`
- Review API documentation: http://localhost:8000/docs
- Test individual connectors with provided test commands

---

**ContextBridge** - Now with REAL enterprise data integration! 🚀
