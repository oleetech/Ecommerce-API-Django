from django.contrib import admin
from .models import Product, Category, Tag, Image

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

admin.site.register(Tag, TagAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'src', 'name', 'alt')

admin.site.register(Image, ImageAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'price')
    list_filter = ('status', 'catalog_visibility', 'tax_status')
    search_fields = ('name',)
    filter_horizontal = ('categories', 'tags', 'images')
    readonly_fields = ('date_created', 'date_created_gmt', 'date_modified', 'date_modified_gmt', 'total_sales')

admin.site.register(Product, ProductAdmin)
