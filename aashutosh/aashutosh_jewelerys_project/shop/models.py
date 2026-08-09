from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# -----------------------------
# CATEGORY MODEL
# -----------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    sort_order = models.IntegerField(default=0, help_text="Order of display (lower numbers first)")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def image_url(self):
        """Return a valid image URL even if no image is uploaded."""
        if self.image:
            return self.image.url
        return '/static/shop/images/placeholder.jpg'

    def get_absolute_url(self):
        """URL for this category's subcategories page."""
        return reverse("category_subcategories", args=[str(self.id)])


# -----------------------------
# SUBCATEGORY MODEL
# -----------------------------
class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='subcategory_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Show in 'Recommended for you' section")
    sort_order = models.IntegerField(default=0, help_text="Order of display (lower numbers first)")

    class Meta:
        verbose_name_plural = "Subcategories"
        ordering = ['sort_order', 'name']

    def __str__(self):
        cat_name = self.category.name if self.category else "No Category"
        subcat_name = self.name if self.name else "Unnamed SubCategory"
        return f"{cat_name} - {subcat_name}"

    def image_url(self):
        """Return subcategory image or fallback placeholder."""
        if self.image:
            return self.image.url
        return '/static/shop/images/placeholder.jpg'

    def get_absolute_url(self):
        """URL to view all products under this subcategory."""
        return reverse("subcategory_products", args=[str(self.id)])


