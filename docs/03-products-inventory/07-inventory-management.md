# 07 — Inventory Management

## 7.1 Introduction

Inventory management is a core part of the Board’s Cafe system. The module is responsible for recording, monitoring, receiving, consuming, adjusting, and controlling the stock used by the cafe.

The system must help staff know:

* What inventory items the cafe has
* How much stock is currently available
* Which items are running low
* Which stock has expired or is no longer usable
* Where stock came from
* How stock was received
* How much stock was consumed
* Why stock quantities were adjusted
* Which batches were used
* How inventory changes affect product production and sales

The inventory module works closely with the **Products & Recipes**, **Batch & Expiry Management**, **Purchases & Suppliers**, **POS & Order Management**, **Waste Management**, and **Reports & Dashboard** modules.

---

# 7.2 Inventory Management Objectives

The main objectives are to:

1. Maintain accurate inventory records.
2. Track quantities of ingredients and direct-sale items.
3. Support different units of measurement.
4. Track stock received from suppliers.
5. Track stock consumed during production.
6. Prevent expired stock from being used.
7. Support batch-level inventory tracking for applicable items.
8. Record all stock movements.
9. Detect low-stock items.
10. Support physical stock counting.
11. Record stock adjustments and their reasons.
12. Support traceability of inventory usage.
13. Reduce stock losses and unnecessary waste.
14. Provide reliable inventory information for management decisions.

---

# 7.3 Inventory Item Concept

An **Inventory Item** represents a physical item that the cafe stores and manages.

An inventory item may be:

* A raw ingredient
* A food ingredient
* A beverage ingredient
* A packaging/consumable item
* A direct-sale product that is stocked and sold without production

Examples include:

* Tomatoes
* Onions
* Lettuce
* Potatoes
* Milk
* Eggs
* Wheat flour
* Sugar
* Cooking oil
* Chicken
* Coffee beans
* Tea
* Bottled water
* Packaged juice
* Bread or buns

The inventory item is different from the customer-facing product concept described in Document 06.

For example:

**Inventory Item:**

> Tomatoes

**Products using it:**

* Burger
* Sandwich
* Pizza
* Salad

There must be one shared **Tomatoes** inventory item rather than separate tomato records for every product.

---

# 7.4 Inventory Item Master Data

Each inventory item should have information such as:

| Field               | Description                          |
| ------------------- | ------------------------------------ |
| Item ID             | Unique identifier                    |
| Item Name           | Name of the inventory item           |
| Category            | Inventory category                   |
| Description         | Optional description                 |
| Base Unit           | Main unit used for stock             |
| Purchase Unit       | Unit commonly used when purchasing   |
| Reorder Level       | Minimum desired stock level          |
| Maximum Stock Level | Optional desired upper level         |
| Track Batch         | Whether batches must be tracked      |
| Track Expiry        | Whether expiry dates must be tracked |
| Status              | Active, inactive, or blocked         |
| Notes               | Additional information               |

---

# 7.5 Inventory Categories

Inventory items should be organized into meaningful categories.

Examples include:

* Vegetables
* Fruits
* Dairy
* Meat
* Poultry
* Eggs
* Grains and Flour
* Oils
* Spices
* Baking Ingredients
* Coffee and Tea
* Beverages
* Packaged Products
* Bread and Bakery
* Other Consumables

The category structure should make it easier to search, filter, count, and report inventory.

---

# 7.6 Units of Measurement

Inventory must support different measurement types.

### Weight

Examples:

* Kilogram (kg)
* Gram (g)

Used for:

* Tomatoes
* Onions
* Flour
* Chicken
* Coffee beans
* Sugar

### Volume

Examples:

* Liter (L)
* Milliliter (ml)

Used for:

* Milk
* Cooking oil
* Juice
* Other liquids

### Count

Examples:

* Piece
* Unit
* Egg
* Bottle
* Packet

Used for:

* Eggs
* Bread
* Buns
* Bottled water
* Packaged products

---

# 7.7 Base Unit

Each inventory item should have a **base unit** used for internal stock calculations.

For example:

