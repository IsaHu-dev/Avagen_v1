from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
import ssl
import logging

logger = logging.getLogger(__name__)


class CustomEmailBackend(SMTPBackend):
    def open(self):
        if self.connection:
            return False
        # Create SSL context

        context = ssl.create_default_context()

        # Create SMTP connection

        self.connection = self.connection_class(
            self.host, self.port, timeout=self.timeout
        )

        if self.use_tls:
            self.connection.starttls(context=context)
        if self.username:
            self.connection.login(self.username, self.password)
        return True

    def send_messages(self, email_messages):
        """Override send_messages to add logging"""
        if not email_messages:
            return 0
        try:
            result = super().send_messages(email_messages)
            logger.info(f"Successfully sent {result} email(s)")
            return result
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            raise