# -----------------------------
# PRODUCT MODEL
# -----------------------------
class Product(models.Model):
    BADGE_CHOICES = [
        ('NEW', 'New Arrival'),
        ('SALE', 'On Sale'),
        ('BEST', 'Best Seller'),
        ('TRENDING', 'Trending'),
        ('NONE', 'None'),
    ]

    STONE_CHOICES = [
        ('NONE', 'None'),
        ('MOISSANITE', 'Moissanite'),
        ('LAB_GROWN', 'Lab Grown'),
        ('AMERICAN', 'American Diamond'),
        ('DIAMOND', 'Diamond'),
        ('RUBY', 'Ruby'),
        ('EMERALD', 'Emerald'),
        ('SAPPHIRE', 'Sapphire'),
        ('PEARL', 'Pearl'),
        ('AMETHYST', 'Amethyst'),
        ('OTHER', 'Other'),
    ]

    COLOR_CHOICES = [
        ('GOLD', 'Gold'),
        ('SILVER', 'Silver'),
        ('ROSE_GOLD', 'Rose Gold'),
        ('PLATINUM', 'Platinum'),
        ('MULTI', 'Multi-color'),
    ]

    METAL_CHOICES = [
        ('GOLD', 'Gold'),
        ('SILVER', 'Silver'),
        ('PLATINUM', 'Platinum'),
    ]

    # Purity choices separated for clarity:
    GOLD_PURITY_CHOICES = [
        ('9K', '9K'),
        ('10K', '10K'),
        ('14K', '14K'),
        ('18K', '18K'),
        ('22K', '22K'),
        ('24K', '24K'),
        ('OTHER', 'Other'),
    ]

    SILVER_PURITY_CHOICES = [
        ('STERLING', 'Sterling (925)'),
        ('999', '999 Fine Silver'),
        ('OTHER', 'Other'),
    ]

    PLATINUM_PURITY_CHOICES = [
        ('950', '950 Platinum'),
        ('900', '900 Platinum'),
        ('OTHER', 'Other'),
    ]

    # --- Basic Info ---
    name = models.CharField(max_length=200, blank=True, null=True)
    subcategory = models.ForeignKey(
        'SubCategory',  # quoted in case SubCategory defined later in file
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jewellery_items"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='jewellery/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='NONE', blank=True, null=True)
    stone_type = models.CharField(max_length=20, choices=STONE_CHOICES, default='NONE', blank=True, null=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='GOLD', blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    occasion = models.CharField(max_length=100, blank=True, null=True)
    collection = models.CharField(max_length=100, blank=True, null=True)

    # --- Metal & Stone Details ---
    metal_type = models.CharField(max_length=20, choices=METAL_CHOICES, default='GOLD', blank=True, null=True)

    # Weights
    gross_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True, null=True, help_text="Gross weight in grams")
    net_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True, null=True, help_text="Net metal weight in grams")

    # Gold-specific fields
    gold_purity = models.CharField(
        max_length=10,
        choices=GOLD_PURITY_CHOICES,
        default='22K',
        blank=True,
        null=True,
        help_text="Gold purity (only relevant when metal_type is Gold)"
    )
    gold_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True, null=True)

    # Silver-specific fields
    silver_purity = models.CharField(
        max_length=20,
        choices=SILVER_PURITY_CHOICES,
        default='STERLING',
        blank=True,
        null=True,
        help_text="Silver purity (only relevant when metal_type is Silver)"
    )
    silver_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True, null=True)

    # Platinum-specific fields (optional)
    platinum_purity = models.CharField(
        max_length=10,
        choices=PLATINUM_PURITY_CHOICES,
        default='950',
        blank=True,
        null=True,
        help_text="Platinum purity (only relevant when metal_type is Platinum)"
    )
    platinum_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True, null=True)

    # Shared stone fields
    diamond_weight = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True, null=True)
    diamond_clarity = models.CharField(max_length=50, blank=True, null=True)
    diamond_color = models.CharField(max_length=50, blank=True, null=True)

    # --- Price Breakdown ---
    # Keep both metal value fields — only one will usually be non-zero depending on metal_type
    gold_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    silver_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    platinum_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)

    stone_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    making_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    gst = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    # --- Auto Total ---
    is_manual_price = models.BooleanField(
        default=False,
        verbose_name="Manual Price Override",
        help_text="Check this to manually enter pricing values (Metal Value, Making Charges, GST) and prevent automatic updates based on daily rates."
    )
    total_price = models.DecimalField(max_digits=14, decimal_places=2, default=0, editable=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Products"
        db_table = 'shop_jewellery'

    def __str__(self):
        return self.name or "Unnamed Product"

    def recalculate_price(self, save=False):
        """
        Recalculates gold/silver value, making charges, gst and total price
        based on the current MetalRate records in the database.
        """
        if self.is_manual_price:
            # Preserving manual values entered by admin. Just calculate total_price:
            metal_total = (self.gold_value or 0) + (self.silver_value or 0) + (self.platinum_value or 0)
            self.total_price = (
                metal_total +
                (self.stone_value or 0) +
                (self.making_charges or 0) +
                (self.gst or 0)
            )
            # If the user did not specify a price but specified breakdown, use total_price
            if not self.price or self.price == 0:
                self.price = self.total_price
            if save:
                super().save()
            return

        rate = None
        weight = 0
        
        if self.metal_type == 'GOLD':
            purity_code = f"GOLD_{self.gold_purity}" if self.gold_purity else "GOLD_22K"
            weight = self.net_weight or self.gross_weight or self.gold_weight or 0
            try:
                rate = MetalRate.objects.get(metal_type=purity_code)
            except:
                pass
        elif self.metal_type == 'SILVER':
            purity_code = f"SILVER_{self.silver_purity}" if self.silver_purity else "SILVER"
            weight = self.net_weight or self.gross_weight or self.silver_weight or 0
            try:
                rate = MetalRate.objects.get(metal_type=purity_code)
            except:
                try:
                    rate = MetalRate.objects.get(metal_type='SILVER')
                except:
                    pass
                
        if rate:
            # 1. Calculate metal value
            metal_value = rate.rate_per_gram * weight
            if self.metal_type == 'GOLD':
                self.gold_value = metal_value
                self.silver_value = 0
                self.platinum_value = 0
            elif self.metal_type == 'SILVER':
                self.silver_value = metal_value
                self.gold_value = 0
                self.platinum_value = 0
                
            # 2. Calculate making charge based on the daily rate
            if rate.making_type == 'FIXED':
                self.making_charges = rate.making_charge * weight
            else:
                self.making_charges = (metal_value * rate.making_charge) / 100
                
            # 3. Calculate GST (3% of metal value + making charges)
            subtotal = metal_value + (self.making_charges or 0)
            self.gst = (subtotal * rate.gst_percentage) / 100
            
            # 4. Total Price
            self.total_price = subtotal + (self.gst or 0) + (self.stone_value or 0)
            self.price = self.total_price
            
            if save:
                super().save()
        else:
            # Fallback if no rate exists: sum manual values
            metal_total = (self.gold_value or 0) + (self.silver_value or 0) + (self.platinum_value or 0)
            self.total_price = (
                metal_total +
                (self.stone_value or 0) +
                (self.making_charges or 0) +
                (self.gst or 0)
            )
            self.price = self.total_price

    def save(self, *args, **kwargs):
        """
        Automatically calculate total_price and keep price synced.
        """
        self.recalculate_price(save=False)
        super().save(*args, **kwargs)

    def get_badge_color(self):
        colors = {
            'NEW': 'success',
            'SALE': 'danger',
            'BEST': 'warning',
            'TRENDING': 'info',
        }
        return colors.get(self.badge, 'secondary')

    def image_url(self):
        if self.image:
            return self.image.url
        return '/static/shop/images/placeholder.jpg'

    def get_absolute_url(self):
        """Direct link to jewellery detail page."""
        return reverse("product_detail", args=[str(self.id)])


# -----------------------------
# PRODUCT IMAGE MODEL
# -----------------------------
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='jewellery/gallery/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'shop_jewelleryimage'

    def __str__(self):
        prod_name = self.product.name if self.product else "No Product"
        return f"Image for {prod_name}"





# -----------------------------
# WISHLIST MODEL
# -----------------------------
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        u_name = self.user.username if self.user else "Anonymous"
        p_name = self.product.name if self.product else "No Product"
        return f"{u_name} - {p_name}"

    def added_time(self):
        return self.created_at.strftime("%b %d, %Y")



# -----------------------------
# METAL RATE MODEL (Today's Rates)
# -----------------------------
class MetalRate(models.Model):
    METAL_CHOICES = [
        ("GOLD_24K", "24K Gold"),
        ("GOLD_22K", "22K Gold"),
        ("GOLD_18K", "18K Gold"),
        ("GOLD_14K", "14K Gold"),
        ("GOLD_9K", "9K Gold"),
        ("SILVER", "92.5 Silver Jewellery"),
    ]
    MAKING_CHOICES = [
        ("FIXED", "Fixed (₹/g)"),
        ("PERCENTAGE", "Percentage (%)"),
    ]
    
    metal_type = models.CharField(
        max_length=50, 
        unique=True,
        blank=True,
        null=True,
        help_text="Enter metal rate code (e.g. GOLD_24K, GOLD_22K, GOLD_18K, GOLD_14K, GOLD_9K, SILVER_999, SILVER_STERLING, SILVER, PLATINUM)."
    )
    purity = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.0,
        blank=True,
        null=True
    )
    rate_per_gram = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.0,
        blank=True,
        null=True
    )
    making_charge = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.0
    )
    making_type = models.CharField(
        max_length=20, 
        choices=MAKING_CHOICES, 
        default="FIXED"
    )
    gst_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=3.0
    )
    status = models.BooleanField(default=True, help_text="Show this metal rate block on frontend")
    show_making_charge = models.BooleanField(default=True, help_text="Show making charge value on frontend")
    show_gst = models.BooleanField(default=True, help_text="Show GST calculation on frontend")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Metal Rates"
        ordering = ["metal_type"]

    def __str__(self):
        return f"{self.get_metal_type_display()} - ₹{self.rate_per_gram}/g"

    @classmethod
    def get_ordered_rates(cls, qs=None):
        """
        Returns MetalRate queryset ordered logically:
        All Gold rates sorted by purity descending (24K -> 22K -> 20K -> 18K -> 14K -> 12K -> 9K),
        followed by Silver rates, Platinum, and any others.
        """
        from django.db.models import Q, Case, When, Value, IntegerField
        if qs is None:
            qs = cls.objects.filter(status=True)
        return qs.annotate(
            metal_category=Case(
                When(Q(metal_type__icontains='GOLD'), then=Value(1)),
                When(Q(metal_type__icontains='SILVER'), then=Value(2)),
                When(Q(metal_type__icontains='PLATINUM'), then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )
        ).order_by('metal_category', '-purity')
    
    def get_metal_type_display(self):
        if not self.metal_type:
            return ""
        # Return the display name from choices if available
        for choice in self.METAL_CHOICES:
            if choice[0] == self.metal_type:
                return choice[1]
        
        # Parse dynamically (e.g. GOLD_14K -> 14K Gold, SILVER_999 -> 999 Silver)
        parts = self.metal_type.split('_')
        if len(parts) == 2:
            metal, purity = parts
            return f"{purity} {metal.capitalize()}"
        return self.metal_type.replace('_', ' ').title()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Automatically update all Product products matching this metal rate
        if self.metal_type and self.metal_type.startswith('GOLD_'):
            purity = self.metal_type.replace('GOLD_', '')
            products = Product.objects.filter(metal_type='GOLD', gold_purity=purity)
        elif self.metal_type and self.metal_type.startswith('SILVER'):
            purity = self.metal_type.replace('SILVER_', '')
            if purity == 'SILVER':
                products = Product.objects.filter(metal_type='SILVER')
            else:
                products = Product.objects.filter(metal_type='SILVER', silver_purity=purity)
        elif self.metal_type and self.metal_type.startswith('PLATINUM'):
            purity = self.metal_type.replace('PLATINUM_', '')
            if purity == 'PLATINUM':
                products = Product.objects.filter(metal_type='PLATINUM')
            else:
                products = Product.objects.filter(metal_type='PLATINUM', platinum_purity=purity)
        else:
            products = []
            
        for product in products:
            product.recalculate_price(save=True)





# -----------------------------
# POPUP MESSAGE MODEL
# -----------------------------
class PopupMessage(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    poster_image = models.ImageField(upload_to='popup_posters/', blank=True, null=True, help_text="Upload discount poster image")
    status = models.BooleanField(default=True)
    show_on_refresh = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Layout Customizations
    show_title = models.BooleanField(default=True, help_text="Toggle title visibility")
    show_message = models.BooleanField(default=True, help_text="Toggle message text visibility")
    show_poster_image = models.BooleanField(default=True, help_text="Toggle poster image visibility")
    show_rates_grid = models.BooleanField(default=True, help_text="Toggle daily rates grid inside popup")
    
    # Custom Action Buttons & Links
    show_shop_button = models.BooleanField(default=True, help_text="Toggle Shop button visibility")
    shop_button_text = models.CharField(max_length=50, default="Shop", help_text="Text for Shop button")
    shop_button_url = models.CharField(max_length=255, default="/shop/", help_text="URL path for Shop button")
    
    show_rates_button = models.BooleanField(default=True, help_text="Toggle Rates button visibility")
    rates_button_text = models.CharField(max_length=50, default="Rates", help_text="Text for Rates button")
    rates_button_url = models.CharField(max_length=255, default="/live-rates/", help_text="URL path for Rates button")
    
    show_calc_button = models.BooleanField(default=True, help_text="Toggle Calculator button visibility")
    calc_button_text = models.CharField(max_length=50, default="Calc", help_text="Text for Calculator button")
    calc_button_url = models.CharField(max_length=255, default="#live-calculator", help_text="URL path/anchor for Calculator button")
    
    class Meta:
        verbose_name_plural = "Popup Messages"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or "Untitled Popup Message"


# -----------------------------
# TESTIMONIAL MODEL
# -----------------------------
class Testimonial(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    rating = models.PositiveIntegerField(default=5, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, default="Verified Buyer")
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True, help_text="Optional product/customer image uploaded with feedback")
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        name_display = self.name if self.name else "Anonymous"
        return f"{name_display} - {self.rating} stars"


# -----------------------------
# SIGNATURE COLLECTION SECTION MODEL
# -----------------------------
class SignatureCollection(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, help_text="Section title for Signature Collection")
    subtitle = models.TextField(blank=True, null=True, help_text="Section subtitle/description")
    is_active = models.BooleanField(default=True, help_text="Show this section on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Signature Collections"
        ordering = ['-created_at']

    def __str__(self):
        return self.title or "Signature Collection Section"


class SignatureCollectionItem(models.Model):
    collection = models.ForeignKey(SignatureCollection, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True, help_text="Item title")
    description = models.TextField(blank=True, null=True, help_text="Short description for this item")
    image = models.ImageField(upload_to='signature_collection/', blank=True, null=True, help_text="Image for this signature collection item")
    sort_order = models.IntegerField(default=0, help_text="Order of display (lower numbers first)")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', '-id']

    def __str__(self):
        return self.title or f"Signature Item {self.id}"

    def image_url(self):
        if self.image:
            return self.image.url
        return '/static/img/no-image.png'


# -----------------------------
# REEL MODEL
# -----------------------------
class Reel(models.Model):
    title = models.CharField(max_length=200, blank=True)
    video = models.FileField(upload_to='reels/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='reels/covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Reel {self.id}"


