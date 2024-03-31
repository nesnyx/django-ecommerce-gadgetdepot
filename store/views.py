from django.shortcuts import render,get_object_or_404,redirect
from store.models import Product,Specification
from category.models import Category
from carts.models import CartItem
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from store.forms import ReviewForm
from carts.views import _cart_id_session
from store.models import Review
from django.urls import reverse
from orders.models import OrderProduct
from django.contrib import messages
from store.models import Review
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login_page')
def store_page(request,category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products, 10)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()


    return render(request,'store/shop.html',{
      
        "product" : paged_products,
        'count' : product_count
    })

def product_detail(request,category_slug,product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id_session(request),product=product).exists()
        spec = Specification.objects.all()
    except Exception as e:
        raise e
    
    try:
        orderproduct = OrderProduct.objects.filter(user = request.user, product_id= product.id).exists()
    except:
        orderproduct = None

    reviews = Review.objects.filter(product_id=product.id ,status=True)
    reviews_user = Review.objects.get(user_id = request.user, product_id=product.id)

    return render(request, 'store/product_dtl.html',{
        'product' : product,
        'in_cart': in_cart,
        'spec' : spec,
        'order' :orderproduct,
        'review' : reviews,
        'user_review' : reviews_user
    })


def search(request):
    """checking has keyword or not into url"""
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)  | Q(product_name__icontains=keyword))
            product_count = product.count()
            


    return render(request, 'store/shop.html',{'product':product,'count' : product_count})


def submit_review(request, product_id):
    current_user = request.user
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = Review()
        product = Product.objects.get(id=product_id)
        # reviews = Review.objects.get(user__id=request.user.id, product__id=product_id)
        if form.is_valid():
            review = Review(
                user = current_user,
                product = product,
                subject = request.POST['subject'],
                review = request.POST['review'],
                rating = request.POST['rating'],
                ip = request.META.get('REMOTE_ADDR'),
            )
            review.save()
            messages.success(request, 'Thank you! Your reviews Has been added')
            print(product.category.slug, product.slug)

            return redirect(url)    
    

def my_orders(request): 
    return render(request, 'accounts/my_orders.html')

