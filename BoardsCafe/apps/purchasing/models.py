import uuid
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Supplier(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        SUSPENDED = "suspended", "Suspended"

    name = models.CharField(max_length=200, unique=True)
    contact_person = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    tax_id = models.CharField(max_length=64, blank=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_cafe_suppliers",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Purchase(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ORDERED = "ordered", "Ordered"
        PARTIALLY_RECEIVED = "partially_received", "Partially received"
        RECEIVED = "received", "Received"
        CANCELLED = "cancelled", "Cancelled"

    purchase_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchases",
    )
    purchase_date = models.DateField()
    expected_delivery_date = models.DateField(null=True, blank=True)
    supplier_invoice = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=24,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="cafe_purchases",
    )
    ordered_at = models.DateTimeField(null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-purchase_date", "-created_at"]

    @property
    def total_amount(self):
        return sum(
            (item.ordered_quantity * item.unit_cost for item in self.items.all()),
            Decimal("0.00"),
        )

    def __str__(self):
        return str(self.purchase_number)


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="items",
    )
    inventory_item = models.ForeignKey(
        "inventory.InventoryItem",
        on_delete=models.PROTECT,
        related_name="purchase_items",
    )
    ordered_quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        validators=[MinValueValidator(Decimal("0.001"))],
    )
    received_quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        default=Decimal("0.000"),
        validators=[MinValueValidator(Decimal("0.000"))],
    )
    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["inventory_item__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["purchase", "inventory_item"],
                name="purchase_unique_inventory_item",
            ),
            models.CheckConstraint(
                condition=Q(ordered_quantity__gt=0),
                name="purchase_item_ordered_quantity_positive",
            ),
            models.CheckConstraint(
                condition=Q(received_quantity__gte=0),
                name="purchase_item_received_quantity_nonnegative",
            ),
            models.CheckConstraint(
                condition=Q(unit_cost__gte=0),
                name="purchase_item_unit_cost_nonnegative",
            ),
        ]

    @property
    def line_total(self):
        return self.ordered_quantity * self.unit_cost

    def __str__(self):
        return f"{self.inventory_item.name} ({self.purchase})"


class PurchaseReceipt(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.PROTECT,
        related_name="receipts",
    )
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="purchase_receipts",
    )
    received_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-received_at"]

    def __str__(self):
        return f"Receipt for {self.purchase}"


class PurchaseReceiptItem(models.Model):
    receipt = models.ForeignKey(
        PurchaseReceipt,
        on_delete=models.CASCADE,
        related_name="items",
    )
    purchase_item = models.ForeignKey(
        PurchaseItem,
        on_delete=models.PROTECT,
        related_name="receipt_items",
    )
    batch_number = models.CharField(max_length=100, blank=True)
    quantity_received = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        validators=[MinValueValidator(Decimal("0.001"))],
    )
    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity_received__gt=0),
                name="receipt_item_quantity_positive",
            ),
            models.CheckConstraint(
                condition=Q(unit_cost__gte=0),
                name="receipt_item_unit_cost_nonnegative",
            ),
        ]

    def __str__(self):
        return f"{self.purchase_item.inventory_item.name}: {self.quantity_received}"
