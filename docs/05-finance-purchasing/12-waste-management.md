# 12 — Waste Management

## 1. Purpose

The Waste Management module manages products and ingredients that are lost, damaged, expired, spoiled, rejected, returned, or otherwise removed from usable stock at Board’s Cafe.

The module provides a controlled way to:

* Record wasted inventory
* Track why stock was wasted
* Track expired products
* Track spoiled ingredients
* Track damaged products
* Track preparation and production waste
* Track overproduction
* Track customer-returned items
* Track supplier-rejected items
* Reduce inventory accurately
* Track the financial impact of waste
* Identify repeated sources of waste
* Support management reporting

Waste records must be connected to inventory and, where applicable, the relevant batch, purchase, order, production activity, or supplier.

---

# 2. Waste Management Objectives

The system should help Board’s Cafe answer questions such as:

* What products are being wasted?
* How much stock is being wasted?
* Why is it being wasted?
* Which batches are expiring?
* Which ingredients are frequently spoiled?
* How much waste comes from production?
* Which products are being overproduced?
* Which supplier deliveries have high rejection rates?
* How much money is being lost through waste?
* Which staff member recorded the waste?
* When did the waste occur?
* Which branch or storage location generated the waste?

---

# 3. What Counts as Waste?

Waste is any inventory that is no longer available for its intended usable purpose and must be removed, reduced, or reclassified.

Examples include:

### Expired Stock

```text id="x9o5hy"
Milk
Expiry: 08 Oct 2026
Today: 09 Oct 2026
```

The milk is no longer usable according to the cafe's expiry rules.

### Spoiled Stock

```text id="a3s9k2"
Tomatoes
Condition:
Spoiled / rotten
```

### Damaged Stock

```text id="2j0w0x"
Glass bottle
Condition:
Broken
```

### Preparation Waste

```text id="7qf3zc"
Vegetable trimming
Peels
Unusable parts
```

### Production Waste

```text id="0r9q6d"
Food prepared incorrectly
Burnt food
Failed production batch
```

### Overproduction

Food prepared for expected demand but not sold or otherwise reusable.

### Customer Return

Food or product returned by a customer and determined to be unsuitable for resale or reuse.

### Supplier Rejection

Goods received from a supplier but rejected because of:

* Damage
* Poor quality
* Incorrect item
* Expiry
* Other quality issues

---

# 4. Waste Categories

The system should support configurable waste categories.

Suggested categories are:

```text
EXPIRY
SPOILAGE
DAMAGE
PREPARATION
PRODUCTION
OVERPRODUCTION
CUSTOMER_RETURN
SUPPLIER_REJECTION
CONTAMINATION
QUALITY_ISSUE
OTHER
```

The categories should be configurable by an authorized administrator.

---

# 5. Waste Sources

The system should identify where the waste originated.

Possible sources include:

```text
INVENTORY
RECEIVING
PRODUCTION
POS_ORDER
CUSTOMER_RETURN
PURCHASE
STORAGE
OTHER
```

For example:

```text id="j7y4u2"
Source:
PRODUCTION

Reason:
Failed production
```

or:

```text id="1d7p6x"
Source:
INVENTORY

Reason:
Expired
```

---

# 6. Waste Record

Each waste event should create a waste record.

A waste record may contain:

| Field              | Description                    |
| ------------------ | ------------------------------ |
| Waste ID           | Unique identifier              |
| Waste Number       | Human-readable reference       |
| Inventory Item     | Item being wasted              |
| Batch              | Related batch where applicable |
| Quantity           | Quantity wasted                |
| Unit               | kg, litre, piece, etc.         |
| Category           | Waste reason/category          |
| Source             | Where waste originated         |
| Reason             | Detailed explanation           |
| Cost               | Estimated/recorded stock cost  |
| Location           | Storage/branch/location        |
| Recorded By        | Staff member                   |
| Approved By        | Approver where required        |
| Date/Time          | When waste was recorded        |
| Related Order      | Optional                       |
| Related Purchase   | Optional                       |
| Related Production | Optional                       |
| Notes              | Additional information         |

