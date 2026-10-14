# Board’s Cafe Management System

# 02 — Business Requirements

## 2.1 Introduction

The Board’s Cafe Management System is an internal web-based system intended to support the daily operations of Board’s Cafe.

The system will provide a centralized way for authorized staff to manage customer orders, menu products, recipes, ingredients, inventory, stock batches, expiry dates, purchases, suppliers, payments, expenses, waste, reports, notifications, and staff access.

The system will be designed around the actual operational processes of Board’s Cafe.

---

# 2.2 Business Problem

Board’s Cafe needs to manage several activities that are connected to one another.

When a customer places an order, staff need to record the order and send it for preparation.

When a menu product is prepared, ingredients such as milk, wheat flour, sugar, coffee, eggs, butter, and other materials are consumed.

At the same time, these ingredients are purchased from suppliers and stored as inventory.

Some ingredients are perishable and have expiry dates. The same ingredient can also be received multiple times, with different quantities, costs, batch numbers, and expiry dates.

For example:

```text
Milk

Batch M001
20 Litres
Expires: 10 October

Batch M002
30 Litres
Expires: 25 October
```

Therefore, simply knowing that Board’s Cafe has "50 litres of milk" is not sufficient.

The cafe needs to know:

* Which batch the stock belongs to.
* How much remains in each batch.
* When each batch expires.
* Which batch should be consumed first.
* How much stock was consumed.
* Why stock was removed.
* Who performed important stock operations.

Without proper tracking, expired stock can remain unnoticed, stock quantities can become inaccurate, and the cafe can experience avoidable losses.

---

# 2.3 Business Goal

The primary goal is to provide Board’s Cafe with one reliable internal system for controlling its daily operations and maintaining accurate business records.

The system should help the cafe:

* Improve stock visibility.
* Reduce expired stock.
* Reduce unnecessary waste.
* Improve order management.
* Improve ingredient tracking.
* Improve purchasing decisions.
* Monitor expenses.
* Track payments.
* Improve staff accountability.
* Provide management with useful information for decision-making.

---

# 2.4 Business Objectives

The system shall support the following objectives.

## BO-001 — Centralize Operations

Bring important cafe operations into one system instead of maintaining disconnected records.

## BO-002 — Improve Inventory Control

Allow staff to know what stock is available, how much remains, and how inventory changes over time.

## BO-003 — Reduce Expired Products

Identify stock that is approaching expiry and expired stock so staff can take appropriate action.

## BO-004 — Reduce Waste

Track expired, damaged, spoiled, and otherwise wasted stock.

## BO-005 — Connect Sales and Inventory

Connect menu products sold to the ingredients required to prepare them.

## BO-006 — Improve Purchasing

Provide information that helps staff understand stock requirements and purchasing history.

## BO-007 — Improve Financial Visibility

Track sales, payments, purchases, and operating expenses.

## BO-008 — Improve Staff Accountability

Record important actions performed by staff members.

## BO-009 — Improve Security

Ensure staff can only access functions and information permitted by their assigned roles and permissions.

## BO-010 — Support Management Decisions

Provide reports and dashboards that help management understand the operational and financial condition of the cafe.

---

# 2.5 Core Business Concepts

The system will be based on several important business concepts.

## 2.5.1 Menu Product

A menu product is something sold to customers.

Examples include:

* Cappuccino
* Latte
* Tea
* Pancake
* Cake
* Sandwich
* Other cafe products

A menu product has a selling price and may have a recipe.

---

## 2.5.2 Ingredient

An ingredient is a raw material or stock item used to prepare one or more menu products.

Examples include:

* Milk
* Wheat flour / Ifarini
* Sugar
* Coffee
* Eggs
* Butter
* Cooking oil
* Chocolate

---

## 2.5.3 Recipe

A recipe defines the ingredients and quantities required to prepare a menu product.

For example:

```text
Cappuccino
│
├── Milk       150 ml
├── Coffee      20 g
└── Sugar       10 g
```

---

## 2.5.4 Shared Ingredients

An important business requirement is that an ingredient can be used in multiple menu products.

For example:

```text
Milk
│
├── Cappuccino
├── Latte
├── Tea
├── Pancake
└── Cake
```

