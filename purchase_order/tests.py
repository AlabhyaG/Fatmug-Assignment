import json
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.contrib.auth.models import User
from.models import PurchaseOrderModel
from.models import VendorModel
from.serializers import *


class BaseApiTest(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Generate JWT token for the test user
        self.access_token = AccessToken.for_user(self.user)

        # Authenticate the test client with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Create a vendor
        self.vendor1 = VendorModel.objects.create(
            name='Vendor 1', 
            vendor_code='VC001',
            contact_details="Vendor 1 contact",
            address="Vendor 1 address"
        )
        self.vendor2 = VendorModel.objects.create(
            name='Vendor 2', 
            vendor_code='VC002',
            contact_details="Vendor 2 contact details",
            address="Vendor 2 contact"
        )

        # Create a purchase order
        self.purchase_order1 = PurchaseOrderModel.objects.create(
            po_number='PO001',
            vendor=self.vendor1,
            order_date=timezone.make_aware(datetime(2024, 1, 1)),
            delivery_date=timezone.make_aware(datetime(2024, 2, 1)),
            items={'item': 'Test Item'},
            quantity=10,
            status='Pending',
            issue_date=timezone.now()
        )
        self.purchase_order2 = PurchaseOrderModel.objects.create(
            po_number='PO002',
            vendor=self.vendor1,
            order_date=timezone.make_aware(datetime(2024, 1, 1)),
            delivery_date=timezone.make_aware(datetime(2024, 3, 1)),
            items={'item': 'Test Item'},
            quantity=15,
            status='Pending',
            issue_date=timezone.now()
        )
        self.purchase_order3 = PurchaseOrderModel.objects.create(
            po_number='PO003',
            vendor=self.vendor1,
            order_date=timezone.make_aware(datetime(2024, 1, 1)),
            delivery_date=timezone.make_aware(datetime(2024, 3, 1)),
            items={'item': 'Test Item'},
            quantity=20,
            status='Pending',
            issue_date=timezone.now()
        )


class PurchaseOrderListAPIViewTest(BaseApiTest):
    def test_get_purchase_orders(self):
        # Test retrieving all purchase orders
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        # Test retrieving purchase orders by vendor
        response = self.client.get(
            '/api/purchase_orders/',
            {
                'vendor': self.vendor1.vendor_code
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(
            response.data[0]['vendor'], 
            self.vendor1.vendor_code
        )

    def test_get_purchase_orders_no_vendor(self):
        # Test retrieving purchase orders without specifying a vendor
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(
            response.status_code, 
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 3)

    def test_post_purchase_order(self):
        # Data for creating a new vendor
        new_purchase_order_data = {
            'po_number': 'PO004',
            'vendor': self.vendor1.vendor_code,
            'items': json.dumps({'item': 'Test Item'}),
            'quantity': 20,
        }
        # Send a POST request to create a new vendor
        response = self.client.post(
            '/api/purchase_orders/',
              new_purchase_order_data
              )

        # Assert that the status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the new vendor is created in the database
        # self.assertTrue(
        #     VendorModel.objects.filter(
        #         po_number='PO0004',  
        #     ).exists()
        # )
        new_purchase_order_data = {
            'po_number': 'PO004',
            'vendor': 'v00ddd',
            'items': json.dumps({'item': 'Test Item'}),
            'quantity': 20,
        }
        response = self.client.post(
            '/api/purchase_orders/',
              new_purchase_order_data
        )
        self.assertEqual(
            response.status_code, 
            status.HTTP_400_BAD_REQUEST
        )


class PurchaseOrderSpecificAPIViewTest(BaseApiTest):
    def test_get_specific_purchase_order(self):
        response1 = self.client.get('/api/purchase_orders/PO003/')
        response2 = self.client.get('/api/purchase_orders/PO002/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        # Update data for the purchase order
        updated_data = {
            'quality_rating': 4,  # Update quality rating
        }

        # Send a PUT request to update the purchase order
        response = self.client.put(
            f'/api/purchase_orders/
            {
                self.purchase_order1.po_number
            }/', updated_data
        )

        # Assert that the status code is 200 (OK) or 400 (Bad Request)
        self.assertIn(
            response.status_code, [
                status.HTTP_200_OK, 
                status.HTTP_400_BAD_REQUEST, 
                status.HTTP_405_METHOD_NOT_ALLOWED
                ]
            )

        # If the request is successful, assert that the
        # purchase order is updated with the new quality rating
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(
                response.data['quality_rating'], 
                updated_data['quality_rating']
            )

        # If the request fails due to a bad request, assert that the response contains errors
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            self.assertTrue('quality_rating' in response.data)

    # for testing delete api
    def test_delete_purchase_order(self):
        response = self.client.delete(
            f'/api/purchase_orders/{
                self.purchase_order1.po_number
            }/'
        )
        self.assertEqual(
            response.status_code, 
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(
            PurchaseOrderModel.objects.filter(
                po_number=self.purchase_order1.po_number
            ).exists()
        )

    def test_delete_invalid_vendor(self):
        response = self.client.delete(
            f'/api/vendors/{self.purchase_orders4.po_number}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_acknowledge_purchase_order(self):
        # Send a POST request to acknowledge the purchase order
        response = self.client.post(
            f'/api/purchase_orders/
            {
                self.purchase_order1.po_number
            }/acknowledge/'
        )

        # Assert that the status code is 200 (OK) or 404 (Not Found) or 405 (Method Not Allowed)
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND, 
            status.HTTP_405_METHOD_NOT_ALLOWED
            ]
        )

        # If the request is successful, assert that the purchase order is acknowledged
        if response.status_code == status.HTTP_200_OK:
            self.assertTrue(
                PurchaseOrderModel.objects.get(
                    po_number=self.purchase_order1.po_number
                ).acknowledgment_date
            )

        # If the request fails due to the purchase order not found, assert that the response contains an error message
        if response.status_code == status.HTTP_404_NOT_FOUND:
            self.assertEqual(
                response.data['error'], 
                'Purchase Order Not Found'
            )

        # If the request fails due to the purchase order already acknowledged, assert that the response contains a message
        if response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            self.assertEqual(
                response.data['message'],
                'Already Acknowledged'
            )
