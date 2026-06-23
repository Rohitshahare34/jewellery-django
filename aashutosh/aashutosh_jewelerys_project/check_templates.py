import os
import django
from django.conf import settings

# Configure Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aashutosh_jewelerys.settings")
django.setup()

# Let's find allauth's template files
try:
    import allauth
    allauth_path = os.path.dirname(allauth.__file__)
    template_path = os.path.join(allauth_path, "templates")
    print("Allauth template path:", template_path)
    
    if os.path.exists(template_path):
        print("\nAllauth templates found:")
        for root, dirs, files in os.walk(template_path):
            for file in files:
                print(os.path.relpath(os.path.join(root, file), template_path))
except ImportError:
    print("Allauth not found")

print("\nOur template directories:")
for dir in settings.TEMPLATES[0]['DIRS']:
    print(dir)
    
print("\nChecking if our custom templates exist:")
for dir in settings.TEMPLATES[0]['DIRS']:
    social_tpl = os.path.join(dir, "socialaccount")
    if os.path.exists(social_tpl):
        print("✓ Found:", social_tpl)
        print("  Contents:", os.listdir(social_tpl))
