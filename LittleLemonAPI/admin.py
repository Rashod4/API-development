from django.contrib import admin
from .models import Category, Cart, MenuItem, OrderItem, Order
# Register your models here.
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)