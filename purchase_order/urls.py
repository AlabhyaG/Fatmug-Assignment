from django.urls import path
from . views import *
urlpatterns=[
    path(
        'api/purchase_orders/',
         PurchaseOrderListAPIView.as_view(),
         name="Get-Purchase-Oder"
     ),
    path(
        'api/purchase_orders/<str:pk>/',
         PurchaseOrderSpecificAPIView.as_view(),
         name="Get-Purchase-Oder"
     ),
     path(
         'api/purchase_orders/<str:pk>/acknowledge/',
         AcknowledgePurchaseOrderApiView.as_view(),
         name='Acknowledgment'
     )
]