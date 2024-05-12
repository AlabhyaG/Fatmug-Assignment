from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from.serializers import *
from.models import VendorModel

class AllVendorAPIView(APIView):
    """
    API View for listing and creating vendors.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of vendors.
        
        Returns:
        - 200 OK: A list of vendors with vendor code and vendor name.
        """
        try:
            vendors = VendorModel.objects.all()
        except VendorModel.DoesNotExist:
            return Response(
                {
                    'error':'Vendor Not Found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
        serializer = VendorListSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new vendor.
        
        Request Body:
        - vendor_name (str): The name of the vendor.
        - contact_info (str): Contact information of the vendor.
        - address(str): Address of the vendor
        - vendor_code (str): Vendor code of the vendor
        
        Returns:
        - 201 Created: The vendor was successfully created.
        - 400 Bad Request: The request was malformed.
        """
        serializer = VendorSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

class SpecificVendorAPIView(APIView):
   
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieve a specific vendor by its vendor code.
        
        Path Parameters:
        - pk (str): The vendor code of the vendor to retrieve.
        
        Returns:
        - 200 OK: The vendor details which include:
        vendor name,vendor code, address, and contact_details.
        - 404 Not Found: The vendor does not exist.
        """
        try:
            vendor = VendorModel.objects.get(vendor_code=pk)
        except VendorModel.DoesNotExist:
            return Response(
                {
                    'error':'Vendor Not Found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
        serializer = VendorSerializers(vendor, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific vendor by its vendor code.
        
        Path Parameters:
        - pk (str): The vendor code of the vendor to update.
        
        Request Body:
        - vendor_name (str): Optional. The new name of the vendor.
        - contact_info (str): Optional. The new contact information of the vendor.
        
        Returns:
        - 200 OK: The vendor was successfully updated.
        - 400 Bad Request: The request was malformed.
        - 404 Not Found: The vendor does not exist.
        """
        try:
            vendor = VendorModel.objects.get(vendor_code=pk)
        except VendorModel.DoesNotExist:
            return Response(
                {
                    'error': 'Vendor not found'
                }, 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UpdateVendorSerializer(
            vendor, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk, format=None):
        """
        Delete a specific vendor by its vendor code.
        
        Path Parameters:
        - pk (str): The vendor code of the vendor to delete.
        
        Returns:
        - 204 No Content: The vendor was successfully deleted.
        - 404 Not Found: The vendor does not exist.
        """
        try:
            vendor = VendorModel.objects.get(vendor_code=pk)
            vendor.delete()
            return Response(
                {
                    'message': 'Vendor deleted successfully'
                }, 
                status=status.HTTP_204_NO_CONTENT
            )
        except VendorModel.DoesNotExist:
            return Response(
                {
                    'error': 'Vendor not found'
                }, 
                status=status.HTTP_404_NOT_FOUND
            )

class PerformanceVendorApiView(APIView):
    """
    API View for retrieving performance metrics of a specific vendor.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieve performance metrics of a specific vendor by its vendor code.
        
        Path Parameters:
        - pk (str): The vendor code of the vendor to fetch performance metrics for.
        
        Returns:
        - 200 OK: The performance metrics of the vendor.
        - Gives : On time delivery rate, Fulfillment rate, 
                  avg response time and quality avg
        """
        try:
            performance_object = VendorModel.objects.get(vendor_code=pk)
        except VendorModel.DoesNotExist:
            return Response(
                {
                    'error': 'Vendor not found'
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = VendorPerformanceSerializer(performance_object, many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
