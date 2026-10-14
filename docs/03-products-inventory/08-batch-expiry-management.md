# Board’s Cafe Management System

# 08 — Batch & Expiry Management

## 8.1 Introduction

Batch and expiry management is a critical part of the Board’s Cafe Management System.

Board’s Cafe uses different types of inventory, including fresh vegetables, fruits, dairy products, meat, eggs, flour, beverages, and other ingredients. Many of these items have limited shelf lives and can become unusable after their expiry date.

The system must therefore track stock at the **batch level**, rather than only maintaining one total quantity for an inventory item.

For example, the cafe may have:

```text
Milk

Batch M001
20 L
Received: 5 Oct
Expires: 10 Oct

Batch M002
30 L
Received: 8 Oct
Expires: 25 Oct
```

Although both batches are milk, they must remain separate because they have different receiving dates, quantities, and expiry dates.

This module works together with:

* Products & Recipes
* Inventory Management
* Purchases & Suppliers
* POS & Order Management
* Waste Management
* Notifications & Alerts
* Reports & Dashboard
* Audit Logging

---

# 8.2 Purpose

The purpose of this module is to help Board’s Cafe:

1. Track inventory batches.
2. Record expiry dates.
3. Identify stock approaching expiry.
4. Prevent expired stock from being used.
5. Support FEFO consumption.
6. Reduce avoidable food waste.
7. Provide expiry notifications.
8. Track expired stock.
9. Support proper disposal of expired stock.
10. Maintain traceability of stock from receipt to consumption or disposal.

---

# 8.3 Why Batch-Level Tracking Is Required

Tracking only the total quantity of an inventory item is not enough.

Incorrect model:

```text
Milk = 50 L
```

This does not tell staff:

* When the milk was received.
* Which supplier provided it.
* Which batch it belongs to.
* Which quantity expires first.
* Which stock should be consumed first.

The correct model is:

```text
Milk
│
├── Batch M001
│   ├── 20 L
│   └── Expires: 10 Oct
│
└── Batch M002
    ├── 30 L
    └── Expires: 25 Oct
```

This allows the system to manage each physical batch independently.

---

# 8.4 Inventory Items That May Require Expiry Tracking

Expiry tracking should be configurable per inventory item.

Examples of commonly perishable items include:

### Vegetables

* Tomatoes
* Onions
* Lettuce
* Cabbage
* Carrots
* Potatoes
* Green peppers

### Fruits

* Bananas
* Oranges
* Avocados
* Apples
* Other fresh fruits

### Dairy

* Milk
* Cheese
* Butter
* Cream
* Yoghurt

### Meat and Poultry

* Beef
* Chicken
* Other fresh meat

### Other Perishable Ingredients

* Eggs
* Fresh juice
* Bakery ingredients
* Prepared ingredients

Not every inventory item must necessarily have an expiry date.

For example, some dry goods may have different storage and expiry requirements.

Therefore, the system should allow expiry tracking to be enabled where required.

---

# 8.5 Batch Concept

A **batch** represents a quantity of an inventory item received or created under the same batch information.

A batch may contain:

* Batch ID
* Inventory item
* Batch number
* Quantity received
* Remaining quantity
* Unit
* Date received
* Expiry date
* Supplier
* Purchase reference
* Unit cost
* Status
* Created date
* Created by

Example:

```text
Inventory Item:
Tomatoes

Batch:
TOM-2026-001

Quantity Received:
10 kg

Remaining:
6.5 kg

Received:
5 October 2026

Expiry:
10 October 2026
```

---

# 8.6 Batch Number

Where suppliers provide a batch or lot number, the system should store it.

Example:

```text
Batch Number:
MILK-24091
```

If a supplier does not provide a batch number, the system may generate an internal batch identifier according to Board’s Cafe's operational rules.

The batch identifier should allow staff to distinguish one batch from another.

---

# 8.7 Batch Quantity

Each batch should maintain:

* Original quantity
* Current remaining quantity

Example:

