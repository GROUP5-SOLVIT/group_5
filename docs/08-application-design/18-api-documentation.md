# Board’s Cafe Management System

# 18 — API Documentation

## 18.1 Introduction

The Board’s Cafe Management System will provide a RESTful API for communication between the frontend application and the backend system.

The API will provide controlled access to the system's business operations, including:

* Authentication
* User management
* Roles and permissions
* Menu management
* Recipe management
* Inventory management
* Batch and expiry tracking
* Stock movements
* POS orders
* Ingredient consumption
* Suppliers and purchases
* Expenses
* Waste management
* Notifications
* Reports
* Audit logs

The API will follow the database structure and business rules defined in Documents 16 and 17.

---

# 18.2 API Architecture

The system will follow a client-server architecture:

```text
┌──────────────────────────┐
│       Frontend           │
│   Board's Cafe Web App   │
└────────────┬─────────────┘
             │
             │ HTTPS / REST API
             ▼
┌──────────────────────────┐
│        Backend           │
│   Business Logic / API   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│        Database          │
│      PostgreSQL          │
└──────────────────────────┘
```

The frontend should not communicate directly with the database.

---

# 18.3 API Base URL

The production API should use a secure HTTPS address.

Example:

```text
https://api.boardscafe.rw/api/v1/
```

During development, a local URL may be used:

```text
http://localhost:8000/api/v1/
```

The actual production domain will be configured during deployment.

---

# 18.4 API Versioning

The API should be versioned.

The initial version will be:

```text
/api/v1/
```

Example:

```text
/api/v1/products/
/api/v1/inventory/
/api/v1/orders/
```

Versioning makes it possible to introduce future API changes without immediately breaking existing clients.

---

# 18.5 Authentication

The API will require authentication for protected operations.

A token-based authentication mechanism should be used.

The general flow is:

```text
Login
  ↓
Access Token
  ↓
Authenticated Request
  ↓
API
  ↓
Authorization Check
  ↓
Response
```

The frontend should send the access token with protected requests.

Example:

```http
Authorization: Bearer <access_token>
```

---

# 18.6 Authentication Endpoints

## Login

```http
POST /api/v1/auth/login/
```

Request:

```json
{
  "email": "staff@example.com",
  "password": "password"
}
```

Response:

```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>",
  "user": {
    "id": 1,
    "name": "Staff Member",
    "roles": [
      "Cashier"
    ]
  }
}
```

---

## Refresh Token

```http
POST /api/v1/auth/token/refresh/
```

Request:

```json
{
  "refresh": "<refresh_token>"
}
```

Response:

```json
{
  "access": "<new_access_token>"
}
```

---

## Logout

```http
POST /api/v1/auth/logout/
```

The implementation should invalidate the refresh token or otherwise terminate the authenticated session according to the selected authentication strategy.

---

# 18.7 Current User

```http
GET /api/v1/auth/me/
```

Returns information about the authenticated staff member.

Example response:

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "roles": [
    "Manager"
  ],
  "permissions": [
    "inventory.view",
    "inventory.adjust",
    "orders.view"
  ]
}
```

---

# 18.8 User Management

User management is restricted to authorized administrators.

## List Users

```http
GET /api/v1/users/
```

## Create User

```http
POST /api/v1/users/
```

Example:

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+250780000000",
  "role_ids": [2]
}
```

## Get User

```http
GET /api/v1/users/{id}/
```

## Update User

```http
PATCH /api/v1/users/{id}/
```

## Deactivate User

```http
POST /api/v1/users/{id}/deactivate/
```

Users should generally be deactivated instead of permanently deleting accounts that are associated with historical business activities.

---

# 18.9 Role Management

## List Roles

```http
GET /api/v1/roles/
```

## Create Role

```http
POST /api/v1/roles/
```

## Get Role

```http
GET /api/v1/roles/{id}/
```

## Update Role

```http
PATCH /api/v1/roles/{id}/
```

## Delete/Deactivate Role

```http
DELETE /api/v1/roles/{id}/
```

Deletion should be restricted where the role is referenced by historical or active assignments.

---

# 18.10 Permission Management

## List Permissions

```http
GET /api/v1/permissions/
```

## Assign Permission to Role

```http
POST /api/v1/roles/{role_id}/permissions/
```

