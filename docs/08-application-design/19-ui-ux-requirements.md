# 19. UI/UX Requirements

## 19.1 Introduction

The Board’s Cafe system will provide a web-based interface for internal staff to manage cafe operations. The interface should be simple, clear, and easy to use because different staff members will use the system for different tasks such as taking orders, managing stock, recording purchases, monitoring expired products, recording expenses, and viewing reports.

The design should focus on practical daily operations rather than unnecessary visual complexity.

The interface must also respect the user's assigned role and permissions. Staff members should only see and access functions they are allowed to use.

---

## 19.2 UI/UX Objectives

The user interface should achieve the following objectives:

1. Make common cafe operations quick to perform.
2. Make stock levels easy to understand.
3. Make expired and soon-to-expire products easy to identify.
4. Reduce errors when entering orders, purchases, stock, and expenses.
5. Provide clear feedback after successful or unsuccessful operations.
6. Make important information visible from the dashboard.
7. Support role-based access.
8. Provide consistent navigation across the system.
9. Work properly on desktop and smaller screens where practical.
10. Keep the interface simple enough for staff who may not have advanced technical skills.

---

# 19.3 General Layout

The application should use a consistent layout across the main pages.

A typical layout will contain:

```text
+------------------------------------------------------+
| Board's Cafe                 User / Notifications    |
+-------------------+----------------------------------+
|                   |                                  |
| Dashboard         |                                  |
| POS / Orders      |          Main Content            |
| Products          |                                  |
| Recipes           |                                  |
| Inventory         |                                  |
| Purchases         |                                  |
| Suppliers         |                                  |
| Expenses          |                                  |
| Waste             |                                  |
| Reports           |                                  |
| Notifications     |                                  |
| Users & Roles     |                                  |
| Audit Logs        |                                  |
|                   |                                  |
+-------------------+----------------------------------+
```

The exact layout may be adjusted during implementation, but the main navigation should remain consistent.

---

# 19.4 Navigation

The main navigation should provide access to the system's major modules.

Recommended navigation:

* Dashboard
* POS / Orders
* Menu Products
* Recipes
* Inventory
* Batches & Expiry
* Purchases
* Suppliers
* Expenses
* Waste
* Reports
* Notifications
* Users & Roles
* Audit Logs

Items that the current user does not have permission to access should either be hidden or disabled.

For example, a cashier may see:

```text
Dashboard
POS / Orders
Orders
Notifications
```

while an administrator may see all available modules.

---

# 19.5 Login Page

The login page will be the main entry point into the system.

The page should contain:

* Board's Cafe name or branding
* Username or email field
* Password field
* Show/hide password option
* Login button
* Clear validation messages

Example:

```text
+----------------------------------+
|          Board's Cafe            |
|                                  |
|  Email / Username                |
|  [________________________]      |
|                                  |
|  Password                        |
|  [________________________]      |
|                                  |
|        [     Login     ]         |
|                                  |
+----------------------------------+
```

### Validation

The interface should clearly inform the user when:

* Required fields are empty.
* Login credentials are incorrect.
* The account is inactive.
* The server is unavailable.

Sensitive authentication information should not be displayed in error messages.

---

# 19.6 Dashboard

The dashboard should provide a quick overview of important cafe activities.

The information displayed should depend on the user's role and permissions.

Possible dashboard sections include:

### Sales Summary

* Today's sales
* Number of orders
* Paid orders
* Unpaid or partially paid orders

### Inventory Summary

* Total inventory items
* Low-stock items
* Expired batches
* Batches expiring soon
* Recent stock movements

### Purchase Summary

* Recent purchases
* Pending purchases
* Recently received stock

### Waste Summary

* Today's waste
* Recent waste records
* Expired stock recorded as waste

### Expenses

* Today's expenses
* Recent expenses
* Expense totals

### Alerts

Important alerts should be visible without requiring the user to search through the system.

Example:

```text
--------------------------------------------------
Today's Overview
--------------------------------------------------

Sales             Orders          Expenses
125,000 RWF       34              42,000 RWF

--------------------------------------------------
Inventory Alerts
--------------------------------------------------

⚠ 5 items are low in stock
⚠ 3 batches are expiring soon
⚠ 2 batches have expired

--------------------------------------------------
Recent Activity
--------------------------------------------------

Purchase received
Order completed
Stock adjustment
Waste recorded
```

