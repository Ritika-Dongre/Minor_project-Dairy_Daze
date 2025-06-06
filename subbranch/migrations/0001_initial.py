# Generated by Django 5.1.7 on 2025-04-04 13:37

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0002_alter_gallery_options_alter_gallery_image_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('New Order', 'New Order'), ('Item Shipped', 'Item Shipped'), ('Item Delivered', 'Item Delivered')], default=None, max_length=100)),
                ('seen', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.orderitem')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Notifications',
            },
        ),
        migrations.CreateModel(
            name='Subbranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='branch-image.jpg', upload_to='images')),
                ('store_name', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('subbranch_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=20, prefix='', unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subbranch', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('payout_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=10, prefix='', unique=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hfjfjf', to='store.orderitem')),
                ('subbranch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subbranch.subbranch')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(blank=True, choices=[('PayPal', 'PayPal'), ('Stripe', 'Stripe'), ('Flutterwave', 'Flutterwave'), ('Paystack', 'Paystack'), ('RazorPay', 'RazorPay')], max_length=50, null=True)),
                ('bank_name', models.CharField(max_length=500)),
                ('account_number', models.CharField(max_length=100)),
                ('account_name', models.CharField(max_length=100)),
                ('bank_code', models.CharField(blank=True, max_length=100, null=True)),
                ('stripe_id', models.CharField(blank=True, max_length=100, null=True)),
                ('paypal_address', models.CharField(blank=True, max_length=100, null=True)),
                ('subbranch', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subbranch.subbranch')),
            ],
            options={
                'verbose_name_plural': 'Bank Account',
            },
        ),
    ]
