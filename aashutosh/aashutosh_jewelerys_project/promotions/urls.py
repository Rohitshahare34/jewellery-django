from django.urls import path
from . import views

app_name = 'promotions'

urlpatterns = [
    path('offers/', views.active_campaign_view, name='active_campaign'),
    path('campaign/<slug:slug>/', views.campaign_detail, name='campaign_detail'),
    path('api/validate-coupon/', views.validate_coupon_api, name='validate_coupon_api'),
]
