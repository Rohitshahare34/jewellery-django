import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aashutosh_jewelerys.settings')
django.setup()

from django.core import serializers
from django.contrib.auth.models import User
from shop.models import Category, SubCategory, Jewellery, JewelleryImage, MetalPrice, MetalRate, JewelryProduct, Testimonial, Reel, PopupMessage

# Dependency-ordered list of models to export
MODELS_TO_EXPORT = [
    User,
    Category,
    SubCategory,
    Jewellery,
    JewelleryImage,
    MetalPrice,
    MetalRate,
    JewelryProduct,
    Testimonial,
    Reel,
    PopupMessage,
]

def dump_data(filepath="db_transfer.json"):
    """Export database data to a JSON file."""
    print("Exporting local database data...")
    all_objects = []
    
    for model in MODELS_TO_EXPORT:
        qs = model.objects.all()
        print(f"- {model.__name__}: {qs.count()} objects found.")
        all_objects.extend(list(qs))
        
    # Serialize to JSON fixture format
    data = serializers.serialize(
        "json", 
        all_objects, 
        indent=4, 
        use_natural_foreign_keys=True, 
        use_natural_primary_keys=True
    )
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)
        
    print(f"\n[SUCCESS] Successfully exported all database data to: {filepath}")
    print("You can now copy this file to your AWS server and run the load command.")

def load_data(filepath="db_transfer.json"):
    """Import JSON data into the target database."""
    if not os.path.exists(filepath):
        print(f"[ERROR] Import file not found: {filepath}")
        sys.exit(1)
        
    print("Clearing existing data (in reverse dependency order to preserve foreign keys)...")
    
    # We clear everything EXCEPT superusers/staff from User model
    for model in reversed(MODELS_TO_EXPORT):
        if model == User:
            # Only delete non-staff users to protect admin login credentials
            count = User.objects.filter(is_staff=False, is_superuser=False).count()
            User.objects.filter(is_staff=False, is_superuser=False).delete()
            print(f"- {model.__name__}: Deleted {count} non-admin users.")
        else:
            count = model.objects.count()
            model.objects.all().delete()
            print(f"- {model.__name__}: Deleted {count} objects.")
            
    print(f"\nImporting data from {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()
        
    count = 0
    for obj in serializers.deserialize("json", data):
        # Prevent integrity error if user already exists
        if isinstance(obj.object, User):
            if User.objects.filter(username=obj.object.username).exists():
                existing = User.objects.get(username=obj.object.username)
                existing.email = obj.object.email
                existing.password = obj.object.password
                existing.is_active = obj.object.is_active
                existing.is_staff = obj.object.is_staff
                existing.is_superuser = obj.object.is_superuser
                existing.save()
                count += 1
                continue
        
        obj.save()
        count += 1
        
    print(f"\n[SUCCESS] Loaded {count} objects into the database successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python db_transfer.py dump   <- Run this on local machine to export data")
        print("  python db_transfer.py load   <- Run this on AWS server to import data")
        sys.exit(1)
        
    command = sys.argv[1].lower()
    if command == "dump":
        dump_data()
    elif command == "load":
        load_data()
    else:
        print(f"Unknown command: {command}")
        print("Supported commands: dump, load")
        sys.exit(1)
