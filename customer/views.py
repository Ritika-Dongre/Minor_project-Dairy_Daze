from django.shortcuts import render, redirect
from .models import Wishlist, Message
from django.contrib.auth.decorators import login_required
from store.models import Product, Order, CartItem, Subscription, OrderItem, Cart, Review, SubbranchReview
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from userauths.models import User as CustomUser
from userauths.models import Profile
from subbranch.models import Subbranch
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from subbranch.models import Subbranch, Notifications
from userauths.models import Profile
# def aboutus(request):
#     return render(request, 'aboutus.html')

# def mfontpage(request):
#     return render(request, 'mfontpage.html')

# def productpage(request):
#     if request.user.is_authenticated:
#         return redirect('customer:product1')
#     products = Product.objects.all()
#     return render(request, 'productpage.html', {'products': products})

# def mhome(request):
#     return render(request, 'mhome.html')

# def mjoinas(request):
#     return render(request, 'mjoinas.html')

# def customerlogin(request):
#     return render(request, 'customerlogin.html')

# def profile(request):
#     return render(request, 'profile.html')

# def product(request):
#     return render(request, 'product.html')

# @login_required
# def product1(request):
#     products = Product.objects.all()
#     wishlist_items = []
#     cart_items = []
#     subbranch_email = None
    
#     if request.user.is_authenticated:
#         wishlist_items = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
#         cart_items = list(CartItem.objects.filter(cart__user=request.user))
        
#         # Safely get the user's profile and zipcode
#         try:
#             user_profile = request.user.profile
#             user_zipcode = user_profile.zipcode
#             if user_zipcode:
#                 # Find the subbranch that serves this zipcode
#                 subbranch = Subbranch.objects.filter(zip_code=user_zipcode).first()
#                 if subbranch:
#                     subbranch_email = subbranch.email
#         except:
#             pass
    
#     return render(request, 'product1.html', {
#         'products': products,
#         'wishlist_items': wishlist_items,
#         'cart_items': cart_items,
#         'subbranch_email': subbranch_email,
#     })

# #Wishlist
# @login_required
# def wishlist(request):
#     wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
#     return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

# @login_required
# def toggle_wishlist(request, product_id):
#     if request.method == 'POST':
#         product = get_object_or_404(Product, id=product_id)
#         wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        
#         if not created:
#             wishlist_item.delete()
        
#         wishlist_count = Wishlist.objects.filter(user=request.user).count()
#         return JsonResponse({
#             'success': True,
#             'wishlist_count': wishlist_count
#         })
#     return JsonResponse({'success': False}, status=400)

# @login_required
# def orders(request):
#     orders = Order.objects.filter(customer=request.user).order_by('-date')
#     return render(request, 'orders.html', {'orders': orders})

# @login_required
# def subscriptions(request):
#     subscriptions = Subscription.objects.filter(user=request.user)
#     return render(request, 'subscriptions.html', {'subscriptions': subscriptions})

# @login_required
# def toggle_subscription(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         subscription_id = data.get('subscription_id')
#         product_id = data.get('product_id')
        
#         if subscription_id:
#             # Toggle existing subscription status
#             try:
#                 subscription = Subscription.objects.get(id=subscription_id, user=request.user)
#                 subscription.is_active = not subscription.is_active
#                 subscription.save()
                
#                 return JsonResponse({
#                     'success': True,
#                     'is_active': subscription.is_active
#                 })
#             except Subscription.DoesNotExist:
#                 return JsonResponse({'success': False, 'error': 'Subscription not found'}, status=404)
        
#         elif product_id:
#             # Create or delete subscription
#             try:
#                 product = Product.objects.get(id=product_id)
#                 subscription, created = Subscription.objects.get_or_create(
#                     user=request.user,
#                     product=product,
#                     defaults={'is_active': True}
#                 )
                
#                 if not created:
#                     subscription.delete()
#                     subscribed = False
#                 else:
#                     subscribed = True
                
#                 return JsonResponse({
#                     'success': True,
#                     'subscribed': subscribed
#                 })
#             except Product.DoesNotExist:
#                 return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
        
#         else:
#             return JsonResponse({'success': False, 'error': 'Missing subscription_id or product_id'}, status=400)
    
#     return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# @login_required
# def update_subscription_quantity(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         subscription_id = data.get('subscription_id')
#         quantity = data.get('quantity')
        
#         if not quantity or quantity < 1:
#             return JsonResponse({'success': False, 'error': 'Invalid quantity'}, status=400)
        
#         try:
#             subscription = Subscription.objects.get(id=subscription_id, user=request.user)
#             subscription.quantity = quantity
#             subscription.save()
            
