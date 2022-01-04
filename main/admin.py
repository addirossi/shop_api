from django.contrib import admin

from .models import Category, Product, ProductImage


class ProductImagesInline(admin.TabularInline):
    model = ProductImage
    fields = ['image']


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
