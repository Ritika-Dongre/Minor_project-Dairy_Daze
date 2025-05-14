from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from userauths import models as user_models
from django.contrib.auth.models import User
from subbranch.models import Subbranch
# from subbranch import models as subbranch_models
import shortuuid
from django.utils import timezone




STATUS = (
    ("Published", "Published"),
    ("Draft", "Draft"),
    ("Disabled", "Disabled"),
)

PAYMENT_STATUS = (
    ("Paid", "Paid"),
    ("Processing", "Processing"),
    ("Failed", "Failed"),
)

PAYMENT_METHOD = (
    ("PayPal", "PayPal"),
    ("Stripe", "Stripe"),
    ("Flutterwave", "Flutterwave"),
    ("Paystack","Paystack"),
    ("RazorPay","RazorPay"),
)

ORDER_STATUS = (
    ("Pending", "Pending"),
    ("Processing", "Processing"),
    ("Shipped", "Shipped"),
    ("Fulfilled","Fulfilled"),
    ("Cancelled","Cancelled"),
)

SHIPPING_SERVICE = (
    ("DHL", "DHL"),
    ("FedX", "FedX"),
    ("UPS", "UPS"),
    ("GIG Logistics", "GIG Logistics"),
)

RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

class Category(models.Model):
    title = models.CharField(max_length=255)
    # FileField-to allow user to upload file in any format
    image = models.ImageField(upload_to="image", null=True, blank=True)
    slug = models.SlugField(unique=True)
    # slug-often used in url's to make them easier to read, but also to make them more search engine friendly.

    def __str__(self):
        return self.title
    
    # Meta class will rename Category to Categories in case of multiple items
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['title']


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    description = CKEditor5Field('Text', config_name='extends')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True, blank=True)

    price = models.DecimalField(max_digits=12,decimal_places=2,default=0.00, null=True, blank=True, verbose_name="Sale Price")

    regular_price = models.DecimalField(max_digits=12,decimal_places=2,default=0.00, null=True, blank=True, verbose_name="Regular Price")

    stock = models.PositiveIntegerField(default=0, null=True, blank=True)

    shipping = models.DecimalField(max_digits=12,decimal_places=2,default=0.00, null=True, blank=True, verbose_name="Shipping Amount")

    status = models.CharField(choices=STATUS,max_length=50,default="Published")

    featured = models.BooleanField(default=False, verbose_name="Marketplace Featured")

    subbranch = models.ForeignKey(user_models.User, on_delete=models.SET_NULL,null=True,blank=True)
    # each product will have unique sku
    sku = ShortUUIDField(unique=True, length=5, max_length=50,prefix="SKU",alphabet="1234567890")
    # ShortUUIDField-stores universally unique identifiers (UUIDs) in a shorter, more user-friendly format.
    slug = models.SlugField(null=True,blank=True)

    date = models.DateTimeField(default=timezone.now)
    unit = models.CharField(max_length=50, null=True, blank=True, help_text="e.g., kg, litre, piece")
    total_orders = models.PositiveIntegerField(default=0, help_text="Auto-updated number of orders placed for this product")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(shortuuid.uuid().lower()[:2])
        super(Product, self).save(*args, **kwargs)


class Variant(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=1000,verbose_name="Variant Name",null=True,blank=True)

    def items(self):
        return VariantItem.objects.filter(variant=self)
    
    def __str__(self):
        return self.name
    
# features of product
class VariantItem(models.Model):
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE,related_name="variant_items")
    title = models.CharField(max_length=1000,verbose_name="Item Title",null=True,blank=True)
    content = models.CharField(max_length=1000,verbose_name="Item Content",null=True, blank=True)

    def __str__(self):
        return self.variant.name
    
class Gallery(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to="images")
    gallery_id = ShortUUIDField(length=6,max_length=10,alphabet="1234567890")

    def __str__(self):
        return f"{self.product.name} - image"
    
    class Meta:
        verbose_name_plural = "Gallery"
    


    # class Coupon(models.Model):
    #     subbranch = models.ForeignKey(user_models.User, on_delete=models.SET_NULL,null=True)
    #     code = models.CharField(max_length=100)
    #     discount = models.IntegerField(default=1)

    #     def __str__(self):
    #         return self.code


class Cart(models.Model):
    user = models.OneToOneField('userauths.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        unique_together = ('cart', 'product')








class Order(models.Model):
    subbranches = models.ManyToManyField(user_models.User,blank=True)
    customer = models.ForeignKey(user_models.User,on_delete=models.SET_NULL,null=True,blank=True,related_name="customer")
    service_fee = models.DecimalField(default=0.00,max_digits=12,decimal_places=2)
    sub_total = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    shipping = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    tax = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    total = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    payment_status = models.CharField(max_length=100,choices=PAYMENT_STATUS,default="Processing")
    payment_method = models.CharField(max_length=100,choices=PAYMENT_METHOD,default=None,null=True,blank=True)
    order_status = models.CharField(max_length=100,choices=ORDER_STATUS,default="Pending")
    initial_total = models.DecimalField(max_digits=12,default=0.00,decimal_places=2,help_text="The original total ")
    saved = models.DecimalField(max_digits=12,decimal_places=2,default=0.00,null=True,blank=True,help_text="Amount")
   
    order_id = ShortUUIDField(length=6,max_length=25,alphabet="1234567890")
    payment_id = models.CharField(null=True,blank=True,max_length=1000)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Orders"
        ordering = ['-date']

    def __str__(self):
        return self.order_id
        
    def order_items(self):
        return OrderItem.objects.filter(order=self)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    order_status = models.CharField(max_length=100,choices=ORDER_STATUS,default="Pending")
    # shipping_service = models.CharField(max_length=100,choices=SHIPPING_SERVICE,default=None,null=True,blank=True)
    tracking_id = models.CharField(max_length=100,default=None,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    color = models.CharField(max_length=100,null=True,blank=True)
    size = models.CharField(max_length=100,null=True,blank=True)
    price = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    sub_total = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    shipping = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    tax = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    total = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    initial_total = models.DecimalField(max_digits=12,default=0.00,decimal_places=2,help_text="Grand total of all items")
    saved = models.DecimalField(max_digits=12,decimal_places=2,default=0.00,null=True,blank=True,help_text="Amount")
    # coupons = models.ManyToManyField(Coupon,blank=True)
    # applied_coupon = models.BooleanField(default=False)
    item_id = ShortUUIDField(length=6,max_length=25,alphabet="1234567890")
    subbranch = models.ForeignKey(user_models.User,null=True,on_delete=models.SET_NULL,related_name="subbranch_order_items")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.item_id
        
    def order_id(self):
        return f"{self.order.order_id}"
    
    class Meta:
        ordering = ['-date']

class Review(models.Model):
    user = models.ForeignKey(user_models.User,on_delete=models.SET_NULL,blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True,related_name="reviews")
    review = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True,blank=True)
    rating = models.IntegerField(choices=RATING,default=None)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} review on {self.product.name}"


class Subscription(models.Model):
    user = models.ForeignKey('userauths.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s subscription for {self.product.name}"
    
class SubbranchReview(models.Model):
    user = models.ForeignKey('userauths.User', on_delete=models.SET_NULL, blank=True, null=True)
    subbranch = models.ForeignKey('subbranch.Subbranch', on_delete=models.SET_NULL, blank=True, null=True, related_name="reviews")
    review = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    rating = models.IntegerField(choices=RATING, default=None)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} review on {self.subbranch.store_name}"
    