Similarly:

```text
Wheat Flour
│
├── Pancake
├── Cake
├── Bread
└── Mandazi
```

Therefore, the system must support the relationship:

> **One ingredient can be used in many menu products, and one menu product can use many ingredients.**

This relationship will later be represented through the recipe structure in the database and ERD.

---

# 2.6 Made-to-Order Business Model

Board’s Cafe may prepare products after a customer places an order.

Therefore, the system should support a made-to-order process.

The general process is:

```text
Customer
    ↓
Order
    ↓
Order Confirmation
    ↓
Kitchen Preparation
    ↓
Recipe
    ↓
Ingredient Requirements
    ↓
Inventory Consumption
    ↓
Product Ready
    ↓
Order Completion
    ↓
Payment
```

The system should not automatically consume inventory merely because an order has been created.

Inventory consumption should occur according to the defined preparation/consumption workflow.

---

# 2.7 Inventory and Expiry Business Requirement

Inventory must be tracked in a way that supports expiry management.

The system should distinguish between:

```text
Inventory Item
       ↓
Inventory Batch
       ↓
Quantity
       ↓
Expiry Date
```

For example:

```text
Milk
│
├── Batch M001
│   ├── 20 L
│   └── 10 October
│
└── Batch M002
    ├── 30 L
    └── 25 October
```

The system should therefore be able to identify the exact stock that is approaching expiry.

---

# 2.8 Expiry Management Objective

The system should help Board’s Cafe prevent avoidable expiry losses.

It should:

1. Record expiry dates.
2. Monitor approaching expiry.
3. Identify expired stock.
4. Alert authorized staff.
5. Prevent expired stock from normal consumption.
6. Prioritize stock with the earliest valid expiry.
7. Record expired stock when it becomes waste.
8. Provide reports about expiry-related losses.

---

# 2.9 FEFO Business Principle

Where applicable, inventory consumption should follow:

**First Expired, First Out (FEFO).**

For example:

```text
Milk Batch A → Expires 10 Oct
Milk Batch B → Expires 20 Oct
Milk Batch C → Expires 30 Oct
```

If the cafe needs milk, the system should prioritize:

```text
Batch A
   ↓
Batch B
   ↓
Batch C
```

provided that each batch is valid and has sufficient available quantity.

---

# 2.10 Stock Traceability

The business requires inventory changes to be traceable.

For an inventory change, the system should be able to determine:

* What item changed?
* Which batch changed?
* What quantity changed?
* Was stock added or removed?
* Why did it change?
* What business transaction caused it?
* Who performed the action?
* When did it happen?

This is particularly important for:

* Purchases.
* Recipe consumption.
* Waste.
* Stock adjustments.
* Returns.
* Corrections.

---

# 2.11 Order Management

The system should support the complete customer order lifecycle.

A typical order may follow:

```text
Draft
  ↓
Confirmed
  ↓
Preparing
  ↓
Ready
  ↓
Completed
```

Additional states may include:

```text
Cancelled
Refunded
```

The exact status rules will be defined in the functional and workflow documentation.

---

# 2.12 Kitchen Operations

The system should allow kitchen staff to see orders that require preparation.

Kitchen staff should be able to understand:

* What products have been ordered.
* Required quantities.
* Which orders are waiting.
* Which orders are being prepared.
* Which orders are ready.

This allows the POS/order process and kitchen process to remain connected.

---

# 2.13 Purchasing

Board’s Cafe needs to record stock purchased from suppliers.

A purchase should be associated with:

```text
Supplier
    ↓
Purchase
    ↓
Purchased Items
    ↓
Received Stock
    ↓
Inventory Batch
```

For relevant items, the purchase process should capture:

* Quantity.
* Purchase cost.
* Supplier.
* Batch number.
* Expiry date.
* Date received.

---

# 2.14 Supplier Management

The system should maintain supplier information and purchase history.

This should allow authorized staff to determine:

* Which suppliers provide particular items.
* What has been purchased.
* When it was purchased.
* How much was purchased.
* How much was paid.

---

# 2.15 Expense Management

The system should allow authorized staff to record operating expenses.

