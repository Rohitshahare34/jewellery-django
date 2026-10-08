from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from shop.models import Product, Category


class Campaign(models.Model):
    THEME_CHOICES = [
        ('GOLD', 'Royal Gold Festive'),
        ('RED', 'Ruby Red Festival'),
        ('DARK', 'Midnight Dark Gold'),
        ('EMERALD', 'Emerald Luxury'),
    ]

    MEDIA_TYPE_CHOICES = [
        ('IMAGE', 'Photo / Banner Image'),
        ('VIDEO', 'Video (MP4 / Reel)'),
    ]

    INLINE_MEDIA_CHOICES = [
        ('NONE', 'No Media (Text & Timer Only)'),
        ('IMAGE', 'Photo / Banner Image'),
        ('VIDEO', 'Video (MP4 / Reel)'),
    ]

    name = models.CharField(max_length=200, help_text="Campaign Title (e.g., Diwali Dhamaka Offer 2026)")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    headline = models.CharField(max_length=255, blank=True, null=True, default="", help_text="Headline for campaign offer")
    sub_headline = models.TextField(blank=True, null=True, default="", help_text="Sub-headline for campaign offer")
    
    is_active = models.BooleanField(default=False, help_text="Master toggle to activate or deactivate this campaign globally.")
    start_date = models.DateTimeField(null=True, blank=True, help_text="Optional campaign launch start time.")
    end_date = models.DateTimeField(null=True, blank=True, help_text="Campaign expiry time used for the real-time countdown timer.")
    
    theme_style = models.CharField(max_length=30, choices=THEME_CHOICES, default='GOLD', help_text="Visual accent theme for promotional components.")
    
    banner_image = models.ImageField(upload_to='campaigns/banners/', blank=True, null=True, help_text="Hero banner graphic for campaign landing section")
    
    # Popup Modal Media Options
    popup_media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='IMAGE', help_text="Display Photo or Video in popup modal")
    popup_image = models.ImageField(upload_to='campaigns/popups/', blank=True, null=True, help_text="Special popup modal banner image")
    popup_video = models.FileField(upload_to='campaigns/popup_videos/', blank=True, null=True, help_text="Special popup modal video (MP4 format)")
    
    promo_code = models.CharField(max_length=50, blank=True, null=True, help_text="Featured promotional code (e.g., FESTIVE15)")
    discount_label = models.CharField(max_length=100, blank=True, null=True, default="", help_text="Discount badge text")
    discount_details = models.TextField(blank=True, null=True, default="", help_text="Discount details description")
    
    # --- Modular Feature Toggles ---
    show_top_announcement = models.BooleanField(default=True, help_text="Show sticky announcement bar on top of website navbar")
    announcement_text = models.CharField(max_length=255, blank=True, null=True, default="", help_text="Top announcement text")
    announcement_link_text = models.CharField(max_length=50, blank=True, null=True, default="", help_text="Link button label")
    
    show_countdown_timer = models.BooleanField(default=True, help_text="Display real-time countdown timer widget")
    show_popup_modal = models.BooleanField(default=False, help_text="Display promotional popup modal on home/shop pages")
    show_floating_video = models.BooleanField(default=False, help_text="Display floating widget on bottom corner of screen")
    show_inline_card = models.BooleanField(default=False, help_text="Show wide promotional campaign card under Signature Collections on homepage")
    
    # Floating Widget Media Options (Video or Photo)
    floating_media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='VIDEO', help_text="Display Video or Photo in floating widget")
    floating_image = models.ImageField(upload_to='campaigns/floating_images/', blank=True, null=True, help_text="Floating widget photo/image")
    floating_video = models.FileField(upload_to='campaigns/videos/', blank=True, null=True, help_text="Short promotional video/reel (MP4 format)")
    floating_video_title = models.CharField(max_length=150, blank=True, null=True, default="", help_text="Floating video reel title")
    
    # Inline Card Options
    INLINE_POSITION_CHOICES = [
        ('ABOVE', 'Above Signature Collections'),
        ('BELOW', 'Below Signature Collections'),
    ]
    inline_card_position = models.CharField(max_length=10, choices=INLINE_POSITION_CHOICES, default='ABOVE', help_text="Choose whether inline card shows Above or Below Signature Collections section")
    inline_media_type = models.CharField(max_length=10, choices=INLINE_MEDIA_CHOICES, default='NONE', help_text="Display Photo, Video, or Text-only inside inline campaign card")
    inline_image = models.ImageField(upload_to='campaigns/inline_images/', blank=True, null=True, help_text="Inline card photo/image (Recommended aspect ratio ~4:3)")
    inline_video = models.FileField(upload_to='campaigns/inline_videos/', blank=True, null=True, help_text="Inline card video (MP4 format)")
    card_background_image = models.ImageField(upload_to='campaigns/card_bg/', blank=True, null=True, help_text="Optional background image for the inline campaign banner box")
    
    # --- Hero Section Override Options ---
    HERO_DISPLAY_CHOICES = [
        ('EXISTING', 'Existing Website Hero'),
        ('CAMPAIGN', 'Campaign Promotional Hero'),
        ('HIDE', 'Hide Hero Section Entirely'),
    ]
    show_hero_override = models.BooleanField(default=False, help_text="Master toggle to enable campaign promotional hero section")
    hero_display_type = models.CharField(max_length=20, choices=HERO_DISPLAY_CHOICES, default='EXISTING', help_text="Choose whether to show normal website hero or campaign hero")
    hero_show_text_overlay = models.BooleanField(default=True, help_text="Display text overlay, title, countdown & CTA on top of promotional hero media")
    
    hero_desktop_media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='IMAGE', help_text="Desktop Hero Media Type (Photo or Video)")
    hero_desktop_image = models.ImageField(upload_to='campaigns/hero_desktop/', blank=True, null=True, help_text="Promotional Hero graphic for Desktop (Recommended: 1920x960 px)")
    hero_desktop_video = models.FileField(upload_to='campaigns/hero_desktop_videos/', blank=True, null=True, help_text="Promotional Hero video for Desktop (MP4 format)")
    
    hero_mobile_media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='IMAGE', help_text="Mobile Hero Media Type (Photo or Video)")
    hero_mobile_image = models.ImageField(upload_to='campaigns/hero_mobile/', blank=True, null=True, help_text="Promotional Hero graphic for Mobile (Recommended: 1080x1350 px)")
    hero_mobile_video = models.FileField(upload_to='campaigns/hero_mobile_videos/', blank=True, null=True, help_text="Promotional Hero video for Mobile (MP4 format)")
    
    # --- Product & Category Scope ---
    featured_products = models.ManyToManyField(Product, blank=True, related_name="campaign_promotions", help_text="Products featured in this festival campaign")
    target_categories = models.ManyToManyField(Category, blank=True, related_name="campaign_promotions", help_text="Categories linked to this campaign")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Festival Campaign"
        verbose_name_plural = "Festival & Promotion Campaigns"
        ordering = ['-created_at']

    def __str__(self):
        status_str = "ACTIVE" if self.is_currently_active() else "INACTIVE"
        return f"{self.name} [{status_str}]"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "campaign"
            slug = base_slug
            counter = 1
            while Campaign.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def is_currently_active(self):
        """Check if campaign is marked active and within start/end dates if configured."""
        if not self.is_active:
            return False
        now = timezone.now()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True

    def get_end_date_iso(self):
        """Return ISO string format for JavaScript countdown initialization."""
        if self.end_date:
            return self.end_date.isoformat()
        return ""

    def get_start_date_iso(self):
        """Return ISO string format for campaign start date."""
        if self.start_date:
            return self.start_date.isoformat()
        return ""

    def banner_url(self):
        if self.banner_image:
            return self.banner_image.url
        return ""

    def popup_url(self):
        if self.popup_image:
            return self.popup_image.url
        return ""


class PromotionalCoupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('PERCENT', 'Percentage Off (%)'),
        ('FLAT', 'Flat Amount Off (₹)'),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='coupons')
    code = models.CharField(max_length=50, unique=True, help_text="Unique promo code entered by customer at checkout")
    title = models.CharField(max_length=100, blank=True, help_text="Short label for coupon offer")
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='PERCENT')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Discount value in % or ₹")
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Minimum cart total to apply coupon")
    
    is_active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(default=1000, help_text="Max times this coupon can be redeemed")
    used_count = models.PositiveIntegerField(default=0)
    
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Promotional Coupon"
        verbose_name_plural = "Promotional Coupons"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} ({self.get_discount_type_display()} - {self.discount_value})"

    def is_valid(self, cart_total=0):
        if not self.is_active:
            return False, "This coupon is currently inactive."
        if self.used_count >= self.usage_limit:
            return False, "This coupon limit has been reached."
        now = timezone.now()
        if self.valid_from and now < self.valid_from:
            return False, "This coupon is not valid yet."
        if self.valid_to and now > self.valid_to:
            return False, "This coupon has expired."
        if cart_total < self.minimum_order_amount:
            return False, f"Minimum order amount of ₹{self.minimum_order_amount:,.2f} required for this coupon."
        return True, "Coupon applied successfully!"

    def calculate_discount(self, cart_total):
        valid, msg = self.is_valid(cart_total)
        if not valid:
            return 0
        if self.discount_type == 'PERCENT':
            return (float(cart_total) * float(self.discount_value)) / 100.0
        else:
            return min(float(self.discount_value), float(cart_total))
