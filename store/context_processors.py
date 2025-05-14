from .models import CartItem
from customer.models import Wishlist

def cart_wishlist_count(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(cart__user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return {
            'cart_count': cart_count,
            'wishlist_count': wishlist_count
        }
    return {
        'cart_count': 0,
        'wishlist_count': 0
    } 