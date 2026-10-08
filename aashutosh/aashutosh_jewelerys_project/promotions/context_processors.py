from django.utils import timezone
from .models import Campaign


def promotion_context(request):
    """
    Safely inject the active festival/promotion campaign into all templates.
    Returns:
      - active_campaign: The currently active Campaign instance (or None)
      - promotion_enabled: True if an active campaign exists, False otherwise
    """
    try:
        now = timezone.now()
        active_campaigns = Campaign.objects.filter(is_active=True)
        
        valid_campaign = None
        for campaign in active_campaigns:
            if campaign.start_date and now < campaign.start_date:
                continue
            if campaign.end_date and now > campaign.end_date:
                continue
            valid_campaign = campaign
            break

        if valid_campaign:
            return {
                'active_campaign': valid_campaign,
                'promotion_enabled': True,
            }
    except Exception:
        # Guarantee safety in case tables are being migrated or missing
        pass

    return {
        'active_campaign': None,
        'promotion_enabled': False,
    }
