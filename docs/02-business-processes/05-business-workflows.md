# Board’s Cafe Management System

# 05 — Business Workflows

## 5.1 Introduction

This document defines the main business workflows supported by the Board’s Cafe Management System.

The workflows describe how daily activities are performed inside Board’s Cafe and how different system modules interact with each other.

The system is designed for **internal staff use**. Different staff members perform different activities according to their assigned roles and permissions.

The main operational flow is:

```text
Purchase / Receive Stock
          ↓
      Inventory
          ↓
       Batches
          ↓
   Expiry Monitoring
          ↓
     Recipe / BOM
          ↓
      Customer Order
          ↓
       Production
          ↓
 Ingredient Consumption
          ↓
     Order Completion
          ↓
        Payment
          ↓
       Reporting
```

The system shall maintain traceability between these activities.

---

# 5.2 Main Business Areas

The main workflows are:

1. User and access management
2. Product and recipe setup
3. Supplier and purchasing
4. Stock receiving
5. Inventory and batch management
6. Expiry monitoring
7. Customer order
8. Production and preparation
9. Ingredient consumption
10. Payment
11. Order cancellation
12. Refund
13. Waste management
14. Stock adjustment
15. Low-stock management
16. Reporting
17. Audit logging

---

# 5.3 User Creation and Role Assignment Workflow

### Purpose

To allow an authorized administrator to create staff accounts and assign appropriate responsibilities.

### Actors

* Administrator

### Workflow

```text
Administrator
     ↓
Open User Management
     ↓
Create User
     ↓
Enter Staff Information
     ↓
Select Role
     ↓
System Validates Information
     ↓
Create Account
     ↓
Assign Role
     ↓
Account Becomes Active
```

### Steps

1. Administrator opens the User Management module.
2. Administrator selects **Create User**.
3. Administrator enters the staff member's information.
4. Administrator selects an appropriate role.
5. System validates the information.
6. System creates the user account.
7. System associates the selected role with the user.
8. System records the action in the audit log.

### Result

The staff member can log in and access functions permitted by the assigned role.

---

# 5.4 User Login Workflow

### Actors

* All system users

### Workflow

```text
Staff Member
     ↓
Enter Credentials
     ↓
System Validates Credentials
     ↓
Account Active?
   ↙       ↘
 YES       NO
  ↓         ↓
Login     Reject
  ↓
Load Permissions
  ↓
Dashboard
```

### Steps

1. Staff member enters their credentials.
2. System validates the credentials.
3. System verifies that the account is active.
4. System identifies the user's role.
5. System loads the permissions associated with the role.
6. System grants access to authorized functions.
7. System displays the appropriate dashboard.

---

# 5.5 Product Setup Workflow

### Purpose

To create the menu products sold by Board’s Cafe.

### Actors

* Administrator
* Manager
* Authorized staff

### Workflow

```text
Authorized Staff
       ↓
Create Category
       ↓
Create Menu Product
       ↓
Enter Price
       ↓
Set Availability
       ↓
Save Product
```

### Steps

1. Authorized staff creates or selects a category.
2. Staff creates a menu product.
3. Staff enters the product name.
4. Staff enters the selling price.
5. Staff provides other relevant information.
6. Staff sets the product as active/available.
7. System saves the product.

Example:

```text
Category: Breakfast

Products:
- Pancakes
- Omelette
- French Toast
```

---

# 5.6 Recipe Creation Workflow

### Purpose

To define the ingredients required to prepare a menu product.

### Actors

* Administrator
* Manager
* Authorized kitchen/production staff

### Workflow

```text
Menu Product
      ↓
Create Recipe
      ↓
Select Ingredient
      ↓
Enter Quantity
      ↓
Select Unit
      ↓
Add More Ingredients
      ↓
Save Recipe
```

### Example

For a cup of coffee:

```text
Coffee
 ├── Coffee Beans → 15 g
 ├── Milk        → 100 ml
 └── Sugar       → 5 g
```

For pancakes:

```text
Pancakes
 ├── Wheat Flour → 100 g
 ├── Milk        → 80 ml
 ├── Eggs        → 1 piece
 └── Sugar       → 10 g
```