| Inventory Item | Base Unit |
| -------------- | --------- |
| Tomatoes       | kg        |
| Wheat Flour    | kg        |
| Milk           | L         |
| Cooking Oil    | L         |
| Eggs           | piece     |
| Bread Bun      | piece     |
| Chicken        | kg        |
| Coffee Beans   | kg        |

Using a consistent base unit makes stock calculations easier.

---

# 7.8 Unit Conversion

The system should support conversion between compatible units.

Examples:

* 1 kg = 1,000 g
* 1 L = 1,000 ml

Therefore:

If the cafe receives:

> 5 kg of tomatoes

the system can internally represent this as:

> 5 kg

or:

> 5,000 g

depending on the selected base unit.

Conversions should only occur between compatible measurement types.

For example:

* kg ↔ g is valid.
* L ↔ ml is valid.
* kg ↔ L is not automatically valid.

---

# 7.9 Current Stock

The system should maintain the current quantity of each inventory item.

For example:

| Item        | Current Stock | Unit   |
| ----------- | ------------: | ------ |
| Tomatoes    |            23 | kg     |
| Milk        |            18 | L      |
| Flour       |            40 | kg     |
| Eggs        |           120 | pieces |
| Cooking Oil |            15 | L      |

Current stock should be derived from recorded inventory transactions rather than being changed without an explanation.

---

# 7.10 Usable Stock

The system should distinguish between **total physical stock** and **usable stock**.

Usable stock is the quantity that can currently be used for production or sale.

For example:

Tomatoes:

* Batch A: 5 kg — expired
* Batch B: 8 kg — valid
* Batch C: 10 kg — valid

Total physical stock:

> 23 kg

Usable stock:

> 18 kg

The expired 5 kg must not be available for production.

---

# 7.11 Stock Status

Inventory quantities may have different statuses.

Examples include:

* Available
* Reserved
* Expired
* Damaged
* Spoiled
* Blocked
* Quarantined
* Consumed

Only appropriate available stock should be considered usable.

The exact statuses may be controlled by the inventory and batch/expiry workflows.

---

# 7.12 Stock Receiving

When new inventory arrives at the cafe, staff should record the received stock.

A stock receipt should capture information such as:

* Inventory item
* Quantity
* Unit
* Supplier
* Purchase reference
* Date received
* Unit cost
* Total cost
* Batch information where applicable
* Expiry date where applicable
* Staff member who received the stock

For example:

> 20 kg of tomatoes received from a supplier.

The system records the receipt and increases the available inventory.

---

# 7.13 Receiving Perishable Stock

For items that require batch and expiry tracking, receiving stock should create a batch record.

Example:

> Tomatoes
> Quantity: 10 kg
> Batch: TOM-2026-001
> Expiry: 10 October 2026

The system should associate the received quantity with that batch.

This allows the cafe to know exactly which stock is approaching expiry.

---

# 7.14 Stock Increase

Inventory can increase through legitimate stock-in transactions.

Examples include:

* Purchase receipt
* Supplier delivery
* Approved stock adjustment
* Returned stock, where applicable
* Other approved inventory additions

Every increase should have a recorded reason.

---

# 7.15 Stock Decrease

Inventory can decrease through legitimate stock-out transactions.

Examples include:

* Ingredient consumption
* Direct-sale product sale
* Waste
* Expired stock removal
* Damaged stock
* Approved stock adjustment
* Other approved inventory movements

The system should not simply reduce a quantity without recording why the quantity changed.

---

# 7.16 Stock Movements

A **Stock Movement** represents a change in inventory quantity.

Typical movement types include:

| Movement Type  | Purpose                                 |
| -------------- | --------------------------------------- |
| RECEIPT        | Stock received                          |
| CONSUMPTION    | Ingredient used                         |
| SALE           | Direct-sale item sold                   |
| WASTE          | Stock wasted                            |
| EXPIRY         | Expired stock removed                   |
| ADJUSTMENT_IN  | Approved increase                       |
| ADJUSTMENT_OUT | Approved decrease                       |
| RETURN         | Stock returned                          |
| TRANSFER       | Stock moved between supported locations |

