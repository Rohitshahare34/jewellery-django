import os
import sys
import subprocess

def create_project_structure():
    """Create the complete Django project structure"""
    
    structure = {
        'aashutosh_jewelerys_project': [
            'manage.py',
            'requirements.txt',
            'setup_project.py',
            ['aashutosh_jewelerys', [
                '__init__.py',
                'settings.py',
                'urls.py',
                'wsgi.py',
                'asgi.py'
            ]],
            ['shop', [
                '__init__.py',
                'admin.py',
                'apps.py',
                'models.py',
                'views.py',
                'urls.py',
                'context_processors.py',
                ['management', [
                    '__init__.py',
                    ['commands', [
                        '__init__.py',
                        'populate_sample_data.py'
                    ]]
                ]],
                ['templates', [
                    '__init__.py',
                    ['shop', [
                        'base.html',
                        'home.html',
                        'shop.html',
                        'category.html',
                        'product_detail.html',
                        'about.html',
                        'contact.html',
                        'login_register.html'
                    ]]
                ]],
                ['static', [
                    '__init__.py',
                    ['shop', [
                        'css/',
                        'js/',
                        'images/'
                    ]]
                ]]
            ]],
            'media/',
            'static/'
        ]
    }

    def create_path(base_path, items):
        for item in items:
            if isinstance(item, list):
                dir_name = item[0]
                dir_path = os.path.join(base_path, dir_name)
                print(f"Creating directory: {dir_path}")
                os.makedirs(dir_path, exist_ok=True)
                create_path(dir_path, item[1])
            elif item.endswith('/'):
                dir_path = os.path.join(base_path, item)
                print(f"Creating directory: {dir_path}")
                os.makedirs(dir_path, exist_ok=True)
            else:
                file_path = os.path.join(base_path, item)
                print(f"Creating file: {file_path}")
                with open(file_path, 'w') as f:
                    f.write(f"# {item}\n")
    
    base_dir = os.getcwd()
    project_dir = os.path.join(base_dir, 'aashutosh_jewelerys_project')

    print("Creating Aashutosh Jewelerys Project Structure...")
    print("=" * 50)

    # ✅ FIX HERE: loop through structure items
    for key, value in structure.items():
        project_path = os.path.join(base_dir, key)
        os.makedirs(project_path, exist_ok=True)
        create_path(project_path, value)

    print("\nProject structure created successfully!")
    return project_dir

def create_requirements_file(project_dir):
    """Create requirements.txt file"""
    requirements_content = """Django>=5.0
Pillow>=10.0.0
"""
    requirements_path = os.path.join(project_dir, 'requirements.txt')
    with open(requirements_path, 'w') as f:
        f.write(requirements_content)
    print("Created requirements.txt")

def create_manage_py(project_dir):
    """Create manage.py file"""
    manage_py_content = '''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aashutosh_jewelerys.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
'''
    manage_py_path = os.path.join(project_dir, 'manage.py')
    with open(manage_py_path, 'w') as f:
        f.write(manage_py_content)
    print("Created manage.py")

def main():
    print("AASHUTOSH JEWELERYS - DJANGO PROJECT SETUP")
    print("=" * 50)
    
    project_dir = create_project_structure()
    create_requirements_file(project_dir)
    create_manage_py(project_dir)
    
    print("\n" + "=" * 50)
    print("SETUP COMPLETE!")
    print("Next steps:")
    print("1. cd aashutosh_jewelerys_project")
    print("2. pip install -r requirements.txt")
    print("3. python manage.py migrate")
    print("4. python manage.py createsuperuser")
    print("5. python manage.py runserver")
    print("=" * 50)

if __name__ == '__main__':
    main()
