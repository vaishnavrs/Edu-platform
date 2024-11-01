from django.urls import path
from .views import *
urlpatterns = [
    path('create_payment/', CreatePayment.as_view(), name='create_payment'),
    path('verify_payment/', VerifyPayment.as_view(), name='verify_payment'),
]