---

# 19.7 POS / Order Interface

The POS interface should allow staff to create and manage customer orders efficiently.

The interface should make it easy to:

1. Select a menu product.
2. Enter quantity.
3. Add the product to the order.
4. View selected items.
5. Modify quantities.
6. Remove items.
7. View the order subtotal.
8. View the total amount.
9. Record payment.
10. Submit or complete the order.

Example:

```text
+-----------------------------+-----------------------+
| Menu Products               | Current Order         |
|                             |                       |
| [Burger]   [Tea]            | Burger x2    5,000    |
| [Coffee]   [Pizza]          | Tea x1        1,000   |
| [Juice]    [Sandwich]       |                       |
|                             | --------------------  |
|                             | Total:       6,000    |
|                             |                       |
|                             | [Pay] [Save] [Cancel]|
+-----------------------------+-----------------------+
```

The interface should prevent invalid quantities and should display clear confirmation before completing important actions where necessary.

---

# 19.8 Menu Product Interface

The menu product page should allow authorized users to manage products sold by the cafe.

The page should provide:

* Product name
* Category
* Selling price
* Description where applicable
* Availability/status
* Recipe information
* Created/updated information

Example table:

| Product  | Category |     Price | Status | Recipe |
| -------- | -------- | --------: | ------ | ------ |
| Coffee   | Drinks   | 1,000 RWF | Active | View   |
| Sandwich | Food     | 3,000 RWF | Active | View   |
| Juice    | Drinks   | 1,500 RWF | Active | View   |

Actions may include:

* Add product
* Edit product
* View product
* View recipe
* Deactivate product

Historical order records should not be affected when a product is deactivated.

---

# 19.9 Recipe Interface

The recipe interface should show the ingredients required to prepare a menu product.

Example:

```text
Product: Milk Tea

Recipe Ingredients
--------------------------------
Milk             250 ml
Tea               10 g
Sugar             15 g
--------------------------------
```

Authorized users should be able to:

* Create a recipe.
* Add ingredients.
* Edit ingredient quantities.
* Remove ingredients.
* View the complete recipe.

The interface should clearly display the unit used for each ingredient.

---

# 19.10 Inventory Interface

The inventory interface should provide a clear view of available stock.

Important information includes:

* Inventory item
* Category
* Unit
* Current quantity
* Minimum stock level
* Stock status
* Number of active batches

Example:

| Item        | Unit  | Current Stock | Minimum | Status |
| ----------- | ----- | ------------: | ------: | ------ |
| Milk        | Litre |            12 |      10 | Normal |
| Sugar       | Kg    |             4 |       8 | Low    |
| Wheat Flour | Kg    |            25 |      10 | Normal |
| Tomatoes    | Kg    |             3 |       5 | Low    |

The system should visually distinguish normal, low-stock, expired, and expiring-soon situations.

---

# 19.11 Batch & Expiry Interface

Because expiry is tracked at batch level, the user interface should make batch information easy to inspect.

The batch page should display:

* Inventory item
* Batch number
* Quantity received
* Remaining quantity
* Received date
* Expiry date
* Supplier/purchase reference
* Batch status

Example:

| Item   | Batch    | Remaining | Expiry Date | Status        |
| ------ | -------- | --------: | ----------- | ------------- |
| Milk   | MILK-001 |       5 L | 10 Oct 2026 | Expiring Soon |
| Yogurt | YOG-004  |    12 pcs | 08 Oct 2026 | Expired       |
| Flour  | FLR-010  |     20 Kg | 20 Dec 2026 | Normal        |

The interface should provide filters such as:

* All batches
* Active
* Expired
* Expiring soon
* Depleted

---

# 19.12 Expired Product Alerts

Expired stock is an important operational concern for Board's Cafe.

The system should make expired products highly visible to authorized staff.

For example:

```text
⚠ EXPIRED STOCK

Yogurt
Batch: YOG-004
Quantity: 12 pcs
Expired: 08 Oct 2026

[View Batch] [Record Waste]
```

The user should be able to open the batch details and record the expired stock as waste where appropriate.

Expired stock must not be available for normal recipe consumption.

---

