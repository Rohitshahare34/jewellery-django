"""
Metal Price API Integration Module
Fetches live gold and silver prices from GoldAPI.io
"""
import requests
import logging
from django.conf import settings
from decimal import Decimal
from datetime import datetime

logger = logging.getLogger(__name__)

# Constants
TROY_OUNCE_TO_GRAM = Decimal('31.1035')  # 1 troy ounce = 31.1035 grams
USD_TO_INR = Decimal('83.50')  # Approximate conversion rate (you can make this dynamic)


def fetch_gold_price():
    """
    Fetch current gold price from API in USD, convert to INR, add Maharashtra margin
    Returns: dict with price_per_gram (24K), change_percent, is_up
    """
    try:
        api_key = settings.GOLD_API_KEY
        
        if not api_key or api_key == 'your_api_key_here':
            logger.warning("API key not configured. Using demo data.")
            return get_demo_gold_price()
        
        # GoldAPI.io endpoint - XAU/USD (more reliable)
        url = "https://www.goldapi.io/api/XAU/USD"
        headers = {
            'x-access-token': api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # API returns price per GRAM in USD
        price_gram_24k_usd = Decimal(str(data.get('price_gram_24k', 0)))
        
        # Convert USD to INR (approximate rate)
        usd_to_inr = Decimal('84.50')  # Current approx rate
        price_gram_24k_inr_base = price_gram_24k_usd * usd_to_inr
        
        # Add Maharashtra market adjustment (~8-10% for local taxes, margins)
        maharashtra_margin = Decimal('1.08')  # 8% adjustment for Maharashtra rates
        price_gram_24k_inr = price_gram_24k_inr_base * maharashtra_margin
        
        # Calculate 22K price (91.67% of 24K)
        price_gram_22k_inr = price_gram_24k_inr * Decimal('0.9167')
        
        # Get change percentage
        change_percent = Decimal(str(data.get('chp', 0)))
        is_up = change_percent >= 0
        
        logger.info(f"Gold 24K: ${price_gram_24k_usd} = Base ₹{price_gram_24k_inr_base} = Maharashtra ₹{price_gram_24k_inr}")
        
        return {
            'price_per_gram': round(price_gram_24k_inr, 2),
            'price_24k': round(price_gram_24k_inr, 2),
            'price_22k': round(price_gram_22k_inr, 2),
            'change_percent': abs(change_percent),
            'is_up': is_up,
        }
        
    except Exception as e:
        logger.error(f"Error fetching gold price: {e}")
        return get_demo_gold_price()


def fetch_silver_price():
    """
    Fetch current silver price from API in USD, convert to INR, add Maharashtra margin
    Returns: dict with price_per_gram, change_percent, is_up
    """
    try:
        api_key = settings.GOLD_API_KEY
        
        if not api_key or api_key == 'your_api_key_here':
            logger.warning("API key not configured. Using demo data.")
            return get_demo_silver_price()
        
        # GoldAPI.io endpoint for Silver in USD
        url = "https://www.goldapi.io/api/XAG/USD"
        headers = {
            'x-access-token': api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # API returns price per GRAM in USD (silver uses price_gram_24k field)
        price_gram_usd = Decimal(str(data.get('price_gram_24k', 0)))
        
        # Convert USD to INR
        usd_to_inr = Decimal('84.50')
        price_gram_inr_base = price_gram_usd * usd_to_inr
        
        # Add Maharashtra market adjustment (~8%)
        maharashtra_margin = Decimal('1.08')
        price_gram_inr = price_gram_inr_base * maharashtra_margin
        
        # Get change percentage
        change_percent = Decimal(str(data.get('chp', 0)))
        is_up = change_percent >= 0
        
        logger.info(f"Silver: ${price_gram_usd} = Base ₹{price_gram_inr_base} = Maharashtra ₹{price_gram_inr}")
        
        return {
            'price_per_gram': round(price_gram_inr, 2),
            'change_percent': abs(change_percent),
            'is_up': is_up,
        }
        
    except Exception as e:
        logger.error(f"Error fetching silver price: {e}")
        return get_demo_silver_price()


def get_demo_gold_price():
    """Return demo gold price for testing/development (Maharashtra rates)"""
    price_24k = Decimal('14850.00')  # Maharashtra 24K rate
    return {
        'price_per_gram': price_24k,
        'price_24k': price_24k,
        'price_22k': price_24k * Decimal('0.9167'),  # ₹13,613
        'change_percent': Decimal('0.45'),
        'is_up': True,
    }


def get_demo_silver_price():
    """Return demo silver price for testing/development (Maharashtra rates)"""
    return {
        'price_per_gram': Decimal('88.50'),  # Maharashtra silver rate
        'change_percent': Decimal('0.32'),
        'is_up': False,
    }


def update_metal_prices():
    """
    Fetch and update both gold and silver prices in database
    Returns: dict with success status and messages
    """
    from .models import MetalPrice
    
    try:
        # Fetch gold price
        gold_data = fetch_gold_price()
        
        # Update or create gold price
        gold_price, created = MetalPrice.objects.update_or_create(
            metal_type='GOLD',
            defaults={
                'price_per_gram': gold_data['price_per_gram'],  # 24K
                'price_22k': gold_data.get('price_22k'),
                'change_percent': gold_data['change_percent'],
                'is_up': gold_data['is_up'],
            }
        )
        
        # Fetch silver price
        silver_data = fetch_silver_price()
        
        # Update or create silver price
        silver_price, created = MetalPrice.objects.update_or_create(
            metal_type='SILVER',
            defaults={
                'price_per_gram': silver_data['price_per_gram'],
                'change_percent': silver_data['change_percent'],
                'is_up': silver_data['is_up'],
            }
        )
        
        logger.info("Metal prices updated successfully")
        return {
            'success': True,
            'message': 'Prices updated successfully',
            'gold': gold_data,
            'silver': silver_data,
        }
        
    except Exception as e:
        logger.error(f"Error updating metal prices: {e}")
        return {
            'success': False,
            'message': f'Error updating prices: {str(e)}',
        }