Each movement should contain enough information to explain the change.

---

# 7.17 Stock Movement Information

A stock movement may contain:

* Movement ID
* Inventory item
* Batch, when applicable
* Movement type
* Quantity
* Unit
* Reference
* Reason
* Date and time
* User who performed the action
* Related order, purchase, waste record, or adjustment where applicable
* Notes

This creates an inventory history that can be reviewed later.

---

# 7.18 Inventory Consumption Through Recipes

Recipe-based products consume inventory items.

For example, suppose a burger recipe requires:

* 100 g tomatoes
* 150 g beef
* 50 g lettuce
* 1 bun

When one burger is produced, the required quantities are deducted from inventory.

If a customer orders two burgers:

* Tomatoes: 200 g
* Beef: 300 g
* Lettuce: 100 g
* Buns: 2 pieces

The system should calculate these requirements from the recipe.

---

# 7.19 Shared Ingredient Consumption

When multiple products in an order use the same ingredient, the system should aggregate the requirement.

Example order:

* 2 Burgers
* 1 Sandwich
* 1 Pizza
* 1 Salad

If all four products use tomatoes, the system should calculate the **total tomato requirement** for the complete order.

It should not treat each product's tomato usage as an isolated inventory stock.

This allows the system to correctly determine whether enough tomatoes are available.

---

# 7.20 Inventory Availability Check

Before production, the system should check whether sufficient usable inventory exists.

For example:

A customer orders products requiring:

> 6 kg tomatoes

Current usable tomato stock:

> 5 kg

The system should identify that the available stock is insufficient.

Expired tomatoes must not be included in the calculation.

---

# 7.21 Inventory Reservation

Where required by the order workflow, inventory may be temporarily reserved for an order or production process.

Reserved inventory should not be counted as freely available for another production request.

For example:

Available tomatoes:

> 10 kg

Order A reserves:

> 4 kg

Remaining freely available stock:

> 6 kg

This helps prevent multiple orders from assuming the same stock is available.

The exact reservation behavior should follow the POS and order-management workflow.

---

# 7.22 Batch-Based Consumption

For batch-tracked inventory, consumption should be linked to the appropriate batch.

Example:

Tomato stock:

| Batch | Quantity | Expiry |
| ----- | -------: | ------ |
| A     |     5 kg | Oct 10 |
| B     |     8 kg | Oct 13 |
| C     |    10 kg | Oct 17 |

Production requires:

> 6 kg

The system should consume:

> 5 kg from Batch A
> 1 kg from Batch B

This leaves:

* Batch A: 0 kg
* Batch B: 7 kg
* Batch C: 10 kg

---

# 7.23 FEFO Consumption

For applicable perishable inventory, the system should use **FEFO — First-Expire, First-Out**.

The system selects the valid batch with the earliest expiry date before later-expiring batches.

Example:

| Batch | Quantity | Expiry |
| ----- | -------: | ------ |
| A     |     5 kg | Oct 10 |
| B     |     8 kg | Oct 13 |
| C     |    10 kg | Oct 17 |

For a 6 kg requirement:

1. Use Batch A first.
2. Use 1 kg from Batch B.
3. Do not use Batch C.

This reduces the likelihood of stock expiring unnecessarily.

---

# 7.24 Expired Stock

Expired inventory must not be treated as usable inventory.

When a batch reaches its expiry date, the system should identify it as expired according to the batch and expiry rules.

Expired stock should:

* Remain visible in inventory history
* Be excluded from usable stock
* Not be selected for production
* Not be used to satisfy recipe requirements
* Be available for expiry/waste processing
* Remain traceable

---

# 7.25 Low-Stock Monitoring

Each relevant inventory item may have a **reorder level**.

Example:

> Milk reorder level = 10 L

Current usable stock:

> 7 L

The system should identify milk as low stock.

Low-stock information can be used by authorized staff to decide when more inventory should be purchased.

---

# 7.26 Stock Counting

The system should support physical inventory counting.

Staff may periodically compare:

> System Quantity

with:

