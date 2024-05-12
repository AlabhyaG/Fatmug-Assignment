from django.urls import path
from . views import *

urlpatterns=[
    path(
        'api/vendors/',
         AllVendorAPIView.as_view(),
         name='All-Vendor-View'
    ),
    path(
        'api/vendors/<str:pk>/',
        SpecificVendorAPIView.as_view(),
        name="Specific-Vendor-View"
    ),
    path(
        'api/vendors/<str:pk>/performance/',
        PerformanceVendorApiView.as_view(),
        name="Performace-Vendor"
    )
]