Examples include:

* Electricity.
* Water.
* Internet.
* Maintenance.
* Cleaning.
* Transport.
* Other business expenses.

Expenses should be categorized so management can understand where money is being spent.

---

# 2.16 Payment Management

The system should record payments associated with customer orders.

The business should be able to determine:

* Which order was paid.
* Amount paid.
* Payment method.
* Payment status.
* Payment date.
* Staff member who recorded the payment.

The final supported payment methods should be configurable according to Board’s Cafe's actual payment practices.

---

# 2.17 Waste Management

The system should track stock that cannot be sold or used.

Waste may result from:

* Expiry.
* Spoilage.
* Damage.
* Incorrect preparation.
* Accidental loss.
* Other causes.

The system should record the quantity and reason for the waste.

---

# 2.18 Reporting Requirements

Management should be able to obtain useful information about:

### Sales

* Total sales.
* Number of orders.
* Best-selling products.
* Sales by period.

### Inventory

* Current stock.
* Low-stock items.
* Stock consumption.
* Stock movements.

### Expiry

* Expiring-soon stock.
* Expired stock.
* Stock value at risk.
* Expiry-related waste.

### Purchasing

* Purchases.
* Supplier activity.
* Purchase spending.

### Expenses

* Expenses by category.
* Expenses by period.

### Waste

* Waste quantity.
* Waste reason.
* Waste value.
* Expiry-related waste.

---

# 2.19 Staff and Access Management

The system will be used by internal staff.

The administrator will have authority over staff access.

The business access structure is:

```text
Admin
   ↓
Users
   ↓
Roles
   ↓
Permissions
   ↓
Allowed Actions
```

The administrator should be able to:

* Create users.
* Edit users.
* Activate users.
* Deactivate users.
* Assign roles.
* Create roles where permitted.
* Assign permissions.
* Remove permissions.
* Reset passwords.
* Control access to system modules.

The detailed permission matrix will be defined in Document 04.

---

# 2.20 Accountability

Important business activities should be traceable to the staff member who performed them.

Examples include:

* Recording a purchase.
* Adjusting stock.
* Recording waste.
* Cancelling an order.
* Processing a refund.
* Recording an expense.
* Changing a recipe.
* Changing a selling price.
* Managing users and permissions.

This requirement will be implemented through audit logging.

---

# 2.21 Business Constraints

The system must respect the following constraints:

1. It is an internal staff system.
2. Only authorized users can access protected functionality.
3. Different staff members have different responsibilities.
4. Expired stock must not be used as normal inventory.
5. Inventory changes must be traceable.
6. Recipe quantities determine ingredient requirements.
7. An ingredient can be shared by multiple menu products.
8. Stock may exist in multiple batches.
9. Different batches may have different expiry dates.
10. Financial records must remain traceable to their source transactions.
11. Historical business transactions should not be lost simply because a related user or product becomes inactive.

---

# 2.22 Expected Business Benefits

After implementation, Board’s Cafe should be able to:

* Know its current inventory position.
* Identify stock approaching expiry.
* Reduce expired stock.
* Understand ingredient consumption.
* Improve purchasing decisions.
* Track customer orders.
* Improve communication between front staff and kitchen staff.
* Track payments.
* Monitor expenses.
* Measure waste.
* Analyze sales.
* Improve staff accountability.
* Make decisions using centralized business information.

---

# 2.23 Business Success Criteria

The system should be considered successful when Board’s Cafe can perform the following core process reliably:

```text
Staff Login
    ↓
Create Customer Order
    ↓
Select Menu Products
    ↓
Confirm Order
    ↓
Kitchen Preparation
    ↓
Determine Required Ingredients
    ↓
Select Valid Inventory Batches
    ↓
Consume Ingredients
    ↓
Complete Order
    ↓
Record Payment
    ↓
Update Stock
    ↓
Update Reports
```

At the same time, the system should continuously monitor:

```text
Low Stock
     +
Expiring Soon
     +
Expired Stock
     +
Waste
     +
Purchases
     +
Expenses
     +
Sales
```

The overall objective is to give Board’s Cafe better control over its operations while reducing avoidable stock and financial losses.
