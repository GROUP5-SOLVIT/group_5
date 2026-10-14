# Board’s Cafe Management System

# 16 — Database Design

## 16.1 Introduction

The database will provide the permanent data storage structure for the Board’s Cafe Management System.

The database design is derived from the business requirements, functional requirements, user roles, business workflows, products and recipes, inventory, expiry management, POS orders, purchases, expenses, waste, notifications, and audit logging defined in the previous documents.

The database must support the actual way Board’s Cafe operates rather than simply storing isolated records.

The most important operational relationship is:

```text
Customer Order
      ↓
Menu Product
      ↓
Recipe
      ↓
Ingredient
      ↓
Valid Stock Batch
      ↓
Ingredient Consumption
      ↓
Stock Movement
```

At the same time, inventory must support:

```text
Purchase
   ↓
Received Stock
   ↓
Batch
   ↓
Expiry
   ↓
FEFO
   ↓
Consumption / Waste
```

---

# 16.2 Database Design Objectives

The database should:

1. Store accurate business information.
2. Maintain relationships between business entities.
3. Support multiple staff users and permissions.
4. Support menu products and recipes.
5. Allow one ingredient to be used by many products.
6. Allow one product to contain many ingredients.
7. Track inventory quantities.
8. Track stock by batch where required.
9. Track expiry dates at batch level.
10. Record stock movements.
11. Support made-to-order production.
12. Track ingredient consumption.
13. Track customer orders.
14. Track payments.
15. Track suppliers and purchases.
16. Track expenses.
17. Track waste.
18. Support notifications.
19. Maintain audit history.
20. Preserve historical business transactions.

---

# 16.3 Database Design Principles

The database should follow these principles.

### 16.3.1 Single Source of Truth

Important business information should have one authoritative location.

For example, an ingredient such as milk should not be duplicated simply because it is used in several menu products.

```text
Inventory Item
      ↓
Milk
      ↓
├── Cappuccino
├── Latte
├── Tea
├── Pancake
└── Cake
```

This follows the shared-ingredient requirement established for Board’s Cafe.

---

### 16.3.2 Referential Integrity

Relationships between records should be protected using appropriate foreign keys and database constraints.

For example:

```text
Order Item
    ↓
Menu Product
```

An order item should not reference a menu product that does not exist.

---

### 16.3.3 Historical Integrity

Historical transactions should remain meaningful even when a related record becomes inactive.

For example, if a menu product is discontinued:

```text
Product
   ↓
INACTIVE
```

previous orders containing that product should remain available.

---

### 16.3.4 Traceability

Important changes should be traceable through stock movements and audit logs.

---

### 16.3.5 Avoid Unnecessary Duplication

The database should avoid storing the same information repeatedly when it can be derived from related records.

---

# 16.4 Main Entity Groups

The database can be organized into the following logical groups.

| Group          | Main Entities                        |
| -------------- | ------------------------------------ |
| Administration | Users, Roles, Permissions            |
| Menu           | Categories, Menu Products            |
| Recipes        | Recipes, Recipe Ingredients          |
| Inventory      | Inventory Items, Units, Stock        |
| Batches        | Stock Batches, Expiry                |
| Stock Control  | Stock Movements, Consumption         |
| Sales          | Orders, Order Items                  |
| Purchasing     | Suppliers, Purchases, Purchase Items |
| Finance        | Payments, Expenses                   |
| Waste          | Waste Records, Waste Items           |
| Notifications  | Notifications                        |
| Audit          | Audit Logs                           |

---

# 16.5 Administration Entities

## 16.5.1 User

The User entity represents an internal staff member who can access the system.

Possible attributes include:

| Field      | Description                       |
| ---------- | --------------------------------- |
| id         | Unique identifier                 |
| username   | Login identifier where applicable |
| email      | Staff email                       |
| password   | Securely stored password hash     |
| first_name | First name                        |
| last_name  | Last name                         |
| phone      | Optional phone                    |
| is_active  | Account status                    |
| created_at | Creation date                     |
| updated_at | Last update                       |

Passwords must never be stored in plain text.

---

## 16.5.2 Role

A Role defines a group of responsibilities assigned to users.

Examples may include:

```text
Administrator
Manager
Cashier
Storekeeper
Kitchen Staff
Accountant
```

The final roles should follow Board’s Cafe's approved permission structure.

---

## 16.5.3 Permission

A Permission defines a specific action that a user may perform.

Examples:

```text
users.view
users.create
users.update

inventory.view
inventory.receive
inventory.adjust

orders.view
orders.create
orders.cancel

waste.view
waste.create
waste.approve
```

---

## 16.5.4 User–Role Relationship

A user may have one or more roles depending on the final RBAC design.

Conceptually:

```text
USER
  │
  └──── ROLE
           │
           └──── PERMISSIONS
```

The administrator is responsible for managing user access and assigning roles and permissions.

---

# 16.6 Menu Entities

## 16.6.1 Menu Category

A Menu Category groups customer-facing products.

Examples:

```text
Breakfast
Lunch
Burgers
Pizza
Drinks
Coffee
Desserts
```

Possible attributes:

| Field       | Description          |
| ----------- | -------------------- |
| id          | Unique identifier    |
| name        | Category name        |
| description | Optional description |
| status      | Active/inactive      |
| created_at  | Creation date        |
| updated_at  | Last update          |

---

# 16.7 Menu Product

A Menu Product represents something that can be offered to a customer.

Examples:

```text
Cappuccino
Latte
Chicken Burger
Pancake
Pizza
Cake
```

Possible attributes:

| Field         | Description           |
| ------------- | --------------------- |
| id            | Unique identifier     |
| category_id   | Product category      |
| name          | Product name          |
| description   | Product description   |
| selling_price | Current selling price |
| status        | Available/unavailable |
| created_at    | Creation date         |
| updated_at    | Last update           |

Historical orders should preserve the relevant selling information even if the product's current price later changes.

---

# 16.8 Inventory Entities

## 16.8.1 Inventory Item

An Inventory Item represents a physical material or stocked product managed by the cafe.

Examples:

```text
Milk
Wheat Flour
Tomatoes
Onions
Eggs
Butter
Sugar
Coffee Beans
Cooking Oil
Chicken
Bottled Water
Bread
```

An inventory item may be:

* Raw ingredient
* Food ingredient
* Beverage ingredient
* Packaging material
* Consumable
* Direct-sale stocked item

---

# 16.9 Inventory Item Attributes

Possible fields:

| Field               | Description              |
| ------------------- | ------------------------ |
| id                  | Unique identifier        |
| category_id         | Inventory category       |
| name                | Item name                |
| description         | Description              |
| base_unit_id        | Base measurement unit    |
| reorder_level       | Minimum desired quantity |
| maximum_stock_level | Optional maximum level   |
| track_batch         | Batch tracking flag      |
| track_expiry        | Expiry tracking flag     |
| status              | Active/inactive/blocked  |
| created_at          | Creation date            |
| updated_at          | Last update              |

---

# 16.10 Units of Measurement

The database should support different units.

Examples:

```text
kg
g
L
ml
piece
bottle
packet
```

Units should be categorized by measurement type.

```text
WEIGHT
  kg
  g

VOLUME
  L
  ml

COUNT
  piece
  bottle
  packet
```

Compatible units may have conversion rules.

For example:

```text
1 kg = 1,000 g
1 L  = 1,000 ml
```

---

# 16.11 Stock and Inventory Quantities

The database should support the recording of stock quantities.

However, stock should not simply be changed without an explanation.

Stock changes should be represented through appropriate inventory transactions or stock movements.

For example:

```text
Purchase Received
       +
Stock Adjustment
       -
Consumption
       -
Waste
       -
Transfer
       =
Current Stock
```

This creates a traceable inventory history.

---

# 16.12 Stock Batch

A Stock Batch represents a specific quantity of inventory received or identified as one batch.

This is especially important for perishable products.

Example:

```text
Milk

Batch M001
20 L
Expiry: 10 Oct

Batch M002
30 L
Expiry: 25 Oct
```

The database must therefore avoid storing only:

```text
Milk = 50 L
```

when batch tracking is required.

---

# 16.13 Stock Batch Attributes

Possible fields:

| Field              | Description                           |
| ------------------ | ------------------------------------- |
| id                 | Unique identifier                     |
| inventory_item_id  | Related inventory item                |
| batch_number       | Batch identifier                      |
| quantity_received  | Original quantity                     |
| quantity_remaining | Remaining quantity                    |
| unit_cost          | Cost per base unit                    |
| received_date      | Date received                         |
| expiry_date        | Expiry date                           |
| status             | Batch status                          |
| purchase_item_id   | Source purchase item where applicable |
| created_at         | Creation date                         |
| updated_at         | Last update                           |

---

# 16.14 Batch Status

Possible statuses include:

```text
AVAILABLE
RESERVED
EXPIRED
DAMAGED
SPOILED
BLOCKED
QUARANTINED
DEPLETED
```

The exact values should be finalized during implementation.

---

# 16.15 Expiry Data

Expiry belongs to the **stock batch**, not simply to the inventory item.

For example:

```text
Inventory Item:
Milk

Batch M001
Expiry:
10 October

Batch M002
Expiry:
25 October
```

This allows the system to determine which stock should be used first.

---

# 16.16 FEFO

The inventory system should support **First Expired, First Out (FEFO)** for applicable perishable inventory.

Conceptually:

```text
Valid Batch A
Expires: 10 Oct
       ↓
Valid Batch B
Expires: 15 Oct
       ↓
Valid Batch C
Expires: 25 Oct
```

The system should prioritize Batch A before Batch B and Batch C.

Expired batches must not be selected for normal consumption.

---

# 16.17 Stock Movement

A Stock Movement records a change in inventory.

Possible movement types include:

```text
RECEIPT
CONSUMPTION
ADJUSTMENT
WASTE
RETURN
TRANSFER_IN
TRANSFER_OUT
CORRECTION
```

Possible attributes:

| Field             | Description                    |
| ----------------- | ------------------------------ |
| id                | Unique identifier              |
| inventory_item_id | Inventory item                 |
| batch_id          | Related batch where applicable |
| movement_type     | Type of movement               |
| quantity          | Quantity changed               |
| unit              | Unit                           |
| reference_type    | Source transaction             |
| reference_id      | Source record ID               |
| reason            | Explanation where applicable   |
| performed_by      | User                           |
| created_at        | Date/time                      |

---

# 16.18 Stock Movement Direction

The database should make it clear whether a movement increases or decreases stock.

For example:

```text
RECEIPT
+20 kg

CONSUMPTION
-2 kg

WASTE
-1 kg

ADJUSTMENT
-3 kg
```

This makes stock calculations easier to understand.

---

# 16.19 Recipe Entities

## 16.19.1 Recipe

A Recipe defines how a menu product is prepared.

Example:

```text
Cappuccino
    ↓
Milk
Coffee
Sugar
```

Another:

```text
Pancake
    ↓
Wheat Flour
Milk
Egg
Sugar
Butter
```

---

# 16.20 Recipe Ingredient

Because one menu product can use multiple ingredients and one ingredient can be used by multiple products, the relationship is many-to-many.

This should be implemented through a linking entity such as:

```text
RecipeIngredient
```

Conceptually:

```text
MENU PRODUCT
      │
      ▼
    RECIPE
      │
      ▼
RECIPE INGREDIENT
      │
      ▼
INVENTORY ITEM
```

Possible fields:

| Field             | Description                    |
| ----------------- | ------------------------------ |
| id                | Unique identifier              |
| recipe_id         | Recipe                         |
| inventory_item_id | Ingredient                     |
| quantity          | Required quantity              |
| unit_id           | Measurement unit               |
| optional          | Whether ingredient is optional |
| created_at        | Creation date                  |
| updated_at        | Last update                    |

---

# 16.21 Shared Ingredients

The database must support one inventory item being used by many menu products.

Example:

```text
Milk
 │
 ├── Cappuccino
 ├── Latte
 ├── Tea
 ├── Pancake
 └── Cake
```

Likewise:

```text
Wheat Flour
 │
 ├── Pancake
 ├── Cake
 ├── Bread
 └── Mandazi
```

This prevents unnecessary duplication.

---

# 16.22 Made-to-Order Production

Board’s Cafe may prepare products when customers place orders rather than producing all menu products in advance.