```text
Original Quantity:
20 L

Consumed:
7 L

Remaining:
13 L
```

The system should not lose the original quantity when stock is consumed.

This allows historical reporting and traceability.

---

# 8.8 Batch Status

A batch may have different statuses.

Possible statuses include:

```text
AVAILABLE
RESERVED
LOW
EXPIRING_SOON
EXPIRED
BLOCKED
DAMAGED
SPOILED
DEPLETED
DISPOSED
```

The exact status model can be refined during database design.

A batch's status should reflect its current operational condition.

---

# 8.9 Expiry Date

An expiry date defines the date after which the relevant stock should not normally be used.

Example:

```text
Milk Batch M001
Expiry Date: 10 October 2026
```

The system should compare the batch expiry date with the current date/time according to Board’s Cafe's defined expiry rules.

Once the expiry condition is reached, the stock should no longer be considered usable.

---

# 8.10 Expiry Date vs Best-Before Date

The system should distinguish between different types of date information where necessary.

Possible date types include:

* Expiry date
* Best-before date
* Production date
* Received date

For the initial system, the most important date for preventing unsafe use is the **expiry date**.

Where Board’s Cafe requires additional date types, they can be stored separately.

---

# 8.11 Expiry Tracking Rule

For an item configured to track expiry:

```text
Batch
   ↓
Expiry Date
   ↓
System Monitors Date
   ↓
Expiry Status
```

Example:

```text
Today: 7 Oct

Milk Batch M001
Expiry: 10 Oct

Status:
EXPIRING_SOON
```

If today becomes 11 Oct:

```text
Milk Batch M001
Expiry: 10 Oct

Status:
EXPIRED
```

---

# 8.12 Expiry Warning Period

Board’s Cafe should define an expiry-warning period for applicable inventory.

For example:

```text
Expiry Warning Period = 3 days
```

If today is:

> 7 October

and a batch expires:

> 10 October

the system can classify it as:

> Expiring Soon

The warning period should be configurable rather than permanently hard-coded.

Different inventory categories may eventually require different warning periods.

---

# 8.13 Expiry Status Calculation

Conceptually:

```text
If current date < expiry date
    → VALID

If expiry date is within warning period
    → EXPIRING_SOON

If current date >= expiry date
    → EXPIRED
```

The exact boundary should be defined consistently during implementation.

---

# 8.14 Expiring-Soon Stock

The system should provide staff with a list of inventory batches that are approaching expiry.

Example:

```text
EXPIRING SOON

Milk
Batch M001
Remaining: 8 L
Expires: 10 Oct
Days Remaining: 2

Tomatoes
Batch T002
Remaining: 4 kg
Expires: 11 Oct
Days Remaining: 3
```

This gives staff time to prioritize the stock.

---

# 8.15 Expired Stock

Once a batch is expired, it must not be treated as usable stock.

Example:

```text
Tomatoes

Batch T001
Quantity: 5 kg
Expiry: 6 Oct

Today: 8 Oct
```

The system should classify:

```text
Status = EXPIRED
Usable Quantity = 0 kg
```

The physical quantity may still exist until staff process it, but it must not be available for normal production or sale.

---

# 8.16 Physical Stock vs Usable Stock

The system should distinguish between physical stock and usable stock.

Example:

```text
Tomatoes

Batch A = 5 kg → Expired
Batch B = 8 kg → Valid
Batch C = 10 kg → Valid
```

Physical stock:

```text
5 + 8 + 10 = 23 kg
```

Usable stock:

```text
8 + 10 = 18 kg
```

Therefore:

```text
Physical Stock = 23 kg
Usable Stock = 18 kg
```

This distinction is important for accurate inventory reporting.

---

# 8.17 Expired Stock Must Not Be Used

The system must prevent expired batches from being selected for:

* Production
* Recipe consumption
* Direct sale
* Stock reservation

For example:

```text
Required Tomatoes:
3 kg

Batch A:
5 kg
Expired

Batch B:
2 kg
Valid
```

