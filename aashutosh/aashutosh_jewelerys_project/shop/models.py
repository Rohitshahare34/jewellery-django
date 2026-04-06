from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# -----------------------------
# CATEGORY MODEL
# -----------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def image_url(self):
        """Return a valid image URL even if no image is uploaded."""
        if self.image:
            return self.image.url
        return '/static/img/no-image.png'

    def get_absolute_url(self):
        """URL for this category's subcategories page."""
        return reverse("category_subcategories", args=[str(self.id)])


# -----------------------------
# SUBCATEGORY MODEL
# -----------------------------
class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='subcategory_images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Subcategories"
        ordering = ['name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def image_url(self):
        """Return subcategory image or fallback placeholder."""
        if self.image:
            return self.image.url
        return '/static/img/no-image.png'

    def get_absolute_url(self):
        """URL to view all products under this subcategory."""
        return reverse("subcategory_products", args=[str(self.id)])


# -----------------------------
# JEWELLERY MODEL
# -----------------------------
class Jewellery(models.Model):
    BADGE_CHOICES = [
        ('NEW', 'New Arrival'),
        ('SALE', 'On Sale'),
        ('BEST', 'Best Seller'),
        ('TRENDING', 'Trending'),
        ('NONE', 'None'),
    ]

    STONE_CHOICES = [
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
    name = models.CharField(max_length=200)
    subcategory = models.ForeignKey(
        'SubCategory',  # quoted in case SubCategory defined later in file
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jewellery_items"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='jewellery/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='NONE')
    stone_type = models.CharField(max_length=20, choices=STONE_CHOICES, default='OTHER')
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='GOLD')
    in_stock = models.BooleanField(default=True)

    # --- Metal & Stone Details ---
    metal_type = models.CharField(max_length=20, choices=METAL_CHOICES, default='GOLD')

    # Gold-specific fields
    gold_purity = models.CharField(
        max_length=10,
        choices=GOLD_PURITY_CHOICES,
        default='22K',
        blank=True,
        null=True,
        help_text="Gold purity (only relevant when metal_type is Gold)"
    )
    gold_weight = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True, null=True)

    # Silver-specific fields
    silver_purity = models.CharField(
        max_length=20,
        choices=SILVER_PURITY_CHOICES,
        default='STERLING',
        blank=True,
        null=True,
        help_text="Silver purity (only relevant when metal_type is Silver)"
    )
    silver_weight = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True, null=True)

    # Platinum-specific fields (optional)
    platinum_purity = models.CharField(
        max_length=10,
        choices=PLATINUM_PURITY_CHOICES,
        default='950',
        blank=True,
        null=True,
        help_text="Platinum purity (only relevant when metal_type is Platinum)"
    )
    platinum_weight = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True, null=True)

    # Shared stone fields
    diamond_weight = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True, null=True)
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
    total_price = models.DecimalField(max_digits=14, decimal_places=2, default=0, editable=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Jewellery"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Automatically calculate total_price and keep price synced.
        total_price sums the relevant metal value(s) + stone_value + making_charges + gst.
        (If metal-specific value fields are zero for a given metal, they won't affect total.)
        """
        # Sum all metal values (only one usually non-zero depending on metal_type)
        metal_total = (self.gold_value or 0) + (self.silver_value or 0) + (self.platinum_value or 0)

        self.total_price = (
            metal_total +
            (self.stone_value or 0) +
            (self.making_charges or 0) +
            (self.gst or 0)
        )

        # Keep price in sync with calculated total
        self.price = self.total_price

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
        return '/static/img/no-image.png'

    def get_absolute_url(self):
        """Direct link to jewellery detail page."""
        return reverse("jewellery_detail", args=[str(self.id)])


# -----------------------------
# JEWELLERY IMAGE MODEL
# -----------------------------
class JewelleryImage(models.Model):
    jewellery = models.ForeignKey(Jewellery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='jewellery/gallery/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.jewellery.name}"


# -----------------------------
# PRODUCT MODEL
# -----------------------------
class Product(models.Model):
    subcategory = models.ForeignKey('SubCategory', related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    is_available = models.BooleanField(default=True)

    metal_type = models.CharField(max_length=50, blank=True, null=True)
    gold_purity = models.CharField(max_length=10, blank=True, null=True)
    gold_weight = models.CharField(max_length=20, blank=True, null=True)
    diamond_weight = models.CharField(max_length=20, blank=True, null=True)
    diamond_clarity = models.CharField(max_length=20, blank=True, null=True)
    diamond_color = models.CharField(max_length=20, blank=True, null=True)

    badge = models.CharField(
        max_length=50,
        choices=[
            ('NONE', 'None'),
            ('NEW', 'New Arrival'),
            ('TRENDING', 'Trending'),
            ('BEST', 'Best Seller'),
        ],
        default='NONE'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def image_url(self):
        return self.image.url if self.image else '/static/img/no-image.png'

    def get_badge_color(self):
        colors = {'NEW': 'success', 'TRENDING': 'info', 'BEST': 'warning'}
        return colors.get(self.badge, 'secondary')

    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)])


# -----------------------------
# PRODUCT IMAGE MODEL
# -----------------------------
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"


# -----------------------------
# WISHLIST MODEL
# -----------------------------
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    def added_time(self):
        return self.created_at.strftime("%b %d, %Y")