#             return JsonResponse({'success': True})
#         except Subscription.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Subscription not found'}, status=404)
    
#     return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# @login_required
# def payments(request):
#     # Get all orders for the current user
#     orders = Order.objects.filter(customer=request.user)
    
#     # Create a list of payment records from orders
#     payments = []
#     for order in orders:
#         payment = {
#             'order': order,
#             'date': order.date,
#             'amount': order.total,
#             'status': order.payment_status,
#             'id': order.order_id
#         }
#         payments.append(payment)
    
#     context = {
#         'payments': payments,
#         'cart_items': request.user.cart.items.all() if hasattr(request.user, 'cart') else [],
#         'wishlist_items': [item.product.id for item in request.user.wishlist.items.all()] if hasattr(request.user, 'wishlist') else [],
#     }
    
#     return render(request, 'payments.html', context)

# @login_required
# def payment_gateway(request, payment_id):
#     # Get the order
#     order = get_object_or_404(Order, order_id=payment_id, customer=request.user)
    
#     context = {
#         'order': order,
#         'cart_items': request.user.cart.items.all() if hasattr(request.user, 'cart') else [],
#         'wishlist_items': [item.product.id for item in request.user.wishlist.items.all()] if hasattr(request.user, 'wishlist') else [],
#     }
    
#     return render(request, 'payment_gateway.html', context)


# @login_required
# def contact_store(request):
#     user = request.user
#     subbranch_email = "contact@dairydaze.com"  # Default email

#     if hasattr(user, 'profile') and user.profile.zipcode:
#         # Try to get the subbranch based on user's zipcode
#         try:
#             subbranch = User.objects.get(is_subbranch=True, profile__zipcode=user.profile.zipcode)
#             if subbranch:
#                 subbranch_email = subbranch.email
#         except User.DoesNotExist:
#             pass

#     return render(request, 'contact_store.html', {
#         'subbranch_email': subbranch_email,
#         'cart_items': CartItem.objects.filter(cart__user=request.user) if request.user.is_authenticated else [],
#         'wishlist_items': Wishlist.objects.filter(user=request.user) if request.user.is_authenticated else []
#     })

# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         user = request.user
#         profile = user.profile

#         # Update user email
#         user.email = request.POST.get('email', user.email)
#         user.save()

#         # Update profile fields
#         profile.full_name = request.POST.get('full_name', profile.full_name)
#         profile.mobile = request.POST.get('mobile', profile.mobile)
#         profile.state = request.POST.get('state', profile.state)
#         profile.city = request.POST.get('city', profile.city)
#         profile.zipcode = request.POST.get('zipcode', profile.zipcode)
#         profile.save()

#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False})

# @login_required
# def update_profile_photo(request):
#     if request.method == 'POST' and request.FILES.get('photo'):
#         profile = request.user.profile
#         profile.photo = request.FILES['photo']
#         profile.save()
#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False})

# @login_required
# def send_message(request):
#     if request.method == 'POST':
#         try:
#             user_zipcode = request.user.profile.zipcode
#             subbranch = Subbranch.objects.filter(zip_code=user_zipcode).first()
#             if subbranch:
#                 message = Message.objects.create(
#                     sender=request.user,
#                     subbranch=subbranch,
#                     subject=request.POST.get('subject'),
#                     message=request.POST.get('message')
#                 )
#                 return JsonResponse({
#                     'success': True,
#                     'message': 'Message sent successfully!'
#                 })
#             else:
#                 return JsonResponse({
#                     'success': False,
#                     'message': 'No subbranch found for your area.'
#                 })
#         except Exception as e:
#             print(f"Error sending message: {str(e)}")
#             return JsonResponse({
#                 'success': False,
#                 'message': str(e)
#             })
#     return JsonResponse({
#         'success': False,
#         'message': 'Invalid request method'
#     })

# @login_required
# def subbranch_messages(request):
#     if not hasattr(request.user, 'subbranch'):
#         return redirect('customer:product1')
#     messages = Message.objects.filter(subbranch=request.user.subbranch).order_by('-created_at')
#     return render(request, 'subbranch_messages.html', {
#         'messages': messages,
#         'unread_count': messages.filter(is_read=False).count()
#     })

# @login_required
# def mark_message_read(request, message_id):
#     if request.method == 'POST' and hasattr(request.user, 'subbranch'):
#         message = get_object_or_404(Message, id=message_id, subbranch=request.user.subbranch)
#         message.is_read = True
#         message.save()
#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False})

