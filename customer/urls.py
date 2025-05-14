from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    # Landing pages
    path('', views.mfontpage, name='mfontpage'),
    path('productpage/', views.productpage, name='productpage'),
    path('mhome/', views.mhome, name='mhome'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('mjoinas/', views.mjoinas, name='mjoinas'),
    
    # Product pages
    path('product/', views.product, name='product'),
    path('product1/', views.product1, name='product1'),
    
    # User pages
    path('profile/', views.profile, name='profile'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('orders/', views.orders, name='orders'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('toggle-subscription/', views.toggle_subscription, name='toggle_subscription'),
    path('update-subscription-quantity/', views.update_subscription_quantity, name='update_subscription_quantity'),
    path('payments/', views.payments, name='payments'),
    path('create-order/', views.create_order, name='create_order'),
    path('contact-store/', views.contact_store, name='contact_store'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-profile-photo/', views.update_profile_photo, name='update_profile_photo'),
    path('send-message/', views.send_message, name='send_message'),
    path('subbranch/messages/', views.subbranch_messages, name='subbranch_messages'),
    path('subbranch/messages/mark-read/<int:message_id>/', views.mark_message_read, name='mark_message_read'),
    path('messages/<int:message_id>/reply/', views.reply_to_message, name='reply_to_message'),
    path('review/', views.review_page, name='review'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('settings/', views.settings_page, name='settings'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('check-payment-status/<str:payment_id>/', views.check_payment_status, name='check_payment_status'),
    path('payment-success/', views.payment_success, name='payment_success'),
]