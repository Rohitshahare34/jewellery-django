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
    from .models import MetalRate
    
    gold_24k = MetalRate.objects.filter(metal_type='GOLD_24K', status=True).first()
    gold_22k = MetalRate.objects.filter(metal_type='GOLD_22K', status=True).first()
    gold_18k = MetalRate.objects.filter(metal_type='GOLD_18K', status=True).first()
    silver = MetalRate.objects.filter(metal_type='SILVER', status=True).first()
    
    # Build rates list dynamically from MetalRate database records
    rates_list = []
    rates = MetalRate.objects.filter(status=True).order_by('metal_type')
    
    for rate in rates:
        rates_list.append({
            'metal_type': rate.get_metal_type_display(),
            'metal_code': rate.metal_type,
            'purity': float(rate.purity),
            'rate_per_gram': float(rate.rate_per_gram),
            'making_charge': float(rate.making_charge),
            'making_type': rate.making_type,
            'gst_percentage': float(rate.gst_percentage)
        })
        
    # Backward compatibility mock class for gold_price references in templates
    class MockGoldPrice:
        def __init__(self, p24, p22):
            self.price_per_gram = p24
            self.price_22k = p22
        def last_updated_formatted(self):
            return "Updated today"
            
    mock_gold = MockGoldPrice(
        gold_24k.rate_per_gram if gold_24k else 0.0,
        gold_22k.rate_per_gram if gold_22k else 0.0
    )
    
    return {
        'gold_price': mock_gold,
        'gold_24k': gold_24k,
        'gold_22k': gold_22k,
        'gold_18k': gold_18k,
        'silver_rate': silver,
        'active_rates': rates,
        'metal_rates_json': json.dumps(rates_list)
    }


def popup_context(request):
    """
    Add active popup message to template context.
    Shows popup on home page when status is True.
    """
    from .models import PopupMessage
    
    # Show popup only on home page
    if request.path == '/':
        active_popup = PopupMessage.objects.filter(status=True).first()
        return {'active_popup': active_popup}
    
    return {'active_popup': None}


def wishlist_context(request):
    """Add user's wishlist product IDs and count to global context."""
    if request.user.is_authenticated:
        from .models import Wishlist
        wishlist_ids = list(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))
        return {'user_wishlist_ids': wishlist_ids, 'wishlist_count': len(wishlist_ids)}
    return {'user_wishlist_ids': [], 'wishlist_count': 0}