> Physically Counted Quantity

Example:

System says:

> Tomatoes = 20 kg

Physical count:

> Tomatoes = 18.5 kg

Difference:

> -1.5 kg

An authorized staff member can record an adjustment with an appropriate reason.

---

# 7.27 Inventory Adjustments

Inventory adjustments should be used when the physical quantity differs from the system quantity or when an authorized correction is required.

Examples:

* Physical count difference
* Damaged stock discovered
* Spoilage
* Measurement correction
* Data-entry error
* Other approved reason

Adjustments should never silently overwrite the existing quantity.

Instead, the adjustment should create an inventory movement.

---

# 7.28 Adjustment Approval

Depending on the permission structure, some inventory adjustments may require authorization.

For example:

A staff member may have permission to:

> `inventory.view`

but not:

> `inventory.adjust`

An authorized manager or administrator can perform or approve the adjustment.

This follows the RBAC model defined in Document 04.

---

# 7.29 Direct-Sale Inventory Items

Some products may be sold directly without recipe-based production.

Examples:

* Bottled water
* Packaged juice
* Other packaged products

When such a product is sold, its inventory quantity should decrease directly.

Example:

Stock:

> Bottled Water = 50 bottles

Customer buys:

> 3 bottles

Remaining stock:

> 47 bottles

This is different from a recipe-based product, where ingredient inventory is consumed.

---

# 7.30 Recipe-Based vs Direct-Sale Inventory Impact

| Product Type | Inventory Effect                   |
| ------------ | ---------------------------------- |
| Recipe-based | Consumes recipe ingredients        |
| Direct-sale  | Deducts the stocked product itself |

Example:

**Burger**

Customer orders one burger.

The system consumes:

* Bun
* Beef
* Tomatoes
* Lettuce
* Other defined ingredients

**Bottled Water**

Customer buys one bottle.

The system deducts:

* 1 bottled water

---

# 7.31 Inventory and Waste

Inventory management must work together with Waste Management.

When stock is:

* Spoiled
* Damaged
* Expired
* Dropped
* Otherwise unusable

the quantity should be recorded as waste or through the appropriate inventory process.

The system should retain:

* Item
* Quantity
* Batch where applicable
* Reason
* Date
* User
* Related information

This makes inventory losses visible instead of simply reducing stock.

---

# 7.32 Inventory Traceability

The system should make it possible to trace inventory changes.

For a particular inventory item, staff should be able to determine:

* When it was received
* How much was received
* Which supplier supplied it
* Which batch it belongs to
* When it expires
* How much was consumed
* Which order or production process consumed it
* How much was wasted
* Whether stock was adjusted
* Who performed the action

This is particularly important for perishable ingredients.

---

# 7.33 Inventory History

Each inventory item should have a history of stock movements.

Example:

**Tomatoes**

| Date  | Movement   | Quantity | Balance |
| ----- | ---------- | -------: | ------: |
| Oct 1 | Receipt    |   +10 kg |   10 kg |
| Oct 2 | Receipt    |   +15 kg |   25 kg |
| Oct 3 | Production |    -4 kg |   21 kg |
| Oct 4 | Production |    -3 kg |   18 kg |
| Oct 5 | Waste      |    -1 kg |   17 kg |

The history provides an explanation for the current stock.

---

# 7.34 Inventory Search and Filtering

Authorized staff should be able to search and filter inventory.

Possible filters include:

* Item name
* Category
* Status
* Low stock
* Batch
* Expiry status
* Supplier
* Date received
* Stock movement type

This allows staff to quickly locate relevant inventory information.

---

# 7.35 Inventory Dashboard Information

The inventory dashboard may display:

* Total inventory items
* Low-stock items
* Out-of-stock items
* Expiring items
* Expired items
* Recent stock receipts
* Recent consumption
* Recent waste
* Recent adjustments
* Inventory movement trends

The dashboard should provide useful operational information to authorized staff.

---

# 7.36 Inventory Permissions

Inventory operations must follow role-based permissions.

Example permissions include:

```text
inventory.view
inventory.create
inventory.update
inventory.receive
inventory.adjust
inventory.consume
inventory.view_movements
inventory.view_history
inventory.manage_stock_levels
inventory.manage_batches
inventory.process_expiry
```

The exact permissions assigned to each role are defined in the User Roles & Permissions document.

---

# 7.37 Inventory and Audit Logging

Important inventory actions should be recorded in the audit log.

Examples include:

* Creating an inventory item
* Updating an inventory item
* Receiving stock
* Adjusting stock
* Changing reorder levels
* Blocking inventory
* Processing expired stock
* Recording significant stock consumption

The audit record should identify:

* User
* Action
* Date and time
* Affected record
* Relevant details

---

# 7.38 Inventory Data Model

The inventory module will conceptually contain entities such as:

### InventoryItem

Represents the item being stocked.

Possible fields:

```text
id
name
category_id
description
base_unit
reorder_level
maximum_stock_level
track_batch
track_expiry
status
created_at
updated_at
```

### StockMovement

Represents a change in inventory.

Possible fields:

```text
id
inventory_item_id
batch_id
movement_type
quantity
unit
reference_type
reference_id
reason
performed_by
created_at
```

### StockAdjustment

Represents an authorized inventory correction.

Possible fields:

```text
id
inventory_item_id
quantity_before
quantity_after
difference
reason
performed_by
approved_by
created_at
```

Batch-related information is handled in greater detail in **Document 08 — Batch & Expiry Management**.

---

# 7.39 Core Inventory Relationships

Conceptually:

```text
InventoryItem
      |
      | 1
      |
      | N
StockMovement
      |
      | N
      |
     Batch
```

Inventory also connects to other modules:

```text
InventoryItem
      |
      +---- RecipeIngredient
      |
      +---- StockMovement
      |
      +---- Purchase
      |
      +---- Waste
      |
      +---- Batch
      |
      +---- Product
```

The final database relationships will be defined in **Document 16 — Database Design** and visualized in **Document 17 — ERD**.

---

# 7.40 Inventory Business Rules

The following rules apply to inventory management:

1. Every inventory item must have a unique identifier.
2. Every inventory item must have a name.
3. Every inventory item must have a defined base unit.
4. Inventory categories should be defined for easier organization.
5. Stock quantities must use compatible units.
6. Stock increases must be recorded as inventory movements.
7. Stock decreases must be recorded as inventory movements.
8. Inventory quantities must not be changed silently.
9. Every stock adjustment must have a reason.
10. Expired stock must not count as usable stock.
11. Expired stock must not be consumed in production.
12. Batch-tracked items must maintain batch information.
13. Applicable perishable items should use FEFO consumption.
14. Ingredient consumption must be connected to the appropriate production/order process.
15. Shared ingredients must use the same inventory item across recipes.
16. Low-stock conditions should be determined from usable stock where applicable.
17. Direct-sale stocked products should reduce their own inventory when sold.
18. Recipe-based products should consume their defined ingredients.
19. Waste must be recorded rather than silently removing inventory.
20. Important inventory operations must be auditable.
21. Historical stock movements must not be deleted simply to correct the current balance.
22. Deactivated inventory items should remain available for historical records.
23. Unauthorized users must not perform restricted inventory operations.
24. Physical stock differences should be recorded through adjustments.
25. Inventory history must remain traceable.
26. Inventory records must support accurate reporting.

---

# 7.41 Example — Tomato Inventory

Assume the cafe has:

| Batch | Quantity | Expiry |
| ----- | -------: | ------ |
| A     |     5 kg | Oct 10 |
| B     |     8 kg | Oct 13 |
| C     |    10 kg | Oct 17 |

Total physical stock:

> 23 kg

Usable stock:

> 23 kg, assuming all batches are still valid

A customer order requires:

> 6 kg

The system applies FEFO:

```text
Batch A → 5 kg
Batch B → 1 kg
```

Remaining stock:

```text
Batch A → 0 kg
Batch B → 7 kg
Batch C → 10 kg
```

Total remaining stock:

> 17 kg

---

# 7.42 Example — Expired Tomato Stock

