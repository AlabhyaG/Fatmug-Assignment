from purchase_order.models import PurchaseOrderModel
from django.utils import timezone

utc = timezone.now()

def calculate_avg_response_time(self, purchase_order):
    """
    Calculate the average response time for a
    vendor based on the acknowledgment dates of their purchase orders.

    Parameters:
    - purchase_order (PurchaseOrderModel): The purchase order instance 
      for which the vendor's average response time is to be calculated.

    Operations:
    - Retrieves the vendor associated with the purchase order.
    - Calculates the response time in hours between the
      order date and the acknowledgment date.
    - Updates the vendor's average response time based on
      the new response time and the count of acknowledged orders.
    """

    vendor1 = purchase_order.vendor
    order_datetime = purchase_order.order_date
    ack_datetime = purchase_order.acknowledgment_date
    ack_orders_count = PurchaseOrderModel.objects.filter(
        acknowledgment_date__isnull=False
    ).count()
    response_time_seconds = ((ack_datetime - order_datetime).total_seconds()) / 3600
    avg_response = vendor1.average_response_time

    if avg_response is not None:
        new_avg_response = (
            avg_response * (ack_orders_count - 1) +
            response_time_seconds
        ) / ack_orders_count
        vendor1.average_response_time = new_avg_response
        vendor1.save()


def fulfillment_rate(self, purchase_order):
    """
    Calculate the fulfillment rate for a vendor 
    based on the completion status of their purchase orders.

    Parameters:
    - purchase_order (PurchaseOrderModel): The purchase order instance for 
      which the vendor's fulfillment rate is to be calculated.

    Operations:
    - Retrieves the vendor associated with the purchase order.
    - Counts the number of completed orders and the total 
      number of orders by the vendor.
    - Updates the vendor's fulfillment rate based on the ratio of 
      completed orders to total orders.
    """

    vendor_id = purchase_order.vendor
    completed_order_count = PurchaseOrderModel.objects.filter(
        vendor=vendor_id, status="completed"
    ).count()
    total_order_by_vendor_count = PurchaseOrderModel.objects.filter(
        vendor=vendor_id
    ).count()
    vendor_id.fulfillment_rate = completed_order_count / total_order_by_vendor_count
    vendor_id.save()


def on_time_delivery_rate(self, purchase_order, expected_delivery_date):
    """
    Calculate the on-time delivery rate for a vendor based on the delivery dates of their purchase orders.

    Parameters:
    - purchase_order (PurchaseOrderModel): The purchase order instance for which the vendor's on-time delivery rate is to be calculated.
    - expected_delivery_date (datetime): The expected delivery date for the purchase order.

    Operations:
    - Retrieves the vendor associated with the purchase order.
    - Checks if the current delivery date is on or before the expected delivery date.
    - Updates the vendor's on-time delivery rate based on whether the order was delivered on time.
    """

    vendor_id = purchase_order.vendor
    current_deliver_date = purchase_order.delivery_date
    prev_on_time_delivery_rate = vendor_id.on_time_delivery_rate
    total_completed_order = PurchaseOrderModel.objects.filter(
        vendor=vendor_id, status="completed"
    ).count()
    if current_deliver_date <= expected_delivery_date:
        new_on_time_delivery_rate = (
            prev_on_time_delivery_rate * (total_completed_order - 1) + 1
        ) / total_completed_order
        vendor_id.on_time_delivery_rate = new_on_time_delivery_rate
    vendor_id.save()


def quality_rating_avg(self, purchase_order,prev_quality_rate):
    """
    Calculate the average quality rating for a vendor based on the quality ratings of their purchase orders.

    Parameters:
    - purchase_order (PurchaseOrderModel): The purchase order instance for which the vendor's average quality rating is to be calculated.
    - prev_quality_rate (int): The previous average quality rating for the vendor.

    Operations:
    - Retrieves the vendor associated with the purchase order.
    - Calculates the new average quality rating based on the current quality rating and the previous average.
    - Updates the vendor's average quality rating.
    """

    vendor_id = purchase_order.vendor
    quality_rate = purchase_order.quality_rating
    prev_quality_avg = vendor_id.quality_rating_avg
    total_quality_rate = PurchaseOrderModel.objects.filter(
        vendor=vendor_id, quality_rating__isnull=False
    ).count()
    if quality_rate is not None and prev_quality_rate is None:
        new_total_quality_rate = quality_rate + prev_quality_avg * (total_quality_rate-1)
        vendor_id.quality_rating_avg = new_total_quality_rate / total_quality_rate
    elif quality_rate is not None and prev_quality_rate is not None:
        new_total_quality_rate=quality_rate + (
            prev_quality_avg * ( total_quality_rate) - prev_quality_rate
        )
        vendor_id.quality_rating_avg = new_total_quality_rate / total_quality_rate
    vendor_id.save()