# 19.13 FEFO Stock Selection

Where FEFO is applicable, the interface should not require staff to manually select the oldest-expiring batch during normal stock consumption.

The backend should determine the appropriate batch.

The interface may show information such as:

```text
Stock Consumption

Item: Milk
Required: 2 L

System will use:
Batch MILK-001
Expiry: 10 Oct 2026
Available: 5 L

[Confirm]
```

The purpose is to keep the process simple while still providing transparency when necessary.

---

# 19.14 Purchase Interface

The purchase interface should allow authorized users to record purchases and received stock.

A purchase form may include:

* Supplier
* Purchase date
* Reference number
* Items
* Quantity
* Unit cost
* Total cost
* Expiry date where applicable
* Batch number where applicable

When stock is received, the system should create the appropriate stock batch information.

Example:

```text
Supplier: ABC Foods

Item             Qty     Unit Cost
------------------------------------
Milk             20 L    900 RWF
Sugar            10 Kg   1,200 RWF

Total: 30,000 RWF

[Receive Stock]
```

---

# 19.15 Supplier Interface

The supplier page should provide:

* Supplier name
* Contact information
* Address where applicable
* Status
* Purchase history

Users with the appropriate permissions should be able to:

* Add supplier
* Edit supplier
* View supplier
* Deactivate supplier
* View purchase history

---

# 19.16 Expense Interface

The expense interface should provide a simple form for recording cafe expenses.

Fields may include:

* Expense category
* Amount
* Date
* Description
* Payment method where applicable
* Supporting reference where applicable

Example:

```text
Expense Category
[Electricity ▼]

Amount
[50,000]

Date
[08/10/2026]

Description
[Monthly electricity payment]

[Save Expense]
```

The interface should clearly display confirmation after an expense is successfully recorded.

---

# 19.17 Waste Interface

The waste interface should allow authorized users to record stock that can no longer be used.

Waste reasons may include:

* Expired
* Damaged
* Spoiled
* Spilled
* Preparation waste
* Other

Example:

```text
Record Waste

Item:       Milk
Batch:      MILK-003
Quantity:   2 L
Reason:     Expired
Notes:      Expired before use

[Record Waste]
```

Where waste is associated with a batch, the system should update the available stock correctly.

---

# 19.18 Notifications Interface

The notification area should display important system alerts.

Possible notifications include:

* Expired stock
* Stock expiring soon
* Low-stock items
* Purchase received
* Important system activity

Example:

```text
Notifications

● 3 milk batches are expiring soon.
● Sugar is below the minimum stock level.
● 2 batches have expired.
● Purchase #PO-104 has been received.
```

Users should be able to:

* View notifications
* Mark a notification as read
* Mark all notifications as read

---

# 19.19 Reports Interface

Reports should be presented in a readable format using tables, summary cards, and charts where useful.

Possible reports include:

### Sales Report

* Date
* Number of orders
* Total sales
* Paid amount
* Outstanding amount

### Inventory Report

* Item
* Current stock
* Low-stock status
* Batch information
* Expiry status

### Waste Report

* Item
* Quantity
* Reason
* Date
* Batch
* Recorded by

### Purchase Report

* Supplier
* Purchase
* Date
* Amount
* Received status

### Expense Report

* Category
* Amount
* Date
* Description

Reports should support useful filters such as:

* Date range
* Category
* Product
* Supplier
* Status

---

# 19.20 Users & Roles Interface

Administrators should have a dedicated interface for managing system users.

The user list should display:

* User name
* Username/email
* Role
* Account status
* Date created
* Last activity where available

Example:

| User  | Role              | Status |
| ----- | ----------------- | ------ |
| John  | Cashier           | Active |
| Alice | Inventory Manager | Active |
| Peter | Administrator     | Active |

Actions may include:

* Create user
* Edit user
* Assign role
* Change permissions where allowed
* Deactivate account

---

# 19.21 Audit Log Interface

Authorized administrators should be able to view important system activities.

Example:

| Date        | User  | Action            | Module    |
| ----------- | ----- | ----------------- | --------- |
| 08 Oct 2026 | John  | Created order     | Orders    |
| 08 Oct 2026 | Alice | Received purchase | Inventory |
| 08 Oct 2026 | Peter | Created user      | Users     |

