from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # === Home Page ===
    path('', views.home, name='home'),

    # === Shop Pages ===
    path('shop/', views.shop_view, name='shop'),
    path('categories/', views.shop_by_category, name='shop_by_category'),

    # === Category & Subcategory Navigation ===
    path('category/<int:id>/', views.category_products, name='category_products'),
    path('category/<int:category_id>/subcategories/', views.category_subcategories, name='category_subcategories'),
    path('subcategory/<int:subcategory_id>/', views.subcategory_products, name='subcategory_products'),

    # === All Products ===
    path('all-products/', views.all_products, name='all_products'),

    # === Product Details ===
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # === Search ===
    path('search/', views.search, name='search'),

    # === Cart ===
    path('cart/', views.cart, name='cart'),

    # === Wishlist ===
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.wishlist_toggle, name='wishlist_toggle'),

    # === User Profile ===
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('change-password/', views.change_password_view, name='change_password'),

    # === Static Pages ===
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # === Authentication ===
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # === Metal Price API ===
    path('api/metal-prices/', views.get_metal_prices, name='get_metal_prices'),
    path('api/refresh-prices/', views.refresh_metal_prices, name='refresh_metal_prices'),
]
