from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from .models import VendorModel
from .serializers import VendorListSerializer

class BaseAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Generate JWT token for the test user
        self.access_token = AccessToken.for_user(self.user)

        # Authenticate the test client with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Create sample vendor data
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

class AllVendorAPIViewTest(BaseAPITestCase):
    
# to test get request for retrieving all vendor info
    def test_get_vendors(self):
        # Send a GET request to the endpoint
        response = self.client.get('/api/vendors/')

        # Assert that the status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data contains the expected vendors
        expected_data = [
            {'name': 'Vendor 1', 'vendor_code': 'VC001'},
            {'name': 'Vendor 2', 'vendor_code': 'VC002'}
        ]
        self.assertEqual(response.data, expected_data)
# to test post request 
    def test_post_vendor(self):
        # Data for creating a new vendor
        new_vendor_data = {
            'name': 'New Vendor',
            'vendor_code': 'NEW001',
            'contact_details':'New Vendor Details',
            'address':'New Vendor address'
        }
        # Send a POST request to create a new vendor
        response = self.client.post('/api/vendors/', new_vendor_data)

        # Assert that the status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the new vendor is created in the database
        self.assertTrue(
            VendorModel.objects.filter(
                name='New Vendor', 
                vendor_code='NEW001',
                contact_details='New Vendor Details',
                address='New Vendor address'

            ).exists()
        )

    def test_create_incomplete_vendor(self):
    # Define incomplete vendor data
        new_vendor_data = {
            'name': 'New Vendor',
            'contact_details': 'New Vendor Details',
        }

    # Send a POST request to create an incomplete vendor
        response = self.client.post('/api/vendors/', new_vendor_data)

    # Assert that the status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SpecificVendorViewTest(BaseAPITestCase):
        
# for testing get request for retrieving a specific user
    def test_get_specific_vendor(self):
        response1 = self.client.get('/api/vendors/VC001/')
        response2 = self.client.get('/api/vendors/VC002/')
        response3 = self.client.get('/api/vendors/VC003/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_404_NOT_FOUND)

        # Assert that the response data contains the expected vendors
        expected_data = [
            {'name': 'Vendor 1', 'vendor_code': 'VC001'},
            {'name': 'Vendor 2', 'vendor_code': 'VC002'}
        ]
        def test_get_specific_vendor(self):
            response1 = self.client.get('/api/vendors/VC001')
            response2 = self.client.get('/api/vendors/VC002')

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    # Assert that the response data contains the expected vendors
        expected_data = [
            {'name': 'Vendor 1', 'vendor_code': 'VC001'},
            {'name': 'Vendor 2', 'vendor_code': 'VC002'}
        ]
        self.assertEqual(
            response1.data['name'], 
            expected_data[0]['name']
        )
        self.assertEqual(
            response1.data['vendor_code'], 
            expected_data[0]['vendor_code']
        )
        self.assertEqual(
            response2.data['name'], 
            expected_data[1]['name']
        )
        self.assertEqual(
            response2.data['vendor_code'], 
            expected_data[1]['vendor_code']
        )
    

class UpdateVendorTestCase(BaseAPITestCase):
    
    def test_update_vendor_success(self):
        # Data for updating the vendor
        update_data = {
            'name': 'Updated Vendor',
            'contact_details': 'Updated contact info',
            
        }

        # Send a PUT request to update the vendor
        response = self.client.put(
            f'/api/vendors/{self.vendor1.vendor_code}/', 
            update_data
        )

        # Assert that the status code is 200 (OK)
        self.assertEqual(
            response.status_code, 
            status.HTTP_200_OK
        )

        # Assert that the vendor was updated correctly
        updated_vendor = VendorModel.objects.get(vendor_code=self.vendor1.vendor_code)
        self.assertEqual(
            updated_vendor.name, 
            update_data['name']
        )
        self.assertEqual(
            updated_vendor.contact_details, 
            update_data['contact_details']
        )
        

    def test_update_vendor_invalid_data(self):
        # Invalid data for updating the vendor (missing required fields)
        empty_data = {
            
        }
        invalid_data={
            'vendor_code':'12v'
        }
        # Send a PUT request with invalid data
        updated_vendor = VendorModel.objects.get(vendor_code=self.vendor1.vendor_code)
        response = self.client.put(f'/api/vendors/{self.vendor1.vendor_code}/', invalid_data)
        self.assertNotEqual(
            updated_vendor.vendor_code,invalid_data['vendor_code']
        )

        # Assert that the status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_vendor_not_found(self):
        # Send a PUT request with a non-existing vendor code
        response = self.client.put('/api/vendors/INVALID_CODE/', {})

        # Assert that the status code is 404 (Not Found)
        self.assertEqual(
            response.status_code, 
            status.HTTP_404_NOT_FOUND
        )
    
class DeleteVendorApiTest(BaseAPITestCase):


    def test_delete_vendor(self):
        response=self.client.delete(
            f'/api/vendors/{self.vendor1.vendor_code}/'
        )
        self.assertEqual(
            response.status_code, 
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(
            VendorModel.objects.filter(
                vendor_code=self.vendor1.vendor_code
                ).exists()
            )
    def test_delete_invalid_vendor(self):
        response=self.client.delete(
            'f/api/vendors/{self.vendor4.vendor_code}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

class PerformanceVendorApiTest(BaseAPITestCase):
    def test_performance_vendor(self):
        response=self.client.get(
            f'/api/vendors/{self.vendor1.vendor_code}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
    def test_performance_invalid_vendor(self):
        response=self.client.delete(
            'f/api/vendors/{self.vendor4.vendor_code}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )