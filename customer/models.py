from django.db import models
from store.models import Product
from userauths.models import User
from subbranch.models import Subbranch
from django.utils import timezone
TYPE = (
    ("New Order", "New Order"),
    ("Item Shipped", "Item Shipped"),
    ("Item Delivered", "Item Delivered"),
)

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="wishlist")

    class Meta:
        verbose_name_plural = "Wishlist"

    def __str__(self):
        if self.product.name:
            return self.product.name
        else:
            return "Wishlist"
        
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    zip_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.full_name}'s address in {self.city}"
    
class Notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    type = models.CharField(max_length=100,choices=TYPE,default=None)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Notifications"

    def __str__(self):
        return self.type

class Payment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    subbranch = models.ForeignKey(Subbranch, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=(("Paid", "Paid"), ("Unpaid", "Unpaid")))
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.status}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    subbranch = models.ForeignKey(Subbranch, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    reply = models.TextField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} to {self.subbranch.store_name}"

    class Meta:
        ordering = ['-created_at']