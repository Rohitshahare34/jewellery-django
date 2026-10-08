from django.contrib import admin
from django.utils.html import format_html
from .models import Campaign, PromotionalCoupon


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    change_form_template = 'admin/promotions/campaign/change_form.html'

    class Media:
        css = {
            'all': ('promotions/css/campaign_admin.css',)
        }
        js = ('promotions/js/campaign_admin.js',)

    list_display = (
        'name',
        'theme_style',
        'is_active_badge',
        'show_hero_override',
        'hero_display_type',
        'start_date',
        'end_date',
        'show_top_announcement',
        'show_countdown_timer',
        'show_popup_modal',
        'show_floating_video',
        'show_inline_card',
        'created_at',
    )
    list_filter = (
        'is_active',
        'show_hero_override',
        'hero_display_type',
        'theme_style',
        'show_top_announcement',
        'show_countdown_timer',
        'show_popup_modal',
        'show_floating_video',
        'show_inline_card',
    )
    search_fields = ('name', 'headline', 'promo_code', 'announcement_text')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('featured_products', 'target_categories')
    readonly_fields = ('desktop_hero_preview', 'mobile_hero_preview')
    
    fieldsets = (
        ('Section 1 — Campaign Information', {
            'fields': ('name', 'slug', 'headline', 'sub_headline', 'is_active', 'theme_style')
        }),
        ('Section 2 — Hero Section Override ⭐', {
            'fields': (
                'show_hero_override',
                'hero_display_type',
                'hero_show_text_overlay',
                'hero_desktop_media_type',
                'hero_desktop_image',
                'hero_desktop_video',
                'desktop_hero_preview',
                'hero_mobile_media_type',
                'hero_mobile_image',
                'hero_mobile_video',
                'mobile_hero_preview',
            ),
            'description': (
                'Optionally replace the normal website Hero section with a festival promotional Hero during campaign start/end dates. '
                'Provide separate media for Desktop (Recommended 1920x960 px, ~2:1) and Mobile (Recommended 1080x1350 px, ~4:5).'
            )
        }),
        ('Section 3 — Schedule & Timing', {
            'fields': ('start_date', 'end_date'),
            'description': 'Configure launch and expiry dates. The countdown timer automatically targets the End Date.'
        }),
        ('Section 4 — Offers & Promo Code', {
            'fields': ('promo_code', 'discount_label', 'discount_details')
        }),
        ('Section 5 — Additional Promotions', {
            'fields': (
                'show_top_announcement', 'announcement_text', 'announcement_link_text',
                'show_countdown_timer',
                'show_inline_card', 'inline_card_position', 'card_background_image',
                'show_popup_modal', 'popup_media_type', 'popup_image', 'popup_video',
                'show_floating_video', 'floating_media_type', 'floating_image', 'floating_video', 'floating_video_title'
            ),
            'description': 'Configure sticky announcement bar, inline homepage card position & custom background image, popup modal, and floating reel widget.'
        }),
        ('Section 6 — Campaign Banner Media', {
            'fields': ('banner_image',)
        }),
        ('Section 7 — Product & Category Targeting', {
            'fields': ('featured_products', 'target_categories'),
            'description': 'Select products and categories highlighted in this festival campaign.'
        }),
    )

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            from django.utils import timezone
            obj = self.get_object(request, object_id)
            if obj:
                now = timezone.now()
                status_label = "DRAFT"
                status_color = "#6c757d"
                
                if obj.is_active:
                    if obj.start_date and now < obj.start_date:
                        status_label = "SCHEDULED"
                        status_color = "#17a2b8"
                    elif obj.end_date and now > obj.end_date:
                        status_label = "EXPIRED"
                        status_color = "#dc3545"
                    else:
                        status_label = "LIVE"
                        status_color = "#28a745"
                else:
                    status_label = "DISABLED"
                    status_color = "#6c757d"

                time_remaining = ""
                if obj.end_date and now < obj.end_date:
                    diff = obj.end_date - now
                    days = diff.days
                    hours = diff.seconds // 3600
                    mins = (diff.seconds % 3600) // 60
                    time_remaining = f"{days} Days {hours} Hours {mins} Minutes"
                elif obj.end_date and now >= obj.end_date:
                    time_remaining = "Campaign Expired"

                is_desktop_ready = bool(obj.hero_desktop_image or obj.hero_desktop_video)
                is_mobile_ready = bool(obj.hero_mobile_image or obj.hero_mobile_video)

                extra_context['campaign_summary'] = {
                    'name': obj.name,
                    'headline': obj.headline,
                    'is_active': obj.is_active,
                    'status_label': status_label,
                    'status_color': status_color,
                    'time_remaining': time_remaining,
                    'is_desktop_ready': is_desktop_ready,
                    'is_mobile_ready': is_mobile_ready,
                    'is_hero_ready': is_desktop_ready and is_mobile_ready,
                    'start_date': obj.start_date,
                    'end_date': obj.end_date,
                }
        return super().changeform_view(request, object_id, form_url, extra_context)

    def desktop_hero_preview(self, obj):
        if not obj or not (obj.hero_desktop_image or obj.hero_desktop_video):
            return format_html('<span style="color: #888;">No Desktop Hero media uploaded yet. Recommended: 1920×960 px (~2:1 aspect ratio)</span>')
        
        media_html = ""
        if obj.hero_desktop_media_type == 'VIDEO' and obj.hero_desktop_video:
            media_html = f'<video src="{obj.hero_desktop_video.url}" controls muted style="width: 100%; max-height: 180px; object-fit: cover; border-radius: 8px;"></video>'
        elif obj.hero_desktop_image:
            media_html = f'<img src="{obj.hero_desktop_image.url}" style="width: 100%; max-height: 180px; object-fit: cover; border-radius: 8px;" />'
            
        return format_html(
            '<div style="background: #151515; padding: 12px; border-radius: 10px; border: 1px solid #d4af37; max-width: 420px;">'
            '<div style="color: #ffd700; font-weight: bold; font-size: 0.85rem; margin-bottom: 6px;">💻 DESKTOP HERO PREVIEW <span style="background: #28a745; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; float: right;">✓ Good fit</span></div>'
            f'{media_html}'
            '<div style="color: #aaa; font-size: 0.75rem; margin-top: 6px;">Target Container: Full Width (calc(111.11vh + 80px)) | Aspect Ratio: ~16:9 - 21:9</div>'
            '</div>'
        )
    desktop_hero_preview.short_description = "Desktop Hero Preview & Dimensions"

    def mobile_hero_preview(self, obj):
        if not obj or not (obj.hero_mobile_image or obj.hero_mobile_video):
            return format_html('<span style="color: #888;">No Mobile Hero media uploaded yet. Recommended: 1080×1350 px (~4:5 portrait aspect ratio)</span>')
        
        media_html = ""
        if obj.hero_mobile_media_type == 'VIDEO' and obj.hero_mobile_video:
            media_html = f'<video src="{obj.hero_mobile_video.url}" controls muted style="width: 100%; max-height: 220px; object-fit: cover; border-radius: 8px;"></video>'
        elif obj.hero_mobile_image:
            media_html = f'<img src="{obj.hero_mobile_image.url}" style="width: 100%; max-height: 220px; object-fit: cover; border-radius: 8px;" />'
            
        return format_html(
            '<div style="background: #151515; padding: 12px; border-radius: 10px; border: 1px solid #d4af37; max-width: 220px;">'
            '<div style="color: #ffd700; font-weight: bold; font-size: 0.85rem; margin-bottom: 6px;">📱 MOBILE HERO PREVIEW <span style="background: #28a745; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; float: right;">✓ Good fit</span></div>'
            f'{media_html}'
            '<div style="color: #aaa; font-size: 0.75rem; margin-top: 6px;">Target Container: Full Screen (calc(100vh + 80px)) | Aspect Ratio: ~4:5 - 9:16</div>'
            '</div>'
        )
    mobile_hero_preview.short_description = "Mobile Hero Preview & Dimensions"

    def is_active_badge(self, obj):
        if obj.is_currently_active():
            return format_html('<span style="background-color: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">LIVE</span>')
        return format_html('<span style="background-color: #6c757d; color: white; padding: 4px 8px; border-radius: 4px;">INACTIVE</span>')
    is_active_badge.short_description = "Status"


@admin.register(PromotionalCoupon)
class PromotionalCouponAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'title',
        'campaign',
        'discount_type',
        'discount_value',
        'minimum_order_amount',
        'used_count',
        'usage_limit',
        'is_active',
        'valid_to',
    )
    list_filter = ('is_active', 'discount_type', 'campaign')
    search_fields = ('code', 'title')
    fieldsets = (
        ('Coupon Basic Info', {
            'fields': ('campaign', 'code', 'title', 'is_active')
        }),
        ('Discount Configuration', {
            'fields': ('discount_type', 'discount_value', 'minimum_order_amount')
        }),
        ('Limits & Validity', {
            'fields': ('usage_limit', 'used_count', 'valid_from', 'valid_to')
        }),
    )
