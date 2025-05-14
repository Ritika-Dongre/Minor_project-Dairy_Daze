from django.urls import path
from store import views

app_name = "store"

urlpatterns = [
    path("",views.index, name="index"),
    path("cart/", views.cart, name="cart"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("update-cart/", views.update_cart, name="update_cart"),
    path("remove-from-cart/", views.remove_from_cart, name="remove_from_cart"),
    path("payment-gateway/<str:payment_id>/", views.payment_gateway, name="payment_gateway"),
    path("razorpay-payment-verify/<str:order_id>/", views.razorpay_payment_verify, name="razorpay_payment_verify"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-failed/", views.payment_failed, name="payment_failed"),
]