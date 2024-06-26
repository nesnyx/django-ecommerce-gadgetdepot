from django.shortcuts import render,redirect
from orders.models import Payment
from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order,OrderProduct
from store.models import Specification,Product
import datetime
import json
import ast
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import JsonResponse

def payments(request,total =0, quantity = 0):
    body_text = request.body
    json_data = json.loads(json.dumps(body_text.decode('utf-8')))
    if not json_data:
         pass
    else:
        json_string_decode = ast.literal_eval(json_data)
        
        order_amount = Order.objects.get(user=request.user, is_ordered=False, order_number=json_string_decode['orderID'])
        # Stora transaction details payment model
        payment = Payment(
            user = request.user,
            payment_id = json_string_decode['transID'],
            payment_method = json_string_decode['payment_method'],
            amount_paid = order_amount.order_total,
            status = json_string_decode['status']
        )
        payment.save()
        order_amount.payment = payment
        order_amount.is_ordered = True
        
        order_amount.save()
        
        # Reduce Quantity
        cartItems = CartItem.objects.filter(user=request.user)
        for item in cartItems:
            orderProduct = OrderProduct()
            orderProduct.order_id = order_amount.id
            orderProduct.payment = payment
            orderProduct.user_id = request.user.id
            orderProduct.product = item.product
            orderProduct.qty = item.quantity
            orderProduct.specification = item.spec
            orderProduct.product_price = order_amount.order_total
            orderProduct.ordered = True
            orderProduct.save()

            # cart_item = CartItem.objects.get(id=item.id)
            # specify = cart_item.spec.all()
            # order_product = OrderProduct.objects.get(id=orderProduct.id)
            # order_product.specification.set(specify)
            # order_product.save()

            #reduce qty
            product = Product.objects.get(id=item.product_id)
            product.qty -= item.quantity
            product.save()
        # Clear Cart
        CartItem.objects.filter(user = request.user).delete()
            
        # Send order received email to customer
        mail_subject = "Thank You For Your Order!"
        message = render_to_string("orders/order_recieved_email.html", {
                "user" : request.user,
                'order': order_amount
                
            })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

    data = {
        'order_number' : order_amount.order_number,
        'transID' : payment.payment_id
    }
        # Send order number and trasancition id back to sendData method 
    
    return JsonResponse(data)


# Create your views here.
def place_order(request,total =0, quantity = 0): 
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    tax = 0
    grand_total = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
    if cart_count <= 0 :
        return redirect('store_page')
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #generated order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user, is_ordered = False,order_number=order_number)
            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total
            }
            return render(request,'orders/payments.html',context)
    else:
        return redirect('checkout')
    
            
 

def order_completed(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number = order_number, is_ordered = True)
        order_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        for i in order_products:
            subtotal += i.product_price * i.qty
        payment = Payment.objects.get(payment_id=transID)
        context = {
            'order' : order,
            'order_product' : order_products,
            'order_number' : order.order_number,
            'transID' : payment.payment_id,
            'payment' : payment,
            'subtotal' : subtotal
        }
        return render(request, 'orders/order_completed.html',context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home_page')
    