from django.contrib import admin
from .models import *
# Register your models here.


class CategroyAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status']
    list_filter = ['category']


admin.site.register(Category, CategroyAdmin)
admin.site.register(Product, ProductAdmin)
