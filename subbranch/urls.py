from django.urls import path
from . import views
from .views import subbranch_payment_status
from django.contrib.auth.views import LogoutView

app_name = 'subbranch'
urlpatterns = [
    path('aboutus/', views.aboutus, name='aboutus'),
    #path('', views.mfontpage, name='mfontpage'),
    path('productpage/', views.productpage, name='productpage'),
    #path('mhome/', views.mhome, name='mhome'),
    #path('mjoinas/', views.mjoinas, name='mjoinas'),
    #path('mregisterfordistributor/', views.mregisterfordistributor, name='mregisterfordistributor'),
    #path('product/', views.product, name='product'),
    path('sub_login/', views.sub_login, name='sub_login'),
    path('sub_index/', views.sub_index, name='sub_index'),
    path('sub_notifications/', views.sub_notifications, name='sub_notifications'),
    path('sub_orders/', views.sub_orders, name='sub_orders'),
    path('sub_products/', views.sub_products, name='sub_products'),
    path('sub_profile/', views.sub_profile, name='sub_profile'),
    path('sub_reviews/', views.sub_reviews, name='sub_reviews'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('sub_payment_status/', views.subbranch_payment_status, name='sub_payment_status'),

    # path('test-email/', views.test_email, name='test_email'),

    #path('customers/', views.subbranch_customers_view, name='subbranch_customers'),

   # path('orders/', views.subbranch_orders_view, name='subbranch_orders'),
   # path('sub_notifications/', views.subbranch_notifications_view, name='sub_notifications'),
   # path('products/', views.subbranch_products_view, name='subbranch_products'),
   # path('customers-today/', views.daily_customers_view, name='subbranch_customers_today'),
    path('payouts/', views.subbranch_payouts_view, name='subbranch_payouts'),
    path('bank-account/', views.bank_account_view, name='bank_account'),
   # path('send_otp/', views.send_otp, name='send_otp'),
   # path('verify_otp/', views.verify_otp, name='verify_otp'),
   path('logout/', LogoutView.as_view(next_page='subbranch:sub_login'), name='logout'),


    path('customers/', views.subbranch_customers_view, name='sub_customers'),
    #path('sub_logout/', views.sub_logout, name='sub_logout'),
    path('add_product/', views.add_product, name='add_product'),
    path('area-customers/', views.customers_in_area, name='customers_in_area'),


    ]
