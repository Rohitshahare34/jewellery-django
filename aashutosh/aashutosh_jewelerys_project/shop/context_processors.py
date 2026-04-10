# context_processors.py
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
    from .models import MetalPrice
    
    gold_price = MetalPrice.objects.filter(metal_type='GOLD').first()
    silver_price = MetalPrice.objects.filter(metal_type='SILVER').first()
    
    return {
        'gold_price': gold_price,
        'silver_price': silver_price,
    }