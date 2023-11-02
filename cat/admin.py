from django.contrib import admin
from .models import Category, CoffeeItem

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name', )}
    list_display = ('category_name', 'coffee', 'updated_at')
    search_fields = ('category_name', 'coffee__coffee_name')

class CoffeeItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('coffee_name', )}
    list_display = ('coffee_name', 'category', 'coffee', 'price', 'is_available', 'updated_at')
    search_fields = ('coffee_name', 'category__category_name', 'price')
    list_filter = ('is_available',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(CoffeeItem, CoffeeItemAdmin)

