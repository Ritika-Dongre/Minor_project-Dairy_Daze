from django.contrib import admin
from subbranch import models as subbranch_models

class SubbranchAdmin(admin.ModelAdmin):
    list_display = ['store_name','user','city','subbranch_id','date']
    search_fields = ['store_name','user__username','subbranch_id']
    prepopulated_fields = {'slug':('store_name',)}
    list_filter = ['city','date']

class PayoutAdmin(admin.ModelAdmin):
    list_display = ['payout_id','subbranch','item','amount','date']
    search_fields = ['payout_id','subbranch__store_name','item__order__order_id']
    list_filter = ['date','subbranch']

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['subbranch','bank_name','account_number','account_type']
    search_fields = ['subbranch__store_name','bank_name','account_number']
    list_filter = ['account_type']

class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['user','type','order','seen']
    list_editable = ['order']

admin.site.register(subbranch_models.Subbranch, SubbranchAdmin)
admin.site.register(subbranch_models.Payout, PayoutAdmin)
admin.site.register(subbranch_models.BankAccount, BankAccountAdmin)
admin.site.register(subbranch_models.Notifications, NotificationsAdmin)