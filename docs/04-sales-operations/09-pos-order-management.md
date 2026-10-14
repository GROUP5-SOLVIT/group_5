# 09 — POS & Order Management

## 1. Purpose

The Point of Sale (POS) and Order Management module handles the process of creating, managing, processing, and completing customer orders within Board’s Cafe.

The module is intended for **internal staff use**. Staff members use the POS interface to create orders, add products, calculate totals, record payments, and monitor the progress of orders.

The POS module must also work with the product, recipe, inventory, batch, production, payment, waste, and audit modules.

A key requirement is that not every product needs to be produced before it is sold.

Board’s Cafe supports two main product types:

1. **Direct-Sale Products** — products that already exist as stocked items and can be sold directly.
2. **Recipe-Based Products** — products prepared using ingredients according to a recipe, where production may happen after a customer places an order.

For example:

* Bottled water → direct-sale product
* Packaged juice → direct-sale product
* Bread → may be direct-sale or recipe-based depending on how the cafe manages it
* Burger → recipe-based product
* Pizza → recipe-based product
* Fresh juice → recipe-based product

This distinction is important because the inventory transaction is different for each type.

---

# 2. POS Objectives

The POS module should allow authorized staff to:

* Create customer orders
* Add products to an order
* Change product quantities
* Remove products from an order
* Calculate order totals
* Apply approved discounts
* Calculate taxes or other configured charges where applicable
* Check product availability
* Check ingredient availability for recipe-based products
* Reserve stock where required
* Send recipe-based orders for production
* Track order preparation status
* Record payments
* Complete orders
* Cancel orders
* Process approved refunds
* View order history
* Search previous orders
* Print or generate receipts
* Track staff responsible for transactions
* Maintain an audit trail

---

# 3. Product Types in POS

## 3.1 Direct-Sale Products

A direct-sale product is already available as a physical stock item.

Examples:

* Bottled water
* Packaged juice
* Soft drinks
* Packaged snacks
* Pre-packed bread
* Other stocked products

When a customer buys a direct-sale product, the system reduces the stock of that product.

### Example

A customer orders:

* 2 bottled waters

If the cafe has 50 bottles:

```text
Opening stock: 50
Sale:          -2
Remaining:     48
```

The system should create the appropriate stock movement.

---

# 4. Recipe-Based Products

A recipe-based product is prepared using ingredients.

Examples:

* Burger
* Pizza
* Fresh juice
* Sandwich
* Omelette
* Coffee-based drinks
* Other prepared food or drinks

The product itself does not necessarily need to exist as a pre-produced stock item.

Instead, the system uses its recipe to determine which ingredients are required.

### Example

A burger recipe may require:

```text
Burger
├── Bun
├── Beef
├── Tomato
├── Lettuce
├── Onion
├── Cheese
└── Sauce
```

When the customer orders one burger, the system checks whether the required ingredients are available.

If sufficient stock exists, the order can proceed to production.

---

# 5. Production on Order

Board’s Cafe should support **production triggered by a customer order**.

This means the cafe does not have to prepare every recipe-based product in advance.

For example:

```text
Customer orders Burger
        ↓
POS creates order
        ↓
System checks recipe
        ↓
System checks ingredient availability
        ↓
Ingredients are reserved/allocated
        ↓
Kitchen receives production request
        ↓
Burger is prepared
        ↓
Ingredients are consumed
        ↓
Order is completed
```

This helps reduce unnecessary production and food waste.

---

# 6. Order Creation

Authorized POS staff should be able to create a new order.

An order should contain information such as:

* Order ID
* Order number/reference
* Order date and time
* Staff member who created it
* Order status
* Customer information where required
* Order type
* Order items
* Subtotal
* Discount
* Tax/charges where applicable
* Total amount
* Payment status
* Notes
* Created date
* Updated date

---

# 7. Order Types

The system may support different order types depending on the cafe's operations.

Examples include:

* Dine-in
* Takeaway
* Pickup
* Other internally configured order types

The selected order type should be stored with the order.

The system should not assume that all orders are dine-in.

---

# 8. Order Items

Each order can contain one or more order items.

For example:

```text
Order #1052

1 × Chicken Burger
2 × Fresh Juice
1 × Bottled Water
```

Each order item should store information such as:

* Product
* Quantity
* Unit price
* Discount if applicable
* Line total
* Production status where applicable
* Notes/customization where supported

The order item should preserve the price used at the time of sale.

Changing the current product price later should not change historical orders.

---

# 9. Product Availability

Before an item is added to an order or confirmed, the system should determine whether it can be fulfilled.

There are two different availability checks.

## 9.1 Direct-Sale Availability

For direct-sale products:

```text
Available Stock >= Requested Quantity
```

Example:

```text
Bottled Water
Available: 20
Requested: 3

Result: AVAILABLE
```

If only two bottles are available:

```text
Available: 2
Requested: 3

Result: INSUFFICIENT STOCK
```

The system should not allow normal sale of more stock than is available.

---

## 9.2 Recipe-Based Availability

For recipe-based products, the system should check the required ingredients.

Example:

```text
Product: Chicken Burger

Required:
Chicken   → 0.15 kg
Bun       → 1 piece
Tomato    → 0.05 kg
Lettuce   → 0.03 kg
Onion     → 0.02 kg
```

If the customer orders two burgers, the system checks the required quantity for two recipes.

```text
Chicken   → 0.30 kg
Bun       → 2 pieces
Tomato    → 0.10 kg
Lettuce   → 0.06 kg
Onion     → 0.04 kg
```

The system should consider **usable stock**, not simply physical stock.

Expired batches must not be counted as available stock.

---

# 10. Shared Ingredients

The POS system must work correctly when an ingredient is shared across multiple products.

For example, **tomatoes** may be used by:

* Burger
* Sandwich
* Pizza
* Salad

There should be one inventory item for tomatoes.

```text
Inventory Item
    Tomato
       ↓
   ┌───┼────┬────┐
   ↓   ↓    ↓    ↓
Burger Sandwich Pizza Salad
```

The system should not create separate inventory items such as:

```text
Burger Tomato
Pizza Tomato
Sandwich Tomato
```

Instead, all recipes reference the same inventory item.

This allows the system to maintain one accurate stock balance.

---

# 11. Multiple Recipe-Based Items in One Order

A single order may contain several recipe-based products that use the same ingredient.

For example:

```text
Order #1055

2 × Burger
1 × Sandwich
```

Both products may require tomatoes.

The system should calculate the total required tomato quantity before confirming production.

Example:

```text
Burger:
2 × 50g tomato = 100g

Sandwich:
1 × 40g tomato = 40g

Total required:
140g tomato
```

The availability check should therefore consider the **combined requirement**.

This prevents the system from incorrectly confirming each item independently when the combined order cannot actually be produced.

---

# 12. Stock Reservation

Where required, the system may reserve inventory when an order is confirmed.

Reservation helps prevent the same stock from being allocated to multiple orders.

For example:

```text
Tomato usable stock: 2 kg

Order A requires: 0.5 kg
Order B requires: 0.8 kg
```

After reservation:

```text
Physical/usable stock: 2 kg
Reserved:              1.3 kg
Available to reserve:  0.7 kg
```

Reserved stock should not be treated as freely available stock for another order.

The exact point at which stock is reserved should be configurable according to the cafe's workflow.

---

# 13. FEFO and Order Production

For batch-tracked ingredients, the system should follow **FEFO (First Expire, First Out)** when selecting stock for production.

Example:

```text
Tomato Batch A
5 kg
Expires: 10 Oct

Tomato Batch B
8 kg
Expires: 13 Oct

Tomato Batch C
10 kg
Expires: 17 Oct
```

If production requires 6 kg:

```text
Batch A → 5 kg
Batch B → 1 kg
```

The system should record the exact batches used.

This maintains traceability between:

```text
Order
  ↓
Production
  ↓
Ingredient Consumption
  ↓
Batch
```

---

# 14. Order Status

The order should have a controlled lifecycle.

A suggested lifecycle is:

```text
DRAFT
   ↓
CONFIRMED
   ↓
PENDING_PRODUCTION
   ↓
IN_PRODUCTION
   ↓
READY
   ↓
COMPLETED
```