The database should therefore support the following flow:

```text
Customer Order
      ↓
Order Item
      ↓
Menu Product
      ↓
Recipe
      ↓
Required Ingredients
      ↓
Valid Stock Batches
      ↓
Ingredient Consumption
      ↓
Stock Movements
```

For example:

```text
Order:
2 Cappuccinos
1 Pancake
```

The system can calculate the required ingredients from the recipes and record the actual consumption.

The made-to-order workflow has already been established as an important business concept for the system.

---

# 16.23 Ingredient Consumption

An Ingredient Consumption record represents ingredients used during preparation.

Possible fields:

| Field             | Description        |
| ----------------- | ------------------ |
| id                | Unique identifier  |
| order_id          | Related order      |
| order_item_id     | Related order item |
| inventory_item_id | Ingredient         |
| batch_id          | Batch consumed     |
| quantity          | Quantity consumed  |
| unit_id           | Unit               |
| consumed_by       | Staff member       |
| created_at        | Date/time          |

This provides traceability between a sale and the inventory consumed to fulfill it.

---

# 16.24 Order Entities

## 16.24.1 Order

An Order represents a customer's purchase.

Possible fields:

| Field        | Description                 |
| ------------ | --------------------------- |
| id           | Unique identifier           |
| order_number | Human-readable order number |
| status       | Order status                |
| subtotal     | Subtotal                    |
| discount     | Discount                    |
| tax          | Tax where applicable        |
| total        | Final amount                |
| created_by   | Staff member                |
| created_at   | Creation date               |
| updated_at   | Last update                 |

---

# 16.25 Order Item

An Order Item represents one product within an order.

Example:

```text
Order #1052

2 × Cappuccino
1 × Pancake
```

Possible fields:

| Field      | Description                |
| ---------- | -------------------------- |
| id         | Unique identifier          |
| order_id   | Parent order               |
| product_id | Menu product               |
| quantity   | Quantity ordered           |
| unit_price | Price at time of sale      |
| subtotal   | Line subtotal              |
| notes      | Optional preparation notes |

The `unit_price` should preserve the price used when the order was created.

---

# 16.26 Order Status

Possible order statuses include:

```text
PENDING
CONFIRMED
PREPARING
READY
COMPLETED
CANCELLED
```

The exact workflow should follow the business process established in Document 09.

---

# 16.27 Payment

A Payment represents money received or processed against an order.

Possible fields:

| Field          | Description                 |
| -------------- | --------------------------- |
| id             | Unique identifier           |
| order_id       | Related order               |
| amount         | Amount paid                 |
| payment_method | Payment method              |
| status         | Payment status              |
| reference      | External/internal reference |
| paid_at        | Payment date                |
| recorded_by    | Staff member                |
| created_at     | Creation date               |

Possible payment methods may include:

```text
CASH
MOBILE_MONEY
CARD
BANK
OTHER
```

The final list should reflect Board’s Cafe's actual payment practices.

---

# 16.28 Supplier Entities

## 16.28.1 Supplier

A Supplier represents a business or person from whom Board’s Cafe purchases inventory.

Possible fields:

| Field      | Description            |
| ---------- | ---------------------- |
| id         | Unique identifier      |
| name       | Supplier name          |
| phone      | Contact number         |
| email      | Email                  |
| address    | Address                |
| status     | Active/inactive        |
| notes      | Additional information |
| created_at | Creation date          |
| updated_at | Last update            |

---

# 16.29 Purchase

A Purchase represents a purchase transaction from a supplier.

Possible fields:

| Field           | Description        |
| --------------- | ------------------ |
| id              | Unique identifier  |
| supplier_id     | Supplier           |
| purchase_number | Purchase reference |
| status          | Purchase status    |
| purchase_date   | Date               |
| subtotal        | Subtotal           |
| total           | Total cost         |
| created_by      | Staff member       |
| created_at      | Creation date      |

---

# 16.30 Purchase Item

A Purchase Item identifies inventory received through a purchase.

Example:

```text
Purchase PO-102

Milk       50 L
Tomatoes   20 kg
Flour      30 kg
```

Possible fields:

| Field             | Description                            |
| ----------------- | -------------------------------------- |
| id                | Unique identifier                      |
| purchase_id       | Parent purchase                        |
| inventory_item_id | Inventory item                         |
| quantity          | Purchased quantity                     |
| unit_id           | Unit                                   |
| unit_cost         | Cost per unit                          |
| total_cost        | Total line cost                        |
| batch_id          | Created/related batch where applicable |

A purchase may therefore result in one or more stock batches.

---

# 16.31 Purchase to Batch Relationship

For batch-tracked inventory:

```text
Supplier
   ↓
Purchase
   ↓
Purchase Item
   ↓
Stock Batch
   ↓
Inventory
```

This provides traceability from the supplier through to the stock currently held by Board’s Cafe.

---

# 16.32 Expense

An Expense represents an operational business expense that is not necessarily an inventory purchase.

Examples:

```text
Electricity
Water
Internet
Cleaning
Maintenance
Transport
Other operating expenses
```

Possible fields:

| Field        | Description               |
| ------------ | ------------------------- |
| id           | Unique identifier         |
| category_id  | Expense category          |
| amount       | Expense amount            |
| description  | Description               |
| expense_date | Date                      |
| status       | Status                    |
| created_by   | User                      |
| approved_by  | Approver where applicable |
| created_at   | Creation date             |

---

# 16.33 Waste

Waste represents inventory that can no longer be used or sold.

Possible reasons include:

```text
EXPIRY
SPOILAGE
DAMAGE
PREPARATION_ERROR
ACCIDENTAL_LOSS
OTHER
```

Possible fields:

| Field            | Description                |
| ---------------- | -------------------------- |
| id               | Unique identifier          |
| reference_number | Waste reference            |
| reason           | Waste reason               |
| status           | Approval/processing status |
| recorded_by      | Staff member               |
| approved_by      | Approver where applicable  |
| created_at       | Creation date              |
| approved_at      | Approval date              |

---

# 16.34 Waste Item

A Waste Item identifies what inventory was wasted.

Possible fields:

| Field             | Description               |
| ----------------- | ------------------------- |
| id                | Unique identifier         |
| waste_id          | Waste record              |
| inventory_item_id | Item                      |
| batch_id          | Batch                     |
| quantity          | Quantity wasted           |
| unit_id           | Unit                      |
| unit_cost         | Cost at time of waste     |
| estimated_value   | Estimated financial value |

This is important for calculating the financial impact of waste.

---

# 16.35 Notification

A Notification informs an appropriate staff member about an event requiring attention.

Possible fields:

| Field        | Description                 |
| ------------ | --------------------------- |
| id           | Unique identifier           |
| recipient_id | User receiving notification |
| type         | Notification type           |
| priority     | Priority                    |
| title        | Short title                 |
| message      | Notification message        |
| related_type | Related entity              |
| related_id   | Related record              |
| is_read      | Read/unread                 |
| read_at      | Read timestamp              |
| created_at   | Creation timestamp          |

Examples include:

```text
LOW_STOCK
EXPIRING_SOON
EXPIRED
NEW_ORDER
ORDER_DELAYED
PURCHASE_APPROVAL
WASTE_APPROVAL
```

---

# 16.36 Audit Log

The Audit Log records important activities performed by users or automated system processes.

Possible fields:

| Field         | Description                          |
| ------------- | ------------------------------------ |
| id            | Unique identifier                    |
| user_id       | User responsible                     |
| action        | Action performed                     |
| module        | Module affected                      |
| resource_type | Resource type                        |
| resource_id   | Resource identifier                  |
| description   | Human-readable description           |
| old_values    | Previous values where applicable     |
| new_values    | New values where applicable          |
| ip_address    | IP address where appropriate         |
| user_agent    | Client information where appropriate |
| created_at    | Timestamp                            |

The audit design follows the requirement that important actions such as user changes, stock adjustments, purchases, waste, order cancellation, refunds, and permission changes should be traceable.

---

# 16.37 Core Relationships

The most important database relationships are:

```text
USER
 │
 ├── ROLE
 │      └── PERMISSION
 │
 ├── ORDERS
 ├── PURCHASES
 ├── EXPENSES
 ├── WASTE
 ├── STOCK MOVEMENTS
 ├── NOTIFICATIONS
 └── AUDIT LOGS
```

