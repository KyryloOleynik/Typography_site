from django.contrib import admin
from .models import News
from .forms import NewsForm

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "related_to_store")
    search_fields = ("title",)
    list_filter = ("created_at", "related_to_store")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    prepopulated_fields = {'slug': ('title',)}
    form = NewsForm