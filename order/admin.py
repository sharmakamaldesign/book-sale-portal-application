from django.contrib import admin
from .models import Order, OrderItem
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','total','shippingPinCode','shippingCity','created','delivered']
admin.site.register(Order, OrderAdmin)

# Register your models here.
