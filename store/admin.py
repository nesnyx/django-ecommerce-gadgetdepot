from django.contrib import admin
from store.models import Product,Variation,Specification, Review
# Register your models here.
class ProductConfig(admin.ModelAdmin):
    list_display = ['product_name','slug','qty','is_available','category']
    prepopulated_fields = {
        'slug' : ('product_name',)
    }

class ReviewConfig(admin.ModelAdmin):
    list_display = ['product','user','rating','review']

class VariationConfig(admin.ModelAdmin):
    list_display = ('product','variation_category','is_active')
    
admin.site.register(Specification)
admin.site.register(Variation,VariationConfig)
admin.site.register(Product,ProductConfig)
admin.site.register(Review, ReviewConfig)