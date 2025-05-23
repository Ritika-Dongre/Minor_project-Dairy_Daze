# Generated by Django 4.2 on 2025-04-20 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subbranch', '0002_subbranch_otp_subbranch_otp_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subbranch',
            name='email',
            field=models.EmailField(default='noemail@example.com', max_length=254),
        ),
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=255)),
                ('product', models.CharField(max_length=255)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subbranch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='subbranch.subbranch')),
            ],
        ),
    ]
