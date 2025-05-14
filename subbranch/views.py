from django.shortcuts import render, redirect
from .models import Subbranch, Payout, BankAccount 
from .forms import SubBranchImageForm

import random
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from customer.models import Payment
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Subbranch, Payout, Notifications
from store.models import Product, Order, Cart, OrderItem
from django.db.models import Sum, Count,Max
from datetime import datetime, timedelta, date
from userauths.models import Profile 
from .forms import BankAccountForm

from django.shortcuts import get_object_or_404
from store.models import Product
from .forms import ProductForm  # you'll add this form next
from django.contrib.auth.views import LogoutView

from datetime import datetime, timedelta
from django.db.models import Sum
from django.utils.timezone import now
from django.db.models.functions import TruncDate

def aboutus(request):
    return render(request, 'aboutus.html')
def productpage(request):
    return render(request, 'productpage.html')
def edit_product(request):
    return render(request, 'edit_product.html')
def sub_login(request):
    if request.method == 'POST':
        subbranch_id = request.POST.get('subbranch_id')
        email = request.POST.get('email')

        if 'send_otp' in request.POST:
            try:
                sub = Subbranch.objects.get(subbranch_id=subbranch_id)
                if sub.email != email:
                    messages.error(request, 'Email does not match our records.')
                    return redirect('subbranch:sub_login')

                otp = str(random.randint(100000, 999999))
                sub.otp = otp
                sub.otp_created_at = timezone.now()
                sub.save()

                send_mail('Your OTP for Sub-Branch Login',
                          f'Hello, your OTP is: {otp}\nValid for 5 minutes.',
                          'your_email@gmail.com', [email], fail_silently=False)

                request.session['subbranch_id'] = subbranch_id
                request.session['email'] = email
                request.session['otp_sent'] = True
                messages.success(request, 'OTP sent to your email!')
                return redirect('subbranch:sub_login')

            except Subbranch.DoesNotExist:
                messages.error(request, 'Invalid Subbranch ID or Email.')

        elif 'verify_otp' in request.POST:
            otp_entered = request.POST.get('otp')
            subbranch_id = request.session.get('subbranch_id')

            try:
                sub = Subbranch.objects.get(subbranch_id=subbranch_id)
                if sub.otp == otp_entered and timezone.now() - sub.otp_created_at <= timedelta(minutes=5):
                    request.session.pop('otp_sent', None)
                    request.session.pop('email', None)
                    login(request, sub.user)
                    return redirect('subbranch:sub_index')
                else:
                    messages.error(request, 'Invalid or expired OTP.')
            except Subbranch.DoesNotExist:
                messages.error(request, 'Session expired or invalid.')

        elif 'resend_otp' in request.POST:
            subbranch_id = request.session.get('subbranch_id')
            email = request.session.get('email')
            try:
                sub = Subbranch.objects.get(subbranch_id=subbranch_id)
                if sub.email != email:
                    messages.error(request, 'Email mismatch.')
                    return redirect('subbranch:sub_login')

                otp = str(random.randint(100000, 999999))
                sub.otp = otp
                sub.otp_created_at = timezone.now()
                sub.save()

                send_mail('Your New OTP for Sub-Branch Login',
                          f'Your new OTP is: {otp}\nIt’s valid for 5 minutes.',
                          'your_email@gmail.com', [email], fail_silently=False)
                messages.success(request, 'A new OTP has been sent to your email.')
                return redirect('subbranch:sub_login')
            except Subbranch.DoesNotExist:
                messages.error(request, 'Subbranch not found.')

    return render(request, 'sub_login.html')

# ------------------ Dashboard ------------------
@login_required
def sub_index(request):
    user = request.user
    today = date.today()
    week_ago = today - timedelta(days=7)

    try:
        subbranch = Subbranch.objects.get(user=user)
    except Subbranch.DoesNotExist:
        messages.error(request, 'Subbranch not found.')
        return redirect('subbranch:sub_login')

    orders = Order.objects.filter(subbranches=user)
    order_items = OrderItem.objects.filter(subbranch=user)
    total_orders = order_items.count()
    weekly_orders = order_items.filter(date__date__gte=week_ago).count()

    total_revenue = order_items.aggregate(total=Sum('total'))['total'] or 0
    weekly_revenue = order_items.filter(date__date__gte=week_ago).aggregate(total=Sum('total'))['total'] or 0

    customers_today = orders.filter(date__date=today).values('customer').distinct().count()
    unique_customers = orders.values('customer').distinct().count()

    payouts = Payout.objects.filter(subbranch=subbranch)
    method_data = payouts.values('item__order__payment_method').annotate(total=Sum('amount'))
    total_earnings = payouts.aggregate(total=Sum('amount'))['total'] or 0
    pending_payouts = payouts.filter(amount=0).count()

    notifications = Notifications.objects.filter(user=user, seen=False)
    notif_count = notifications.count()

    products = Product.objects.filter(subbranch=user)
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    revenue_chart_labels = []
    revenue_chart_data = []
    
    for day in last_7_days:
       daily_total = OrderItem.objects.filter(
        subbranch=user,
        date__date=day
    ).aggregate(total=Sum('total'))['total'] or 0
    revenue_chart_labels.append(day.strftime('%b %d'))
    revenue_chart_data.append(float(daily_total))

    pie_labels = []
    pie_values = []

    for entry in method_data:
       label = entry['item__order__payment_method'] or 'Unknown'
       pie_labels.append(label)
       pie_values.append(float(entry['total']))

    demo_mode = False
    if total_orders == 0 and total_revenue == 0:
        demo_mode = True
        total_orders = random.randint(20, 40)
        weekly_orders = random.randint(5, 15)
        total_revenue = round(random.uniform(3000, 10000), 2)
        weekly_revenue = round(random.uniform(800, 2000), 2)
        customers_today = random.randint(3, 10)
        unique_customers = random.randint(15, 30)
        total_earnings = round(random.uniform(2000, 7000), 2)
        pending_payouts = random.randint(0, 5)

        revenue_chart_labels = [(today - timedelta(days=i)).strftime('%b %d') for i in range(6, -1, -1)]
        revenue_chart_data = [random.randint(100, 1000) for _ in range(7)]

        pie_labels = ['Cash', 'Card', 'Online']
        pie_values = [45.5, 30.0, 24.5]


    context = {
        'subbranch': subbranch,
        'orders': orders,
        'order_items': order_items,
        'total_orders': total_orders,
        'weekly_orders': weekly_orders,
        'total_revenue': total_revenue,
        'weekly_revenue': weekly_revenue,
        'customers_today': customers_today,
        'unique_customers': unique_customers,
        'payouts': payouts,
        'total_earnings': total_earnings,
        'pending_payouts': pending_payouts,
        'notifications': notifications,
        'notif_count': notif_count,
        'products': products,
        'revenue_chart_labels': revenue_chart_labels,
        'revenue_chart_data': revenue_chart_data,
        'pie_labels': pie_labels,
        'pie_values': pie_values
    }

    

    
    return render(request, 'sub_index.html', context)