# @login_required
# def reply_to_message(request, message_id):
#     if request.method == 'POST':
#         try:
#             subbranch = Subbranch.objects.get(user=request.user)
#             message = Message.objects.get(id=message_id, subbranch=subbranch)
#             data = json.loads(request.body)
#             reply_text = data.get('reply')
#             if reply_text:
#                 message.reply = reply_text
#                 message.replied_at = timezone.now()
#                 message.save()
#                 subject = f"Reply to your message: {message.subject}"
#                 email_body = f"""
#                 Dear {message.sender.username},

#                 The store has replied to your message:

#                 Your original message:
#                 {message.message}

#                 Their reply:
#                 {reply_text}

#                 Best regards,
#                 DairyDaze Team
#                 """
#                 try:
#                     send_mail(
#                         subject,
#                         email_body,
#                         settings.DEFAULT_FROM_EMAIL,
#                         [message.sender.email],
#                         fail_silently=False,
#                     )
#                 except Exception as e:
#                     print(f"Failed to send email notification: {e}")
#                 return JsonResponse({'success': True})
#             return JsonResponse({'success': False, 'error': 'Reply text is required'})
#         except Message.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Message not found'}, status=404)
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)}, status=500)
#     return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

# @login_required
# def review_page(request):
#     subbranches = Subbranch.objects.all()
#     user_reviews = SubbranchReview.objects.filter(user=request.user, active=True)
#     return render(request, 'review.html', {
#         'subbranches': subbranches,
#         'user_reviews': user_reviews
#     })

# @login_required
# def submit_review(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             subbranch_id = data.get('subbranch_id')
#             rating = data.get('rating')
#             review_text = data.get('review')
#             if not all([subbranch_id, rating, review_text]):
#                 return JsonResponse({
#                     'success': False,
#                     'message': 'Please fill in all fields'
#                 })
#             subbranch = Subbranch.objects.get(id=subbranch_id)
#             existing_review = SubbranchReview.objects.filter(user=request.user, subbranch=subbranch).first()
#             if existing_review:
#                 existing_review.rating = rating
#                 existing_review.review = review_text
#                 existing_review.save()
#                 message = 'Review updated successfully!'
#             else:
#                 SubbranchReview.objects.create(
#                     user=request.user,
#                     subbranch=subbranch,
#                     rating=rating,
#                     review=review_text,
#                     active=True
#                 )
#                 message = 'Review submitted successfully!'
#             return JsonResponse({
#                 'success': True,
#                 'message': message
#             })
#         except Subbranch.DoesNotExist:
#             return JsonResponse({
#                 'success': False,
#                 'message': 'Store not found'
#             })
#         except Exception as e:
#             return JsonResponse({
#                 'success': False,
#                 'message': str(e)
#             })
#     return JsonResponse({
#         'success': False,
#         'message': 'Invalid request method'
#     })

# @login_required
# def settings_page(request):
#     return render(request, 'settings.html')

# @login_required
# def delete_account(request):
#     if request.method == 'POST':
#         user = request.user
#         # Log the user out
#         logout(request)
#         # Delete the user account
#         user.delete()
#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False})

# @csrf_exempt
# def check_payment_status(request, payment_id):
#     return JsonResponse({'status': 'ok', 'payment_id': payment_id})

# def payment_success(request):
#     return render(request, 'payment_success.html')

# # Create your views here.

from django.shortcuts import render, redirect
from .models import Wishlist, Message
from django.contrib.auth.decorators import login_required
from store.models import Product, Order, CartItem, Subscription, OrderItem, Cart, Review, SubbranchReview
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from userauths.models import User as CustomUser
from userauths.models import Profile
from subbranch.models import Subbranch
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

def aboutus(request):
    return render(request, 'aboutus.html')

def mfontpage(request):
    return render(request, 'mfontpage.html')

def productpage(request):
    if request.user.is_authenticated:
        return redirect('customer:product1')
    products = Product.objects.all()
    return render(request, 'productpage.html', {'products': products})

def mhome(request):
    return render(request, 'mhome.html')

def mjoinas(request):
    return render(request, 'mjoinas.html')

def customerlogin(request):
    return render(request, 'customerlogin.html')

def profile(request):
    return render(request, 'profile.html')

def product(request):
    return render(request, 'product.html')