### Important Rule

The same ingredient may be used by many products.

```text
Milk
 ├── Coffee
 ├── Tea
 ├── Pancakes
 ├── Cake
 └── Other Products
```

The inventory system shall therefore treat **Milk as one inventory item** rather than creating a separate milk stock record for every recipe.

---

# 5.7 Supplier Creation Workflow

### Actors

* Administrator
* Manager
* Authorized procurement/store staff

### Workflow

```text
Authorized Staff
      ↓
Create Supplier
      ↓
Enter Supplier Information
      ↓
Save Supplier
```

Supplier information may include:

* Supplier name
* Contact person
* Telephone
* Email
* Address
* Notes
* Active status

---

# 5.8 Purchase Workflow

### Purpose

To record goods purchased from suppliers.

### Actors

* Manager
* Storekeeper
* Authorized staff

### Workflow

```text
Identify Required Stock
          ↓
Create Purchase
          ↓
Select Supplier
          ↓
Add Items
          ↓
Enter Quantities & Costs
          ↓
Submit / Approve
          ↓
Receive Stock
```

### Steps

1. Staff identifies stock that needs to be purchased.
2. Staff selects a supplier.
3. Staff creates a purchase.
4. Staff adds purchased items.
5. Staff enters quantities.
6. Staff records applicable costs.
7. Purchase is submitted or approved according to permissions.
8. Stock is received when delivered.

---

# 5.9 Stock Receiving Workflow

### Purpose

To record inventory when purchased goods arrive at the cafe.

### Actors

* Storekeeper
* Manager
* Authorized staff

### Workflow

```text
Supplier Delivery
       ↓
Check Delivered Items
       ↓
Check Quantity
       ↓
Check Condition
       ↓
Record Batch
       ↓
Record Expiry Date
       ↓
Record Cost
       ↓
Receive Stock
       ↓
Inventory Updated
```

### Steps

1. Supplier delivers goods.
2. Storekeeper checks the delivered items.
3. Storekeeper checks quantities.
4. Storekeeper checks product condition.
5. Storekeeper records the received stock.
6. System creates or records the relevant batch.
7. Staff records the expiry date where applicable.
8. System records the quantity.
9. System updates inventory.
10. System records the stock movement.

---

# 5.10 Batch Creation Workflow

Each received batch shall be traceable.

Example:

```text
Inventory Item:
Milk

Batch:
MILK-2026-001

Received:
07 October 2026

Quantity:
50 L

Expiry:
15 October 2026

Unit Cost:
2,000 RWF/L
```

The system shall allow another batch of the same product to exist:

```text
Milk
 ├── Batch A → Expires 15 Oct
 ├── Batch B → Expires 20 Oct
 └── Batch C → Expires 30 Oct
```

This is important because stock with the same product name can have different expiry dates.

---

# 5.11 Inventory Monitoring Workflow

The system shall continuously provide information about available stock.

```text
Inventory
    ↓
Check Quantities
    ↓
Check Batch Status
    ↓
Check Expiry
    ↓
Check Minimum Level
    ↓
Generate Status / Alerts
```

The system should identify:

* Available stock
* Low stock
* Expiring-soon stock
* Expired stock
* Depleted batches
* Blocked batches

---

# 5.12 Expiry Monitoring Workflow

### Purpose

To help Board’s Cafe reduce losses caused by expired stock.

### Workflow

```text
Batch
  ↓
Check Expiry Date
  ↓
Calculate Days Remaining
  ↓
Is Expired?
 ┌──────┴──────┐
YES            NO
 ↓              ↓
Expired      Days Remaining
Stock            ↓
              Within Warning
              Period?
             ┌────┴────┐
            YES        NO
             ↓          ↓
          Alert       Normal
```

### Example

If the warning period is 3 days:

```text
Expiry Date: 10 October
Current Date: 7 October

Days Remaining = 3

Status = Expiring Soon
```

If:

```text
Expiry Date: 5 October
Current Date: 7 October

Status = Expired
```

---

# 5.13 Expired Stock Workflow

When a batch expires:

```text
Batch
  ↓
Expiry Date Passed
  ↓
System Marks Batch Expired
  ↓
Normal Consumption Blocked
  ↓
Staff Notified
  ↓
Staff Inspects Stock
  ↓
Record Waste
  ↓
Inventory Updated
```

The system shall not allow expired stock to be consumed normally in production.

---

# 5.14 Expiring-First / FEFO Workflow

Where applicable, the system shall follow **First-Expire, First-Out (FEFO)**.

Example:

```text
Milk Stock

Batch A → 10 L → Expires 10 Oct
Batch B → 20 L → Expires 15 Oct
Batch C → 15 L → Expires 20 Oct
```

If production requires 8 L:

```text
Use Batch A first.
```

If production requires 15 L:

```text
Batch A → 10 L
Batch B → 5 L
```

This reduces the probability of leaving older stock unused until it expires.

---

# 5.15 Customer Order Workflow

### Actors

* Waiter
* Cashier
* Authorized staff

### Workflow

```text
Customer
   ↓
Place Order
   ↓
Staff Creates Order
   ↓
Select Products
   ↓
Enter Quantities
   ↓
Calculate Total
   ↓
Confirm Order
   ↓
Send to Kitchen / Production
```

### Steps

1. Customer places an order.
2. Waiter or Cashier creates the order.
3. Staff selects the requested menu products.
4. Staff enters quantities.
5. System calculates the order total.
6. Staff confirms the order.
7. System assigns the appropriate status.
8. Order becomes available to the kitchen/production staff.

---

# 5.16 Production-on-Order Workflow

Board’s Cafe may prepare certain products **when a customer places an order** rather than producing every product in advance.

This workflow is important for products that require fresh ingredients.

```text
Customer Order
      ↓
Order Confirmed
      ↓
Check Recipe
      ↓
Determine Ingredients
      ↓
Check Available Valid Batches
      ↓
Ingredients Available?
   ┌──────┴───────┐
  YES             NO
   ↓               ↓
Production      Notify Staff
   ↓
Consume Ingredients
   ↓
Prepare Product
   ↓
Mark Ready
   ↓
Complete Order
```

---

# 5.17 Ingredient Requirement Calculation

When an order is confirmed, the system shall determine the ingredients required.

Example:

```text
Product: Pancakes

Recipe:
Flour = 100 g
Milk  = 80 ml
Egg   = 1
Sugar = 10 g
```

Customer orders:

```text
Pancakes × 3
```

The system calculates:

```text
Flour = 100 g × 3 = 300 g
Milk  = 80 ml × 3 = 240 ml
Egg   = 1 × 3 = 3 eggs
Sugar = 10 g × 3 = 30 g
```

These quantities become the expected ingredient consumption for the production.

---

# 5.18 Shared Ingredient Consumption

If multiple ordered products use the same ingredient, the system shall calculate the combined requirement.

Example:

```text
Order:

2 × Pancakes
1 × Coffee
```

Recipes:

```text
Pancakes:
Milk = 80 ml

Coffee:
Milk = 100 ml
```

Total milk requirement:

```text
(80 × 2) + 100
= 260 ml
```

The system should therefore consume:

```text
Milk = 260 ml
```

rather than treating the two requirements as unrelated stock operations.

---

# 5.19 Production Stock Check

Before production begins, the system should verify that sufficient valid stock exists.

Example:

```text
Required:
Milk = 260 ml

Available:
Batch A = 500 ml
Expiry = Future

Result:
Available
```

If:

```text
Required:
Milk = 260 ml

Valid Available:
Milk = 150 ml

Expired:
Milk = 500 ml
```

The system must not count the expired 500 ml as usable stock.

Result:

```text
Insufficient Valid Stock
```

Staff should then be notified so the appropriate action can be taken.

---

# 5.20 Production Workflow

### Actors

* Kitchen Staff

### Workflow

```text
Confirmed Order
      ↓
Kitchen Receives Order
      ↓
Start Preparation
      ↓
View Recipe / Preparation Information
      ↓
Check Ingredients
      ↓
Prepare Product
      ↓
Report Problems if Necessary
      ↓
Mark Ready
```

