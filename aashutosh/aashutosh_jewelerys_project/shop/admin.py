# shop/admin.py
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from .models import (
    Category,
    SubCategory,
    Product,
    ProductImage,
    MetalRate,
    Wishlist,
    Testimonial,
    Reel,
    PopupMessage,
    SignatureCollection,
    SignatureCollectionItem
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
    list_display = ('name', 'sort_order', 'image_preview')
    search_fields = ('name',)
    list_editable = ('sort_order',)

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
    list_display = ('name', 'category', 'is_featured', 'sort_order', 'image_preview')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'is_featured')
    list_editable = ('is_featured', 'sort_order')

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
# PRODUCT IMAGE INLINE
# -----------------------------
class ProductImageInline(admin.TabularInline):
    """Inline for adding multiple images to Product."""
    model = ProductImage
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
# PRODUCT ADMIN
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'subcategory', 'get_category', 'metal_type', 
        'display_purity', 'price', 'is_manual_price', 'is_featured', 'badge', 
        'stone_type', 'in_stock', 'image_preview'
    )
    search_fields = (
        'name', 
        'subcategory__name', 
        'subcategory__category__name'
    )
    list_filter = (
        'is_manual_price',
        'metal_type', 
        'subcategory__category', 
        'is_featured', 
        'badge', 
        'stone_type', 
        'color'
    )
    readonly_fields = ('total_price',)
    inlines = [ProductImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'subcategory', 'description', 'badge', 'is_featured', 'in_stock', 'image')
        }),
        ('Product Details', {
            'fields': (
                'metal_type',
                'gold_purity', 'silver_purity',
                'gold_weight', 'diamond_weight',
                'diamond_clarity', 'diamond_color',
                'stone_type', 'color',
                'occasion', 'collection'
            ),
            'classes': ('collapse',),
        }),
        ('Price Breakdown', {
            'fields': ('is_manual_price', 'gold_value', 'stone_value', 'making_charges', 'gst', 'total_price', 'price'),
            'classes': ('collapse',),
        }),
    )

    # ✅ Automatically assign category when saving Product
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
# TESTIMONIAL ADMIN
# -----------------------------
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'designation', 'image_preview', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('name', 'message', 'designation')
    actions = ['approve_testimonials', 'disapprove_testimonials']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:5px;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Uploaded Image"

    def approve_testimonials(self, request, queryset):
        queryset.update(is_approved=True)
    approve_testimonials.short_description = "Approve selected testimonials"

    def disapprove_testimonials(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_testimonials.short_description = "Disapprove selected testimonials"


# -----------------------------
# REEL ADMIN
# -----------------------------
@admin.register(Reel)
class ReelAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'video_preview')
    search_fields = ('title',)
    list_filter = ('is_active', 'created_at')

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video width="100" height="100" controls><source src="{}" type="video/mp4"></video>',
                obj.video.url
            )
        return "No Video"
    video_preview.short_description = "Video Preview"


# -----------------------------
# POPUP MESSAGE ADMIN
# -----------------------------
@admin.register(PopupMessage)
class PopupMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'show_on_refresh', 'has_poster', 'created_at')
    list_filter = ('status', 'show_on_refresh', 'created_at')
    search_fields = ('title', 'message')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Popup Information', {
            'fields': ('title', 'message', 'poster_image')
        }),
        ('Display Settings', {
            'fields': ('status', 'show_on_refresh')
        }),
        ('Layout Visibility Customizations', {
            'fields': ('show_title', 'show_message', 'show_poster_image', 'show_rates_grid'),
            'description': "Control which design elements are visible in the popup."
        }),
        ('Shop Button Customization', {
            'fields': ('show_shop_button', 'shop_button_text', 'shop_button_url')
        }),
        ('Rates Button Customization', {
            'fields': ('show_rates_button', 'rates_button_text', 'rates_button_url')
        }),
        ('Calculator Button Customization', {
            'fields': ('show_calc_button', 'calc_button_text', 'calc_button_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_poster(self, obj):
        """Check if popup has a poster image"""
        if obj.poster_image:
            return format_html('<span style="color: green;">{}</span>', '✓ Has Poster')
        return format_html('<span style="color: orange;">{}</span>', 'No Poster')
    has_poster.short_description = "Poster"

    def poster_preview(self, obj):
        """Show poster thumbnail in admin"""
        if obj.poster_image:
            return format_html(
                '<img src="{}" width="200" style="border-radius: 5px; object-fit: cover;" />',
                obj.poster_image.url
            )
        return "No Poster"
    poster_preview.short_description = "Poster Preview"





# -----------------------------
# WISHLIST ADMIN
# -----------------------------
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at', 'added_time')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('created_at',)


# -----------------------------
# SIGNATURE COLLECTION ITEM INLINE
# -----------------------------
class SignatureCollectionItemInline(admin.TabularInline):
    model = SignatureCollectionItem
    extra = 3
    fields = ('title', 'description', 'image', 'image_preview', 'sort_order', 'is_active')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:5px; object-fit:cover;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Preview"


# -----------------------------
# SIGNATURE COLLECTION ADMIN
# -----------------------------
@admin.register(SignatureCollection)
class SignatureCollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle')
    inlines = [SignatureCollectionItemInline]


# -----------------------------
# METAL RATE ADMIN (Today's Rates)
# -----------------------------
@admin.register(MetalRate)
class MetalRateAdmin(admin.ModelAdmin):
    list_display = (
        'metal_type', 
        'purity', 
        'rate_per_gram', 
        'making_charge', 
        'making_type', 
        'gst_percentage', 
        'status', 
        'show_making_charge', 
        'show_gst'
    )
    list_editable = (
        'purity', 
        'rate_per_gram', 
        'making_charge', 
        'making_type', 
        'gst_percentage', 
        'status', 
        'show_making_charge', 
        'show_gst'
    )
    list_filter = ('metal_type', 'status')
    search_fields = ('metal_type',)
