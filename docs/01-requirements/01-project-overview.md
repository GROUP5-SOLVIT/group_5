# Board’s Cafe Management System

## 1. Project Overview

### 1.1 Project Name

**Board’s Cafe Management System**

### 1.2 Project Type

Internal web-based cafe management and Point of Sale (POS) system.

### 1.3 Purpose

The Board’s Cafe Management System is designed to help cafe staff manage daily operations from one centralized system.

The system will connect sales, customer orders, menu products, recipes, ingredients, inventory, batches, expiry dates, purchases, suppliers, expenses, payments, waste, reports, notifications, users, roles, and audit activities.

The main goal is to reduce manual work, improve stock control, reduce losses caused by expired products, improve order processing, and give management a clear view of the cafe's performance.

### 1.4 Background

Cafe operations involve several activities that are closely connected.

A customer places an order for one or more menu items. Staff records the order, the kitchen prepares the requested items, and the customer pays for the order.

Behind this process, the cafe must also manage the ingredients used to prepare those menu items.

For example, a cappuccino may require:

* Milk
* Coffee
* Sugar

A pancake may require:

* Flour
* Milk
* Sugar
* Eggs

Therefore, selling a menu item should be connected to the ingredients required to prepare it.

The system should be able to determine how much stock is consumed when menu items are prepared.

The system must also track inventory batches and expiry dates because the same ingredient may be purchased several times and each purchase may have a different batch number, quantity, cost, and expiry date.

### 1.5 Problem Statement

Managing cafe operations manually can make it difficult to know:

* How much stock is currently available.
* Which ingredients are running low.
* Which products are approaching their expiry dates.
* Which products have already expired.
* How much stock was consumed to prepare sold products.
* How much money was spent purchasing stock.
* How much money was lost through expired or wasted products.
* Which menu items are selling the most.
* How much revenue the cafe generates.
* How much the cafe spends on expenses.
* Which employees performed particular transactions.
* Whether inventory records match actual business activity.

Expired products can result in unnecessary financial losses, particularly for products such as milk, yoghurt, bread, juice, and other perishable ingredients.

The system should therefore not only record expired stock but also help staff identify products approaching expiry so that appropriate action can be taken before the products become unusable.

### 1.6 Proposed Solution

Board’s Cafe Management System will provide a centralized platform for managing cafe operations.

The system will provide:

1. Secure staff authentication.
2. User and role management.
3. Permission-based access control.
4. Dashboard and business summaries.
5. POS and order management.
6. Menu product management.
7. Recipe management.
8. Ingredient and inventory management.
9. Batch and expiry tracking.
10. Purchase and supplier management.
11. Expense management.
12. Payment management.
13. Waste management.
14. Reports and analytics.
15. Notifications and alerts.
16. Audit logging.

### 1.7 Target Users

The system is intended for internal cafe staff.

Potential users include:

* Administrator / Owner
* Manager
* Cashier
* Waiter
* Kitchen Staff
* Storekeeper

The exact permissions of each role will be defined in the Roles and Permissions document.

### 1.8 System Scope

The first version of the system will focus on the internal operations of Board’s Cafe.

The system will cover:

**Sales**

* Creating orders
* Managing order items
* Processing payments
* Completing sales
* Viewing sales history
* Cancelling permitted orders
* Handling permitted refunds

**Menu**

* Creating menu products
* Editing menu products
* Managing categories
* Setting selling prices
* Managing recipes

**Inventory**

* Managing ingredients
* Recording stock
* Tracking stock quantities
* Tracking stock movements
* Monitoring low stock
* Tracking inventory batches
* Tracking expiry dates

**Purchases**

* Managing suppliers
* Recording purchases
* Recording purchased quantities
* Recording batch numbers
* Recording expiry dates
* Recording purchase costs

**Expenses**

* Recording business expenses
* Categorizing expenses
* Tracking expenses over time

**Waste**

* Recording expired stock
* Recording damaged stock
* Recording other stock losses
* Calculating estimated financial loss

**Reporting**

* Sales reports
* Inventory reports
* Purchase reports
* Expense reports
* Waste reports
* Profit-related reports
* Expiry reports

**Administration**

* Managing users
* Managing roles
* Managing permissions
* Activating/deactivating users
* Reviewing audit logs

### 1.9 Main Business Principle

The system will connect the cafe's sales activity to its inventory activity.

The core relationship is:

```text
Customer Order
      ↓
Menu Product
      ↓
Recipe
      ↓
Required Ingredients
      ↓
Inventory
      ↓
Stock Consumption
```