The system must not say:

```text
Available = 7 kg
```

for production purposes.

Instead:

```text
Usable = 2 kg
Required = 3 kg

Result:
Insufficient usable stock
```

---

# 8.18 FEFO — First Expire, First Out

Board’s Cafe should use **FEFO** for applicable perishable inventory.

FEFO means:

> The batch that expires first should normally be consumed first.

Example:

```text
Tomatoes

Batch A → 5 kg → expires 10 Oct
Batch B → 8 kg → expires 13 Oct
Batch C → 10 kg → expires 17 Oct
```

If production requires:

> 6 kg

the system should select:

```text
Batch A → 5 kg
Batch B → 1 kg
```

Remaining:

```text
Batch A → 0 kg
Batch B → 7 kg
Batch C → 10 kg
```

---

# 8.19 FEFO vs FIFO

The system should prioritize **FEFO** rather than relying only on FIFO.

FIFO means:

> First In, First Out

FEFO means:

> First Expire, First Out

For perishable cafe ingredients, expiry date is more important than simply the receiving date.

Example:

```text
Batch A
Received: 1 Oct
Expires: 20 Oct

Batch B
Received: 5 Oct
Expires: 10 Oct
```

FIFO would choose Batch A first.

FEFO would choose Batch B first.

For expiry reduction, FEFO is the preferred approach for applicable items.

---

# 8.20 Batch Consumption

When inventory is consumed, the system should reduce the relevant batch quantity.

Example:

```text
Batch M001
Original: 20 L
Current: 20 L
```

Production consumes:

> 3 L

The result is:

```text
Batch M001
Remaining: 17 L
```

A stock movement should also be created to record the consumption.

---

# 8.21 Consumption Across Multiple Batches

If one batch does not contain enough stock, the system can consume from the next eligible batch.

Example:

```text
Milk

Batch M001 → 2 L → expires 10 Oct
Batch M002 → 5 L → expires 15 Oct
```

Required:

> 4 L

The system consumes:

```text
M001 → 2 L
M002 → 2 L
```

Remaining:

```text
M001 → 0 L
M002 → 3 L
```

This follows FEFO.

---

# 8.22 Batch Reservation

Where the order workflow supports inventory reservation, stock may be reserved before actual consumption.

Example:

```text
Milk Batch M001
Available: 10 L

Order requires:
3 L

Reserved:
3 L

Remaining freely available:
7 L
```

Reserved stock should not be counted as freely available to another production process.

The final inventory consumption should occur according to the order and production workflow.

---

# 8.23 Batch Traceability

The system should be able to trace a batch throughout its lifecycle.

For example:

```text
Supplier
   ↓
Purchase
   ↓
Goods Received
   ↓
Batch Created
   ↓
Stored in Inventory
   ↓
Reserved
   ↓
Consumed in Production
   ↓
Order
```

Or:

```text
Supplier
   ↓
Batch
   ↓
Expiry
   ↓
Expired
   ↓
Waste
```

This allows staff and management to understand what happened to a particular batch.

---

# 8.24 Batch-to-Order Traceability

For production-based products, the system should make it possible to identify which batch was consumed for an order.

Example:

```text
Order #1052
2 × Chicken Burger
```

Ingredient consumption:

```text
Tomatoes
Batch T001 → 100 g

Chicken
Batch C003 → 300 g

Lettuce
Batch L002 → 40 g
```

This creates a connection between:

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

# 8.25 Receiving and Batch Creation

When stock is received:

```text
Purchase
   ↓
Goods Received
   ↓
Inventory Item
   ↓
Batch Created
   ↓
Quantity Added
   ↓
Expiry Recorded
```

For example:

```text
Supplier:
ABC Foods

Item:
Milk

Quantity:
20 L

Batch:
M001

Expiry:
10 Oct 2026
```

The system creates the batch and adds its quantity to inventory.

---

# 8.26 Multiple Receipts of the Same Item

The same inventory item can be received many times.

Example:

```text
Milk

Receipt 1:
20 L
Batch M001
Expiry 10 Oct

Receipt 2:
30 L
Batch M002
Expiry 25 Oct

Receipt 3:
25 L
Batch M003
Expiry 5 Nov
```

These must remain separate batches.

The system can still display:

```text
Milk
Total Physical Stock = 75 L
Usable Stock = 75 L
```

while preserving the individual batch records.

---

# 8.27 Partial Batch Consumption

A batch does not have to be completely consumed at once.

Example:

```text
Tomato Batch T001
Received: 10 kg
```

Production 1:

```text
Consumed: 2 kg
Remaining: 8 kg
```

Production 2:

```text
Consumed: 3 kg
Remaining: 5 kg
```

Production 3:

```text
Consumed: 1 kg
Remaining: 4 kg
```

The batch remains active while usable quantity remains.

---

# 8.28 Depleted Batch

When the remaining quantity reaches zero:

```text
Original:
10 kg

Consumed:
10 kg

Remaining:
0 kg
```

the batch should be marked:

```text
DEPLETED
```

It should remain in history for traceability.

It should not be physically deleted.

---

# 8.29 Expired Batch Lifecycle

A typical lifecycle is:

```text
RECEIVED
   ↓
AVAILABLE
   ↓
EXPIRING_SOON
   ↓
EXPIRED
   ↓
DISPOSED
```

However, not every batch will reach every state.

For example, a batch may become:

```text
RECEIVED
   ↓
AVAILABLE
   ↓
DEPLETED
```

before its expiry date.

---

# 8.30 Damaged or Spoiled Batch

A batch may become unusable before its expiry date.

Example:

```text
Milk
Expiry: 20 Oct

Storage problem occurs
Milk becomes spoiled on 12 Oct
```

The stock must not remain available simply because its printed expiry date has not been reached.

The system should allow authorized staff to mark the affected quantity as:

```text
SPOILED
```

or another appropriate unusable status.

The quantity should then be processed through the waste/inventory adjustment workflow.

---

# 8.31 Partial Batch Waste

Only part of a batch may become unusable.

Example:

```text
Milk Batch M001

Original: 20 L
Remaining: 12 L

Spoiled: 4 L
Usable: 8 L
```

The system should record:

```text
Waste:
4 L
```

while keeping:

```text
Usable:
8 L
```

The entire batch should not automatically be discarded unless the business determines that the whole batch is unusable.

---

# 8.32 Expiry Alerts

The system should generate alerts for important expiry conditions.

Possible alerts:

### Expiring Soon

```text
⚠ Expiring Soon

Milk
Batch M001
8 L remaining
Expires in 2 days
```

### Critical Expiry

```text
⚠ Critical Expiry

Tomatoes
Batch T002
4 kg remaining
Expires tomorrow
```

### Expired

```text
❌ Expired Stock

Milk
Batch M001
5 L remaining
Expired today
```

The notification rules should be configurable.

---

# 8.33 Who Receives Expiry Alerts

Expiry alerts should be sent or displayed to authorized staff based on their responsibilities.

Potential recipients include:

* Inventory staff
* Storekeeper
* Kitchen supervisor
* Manager
* Administrator

The exact recipients should be controlled by permissions and Board’s Cafe's operational policy.

---

# 8.34 Expiry Dashboard

The inventory dashboard should provide an expiry section.

Example:

```text
EXPIRY OVERVIEW

Expiring Today:        3
Expiring in 3 Days:    7
Expiring in 7 Days:   15
Expired:               4
```

Staff should be able to open the relevant list and see the affected batches.

---

# 8.35 Expiry List

The system should provide an expiry-focused list.

Example:

| Item     | Batch | Remaining | Expiry | Status        |
| -------- | ----- | --------: | ------ | ------------- |
| Milk     | M001  |       8 L | 10 Oct | Expiring Soon |
| Tomatoes | T002  |      4 kg | 11 Oct | Expiring Soon |
| Chicken  | C004  |      2 kg | 8 Oct  | Expired       |
| Lettuce  | L001  |      3 kg | 14 Oct | Valid         |