The interface should support filtering by:

* User
* Action
* Module
* Date range

Sensitive information should not be unnecessarily exposed.

---

# 19.22 Forms and Validation

All forms should provide clear validation.

Validation messages should be:

* Short
* Specific
* Easy to understand
* Displayed close to the relevant field

Instead of:

```text
Invalid request.
```

Prefer:

```text
Quantity must be greater than 0.
```

For required fields:

```text
Supplier is required.
```

For invalid dates:

```text
Expiry date cannot be earlier than the purchase date.
```

---

# 19.23 Confirmation Messages

The system should provide feedback after important actions.

Examples:

```text
✓ Order created successfully.
```

```text
✓ Stock received successfully.
```

```text
✓ Expense recorded successfully.
```

```text
✓ Waste recorded successfully.
```

For destructive or irreversible actions, the system should request confirmation.

Example:

```text
Deactivate this product?

This product will no longer be available for new orders.

[Cancel] [Deactivate]
```

---

# 19.24 Search and Filtering

Major lists should provide search and filtering functionality.

Search may be available for:

* Products
* Inventory items
* Batches
* Suppliers
* Orders
* Users

Filters may include:

* Category
* Status
* Date
* Expiry status
* Supplier
* Payment status

Search and filtering should be simple enough for staff to use without technical knowledge.

---

# 19.25 Tables

Tables should be used when users need to review multiple records.

Tables should:

* Have clear column names.
* Use consistent formatting.
* Support pagination where necessary.
* Allow sorting where useful.
* Provide actions for individual records.
* Avoid displaying unnecessary information.

On smaller screens, tables should remain usable through responsive behavior such as horizontal scrolling or an alternative card layout.

---

# 19.26 Status Indicators

The system should use clear status labels.

Examples:

```text
Active
Inactive
Paid
Pending
Cancelled
Completed
Low Stock
Normal
Expired
Expiring Soon
Received
Partially Paid
```

Status should not rely only on color. The actual status text should also be displayed so that the information remains understandable.

---

# 19.27 Responsive Design

The application should primarily support desktop and laptop use because it is an internal staff management system.

However, important pages should also remain usable on smaller screens.

Responsive behavior should be considered for:

* Dashboard
* POS
* Inventory
* Orders
* Notifications
* Reports
* Forms

The interface should avoid requiring users to zoom in or out to perform normal operations.

---

# 19.28 Accessibility

The interface should follow basic accessibility principles.

The system should provide:

* Readable text.
* Clear labels.
* Keyboard-accessible controls where practical.
* Sufficient contrast.
* Visible focus states.
* Clear error messages.
* Labels for form fields.
* Icons accompanied by text where the icon alone may be unclear.

Important information such as expired stock should not be communicated through color alone.

---

# 19.29 Loading and Empty States

The application should clearly communicate when data is loading.

Example:

```text
Loading inventory...
```

When there are no records:

```text
No expired batches found.
```

For empty orders:

```text
No items have been added to this order yet.
```

These messages should help the user understand the current state instead of showing a blank screen.

---

# 19.30 Error Handling

If an operation fails, the interface should provide a useful message.

For example:

```text
Unable to save the order.
Please check the information and try again.
```

For inventory-related errors:

```text
Not enough available stock to complete this operation.
```

For expired stock:

```text
This batch has expired and cannot be used for normal consumption.
```

The interface should not expose technical errors, database details, stack traces, or other sensitive backend information to normal users.

---

# 19.31 Role-Based UI

The interface should reflect the user's permissions.

For example:

### Administrator

May access:

* Dashboard
* POS
* Products
* Recipes
* Inventory
* Purchases
* Suppliers
* Expenses
* Waste
* Reports
* Notifications
* Users & Roles
* Audit Logs

### Cashier

May primarily access:

* Dashboard
* POS
* Orders
* Notifications

### Inventory Staff

May primarily access:

* Dashboard
* Inventory
* Batches & Expiry
* Purchases
* Suppliers
* Waste
* Notifications

### Manager

May primarily access:

* Dashboard
* Orders
* Inventory
* Purchases
* Expenses
* Waste
* Reports
* Notifications

The final access available to each role must be controlled by the backend permission system rather than relying only on hiding frontend elements.

---

# 19.32 User Experience for Made-to-Order Products