# ------------------ Other Views ------------------
@login_required
def sub_orders(request):
    orders = Order.objects.filter(subbranches=request.user)
    return render(request, 'sub_orders.html', {'orders': orders})

@login_required
def sub_products(request):
    
    
    products = Product.objects.filter(subbranch=request.user)
    for p in products:
        p.total_orders = OrderItem.objects.filter(product=p, subbranch=request.user).count()
    return render(request, 'sub_products.html', {'products': products})

@login_required
def sub_profile(request):
    subbranch = Subbranch.objects.get(user=request.user)
    if request.method == 'POST':
        form = SubBranchImageForm(request.POST, request.FILES, instance=subbranch)
        if form.is_valid():
            form.save()
            return redirect('subbranch:sub_profile')
    else:
        form = SubBranchImageForm(instance=subbranch)

    return render(request, 'sub_profile.html', {'subbranch': subbranch, 'form': form})

@login_required
def sub_reviews(request):
    return render(request, 'sub_reviews.html')

@login_required
def sub_notifications(request):
    notifications = Notifications.objects.filter(user=request.user).order_by('-date')
    return render(request, 'sub_notifications.html', {
        'notifications': notifications
    })


@login_required
def subbranch_payment_status(request):
    today = date.today()
    one_week_ago = today - timedelta(days=7)
    payments = Payment.objects.filter(subbranch__user=request.user)
    daily_total = payments.filter(date=today).aggregate(total=Sum('amount'))['total'] or 0
    weekly_total = payments.filter(date__gte=one_week_ago).aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'sub_payment_status.html', {
        'payments': payments,
        'daily_total': daily_total,
        'weekly_total': weekly_total
    })

@login_required
def subbranch_payouts_view(request):
    subbranch = Subbranch.objects.get(user=request.user)
    payouts = Payout.objects.filter(subbranch=subbranch)
    total_earnings = payouts.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'sub_payouts.html', {
        'payouts': payouts,
        'total_earnings': total_earnings
    })


@login_required
def subbranch_customers_view(request):
    user = request.user

    try:
        subbranch = Subbranch.objects.get(user=user)
    except Subbranch.DoesNotExist:
        messages.error(request, "Subbranch not found.")
        return redirect('subbranch:sub_login')

    # 💥 Correct way: Filter customers using Profile
    customers = Profile.objects.filter(
        user_Type="Customer",
        zipcode=subbranch.zip_code
    )

    return render(request, 'sub_customers.html', {'customers': customers})
@login_required
def bank_account_view(request):
    subbranch = Subbranch.objects.get(user=request.user)
    try:
        account = BankAccount.objects.get(subbranch=subbranch)
    except BankAccount.DoesNotExist:
        account = None

    if request.method == 'POST':
        form = BankAccountForm(request.POST, instance=account)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.subbranch = subbranch
            bank.save()
            messages.success(request, "Bank account info updated.")
            return redirect('subbranch:bank_account')
    else:
        form = BankAccountForm(instance=account)

    return render(request, 'sub_bank_account.html', {'form': form, 'account': account})
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, subbranch=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('subbranch:sub_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, subbranch=request.user)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('subbranch:sub_products')
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.subbranch = request.user
            product.save()
            messages.success(request, "Product added successfully.")
            return redirect('subbranch:sub_products')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def customers_in_area(request):
    user = request.user
    try:
        subbranch = Subbranch.objects.get(user=user)
    except Subbranch.DoesNotExist:
        messages.error(request, "Subbranch not found.")
        return redirect('subbranch:sub_login')

    # Match based on zip_code
    customers = Profile.objects.filter(
        user_Type="Customer",
        zipcode=subbranch.zip_code
    )

    return render(request, 'sub_customers.html', {'customers': customers})