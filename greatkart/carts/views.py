from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect


from store.models import Variation
from .models import CartItem,Cart
from store.models import Product
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart_id(request):

    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_slug):
    product = Product.objects.get(slug = product_slug)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(product=product,user=request.user)
        product_variation = []

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    
                except:
                    pass
        
        
            if len(product_variation) > 0:
                for items in product_variation:
                    cart_item = cart_item.filter(
                        variations__exact=items,
                    )
        print(cart_item, product_variation)
                
        if cart_item.exists():
            print(cart_item)
            order_item = cart_item.first()
            print(order_item)
            order_item.quantity += 1
            order_item.save()

        # is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
        # if is_cart_item_exists:
        #     cart_item = CartItem.objects.filter(product=product, cart=cart)
        #     ex_var_list = []
        #     id = []
        #     for item in cart_item:
        #         existing_variation = item.variations.all()
        #         ex_var_list.append(list(existing_variation))
        #         id.append(item.id)

        #         if product_variation in ex_var_list:
        #             # increase the cart item quantity
        #             index = ex_var_list.index(product_variation)
        #             item_id = id[index]
        #             item = CartItem.objects.get(product=product, id=item_id)
        #             item.quantity += 1
        #             item.save()

        else:
            item = CartItem.objects.create(product=product, quantity=1, user=request.user)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
                item.save()
        return redirect('cart')
    else:
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
        cart_item = CartItem.objects.filter(product=product,cart=cart)
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    
                except:
                    pass
        
        
            if len(product_variation) > 0:
                for items in product_variation:
                    cart_item = cart_item.filter(
                        variations__exact=items,
                    )
        print(cart_item, product_variation)
                
        if cart_item.exists():
            print(cart_item)
            order_item = cart_item.first()
            print(order_item)
            order_item.quantity += 1
            order_item.save()

        # is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
        # if is_cart_item_exists:
        #     cart_item = CartItem.objects.filter(product=product, cart=cart)
        #     ex_var_list = []
        #     id = []
        #     for item in cart_item:
        #         existing_variation = item.variations.all()
        #         ex_var_list.append(list(existing_variation))
        #         id.append(item.id)

        #         if product_variation in ex_var_list:
        #             # increase the cart item quantity
        #             index = ex_var_list.index(product_variation)
        #             item_id = id[index]
        #             item = CartItem.objects.get(product=product, id=item_id)
        #             item.quantity += 1
        #             item.save()

        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
                item.save()
        # else:
        #     cart_item = CartItem.objects.create(
        #          product = product,
        #         quantity = 1,
        #         cart=cart,
        #         )
        #     if len(product_variation) > 0:
        #         cart_item.variations.clear()
        #         cart_item.variations.add(*product_variation)
        #         cart_item.save()
        return redirect('cart')







def cart(request, total=0, quantity=0, cart_items=None):
    tax=0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:

            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass
    context = {
            'total':total,
            'quantity':quantity,
            'cart_items': cart_items,
            'tax'       : tax,
            'grand_total': grand_total,
        }
    return render(request, 'store/cart.html', context)
        
    
def remove_cart(request, product_slug, cart_item_id ):
    
    product = get_object_or_404(Product, slug = product_slug)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id = cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id = cart_item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_slug, cart_item_id):
    
    product = get_object_or_404(Product, slug = product_slug)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id = cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id = cart_item_id)
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request, total=0, quantity=0,cart_items=None):
    tax=0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass
    context = {
            'total':total,
            'quantity':quantity,
            'cart_items': cart_items,
            'tax'       : tax,
            'grand_total': grand_total,
        }
    return render(request, 'store/checkout.html', context)