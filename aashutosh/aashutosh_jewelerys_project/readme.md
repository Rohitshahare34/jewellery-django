
Step 1: Delete migration files for shop

Go to:

aashutosh_jewelerys_project/shop/migrations/


and delete all files except:

__init__.py

<!-- Step 2: Delete the database (since it’s likely test/demo data) -->
del db.sqlite3
<!--  -->
python manage.py makemigrations

<!--  -->
python manage.py migrate
<!--  -->
python manage.py createsuperuser


<!-- Superuser  -->
user =amrish

password = aashu@123

<!-- Activate the environment -->
venv\Scripts\activate


python manage.py runserver
