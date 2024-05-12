# Project Setup Guide

## Introduction

Welcome to our project This guide will walk you through setting up your development environment, installing dependencies, and running the Django development server.

## Setting Up Your Virtual Environment

Before you start, you'll need to set up a virtual environment to keep your project's dependencies isolated from other Python projects on your system.

### Step 1: Install Virtualenv

If you don't already have `virtualenv` installed, you can install it using pip:
```
pip install virtualenv
```


### Step 2: Create a Virtual Environment

Navigate to your project directory and create a new virtual environment. Replace `venv` with whatever you'd like to name your virtual environment:

```
cd path/to/your/project virtualenv venv
```

### Step 3: Activate the Virtual Environment

Activate the virtual environment. On Windows, run:
```
.\venv\Scripts\activate
```

On macOS and Linux, run:
bash 
```
source venv/bin/activate
```

Your terminal prompt should change to indicate that the virtual environment is active.


## Installing Dependencies

With your virtual environment activated, you can now install the project's dependencies. These are listed in the `requirements.txt` file.

### Step 1: Install Dependencies

Run the following command to install all dependencies listed in `requirements.txt`:

```pip install -r requirements.txt```


This command reads the `requirements.txt` file and installs all the packages listed there.

## Running the Django Development Server

Once your dependencies are installed, you can start the Django development server to begin working on your project.

### Step 1: Start the Django Development Server

Run the following command to start the Django development server:
```
python manage.py runserver
```

By default, the server will start on port 8000. You can access your project by opening a web browser and navigating to `http://127.0.0.1:8000`.

## Running Test Suite

There are two test.py files for both apps that is Vendor App and Purchase Orders App, to run those follow the following step:
### Step 1: Go to the project folder

### Step 2: Go to the vendor_management_system by
```
cd vendor_management_system
```

### Step 3: In terminal type the command:
``` 
python manage.py test
```

This will run both the test suites
# Purchase Order Api Endpoint Usage Details:
# Purchase Order Management API Documentation

This document provides an overview of the Purchase Order Management API, detailing how to interact with purchase orders through various endpoints. The API is designed to facilitate the creation, retrieval, updating, and deletion of purchase orders, along with acknowledging purchase orders and calculating performance metrics.

## Base URL

All API requests should be directed to the base URL of your Django application.

## Authentication

All API endpoints require authentication. Use the `Authorization` header with a valid token to authenticate your requests.

## Purchase Order List API

### GET /purchase-orders/

**Description:** Retrieves a list of purchase orders. Optionally filters orders by vendor.

**Parameters:**

- `vendor` (Optional): The ID of the vendor whose purchase orders to retrieve.

**Returns:**

- 200 OK: A list of purchase orders.
- 400 Bad Request: The request was malformed.
- 404 Not Found: Purchase order with the specified vendor does not exist.

### POST /purchase-orders/

**Description:** Creates a new purchase order.

**Request Body:**

- `vendor_id`: The ID of the vendor.
- `order_details`: Details of the purchase order.

**Returns:**

- 201 Created: The purchase order was successfully created.
- 400 Bad Request: The request was malformed.

## Specific Purchase Order API

### GET /purchase-orders/{pk}/

**Description:** Retrieves a specific purchase order by its PO number.

**Path Parameters:**

- `pk`: The PO number of the purchase order to retrieve.

**Returns:**

- 200 OK: The purchase order details.
- 404 Not Found: The purchase order does not exist.

### PUT /purchase-orders/{pk}/

**Description:** Updates a specific purchase order by its PO number.

**Path Parameters:**

- `pk`: The PO number of the purchase order to update.

**Request Body:**

- `quality_rating` (Optional): The new quality rating for the purchase order.

**Returns:**

- 200 OK: The purchase order was successfully updated.
- 400 Bad Request: The request was malformed.
- 405 Method Not Allowed: The order is not acknowledged yet.

### DELETE /purchase-orders/{pk}/

**Description:** Deletes a specific purchase order by its PO number.

**Path Parameters:**

- `pk`: The PO number of the purchase order to delete.

**Returns:**

- 204 No Content: The purchase order was successfully deleted.
- 404 Not Found: The purchase order does not exist.

## Acknowledge Purchase Order API

### POST /purchase-orders/{pk}/acknowledge/

**Description:** Acknowledges a specific purchase order by its PO number.

**Path Parameters:**

- `pk`: The PO number of the purchase order to acknowledge.

**Returns:**

- 200 OK: The purchase order was successfully acknowledged.
- 404 Not Found: The purchase order does not exist.
- 405 Method Not Allowed: The purchase order is already acknowledged.

## Performance Metrics

- **On-Time Delivery Rate:** Calculated when the order status changes to "completed".
- **Fulfillment Rate:** Calculated every time there is an update to the purchase order.
- **Quality Rating Average:** Updated every time there is an update to the purchase order.

## Error Handling

The API returns appropriate HTTP status codes to indicate the result of the request. Refer to the HTTP status code documentation for more information on interpreting these responses.

## Contact

For any questions or issues, please contact the API administrator.

---

This documentation is subject to change as the API evolves. Always refer to the latest version for the most accurate information.

## Next Steps

- Explore the project's codebase.
- Familiarize yourself with Django's documentation and the Django admin interface.
- Begin developing your project!

Remember, if you encounter any issues, refer to the project's documentation or seek help from the community.
