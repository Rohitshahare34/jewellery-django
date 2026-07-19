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

from .models import Product, Category, SubCategory, Wishlist, PopupMessage, Testimonial, Reel, MetalRate, SignatureCollection, SignatureCollectionItem

# ======================================================
# LIVE RATES VIEW
# ======================================================
def live_rates(request):
    """Today's Rates Page"""
    rates = MetalRate.objects.filter(status=True).order_by('metal_type')
    rates_with_breakdown = []
    
    for rate in rates:
        base_price = rate.rate_per_gram
        
        # Calculate making amount for 1 gram
        making_amount = 0
        if rate.show_making_charge:
            if rate.making_type == 'FIXED':
                making_amount = rate.making_charge
            else:
                making_amount = base_price * (rate.making_charge / 100)
                
        subtotal = base_price + making_amount
        
        # Calculate GST
        gst_amount = (subtotal * rate.gst_percentage / 100) if rate.show_gst else 0
        total_amount = subtotal + gst_amount
        
        rates_with_breakdown.append({
            'rate': rate,
            'breakdown': {
                'base_price': base_price,
                'making_amount': making_amount,
                'subtotal': subtotal,
                'gst_amount': gst_amount,
                'total_amount': total_amount
            }
        })
        
    return render(request, 'shop/live_rates.html', {
        'rates_with_breakdown': rates_with_breakdown
    })


def rate_calculator(request):
    """Rate Calculator Page"""
    metal_rates = MetalRate.objects.filter(status=True).order_by('metal_type')
    
    selected_metal = request.GET.get('metal', None)
    weight = request.GET.get('weight', None)
    
    breakdown = None
    selected_rate = None
    
    if selected_metal and weight:
        try:
            weight = float(weight)
            # Find selected rate in database
            selected_rate = MetalRate.objects.filter(metal_type=selected_metal).first()
            
            if selected_rate:
                base_price = selected_rate.rate_per_gram * weight
                making_amount = 0
                if selected_rate.show_making_charge:
                    if selected_rate.making_type == 'FIXED':
                        making_amount = selected_rate.making_charge * weight
                    else:
                        making_amount = base_price * (selected_rate.making_charge / 100)
                
                subtotal = base_price + making_amount
                gst_amount = (subtotal * selected_rate.gst_percentage / 100) if selected_rate.show_gst else 0
                total_amount = subtotal + gst_amount
                
                breakdown = {
                    'base_price': base_price,
                    'making_amount': making_amount,
                    'subtotal': subtotal,
                    'gst_amount': gst_amount,
                    'total_amount': total_amount
                }
        except Exception as e:
            pass
            
    return render(request, 'shop/rate_calculator.html', {
        'metal_rates': metal_rates,
        'selected_metal': selected_metal,
        'weight': weight,
        'breakdown': breakdown,
        'selected_rate': selected_rate
    })


# ======================================================
# HOME PAGE VIEW
# ======================================================
def home(request):
    featured_products = Product.objects.filter(is_featured=True, in_stock=True)[:8]
    new_arrivals = Product.objects.filter(badge='NEW', in_stock=True)[:6]
    categories = Category.objects.all()[:4]
    testimonials = Testimonial.objects.filter(is_approved=True)
    featured_subcategories = SubCategory.objects.filter(is_featured=True)
    reels = Reel.objects.filter(is_active=True, video__isnull=False).exclude(video='')
    
    # Get active Signature Collection
    signature_collection = SignatureCollection.objects.filter(is_active=True).first()
    signature_items = []
    if signature_collection:
        signature_items = SignatureCollectionItem.objects.filter(collection=signature_collection, is_active=True).order_by('sort_order')

    # Get metal rates to display on home page
    metal_rates = MetalRate.objects.filter(status=True).order_by('metal_type')

    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'hero_videos': [1, 2, 3],  # pass the number of hero videos
        'testimonials': testimonials,
        'featured_subcategories': featured_subcategories,
        'reels': reels,
        'signature_collection': signature_collection,
        'signature_items': signature_items,
        'metal_rates': metal_rates,
    }
    return render(request, 'shop/home.html', context)


# ======================================================
# SHOP PAGE VIEW
# ======================================================
def shop_view(request):
    products = Product.objects.filter(in_stock=True)

    # Filters
    category_filter = request.GET.getlist('category')
    stone_filter = request.GET.get('stone_type')
    color_filter = request.GET.get('color')
    badge_filter = request.GET.get('badge')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    if category_filter:
        products = products.filter(subcategory__category__id__in=category_filter)
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
    products = Product.objects.filter(subcategory=subcategory, in_stock=True)
    
    context = {
        'subcategory': subcategory,
        'products': products,
    }
    return render(request, 'shop/subcategory_products.html', context)


