from django.contrib import admin
from .models import Banner
from django.utils.html import format_html

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'text', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('image_preview',)
    search_fields = ['title', 'text', ]
    date_hierarchy = "created_at"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Превью изображения'