---

## Menu and Recipe

```text
MENU CATEGORY
      │
      └── MENU PRODUCT
               │
               └── RECIPE
                      │
                      └── RECIPE INGREDIENT
                               │
                               └── INVENTORY ITEM
```

---

## Inventory

```text
INVENTORY ITEM
      │
      ├── STOCK BATCH
      │       └── EXPIRY
      │
      └── STOCK MOVEMENTS
```

---

## Sales and Consumption

```text
ORDER
  │
  ├── ORDER ITEM
  │       └── MENU PRODUCT
  │
  ├── PAYMENT
  │
  └── INGREDIENT CONSUMPTION
          │
          ├── INVENTORY ITEM
          └── STOCK BATCH
```

---

## Purchasing

```text
SUPPLIER
    │
    └── PURCHASE
          │
          └── PURCHASE ITEM
                  │
                  ├── INVENTORY ITEM
                  └── STOCK BATCH
```

---

## Waste

```text
WASTE
  │
  └── WASTE ITEM
         │
         ├── INVENTORY ITEM
         └── STOCK BATCH
```

---

# 16.38 Important Many-to-Many Relationships

The database contains several relationships that must not be implemented as simple foreign keys.

## Menu Products ↔ Ingredients

A menu product can contain many ingredients.

An ingredient can be used by many menu products.

Therefore:

```text
Menu Product
      ↕
Recipe Ingredient
      ↕
Inventory Item
```

This is a many-to-many relationship.

---

# 16.39 Orders ↔ Menu Products

One order can contain many menu products.

One menu product can appear in many orders.

Therefore:

```text
Order
  ↕
Order Item
  ↕
Menu Product
```

---

# 16.40 Roles ↔ Permissions

A role can contain many permissions.

A permission can belong to many roles.

Therefore:

```text
Role
  ↕
Role Permission
  ↕
Permission
```

The exact implementation may use Django's built-in permission framework or a custom structure depending on the final backend architecture.

---

# 16.41 Stock Traceability

The database should support tracing an inventory item through its lifecycle.

Example:

```text
SUPPLIER
   ↓
PURCHASE
   ↓
PURCHASE ITEM
   ↓
STOCK BATCH
   ↓
INVENTORY
   ↓
CONSUMPTION
   ↓
ORDER
```

Or:

```text
STOCK BATCH
   ↓
EXPIRY
   ↓
WASTE
   ↓
AUDIT LOG
```

---

# 16.42 Example — Milk Lifecycle

Consider milk purchased for Board’s Cafe.

```text
Supplier:
Dairy Supplier
        ↓
Purchase:
PO-102
        ↓
Purchase Item:
Milk — 50 L
        ↓
Batch:
M001
        ↓
Expiry:
10 Oct 2026
        ↓
Inventory:
Milk — 50 L
        ↓
Used for:
Cappuccino
Latte
Pancake
        ↓
Stock Consumption
        ↓
Remaining:
5 L
        ↓
Expiry
        ↓
Waste
```

The database should be able to preserve this chain.

---

# 16.43 Data Integrity Rules

The database should enforce important business rules where practical.

Examples:

### Positive Quantities

Normal purchase and stock quantities should not be negative.

### Unique Batch Numbers

Batch numbers should be unique within the appropriate scope.

### Valid Foreign Keys

Related records must reference existing records.

### Valid Dates

Expiry dates should be logically valid.

### Valid Status Transitions

Records should not move directly between incompatible states without following the business workflow.

---

# 16.44 Historical Price Preservation

When a customer purchases a product, the order should retain the price used at the time.

Example:

```text
Current Product Price:
5,000 RWF

Old Order:
4,500 RWF
```

Changing the product price must not change historical order totals.

---

# 16.45 Historical Inventory Cost

Where inventory valuation is required, stock movements and batches should preserve relevant cost information.

For example:

```text
Milk Batch M001
Cost: 1,200 RWF/L

Milk Batch M002
Cost: 1,350 RWF/L
```

This allows management to understand differences in inventory cost.

---

# 16.46 Inactive Records

Important master records should generally be deactivated rather than permanently deleted.

Examples:

