# 10 — Purchases & Suppliers

## 1. Purpose

The Purchases & Suppliers module manages the process of obtaining products and ingredients from suppliers and adding received stock into Board’s Cafe inventory.

The module provides a controlled process for:

* Managing suppliers
* Creating purchase orders
* Recording purchased items
* Receiving deliveries
* Recording quantities and costs
* Creating inventory batches
* Recording expiry dates
* Handling partial deliveries
* Handling rejected or damaged items
* Tracking supplier history
* Maintaining purchase records
* Supporting inventory and financial reporting

The purchasing process must connect closely with:

* Inventory Management
* Batch & Expiry Management
* Products & Recipes
* Expenses & Payments
* Waste Management
* Reports & Dashboard
* Audit Logging

---

# 2. Purchasing Objectives

The system should allow authorized staff to:

* Create supplier records
* Update supplier information
* View supplier history
* Create purchase orders
* Add products or ingredients to purchase orders
* Specify expected quantities
* Record expected prices
* Submit purchase orders
* Approve purchase orders where approval is required
* Record supplier deliveries
* Compare ordered and received quantities
* Accept partial deliveries
* Reject damaged or unacceptable items
* Record actual purchase costs
* Create inventory batches
* Record batch numbers
* Record expiry dates
* Update inventory after receiving
* Record supplier references/invoices
* Track outstanding purchases
* View purchase history
* Generate purchasing reports

---

# 3. Supplier Management

A supplier represents a person, company, farmer, distributor, wholesaler, or other source from which Board’s Cafe obtains inventory.

Examples may include suppliers of:

* Milk
* Eggs
* Chicken
* Vegetables
* Fruits
* Wheat flour
* Sugar
* Cooking oil
* Coffee beans
* Tea
* Bottled water
* Packaged drinks
* Bread
* Cleaning or other consumable supplies

The system should maintain one supplier record that can be referenced by multiple purchases.

---

# 4. Supplier Information

A supplier record may contain:

* Supplier ID
* Supplier name
* Contact person
* Phone number
* Email address where applicable
* Physical address
* Business/company information where applicable
* Tax/business identification information where applicable
* Supplier status
* Notes
* Created by
* Created date
* Updated date

The exact fields can be finalized during database design.

---

# 5. Supplier Status

Suggested supplier statuses include:

```text
ACTIVE
INACTIVE
SUSPENDED
```

### ACTIVE

The supplier can be used for new purchases.

### INACTIVE

The supplier is no longer normally used but historical purchase records remain available.

### SUSPENDED

The supplier is temporarily prevented from being used for new purchases.

A supplier should normally be deactivated rather than permanently deleted if historical purchases reference the supplier.

---

# 6. Supplier Products

A supplier may provide many inventory items.

For example:

```text
Supplier A
├── Milk
├── Yogurt
├── Butter
└── Cheese
```

Another supplier may provide:

```text
Supplier B
├── Tomatoes
├── Onions
├── Lettuce
└── Peppers
```

The system should allow the same inventory item to be purchased from multiple suppliers.

For example:

```text
Tomato
├── Supplier A
├── Supplier B
└── Supplier C
```

This allows the cafe to compare suppliers and does not incorrectly tie an inventory item to only one supplier.

---

# 7. Purchase Order

A Purchase Order (PO) is a formal request to purchase inventory from a supplier.

A purchase order should contain information such as:

* Purchase Order ID
* Purchase Order number
* Supplier
* Order date
* Expected delivery date
* Status
* Items
* Quantities
* Expected unit costs
* Expected total
* Notes
* Created by
* Approved by where applicable
* Created date
* Updated date

---

# 8. Purchase Order Items

Each purchase order may contain multiple items.

Example:

```text
Purchase Order #PO-00125

Supplier: Fresh Farm Supplies

10 kg Tomatoes
5 kg Onions
3 kg Lettuce
20 kg Potatoes
```

Each purchase order item should record:

* Inventory item
* Ordered quantity
* Unit
* Expected unit cost
* Expected line total
* Received quantity
* Remaining quantity
* Notes

The received quantity may be different from the ordered quantity.

---

# 9. Purchase Order Status

Suggested purchase order statuses:

```text
DRAFT
SUBMITTED
APPROVED
ORDERED
PARTIALLY_RECEIVED
FULLY_RECEIVED
CANCELLED
CLOSED
```

### DRAFT

The purchase order is being prepared.

### SUBMITTED

The purchase order has been submitted for approval or processing.

### APPROVED

The purchase request has been approved.

### ORDERED

