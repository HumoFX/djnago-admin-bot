from django.contrib import admin
from .models import Product, Order, Category, University

admin.site.register(Category)
admin.site.register(University)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'category', 'author','deep_link']
    list_editable = ['title','author','category']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created', 'updated']
