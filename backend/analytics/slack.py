import os
import requests
import logging

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_notification(message: str) -> bool:
    """
    Send a notification to Slack using an incoming webhook.
    """
    if not SLACK_WEBHOOK_URL:
        logging.warning("SLACK_WEBHOOK_URL is not set.")
        return False

    payload = {"text": message}

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        logging.info("Notification sent to Slack.")
        return True
    except requests.RequestException as e:
        logging.error(f"Failed to send Slack notification: {e}")
        return False
