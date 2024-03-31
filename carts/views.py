from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Specification
from carts.models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from store.models import Variation, Specification
from django.contrib.auth.decorators import login_required
from accounts.models import Account



def _cart_id_session(request):
    cart = request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart


@login_required(login_url='login_page')
def add_cart(request,product_id):
    
    product = Product.objects.get(id=product_id) #get produc
    variation_list = []
    if request.method == 'POST':
        variation_list.append(int(request.POST['specification']))

    specification = Specification.objects.get(id=variation_list[0])
    print('variation list : ',variation_list)
    # Get Cart by Cookies
    # try:
    #     cart = Cart.objects.get(cart_id=_cart_id_session(request)) # get the cart id
    # except Cart.DoesNotExist:
    #     cart=Cart.objects.create(
    #         cart_id=_cart_id_session(request)
    #     )
    # cart.save()
    # end get cart



    if request.user.is_authenticated:
        is_cart_item_exists_user = CartItem.objects.filter(user = request.user,product=product,spec=specification).exists()
        print('is exists: ',is_cart_item_exists_user)

        if is_cart_item_exists_user:
            cart_item = CartItem.objects.filter(
                    user = request.user,product=product,spec=specification
                    )
            ex_var_list= []
            id = ""
            for item in cart_item:
                existing = item.spec.id
                ex_var_list.append(existing)
                id_item = existing
            id = id_item
            print(ex_var_list)
            
            if variation_list == ex_var_list:
                
                product = get_object_or_404(Product, id=product_id)
                cart_item = CartItem.objects.get(product=product,spec=specification)
                cart_item.quantity += 1
                cart_item.save()
                
            else:
                cart_item = CartItem.objects.create(
                    user = request.user,
                    product = product,
                    
                    quantity = 1,
                    spec = specification
                )
                cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                    user = request.user,
                    product = product,
                    quantity = 1,
                    spec = specification
                )
            cart_item.save()
    
    else:
        is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart,spec=specification).exists()
        print('is exists: ',is_cart_item_exists )
        

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                    product=product,cart=cart,spec=specification
                    )
            ex_var_list= []
            id = ""
            for item in cart_item:
                existing = item.spec.id
                ex_var_list.append(existing)
                id_item = existing
            id = id_item
            print(ex_var_list)
            
            if variation_list == ex_var_list:
                
                product = get_object_or_404(Product, id=product_id)
                cart_item = CartItem.objects.get(product=product,cart=cart,spec=specification)
                cart_item.quantity += 1
                cart_item.save()
                return redirect('cart_page')
            else:
                cart_item = CartItem.objects.create(
                    
                    product = product,
                    cart = cart,
                    quantity = 1,
                    spec = specification
                )
                cart_item.save()
        else:
                cart_item = CartItem.objects.create(
                    
                    product = product,
                    cart = cart,
                    quantity = 1,
                    spec = specification
                )
                cart.save()

    return redirect('cart_page')

# cart page
@login_required(login_url='login_page')
def cart(request,total =0, quantity = 0, cart_items=None):
    try:
        tax = 0
        grand_total =0
        if request.user.is_authenticated:
            cart_items= CartItem.objects.filter(user = request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id_session(request))
            cart_items= CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'tax' : tax,
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'grand_total' : grand_total
    }
    return render(request,'store/cart_buy.html',context )



def remove_cart(request,product_id,spec_id):
    
    spec = get_object_or_404(Specification, id=spec_id)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(user=request.user,product=product,spec=spec)
    
    # if cart_item.quantity > 1:
    #     cart_item.quantity -= 1
    #     cart_item.save()
    # else:
    cart_item.delete()
    return redirect('cart_page')

def increase_cart(request,product_id,spec_id):
    spec = get_object_or_404(Specification, id=spec_id)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(user=request.user,product=product,spec=spec)
    cart_item.quantity += 1
    cart_item.save()
    
    return redirect('cart_page')

def decrease_cart(request,product_id,spec_id):
    spec = get_object_or_404(Specification, id=spec_id)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(user=request.user,product=product,spec=spec)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_page')



@login_required(login_url='login_page')
def checkout(request,total =0, quantity = 0, cart_items=None):
    try:
        # cart = Cart.objects.get(cart_id = _cart_id_session(request))
        
        cart_items= CartItem.objects.filter(user=request.user,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    context = {
        'totalWithTax' : (total + (total * 0.1)),
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items
    }
    return render(request, 'store/checkout.html',context)