For example:

```text
2 Cappuccinos
+
1 Pancake
```

may result in the system calculating:

```text
Milk     → 450 ml
Coffee   → 40 g
Sugar    → 40 g
Flour    → 100 g
Egg      → 1
```

The exact quantities will come from the configured recipes.

### 1.10 Made-to-Order Principle

Board’s Cafe may prepare food or drinks after a customer places an order.

Therefore, the system will primarily support a **made-to-order workflow** rather than requiring all menu products to be produced and stored in advance.

The primary flow will be:

```text
Customer
   ↓
Order
   ↓
Kitchen receives order
   ↓
Preparation starts
   ↓
Required ingredients are consumed
   ↓
Item becomes ready
   ↓
Order completed
   ↓
Payment recorded
```

The exact point at which inventory consumption occurs will be defined in the Business Workflows document.

### 1.11 Expiry Management Principle

Expiry will be tracked at the **inventory batch level** rather than only at the product level.

For example:

```text
Milk

Batch M001
20 Litres
Expiry: 10 October

Batch M002
30 Litres
Expiry: 25 October
```

The system must therefore be able to distinguish between the two batches.

The system should:

* identify expired batches;
* identify batches approaching expiry;
* alert authorized staff;
* prevent expired stock from being consumed;
* prioritize valid stock with the earliest expiry date;
* record expired stock as waste when appropriate.

### 1.12 Inventory Consumption Principle

When a menu item is prepared, the system should determine the ingredients required from its recipe.

For example:

```text
Cappuccino
├── Milk       150 ml
├── Coffee      20 g
└── Sugar       10 g
```

If two cappuccinos are prepared:

```text
Milk       300 ml
Coffee      40 g
Sugar       20 g
```

The system should then record the corresponding inventory consumption.

### 1.13 System Design Approach

The Board’s Cafe Management System will be designed as an integrated internal platform for managing the cafe’s daily operations.

The system will bring together sales, customer orders, menu products, recipes, ingredients, inventory, stock batches, expiry management, purchases, suppliers, expenses, payments, waste, reporting, notifications, user management, roles, permissions, and audit activities within one system.

The design will focus on the actual operational needs of Board’s Cafe and will provide role-based access so that each staff member can access only the functions and information required for their responsibilities.

The system will also maintain relationships between customer orders, menu products, recipes, ingredients, inventory consumption, stock batches, expiry dates, and financial transactions to provide consistent and traceable business records.

The database structure, workflows, permissions, user interface, and technical implementation will be developed specifically according to Board’s Cafe’s requirements.

### 1.14 Expected Benefits

The system is expected to help Board’s Cafe:

* Reduce manual record keeping.
* Improve inventory accuracy.
* Reduce expired stock.
* Identify products approaching expiry.
* Reduce unnecessary stock losses.
* Understand ingredient consumption.
* Process customer orders more efficiently.
* Improve payment tracking.
* Monitor expenses.
* Understand sales performance.
* Improve accountability among staff.
* Provide management with useful reports.
* Make business decisions using accurate records.

### 1.15 High-Level System Architecture

At a high level:

```text
                    BOARD'S CAFE
                         │
        ┌────────────────┼────────────────┐
        │                │                │
      STAFF             POS           MANAGEMENT
        │                │                │
        ↓                ↓                ↓
 Authentication       Orders         Dashboard
 Users                 Payments       Reports
 Roles                 Receipts       Analytics
 Permissions
        │
        └───────────────┬────────────────┘
                        ↓
                  BUSINESS LOGIC
                        │
       ┌────────────────┼────────────────┐
       ↓                ↓                ↓
    Products         Inventory        Purchases
    Recipes          Batches          Suppliers
       │             Expiry
       └──────────────┬─────────────────┘
                      ↓
                 FINANCIAL DATA
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       Sales       Expenses      Waste
          │           │           │
          └───────────┼───────────┘
                      ↓
                  REPORTS
```

### 1.16 Success Criteria

The project will be considered successful when the system can reliably support the core cafe workflow:

```text
User Login
    ↓
Create Customer Order
    ↓
Select Menu Products
    ↓
Calculate Order Total
    ↓
Send Order for Preparation
    ↓
Determine Required Ingredients
    ↓
Consume Valid Inventory
    ↓
Complete Order
    ↓
Record Payment
    ↓
Update Inventory
    ↓
Update Reports
```

The system should also be able to detect:

```text
Low Stock
Expiring Soon
Expired Stock
Waste
Unusual Stock Movements
```

and make the relevant information available to authorized staff.