Other possible states include:

```text
CANCELLED
FAILED
REFUNDED
```

Not every order must pass through every status.

For example, a direct-sale order may not require production:

```text
DRAFT
  ↓
CONFIRMED
  ↓
READY
  ↓
COMPLETED
```

A recipe-based order may require:

```text
DRAFT
  ↓
CONFIRMED
  ↓
PENDING_PRODUCTION
  ↓
IN_PRODUCTION
  ↓
READY
  ↓
COMPLETED
```

---

# 15. Order Status Definitions

### DRAFT

The order has been started but has not yet been confirmed.

Staff may still:

* Add items
* Remove items
* Change quantities
* Update notes

### CONFIRMED

The order has been accepted by the POS.

Required availability checks should have passed.

### PENDING_PRODUCTION

The order contains recipe-based products waiting to be prepared.

### IN_PRODUCTION

The kitchen or production staff is preparing the products.

### READY

The order has been prepared and is ready for handover.

### COMPLETED

The order has been fulfilled and the transaction is complete.

### CANCELLED

The order was cancelled before completion.

### REFUNDED

A completed transaction has been refunded according to the cafe's refund rules.

---

# 16. Production Status for Order Items

Order-level status and item-level production status should be treated separately where necessary.

For example:

```text
Order #1060

1 × Bottled Water
1 × Chicken Burger
1 × Fresh Juice
```

The bottled water may be immediately available while the burger and fresh juice are being prepared.

Therefore, individual order items may have statuses such as:

```text
NOT_REQUIRED
PENDING
IN_PRODUCTION
READY
CANCELLED
```

This allows the system to manage mixed orders correctly.

---

# 17. Kitchen / Production Workflow

For recipe-based products, the POS should communicate the required production information to authorized production staff.

A production request should identify:

* Order number
* Product
* Quantity
* Recipe/version used
* Required ingredients
* Special instructions
* Production status
* Staff responsible
* Start time
* Completion time

Example:

```text
Order #1052

2 × Chicken Burger

Status: IN PRODUCTION

Required:
Chicken
Bun
Tomato
Lettuce
Onion
Cheese
Sauce
```

---

# 18. Recipe Version and Historical Orders

Recipes may change over time.

For example:

```text
Old Burger Recipe
150g chicken

New Burger Recipe
160g chicken
```

Historical orders must remain understandable.

The system should therefore preserve the recipe information or recipe version used when production occurred.

A future recipe change should not rewrite historical production records.

---

# 19. Pricing

Each product should have a selling price.

When an order is created, the system should store the actual unit price used for that order item.

Example:

```text
Current Burger Price: 3,500 RWF

Order #1001
Burger: 3,500 RWF
```

If the price later changes:

```text
New Burger Price: 4,000 RWF
```

Order #1001 should still show:

```text
Burger: 3,500 RWF
```

This is important for historical sales reporting.

---

# 20. Discounts

The system may support approved discounts.

A discount may apply to:

* An individual order item
* The entire order

The system should record:

* Discount amount or percentage
* Reason where required
* Staff member who applied it
* Date/time
* Authorization where required

Unauthorized staff should not be able to apply unrestricted discounts.

Discount activity should be included in the audit trail.

---

# 21. Order Total Calculation

The system should calculate the order total consistently.

Conceptually:

```text
Subtotal
    - Discount
    + Tax/Charges
    = Total
```

Example:

```text
Subtotal:      15,000 RWF
Discount:       1,000 RWF
Tax/Charges:        0 RWF
-----------------------
Total:         14,000 RWF
```

The calculation should be performed by the backend rather than trusting totals submitted directly by the POS client.

---

# 22. Payment

An order may have one or more payment records depending on the business requirements.

Payment information may include:

* Payment ID
* Order ID
* Amount
* Payment method
* Payment status
* Transaction/reference number where applicable
* Payment date/time
* Staff member
* Notes

Possible payment methods may include:

* Cash
* Mobile money
* Bank/card payment
* Other configured methods

The exact supported payment methods should be configurable.

---

# 23. Payment Status

Suggested payment statuses:

```text
PENDING
PARTIALLY_PAID
PAID
FAILED
REFUNDED
PARTIALLY_REFUNDED
```

