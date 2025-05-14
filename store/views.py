from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Product, Order
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
import razorpay
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def index(request):
    return HttpResponse("hello")

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user).select_related('product')
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
@require_POST
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            
        cart_count = CartItem.objects.filter(cart__user=request.user).count()
        
        return JsonResponse({
            'success': True,
            'cart_count': cart_count
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@require_POST
def update_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
@require_POST
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()
        
        cart_count = CartItem.objects.filter(cart__user=request.user).count()
        
        return JsonResponse({
            'success': True,
            'cart_count': cart_count
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def payment_gateway(request, payment_id):
    try:
        # Get the order
        order = get_object_or_404(Order, order_id=payment_id, customer=request.user)
        
        # Get Razorpay settings with error handling
        try:
            razorpay_key_id = settings.RAZORPAY_KEY_ID
            if not razorpay_key_id:
                raise ValueError("RAZORPAY_KEY_ID is not configured")
        except AttributeError:
            messages.error(request, "Payment gateway is not properly configured.")
            return redirect('customer:orders')
            
        # Get currency with fallback to INR
        try:
            currency = settings.RAZORPAY_CURRENCY
        except AttributeError:
            currency = 'INR'

        # Validate order amount
        if order.total <= 0:
            messages.error(request, "Invalid order amount")
            return redirect('customer:orders')

        # Create Razorpay Order with error handling
        try:
            amount_in_paise = int(order.total * 100)
            razorpay_order = razorpay_client.order.create({
                'amount': amount_in_paise,
                'currency': currency,
                'payment_capture': '1'
            })
            
            if not razorpay_order.get('id'):
                raise ValueError("Could not create Razorpay order")
                
        except Exception as e:
            messages.error(request, f"Error creating Razorpay order: {str(e)}")
            return redirect('customer:orders')
        
        context = {
            'order': order,
            'razorpay_key_id': razorpay_key_id,
            'order_amount': amount_in_paise,
            'currency': currency,
            'razorpay_order_id': razorpay_order['id'],
            'cart_items': request.user.cart.items.all() if hasattr(request.user, 'cart') else [],
            'wishlist_items': [item.product.id for item in request.user.wishlist.items.all()] if hasattr(request.user, 'wishlist') else [],
        }
        
        return render(request, 'payment_gateway.html', context)
        
    except Exception as e:
        messages.error(request, f"An error occurred while processing your payment: {str(e)}")
        return redirect('customer:orders')

@csrf_exempt
@login_required
def razorpay_payment_verify(request, order_id):
    if request.method == "POST":
        try:
            # Get the order instance
            order = get_object_or_404(Order, order_id=order_id, customer=request.user)
            
            # Get payment verification data
            payment_data = {
                'razorpay_order_id': request.POST.get('razorpay_order_id'),
                'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
                'razorpay_signature': request.POST.get('razorpay_signature')
            }
            
            # Verify signature
            try:
                razorpay_client.utility.verify_payment_signature(payment_data)
                
                # Update order status
                order.payment_status = 'Paid'
                order.payment_method = 'Razorpay'
                order.payment_id = payment_data['razorpay_payment_id']
                order.save()
                
                # Clear cart
                Cart.objects.filter(user=request.user).delete()
                
                messages.success(request, 'Payment successful! Your order has been confirmed.')
                return redirect('store:payment_success')
                
            except Exception as e:
                order.payment_status = 'Failed'
                order.save()
                messages.error(request, 'Payment verification failed. Please try again or contact support.')
                return redirect('store:payment_failed')
                
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
            return redirect('customer:orders')
        except Exception as e:
            messages.error(request, 'An error occurred while processing your payment. Please try again.')
            return redirect('store:payment_failed')
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')