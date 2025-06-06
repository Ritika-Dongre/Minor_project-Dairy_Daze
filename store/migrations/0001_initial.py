# Generated by Django 5.1.7 on 2025-04-03 14:51

import django.db.models.deletion
import django.utils.timezone
import django_ckeditor_5.fields
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='image')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('shipping', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Processing', 'Processing'), ('Failed', 'Failed')], default='Processing', max_length=100)),
                ('payment_method', models.CharField(blank=True, choices=[('PayPal', 'PayPal'), ('Stripe', 'Stripe'), ('Flutterwave', 'Flutterwave'), ('Paystack', 'Paystack'), ('RazorPay', 'RazorPay')], default=None, max_length=100, null=True)),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Fulfilled', 'Fulfilled'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100)),
                ('initial_total', models.DecimalField(decimal_places=2, default=0.0, help_text='The original total ', max_digits=12)),
                ('saved', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='Amount', max_digits=12, null=True)),
                ('order_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=25, prefix='')),
                ('payment_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer', to=settings.AUTH_USER_MODEL)),
                ('subbranches', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Orders',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.FileField(blank=True, default='product.jpg', null=True, upload_to='images')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True, verbose_name='Sale Price')),
                ('regular_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True, verbose_name='Regular Price')),
                ('stock', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('shipping', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True, verbose_name='Shipping Amount')),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft'), ('Disabled', 'Disabled')], default='Published', max_length=50)),
                ('featured', models.BooleanField(default=False, verbose_name='Marketplace Featured')),
                ('sku', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=5, max_length=50, prefix='SKU', unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.category')),
                ('subbranch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Products',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Fulfilled', 'Fulfilled'), ('Cancelled', 'Cancelled')], default='Pending', max_length=100)),
                ('tracking_id', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('qty', models.IntegerField(default=0)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('shipping', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('initial_total', models.DecimalField(decimal_places=2, default=0.0, help_text='Grand total of all items', max_digits=12)),
                ('saved', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='Amount', max_digits=12, null=True)),
                ('item_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=25, prefix='')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('subbranch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subbranch_order_items', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(default='gallery.jpg', upload_to='images')),
                ('gallery_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=10, prefix='')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('sub_total', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('shipping', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('cart_id', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, null=True)),
                ('reply', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], default=None)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='store.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Variant Name')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='VariantItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Item Title')),
                ('content', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Item Content')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant_items', to='store.variant')),
            ],
        ),
    ]