The kitchen staff shall be able to see the orders that require preparation.

---

# 5.21 Ingredient Consumption Workflow

When the defined production/consumption event occurs:

```text
Order
  ↓
Recipe
  ↓
Calculate Required Ingredients
  ↓
Select Valid Batches
  ↓
Apply FEFO
  ↓
Reduce Batch Quantities
  ↓
Create Consumption Record
  ↓
Create Stock Movement
```

For example:

```text
Milk Batch A
Available = 10 L

Production requires:
2 L

After consumption:
Batch A = 8 L
```

The system shall retain the consumption record for traceability.

---

# 5.22 Important Production Rule

The system should clearly distinguish between:

### Menu Product

Something the customer orders.

Examples:

```text
Cappuccino
Pancakes
Burger
Cake
Fresh Juice
```

### Inventory Ingredient

Something used to make another product.

Examples:

```text
Milk
Wheat Flour
Eggs
Sugar
Coffee Beans
Cooking Oil
```

An inventory ingredient may be used by multiple menu products.

Therefore:

```text
Milk
   ├── Cappuccino
   ├── Latte
   ├── Pancakes
   └── Cake
```

This relationship shall be represented in the database through recipes.

---

# 5.23 Payment Workflow

### Actors

* Cashier
* Authorized Manager

### Workflow

```text
Completed / Payable Order
        ↓
Calculate Amount
        ↓
Select Payment Method
        ↓
Enter Payment
        ↓
Validate Amount
        ↓
Record Payment
        ↓
Update Payment Status
        ↓
Receipt
```

Supported payment methods can include those configured by Board’s Cafe.

---

# 5.24 Order Completion Workflow

```text
Order Confirmed
      ↓
Preparation
      ↓
Product Ready
      ↓
Customer Receives Order
      ↓
Payment Confirmed
      ↓
Order Completed
```

The exact order of payment and preparation may vary depending on the cafe's operational policy.

---

# 5.25 Order Cancellation Workflow

### Workflow

```text
Order
  ↓
Cancel Request
  ↓
Check Permission
  ↓
Cancellation Allowed?
 ┌──────┴──────┐
YES           NO
 ↓             ↓
Cancel       Reject
 ↓
Check Consumption
 ↓
Reverse / Adjust
where applicable
 ↓
Audit Log
```

If ingredients have already been consumed, cancellation should not simply erase the consumption history.

The system should handle the appropriate stock correction through a controlled transaction.

---

# 5.26 Refund Workflow

```text
Completed Payment
      ↓
Refund Request
      ↓
Check Permission
      ↓
Check Refund Conditions
      ↓
Approve Refund
      ↓
Record Refund
      ↓
Update Payment Status
      ↓
Audit Log
```

Refund operations should be restricted to authorized staff.

---

# 5.27 Waste Management Workflow

Waste can originate from different situations.

Examples:

* Expired ingredients
* Spoiled ingredients
* Damaged goods
* Preparation mistakes
* Accidental loss
* Other operational causes

### Workflow

```text
Identify Waste
     ↓
Select Item / Batch
     ↓
Enter Quantity
     ↓
Select Reason
     ↓
Submit Waste
     ↓
Approval if Required
     ↓
Reduce Inventory
     ↓
Create Stock Movement
     ↓
Audit Record
```

---

# 5.28 Expired Product Waste Workflow

This is a key workflow for the system.

```text
Batch Approaches Expiry
          ↓
System Alert
          ↓
Staff Reviews Stock
          ↓
Can It Be Used Before Expiry?
       ┌──────┴──────┐
      YES            NO
       ↓              ↓
Prioritize          Monitor
Usage                ↓
                 Expiry Date
                     ↓
                  Expires
                     ↓
                Block Usage
                     ↓
                Record Waste
```

The purpose is not simply to report expired products.

The system should help staff **identify stock early enough to use it before expiry**.

---

# 5.29 Low Stock Workflow

```text
Inventory Quantity
       ↓
Compare with
Minimum Stock Level
       ↓
Below Threshold?
   ┌──────┴──────┐
  YES            NO
   ↓              ↓
Alert           Normal
   ↓
Staff Reviews
   ↓
Create Purchase
```

