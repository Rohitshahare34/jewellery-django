from django.core.management.base import BaseCommand
from shop.models import SignatureCollection, SignatureCollectionItem


class Command(BaseCommand):
    help = "Adds sample Signature Collection data"

    def handle(self, *args, **options):
        # Create a Signature Collection
        collection, created = SignatureCollection.objects.get_or_create(
            title="Our Signature Collections",
            defaults={
                "subtitle": "Exquisite Designs Crafted for You",
                "is_active": True,
            }
        )

        if created or SignatureCollectionItem.objects.filter(collection=collection).count() == 0:
            # Create sample items
            sample_items = [
                {
                    "title": "Gold Ornaments",
                    "description": "Shop Collection",
                    "image_path": "hero-section-imgs/ChatGPT Image Jun 20, 2026, 07_07_35 PM.png",
                    "sort_order": 1
                },
                {
                    "title": "Diamond Rings",
                    "description": "Shop Collection",
                    "image_path": "hero-section-imgs/ChatGPT Image Jun 20, 2026, 07_19_00 PM.png",
                    "sort_order": 2
                },
                {
                    "title": "Traditional Necklace",
                    "description": "Shop Collection",
                    "image_path": "hero-section-imgs/hero1.png",
                    "sort_order": 3
                },
                {
                    "title": "Antique Masterpieces",
                    "description": "Shop Collection",
                    "image_path": "hero-section-imgs/ChatGPT Image Jun 20, 2026, 07_25_40 PM.png",
                    "sort_order": 4
                },
                {
                    "title": "Royal Chokers",
                    "description": "Shop Collection",
                    "image_path": "hero-section-imgs/ChatGPT Image Jun 20, 2026, 07_26_05 PM.png",
                    "sort_order": 5
                },
                {
                    "title": "Bespoke Rings",
                    "description": "Shop Collection",
                    "image_path": "hero-section-imgs/ChatGPT Image Jun 20, 2026, 07_36_19 PM.png",
                    "sort_order": 6
                },
                {
                    "title": "Bridal Special",
                    "description": "Shop Collection",
                    "image_path": "hero-section-imgs/hero2.png",
                    "sort_order": 7
                }
            ]

            for item_data in sample_items:
                SignatureCollectionItem.objects.get_or_create(
                    collection=collection,
                    title=item_data["title"],
                    defaults={
                        "description": item_data["description"],
                        "sort_order": item_data["sort_order"],
                        "is_active": True
                    }
                )

            self.stdout.write(
                self.style.SUCCESS(f"Successfully added sample Signature Collection with {len(sample_items)} items!")
            )
        else:
            self.stdout.write(
                self.style.WARNING("Sample Signature Collection already exists with items!")
            )