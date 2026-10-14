from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import InventoryItem, StockBalance


@receiver(post_save, sender=InventoryItem)
def initialize_stock_balance(sender, instance, created, **kwargs):
    if created:
        StockBalance.objects.get_or_create(item=instance, defaults={'quantity': Decimal('0.000')})
