from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from userauths.forms import UserRegisterForm, LoginForm
from userauths.models import User, Profile
from customer.models import Address
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("customer:product1")
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # The form's save method will create both User and Profile
                    user = form.save()
                    
                    # Create Address
                    Address.objects.create(
                        user=user,
                        full_name=form.cleaned_data['full_name'],
                        mobile=form.cleaned_data['mobile'],
                        email=form.cleaned_data['email'],
                        address=form.cleaned_data['address'],
                        city="Not Specified",
                        state="Not Specified",
                        zip_code="000000",
                        is_default=True
                    )
                    
                    # Login the user
                    login(request, user)
                    messages.success(request, "Registration successful! Welcome to DairyDaze!")
                    return redirect("customer:product1")
                    
            except Exception as e:
                messages.error(request, f"Registration failed. Please try again. Error: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()
    
    return render(request, "mregisterforcustomer.html", {"form": form})


def mhome(request):
    return render(request, "mhome.html")

def product1_view(request):
    return redirect("customer:product1")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("customer:product1")
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect("customer:product1")
        else:
            messages.error(request, "Invalid email or password")
    
    return render(request, "customerlogin.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out")
    return redirect('customer:productpage')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            profile = request.user.profile
            profile.full_name = request.POST.get('full_name')
            profile.mobile = request.POST.get('mobile')
            profile.state = request.POST.get('state')
            profile.city = request.POST.get('city')
            profile.zipcode = request.POST.get('zipcode')
            profile.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def update_profile_photo(request):
    if request.method == 'POST' and request.FILES.get('profile_photo'):
        try:
            profile = request.user.profile
            profile.image = request.FILES['profile_photo']
            profile.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'No photo provided'})