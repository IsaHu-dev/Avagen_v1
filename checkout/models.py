from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    # Payment status choices

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending Payment"),
        ("processing", "Processing"),
        ("paid", "Paid"),
        ("failed", "Payment Failed"),
        ("cancelled", "Cancelled"),
    ]

    order_number = models.CharField(max_length=32, null=False, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    original_cart = models.TextField(null=False, blank=False, default="")
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=""
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
        help_text="Current payment status of the order",
    )
    payment_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time when payment was completed",
    )

    def _generate_order_number(self):
        """Generate a random, unique order number using timestamp and
        random characters"""
        import uuid
        from datetime import datetime

        # Get current timestamp and format it

        timestamp = datetime.now().strftime("%y%m%d")
        # Get first 4 characters of a UUID

        unique_id = uuid.uuid4().hex[:4].upper()

        return f"{timestamp}-{unique_id}"

    def update_total(self):
        """Update grand total based on line items"""
        self.order_total = sum(
            lineitem.lineitem_total for lineitem in self.lineitems.all()
        )
        self.grand_total = self.order_total
        self.save()

    def save(self, *args, **kwargs):
        """Override the original save method to set the order number"""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    def is_paid(self):
        """Check if the order has been paid"""
        return self.payment_status == "paid"

    def update_payment_status(self, status):
        """Update payment status"""
        from django.utils import timezone

        self.payment_status = status

        if status == "paid":
            self.payment_date = timezone.now()
        self.save()


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )
    product = models.ForeignKey(
        "products.DigitalProduct",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False
    )
    license_type = models.CharField(
        max_length=20, null=False, blank=False, default="personal"
    )

    def save(self, *args, **kwargs):
        """Override the original save method to set the lineitem total"""
        self.lineitem_total = (
            self.product.get_price_for_license(self.license_type)
            * self.quantity
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"License {self.product.model_number} on order "
            f"{self.order.order_number}"
        )