Suppose Batch A has expired.

```text
Batch A → 5 kg → Expired
Batch B → 8 kg → Valid
Batch C → 10 kg → Valid
```

Total physical stock:

> 23 kg

Usable stock:

> 18 kg

If an order requires:

> 19 kg

the system must report insufficient usable tomato stock.

The expired 5 kg cannot be used to satisfy the requirement.

---

# 7.43 Example — Milk

Suppose the cafe receives:

> 20 L of milk

The stock is recorded as:

```text
Milk
Quantity: 20 L
```

If a cappuccino recipe requires:

> 250 ml milk

and 10 cappuccinos are produced:

```text
250 ml × 10
= 2,500 ml
= 2.5 L
```

Remaining milk:

```text
20 L - 2.5 L
= 17.5 L
```

If the milk is batch-tracked, the consumption must also be linked to the appropriate valid batch.

---

# 7.44 Example — Flour

Suppose:

> 25 kg wheat flour

is received.

A recipe requires:

> 500 g flour per production unit.

For 20 units:

```text
500 g × 20
= 10,000 g
= 10 kg
```

Remaining flour:

> 15 kg

The stock movement should record the 10 kg consumption.

---

# 7.45 Example — Eggs

Suppose the cafe has:

> 100 eggs

A pancake recipe requires:

> 2 eggs per production unit.

For 20 production units:

```text
2 × 20 = 40 eggs
```

Remaining stock:

> 60 eggs

Because eggs are counted individually, the base unit can be **piece**.

---

# 7.46 Example — Complete Inventory Flow

A typical inventory process is:

```text
Supplier Delivery
       ↓
Stock Receiving
       ↓
Inventory Item
       ↓
Batch Created (if required)
       ↓
Stock Available
       ↓
Customer Order / Production
       ↓
Inventory Availability Check
       ↓
Select Valid Stock
       ↓
FEFO Batch Selection
       ↓
Ingredient Consumption
       ↓
Stock Movement Recorded
       ↓
Inventory Balance Updated
```

For expired or unusable stock:

```text
Inventory
    ↓
Expiry / Damage / Spoilage
    ↓
Stock Identified as Unusable
    ↓
Waste / Expiry Processing
    ↓
Stock Movement Recorded
    ↓
Usable Stock Updated
```

---

# 7.47 Relationship with Other Modules

## Products & Recipes

Recipes determine which inventory items are consumed when products are produced.

```text
Product
   ↓
Recipe
   ↓
RecipeIngredient
   ↓
InventoryItem
```

## Batch & Expiry Management

Batch management determines:

* Which stock belongs to which batch
* Batch quantities
* Expiry dates
* Valid/expired status
* FEFO selection

## POS & Order Management

Customer orders can trigger:

* Ingredient availability checks
* Recipe scaling
* Ingredient consumption
* Direct-sale stock deduction

## Purchases & Suppliers

Purchases increase inventory when goods are received.

## Waste Management

Waste records explain inventory lost through:

* Expiry
* Spoilage
* Damage
* Other waste events

## Reports & Dashboard

Inventory information contributes to:

* Stock reports
* Low-stock reports
* Expiry reports
* Consumption reports
* Waste reports
* Inventory movement reports

## Audit Logging

Important inventory actions are recorded for accountability and traceability.

---

# 7.48 Inventory Module Summary

The Board’s Cafe inventory module provides a controlled way to manage the cafe's physical stock.

It ensures that:

* Ingredients are properly recorded.
* Vegetables such as tomatoes are treated as real inventory items.
* The same ingredient can be shared across multiple recipes.
* Stock quantities remain traceable.
* Purchases increase inventory.
* Production consumes ingredients.
* Direct-sale products reduce their own stock.
* Expired inventory is excluded from usable stock.
* Perishable batches can be consumed using FEFO.
* Waste and adjustments are recorded.
* Low-stock conditions can be identified.
* Inventory changes can be audited.
* Historical inventory information remains available.

The inventory module therefore provides the foundation needed for reliable stock control, recipe production, expiry management, waste reduction, and cafe operations.
