# shop/admin.py
from django.contrib import admin
from .models import Jewellery, JewelleryImage, SubCategory
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from .models import (
    Category,
    SubCategory,
    Product,
    ProductImage,
    Jewellery,
    JewelleryImage,
    MetalPrice
)

# -----------------------------
# ADMIN SITE SETTINGS
# -----------------------------
admin.site.site_header = "Aashutosh Jewelerys Admin"
admin.site.site_title = "Aashutosh Jewelerys Admin Portal"
admin.site.index_title = "Welcome to Aashutosh Jewelerys Admin"

# Safely unregister default LogEntry to declutter admin
try:
    admin.site.unregister(LogEntry)
except admin.sites.NotRegistered:
    pass


# -----------------------------
# CATEGORY ADMIN
# -----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')
    search_fields = ('name',)

    def image_preview(self, obj):
        """Show category image thumbnail in admin."""
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:5px; object-fit:cover;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Image Preview"


# -----------------------------
# SUBCATEGORY ADMIN
# -----------------------------
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'image_preview')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:5px; object-fit:cover;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Image Preview"


# -----------------------------
# PRODUCT IMAGE INLINE
# -----------------------------
class ProductImageInline(admin.TabularInline):
    """Inline for adding multiple images to a Product."""
    model = ProductImage
    extra = 3
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:5px; object-fit:cover;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


# -----------------------------
# PRODUCT ADMIN
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'subcategory', 'metal_type', 'gold_purity', 'is_available')
    search_fields = ('name', 'subcategory__name')
    list_filter = ('subcategory', 'metal_type', 'gold_purity', 'is_available')
    inlines = [ProductImageInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'price', 'subcategory', 'description', 'image', 'badge', 'is_available')
        }),
        ('Metal Details', {
            'fields': ('metal_type', 'gold_purity', 'gold_weight'),
            'classes': ('collapse',),
        }),
        ('Diamond Details', {
            'fields': ('diamond_weight', 'diamond_clarity', 'diamond_color'),
            'classes': ('collapse',),
        }),
        ('General Details', {
            'fields': ('occasion', 'collection'),
            'classes': ('collapse',),
        }),
        ('Price Breakdown', {
            'fields': ('gold_value', 'stone_value', 'making_charges', 'gst'),
            'classes': ('collapse',),
        }),
    )


# -----------------------------
# JEWELLERY IMAGE INLINE
# -----------------------------
class JewelleryImageInline(admin.TabularInline):
    """Inline for adding multiple images to Jewellery."""
    model = JewelleryImage
    extra = 3
    fields = ('image', 'alt_text', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" width="80" style="object-fit:cover;border-radius:5px;"/>',
                obj.image.url
            )
        return ""

    image_preview.short_description = "Preview"


# -----------------------------
# JEWELLERY ADMIN
# -----------------------------
class JewelleryImageInline(admin.TabularInline):
    model = JewelleryImage
    extra = 1

@admin.register(Jewellery)
class JewelleryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'subcategory', 'get_category', 'metal_type', 
        'display_purity', 'price', 'is_featured', 'badge', 
        'stone_type', 'in_stock', 'image_preview'
    )
    search_fields = (
        'name', 
        'subcategory__name', 
        'subcategory__category__name'
    )
    list_filter = (
        'metal_type', 
        'subcategory__category', 
        'is_featured', 
        'badge', 
        'stone_type', 
        'color'
    )
    readonly_fields = ('total_price',)
    inlines = [JewelleryImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'subcategory', 'description', 'badge', 'is_featured', 'in_stock', 'image')
        }),
        ('Jewellery Details', {
            'fields': (
                'metal_type',
                'gold_purity', 'silver_purity',
                'gold_weight', 'diamond_weight',
                'diamond_clarity', 'diamond_color',
                'stone_type', 'color'
            ),
            'classes': ('collapse',),
        }),
        ('Price Breakdown', {
            'fields': ('gold_value', 'stone_value', 'making_charges', 'gst', 'total_price', 'price'),
            'classes': ('collapse',),
        }),
    )

    # ✅ Automatically assign category when saving Jewellery
    def save_model(self, request, obj, form, change):
        if obj.subcategory and hasattr(obj.subcategory, 'category'):
            obj.category = obj.subcategory.category
        super().save_model(request, obj, form, change)

    # ✅ Show category column in admin list
    def get_category(self, obj):
        return obj.subcategory.category.name if obj.subcategory and obj.subcategory.category else "-"
    get_category.short_description = "Category"

    # ✅ Show purity dynamically based on metal type
    def display_purity(self, obj):
        if obj.metal_type == 'GOLD':
            return obj.gold_purity or "-"
        elif obj.metal_type == 'SILVER':
            return obj.silver_purity or "-"
        return "-"
    display_purity.short_description = "Purity"

    # ✅ Image preview for list view
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:5px;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Image Preview"

    class Media:
        # JS for live total price calculation
        js = ('shop/js/admin_jewellery.js',)


# -----------------------------
# METAL PRICE ADMIN
# -----------------------------
@admin.register(MetalPrice)
class MetalPriceAdmin(admin.ModelAdmin):
    list_display = ('metal_type', 'price_per_gram', 'currency', 'change_percent', 'is_up_indicator', 'last_updated')
    list_filter = ('metal_type',)
    readonly_fields = ('last_updated',)
    search_fields = ('metal_type',)
    
    def is_up_indicator(self, obj):
        """Show arrow indicator for price direction."""
        if obj.is_up:
            return format_html('<span style="color: green;">▲ UP</span>')
        else:
            return format_html('<span style="color: red;">▼ DOWN</span>')
    
    is_up_indicator.short_description = "Trend"
    
    class Meta:
        verbose_name = "Metal Price"
        verbose_name_plural = "Metal Prices"