@login_required
def product1(request):
    # Get regular products and products from user's connected subbranch
    products = Product.objects.all()  # Show all products initially
    wishlist_items = []
    cart_items = []
    subscribed_items = []
    subbranch_email = None
    
    if request.user.is_authenticated:
        wishlist_items = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
        cart_items = list(CartItem.objects.filter(cart__user=request.user).values_list('product_id', flat=True))
        subscribed_items = list(Subscription.objects.filter(user=request.user, is_active=True).values_list('product_id', flat=True))
        
        # Get user's connected subbranch
        if hasattr(request.user, 'profile') and request.user.profile.zipcode:
            try:
                subbranch = Subbranch.objects.filter(zip_code=request.user.profile.zipcode).first()
                if subbranch:
                    subbranch_email = subbranch.email
            except:
                pass
    
    return render(request, 'product1.html', {
        'products': products,
        'wishlist_items': wishlist_items,
        'cart_items': cart_items,
        'subscribed_items': subscribed_items,
        'subbranch_email': subbranch_email,
    })

#Wishlist
@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def toggle_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        
        if not created:
            wishlist_item.delete()
        
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return JsonResponse({
            'success': True,
            'wishlist_count': wishlist_count
        })
    return JsonResponse({'success': False}, status=400)

@login_required
def orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-date')
    return render(request, 'orders.html', {'orders': orders})

@login_required
def subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    return render(request, 'subscriptions.html', {'subscriptions': subscriptions})

