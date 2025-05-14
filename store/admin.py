from django.contrib import admin
from store import models as store_models

# TabularInline, for creating multiple gallery images and variant items variants, e.g. if you have an Order model and an OrderItem model, you can use TabularInline to display and edit the order items directly within the order editing page in the admin interface.
class GalleryInline(admin.TabularInline):
    model = store_models.Gallery

class VariantInline(admin.TabularInline):
    model = store_models.Variant

class VariantItemInline(admin.TabularInline):
    model = store_models.VariantItem

class CategoryAdmin(admin.ModelAdmin):
    # list_display = ['title', 'slug']
    # list_display = ['title', 'image']
    # list_editable = ['image']
    # prepopulated_fields = {'slug':('title',)}
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category','price','regular_price','stock','status','featured','subbranch','date']
    search_fields = ['name','category__title','description']
    list_filter = ['status', 'featured', 'category']
    inlines = [GalleryInline, VariantInline]
    prepopulated_fields = {'slug':('name',)}

class VariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name']
    search_fields = ['product__name', 'name']
    inlines = [VariantItemInline]

class VariantItemAdmin(admin.ModelAdmin):
    list_display = ['variant', 'title','content']
    search_fields = ['variant__name', 'title']

class GalleryAdmin(admin.ModelAdmin):
    list_display = ['product','gallery_id']
    search_fields = ['product__name']


class CartItemInline(admin.TabularInline):
    model = store_models.CartItem
    extra = 0

    
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username', 'user__email']
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = store_models.OrderItem
    extra = 0

# class CouponAdmin(admin.ModelAdmin):
#     list_display = ['code','subbranch','discount']
#     search_fields = ['code','subbranch__username']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'total', 'payment_status', 'order_status', 'date']
    list_filter = ['payment_status', 'order_status', 'date']
    search_fields = ['order_id', 'customer__username']
    inlines = [OrderItemInline]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'order_id', 'product', 'qty', 'total', 'order_status', 'date']
    list_filter = ['order_status', 'date']
    search_fields = ['item_id', 'order__order_id', 'product__name']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'active', 'date']
    list_filter = ['rating', 'active', 'date']
    search_fields = ['user__username', 'product__name', 'review']


admin.site.register(store_models.Category,CategoryAdmin)
admin.site.register(store_models.Product,ProductAdmin)
admin.site.register(store_models.Variant,VariantAdmin)
admin.site.register(store_models.VariantItem,VariantItemAdmin)
admin.site.register(store_models.Gallery,GalleryAdmin)
admin.site.register(store_models.Cart,CartAdmin)
admin.site.register(store_models.CartItem)
# admin.site.register(store_models.Coupon,CouponAdmin)
admin.site.register(store_models.Order,OrderAdmin)
admin.site.register(store_models.OrderItem,OrderItemAdmin)
admin.site.register(store_models.Review,ReviewAdmin)