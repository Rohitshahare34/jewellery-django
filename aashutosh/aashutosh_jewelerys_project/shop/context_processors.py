import json

def cart_context(request):
    # Simple cart implementation using session
    cart = request.session.get('cart', {})
    cart_items_count = sum(cart.values())
    return {
        'cart_items_count': cart_items_count,
    }


def metal_prices_context(request):
    """
    Add metal prices to global template context.
    This makes gold and silver prices available in all templates.
    """
    from .models import MetalPrice, MetalRate
    
    gold_price = MetalPrice.objects.filter(metal_type='GOLD').first()
    silver_price = MetalPrice.objects.filter(metal_type='SILVER').first()
    
    # Retrieve active rates and serialize to JSON list of dicts
    rates_list = []
    for rate in MetalRate.objects.filter(status=True):
        rates_list.append({
            'metal_type': rate.get_metal_type_display(),
            'metal_code': rate.metal_type,
            'purity': float(rate.purity),
            'rate_per_gram': float(rate.rate_per_gram),
            'making_charge': float(rate.making_charge),
            'making_type': rate.making_type,
            'gst_percentage': float(rate.gst_percentage)
        })
    
    return {
        'gold_price': gold_price,
        'silver_price': silver_price,
        'metal_rates_json': json.dumps(rates_list)
    }


def popup_context(request):
    """
    Add active popup message to template context.
    Shows popup on home page and rate page when status is True.
    """
    from .models import PopupMessage
    
    # Show popup on home page and rate page
    if request.path == '/' or request.path == '/live-rates/' or request.path == '/rate-calculator/':
        popup = PopupMessage.objects.filter(status=True).first()
        return {'popup': popup}
    
    return {'popup': None}