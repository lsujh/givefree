from django.contrib import admin
from .models import Category, Things
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter


class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'slug', 'parent', 'id',)
    list_display_links = ('slug',)
    list_filter = (('parent', TreeRelatedFieldListFilter),)
    prepopulated_fields = {'slug': ('name',)}


class ThingsAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ('name', 'category', 'quantity', 'price', 'created', 'is_active', 'id')
    list_display_links = ('name', 'category',)
    list_editable = ('is_active', 'quantity', 'price')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = (('category', TreeRelatedFieldListFilter),)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Things, ThingsAdmin)