The order's payment status should be derived from its payment records where possible.

Example:

```text
Order Total: 10,000 RWF
Paid:          6,000 RWF

Payment Status:
PARTIALLY_PAID
```

---

# 24. Partial Payments

If the cafe allows partial payments, the system should support multiple payment records for the same order.

Example:

```text
Order Total: 20,000 RWF

Payment 1:
Cash → 10,000 RWF

Payment 2:
Mobile Money → 10,000 RWF
```

Total paid:

```text
20,000 RWF
```

Order status:

```text
PAID
```

---

# 25. Change Calculation

For cash payments, the system should calculate the customer's change.

Example:

```text
Order Total:     7,500 RWF
Cash Received:  10,000 RWF
Change:          2,500 RWF
```

The backend should perform the calculation to prevent incorrect totals.

---

# 26. Receipts

After successful payment, the system should support receipt generation.

A receipt may contain:

* Cafe name
* Order number
* Date/time
* Staff member
* Products
* Quantities
* Unit prices
* Discounts
* Total
* Payment method
* Amount paid
* Change
* Transaction reference where applicable

The system should preserve the transaction record even if the receipt is later printed again.

---

# 27. Order Cancellation

Authorized staff should be able to cancel an order according to its current status.

Cancellation should not simply delete the order from the database.

Instead, the order should be marked as cancelled and the system should record:

* Cancellation reason
* Staff member
* Date/time
* Any affected stock reservations
* Any affected payments
* Any production changes

If stock has already been consumed, the system should not silently restore it.

A proper reversal or adjustment process should be used.

---

# 28. Refunds

Refunds should be controlled and audited.

A refund may occur when:

* A customer returns a product
* An order is cancelled after payment
* An incorrect transaction was completed
* Another approved business reason exists

The system should record:

* Original order
* Refund amount
* Refund reason
* Refund method
* Staff member
* Date/time
* Authorization where required

Refunding an order should not delete the original sale.

---

# 29. Inventory Integration

POS transactions must be connected to inventory.

### Direct-sale product

```text
Customer Order
      ↓
Confirm Order
      ↓
Check Product Stock
      ↓
Sale
      ↓
Stock Decrease
      ↓
Stock Movement
```

### Recipe-based product

```text
Customer Order
      ↓
Check Recipe
      ↓
Check Ingredients
      ↓
Reserve/Allocate Stock
      ↓
Production
      ↓
Ingredient Consumption
      ↓
Stock Movements
      ↓
Order Ready
```

---

# 30. Batch Traceability

Where ingredients are batch-tracked, the system should record which batches were consumed for production.

Example:

```text
Order #1080
   ↓
Production #205
   ↓
Tomato: 100g
   ↓
Batch TOM-20261005-A
```

This allows the cafe to determine which orders were affected by a particular batch.

This is particularly useful when dealing with:

* Expired stock
* Spoiled ingredients
* Damaged batches
* Supplier quality issues
* Food safety investigations

---

# 31. Waste Integration

Waste may occur during production or after an order.

Examples:

* A tomato is spoiled during preparation
* Ingredients are damaged
* Prepared food is rejected
* An order is cancelled after production has started
* Excess food cannot be reused

Waste should be recorded separately through the Waste Management module.

The POS or production process may create a reference to the waste record.

The system should avoid silently changing inventory to hide the loss.

---

# 32. Order Search and History

Authorized staff should be able to search historical orders.

Search/filter options may include:

* Order number
* Date
* Product
* Customer where applicable
* Staff member
* Order status
* Payment status
* Payment method
* Amount
* Order type

Historical order records should remain available according to the system's data-retention policy.

---

# 33. POS Dashboard

The POS interface may provide quick operational information such as:

* New order
* Open orders
* Orders in production
* Ready orders
* Completed orders
* Pending payments
* Today's sales
* Number of orders
* Cancelled orders

The dashboard should only show information the logged-in staff member is authorized to access.

---

# 34. Permissions

Suggested POS permissions include:

