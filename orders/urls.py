from django.urls.conf import path
from .views import OrderGenericAPIView, ExportAPIView

urlpatterns = [
    path('orders/',  OrderGenericAPIView.as_view()),
    path('orders/<str:pk>', OrderGenericAPIView.as_view()),
    path('export/', ExportAPIView.as_view()),
]
