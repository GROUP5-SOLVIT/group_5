import decimal

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.db.models import Q
from django.db.models.functions import Lower


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='InventoryCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('symbol', models.CharField(max_length=24)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('sku', models.CharField(blank=True, max_length=64, null=True)),
                ('description', models.TextField(blank=True)),
                ('minimum_stock_level', models.DecimalField(decimal_places=3, default=decimal.Decimal('0.000'), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal('0'))])),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('base_unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='inventory.unitofmeasure')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='inventory.inventorycategory')),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='StockBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=3, default=decimal.Decimal('0.000'), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal('0'))])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stock_balance', to='inventory.inventoryitem')),
            ],
            options={'ordering': ['item__name']},
        ),
        migrations.AddConstraint(
            model_name='inventorycategory',
            constraint=models.UniqueConstraint(Lower('name'), name='inventory_category_name_ci_uniq'),
        ),
        migrations.AddConstraint(
            model_name='unitofmeasure',
            constraint=models.UniqueConstraint(Lower('name'), name='inventory_unit_name_ci_uniq'),
        ),
        migrations.AddConstraint(
            model_name='unitofmeasure',
            constraint=models.UniqueConstraint(Lower('symbol'), name='inventory_unit_symbol_ci_uniq'),
        ),
        migrations.AddConstraint(
            model_name='inventoryitem',
            constraint=models.UniqueConstraint(Lower('sku'), condition=Q(sku__isnull=False) & ~Q(sku=''), name='inventory_item_sku_ci_uniq'),
        ),
        migrations.AddConstraint(
            model_name='inventoryitem',
            constraint=models.CheckConstraint(condition=Q(minimum_stock_level__gte=0), name='inventory_item_min_stock_nonnegative'),
        ),
        migrations.AddConstraint(
            model_name='stockbalance',
            constraint=models.CheckConstraint(condition=Q(quantity__gte=0), name='inventory_stock_quantity_nonnegative'),
        ),
    ]