Example:

```text
Milk

Current Stock = 5 L
Minimum Level = 10 L

Status = Low Stock
```

The system should notify the appropriate staff.

---

# 5.30 Stock Adjustment Workflow

Stock adjustments shall be controlled because they affect inventory accuracy.

```text
Identify Difference
       ↓
Create Adjustment
       ↓
Enter Quantity Difference
       ↓
Enter Reason
       ↓
Approval if Required
       ↓
Update Inventory
       ↓
Create Stock Movement
       ↓
Audit Log
```

Possible reasons include:

* Physical stock count
* Data correction
* Damaged stock
* Missing stock
* Counting error
* Other approved reason

---

# 5.31 Physical Stock Count Workflow

```text
Select Inventory
      ↓
Count Physical Stock
      ↓
Compare With System Quantity
      ↓
Difference?
   ┌────┴────┐
  YES        NO
   ↓          ↓
Adjustment   Confirm
   ↓
Record Reason
   ↓
Approval if Required
   ↓
Update Stock
```

---

# 5.32 Inventory Transfer Workflow

If Board’s Cafe operates multiple stock locations in the future, the system should support controlled stock transfers.

```text
Source Location
      ↓
Transfer Request
      ↓
Select Item / Batch
      ↓
Enter Quantity
      ↓
Approve
      ↓
Remove From Source
      ↓
Add To Destination
      ↓
Record Transfer
```

This workflow can remain optional until multiple locations are required.

---

# 5.33 Expense Workflow

### Actors

* Manager
* Administrator
* Authorized staff

```text
Expense Occurs
      ↓
Record Expense
      ↓
Select Category
      ↓
Enter Amount
      ↓
Enter Description
      ↓
Submit
      ↓
Approval if Required
      ↓
Expense Recorded
```

---

# 5.34 Report Generation Workflow

```text
User
 ↓
Select Report
 ↓
Select Date Range
 ↓
Apply Filters
 ↓
System Retrieves Data
 ↓
Calculate Results
 ↓
Display Report
 ↓
Export if Permitted
```

Examples:

* Daily sales report
* Monthly sales report
* Inventory report
* Expiry report
* Waste report
* Purchase report
* Expense report
* Payment report
* Ingredient consumption report

---

# 5.35 Daily Operations Workflow

A typical Board’s Cafe operating day may follow this structure:

```text
                    START DAY
                       │
                       ▼
                Check Dashboard
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Low Stock    Expiring      Orders
                       Stock
          │            │
          ▼            ▼
       Purchase     Prioritize
       Planning      Usage
                       │
                       ▼
                Customer Orders
                       │
                       ▼
                 Kitchen / Production
                       │
                       ▼
              Ingredient Consumption
                       │
                       ▼
                  Order Ready
                       │
                       ▼
                    Payment
                       │
                       ▼
               Order Completed
                       │
                       ▼
                Stock Updated
                       │
                       ▼
                Waste Recorded
                 if applicable
                       │
                       ▼
                End-of-Day Reports
```

---

# 5.36 End-of-Day Workflow

At the end of the business day, authorized staff may perform:

1. Review completed orders.
2. Review payments.
3. Review inventory changes.
4. Review low-stock items.
5. Review expiring stock.
6. Record any waste.
7. Review expenses.
8. Review stock discrepancies.
9. Review important notifications.
10. Generate or view daily reports.

---

# 5.37 End-of-Day Inventory Review

```text
End of Day
    ↓
Review Inventory
    ↓
Check Low Stock
    ↓
Check Expiring Stock
    ↓
Check Expired Stock
    ↓
Check Waste
    ↓
Check Stock Adjustments
    ↓
Review Inventory Report
```

---

# 5.38 Audit Workflow

Important actions shall generate audit records.

```text
Staff Performs Action
        ↓
Permission Check
        ↓
Action Executed
        ↓
Audit Event Created
        ↓
Store:
- User
- Action
- Resource
- Date/Time
- Relevant Details
```

Examples of actions that should be audited:

* User creation
* Role assignment
* Permission changes
* Product price changes
* Recipe changes
* Stock adjustments
* Stock receiving
* Waste recording
* Refunds
* Expense approval
* Batch blocking
* Other sensitive operations

---

# 5.39 Notification Workflow

Notifications may be generated automatically by the system.

```text
System Event
     ↓
Evaluate Rule
     ↓
Condition Met?
  ┌────┴────┐
 YES        NO
  ↓          ↓
Create      Nothing
Alert
  ↓
Notify Staff
  ↓
Staff Views
  ↓
Mark as Read
```

Examples:

```text
Milk expires in 2 days
        ↓
Expiry Alert

Flour below minimum level
        ↓
Low Stock Alert

New customer order
        ↓
Kitchen Notification
```

---

# 5.40 Automated Expiry Monitoring

The system should periodically check inventory batches.

Conceptually:

```text
Scheduled Check
      ↓
Find Active Batches
      ↓
Check Expiry Dates
      ↓
Update Status
      ↓
Generate Alerts
      ↓
Notify Authorized Staff
```

The system should not depend entirely on a staff member manually checking every expiry date.

---

# 5.41 Complete Order-to-Inventory Workflow

This is one of the most important workflows in the Board’s Cafe system.

```text
                 CUSTOMER
                    │
                    ▼
               PLACE ORDER
                    │
                    ▼
              CREATE ORDER
                    │
                    ▼
             CONFIRM ORDER
                    │
                    ▼
             READ RECIPE
                    │
                    ▼
       CALCULATE INGREDIENTS
                    │
                    ▼
          CHECK VALID BATCHES
                    │
                    ▼
             APPLY FEFO
                    │
                    ▼
              PRODUCTION
                    │
                    ▼
         CONSUME INGREDIENTS
                    │
                    ├───────────────┐
                    ▼               ▼
             UPDATE BATCH       STOCK MOVEMENT
                    │
                    ▼
              ORDER READY
                    │
                    ▼
                 PAYMENT
                    │
                    ▼
             ORDER COMPLETED
                    │
                    ▼
                REPORTING
```

---

# 5.42 Complete Purchase-to-Inventory Workflow

```text
Supplier
   ↓
Purchase Order / Purchase
   ↓
Supplier Delivery
   ↓
Receive Stock
   ↓
Create Batch
   ↓
Record Quantity
   ↓
Record Expiry
   ↓
Record Cost
   ↓
Update Inventory
   ↓
Create Stock Movement
   ↓
Expiry Monitoring
```

---

# 5.43 Complete Expiry-to-Waste Workflow

```text
Inventory Batch
      ↓
Expiry Monitoring
      ↓
Approaching Expiry
      ↓
Alert Staff
      ↓
Prioritize Consumption
      │
      ├───────────────► Used in Production
      │
      └── If Not Used
              ↓
           Expires
              ↓
        Block Normal Use
              ↓
        Record Waste
              ↓
       Reduce Inventory
              ↓
       Stock Movement
              ↓
        Waste Report
```

---

# 5.44 Exception Handling

The system shall handle situations where the normal workflow cannot continue.

### Example 1 — Insufficient Ingredients

```text
Order
 ↓
Recipe
 ↓
Check Stock
 ↓
Insufficient Stock
 ↓
Notify Staff
```

The order should not silently consume unavailable stock.

### Example 2 — Expired Ingredient

```text
Recipe
 ↓
Check Batch
 ↓
Batch Expired
 ↓
Do Not Consume
 ↓
Find Another Valid Batch
```

### Example 3 — No Valid Batch

```text
Required Ingredient
        ↓
No Valid Batch
        ↓
Production Cannot Continue Normally
        ↓
Notify Authorized Staff
```

### Example 4 — Payment Failure

```text
Order
 ↓
Payment Attempt
 ↓
Payment Failed
 ↓
Payment Remains Unpaid
 ↓
Order Follows Configured Policy
```

### Example 5 — Stock Discrepancy

```text
Physical Count
      ↓
Different From System
      ↓
Adjustment Required
      ↓
Authorized Adjustment
      ↓
Audit Record
```

---

# 5.45 Business Workflow Principles

