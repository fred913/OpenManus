import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import config
from app.tool.base import BaseTool


class EmailSender(BaseTool):
    name: str = "email_sender"
    description: str = """Send an email to a specified recipient.
Use this tool when you need to send emails for notifications, alerts, or any other communication.
The tool accepts the recipient's email address, subject, and body of the email .
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "recipient_email": {
                "type": "string",
                "description": "(required) The recipient's email address.",
            },
            "subject": {
                "type": "string",
                "description": "(required) The subject of the email.",
            },
            "body": {
                "type": "string",
                "description": "(required) The body of the email.",
            },
        },
        "required": ["recipient_email", "subject", "body"],
    }

    async def execute(self, recipient_email: str, subject: str, body: str) -> str:
        """
        Send an email using Gmail's SMTP server.

        Args:
            recipient_email (str): The recipient's email address.
            subject (str): The subject of the email.
            body (str): The body of the email.

        Returns:
            str: A message indicating the result of the email sending operation.
        """

        try:
            sender_email = config.email_config.sender_email
            app_password = config.email_config.app_password

            # Check if email settings are None
            if not sender_email or not app_password:
                raise ValueError(
                    "Email configuration is invalid. "
                    "Please check if sender_email and app_password are properly set "
                    "in the [email.gmail] section of your config.toml file."
                )

            # Create a multipart message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()  # Secure the connection

                try:
                    server.login(sender_email, app_password)
                except smtplib.SMTPAuthenticationError:
                    raise ValueError(
                        "Gmail authentication failed. "
                        "Please verify your app_password is correct. "
                        "Make sure you have enabled 2-Step Verification and set up an App Password properly."
                    )

                # Send the email
                server.sendmail(sender_email, recipient_email, message.as_string())
                return f"Email successfully sent to {recipient_email}"

            except smtplib.SMTPException as smtp_error:
                raise ValueError(f"SMTP server error: {str(smtp_error)}")
            finally:
                server.quit()

        except Exception as e:
            return f"Failed to send email to {recipient_email}: {str(e)}"
