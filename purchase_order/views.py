from datetime import datetime, timedelta, date
from django.utils import timezone
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from.models import PurchaseOrderModel
from vendor.models import *
from.serializers import *
from.utils.performance_metric_function import *

# Constants
utc = timezone.now()

class PurchaseOrderListAPIView(APIView):
    """
    API View for listing and creating purchase orders.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):

        """
        Retrieve all purchase orders with a option to
        filter the orders by vendor.
        
        Parameters:
        - vendor (str): Optional. The ID of the vendor whose purchase orders to retrieve.
        
        Returns:
        - List of purchase orders.
        """

        try:
            vendor_id = request.query_params.get('vendor')
        except PurchaseOrderModel.DoesNotExist:
            return Response(
                {
                    'error':'Purchase order with this vendor does not exist'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        queryset = PurchaseOrderModel.objects.all()

        if vendor_id:
            queryset = queryset.filter(vendor=vendor_id)
        serializer = PurchaseOrderSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):

        """
        Create a new purchase order.
        
        Request Body:
        - vendor_id (int): The ID of the vendor.
        - order_details (dict): Details of the purchase order.
        
        Returns:
        - 201 Created: The purchase order was successfully created.
        - 400 Bad Request: The request was malformed.
        """

        serializer = PurchaseOrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderSpecificAPIView(APIView):
    """
    API View for fetching, updating, and deleting specific purchase orders.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):

        """
        Retrieve a specific purchase order by its PO number.
        
        Path Parameters:
        - pk (int): The PO number of the purchase order to retrieve.
        
        Returns:
        - 200 OK: The purchase order details.
        - 404 Not Found: The purchase order does not exist.
        """

        purchase_order = PurchaseOrderModel.objects.get(po_number=pk)
        serializer = PurchaseOrderCreateSerializer(purchase_order, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific purchase order by its PO number.
        
        Path Parameters:
        - pk (int): The PO number of the purchase order to update.
        
        Request Body:
        - quality_rating (int): Optional. The new quality rating for the purchase order.

        Real-time Update:
        - Triggers performance metric function to update the performance metrric of 
          vendors with change in  puchase orders
        - Quality rating average will be calculated everytime whenever update request is given
        - on time delivery and fulfillment rate is calculated when status change to complete
        
        Returns:
        - 200 OK: The purchase order was successfully updated.
        - 400 Bad Request: The request was malformed.
        - 405 Method Not Allowed: The order is not acknowledged yet.
        """
        try:
            purchase_order = PurchaseOrderModel.objects.get(po_number=pk)
        except PurchaseOrderModel.DoesNotExist:
            return Response(
                {
                    'error': 'Purchase Order not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if purchase_order.acknowledgment_date is None:
            return Response(
                {
                    'error': "The order is not acknowledged yet"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        
        # parameter needed for performance metric functions
        expected_delivery_date = purchase_order.delivery_date
        prev_quality_rating=purchase_order.quality_rating
        fl=False # for checking weather the status is already completed
        if 'quality_rating' in request.data:
            purchase_order.quality_rating = request.data['quality_rating']

        if(purchase_order.status != "completed"):
            purchase_order.status = "completed"
            purchase_order.delivery_date = timezone.localtime(utc)
            fl=True

        serializer = PurchaseOrderUpdateSerializer(
            purchase_order, 
            data=request.data, 
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            # Performace Metric Function
            if(fl==False): 
                # Only trigger when order status is changed
                on_time_delivery_rate(
                    self, 
                    purchase_order, 
                    expected_delivery_date
                )
                fulfillment_rate(
                    self, 
                    purchase_order
                )
            # Trigger everytime there is a update    
            quality_rating_avg(
                self, 
                purchase_order,
                prev_quality_rating
            )
            return Response(
                serializer.data, 
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        """
        Delete a specific purchase order by its PO number.
        
        Path Parameters:
        - pk (int): The PO number of the purchase order to delete.
        
        Returns:
        - 204 No Content: The purchase order was successfully deleted.
        - 404 Not Found: The purchase order does not exits
        """
        try:
            purchase_order = PurchaseOrderModel.objects.get(po_number=pk)
            purchase_order.delete()
            return Response(
                {
                    'message': 'Vendor deleted successfully'
                }, 
                status=status.HTTP_204_NO_CONTENT
            )
        except PurchaseOrderModel.DoesNotExist:
            return Response(
                {
                    'error': 'Vendor not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )


class AcknowledgePurchaseOrderApiView(APIView):
    """
    API View for acknowledging a purchase order.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        """
        Acknowledge a specific purchase order by its PO number.
        
        Path Parameters:
        - pk (int): The PO number of the purchase order to acknowledge.
        
        Real Time Update:
        - Calculate average response time whenever a order is acknowledged.
        Returns:
        - 200 OK: The purchase order was successfully acknowledged.
        - 404 Not Found: The purchase order does not exist.
        - 405 Method Not Allowed: The purchase order is already acknowledged.
        """

        try:
            purchase_order = PurchaseOrderModel.objects.get(po_number=pk)
        except PurchaseOrderModel.DoesNotExist:
            return Response(
                {
                    'error': 'Purchase Order Not Found'
                }, 
                status=status.HTTP_404_NOT_FOUND
            )

        if purchase_order.acknowledgment_date:
            return Response(
                {
                    'message': 'Already Acknowledged'
                }, 
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        
        purchase_order.acknowledgment_date = timezone.localtime(utc)
        purchase_order.save(update_fields=['acknowledgment_date'])

        calculate_avg_response_time(self, purchase_order)

        return Response(
            {
                'message': 'Purchase Order Acknowledged'
            }, 
            status=status.HTTP_200_OK
        )