Example:

```json
{
  "permission_id": 12
}
```

## Remove Permission

```http
DELETE /api/v1/roles/{role_id}/permissions/{permission_id}/
```

Only authorized administrators should manage permissions.

---

# 18.11 Menu Categories

## List Categories

```http
GET /api/v1/menu/categories/
```

## Create Category

```http
POST /api/v1/menu/categories/
```

Example:

```json
{
  "name": "Drinks",
  "description": "Hot and cold drinks"
}
```

## Get Category

```http
GET /api/v1/menu/categories/{id}/
```

## Update Category

```http
PATCH /api/v1/menu/categories/{id}/
```

## Deactivate Category

```http
POST /api/v1/menu/categories/{id}/deactivate/
```

---

# 18.12 Menu Products

## List Products

```http
GET /api/v1/menu/products/
```

Supported query parameters may include:

```text
?category=2
?status=active
?search=coffee
```

## Create Product

```http
POST /api/v1/menu/products/
```

Example:

```json
{
  "category_id": 2,
  "name": "Cappuccino",
  "description": "Hot cappuccino",
  "selling_price": "2500.00"
}
```

## Get Product

```http
GET /api/v1/menu/products/{id}/
```

## Update Product

```http
PATCH /api/v1/menu/products/{id}/
```

## Deactivate Product

```http
POST /api/v1/menu/products/{id}/deactivate/
```

---

# 18.13 Recipe Management

## Get Product Recipe

```http
GET /api/v1/menu/products/{product_id}/recipe/
```

## Create Recipe

```http
POST /api/v1/recipes/
```

Example:

```json
{
  "menu_product_id": 5,
  "name": "Cappuccino Recipe",
  "instructions": "Prepare espresso and add steamed milk."
}
```

---

# 18.14 Recipe Ingredients

## List Recipe Ingredients

```http
GET /api/v1/recipes/{recipe_id}/ingredients/
```

## Add Ingredient

```http
POST /api/v1/recipes/{recipe_id}/ingredients/
```

Example:

```json
{
  "inventory_item_id": 3,
  "quantity_required": "250.00",
  "unit_id": 2
}
```

## Update Recipe Ingredient

```http
PATCH /api/v1/recipes/{recipe_id}/ingredients/{id}/
```

## Remove Recipe Ingredient

```http
DELETE /api/v1/recipes/{recipe_id}/ingredients/{id}/
```

---

# 18.15 Inventory Categories

## List

```http
GET /api/v1/inventory/categories/
```

## Create

```http
POST /api/v1/inventory/categories/
```

## Update

```http
PATCH /api/v1/inventory/categories/{id}/
```

---

# 18.16 Units

## List Units

```http
GET /api/v1/inventory/units/
```

Example response:

```json
[
  {
    "id": 1,
    "name": "Kilogram",
    "abbreviation": "kg",
    "unit_type": "WEIGHT"
  },
  {
    "id": 2,
    "name": "Liter",
    "abbreviation": "L",
    "unit_type": "VOLUME"
  }
]
```

---

# 18.17 Inventory Items

## List Inventory

```http
GET /api/v1/inventory/items/
```

Possible filters:

```text
?category=1
?status=active
?low_stock=true
?search=milk
```

## Create Inventory Item

```http
POST /api/v1/inventory/items/
```

Example:

```json
{
  "category_id": 1,
  "unit_id": 2,
  "name": "Milk",
  "reorder_level": "10.00"
}
```

## Get Inventory Item

```http
GET /api/v1/inventory/items/{id}/
```

## Update Inventory Item

```http
PATCH /api/v1/inventory/items/{id}/
```

---

# 18.18 Current Stock

```http
GET /api/v1/inventory/stock/
```

Example response:

```json
{
  "inventory_item_id": 3,
  "name": "Milk",
  "unit": "L",
  "quantity_available": "42.50",
  "reorder_level": "10.00",
  "status": "NORMAL"
}
```

---

# 18.19 Stock Batches

## List Batches

```http
GET /api/v1/inventory/batches/
```

Possible filters:

```text
?inventory_item=3
?status=available
?expiring_soon=true
?expired=true
```

## Get Batch

```http
GET /api/v1/inventory/batches/{id}/
```

Example response:

```json
{
  "id": 15,
  "inventory_item": {
    "id": 3,
    "name": "Milk"
  },
  "batch_number": "MILK-001",
  "quantity_received": "50.00",
  "quantity_remaining": "18.50",
  "unit_cost": "1200.00",
  "received_date": "2026-10-01",
  "expiry_date": "2026-10-10",
  "status": "AVAILABLE"
}
```

---

# 18.20 Expired Products

## List Expired Stock

```http
GET /api/v1/inventory/batches/expired/
```

## Expiring Soon

```http
GET /api/v1/inventory/batches/expiring-soon/
```

The API should support a configurable period for "expiring soon".

Example:

```text
GET /api/v1/inventory/batches/expiring-soon/?days=3
```

---

# 18.21 FEFO Stock Selection

The frontend should not manually decide which batch to consume.

The backend should apply the FEFO business rule.

Example:

```http
POST /api/v1/inventory/consume/
```

Request:

```json
{
  "inventory_item_id": 3,
  "quantity": "5.00",
  "unit_id": 2
}
```

The backend determines eligible batches and selects stock according to FEFO where applicable.

Example:

```text
Batch A → expires 10 Oct → 3 L
Batch B → expires 15 Oct → 8 L

Requested:
5 L

Consume:
Batch A → 3 L
Batch B → 2 L
```

---

# 18.22 Stock Adjustments

Stock adjustments should require appropriate permission.

```http
POST /api/v1/inventory/adjustments/
```

Example:

```json
{
  "inventory_item_id": 3,
  "batch_id": 15,
  "quantity": "-2.00",
  "reason": "Physical stock count correction"
}
```

The API should validate the adjustment and create an appropriate stock movement.

---

# 18.23 Stock Movements

## List Movements

```http
GET /api/v1/inventory/movements/
```

Possible filters:

```text
?inventory_item=3
?batch=15
?movement_type=WASTE
?date_from=2026-10-01
?date_to=2026-10-08
```

## Get Movement

```http
GET /api/v1/inventory/movements/{id}/
```

Stock movements should generally be treated as historical records rather than editable records.

---

# 18.24 Suppliers

## List Suppliers

```http
GET /api/v1/suppliers/
```

## Create Supplier

```http
POST /api/v1/suppliers/
```

Example:

```json
{
  "name": "Example Dairy Supplier",
  "phone": "+250780000000",
  "email": "supplier@example.com"
}
```

## Get Supplier

```http
GET /api/v1/suppliers/{id}/
```

## Update Supplier

```http
PATCH /api/v1/suppliers/{id}/
```

## Deactivate Supplier

```http
POST /api/v1/suppliers/{id}/deactivate/
```

---

# 18.25 Purchases

## List Purchases

```http
GET /api/v1/purchases/
```

## Create Purchase

```http
POST /api/v1/purchases/
```

Example:

```json
{
  "supplier_id": 2,
  "purchase_date": "2026-10-08",
  "items": [
    {
      "inventory_item_id": 3,
      "quantity": "50.00",
      "unit_cost": "1200.00",
      "unit_id": 2
    }
  ]
}
```

The backend should validate the purchase and create the appropriate stock records when the purchase is received.

---

# 18.26 Purchase Receiving

Receiving inventory should be treated as a controlled operation.

```http
POST /api/v1/purchases/{id}/receive/
```

Example:

```json
{
  "items": [
    {
      "purchase_item_id": 1,
      "batch_number": "MILK-001",
      "quantity_received": "50.00",
      "expiry_date": "2026-10-15"
    }
  ]
}
```

The receiving process may create stock batches and stock movements.

---

# 18.27 POS Orders

## Create Order

```http
POST /api/v1/orders/
```

Example:

```json
{
  "items": [
    {
      "menu_product_id": 5,
      "quantity": 2
    },
    {
      "menu_product_id": 8,
      "quantity": 1
    }
  ],
  "notes": "No sugar"
}
```

The backend should calculate the order totals rather than trusting totals supplied by the frontend.

---

# 18.28 Order Calculation

The backend should calculate:

```text
Subtotal
   ↓
Discount
   ↓
Tax where applicable
   ↓
Final Total
```

Example:

```json
{
  "subtotal": "7500.00",
  "discount": "500.00",
  "tax": "0.00",
  "total_amount": "7000.00"
}
```

