import logging

logger = logging.getLogger(__name__)

class EmailService:
    def send_email(self, to_email, subject, body):
        """
        Mock sending email. Logs the email.
        """
        logger.info(f"Sending Email to {to_email}: {subject}")
        print(f"--- EMAIL SENT to {to_email} ---\nSubject: {subject}\nBody:\n{body}\n-------------------------------")
        return True
