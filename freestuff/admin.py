from django.contrib import admin
from .models import Category, Things, Images
from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter


class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'slug', 'parent', 'id',)
    list_display_links = ('slug',)
    list_filter = (('parent', TreeRelatedFieldListFilter),)
    prepopulated_fields = {'slug': ('name',)}


class ImagesInline(admin.StackedInline):
    model = Images


class ThingsAdmin(admin.ModelAdmin):
    ordering = ['-created']
    list_display = ('owner', 'name', 'category', 'quantity', 'price', 'created', 'is_active',
                    'id', 'keywords')
    list_display_links = ('name', 'category',)
    list_editable = ('is_active', 'quantity', 'price')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = (('category', TreeRelatedFieldListFilter),)
    readonly_fields = ('owner',)
    inlines = [ImagesInline]

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'category':
    #         kwargs['queryset'] = Things.objects.filter(owner=request.user)
    #
    #     return super(ThingsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

admin.site.register(Category, CategoryAdmin)
admin.site.register(Things, ThingsAdmin)
