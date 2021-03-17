from django.contrib import admin
from .models import Product, Order, Category, University

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(University)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created', 'updated']
