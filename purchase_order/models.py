from django.db import models
from vendor.models import VendorModel

class PurchaseOrderModel(models.Model):
    """
    Represents a purchase order in the system.
    """
    po_number = models.CharField(
        max_length=50,
        unique=True,
        primary_key=True,
        help_text="Unique identifier for the purchase order."
    )
    vendor = models.ForeignKey(
        VendorModel,
        on_delete=models.CASCADE,
        help_text="Related vendor for the purchase order."
    )
    order_date = models.DateTimeField(
        help_text="Date when the purchase order was placed."
    )
    delivery_date = models.DateTimeField(
        help_text="Expected delivery date for the purchase order."
    )
    items = models.JSONField(
        help_text="Details of the items in the purchase order."
    )
    quantity = models.PositiveIntegerField(
        help_text="Quantity of items in the purchase order."
    )
    status = models.CharField(
        max_length=20,
        default="Pending",
        help_text="Current status of the purchase order."
    )
    quality_rating = models.FloatField(
        null=True,
        blank=True,
        help_text="Quality rating assigned to the purchase order."
    )
    issue_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date when the purchase order was issued."
    )
    acknowledgment_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date when the purchase order was acknowledged."
    )

    def __str__(self):
        """
        Returns a string representation of the purchase order.
        """
        return self.po_number
