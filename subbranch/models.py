from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.utils.text import slugify
import random
from django.utils import timezone
from datetime import timedelta
# from customer.models import Address

NOTIFICATION_TYPE = (
    ("New Order","New Order"),
    ("New Review","New Review"),
)

PAYMENT_METHOD = (
    ("PayPal", "PayPal"),
    ("Stripe", "Stripe"),
    ("Flutterwave", "Flutterwave"),
    ("Paystack","Paystack"),
    ("RazorPay","RazorPay"),
)

TYPE = (
    ("New Order","New Order"),
    ("Item Shipped", "Item Shipped"),
    ("Item Delivered", "Item Delivered"),
)


class Subbranch(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,related_name="subbranch")
    email = models.EmailField(default='noemail@example.com') 
    image = models.ImageField(upload_to="images",default="branch-image.jpg",blank=True)
    store_name = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True,default=None)
    city = models.CharField(max_length=100,null=True,blank=True,default=None)
    address = models.CharField(max_length=100,null=True,blank=True,default=None)
    zip_code = models.CharField(max_length=20,null=True,blank=True,default=None)
    subbranch_id = ShortUUIDField(unique=True,length=6,max_length=20,alphabet="1234567890")
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True,null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.subbranch_id
    
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.store_name)
        super(Subbranch, self).save(*args, **kwargs)

class Payout(models.Model):
    subbranch = models.ForeignKey(Subbranch,on_delete=models.SET_NULL,null=True)
    item = models.ForeignKey("store.OrderItem",on_delete=models.SET_NULL,null=True,related_name="payouts")
    amount = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    payout_id = ShortUUIDField(unique=True,length=6,max_length=10,alphabet="1234567890")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.subbranch)
    
    class Meta:
        ordering = ['-date']
 
class BankAccount(models.Model):
    subbranch = models.OneToOneField(Subbranch,on_delete=models.SET_NULL,null=True)
    account_type = models.CharField(max_length=50,choices=PAYMENT_METHOD,null=True,blank=True)
    bank_name = models.CharField(max_length=500)
    account_number = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=100,null=True,blank=True)
    stripe_id = models.CharField(max_length=100,null=True,blank=True)
    paypal_address = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        verbose_name_plural = "Bank Account"

    def __str__(self):
        return self.bank_name
        
class Notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="vendor_notifications")
    type = models.CharField(max_length=100,choices=TYPE,default=None)
    order = models.ForeignKey("store.OrderItem",on_delete=models.CASCADE,null=True,blank=True)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Notifications"

    def __str__(self):
        return self.type    


# class CustomerOrder(models.Model):
#     customer = models.ForeignKey(Address, on_delete=models.CASCADE)
#     subbranch = models.ForeignKey(Subbranch, related_name='orders', on_delete=models.CASCADE)
#     order_date = models.DateTimeField(auto_now_add=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

#     def __str__(self):
#         return f"Order {self.id} - {self.customer_name}"    