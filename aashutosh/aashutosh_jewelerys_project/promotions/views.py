from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from .models import Campaign, PromotionalCoupon


def campaign_detail(request, slug):
    """
    Campaign landing page displaying campaign graphics, countdown timer, 
    discount terms, and featured products.
    """
    campaign = get_object_or_404(Campaign, slug=slug)
    featured_products = campaign.featured_products.all()
    target_categories = campaign.target_categories.all()
    
    context = {
        'campaign': campaign,
        'featured_products': featured_products,
        'target_categories': target_categories,
    }
    return render(request, 'promotions/campaign_detail.html', context)


def active_campaign_view(request):
    """
    Short URL endpoint /offers/ redirecting to or showing the active campaign.
    """
    now = timezone.now()
    campaigns = Campaign.objects.filter(is_active=True)
    active_campaign = None
    for c in campaigns:
        if c.start_date and now < c.start_date:
            continue
        if c.end_date and now > c.end_date:
            continue
        active_campaign = c
        break

    if active_campaign:
        return redirect('promotions:campaign_detail', slug=active_campaign.slug)
    
    # Fallback if no active campaign: render offers fallback or redirect home
    return redirect('home')


@csrf_protect
@require_POST
def validate_coupon_api(request):
    """
    API endpoint to validate a promo code against cart total.
    """
    import json
    try:
        data = json.loads(request.body.decode('utf-8'))
        code = data.get('code', '').strip().upper()
        cart_total = float(data.get('cart_total', 0))
    except Exception:
        code = request.POST.get('code', '').strip().upper()
        cart_total = float(request.POST.get('cart_total', 0))

    if not code:
        return JsonResponse({'valid': False, 'message': 'Please enter a valid coupon code.'}, status=400)

    try:
        coupon = PromotionalCoupon.objects.get(code=code)
        valid, msg = coupon.is_valid(cart_total)
        if valid:
            discount_amount = coupon.calculate_discount(cart_total)
            final_total = max(0, cart_total - discount_amount)
            return JsonResponse({
                'valid': True,
                'message': msg,
                'code': coupon.code,
                'discount_type': coupon.discount_type,
                'discount_value': float(coupon.discount_value),
                'discount_amount': round(discount_amount, 2),
                'final_total': round(final_total, 2),
            })
        else:
            return JsonResponse({'valid': False, 'message': msg}, status=400)
    except PromotionalCoupon.DoesNotExist:
        return JsonResponse({'valid': False, 'message': f"Coupon code '{code}' is invalid or expired."}, status=404)
