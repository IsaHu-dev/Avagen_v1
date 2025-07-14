from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
import ssl


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