The list should support filtering and sorting.

---

# 8.36 Expiry Sorting

Staff should be able to sort batches by:

* Earliest expiry
* Latest expiry
* Item
* Category
* Quantity
* Status

The default operational view should prioritize batches with the earliest expiry.

---

# 8.37 Expired Stock Processing

When stock becomes expired, the system should not automatically delete it.

Instead:

```text
Batch
   ↓
EXPIRED
   ↓
Staff Review
   ↓
Waste / Disposal Record
   ↓
Stock Movement
   ↓
Batch Quantity Updated
```

This preserves an audit trail.

---

# 8.38 Expired Stock Disposal

Authorized staff should record the disposal of expired stock.

Example:

```text
Item:
Milk

Batch:
M001

Expired Quantity:
5 L

Reason:
Expired

Action:
Disposed

Performed By:
Authorized Staff

Date:
11 Oct 2026
```

The system should then remove the quantity from usable inventory while preserving the historical record.

---

# 8.39 Expiry and Waste Relationship

Expired stock should be connected to the waste-management module.

Example:

```text
Batch
   ↓
Expires
   ↓
Expired Stock
   ↓
Waste Record
   ↓
Waste Reason = EXPIRY
```

This allows management to report:

> How much inventory was lost because of expiry?

---

# 8.40 Expiry Cost Calculation

Where inventory cost information is available, the system should estimate the value of expired stock.

Example:

```text
Milk

Expired Quantity:
5 L

Cost:
1,200 RWF/L
```

Estimated expired value:

```text
5 × 1,200
= 6,000 RWF
```

This information can be used in waste and management reports.

---

# 8.41 Expiry Reports

The system should support reports such as:

* Expiring stock
* Expired stock
* Expired stock by item
* Expired stock by category
* Expired stock by batch
* Expired stock by date
* Expired stock value
* Waste caused by expiry
* Most frequently expired ingredients

Example:

```text
October Expiry Report

Milk:
12 L expired

Tomatoes:
8 kg expired

Lettuce:
4 kg expired

Total Estimated Loss:
XX RWF
```

---

# 8.42 Identifying Frequently Expired Items

Management should be able to identify ingredients that repeatedly expire.

Example:

```text
Most Expired Ingredients

1. Tomatoes
2. Lettuce
3. Milk
4. Fresh Juice Ingredients
```

This information can support better purchasing decisions.

For example, management may decide to:

* Purchase smaller quantities.
* Purchase more frequently.
* Change suppliers.
* Adjust reorder levels.
* Promote products using the ingredient.
* Improve storage.
* Review recipe usage.

---

# 8.43 Expiry and Customer Orders

Customer orders can help reduce expiry-related waste.

Suppose:

```text
Tomatoes
4 kg remaining
Expires tomorrow
```

The system can show the expiring stock to authorized staff.

Staff can then prioritize valid use of the ingredient in normal production where appropriate.

The system must **not** encourage unnecessary production merely to avoid expiry. Production should remain based on legitimate customer demand and approved business processes.

---

# 8.44 Expiry and Recipe Production

When production is triggered by a customer order:

```text
Customer Order
      ↓
Recipe
      ↓
Required Ingredients
      ↓
Check Usable Batches
      ↓
FEFO
      ↓
Consume Ingredients
```

Expired batches are excluded.

This connects expiry management directly with production.

---

# 8.45 Expiry and Direct-Sale Products

Direct-sale products may also require batch and expiry tracking.

Example:

```text
Bottled Juice

Batch J001
20 bottles
Expiry: 15 Oct

Batch J002
30 bottles
Expiry: 30 Oct
```

When customers purchase the juice, the system should select the appropriate valid batch according to the configured stock-rotation rules.

---

# 8.46 Manual Override

The system should not allow ordinary staff to bypass expiry controls without authorization.