The frontend should display these values returned by the backend.

---

# 18.29 Order Status

## Update Order Status

```http
PATCH /api/v1/orders/{id}/status/
```

Example:

```json
{
  "status": "PREPARING"
}
```

Allowed transitions should be controlled by backend business rules.

Example:

```text
PENDING
   ↓
CONFIRMED
   ↓
PREPARING
   ↓
READY
   ↓
COMPLETED
```

Cancellation should only be possible under permitted conditions.

---

# 18.30 Order Items

```http
GET /api/v1/orders/{id}/items/
```

Individual order items should normally be created through the order endpoint or controlled order-item operations rather than allowing arbitrary changes to completed orders.

---

# 18.31 Ingredient Consumption

Ingredient consumption connects an order to inventory.

```http
POST /api/v1/orders/{order_id}/consume/
```

In the preferred workflow, the backend determines the required ingredients from the product recipes.

Example:

```text
Order
 ↓
2 × Cappuccino
 ↓
Recipe
 ↓
Milk + Coffee
 ↓
FEFO Batch Selection
 ↓
Ingredient Consumption
 ↓
Stock Movement
```

The frontend should not calculate the final inventory deduction itself.

---

# 18.32 Payment

## Create Payment

```http
POST /api/v1/orders/{order_id}/payments/
```

Example:

```json
{
  "amount": "5000.00",
  "payment_method": "CASH"
}
```

## List Payments

```http
GET /api/v1/orders/{order_id}/payments/
```

## Payment Details

```http
GET /api/v1/payments/{id}/
```

---

# 18.33 Expenses

## Expense Categories

```http
GET /api/v1/expenses/categories/
```

```http
POST /api/v1/expenses/categories/
```

## Expenses

```http
GET /api/v1/expenses/
```

```http
POST /api/v1/expenses/
```

Example:

```json
{
  "category_id": 2,
  "description": "Electricity bill",
  "amount": "85000.00",
  "expense_date": "2026-10-08",
  "payment_method": "BANK"
}
```

---

# 18.34 Waste Management

## Create Waste Record

```http
POST /api/v1/waste/
```

Example:

```json
{
  "reason": "EXPIRY",
  "items": [
    {
      "inventory_item_id": 3,
      "batch_id": 15,
      "quantity": "5.00"
    }
  ],
  "notes": "Milk expired before use"
}
```

The backend should validate that the batch exists and has sufficient remaining quantity.

---

# 18.35 Expired Stock to Waste

A controlled operation may allow authorized staff to move expired stock into waste.

```http
POST /api/v1/inventory/batches/{id}/record-waste/
```

The operation should:

1. Validate the batch.
2. Confirm that it is expired or otherwise eligible for waste.
3. Record the waste.
4. Reduce the batch quantity.
5. Create a stock movement.
6. Create an audit log.
7. Generate notifications where applicable.

---

# 18.36 Notifications

## List Notifications

```http
GET /api/v1/notifications/
```

## Mark as Read

```http
PATCH /api/v1/notifications/{id}/read/
```

## Mark All as Read

```http
POST /api/v1/notifications/read-all/
```

Example notification:

```json
{
  "id": 10,
  "title": "Milk Expiring Soon",
  "message": "Milk batch MILK-001 expires in 2 days.",
  "notification_type": "EXPIRING_SOON",
  "is_read": false
}
```

---

# 18.37 Reports

Reports should be generated from existing transactional data.

## Sales Summary

```http
GET /api/v1/reports/sales/
```

Example:

```text
?date_from=2026-10-01
&date_to=2026-10-08
```

Possible response:

```json
{
  "total_orders": 125,
  "total_sales": "850000.00",
  "total_paid": "820000.00",
  "average_order_value": "6800.00"
}
```

---

# 18.38 Inventory Report

```http
GET /api/v1/reports/inventory/
```

The report may include:

* Current stock
* Low-stock items
* Expired stock
* Expiring stock
* Stock value
* Stock movements

---

# 18.39 Waste Report

```http
GET /api/v1/reports/waste/
```

Possible filters:

```text
?date_from=2026-10-01
&date_to=2026-10-08
&reason=EXPIRY
```

The report may provide:

* Total wasted quantity
* Waste cost
* Waste by item
* Waste by reason
* Waste by period