The supplier has received or been sent the purchase order.

### PARTIALLY_RECEIVED

Some items or quantities have been received, but the full order has not been received.

### FULLY_RECEIVED

All expected quantities have been received and accepted.

### CANCELLED

The purchase order was cancelled.

### CLOSED

The purchase process is complete and no further receiving is expected.

---

# 10. Purchase Approval

Depending on the cafe's internal controls, purchases may require approval.

For example:

```text
Staff creates PO
       ↓
Manager reviews PO
       ↓
Manager approves
       ↓
Supplier receives order
```

The approval process should be permission-based.

The system should record:

* Approving user
* Approval date/time
* Approval status
* Comments where applicable

Staff members should not be able to approve purchases they are not authorized to approve.

---

# 11. Purchase Order Workflow

The general purchasing workflow is:

```text
Identify Stock Need
       ↓
Create Purchase Order
       ↓
Select Supplier
       ↓
Add Items
       ↓
Enter Quantities
       ↓
Enter Expected Costs
       ↓
Submit
       ↓
Approval
       ↓
Send/Place Order
       ↓
Supplier Delivers
       ↓
Receive Goods
       ↓
Inspect Goods
       ↓
Accept / Reject
       ↓
Create Batch Records
       ↓
Update Inventory
       ↓
Record Actual Cost
       ↓
Record Supplier Invoice
       ↓
Complete Purchase
```

---

# 12. Stock Replenishment

Purchases may be initiated because inventory has reached or fallen below its reorder level.

For example:

```text
Tomatoes

Current usable stock: 2 kg
Reorder level:        5 kg
```

The system can identify tomatoes as requiring replenishment.

A staff member may then create a purchase order.

The system should not automatically purchase stock unless automatic purchasing is explicitly enabled in the future.

---

# 13. Receiving Goods

When a supplier delivers goods, authorized staff should record the actual received quantities.

The receiving process should compare:

```text
Ordered Quantity
        vs
Received Quantity
```

Example:

```text
Ordered:
20 kg Tomatoes

Received:
18 kg Tomatoes
```

The system records:

```text
Ordered:  20 kg
Received: 18 kg
Missing:   2 kg
```

The purchase order may therefore become:

```text
PARTIALLY_RECEIVED
```

---

# 14. Full Delivery

If the supplier delivers the complete order:

```text
Ordered:
20 kg Tomatoes

Received:
20 kg Tomatoes
```

The purchase order can become:

```text
FULLY_RECEIVED
```

The received stock is then added to inventory.

---

# 15. Over-Delivery

A supplier may deliver more than the ordered quantity.

Example:

```text
Ordered: 20 kg
Received: 22 kg
```

The system should not silently accept the extra 2 kg.

The cafe's business rules should determine whether over-delivery is:

* Allowed
* Allowed only with approval
* Recorded separately
* Rejected

If accepted, the actual received quantity must be recorded accurately.

---

# 16. Partial Delivery

A supplier may deliver an order in multiple deliveries.

Example:

```text
Purchase Order:
100 kg flour

Delivery 1:
60 kg

Delivery 2:
40 kg
```

After delivery 1:

```text
Received: 60 kg
Remaining: 40 kg
Status: PARTIALLY_RECEIVED
```

After delivery 2:

```text
Received: 100 kg
Remaining: 0 kg
Status: FULLY_RECEIVED
```

Each delivery should have its own receiving record.

---

# 17. Goods Inspection

Received goods should be checked before being added as usable inventory.

The receiving process may verify:

* Correct item
* Correct quantity
* Physical condition
* Packaging condition
* Batch number
* Expiry date
* Unit
* Purchase price
* Supplier
* Delivery reference

For perishable products, expiry information is especially important.

---

# 18. Rejected Goods

Goods that are damaged, spoiled, incorrect, or otherwise unacceptable should not automatically become usable inventory.

Examples:

* Rotten tomatoes
* Damaged milk packaging
* Expired products
* Broken bottles
* Incorrect products
* Poor-quality ingredients

The receiving process should allow staff to record:

```text
Ordered:       50 kg
Delivered:     50 kg
Accepted:      47 kg
Rejected:       3 kg
```

The rejected quantity should be recorded with a reason.

---

# 19. Batch Creation During Receiving

When a received inventory item requires batch tracking, the system should create a batch record.

Example:

```text
Purchase:
20 kg Tomatoes

Batch:
TOM-20261008-A

Quantity:
20 kg

Received:
8 Oct 2026

Expiry:
13 Oct 2026
```

