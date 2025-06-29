from django.db import models
from django.utils import timezone


class NewsletterSubscriber(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
    ]

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def send_newsletter(self):
        """Send the newsletter to all active subscribers"""
        from django.core.mail import send_mail
        from django.conf import settings
        
        subscribers = NewsletterSubscriber.objects.filter(is_active=True)
        success_count = 0
        
        for subscriber in subscribers:
            try:
                # Send email
                send_mail(
                    subject=self.subject,
                    message=self.content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )
                success_count += 1
                
            except Exception as e:
                print(f"Failed to send newsletter to {subscriber.email}: {e}")
        
        # Update newsletter status
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.save()
        
        return success_count
