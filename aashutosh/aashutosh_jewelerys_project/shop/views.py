from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ProfileForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .models import Jewellery, Product, Category, SubCategory, Wishlist

# ======================================================
# HOME PAGE VIEW
# ======================================================
def home(request):
    featured_products = Jewellery.objects.filter(is_featured=True, in_stock=True)[:8]
    new_arrivals = Jewellery.objects.filter(badge='NEW', in_stock=True)[:6]
    categories = Category.objects.all()[:4]

    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'hero_videos': [1, 2, 3],  # pass the number of hero videos
    }
    return render(request, 'shop/home.html', context)


# ======================================================
# SHOP PAGE VIEW
# ======================================================
def shop_view(request):
    products = Jewellery.objects.filter(in_stock=True)

    # Filters
    category_filter = request.GET.get('category')
    stone_filter = request.GET.get('stone_type')
    color_filter = request.GET.get('color')
    badge_filter = request.GET.get('badge')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    if category_filter:
        products = products.filter(category__id=category_filter)
    if stone_filter:
        products = products.filter(stone_type=stone_filter)
    if color_filter:
        products = products.filter(color=color_filter)
    if badge_filter:
        products = products.filter(badge=badge_filter)
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:  # newest
        products = products.order_by('-created_at')

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'current_filters': request.GET,
    }
    return render(request, 'shop/shop.html', context)


# ======================================================
# CATEGORY → SUBCATEGORY SYSTEM
# ======================================================
def shop_by_category(request):
    """Displays all main categories."""
    categories = Category.objects.all()
    return render(request, 'shop/shop_by_category.html', {'categories': categories})


def category_subcategories(request, category_id):
    """Displays all subcategories under a selected category."""
    category = get_object_or_404(Category, id=category_id)
    subcategories = SubCategory.objects.filter(category=category)
    return render(request, 'shop/subcategory_list.html', {
        'category': category,
        'subcategories': subcategories
    })


def subcategory_products(request, subcategory_id):
    # Get subcategory or show 404 if invalid
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    
    # Get all products under this subcategory
    products = Product.objects.filter(subcategory=subcategory, is_available=True)
    
    context = {
        'subcategory': subcategory,
        'products': products,
    }
    return render(request, 'shop/subcategory_products.html', context)


# ======================================================
# PRODUCT DETAIL VIEW
# ======================================================
def product_detail(request, pk):
    # Get the jewellery product by ID
    product = get_object_or_404(Jewellery, pk=pk)

    # Get all related images (safe check)
    images = product.images.all() if hasattr(product, 'images') else []

    # Get subcategory and main category safely
    subcategory = product.subcategory
    category = subcategory.category if subcategory else None

    # Fetch related products from the same subcategory
    related_products = Jewellery.objects.filter(
        subcategory=subcategory,
        in_stock=True
    ).exclude(pk=pk)[:4]

    context = {
        'product': product,
        'images': images,
        'subcategory': subcategory,
        'category': category,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)


# ======================================================
# SEARCH
# ======================================================
def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Product.objects.filter(name__icontains=query)
    return render(request, 'shop/search_results.html', {'query': query, 'results': results})


# ======================================================
# CART
# ======================================================
def cart(request):
    return render(request, 'shop/cart.html')


# ======================================================
# PROFILE & WISHLIST
# ======================================================
def profile_view(request):
    """
    Display the user's profile information along with their wishlist items.
    """
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user).select_related('product')

    context = {
        'user': user,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'shop/profile.html', context)


@require_POST
def toggle_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        in_wishlist = False
    else:
        wishlist.products.add(product)
        in_wishlist = True
    
    return JsonResponse({'in_wishlist': in_wishlist})


# ======================================================
# AUTHENTICATION
# ======================================================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect("/admin/")
            next_url = request.POST.get("next") or request.GET.get("next") or "home"
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "shop/login.html", {"login_form": True})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'shop/login.html', {'register_form': True, 'form': form})


# ======================================================
# STATIC PAGES
# ======================================================
def services(request):
    """Display our jewelry services page."""
    return render(request, 'shop/services.html')

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/contact.html')

def category_products(request, id):
    category = get_object_or_404(Category, id=id)
    products = Jewellery.objects.filter(category=category)
    return render(request, 'shop/category_products.html', {
        'category': category,
        'products': products,
    })

def all_products(request):
    """Display all available products across all categories and subcategories."""
    products = Product.objects.filter(in_stock=True).order_by('-created_at')
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'shop/all_products.html', context)

def profile_edit(request):
    """
    Allow users to edit their username and email.
    """
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Update fields
        user.username = username
        user.email = email
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    context = {'user': user}
    return render(request, 'shop/profile_edit.html', context)


def edit_profile_view(request):
    """
    Allow the user to update their profile details.
    """
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        if not username or not email:
            messages.error(request, "Username and email cannot be empty.")
            return redirect('edit_profile')

        # Update and save
        user.username = username
        user.email = email
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'shop/edit_profile.html', {'user': user})


# ===== CHANGE PASSWORD PAGE =====
def change_password_view(request):
    """
    Allow user to change their password securely.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, "Your password has been updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'shop/change_password.html', {'form': form})

def wishlist_toggle(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user, product=product
        )

        if not created:
            wishlist_item.delete()
            return JsonResponse({"success": True, "added": False})
        else:
            return JsonResponse({"success": True, "added": True})

    return JsonResponse({"success": False, "message": "Invalid request"})

def wishlist_view(request):
    """Display all wishlist items for the logged-in user."""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "shop/wishlist.html", {"wishlist_items": wishlist_items})