from django.contrib import admin

from store.models import Product, Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'category','created_date', 'stock', 'is_available']
    prepopulated_fields = {'slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value','is_active', 'created_date']
    list_editable = ['is_active']

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