The batch becomes part of the inventory system.

This allows later FEFO selection and expiry monitoring.

---

# 20. Multiple Batches in One Delivery

A delivery may contain multiple batches of the same inventory item.

For example:

```text
Milk
       ↓
Batch A → 20 L → Expires 10 Oct
Batch B → 30 L → Expires 13 Oct
```

The system should preserve both batches separately.

It should not combine them into a single batch merely because they are the same inventory item.

---

# 21. Expiry Information

For expiry-tracked products, receiving staff should record the expiry date where available.

Examples:

* Milk
* Yogurt
* Chicken
* Eggs
* Tomatoes
* Lettuce
* Fresh juice
* Other perishable ingredients

If an inventory item is configured to require expiry tracking, the system should require appropriate expiry information during receiving.

The exact rules should be finalized in the Batch & Expiry Management module.

---

# 22. Purchase Costs

The system should record the actual cost paid to the supplier.

Example:

```text
Tomatoes
Quantity: 20 kg
Unit Cost: 1,200 RWF/kg

Total:
24,000 RWF
```

For multiple items:

```text
Tomatoes:
20 kg × 1,200 = 24,000 RWF

Onions:
10 kg × 900 = 9,000 RWF

Total:
33,000 RWF
```

The purchase record should preserve the actual transaction cost.

---

# 23. Expected Cost vs Actual Cost

The expected purchase cost may differ from the actual supplier invoice.

Example:

```text
Expected:
1,100 RWF/kg

Actual:
1,200 RWF/kg
```

The system should preserve both where relevant.

This allows the cafe to identify price changes and purchasing variances.

---

# 24. Supplier Invoice

A supplier may provide an invoice or delivery reference.

The system should allow authorized staff to record:

* Invoice number
* Invoice date
* Supplier
* Purchase order
* Total invoice amount
* Payment status
* Reference information
* Notes

The invoice should be linked to the relevant purchase records.

---

# 25. Purchase Payment Status

A purchase may be:

```text
UNPAID
PARTIALLY_PAID
PAID
OVERDUE
CANCELLED
```

This allows the cafe to track supplier obligations.

Payment information should be handled together with the Expenses & Payments module rather than being duplicated across unrelated systems.

---

# 26. Inventory Integration

Receiving a purchase should increase inventory.

Example:

```text
Supplier Delivery
       ↓
Goods Received
       ↓
Accepted Quantity
       ↓
Batch Created
       ↓
Inventory Increased
       ↓
Stock Movement Recorded
```

For example:

```text
Tomatoes

Existing usable stock: 5 kg
Received:              20 kg
New usable stock:      25 kg
```

The inventory movement should record that the increase came from a purchase receipt.

---

# 27. Stock Movement

The inventory system should record a stock movement for received goods.

Suggested movement:

```text
RECEIPT
```

The movement may reference:

* Inventory item
* Batch
* Quantity
* Unit
* Purchase order
* Receiving record
* Supplier
* User
* Date/time

This creates a traceable connection between purchasing and inventory.

---

# 28. Purchase-to-Batch Traceability

The system should maintain the relationship:

```text
Supplier
   ↓
Purchase Order
   ↓
Purchase Order Item
   ↓
Goods Receipt
   ↓
Batch
   ↓
Inventory
```

This allows staff to answer questions such as:

* Where did this batch come from?
* Which supplier supplied it?
* When was it received?
* How much was received?
* What was the purchase cost?
* When does it expire?
* Which orders eventually consumed it?

---

# 29. Supplier Performance

The system may provide supplier performance information based on historical purchases.

Possible measurements include:

* Number of purchases
* Total purchase value
* Delivery frequency
* Partial deliveries
* Rejected quantities
* Damaged quantities
* Price changes
* Delivery delays
* Expired goods received
* Average purchase cost

These reports should support management decisions.

---

# 30. Supplier Price History

The system should preserve historical purchase prices.

Example:

```text
Tomatoes

Supplier A:
Jan → 900 RWF/kg
Feb → 1,000 RWF/kg
Mar → 1,200 RWF/kg
```

This allows managers to identify changes in supplier pricing.

The current price should not overwrite historical purchase costs.

---

# 31. Multiple Suppliers

The same inventory item may be purchased from different suppliers.

Example:

```text
                 Tomato
              /    |    \
             /     |     \
      Supplier A Supplier B Supplier C
```

The system should maintain the actual supplier used for every purchase.

This supports supplier comparison and purchasing flexibility.

---

# 32. Purchase Returns

