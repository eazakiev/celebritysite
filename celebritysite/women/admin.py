from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Women


class WomenAdmin(admin.ModelAdmin):
    """Класс WomenAdmin.
    Args:
        admin (class): _description_
    """
    list_display = ('id', 'title', 'time_create',
                    'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        """Возвращает HTML-код фотографии."""
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    """Класс CategoryAdmin.
    Args:
        admin (class): _description_
    """
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админка сайта о женщинах'
admin.site.site_header = 'Административная панель'
