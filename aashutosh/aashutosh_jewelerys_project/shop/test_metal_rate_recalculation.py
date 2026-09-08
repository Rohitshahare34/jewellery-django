from decimal import Decimal

from django.test import TestCase

from shop.models import Category, SubCategory, Product, MetalRate, ProductImage


def expected_breakdown(rate_per_gram, weight, making_per_gram, stone_value, gst_percentage=Decimal('3.0')):
    """Mirrors Product.recalculate_price when making_per_gram > 0 and is_manual_price is False."""
    metal = Decimal(str(rate_per_gram)) * Decimal(str(weight))
    making = Decimal(str(making_per_gram)) * Decimal(str(weight))
    taxable = metal + Decimal(str(stone_value)) + making
    gst = (taxable * Decimal(str(gst_percentage))) / Decimal('100')
    total = taxable + gst
    return metal, making, gst, total


class MetalRateProductRecalculationTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Jewellery")
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name="Rings",
        )

        self.gold_rate = MetalRate.objects.create(
            metal_type="GOLD_22K",
            purity=22.0,
            rate_per_gram=Decimal('15000.00'),
            making_charge=Decimal('300.00'),
            making_type="FIXED",
            gst_percentage=Decimal('3.0'),
            status=True,
        )
        self.silver_rate = MetalRate.objects.create(
            metal_type="SILVER",
            purity=92.5,
            rate_per_gram=Decimal('200.00'),
            making_charge=Decimal('50.00'),
            making_type="FIXED",
            gst_percentage=Decimal('3.0'),
            status=True,
        )

        self.gold_product = Product.objects.create(
            name="22K Gold Ring",
            subcategory=self.subcategory,
            metal_type="GOLD",
            gold_purity="22K",
            gold_weight=Decimal('10.000'),
            making_per_gram=Decimal('100.00'),
            stone_type="DIAMOND",
            stone_value=Decimal('500.00'),
            diamond_weight=Decimal('0.250'),
            diamond_clarity="VS1",
            diamond_color="F",
            description="Handcrafted gold ring",
            in_stock=True,
            is_featured=False,
            badge="NEW",
        )
        self.silver_product = Product.objects.create(
            name="Silver Bangle",
            subcategory=self.subcategory,
            metal_type="SILVER",
            silver_purity="STERLING",
            silver_weight=Decimal('20.000'),
            making_per_gram=Decimal('40.00'),
            stone_type="NONE",
            stone_value=Decimal('100.00'),
            description="Sterling silver bangle",
            in_stock=True,
        )
        self.manual_gold = Product.objects.create(
            name="Manual Gold Piece",
            subcategory=self.subcategory,
            metal_type="GOLD",
            gold_purity="22K",
            gold_weight=Decimal('5.000'),
            is_manual_price=True,
            gold_value=Decimal('99999.00'),
            stone_value=Decimal('10.00'),
            making_charges=Decimal('20.00'),
            gst=Decimal('30.00'),
        )

    def _reload(self, obj):
        return type(obj).objects.get(pk=obj.pk)

    def _assert_gold_priced_at(self, rate_per_gram):
        product = self._reload(self.gold_product)
        metal, making, gst, total = expected_breakdown(
            rate_per_gram, 10, 100, 500
        )
        self.assertEqual(product.name, "22K Gold Ring")
        self.assertEqual(product.gold_weight, Decimal('10.000'))
        self.assertEqual(product.gold_purity, "22K")
        self.assertEqual(product.making_per_gram, Decimal('100.00'))
        self.assertEqual(product.stone_type, "DIAMOND")
        self.assertEqual(product.stone_value, Decimal('500.00'))
        self.assertEqual(product.diamond_weight, Decimal('0.250'))
        self.assertEqual(product.diamond_clarity, "VS1")
        self.assertEqual(product.diamond_color, "F")
        self.assertEqual(product.subcategory_id, self.subcategory.id)
        self.assertEqual(product.subcategory.category_id, self.category.id)
        self.assertTrue(product.in_stock)
        self.assertEqual(product.badge, "NEW")
        self.assertFalse(product.image)
        self.assertEqual(product.gold_value, metal)
        self.assertEqual(product.making_charges, making)
        self.assertEqual(product.gst, gst)
        self.assertEqual(product.total_price, total)
        self.assertEqual(product.price, total)

    def _assert_silver_priced_at(self, rate_per_gram):
        product = self._reload(self.silver_product)
        metal, making, gst, total = expected_breakdown(
            rate_per_gram, 20, 40, 100
        )
        self.assertEqual(product.name, "Silver Bangle")
        self.assertEqual(product.silver_weight, Decimal('20.000'))
        self.assertEqual(product.silver_purity, "STERLING")
        self.assertEqual(product.making_per_gram, Decimal('40.00'))
        self.assertEqual(product.stone_value, Decimal('100.00'))
        self.assertEqual(product.subcategory_id, self.subcategory.id)
        self.assertTrue(product.in_stock)
        self.assertEqual(product.silver_value, metal)
        self.assertEqual(product.making_charges, making)
        self.assertEqual(product.gst, gst)
        self.assertEqual(product.total_price, total)
        self.assertEqual(product.price, total)

    def test_new_product_uses_current_rate(self):
        self._assert_gold_priced_at(15000)
        self._assert_silver_priced_at(200)

    def test_gold_rate_update_recalculates_existing_gold_product(self):
        self.gold_rate.rate_per_gram = Decimal('16000.00')
        self.gold_rate.save()
        self._assert_gold_priced_at(16000)

    def test_second_gold_rate_update_recalculates_again(self):
        self.gold_rate.rate_per_gram = Decimal('16000.00')
        self.gold_rate.save()
        self.gold_rate.rate_per_gram = Decimal('17000.00')
        self.gold_rate.save()
        self._assert_gold_priced_at(17000)

    def test_consecutive_gold_rate_updates(self):
        for rate in ('16000.00', '17000.00', '15800.00'):
            self.gold_rate.rate_per_gram = Decimal(rate)
            self.gold_rate.save()
            self._assert_gold_priced_at(rate)

    def test_silver_rate_update_recalculates_existing_silver_product(self):
        self.silver_rate.rate_per_gram = Decimal('250.00')
        self.silver_rate.save()
        self._assert_silver_priced_at(250)

    def test_second_silver_rate_update_recalculates_again(self):
        self.silver_rate.rate_per_gram = Decimal('250.00')
        self.silver_rate.save()
        self.silver_rate.rate_per_gram = Decimal('230.00')
        self.silver_rate.save()
        self._assert_silver_priced_at(230)

    def test_gold_rate_update_does_not_change_silver_products(self):
        silver_before = self._reload(self.silver_product)
        self.gold_rate.rate_per_gram = Decimal('16000.00')
        self.gold_rate.save()
        silver_after = self._reload(self.silver_product)
        self.assertEqual(silver_before.price, silver_after.price)
        self.assertEqual(silver_before.silver_value, silver_after.silver_value)
        self.assertEqual(silver_before.gst, silver_after.gst)
        self._assert_gold_priced_at(16000)

    def test_silver_rate_update_does_not_change_gold_products(self):
        gold_before = self._reload(self.gold_product)
        self.silver_rate.rate_per_gram = Decimal('250.00')
        self.silver_rate.save()
        gold_after = self._reload(self.gold_product)
        self.assertEqual(gold_before.price, gold_after.price)
        self.assertEqual(gold_before.gold_value, gold_after.gold_value)
        self.assertEqual(gold_before.gst, gold_after.gst)
        self._assert_silver_priced_at(250)

    def test_manual_price_product_not_overwritten_by_rate_update(self):
        before = self._reload(self.manual_gold)
        self.gold_rate.rate_per_gram = Decimal('16000.00')
        self.gold_rate.save()
        after = self._reload(self.manual_gold)
        self.assertEqual(after.name, "Manual Gold Piece")
        self.assertEqual(after.gold_value, before.gold_value)
        self.assertEqual(after.making_charges, before.making_charges)
        self.assertEqual(after.gst, before.gst)
        self.assertEqual(after.price, before.price)

    def test_rate_update_does_not_create_or_delete_images(self):
        self.assertEqual(ProductImage.objects.filter(product=self.gold_product).count(), 0)
        self.gold_rate.rate_per_gram = Decimal('16000.00')
        self.gold_rate.save()
        self.assertEqual(ProductImage.objects.filter(product=self.gold_product).count(), 0)
        self.assertFalse(self._reload(self.gold_product).image)

    def test_gst_follows_existing_formula_after_rate_change(self):
        self.gold_rate.rate_per_gram = Decimal('16000.00')
        self.gold_rate.save()
        product = self._reload(self.gold_product)
        taxable = product.gold_value + product.stone_value + product.making_charges
        expected_gst = (taxable * Decimal('3.0')) / Decimal('100')
        self.assertEqual(product.gst, expected_gst)
        self.assertEqual(product.total_price, taxable + expected_gst)