---

# 18.40 Purchase Report

```http
GET /api/v1/reports/purchases/
```

The report may include:

* Total purchases
* Purchases by supplier
* Purchases by period
* Most purchased inventory items

---

# 18.41 Expense Report

```http
GET /api/v1/reports/expenses/
```

Possible filters:

```text
?date_from=2026-10-01
&date_to=2026-10-08
&category=1
```

---

# 18.42 Dashboard

The dashboard endpoint can provide the summary information required by the internal staff web application.

```http
GET /api/v1/dashboard/
```

Example:

```json
{
  "sales_today": "185000.00",
  "orders_today": 31,
  "low_stock_items": 5,
  "expiring_soon": 4,
  "expired_items": 2,
  "pending_orders": 3,
  "waste_today": "12500.00"
}
```

Dashboard values should be calculated from current system data.

---

# 18.43 Audit Logs

## List Audit Logs

```http
GET /api/v1/audit-logs/
```

Possible filters:

```text
?user=4
?action=CREATE
&resource_type=INVENTORY_ITEM
&date_from=2026-10-01
&date_to=2026-10-08
```

Access should be restricted to authorized users.

---

# 18.44 Standard API Response

Successful responses should use a consistent structure where appropriate.

Example:

```json
{
  "success": true,
  "message": "Product created successfully.",
  "data": {
    "id": 10,
    "name": "Cappuccino"
  }
}
```

For list endpoints:

```json
{
  "success": true,
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100
  }
}
```

The exact response wrapper can be finalized during backend implementation.

---

# 18.45 Validation Errors

Invalid requests should return clear validation errors.

Example:

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": {
    "quantity": [
      "Quantity must be greater than zero."
    ]
  }
}
```

Errors should be understandable to frontend developers and should not expose sensitive backend information.

---

# 18.46 Authentication Error

Example:

```json
{
  "success": false,
  "message": "Authentication credentials were not provided."
}
```

HTTP status:

```text
401 Unauthorized
```

---

# 18.47 Permission Error

When an authenticated user does not have permission:

```json
{
  "success": false,
  "message": "You do not have permission to perform this action."
}
```

HTTP status:

```text
403 Forbidden
```

---

# 18.48 Not Found Error

Example:

```json
{
  "success": false,
  "message": "Inventory item not found."
}
```

HTTP status:

```text
404 Not Found
```

---

# 18.49 Business Rule Errors

The API must return meaningful errors when a business rule is violated.

Example:

```json
{
  "success": false,
  "message": "Insufficient stock available for Milk."
}
```

Another example:

```json
{
  "success": false,
  "message": "The selected stock batch has expired and cannot be used."
}
```

Another:

```json
{
  "success": false,
  "message": "This order cannot be cancelled because it has already been completed."
}
```

---

# 18.50 Pagination

Large datasets should support pagination.

Applicable endpoints include:

* Users
* Products
* Inventory
* Batches
* Stock movements
* Orders
* Purchases
* Expenses
* Waste
* Notifications
* Audit logs

Example:

```text
GET /api/v1/inventory/items/?page=2&page_size=20
```

---

# 18.51 Searching

Search should be supported where useful.

Example:

```text
GET /api/v1/inventory/items/?search=milk
```

```text
GET /api/v1/menu/products/?search=coffee
```

```text
GET /api/v1/suppliers/?search=dairy
```

---

# 18.52 Filtering

Filtering should allow staff to find specific records efficiently.

Examples:

```text
/inventory/batches/?expired=true

/inventory/items/?low_stock=true

/orders/?status=PREPARING

/waste/?reason=EXPIRY