# ======================================================
# PRODUCT DETAIL VIEW
# ======================================================
def product_detail(request, pk):
    # Get the product by ID
    product = get_object_or_404(Product, pk=pk)

    # Get all related images (safe check)
    images = product.images.all() if hasattr(product, 'images') else []

    # Get subcategory and main category safely
    subcategory = product.subcategory
    category = subcategory.category if subcategory else None

    # Fetch related products from the same subcategory
    related_products = Product.objects.filter(
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
        results = Product.objects.filter(name__icontains=query, in_stock=True)
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
    wishlist_items = Wishlist.objects.filter(user=user, product__isnull=False).select_related('product')

    context = {
        'user': user,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'shop/profile.html', context)


@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user, product=product
    )
    if not created:
        wishlist_item.delete()
        in_wishlist = False
    else:
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
    products = Product.objects.filter(subcategory__category=category)
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
        if not request.user.is_authenticated:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Content-Type') == 'application/json' or 'application/json' in request.META.get('HTTP_ACCEPT', ''):
                return JsonResponse({"success": False, "message": "Authentication required"}, status=401)
            return redirect('login')

        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user, product=product
        )

        if not created:
            wishlist_item.delete()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Content-Type') == 'application/json' or 'application/json' in request.META.get('HTTP_ACCEPT', ''):
                return JsonResponse({"success": True, "added": False, "status": "removed"})
            return redirect('wishlist')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Content-Type') == 'application/json' or 'application/json' in request.META.get('HTTP_ACCEPT', ''):
                return JsonResponse({"success": True, "added": True, "status": "added"})
            return redirect('wishlist')

    return JsonResponse({"success": False, "message": "Invalid request"})

def wishlist_view(request):
    """Display all wishlist items for the logged-in user."""
    wishlist_items = Wishlist.objects.filter(user=request.user, product__isnull=False).select_related("product")
    return render(request, "shop/wishlist.html", {"wishlist_items": wishlist_items})


# ======================================================
# METAL PRICE API ENDPOINTS
# ======================================================
def get_metal_prices(request):
    """
    AJAX endpoint to fetch latest metal prices from database.
    Returns JSON response with gold and silver prices.
    """
    try:
        rates = MetalRate.objects.filter(status=True)
        rates_dict = {}
        for r in rates:
            rates_dict[r.metal_type.lower()] = str(r.rate_per_gram)
            
        gold_24k = rates.filter(metal_type='GOLD_24K').first()
        gold_22k = rates.filter(metal_type='GOLD_22K').first()
        gold_18k = rates.filter(metal_type='GOLD_18K').first()
        silver = rates.filter(metal_type='SILVER').first()
        
        response_data = {
            'success': True,
            'rates': rates_dict,
            'gold': {
                'price': str(gold_24k.rate_per_gram) if gold_24k else '0',
                'price_24k': str(gold_24k.rate_per_gram) if gold_24k else '0',
                'price_22k': str(gold_22k.rate_per_gram) if gold_22k else '0',
                'price_18k': str(gold_18k.rate_per_gram) if gold_18k else '0',
                'change_percent': '0',
                'is_up': True,
            },
            'silver': {
                'price': str(silver.rate_per_gram) if silver else '0',
                'change_percent': '0',
                'is_up': True,
            },
        }
        
        last_updated = "Updated today"
        response_data['gold']['last_updated'] = last_updated
        response_data['silver']['last_updated'] = last_updated
            
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@require_POST
def refresh_metal_prices(request):
    """
    Manual trigger to refresh metal prices (dummy response since MetalPrice is removed).
    """
    return JsonResponse({
        'success': True,
        'message': 'Prices are managed manually via Today\'s Rates admin panel.'
    })


@require_POST
def submit_testimonial(request):
    """Saves submitted customer feedback to database and returns JSON."""
    name = request.POST.get('name', '').strip()
    rating = request.POST.get('rating', '5')
    message = request.POST.get('message', '').strip()
    designation = request.POST.get('designation', '').strip()

    if not designation:
        designation = 'Verified Buyer'

    if not name or not message:
        return JsonResponse({'success': False, 'error': 'Name and feedback message are required.'}, status=400)

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            rating = 5
    except ValueError:
        rating = 5

    image = request.FILES.get('image')

    testimonial = Testimonial.objects.create(
        name=name,
        rating=rating,
        message=message,
        designation=designation,
        image=image,
        is_approved=True  # Auto-approve so it shows on front page instantly
    )

    return JsonResponse({
        'success': True,
        'testimonial': {
            'name': testimonial.name,
            'rating': testimonial.rating,
            'message': testimonial.message,
            'designation': testimonial.designation,
            'image_url': testimonial.image.url if testimonial.image else None,
            'created_at': testimonial.created_at.strftime('%Y-%m-%d')
        }
    })