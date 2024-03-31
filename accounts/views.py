from django.shortcuts import render,redirect,get_object_or_404
from accounts.forms import RegistrationForm
from accounts.models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from carts.models import Cart,CartItem
from carts.views import _cart_id_session
from django.http import HttpRequest
from orders.models import Order,OrderProduct
from django.db.models import Count, Avg
from accounts.forms import UserForm, UserProfileForm
from accounts.models import UserProfile
import requests
# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name,username=username,email=email,password=password)
            user.phone_number = phone_number
            user.save()
            
            # User Profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.jpeg'
            profile.save() 


            current_site = get_current_site(request)
            mail_subject = "Please activate your account!"
            message = render_to_string("accounts/accounts_verification.html", {
                "user" : user,
                "domain" : current_site,
                "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
                "token" : default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Thank you!, we have sent you an email for verification')

            return redirect('/accounts/login?command=verification&email=' + email)
    else:
        form = RegistrationForm()       
    return render(request, 'accounts/register.html',{
        'form' : form
    })


def login(request): 
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id =_cart_id_session(request))
                is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    cart_item = CartItem.objects.filter(cart=cart)
                    print(cart_item)
                    for item in cart_item:
                        print(item)
                        item.user = user
                        item.save()
                        
            except: 
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
           
            
            return redirect('dashboard_page')
            
            
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login_page')
    return render(request, 'accounts/login.html')


@login_required(login_url="login_page")
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect('login_page')



@login_required(login_url="login_page")
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id= request.user.id,is_ordered=True)
    orders_count = orders.count()
    return render(request, 'accounts/dashboard.html',
                  {'count' : orders_count})


def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your Account active Now!")
        return redirect('login_page')
    else:
        messages.error(request, "Invalid Activation link")
        return redirect('register_page')
    


def forgetPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact = email)
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string("accounts/reset_password_email.html", {
                "user" : user,
                "domain" : current_site,
                "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
                "token" : default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "Password reset email has been sent to your email address")
            return redirect('login_page')

        else:
            messages.error(request, "Account does not exist")
            return redirect('forgetPassword')
    return render(request, 'accounts/forgetpassword.html')


def resetPassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):

        request.session['uid'] = uid
        
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('login_page')
    

def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login_page')
        else:
            messages.error(request,'Password Does not Match')
            return redirect('resetPassword')
    else:

        return render(request,'accounts/resetpassword.html')
    

def my_orders(request): 
    order = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    return render(request, 'accounts/my_orders.html', {
        'orders' : order
    })


def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST , instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your Profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
         
    return render(request, 'accounts/edit_profile.html',
                  {
                      'user_form' : user_form,
                      'profile_form' : profile_form,
                      'userprofile' : userprofile
                  })

@login_required(login_url='login_page')
def order_detail(request,order_id):
    order_detail= OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    sub_total = 0
    for i in order_detail:
        sub_total += i.product_price * i.qty
    return render(request, 'accounts/order_detail.html',{
        'order_detail' : order_detail,
        'order' : order,
        'subtotal' : sub_total
    })
