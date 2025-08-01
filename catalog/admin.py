from django.contrib import admin
from .models import Service, ServiceCategory, ServiceOption, ServiceOptionCategory
from django.utils.html import format_html
import nested_admin

class ServiceCategoryInline(nested_admin.NestedStackedInline):
    extra = 1
    model = ServiceCategory
    verbose_name = "Підкатегорія данної категорії"
    verbose_name_plural = "Підкатегорії данної категорії"

class ServiceOptionInline(nested_admin.NestedTabularInline):
    model = ServiceOption
    extra = 1
    verbose_name = "Опція"
    verbose_name_plural = "Опції"

class ServiceOptionCategoryInline(nested_admin.NestedStackedInline):
    model = ServiceOptionCategory
    inlines = [ServiceOptionInline]
    extra = 1
    verbose_name = "Категорія опцій"
    verbose_name_plural = "Категорії опцій"

class IsMainFilter(admin.SimpleListFilter):
    title = 'Головна категорія'
    parameter_name = 'is_main'

    def lookups(self, request, model_admin):
        return (('yes', 'так'), ('no', 'ні'))
    
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(parent__isnull=True)
        if self.value() == 'no':
            return queryset.filter(parent__isnull=False)
        return queryset

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_filter = (IsMainFilter, )
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', ]

    inlines = [ServiceCategoryInline]

    # Для отображения изображений (опционально)
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Превью изображения'

@admin.register(Service)
class ServiceAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'category', 'price_from', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active',)
    search_fields = ['title', ]

    inlines = [ServiceOptionCategoryInline]

    # Для отображения изображений (опционально)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Превью изображения'


@admin.register(ServiceOption)
class ServiceOptionAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'price')
    list_filter = ('category',)
    search_fields = ['title', ]

@admin.register(ServiceOptionCategory)
class ServiceOptionCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', )
    list_filter = ('service',)
    search_fields = ['title', ]
    inlines = [ServiceOptionInline]