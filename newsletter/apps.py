from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsletter'

    def ready(self):
        # Import signals to register them
        # pylint: disable=unused-import
        import newsletter.signals  # noqa