```text
pos.view
pos.create_order
pos.update_order
pos.cancel_order
pos.confirm_order
pos.view_orders
pos.view_order_details
pos.process_payment
pos.refund
pos.apply_discount
pos.print_receipt
pos.view_sales
pos.manage_order_status
pos.manage_production_status
```

Not every role should receive all permissions.

For example:

| Permission         | Admin | Manager |       Cashier | Kitchen Staff |
| ------------------ | ----: | ------: | ------------: | ------------: |
| Create order       |     ✓ |       ✓ |             ✓ |            No |
| Update order       |     ✓ |       ✓ |             ✓ |            No |
| Confirm order      |     ✓ |       ✓ |             ✓ |            No |
| Process payment    |     ✓ |       ✓ |             ✓ |            No |
| Apply discount     |     ✓ |       ✓ |    Restricted |            No |
| Cancel order       |     ✓ |       ✓ |    Restricted |            No |
| Refund             |     ✓ |       ✓ | No/Restricted |            No |
| View production    |     ✓ |       ✓ |             ✓ |             ✓ |
| Update production  |     ✓ |       ✓ |            No |             ✓ |
| View sales reports |     ✓ |       ✓ |    Restricted |            No |

The exact permissions should be finalized in the User Roles & Permissions and Security documents.

---

# 35. Audit Logging

Important POS actions should be recorded in the audit log.

Examples include:

* Order created
* Order updated
* Order confirmed
* Order cancelled
* Discount applied
* Payment recorded
* Payment failed
* Refund processed
* Order status changed
* Production started
* Production completed
* Manual price override
* Stock reservation
* Stock consumption
* Receipt reprinted

The audit record should identify:

* User
* Action
* Entity
* Entity ID
* Date/time
* Relevant details
* Previous value where appropriate
* New value where appropriate

---

# 36. Important Business Rules

The POS module should follow these rules:

1. Only authorized staff can access POS functions.
2. Orders must have at least one valid order item before confirmation.
3. Product prices used in completed orders must be preserved.
4. Direct-sale products must have sufficient usable stock.
5. Recipe-based products must have sufficient usable ingredients.
6. Expired inventory must not be considered available for normal production or sale.
7. FEFO should be used for applicable batch-tracked ingredients.
8. Shared ingredients must be consumed from their common inventory item.
9. Multiple products in one order must be checked together when they share ingredients.
10. Stock must not become negative through normal POS operations.
11. Order totals must be calculated and validated by the backend.
12. Discounts must follow permission rules.
13. Payments must be recorded separately from orders.
14. Completed sales must not be deleted.
15. Cancellations and refunds must be recorded rather than hidden.
16. Stock changes must generate appropriate inventory records.
17. Recipe changes must not rewrite historical production records.
18. Batch consumption must be traceable where batch tracking is enabled.
19. Important POS actions must be audited.
20. Unauthorized users must not be able to override stock, expiry, pricing, payment, or refund rules.

---

# 37. Main POS Workflow

The general POS workflow is:

```text
Staff Login
    ↓
Open POS
    ↓
Create Order
    ↓
Select Order Type
    ↓
Add Products
    ↓
Set Quantities
    ↓
Calculate Total
    ↓
Check Availability
    ↓
    ├── Direct-Sale Product
    │       ↓
    │   Check Product Stock
    │
    └── Recipe-Based Product
            ↓
        Check Recipe
            ↓
        Check Ingredients
            ↓
        Check Usable Batches
    ↓
Confirm Order
    ↓
    ├── Direct-Sale
    │       ↓
    │   Deduct Stock
    │
    └── Recipe-Based
            ↓
        Reserve/Allocate Ingredients
            ↓
        Send to Production
            ↓
        Prepare Product
            ↓
        Consume Ingredients
    ↓
Process Payment
    ↓
Generate Receipt
    ↓
Order Ready / Completed
    ↓
Audit Record
```

---

# 38. Example: Direct-Sale Order

A customer purchases:

```text
2 × Bottled Water
1 × Packaged Juice
```

The POS checks:

```text
Bottled Water:
Available = 30
Required  = 2
Result    = Available

Packaged Juice:
Available = 10
Required  = 1
Result    = Available
```

The order is confirmed.

Stock becomes:

```text
Bottled Water:
30 → 28

Packaged Juice:
10 → 9
```

The corresponding stock movements are recorded.

---

# 39. Example: Recipe-Based Order

A customer orders:

```text
2 × Chicken Burger
```

The system retrieves the burger recipe.

Required ingredients:

```text
Chicken:  0.30 kg
Buns:     2 pieces
Tomato:   0.10 kg
Lettuce:  0.06 kg
Onion:    0.04 kg
Cheese:   2 pieces
Sauce:    0.04 L
```

The system checks usable inventory.

If all required ingredients are available:

```text
Order → CONFIRMED
```

The required ingredients are reserved or allocated.

The kitchen receives:

```text
2 × Chicken Burger
```

After preparation:

```text
Ingredients → CONSUMED
Order → READY
```

Payment is then completed according to the cafe's configured workflow.

---

# 40. Example: Mixed Order

A customer orders:

```text
2 × Chicken Burger
1 × Bottled Water
1 × Fresh Juice
```

The system treats each product according to its type.

```text
Chicken Burger
→ Recipe-based
→ Ingredient availability check
→ Production

Bottled Water
→ Direct-sale
→ Product stock check

Fresh Juice
→ Recipe-based
→ Ingredient availability check
→ Production
```

All items remain part of the same customer order.

The order should only be marked fully ready when the required items have reached their appropriate ready state.

---

# 41. Relationship With Other Modules

The POS module connects closely with other Board’s Cafe modules.

```text
Products
   ↓
Recipes
   ↓
Inventory Items
   ↓
Batches
   ↓
POS Orders
   ↓
Production
   ↓
Ingredient Consumption
   ↓
Payments
   ↓
Reports
   ↓
Audit Logs
```

The main relationships are:

```text
Product → Order Item
Product → Recipe
Recipe → Recipe Ingredient
Inventory Item → Batch
Order → Order Item
Order → Payment
Order → Production
Production → Ingredient Consumption
Ingredient Consumption → Batch
Order → Audit Log
```

---

# 42. Data Integrity Requirements

The POS system should maintain consistency between:

* Orders
* Order items
* Products
* Recipes
* Inventory
* Batches
* Production
* Payments
* Waste
* Audit logs

For example, the system should avoid a situation where:

```text
Order says 2 burgers were sold
but
Inventory shows no ingredient consumption
```

or:

```text
Payment says 20,000 RWF was received
but
Order total says 15,000 RWF
```

Such operations should be validated by the backend.

Where multiple records must be updated together, the backend should use appropriate database transaction handling.

---

# 43. POS and Reporting

Completed POS transactions should provide data for reporting.

Reports may include:

* Daily sales
* Weekly sales
* Monthly sales
* Product sales
* Best-selling products
* Sales by staff member
* Sales by order type
* Payment method totals
* Discounts
* Refunds
* Cancelled orders
* Production quantities
* Ingredient consumption
* Food cost analysis where supported

POS should therefore be treated as a source of reliable transaction data rather than simply a screen for taking orders.

---

# 44. Summary

The Board’s Cafe POS module provides the operational link between customer orders and the rest of the cafe management system.

The key distinction is:

```text
DIRECT-SALE PRODUCT
        ↓
Check product stock
        ↓
Sell
        ↓
Reduce product stock
```

while:

```text
RECIPE-BASED PRODUCT
        ↓
Read recipe
        ↓
Check shared ingredients
        ↓
Check usable batches
        ↓
Reserve/allocate
        ↓
Produce on order
        ↓
Consume ingredients
        ↓
Complete sale
```

This design allows Board’s Cafe to support both stocked products and freshly prepared products while maintaining accurate inventory, batch traceability, expiry control, production records, payments, and sales history.

### Core POS Flow

```text
PRODUCT
   ↓
ORDER
   ↓
AVAILABILITY CHECK
   ↓
DIRECT SALE ────────────────┐
                            │
RECIPE-BASED → PRODUCTION ──┤
                            ↓
                       CONSUMPTION
                            ↓
                         PAYMENT
                            ↓
                         RECEIPT
                            ↓
                        COMPLETION
                            ↓
                         REPORTING
                            ↓
                       AUDIT LOG
```