For products prepared after an order is created, the interface should keep the process simple.

A typical flow is:

```text
Select Menu Product
        ↓
Enter Quantity
        ↓
Add to Order
        ↓
Confirm Order
        ↓
System identifies Recipe
        ↓
System calculates required Ingredients
        ↓
System selects eligible Stock Batches
        ↓
Stock is consumed
        ↓
Order is completed
```

Staff should not need to manually calculate ingredient quantities.

Where necessary, authorized staff should be able to view which ingredients and batches were consumed for an order.

---

# 19.33 Consistency Requirements

The same UI conventions should be used throughout the system.

For example:

* Primary actions should use consistent button placement.
* Forms should follow a similar structure.
* Tables should use consistent pagination.
* Status labels should follow the same naming.
* Confirmation dialogs should have consistent wording.
* Date and currency formatting should be consistent.
* Error messages should follow the same style.

This will make the system easier for staff to learn and use.

---

# 19.34 Currency and Date Display

Financial values should be displayed using the appropriate currency format, such as:

```text
25,000 RWF
```

Dates should be displayed consistently throughout the application.

For example:

```text
08 Oct 2026
```

The exact formatting can be finalized during implementation.

---

# 19.35 UI Security Considerations

The interface should not expose information that a user is not authorized to access.

The frontend should:

* Hide or disable unauthorized actions.
* Avoid displaying sensitive data unnecessarily.
* Require confirmation for sensitive operations.
* Automatically handle expired authentication sessions.
* Redirect unauthenticated users to the login page.

However, frontend restrictions are only for user experience. Actual authorization must always be enforced by the backend API.

---

# 19.36 Design Principles

The Board's Cafe interface should follow these principles:

### 1. Simplicity

Staff should be able to complete common tasks without unnecessary steps.

### 2. Clarity

Information should be presented in a way that is easy to understand.

### 3. Visibility

Important operational issues such as expired and low stock should be easy to notice.

### 4. Consistency

Similar actions should work in similar ways throughout the application.

### 5. Accuracy

Forms and workflows should reduce data-entry mistakes.

### 6. Feedback

Users should always receive clear feedback when an operation succeeds, fails, or requires attention.

### 7. Permission Awareness

Users should only be given access to functions appropriate to their roles and permissions.

---

# 19.37 Main UI Screens

The initial system should contain at least the following screens:

```text
1. Login
2. Dashboard
3. POS / New Order
4. Orders
5. Order Details
6. Menu Categories
7. Menu Products
8. Product Details
9. Recipe Management
10. Inventory Dashboard
11. Inventory Items
12. Stock Batches
13. Expired Stock
14. Expiring Soon
15. Stock Movements
16. Suppliers
17. Purchases
18. Purchase Details / Receiving
19. Expenses
20. Waste
21. Notifications
22. Reports
23. Users
24. Roles & Permissions
25. Audit Logs
26. User Profile
```

The exact number of screens may change during implementation as related functions are combined or separated.

---

# 19.38 UI/UX Acceptance Criteria

The UI/UX implementation will be considered acceptable when:

* Users can log in successfully.
* Users only see or access functions permitted by their roles.
* Staff can create and manage orders.
* Menu products and recipes can be viewed and managed by authorized users.
* Inventory levels are clearly displayed.
* Batch and expiry information is visible.
* Expired and expiring-soon stock can be identified easily.
* Purchases and received stock can be recorded.
* Expenses and waste can be recorded.
* Notifications are clearly displayed.
* Reports can be viewed and filtered.
* Users and roles can be managed by authorized administrators.
* Important system actions provide clear feedback.
* Validation errors are understandable.
* The application remains usable on supported screen sizes.
* The interface does not expose unauthorized or sensitive information.

---

# 19.39 Summary

The Board's Cafe UI/UX should provide a simple and practical interface for managing daily cafe operations.

The most important user experience areas are:

```text
Orders
  ↓
Recipes
  ↓
Inventory
  ↓
Batches & Expiry
  ↓
FEFO Consumption
  ↓
Waste
  ↓
Reports
```

The interface should make these processes easy to understand while keeping the underlying business rules and calculations in the backend.

The design should prioritize **simplicity, visibility, accuracy, consistency, and role-based access**.

---