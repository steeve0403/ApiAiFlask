import logging
from flask_mail import Message
from src.extensions import mail
from flask import current_app

logger = logging.getLogger(__name__)

# Send an email alert
def send_email_alert(subject, error_details):
    """
    Sends an email alert in case of a critical error.
    :param subject: The subject of the email.
    :param error_details: Details of the error to include in the email.
    """
    try:
        msg = Message(
            subject="Z-AI Alert: " + subject,
            recipients=[current_app.config['ADMIN_EMAIL']],  # Admin email configured in config.py
            body=f"Critical error detected:\n\n{error_details}"
        )
        mail.send(msg)
        logger.info(f"Email alert sent: {subject}")
    except Exception as e:
        logger.error(f"Error while sending email alert: {str(e)}")

# Send a Slack alert
# def send_slack_alert(message):
#     """
#     Sends an alert to a Slack channel via a webhook.
#     :param message: Message to send to Slack.
#     """
#     webhook_url = current_app.config.get('SLACK_WEBHOOK_URL')  # Configured in config.py
#     slack_data = {'text': f"Critical error: {message}"}
#
#     try:
#         response = requests.post(webhook_url, json=slack_data)
#         if response.status_code != 200:
#             logger.error(f"Error sending Slack message: {response.text}")
#         else:
#             logger.info("Slack alert sent successfully.")
#     except Exception as e:
#         logger.error(f"Error sending Slack message: {str(e)}")