---

# 7. Waste Quantity

The quantity wasted must be recorded using the item's configured unit.

Examples:

```text
Milk:
5 litres

Flour:
10 kg

Tomatoes:
3 kg

Eggs:
12 pieces
```

The system should validate that the waste quantity does not exceed the available quantity for the relevant stock/batch unless an authorized adjustment workflow explicitly allows it.

---

# 8. Waste and Inventory

Recording waste must result in an appropriate inventory reduction.

Example:

```text id="g9j0km"
Tomatoes

Before:
20 kg

Waste:
3 kg

After:
17 kg
```

The inventory change should be recorded through a stock movement.

Example:

```text
Stock Movement:
WASTE

Quantity:
-3 kg
```

The system should not simply overwrite the inventory balance.

---

# 9. Waste and Batch Tracking

If an item is batch-tracked, the waste record should identify the affected batch.

Example:

```text
Milk

Batch:
MILK-20261006-A

Available:
20 L

Wasted:
5 L

Remaining:
15 L
```

This makes it possible to determine exactly which batch generated the waste.

---

# 10. Expired Products

Expiry is one of the most important waste categories for Board’s Cafe.

Examples include:

* Milk
* Yogurt
* Fresh juice
* Meat
* Chicken
* Fish
* Eggs
* Tomatoes
* Lettuce
* Fruits
* Other perishable ingredients

When stock reaches or passes its expiry date according to the configured business rule, the system should identify it as expired.

The system should not silently remove the item from inventory.

Instead, the item should go through an appropriate expiry/waste process.

---

# 11. Expiry-to-Waste Workflow

The workflow may be:

```text
Batch
  ↓
Expiry Approaching
  ↓
Expiry Alert
  ↓
Staff Inspection
  ↓
Expired?
  ↓
YES
  ↓
Create Waste Record
  ↓
Reduce Inventory
  ↓
Stock Movement
  ↓
Audit Log
```

This ensures that expired stock remains traceable.

---

# 12. Automatic Expiry Detection

The system may periodically check batch expiry dates.

For example:

```text
Every day
     ↓
Check active batches
     ↓
Find expired batches
     ↓
Mark as expired / flag
     ↓
Notify authorized staff
```

However, automatically changing stock to waste should only happen if Board’s Cafe explicitly chooses that business rule.

A safer default is:

```text
System detects expiry
       ↓
System alerts staff
       ↓
Authorized staff verifies
       ↓
Waste is recorded
```

This avoids incorrectly wasting stock that may have special handling rules.

---

# 13. Near-Expiry Stock

The system should identify stock that is approaching expiry.

Example:

```text
Milk

Expiry:
10 Oct

Today:
08 Oct

Status:
EXPIRING_SOON
```

The system may generate alerts based on configured thresholds.

For example:

```text
7 days before expiry
3 days before expiry
1 day before expiry
Expired
```

The exact thresholds should be configurable.

---

# 14. Spoiled Products

An item may become unusable before its expiry date.

Example:

```text
Tomatoes

Expiry:
15 Oct

Actual condition:
Spoiled on 10 Oct
```

The item should be recorded as:

```text
Category:
SPOILAGE
```

rather than `EXPIRY`.

This distinction is important for identifying storage and handling problems.

---

# 15. Damaged Products

Products may become unusable because of physical damage.

Examples:

* Broken bottles
* Damaged packaging
* Dropped food containers
* Crushed products
* Broken eggs
* Damaged equipment-related stock

Example:

```text
Eggs

Received:
30 pieces

Damaged:
4 pieces

Usable:
26 pieces
```

The waste record should identify:

```text
Category:
DAMAGE
```

---

# 16. Preparation Waste

