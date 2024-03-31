from django.contrib import admin
from carts import models
from store.models import Variation
class CartItemConfig(admin.ModelAdmin):
    list_display = ('product','quantity','cart','user')
    

# Register your models here.
admin.site.register(models.Cart)
admin.site.register(models.CartItem ,CartItemConfig)