@login_required
def toggle_subscription(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subscription_id = data.get('subscription_id')
        product_id = data.get('product_id')
        
        if subscription_id:
            # Toggle existing subscription status
            try:
                subscription = Subscription.objects.get(id=subscription_id, user=request.user)
                subscription.is_active = not subscription.is_active
                subscription.save()
                
                return JsonResponse({
                    'success': True,
                    'is_active': subscription.is_active
                })
            except Subscription.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Subscription not found'}, status=404)
        
        elif product_id:
            # Create or delete subscription
            try:
                product = Product.objects.get(id=product_id)
                subscription, created = Subscription.objects.get_or_create(
                    user=request.user,
                    product=product,
                    defaults={'is_active': True}
                )
                
                if not created:
                    subscription.delete()
                    subscribed = False
                else:
                    subscribed = True
                
                return JsonResponse({
                    'success': True,
                    'subscribed': subscribed
                })
            except Product.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)
        
        else:
            return JsonResponse({'success': False, 'error': 'Missing subscription_id or product_id'}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
def update_subscription_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subscription_id = data.get('subscription_id')
        quantity = data.get('quantity')
        
        if not quantity or quantity < 1:
            return JsonResponse({'success': False, 'error': 'Invalid quantity'}, status=400)
        
        try:
            subscription = Subscription.objects.get(id=subscription_id, user=request.user)
            subscription.quantity = quantity
            subscription.save()
            
            return JsonResponse({'success': True})
        except Subscription.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Subscription not found'}, status=404)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
def payments(request):
    # Get all unpaid orders for the current user
    orders = Order.objects.filter(
        customer=request.user,
        payment_status='Processing'
    ).order_by('-date')
    
    # Create a list of payment records from orders
    payments = []
    for order in orders:
        payment = {
            'order': order,
            'date': order.date,
            'amount': order.total,
            'status': order.payment_status,
            'id': order.order_id
        }
        payments.append(payment)
    
    context = {
        'payments': payments,
        'cart_items': request.user.cart.items.all() if hasattr(request.user, 'cart') else [],
        'wishlist_items': [item.product.id for item in request.user.wishlist.items.all()] if hasattr(request.user, 'wishlist') else [],
    }
    
    return render(request, 'payments.html', context)

@login_required
def create_order(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items.exists():
            return redirect('store:cart')
        
        # Create the order
        order = Order.objects.create(
            customer=request.user,
            payment_status='Processing'
        )
        create_notification_for_subbranch(order)
        total = 0
        # Create order items from cart items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                qty=cart_item.quantity,
                price=cart_item.product.price,
                total=cart_item.product.price * cart_item.quantity
            )
            total += cart_item.product.price * cart_item.quantity
        
        # Update order total
        order.total = total
        order.save()
        # create_notification_for_subbranch(order)

        # Clear the cart
        cart_items.delete()
        
        # Redirect to payment gateway with the order ID
        return redirect('store:payment_gateway', payment_id=order.order_id)
    
    return redirect('store:cart')
def create_notification_for_subbranch(order):
    try:
        profile = Profile.objects.get(user=order.customer)
        subbranch = Subbranch.objects.filter(zip_code=profile.zipcode).first()
        
        if subbranch:
            Notifications.objects.create(
                user=subbranch.user,
                type="New Order",
                order=None,  # Optional, if you have order-item link
                seen=False
            )
    except Exception as e:
        print("Notification Error:", e)

@login_required
def contact_store(request):
    user = request.user
    subbranch_email = "dairydaze4@gmail.com" 

    if hasattr(user, 'profile') and user.profile.zipcode:
        # Try to get the subbranch based on user's zipcode
        try:
            subbranch = User.objects.get(is_subbranch=True, profile__zipcode=user.profile.zipcode)
            if subbranch:
                subbranch_email = subbranch.email
        except User.DoesNotExist:
            pass

    return render(request, 'contact_store.html', {
        'subbranch_email': subbranch_email,
        'cart_items': CartItem.objects.filter(cart__user=request.user) if request.user.is_authenticated else [],
        'wishlist_items': Wishlist.objects.filter(user=request.user) if request.user.is_authenticated else []
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile

        # Update user email
        user.email = request.POST.get('email', user.email)
        user.save()

        # Update profile fields
        profile.full_name = request.POST.get('full_name', profile.full_name)
        profile.mobile = request.POST.get('mobile', profile.mobile)
        profile.state = request.POST.get('state', profile.state)
        profile.city = request.POST.get('city', profile.city)
        profile.zipcode = request.POST.get('zipcode', profile.zipcode)
        profile.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def update_profile_photo(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        profile = request.user.profile
        profile.photo = request.FILES['photo']
        profile.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            user_zipcode = request.user.profile.zipcode
            subbranch = Subbranch.objects.filter(zip_code=user_zipcode).first()
            if subbranch:
                message = Message.objects.create(
                    sender=request.user,
                    subbranch=subbranch,
                    subject=request.POST.get('subject'),
                    message=request.POST.get('message')
                )
                return JsonResponse({
                    'success': True,
                    'message': 'Message sent successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'No subbranch found for your area.'
                })
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

@login_required
def subbranch_messages(request):
    if not hasattr(request.user, 'subbranch'):
        return redirect('customer:product1')
    messages = Message.objects.filter(subbranch=request.user.subbranch).order_by('-created_at')
    return render(request, 'subbranch_messages.html', {
        'messages': messages,
        'unread_count': messages.filter(is_read=False).count()
    })

@login_required
def mark_message_read(request, message_id):
    if request.method == 'POST' and hasattr(request.user, 'subbranch'):
        message = get_object_or_404(Message, id=message_id, subbranch=request.user.subbranch)
        message.is_read = True
        message.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def reply_to_message(request, message_id):
    if request.method == 'POST':
        try:
            subbranch = Subbranch.objects.get(user=request.user)
            message = Message.objects.get(id=message_id, subbranch=subbranch)
            data = json.loads(request.body)
            reply_text = data.get('reply')
            if reply_text:
                message.reply = reply_text
                message.replied_at = timezone.now()
                message.save()
                subject = f"Reply to your message: {message.subject}"
                email_body = f"""
                Dear {message.sender.username},

                The store has replied to your message:

                Your original message:
                {message.message}

                Their reply:
                {reply_text}

                Best regards,
                DairyDaze Team
                """
                try:
                    send_mail(
                        subject,
                        email_body,
                        settings.DEFAULT_FROM_EMAIL,
                        [message.sender.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Failed to send email notification: {e}")
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'Reply text is required'})
        except Message.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Message not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
def review_page(request):
    """View to display the review page with all products"""
    products = Product.objects.all()
    user_reviews = Review.objects.filter(user=request.user)  # Remove active filter
    
    return render(request, 'review.html', {
        'products': products,
        'user_reviews': user_reviews,
    })

@login_required
def submit_review(request):
    """Handle the submission of a product review"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            rating = data.get('rating')
            review_text = data.get('review')

            # Validate required fields
            if not all([product_id, rating, review_text]):
                return JsonResponse({
                    'success': False,
                    'message': 'Please fill in all fields'
                })

            # Validate rating
            try:
                rating = int(rating)
                if not (1 <= rating <= 5):
                    raise ValueError
            except (TypeError, ValueError):
                return JsonResponse({
                    'success': False,
                    'message': 'Rating must be between 1 and 5'
                })

            # Get the product
            product = get_object_or_404(Product, id=product_id)

            # Create or update the review
            review, created = Review.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={
                    'rating': rating,
                    'review': review_text,
                    'active': True
                }
            )

            return JsonResponse({
                'success': True,
                'message': 'Review submitted successfully!'
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request format'
            })
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Product not found'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            })

    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

@login_required
def settings_page(request):
    return render(request, 'settings.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Log the user out
        logout(request)
        # Delete the user account
        user.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@csrf_exempt
def check_payment_status(request, payment_id):
    return JsonResponse({'status': 'ok', 'payment_id': payment_id})

def payment_success(request):
    return render(request, 'payment_success.html')

# Create your views here.