from django.urls import path
from carts import views
urlpatterns = [
    path('', view=views.cart,name='cart_page'),
    path('add_cart/<int:product_id>/', view=views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/<int:spec_id>', view=views.remove_cart,name='remove_cart'),
    path('increase_cart/<int:product_id>/<int:spec_id>', view=views.increase_cart,name='increase_cart'),
    path('decrease_cart/<int:product_id>/<int:spec_id>', view=views.decrease_cart,name='decrease_cart'),
    path('checkout/',view=views.checkout,name='checkout')
]
