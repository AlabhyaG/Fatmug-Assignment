from django.db import models
from django.contrib.auth.models import User
from model_utils import FieldTracker
class VendorModel(models.Model):
    """
    Represents a vendor profile in the system.
    """
    name = models.CharField(
        max_length=255,
        help_text="Name of the vendor."
    )
    contact_details = models.TextField(
        blank=False,
        null=False,
        help_text="Contact details of the vendor."
    )
    address = models.TextField(
        blank=False,
        null=False,
        help_text="Address of the vendor."
    )
    vendor_code = models.CharField(
        max_length=9,
        unique=True,
        primary_key=True,
        help_text="Unique code for the vendor."
    )
    on_time_delivery_rate = models.FloatField(
        blank=True,
        null=True,
        default=0.0,
        help_text="On-time delivery rate of the vendor."
    )
    quality_rating_avg = models.FloatField(
        blank=True,
        null=True,
        default=0.0,
        help_text="Average quality rating of the vendor."
    )
    average_response_time = models.FloatField(
        blank=True,
        null=True,
        default=0.0,
        help_text="Average response time of the vendor."
    )
    fulfillment_rate = models.FloatField(
        blank=True,
        null=True,
        default=0.0,
        help_text="Fulfillment rate of the vendor."
    )
    tracker = FieldTracker(
        fields=[
            'on_time_delivery_rate',
            'quality_rating_avg',
            'average_response_time',
            'fulfillment_rate'
            ]
        )

    def __str__(self):
        """
        Returns a string representation of the vendor.
        """
        return self.name

class HistoricalPerformanceModel(models.Model):
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.vendor) + '| Date: ' + str(self.date)


