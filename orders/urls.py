from django.urls import path
from orders import views

urlpatterns = [
    path('place-order/', view=views.place_order,name='place_order'),
    path('payments/',view=views.payments,name='payments'),
    path('order-completed/', view=views.order_completed, name='order_completed')
]