If goods need to be returned to a supplier, the system should support a controlled purchase return process.

Possible reasons include:

* Damaged goods
* Wrong products
* Poor quality
* Incorrect quantity
* Expired goods
* Supplier error

The return should record:

* Original purchase
* Supplier
* Returned item
* Quantity
* Batch where applicable
* Reason
* Date
* Staff member
* Financial adjustment where applicable

Returned inventory should be removed or adjusted through a proper inventory movement.

---

# 33. Damaged Goods During Receiving

Damage identified during receiving should be recorded separately from accepted stock.

Example:

```text
Delivery:
100 eggs

Accepted:
96 eggs

Damaged:
4 eggs
```

The system should record:

```text
Received: 100
Accepted: 96
Rejected/Damaged: 4
```

The 4 damaged eggs should not be added to usable inventory.

If the cafe decides to dispose of them, the Waste Management module should record the disposal.

---

# 34. Expired Goods at Receiving

A supplier may accidentally deliver expired products.

Example:

```text
Product: Yogurt
Received: 8 Oct
Expiry: 5 Oct
```

The system should flag the item as unacceptable or expired according to the receiving rules.

It should not become normal usable stock.

The event should be recorded for supplier and quality tracking.

---

# 35. Purchase and Waste Relationship

Waste can originate during receiving.

For example:

```text
Supplier delivers:
20 kg Tomatoes

Accepted:
18 kg

Rejected:
2 kg spoiled
```

The system may create a waste/disposal record for the rejected quantity if the cafe physically disposes of it.

This maintains a complete trail:

```text
Purchase
   ↓
Receiving
   ↓
Rejected Quantity
   ↓
Waste
```

---

# 36. Purchase and Expenses Relationship

Purchases may create financial obligations.

For example:

```text
Purchase Order
      ↓
Goods Received
      ↓
Supplier Invoice
      ↓
Expense/Payable
      ↓
Supplier Payment
```

The purchasing module should provide the transaction information required by the Expenses & Payments module.

Financial records should not be duplicated unnecessarily.

---

# 37. Purchase Reports

The system should support reports such as:

### Purchase Summary

* Total purchases
* Number of purchase orders
* Completed purchases
* Pending purchases

### Supplier Report

* Purchases by supplier
* Amount spent per supplier
* Supplier delivery history

### Item Purchase Report

* Quantity purchased
* Average purchase cost
* Latest purchase cost
* Supplier history

### Purchase Variance

* Ordered quantity vs received quantity
* Expected cost vs actual cost

### Rejection Report

* Rejected quantities
* Rejection reasons
* Supplier associated with rejection

### Purchase Payment Report

* Paid purchases
* Unpaid purchases
* Partially paid purchases
* Overdue supplier payments

---

# 38. Purchase Dashboard

Authorized managers may see information such as:

* Pending purchase orders
* Orders awaiting approval
* Expected deliveries
* Partially received purchases
* Recent purchases
* Unpaid supplier invoices
* Top suppliers by spending
* Recently changed purchase prices
* Rejected deliveries

The dashboard should respect user permissions.

---

# 39. Permissions

Suggested purchasing permissions include:

```text
suppliers.view
suppliers.create
suppliers.update
suppliers.deactivate

purchases.view
purchases.create
purchases.update
purchases.submit
purchases.approve
purchases.cancel

purchases.receive
purchases.partial_receive
purchases.reject_items
purchases.return

purchases.view_history
purchases.view_costs
purchases.view_reports
```

The exact permissions should be finalized in the User Roles & Permissions and Security documents.

---

# 40. Example Purchase Workflow

Suppose Board’s Cafe needs tomatoes.

Current stock:

```text
Usable tomatoes: 3 kg
Reorder level:   5 kg
```

The storekeeper identifies that more tomatoes are required.

### Step 1 — Create Purchase Order

```text
Supplier:
Fresh Farm Supplies

Item:
Tomatoes

Quantity:
20 kg

Expected cost:
1,100 RWF/kg
```

### Step 2 — Approval

The manager reviews and approves the purchase.

### Step 3 — Delivery

The supplier delivers:

```text
20 kg tomatoes
```

### Step 4 — Inspection

Staff inspect the delivery:

```text
Accepted:
18 kg

Rejected:
2 kg
```

### Step 5 — Batch Creation

The accepted stock arrives as:

```text
Batch:
TOM-20261008-A

Quantity:
18 kg

Expiry:
13 Oct 2026
```

### Step 6 — Inventory Update

```text
Existing:
3 kg

Received:
18 kg

New usable stock:
21 kg
```

