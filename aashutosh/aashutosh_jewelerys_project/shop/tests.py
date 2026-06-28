from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Category, SubCategory, Product, Wishlist, MetalRate

class ShopTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()

        # Create Category
        self.category = Category.objects.create(name="Gold Jewellery")

        # Create SubCategory
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name="Rings",
            is_featured=True
        )

        # Create Product (unified model)
        self.product = Product.objects.create(
            name="Royal Gold Necklace",
            subcategory=self.subcategory,
            price=50000.00,
            in_stock=True,
            badge="NEW",
            metal_type="GOLD",
            gold_purity="22K",
            gold_weight=10.0,
            gold_value=45000.00,
            stone_value=2000.00,
            making_charges=2000.00,
            gst=1000.00
        )

        # Create MetalRate
        self.metal_rate = MetalRate.objects.create(
            metal_type="GOLD_22K",
            purity=22.0,
            rate_per_gram=6000.00,
            making_charge=300.00,
            making_type="FIXED",
            gst_percentage=3.0,
            status=True
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_shop_page(self):
        response = self.client.get(reverse('shop'))
        self.assertEqual(response.status_code, 200)

    def test_categories_page(self):
        response = self.client.get(reverse('shop_by_category'))
        self.assertEqual(response.status_code, 200)

    def test_category_products_page(self):
        response = self.client.get(reverse('category_products', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)

    def test_category_subcategories_page(self):
        response = self.client.get(reverse('category_subcategories', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)

    def test_subcategory_products_page(self):
        response = self.client.get(reverse('subcategory_products', args=[self.subcategory.id]))
        self.assertEqual(response.status_code, 200)

    def test_all_products_page(self):
        response = self.client.get(reverse('all_products'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_page(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_search_page(self):
        response = self.client.get(reverse('search') + '?q=Necklace')
        self.assertEqual(response.status_code, 200)

    def test_services_page(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_wishlist_page_unauthenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)

    def test_cart_page(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_profile_page(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_page(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_change_password_page(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_metal_prices_api(self):
        response = self.client.get(reverse('get_metal_prices'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'success': True,
            'gold': {
                'price': '0',
                'price_24k': '0',
                'price_22k': '6000.00',
                'change_percent': '0',
                'is_up': True,
                'last_updated': 'Updated today',
            },
            'silver': {
                'price': '0',
                'change_percent': '0',
                'is_up': True,
                'last_updated': 'Updated today',
            }
        })

    def test_live_rates_page(self):
        response = self.client.get(reverse('live_rates'))
        self.assertEqual(response.status_code, 200)

    def test_rate_calculator_page(self):
        response = self.client.get(reverse('rate_calculator'))
        self.assertEqual(response.status_code, 200)

    def test_submit_testimonial(self):
        response = self.client.post(reverse('submit_testimonial'), {
            'name': 'Test Client',
            'rating': '5',
            'message': 'Amazing designs!',
            'designation': 'Regular Customer'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.content)