```text
Product → INACTIVE
Supplier → INACTIVE
Inventory Item → INACTIVE
User → INACTIVE
```

Historical transactions should remain intact.

---

# 16.47 Database Transactions

Operations involving multiple related records should be performed atomically where appropriate.

For example, completing a made-to-order sale may involve:

```text
Create/Update Order
       ↓
Create Order Items
       ↓
Record Payment
       ↓
Determine Ingredient Consumption
       ↓
Deduct Valid Stock Batches
       ↓
Create Stock Movements
```

If a critical step fails, the system should avoid leaving partially completed business transactions.

---

# 16.48 Example Transaction

Suppose a customer orders:

```text
2 Cappuccinos
```

The recipe requires:

```text
Milk:
450 ml per cappuccino

Coffee:
20 g per cappuccino
```

The database transaction may record:

```text
Order:
2 Cappuccinos

Consumption:
Milk → 900 ml
Coffee → 40 g

Stock Movements:
Milk → -900 ml
Coffee → -40 g
```

The consumed quantities should be traceable back to the order.

---

# 16.49 Database Normalization

The database should follow appropriate normalization principles to reduce unnecessary duplication and update anomalies.

For example, supplier information should not be copied into every purchase item.

Instead:

```text
Supplier
   ↓
Purchase
   ↓
Purchase Items
```

Likewise, product information should not be copied into every recipe ingredient.

Instead:

```text
Menu Product
   ↓
Recipe
   ↓
Recipe Ingredients
   ↓
Inventory Item
```

---

# 16.50 Reporting Data

Reports should primarily be generated from transactional data rather than manually maintained summary values.

For example:

```text
Sales Report
     ↓
Orders + Order Items + Payments

Inventory Report
     ↓
Inventory + Batches + Stock Movements

Waste Report
     ↓
Waste + Waste Items

Purchase Report
     ↓
Purchases + Purchase Items
```

This reduces inconsistencies between reports and operational records.

---

# 16.51 Database Security

The database must be protected from unauthorized access.

Application users should not have unrestricted database access.

Access should normally follow:

```text
User
  ↓
Authentication
  ↓
Authorization
  ↓
Application
  ↓
Database
```

Sensitive data should be protected according to the Security Requirements document.

---

# 16.52 Database Backup

The production database should be backed up regularly.

Backups should support recovery from:

* Hardware failure
* Software errors
* Accidental deletion
* Data corruption
* Security incidents

Backup and recovery procedures will be detailed further in the Technical Architecture and Security documents.

---

# 16.53 Initial Entity List

The initial database entity list is:

```text
1. User
2. Role
3. Permission
4. RolePermission
5. UserRole
6. MenuCategory
7. MenuProduct
8. Recipe
9. RecipeIngredient
10. InventoryCategory
11. Unit
12. InventoryItem
13. StockBatch
14. StockMovement
15. IngredientConsumption
16. Supplier
17. Purchase
18. PurchaseItem
19. Order
20. OrderItem
21. Payment
22. ExpenseCategory
23. Expense
24. Waste
25. WasteItem
26. Notification
27. AuditLog
```

Some of these may be combined with framework-provided models or adjusted during implementation.

The final entity list must be validated against the ERD before coding.

---

# 16.54 Database Design Summary

The Board’s Cafe database is centered around several connected business areas:

```text
                 USERS
                   │
            ROLES & PERMISSIONS
                   │
                   ▼
              APPLICATION
                   │
     ┌─────────────┼─────────────┐
     ▼             ▼             ▼
   SALES        INVENTORY     PURCHASING
     │             │             │
     │             ▼             │
     │          BATCHES           │
     │             │             │
     │          EXPIRY            │
     │             │             │
     │          WASTE             │
     │             │             │
     └──────► CONSUMPTION ◄───────┘
                   │
                   ▼
               REPORTS
                   │
          ┌────────┴────────┐
          ▼                 ▼
    NOTIFICATIONS       AUDIT LOGS
```

The most important relationship remains:

```text
Order
  ↓
Menu Product
  ↓
Recipe
  ↓
Ingredient
  ↓
Batch
  ↓
FEFO
  ↓
Consumption
  ↓
Stock Movement
```

