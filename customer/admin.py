from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from customer import models as customer_models
from .models import Wishlist, Address, Notifications, Message

class AddressAdmin(ImportExportActionModelAdmin):
    list_display = ['user','full_name']

class WishlistAdmin(ImportExportActionModelAdmin):
    list_display = ['user','product']

class NotificationAdmin(ImportExportActionModelAdmin):
    list_display = ['user','type','seen','date']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'subbranch', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('subject', 'message', 'sender__email', 'subbranch__email')
    ordering = ('-created_at',)

admin.site.register(customer_models.Address,AddressAdmin)
admin.site.register(customer_models.Wishlist,WishlistAdmin)
admin.site.register(customer_models.Notifications,NotificationAdmin)