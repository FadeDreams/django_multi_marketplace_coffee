from django.contrib import admin
from .models import Coffee


class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'coffee_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'coffee_name')
    list_editable = ('is_approved', )

admin.site.register(Coffee, CoffeeAdmin)

