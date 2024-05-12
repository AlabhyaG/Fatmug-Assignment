from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import *


@receiver(post_save, sender=VendorModel)
def update_history(sender, instance, created, **kwargs):
    if not created:
        tracked_fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
        if any(instance.tracker.has_changed(field) for field in tracked_fields):
            HistoricalPerformanceModel.objects.create(
                vendor=instance,
                on_time_delivery_rate=instance.on_time_delivery_rate,
                quality_rating_avg=instance.quality_rating_avg,
                average_response_time=instance.average_response_time,
                fulfillment_rate=instance.fulfillment_rate
            )


# In VendorModel, add a setup to track changes