/purchases/?supplier=2
```

---

# 18.53 Sorting

Endpoints may support sorting where useful.

Example:

```text
GET /api/v1/inventory/batches/?ordering=expiry_date
```

For expiry management:

```text
expiry_date ASC
```

should place the earliest expiry first.

---

# 18.54 API Permission Matrix

API access must follow the role and permission system.

A simplified example:

| API Area   | Admin | Manager | Cashier | Storekeeper | Accountant |
| ---------- | ----: | ------: | ------: | ----------: | ---------: |
| Users      |  Full | Limited |      No |          No |         No |
| Roles      |  Full |      No |      No |          No |         No |
| Menu       |  Full |    Full |    View |        View |       View |
| Recipes    |  Full |    Full |    View |        View |       View |
| Inventory  |  Full |    Full |    View |        Full |       View |
| Batches    |  Full |    Full |    View |        Full |       View |
| Orders     |  Full |    Full |    Full |        View |       View |
| Payments   |  Full |    Full |    Full |          No |       Full |
| Purchases  |  Full |    Full |      No |        Full |       View |
| Expenses   |  Full |    Full |      No |          No |       Full |
| Waste      |  Full | Approve |  Record |      Record |       View |
| Reports    |  Full |    Full | Limited |   Inventory |  Financial |
| Audit Logs |  Full |    View |      No |          No |    Limited |

The exact permission matrix must follow Document 04.

---

# 18.55 API Security Requirements

The API should:

1. Use HTTPS in production.
2. Require authentication for protected endpoints.
3. Enforce role and permission checks.
4. Validate all input.
5. Never trust calculated totals from the frontend.
6. Never expose passwords.
7. Avoid exposing sensitive internal errors.
8. Protect administrative endpoints.
9. Apply appropriate rate limiting.
10. Validate object ownership or access where applicable.
11. Use secure token handling.
12. Record important security-sensitive actions in audit logs.

---

# 18.56 Important Backend Business Rules

Business rules should be implemented in the backend rather than relying on the frontend.

Examples include:

### Stock

```text
Cannot consume more stock than available.
```

### Expiry

```text
Expired batches cannot be used for normal production.
```

### FEFO

```text
Earlier-expiring eligible batches should be consumed first.
```

### Orders

```text
Completed orders cannot be freely edited.
```

### Payments

```text
Payment amounts must be validated against the order.
```

### Permissions

```text
A user cannot perform an action without the required permission.
```

### Waste

```text
Waste quantities cannot exceed available batch quantities.
```

---

# 18.57 Atomic Inventory Operations

Operations that change inventory should be performed atomically.

For example:

```text
Order Completion
      ↓
Recipe Calculation
      ↓
FEFO Batch Selection
      ↓
Ingredient Consumption
      ↓
Batch Quantity Update
      ↓
Stock Movement
      ↓
Audit Log
```

These operations should be protected by database transactions where appropriate.

---

# 18.58 API Documentation

The API should provide machine-readable documentation.

The implementation should support an OpenAPI specification.

The API documentation should allow developers to understand:

* Available endpoints
* HTTP methods
* Request parameters
* Request bodies
* Response structures
* Authentication requirements
* Permission requirements
* Validation errors
* HTTP status codes

A browsable API documentation interface may be provided for development and testing.

---

# 18.59 API Naming Convention

Endpoint names should use predictable plural resource names.

Preferred:

```text
/users/
/roles/
/permissions/
/menu/products/
/inventory/items/
/inventory/batches/
/orders/
/purchases/
/expenses/
/waste/
/notifications/
```

Avoid inconsistent naming such as:

```text
/getProducts
/createNewProduct
/fetchInventory
```

RESTful resource-oriented naming should be preferred.

---

# 18.60 API Design Summary

The Board’s Cafe API connects the frontend web application to the backend business system.

The major API areas are:

```text
                    API
                     |
     ┌───────────────┼────────────────┐
     ↓               ↓                ↓
 Authentication   Administration     Menu
     |               |                |
     ↓               ↓                ↓
   Users        Roles/Permissions   Products
                                      |
                                      ↓
                                    Recipes
                                      |
                                      ↓
                              Recipe Ingredients
                                      |
                                      ↓
                                  Inventory
                                      |
                         ┌────────────┼────────────┐
                         ↓            ↓            ↓
                      Batches       Stock        Expiry
                         |         Movements        |
                         └────────────┬────────────┘
                                      ↓
                                  Consumption
                                      ↑
                                      |
                                   Orders
                                      |
                                   Payments

     Purchases ──→ Inventory
     Waste ──────→ Inventory
     Expenses ───→ Finance
     Notifications → Users
     Audit Logs ──→ All Important Actions
     Reports ─────→ Transactional Data
```

The API is designed around the principle that the **backend is responsible for enforcing business rules**.

The frontend provides the user interface, while the backend validates requests, applies permissions, calculates business results, updates the database, and maintains traceability.

---