Preparation waste occurs while preparing ingredients.

Examples:

* Vegetable peels
* Fruit skins
* Unusable vegetable portions
* Bones
* Trimmings
* Spoiled portions removed during preparation

Not all preparation by-products should necessarily be treated as waste.

For example, some materials may be:

* Reused
* Stored
* Used for stock
* Used for another recipe

Only material that is actually discarded or removed from usable inventory should be recorded as waste.

---

# 17. Production Waste

Production waste occurs when prepared food or a production process results in unusable output.

Examples:

* Burnt food
* Failed recipe
* Incorrect preparation
* Contaminated production batch
* Incorrect quantity
* Production error

Example:

```text
Production:
50 sandwiches

Failed:
3 sandwiches

Waste:
3 sandwiches
```

The production record should be linked where applicable.

---

# 18. Overproduction Waste

Overproduction happens when more food is prepared than can reasonably be sold or reused.

Example:

```text
Expected demand:
50 portions

Produced:
70 portions

Sold:
55 portions

Remaining:
15 portions
```

If 15 portions cannot be safely reused, the system may record:

```text
Category:
OVERPRODUCTION

Quantity:
15 portions
```

This information can later help management improve production planning.

---

# 19. Customer Return Waste

A customer may return a product or prepared meal.

Example:

```text
Order:
#1052

Item:
Chicken Burger

Reason:
Customer returned item

Decision:
Cannot be resold

Waste:
1 portion
```

The waste record should reference the original order.

The related payment/refund should be handled by the POS and Expenses & Payments modules.

---

# 20. Supplier Rejection

Goods may be rejected when received from a supplier.

Example:

```text
Supplier:
Fresh Farm Supplies

Product:
Tomatoes

Delivered:
20 kg

Accepted:
18 kg

Rejected:
2 kg

Reason:
Poor quality
```

The receiving module records the rejected quantity.

If the goods are physically discarded by Board’s Cafe, a waste record may be created.

If they are returned to the supplier, the event should instead be linked to a purchase return.

---

# 21. Waste vs Supplier Return

These two events should not be confused.

### Supplier Return

```text
Supplier delivers damaged goods
       ↓
Cafe returns goods
       ↓
Supplier receives goods back
```

The goods do not become cafe waste.

### Waste

```text
Supplier delivery
       ↓
Cafe accepts stock
       ↓
Stock later becomes unusable
       ↓
Cafe disposes of it
```

This becomes waste.

---

# 22. Contaminated Stock

Inventory may become contaminated and therefore unusable.

Examples:

* Food contamination
* Chemical contamination
* Incorrect storage
* Cross-contamination
* Unsafe handling

Contaminated stock must not be available for normal production or sale.

The system should record:

```text
Category:
CONTAMINATION
```

and require an appropriate reason.

---

# 23. Waste Approval

Depending on Board’s Cafe's internal controls, certain waste records may require approval.

For example:

```text
Staff
  ↓
Records Waste
  ↓
Manager Reviews
  ↓
Approved
  ↓
Inventory Reduced
```

Alternatively, low-value waste may be recorded immediately while high-value waste requires approval.

Approval thresholds should be configurable.

---

# 24. High-Value Waste

The system may require approval when waste exceeds a configured quantity or monetary value.

Example:

```text
Waste Value:
150,000 RWF
```

The system could require manager approval before finalizing the adjustment.

This helps reduce unauthorized inventory manipulation.

---

# 25. Waste Cost

Waste should have an associated financial value where possible.

Example:

```text
Milk:
10 L

Cost:
1,000 RWF/L

Waste Cost:
10,000 RWF
```

The system should preferably calculate waste cost using the appropriate inventory cost rather than the current selling price.

The exact costing method should be finalized during Database Design and financial requirements.

---

# 26. Waste Cost vs Selling Price

Waste value should not normally be calculated using the selling price.

Example:

```text
Milk

Purchase Cost:
1,000 RWF/L

Selling Value:
1,500 RWF/L

Waste:
5 L
```

Inventory waste cost:

```text
5 × 1,000
= 5,000 RWF
```

Potential sales value:

```text
5 × 1,500
= 7,500 RWF
```

These represent different business metrics.

---

# 27. Waste Inventory Movement

Every finalized waste record should create an inventory movement.

Example:

```text
Inventory Item:
Milk

Batch:
MILK-001

Movement:
WASTE

Quantity:
-5 L

Reason:
EXPIRY
```

This provides traceability.

---

# 28. Waste and Production

For items produced by the cafe, waste may involve both ingredients and finished products.

Example:

```text
Production Order
      ↓
Ingredients consumed
      ↓
Finished product created
      ↓
Some finished product wasted
```

The system should distinguish:

```text
Ingredient Waste
```

from:

```text
Finished Product Waste
```

Example:

```text
Ingredient:
2 kg flour wasted

Finished Product:
5 cakes wasted
```

These should not be treated as the same inventory event.

---

# 29. Waste and Recipes

Waste may involve recipe ingredients.

Example:

A cake requires:

```text
Flour
Milk
Eggs
Sugar
Butter
```

If 2 kg of flour is wasted during preparation, the waste record should identify:

```text
Inventory Item:
Flour

Source:
PRODUCTION

Production:
Cake Batch #004

Reason:
Preparation error
```

This allows management to identify production inefficiencies.

---

# 30. Waste and Customer Orders

If waste results from a customer order, the system may link it to the order.

Example:

```text
Order #2004
       ↓
Pizza prepared
       ↓
Incorrect preparation
       ↓
Pizza discarded
       ↓
Waste Record
```

This can help identify repeated order-production problems.

---

# 31. Waste Reasons

The system should provide structured reasons.

Examples:

```text
Expired
Spoiled
Broken
Burnt
Incorrect Preparation
Contaminated
Overproduced
Customer Returned
Supplier Rejected
Storage Problem
Handling Problem
Unknown
Other
```

Staff should select the most appropriate reason and may provide additional notes.

---

# 32. Waste Notes

Staff should be able to provide additional context.

Example:

```text
Reason:
Spoilage

Notes:
Tomatoes were found soft and rotten during morning stock inspection.
```

For high-value waste, notes may be required.

---

# 33. Waste Evidence

Where useful, the system may support evidence such as:

* Photos
* Inspection notes
* Supplier documents
* Quality reports

For example, a staff member may photograph damaged goods.

Access to waste evidence should follow the system's permission rules.

---

# 34. Waste Dashboard

Authorized managers should see:

* Today's waste
* Waste this week
* Waste this month
* Highest-waste products
* Waste by category
* Waste by location
* Waste by staff member
* Expired stock
* Spoiled stock
* Production waste
* Overproduction
* Waste cost

Example:

```text
Waste This Month

Expiry:           85,000 RWF
Spoilage:         45,000 RWF
Production:       60,000 RWF
Damage:           20,000 RWF
Overproduction:   35,000 RWF

Total:
245,000 RWF
```

---

# 35. Waste Reports

The system should support:

### Waste Summary

* Total waste quantity
* Total waste cost
* Number of waste records

### Waste by Category

```text
Expiry
Spoilage
Damage
Production
Overproduction
Other
```

### Waste by Product

Identify products and ingredients with the highest waste.

### Waste by Batch

Identify batches that generated waste.

### Waste by Supplier

Identify suppliers associated with rejected or poor-quality stock.

### Waste by Location

Compare waste across branches/storage locations where applicable.

### Waste by Time

Daily, weekly, monthly, and custom date ranges.

---

# 36. Expiry Waste Report

A dedicated expiry report should show:

* Product
* Batch
* Quantity
* Expiry date
* Waste date
* Cost
* Location
* Reason
* Staff member

Example:

```text
Product: Milk
Batch: MILK-20261001-A
Quantity: 15 L
Expiry: 07 Oct
Wasted: 08 Oct
Cost: 15,000 RWF
```

This report is important for reducing future expiry losses.

---

# 37. Waste Rate

Management may monitor waste relative to production or purchases.

For example:

```text
Waste Rate =
Waste Quantity / Total Relevant Quantity × 100
```

The exact calculation should depend on the item and business context.

Possible measurements include:

* Waste as percentage of purchased stock
* Waste as percentage of production
* Waste cost as percentage of sales
* Expired stock rate

These metrics should be used for management analysis rather than changing inventory balances.

---

# 38. Notifications

The system may notify authorized staff about:

* Expired stock
* Near-expiry stock
* High-value waste
* Repeated waste of the same product
* Unapproved waste records
* Abnormally high waste
* Large production waste

Example:

```text
Alert

Milk batch MILK-20261006-A
has expired.

Quantity:
12 L

Action required:
Inspect and process stock.
```

---

# 39. Permissions

Suggested permissions include:

```text
waste.view
waste.create
waste.update
waste.approve
waste.cancel
waste.delete
waste.view_cost
waste.view_reports

expiry.view
expiry.manage
expiry.process

waste.export
```

Deletion of finalized waste records should be highly restricted or disabled.

Where possible, correction should happen through an audited adjustment rather than deletion.

---

# 40. Important Business Rules

The Waste Management module should follow these rules:

1. Every finalized waste event must identify the inventory item.
2. Batch information should be recorded when the item is batch-tracked.
3. Waste quantity must use the item's configured unit.
4. Waste quantity must not exceed available stock without an authorized adjustment.
5. Finalized waste must reduce inventory.
6. Inventory reduction must create a stock movement.
7. Expiry and spoilage must remain separate reasons.
8. Supplier returns must not automatically become waste.
9. Customer refunds and waste records are different transactions.
10. Waste caused by production should reference the relevant production activity where applicable.
11. Waste caused by a customer order should reference the order where applicable.
12. High-value waste may require approval.
13. Waste costs should be calculated using appropriate inventory cost information.
14. Historical waste records should not be silently deleted.
15. Waste corrections must be audited.
16. Expired stock should be flagged before or when it expires.
17. The system should not automatically discard physical stock without an appropriate business rule.
18. Only authorized users should process or approve waste.
19. Waste reports should preserve historical information even if products or suppliers later become inactive.
20. Important waste actions must be included in the audit log.

---

# 41. Example — Expired Milk

Suppose Board’s Cafe has:

```text
Product:
Milk

Batch:
MILK-20261005-A

Quantity:
30 L

Expiry:
08 Oct 2026
```

On 09 Oct:

```text
System:
Batch is expired
       ↓
Alert Staff
       ↓
Staff Inspects
       ↓
30 L confirmed unusable
       ↓
Create Waste Record
       ↓
Reason:
EXPIRY
       ↓
Inventory:
30 L → 0 L
       ↓
Stock Movement:
WASTE -30 L
       ↓
Audit Log
```

The system can then include the event in the expiry-waste report.

---

# 42. Example — Spoiled Tomatoes

```text
Inventory:
20 kg tomatoes

Expiry:
15 Oct

Inspection:
10 Oct

Condition:
Spoiled

Wasted:
4 kg
```

The system records:

```text
Category:
SPOILAGE

Quantity:
4 kg

Remaining:
16 kg
```

This should not be classified as expiry because the tomatoes became unusable before their expiry date.

---

# 43. Example — Production Waste

A production staff member prepares 50 sandwiches.

```text
Produced:
50

Failed:
3

Usable:
47
```

The system records:

```text
Waste Category:
PRODUCTION

Quantity:
3 sandwiches

Source:
PRODUCTION

Reason:
Incorrect preparation
```

If the sandwiches are finished products, the waste affects finished-product inventory.