The Board’s Cafe system shall follow these principles:

### Principle 1 — Traceability

Important inventory and financial activities should be traceable to the staff member and business transaction responsible.

### Principle 2 — No Normal Consumption of Expired Stock

Expired batches must not be available for normal production consumption.

### Principle 3 — FEFO

Where applicable, stock with the earliest expiry should be consumed first.

### Principle 4 — Recipe-Based Consumption

Ingredient consumption should be determined from the configured recipe rather than manually guessing quantities.

### Principle 5 — Shared Ingredients

One inventory ingredient can be used in multiple menu products.

### Principle 6 — Controlled Adjustments

Direct inventory adjustments must be restricted and auditable.

### Principle 7 — Historical Records

Completed transactions should not be unnecessarily deleted.

### Principle 8 — Permission Enforcement

Every protected operation must be checked against the user's permissions.

### Principle 9 — Automated Monitoring

Expiry and low-stock conditions should be monitored automatically where possible.

### Principle 10 — Production on Demand

For products prepared after an order is placed, the system should connect the order to the required recipe and ingredient consumption.

---

# 5.46 Overall Business Process

The complete Board’s Cafe business process can be summarized as:

```text
                 ┌─────────────────┐
                 │    SUPPLIERS    │
                 └────────┬────────┘
                          │
                       PURCHASE
                          │
                          ▼
                 ┌─────────────────┐
                 │    INVENTORY    │
                 └────────┬────────┘
                          │
                       BATCHES
                          │
             ┌────────────┴────────────┐
             │                         │
          EXPIRY                    STOCK LEVEL
             │                         │
             ▼                         ▼
          ALERTS                   LOW STOCK
             │                         │
             ▼                         ▼
          PRIORITY                 PURCHASE
          USAGE
             │
             ▼
       ┌───────────────┐
       │    RECIPES    │
       └───────┬───────┘
               │
               │
          CUSTOMER ORDER
               │
               ▼
        ┌───────────────┐
        │  PRODUCTION   │
        └───────┬───────┘
                │
         INGREDIENT
         CONSUMPTION
                │
                ▼
           STOCK UPDATE
                │
                ▼
          ORDER COMPLETED
                │
          ┌─────┴─────┐
          ▼           ▼
       PAYMENT       WASTE
          │           │
          └─────┬─────┘
                ▼
             REPORTS
                │
                ▼
           AUDIT LOGS
```

---

# 5.47 Workflow-to-Module Relationship

| Workflow               | Main Module         |
| ---------------------- | ------------------- |
| Login                  | Authentication      |
| User creation          | User Management     |
| Role assignment        | Roles & Permissions |
| Product creation       | Products            |
| Recipe creation        | Recipes             |
| Supplier creation      | Suppliers           |
| Purchase               | Purchases           |
| Stock receiving        | Inventory           |
| Batch creation         | Batch Management    |
| Expiry monitoring      | Batch & Expiry      |
| Customer order         | POS / Orders        |
| Production             | Kitchen             |
| Ingredient consumption | Inventory           |
| Payment                | Payments            |
| Refund                 | Payments            |
| Waste                  | Waste Management    |
| Stock adjustment       | Inventory           |
| Expenses               | Expenses            |
| Notifications          | Notifications       |
| Reports                | Reports             |
| Audit trail            | Audit Logs          |

---

# 5.48 Final Workflow Model

The Board’s Cafe Management System is centered around the relationship between **sales, production, and inventory**.

The core operational cycle is:

```text
BUY
 ↓
RECEIVE
 ↓
STORE
 ↓
MONITOR
 ↓
ORDER
 ↓
PRODUCE
 ↓
CONSUME
 ↓
SELL
 ↓
PAY
 ↓
REPORT
```

At the same time, the system continuously works to reduce stock losses:

```text
STOCK
 ↓
BATCH
 ↓
EXPIRY MONITORING
 ↓
EARLY ALERT
 ↓
PRIORITY USAGE
 ↓
LESS WASTE
```

The system therefore does more than record sales. It connects customer orders with recipes and inventory consumption while continuously monitoring stock levels and expiry dates.