### Step 7 — Records

The system records:

```text
Purchase Order
Goods Receipt
Batch
Stock Movement
Supplier Invoice
Payment/Payable
Audit Log
```

---

# 41. Important Business Rules

The purchasing module should follow these rules:

1. Only authorized staff can create or manage purchases.
2. Supplier records should be unique and reusable.
3. The same inventory item may have multiple suppliers.
4. Historical purchase records must not be deleted simply because a supplier becomes inactive.
5. Purchase orders should have controlled statuses.
6. Approval should be permission-based where required.
7. Received quantities must be recorded separately from ordered quantities.
8. Partial deliveries must be supported.
9. Over-deliveries must follow configured business rules.
10. Damaged or rejected goods must not become usable stock.
11. Expired goods must not become normal usable inventory.
12. Batch-tracked items must create appropriate batch records when received.
13. Multiple batches of the same item must remain separately traceable.
14. Actual purchase costs must be preserved.
15. Historical purchase costs must not be overwritten by new prices.
16. Inventory increases must generate stock movement records.
17. Purchase returns must use controlled inventory adjustments.
18. Supplier invoices and payments should integrate with Expenses & Payments.
19. Waste resulting from rejected or damaged goods should be recorded through Waste Management.
20. Important purchasing actions must be included in the audit log.
21. Purchase records should not be silently deleted after inventory or financial records have been created.
22. Unauthorized users must not be able to change supplier costs, approve purchases, receive goods, or process returns.
23. The system should preserve the relationship between supplier, purchase, receipt, batch, and inventory.
24. Historical records must remain accurate even when suppliers, prices, or inventory configurations change.

---

# 42. Core Purchasing Flow

```text
SUPPLIER
    ↓
PURCHASE ORDER
    ↓
APPROVAL
    ↓
SUPPLIER DELIVERY
    ↓
GOODS RECEIVING
    ↓
INSPECTION
    ↓
 ┌───────────────┐
 │               │
ACCEPTED       REJECTED
 │               │
 ↓               ↓
BATCH          RETURN / WASTE
 │
 ↓
INVENTORY
 │
 ↓
STOCK MOVEMENT
 │
 ↓
AVAILABLE STOCK
```

---

# 43. Relationship With Other Modules

The purchasing module connects to the rest of Board’s Cafe as follows:

```text
Suppliers
    ↓
Purchases
    ↓
Goods Receiving
    ↓
Batches
    ↓
Inventory
    ↓
Recipes / Production
    ↓
POS / Sales
```

Financial relationship:

```text
Purchase
    ↓
Supplier Invoice
    ↓
Expense / Payable
    ↓
Supplier Payment
```

Waste relationship:

```text
Receiving
    ↓
Rejected / Damaged Goods
    ↓
Waste Record
```

Reporting relationship:

```text
Purchases
   ├── Supplier Reports
   ├── Cost Reports
   ├── Inventory Reports
   └── Financial Reports
```

---

# 44. Data Integrity Requirements

The system should maintain consistency between:

* Suppliers
* Purchase orders
* Purchase order items
* Goods receipts
* Batches
* Inventory
* Stock movements
* Supplier invoices
* Payments
* Waste
* Audit logs

For example, the system should prevent situations such as:

```text
Purchase Order:
20 kg tomatoes

Goods Receipt:
20 kg

Inventory:
25 kg added
```

unless the additional 5 kg has a valid, traceable reason.

Similarly, the system should prevent:

```text
Received:
20 kg

Inventory:
0 kg
```

unless the stock has been explicitly rejected, returned, wasted, or otherwise processed.

---

# 45. Summary

The Purchases & Suppliers module provides the controlled connection between suppliers and Board’s Cafe inventory.

The main flow is:

```text
SUPPLIER
   ↓
PURCHASE ORDER
   ↓
APPROVAL
   ↓
DELIVERY
   ↓
RECEIVING
   ↓
INSPECTION
   ↓
BATCH CREATION
   ↓
INVENTORY UPDATE
   ↓
STOCK MOVEMENT
   ↓
SUPPLIER INVOICE
   ↓
PAYMENT / PAYABLE
   ↓
REPORTING
   ↓
AUDIT LOG
```

The most important principle is that **receiving stock is not simply increasing an inventory number**. It must create a traceable record connecting the supplier, purchase, received quantity, batch, expiry information, cost, inventory movement, and financial record.

This provides Board’s Cafe with reliable purchasing history and a strong foundation for inventory control, expiry tracking, cost analysis, and reporting.
