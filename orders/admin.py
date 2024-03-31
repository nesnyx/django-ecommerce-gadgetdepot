from django.contrib import admin
from orders.models import Order,Payment,OrderProduct
# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user','product', 'qty','product_price', 'ordered')
    extra = 0

class PaymentConfig(admin.ModelAdmin):
    list_display = ['user', 'payment_id','amount_paid', 'status']

class OrderConfig(admin.ModelAdmin):
    list_display = ['first_name','order_number','status','is_ordered']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name','last_name','phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Order,OrderConfig)
admin.site.register(Payment,PaymentConfig)
admin.site.register(OrderProduct)