If ingredients were wasted during preparation, those ingredients should be recorded separately where appropriate.

---

# 44. Example — Overproduction

Board’s Cafe prepares 100 portions of a food item.

At closing:

```text
Sold:
80

Remaining:
20
```

If the remaining 20 cannot safely be reused:

```text
Waste Category:
OVERPRODUCTION

Quantity:
20 portions
```

This information can later help management compare production levels with actual demand.

---

# 45. Complete Waste Flow

```text
                 INVENTORY
                     │
        ┌────────────┼─────────────┐
        ↓            ↓             ↓
      EXPIRY      SPOILAGE       DAMAGE
        │            │             │
        └────────────┼─────────────┘
                     ↓
                WASTE RECORD
                     │
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
   PRODUCTION   CUSTOMER RETURN  RECEIVING
       │             │             │
       └─────────────┼─────────────┘
                     ↓
              APPROVAL (if needed)
                     ↓
             INVENTORY MOVEMENT
                     ↓
              STOCK REDUCTION
                     ↓
                WASTE REPORT
                     ↓
               AUDIT LOG
```

---

# 46. Relationship With Other Modules

### Inventory

```text
Inventory
   ↓
Waste
   ↓
Stock Movement
   ↓
Updated Stock
```

### Batch & Expiry

```text
Batch
   ↓
Expiry
   ↓
Alert
   ↓
Waste
```

### Purchases

```text
Purchase
   ↓
Receiving
   ↓
Rejected / Damaged
   ↓
Return or Waste
```

### Production

```text
Production
   ↓
Ingredient Consumption
   ↓
Finished Product
   ↓
Production Waste
```

### POS

```text
Customer Order
   ↓
Returned / Failed Product
   ↓
Waste
```

### Expenses & Payments

```text
Waste
   ↓
Inventory Cost
   ↓
Waste Cost Reporting
```

### Reports

```text
Waste
   ├── Expiry Report
   ├── Product Report
   ├── Supplier Report
   ├── Production Report
   └── Cost Report
```

---

# 47. Data Integrity Requirements

The system should maintain consistency between:

* Inventory
* Batches
* Expiry dates
* Waste records
* Stock movements
* Purchases
* Production
* POS orders
* Supplier returns
* Audit logs

For example, the system should prevent:

```text
Available stock:
10 kg

Waste:
15 kg
```

unless a controlled correction is being performed.

Similarly, the system should not allow:

```text
Waste:
5 kg

Inventory:
No corresponding stock movement
```

because this would make the inventory history unreliable.

Every finalized waste record must have a corresponding inventory effect when the waste represents physical stock leaving usable inventory.

---

# 48. Audit Requirements

Important waste actions must be logged.

Examples:

```text
Waste Created
Waste Approved
Waste Cancelled
Waste Adjusted
Expiry Processed
Inventory Reduced
Waste Record Viewed
```

The audit log should identify:

* User
* Action
* Date/time
* Waste record
* Inventory item
* Previous quantity where applicable
* New quantity where applicable
* Reason

This is especially important because waste records directly affect inventory balances and may have financial implications.

---

# 49. Summary

Waste Management provides Board’s Cafe with a controlled process for identifying, recording, and analyzing inventory losses.

The main flow is:

```text
STOCK
  ↓
Problem Identified
  ↓
Classify Reason
  ↓
Create Waste Record
  ↓
Review / Approve
  ↓
Reduce Inventory
  ↓
Create Stock Movement
  ↓
Calculate Waste Cost
  ↓
Report
  ↓
Audit
```

The most important principle is:

**Board’s Cafe should never simply delete expired, spoiled, damaged, or wasted stock from inventory. Every loss should have a traceable reason and an auditable inventory movement.**

This will allow the cafe to understand not only **how much stock is being lost**, but also **why it is being lost**, which is essential for reducing costs and improving purchasing, storage, production, and sales decisions.
