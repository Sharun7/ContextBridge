"""
Test Real Enterprise Integrations
Verify that all connectors can initialize and connect
"""

import logging
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_slack():
    """Test Slack connector"""
    try:
        from ingestion.slack_connector import SlackConnector
        
        if settings.DEMO_MODE:
            logger.info("📱 Testing Slack (Demo Mode)...")
            connector = SlackConnector(demo_mode=True)
            channels = connector.get_channels()
            logger.info(f"✅ Slack Demo: Found {len(channels)} channels")
            return True
        else:
            if not settings.SLACK_BOT_TOKEN:
                logger.warning("⚠️  Slack: No token configured (set SLACK_BOT_TOKEN)")
                return False
            
            logger.info("📱 Testing Slack (Real API)...")
            connector = SlackConnector(
                demo_mode=False,
                slack_token=settings.SLACK_BOT_TOKEN
            )
            channels = connector.get_channels()
            logger.info(f"✅ Slack Real: Found {len(channels)} channels")
            return True
            
    except Exception as e:
        logger.error(f"❌ Slack test failed: {e}")
        return False


def test_jira():
    """Test Jira connector"""
    try:
        from ingestion.jira_connector import JiraConnector
        
        if settings.DEMO_MODE:
            logger.info("🎫 Testing Jira (Demo Mode)...")
            connector = JiraConnector(demo_mode=True)
            projects = connector.get_projects()
            logger.info(f"✅ Jira Demo: Found {len(projects)} projects")
            return True
        else:
            if not all([settings.JIRA_URL, settings.JIRA_EMAIL, settings.JIRA_API_TOKEN]):
                logger.warning("⚠️  Jira: Missing credentials (set JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN)")
                return False
            
            logger.info("🎫 Testing Jira (Real API)...")
            connector = JiraConnector(
                demo_mode=False,
                jira_url=settings.JIRA_URL,
                jira_email=settings.JIRA_EMAIL,
                jira_api_token=settings.JIRA_API_TOKEN
            )
            projects = connector.get_projects()
            logger.info(f"✅ Jira Real: Found {len(projects)} projects")
            return True
            
    except Exception as e:
        logger.error(f"❌ Jira test failed: {e}")
        return False


def test_google_drive():
    """Test Google Drive connector"""
    try:
        from ingestion.drive_connector import DriveConnector
        
        if settings.DEMO_MODE:
            logger.info("📁 Testing Google Drive (Demo Mode)...")
            connector = DriveConnector(demo_mode=True)
            docs = connector.fetch_documents(limit=5)
            logger.info(f"✅ Drive Demo: Found {len(docs)} documents")
            return True
        else:
            if not any([settings.GOOGLE_DRIVE_CREDENTIALS_PATH, settings.GOOGLE_DRIVE_SERVICE_ACCOUNT_PATH]):
                logger.warning("⚠️  Google Drive: No credentials configured")
                return False
            
            logger.info("📁 Testing Google Drive (Real API)...")
            connector = DriveConnector(
                demo_mode=False,
                credentials_path=settings.GOOGLE_DRIVE_CREDENTIALS_PATH,
                service_account_path=settings.GOOGLE_DRIVE_SERVICE_ACCOUNT_PATH
            )
            docs = connector.fetch_documents(limit=5)
            logger.info(f"✅ Drive Real: Found {len(docs)} documents")
            return True
            
    except Exception as e:
        logger.error(f"❌ Google Drive test failed: {e}")
        return False


def test_gmail():
    """Test Gmail connector"""
    try:
        from ingestion.email_connector import EmailConnector
        
        if settings.DEMO_MODE:
            logger.info("📧 Testing Gmail (Demo Mode)...")
            connector = EmailConnector(demo_mode=True)
            emails = connector.fetch_emails(limit=5)
            logger.info(f"✅ Gmail Demo: Found {len(emails)} emails")
            return True
        else:
            if not any([settings.GMAIL_CREDENTIALS_PATH, settings.GMAIL_SERVICE_ACCOUNT_PATH]):
                logger.warning("⚠️  Gmail: No credentials configured")
                return False
            
            logger.info("📧 Testing Gmail (Real API)...")
            connector = EmailConnector(
                demo_mode=False,
                credentials_path=settings.GMAIL_CREDENTIALS_PATH,
                service_account_path=settings.GMAIL_SERVICE_ACCOUNT_PATH
            )
            emails = connector.fetch_emails(limit=5)
            logger.info(f"✅ Gmail Real: Found {len(emails)} emails")
            return True
            
    except Exception as e:
        logger.error(f"❌ Gmail test failed: {e}")
        return False


def main():
    """Run all integration tests"""
    logger.info("=" * 60)
    logger.info("🧪 Testing ContextBridge Enterprise Integrations")
    logger.info("=" * 60)
    logger.info(f"Mode: {'DEMO' if settings.DEMO_MODE else 'PRODUCTION'}")
    logger.info("")
    
    results = {
        "Slack": test_slack(),
        "Jira": test_jira(),
        "Google Drive": test_google_drive(),
        "Gmail": test_gmail()
    }
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("📊 Test Results")
    logger.info("=" * 60)
    
    for service, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{service:20} {status}")
    
    total = len(results)
    passed = sum(results.values())
    logger.info("")
    logger.info(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All integrations working!")
    elif passed > 0:
        logger.info("⚠️  Some integrations need configuration")
        logger.info("📖 See REAL_INTEGRATION_GUIDE.md for setup instructions")
    else:
        logger.info("❌ No integrations configured")
        logger.info("📖 See REAL_INTEGRATION_GUIDE.md for setup instructions")
    
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
