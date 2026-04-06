# context_processors.py
def cart_context(request):
    # Simple cart implementation using session
    cart = request.session.get('cart', {})
    cart_items_count = sum(cart.values())
    return {
        'cart_items_count': cart_items_count,
    }