If an exceptional business process requires an override, it should require:

* Appropriate permission
* Reason
* User identification
* Date/time
* Audit record

By default:

```text
Expired Stock
      ↓
Cannot be consumed normally
```

This protects inventory integrity and operational safety.

---

# 8.47 Expiry Search and Filtering

Authorized users should be able to search expiry records by:

* Inventory item
* Category
* Batch number
* Supplier
* Expiry date
* Expiry status
* Date received
* Location, if locations are supported
* Quantity remaining

---

# 8.48 Expiry Calendar

A future UI may provide an expiry calendar.

Example:

```text
October

10 ─ Milk M001
11 ─ Tomatoes T002
12 ─ Chicken C004
14 ─ Lettuce L001
17 ─ Milk M003
```

This gives staff a simple overview of upcoming expiry dates.

---

# 8.49 Batch Traceability Example

Consider:

```text
Supplier:
Fresh Foods Ltd

Item:
Tomatoes

Batch:
TOM-001

Received:
5 Oct

Quantity:
10 kg

Expiry:
10 Oct
```

Production:

```text
Order #1005
2 Burgers

Consumed:
100 g
```

Remaining:

```text
9.9 kg
```

Later:

```text
Order #1008
4 Salads

Consumed:
400 g
```

Remaining:

```text
9.5 kg
```

If the remaining 9.5 kg expires:

```text
Batch TOM-001
Expired Quantity:
9.5 kg
```

Waste record:

```text
Reason:
EXPIRY
```

The system can therefore trace:

```text
Supplier
 ↓
Batch
 ↓
Orders
 ↓
Consumption
 ↓
Remaining Stock
 ↓
Expiry
 ↓
Waste
```

---

# 8.50 Batch Data Model

The conceptual batch entity may contain:

```text
Batch
-----
id
inventory_item_id
batch_number
quantity_received
quantity_remaining
unit
received_date
expiry_date
status
supplier_id
purchase_reference
unit_cost
created_by
created_at
updated_at
```

The exact fields and relationships will be finalized in:

**16 — Database Design**

and:

**17 — ERD**

---

# 8.51 Batch Relationships

Conceptually:

```text
Inventory Item
      │
      │ 1
      │
      │ *
    Batch
      │
      ├──── Stock Movement
      │
      ├──── Waste Record
      │
      └──── Ingredient Consumption
```

A single inventory item may therefore have many batches.

```text
Tomatoes
   │
   ├── Batch T001
   ├── Batch T002
   ├── Batch T003
   └── Batch T004
```

---

# 8.52 Batch and Stock Movement

Every quantity change affecting a batch should be traceable through stock movements where applicable.

Example:

```text
Batch T001
Original = 10 kg
```

Movement 1:

```text
RECEIPT
+10 kg
```

Movement 2:

```text
CONSUMPTION
-2 kg
```

Movement 3:

```text
CONSUMPTION
-1 kg
```

Movement 4:

```text
WASTE
-2 kg
```

Remaining:

```text
5 kg
```

This provides a complete movement history.

---

# 8.53 Batch and Audit Logging

Important batch actions should be audited.

Examples:

* Creating a batch
* Editing batch information
* Changing batch status
* Processing expired stock
* Recording expiry waste
* Adjusting batch quantity
* Overriding a blocked/expired condition where authorized

The audit record should identify:

* User
* Action
* Date/time
* Affected batch
* Relevant details
* Reason where applicable

---

# 8.54 Business Rules

The Batch & Expiry Management module shall follow these rules:

1. Batch-tracked inventory must maintain separate batch records.
2. Each batch must belong to an inventory item.
3. Batch quantities must be non-negative.
4. A batch should retain its original received quantity.
5. Remaining quantity must be traceable.
6. Expiry dates must be stored for items configured for expiry tracking.
7. Expired stock must not be considered usable stock.
8. Expired stock must not be consumed through normal production.
9. Expired stock must not be selected for direct sale.
10. FEFO should be used for applicable perishable stock.
11. Staff should be warned before stock reaches expiry.
12. Expiry-warning periods should be configurable.
13. Expired stock must remain visible in historical records.
14. Expired stock should be processed through the appropriate waste/disposal workflow.
15. Spoiled or damaged stock may become unusable before its expiry date.
16. Unusable stock must not be treated as available stock.
17. Partial quantities of a batch may be consumed.
18. Partial quantities of a batch may be wasted.
19. Depleted batches should remain in historical records.
20. Batch quantities must be traceable to stock movements.
21. Where applicable, ingredient consumption should identify the batch consumed.
22. Important batch operations must be audited.
23. Unauthorized users must not bypass expiry controls.
24. Historical batch records should not be destructively deleted.
25. Expiry information should support reporting and management decisions.
26. The system should support both physical stock and usable stock views.
27. Multiple batches of the same inventory item must be supported.
28. Batch expiry information should be considered when checking ingredient availability.
29. Expiry processing should preserve the reason and responsible user.
30. The system should support identifying ingredients that repeatedly expire.

---

# 8.55 Complete Expiry Management Workflow

The complete process is:

```text
Supplier
   ↓
Purchase
   ↓
Stock Received
   ↓
Batch Created
   ↓
Expiry Date Recorded
   ↓
Inventory Available
   ↓
System Monitors Expiry
   ↓
┌─────────────────────────────┐
│                             │
│  Valid                      │
│     ↓                       │
│  Available for Use          │
│                             │
└─────────────────────────────┘
             │
             ▼
       Expiring Soon
             │
             ▼
       Alert Staff
             │
             ▼
      FEFO Prioritization
             │
             ▼
        Consumption
```

If the stock is not consumed:

```text
Expiring Soon
      ↓
Expiry Date Reached
      ↓
EXPIRED
      ↓
Exclude From Usable Stock
      ↓
Staff Review
      ↓
Waste / Disposal
      ↓
Record Waste
      ↓
Update Inventory
```

---

# 8.56 Board’s Cafe Expiry Management Goal

The purpose of expiry management is not simply to tell staff that something has expired.

The system should help staff act **before** expiry happens.

The desired flow is:

```text
Receive Stock
      ↓
Know Expiry Date
      ↓
Monitor Remaining Quantity
      ↓
Warn Staff
      ↓
Prioritize Valid Stock
      ↓
Use Through Normal Customer Demand
      ↓
Reduce Expired Stock
      ↓
Record Any Remaining Waste
```

This supports Board’s Cafe's goal of reducing avoidable food and inventory losses.

---

# 8.57 Module Summary

Batch & Expiry Management provides the detailed control needed for perishable inventory at Board’s Cafe.

The core relationship is:

```text
Inventory Item
      ↓
Many Batches
      ↓
Expiry Dates
      ↓
Usable / Expired Stock
      ↓
FEFO
      ↓
Production / Sale
      ↓
Consumption
```

For stock that is not used before expiry:

```text
Batch
 ↓
Expired
 ↓
Excluded From Usable Stock
 ↓
Waste / Disposal
 ↓
Recorded Loss
```

This module ensures that Board’s Cafe can answer important questions such as:

* Which ingredients are expiring soon?
* How much milk will expire this week?
* Which tomato batch expires first?
* How much stock has already expired?
* Which ingredients are frequently wasted because of expiry?
* What was the financial value of expired stock?
* Which batch was used for a particular customer order?
* Who processed the expired stock?

Together with Documents 06 and 07, this establishes the foundation:

```text
PRODUCT
   ↓
RECIPE
   ↓
INGREDIENT
   ↓
INVENTORY ITEM
   ↓
BATCH
   ↓
EXPIRY
   ↓
FEFO
   ↓
PRODUCTION / SALE
   ↓
CONSUMPTION
   ↓
WASTE
```

This structure will be carried forward into **09 — POS & Order Management**, where we connect customer orders to kitchen preparation, recipe-based production, ingredient availability, and inventory consumption.
