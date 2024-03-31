from django.urls import path
from store import views
urlpatterns = [
    path('',views.store_page,name='store_page'),
    
    path('category/<slug:category_slug>/',views.store_page,name='products_by_category'),

    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',view=views.search,name='search'),
    path("submit_review/<int:product_id>", view=views.submit_review, name='submit_review')
    
]
