import json
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.contrib.auth.models import User
from .models import PurchaseOrderModel
from vendor.models import VendorModel
from .serializers import *

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
        response = self.client.get('/api/purchase_orders/', {'vendor': self.vendor1.vendor_code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['vendor'], self.vendor1.vendor_code)
    

    def test_get_purchase_orders_no_vendor(self):
        # Test retrieving purchase orders without specifying a vendor
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_post_purchase_order(self):
        # Data for creating a new vendor
        new_purchase_order_data = {
            'po_number':'PO004',
            'vendor':self.vendor1.vendor_code,
            'items': json.dumps({'item': 'Test Item'}),
            'quantity':20,
        }
        # Send a POST request to create a new vendor
        response = self.client.post('/api/purchase_orders/', new_purchase_order_data)

        # Assert that the status code is 201 (Created)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the new vendor is created in the database
        # self.assertTrue(
        #     VendorModel.objects.filter(
        #         po_number='PO0004',  
        #     ).exists()
        # )
        new_purchase_order_data = {
            'po_number':'PO004',
            'vendor':'v00ddd',
            'items': json.dumps({'item': 'Test Item'}),
            'quantity':20,
        }
        response = self.client.post('/api/purchase_orders/', new_purchase_order_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
class PurchaseOrderSpecificAPIViewTest(BaseApiTest):
    def test_get_specific_purchase_order(self):
        response1 = self.client.get('/api/purchase_orders/PO003/')
        response2 = self.client.get('/api/purchase_orders/PO002/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    # for testing delete api
    def test_delete_purchase_order(self):
        response=self.client.delete(
            f'/api/purchase_orders/{self.purchase_order1.po_number}/'
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
        response=self.client.delete(
            'f/api/vendors/{self.purchase_orders4.po_number}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )    

