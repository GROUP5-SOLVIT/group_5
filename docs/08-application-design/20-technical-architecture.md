# Board's Cafe Management System

# 20. Technical Architecture

## 20.1 Introduction

The Board's Cafe Management System will be an internal web-based application designed to support the daily operations of the cafe.

The system will connect sales, orders, recipes, inventory, purchasing, expiry management, waste, expenses, payments, notifications, reporting, users, roles, permissions, and audit logging within one system.

The architecture will use a layered client-server approach in which the frontend communicates with the backend through a REST API, while the backend communicates with the relational database.

The backend will be responsible for enforcing business rules, permissions, calculations, stock movements, and data integrity.

---

# 20.2 Architectural Goals

The architecture should provide:

* Clear separation between frontend and backend.
* Secure role-based access control.
* Reliable inventory management.
* Batch-level expiry tracking.
* Recipe-based ingredient consumption.
* Accurate stock calculations.
* Transaction-safe business operations.
* Auditability of important actions.
* Maintainable and understandable code.
* Ability to extend the system in the future.
* Good performance for normal cafe operations.

---

# 20.3 High-Level Architecture

The system will follow a three-layer architecture:

```text
┌─────────────────────────────────────────────┐
│                 WEB BROWSER                 │
│                                             │
│       Board's Cafe Staff Web Application    │
└──────────────────────┬──────────────────────┘
                       │
                       │ HTTPS / REST API
                       ▼
┌─────────────────────────────────────────────┐
│                  BACKEND                    │
│                                             │
│  Authentication                             │
│  Authorization                              │
│  Business Logic                             │
│  Inventory Services                         │
│  Order Services                             │
│  Recipe Services                            │
│  Purchase Services                          │
│  Reporting Services                         │
│  Notification Services                     │
│  Audit Logging                              │
└──────────────────────┬──────────────────────┘
                       │
                       │ ORM / Database Connection
                       ▼
┌─────────────────────────────────────────────┐
│                 DATABASE                    │
│                                             │
│                 PostgreSQL                  │
└─────────────────────────────────────────────┘
```

---

# 20.4 Technology Stack

The initial technology stack should be:

| Layer                      | Technology                       |
| -------------------------- | -------------------------------- |
| Frontend                   | React                            |
| Frontend Language          | TypeScript                       |
| Backend                    | Django                           |
| API Framework              | Django REST Framework            |
| Database                   | PostgreSQL                       |
| Authentication             | JWT                              |
| API Documentation          | OpenAPI                          |
| Version Control            | Git / GitHub                     |
| Deployment                 | To be selected during deployment |
| Web Server / Reverse Proxy | To be selected during deployment |

The final versions of frameworks and packages should be selected according to the project's implementation environment.

---

# 20.5 Frontend Architecture

The frontend will provide the user interface used by Board's Cafe staff.

A component-based architecture should be used.

A possible structure is:

```text
frontend/
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── layouts/
│   ├── services/
│   ├── hooks/
│   ├── context/
│   ├── routes/
│   ├── types/
│   ├── utils/
│   └── assets/
│
└── ...
```

The exact structure may be adjusted during implementation.

---

# 20.6 Frontend Responsibilities

The frontend is responsible for:

* Displaying information.
* Collecting user input.
* Navigating between screens.
* Calling backend APIs.
* Displaying validation errors.
* Displaying success messages.
* Displaying notifications.
* Managing temporary UI state.
* Applying role-aware navigation.
* Presenting dashboards and reports.

The frontend must not be responsible for enforcing security by itself.

---

# 20.7 Backend Architecture

The backend will use Django and Django REST Framework.

The backend should be organized into domain-focused applications rather than putting all functionality into one application.

A possible structure is:

```text
backend/
│
├── config/
│
├── apps/
│   ├── users/
│   ├── roles/
│   ├── menu/
│   ├── recipes/
│   ├── inventory/
│   ├── suppliers/
│   ├── purchases/
│   ├── orders/
│   ├── payments/
│   ├── expenses/
│   ├── waste/
│   ├── notifications/
│   ├── reports/
│   └── audit_logs/
│
├── manage.py
└── ...
```

The exact Django app boundaries can be adjusted if implementation shows that some domains should be combined.

---

# 20.8 Layered Backend Design

The backend should separate different responsibilities.

```text
┌─────────────────────────────┐
│           Views             │
│        API Endpoints        │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│         Serializers         │
│ Validation / Transformation │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│       Service Layer         │
│       Business Logic        │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│           Models            │
│      Data / Relationships   │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│         PostgreSQL          │
└─────────────────────────────┘
```

This separation will make the system easier to maintain and test.

---

# 20.9 API Layer

Django REST Framework will provide the REST API.

The API will handle:

* Authentication.
* Request validation.
* Serialization.
* Authorization.
* Resource operations.
* Business-operation endpoints.
* Error responses.

The API will use versioning:

```text
/api/v1/
```

Example:

```text
/api/v1/orders/
/api/v1/inventory/items/
/api/v1/inventory/batches/
/api/v1/reports/sales/
```

---

# 20.10 Authentication Architecture

Authentication will use token-based authentication.

The general flow is:

```text
Staff Member
     │
     ▼
Login
     │
     ▼
Backend verifies credentials
     │
     ▼
Access + Refresh Tokens
     │
     ▼
Authenticated API Requests
```

The system should use secure password hashing provided by Django.

Passwords must never be stored as plain text.

---

# 20.11 Authorization Architecture

Authorization will use Role-Based Access Control (RBAC).

The initial system roles are:

1. Administrator
2. Manager
3. Cashier
4. Inventory Staff
5. Finance Staff

The authorization model is:

```text
User
  │
  ▼
Role
  │
  ▼
Permissions
```

A user may have one or more roles if the implementation requires it.

The backend will determine whether the authenticated user has permission to perform an operation.

---

# 20.12 Permission-Based API Security

A request should pass through the following checks:

```text
API Request
    ↓
Is user authenticated?
    ↓
      Yes
       ↓
Does user have required permission?
    ↓
      Yes
       ↓
Is request valid?
    ↓
      Yes
       ↓
Apply business rules
    ↓
Update database
    ↓
Return response
```

The frontend's hidden buttons or navigation items are not considered security controls.

---

# 20.13 Database Architecture

PostgreSQL will be used as the primary relational database.

The database will store:

* Users
* Roles
* Permissions
* Menu categories
* Menu products
* Recipes
* Recipe ingredients
* Inventory items
* Units
* Stock batches
* Stock movements
* Suppliers
* Purchases
* Purchase items
* Orders
* Order items
* Payments
* Expenses
* Waste records
* Notifications
* Audit logs

The detailed structure is defined in:

**Document 16 — Database Design**

and:

**Document 17 — ERD**

---

# 20.14 Inventory Architecture

Inventory is one of the core components of the system.

The architecture must distinguish between:

```text
Inventory Item
        ↓
Stock Batches
        ↓
Stock Movements
```

For example:

```text
Inventory Item:
Milk

Batches:

MILK-001 → 20 L → expires 10 Oct
MILK-002 → 30 L → expires 15 Oct
MILK-003 → 25 L → expires 20 Oct
```

The inventory item represents what the cafe stores.

The batch represents a specific quantity received at a particular time with its own expiry information.

---

# 20.15 Batch-Level Expiry Management

Expiry must be tracked at batch level.

The system should not simply store:

```text
Milk expires: 10 Oct
```

because different deliveries of milk may have different expiry dates.

Instead:

```text
Milk
 ├── Batch A → expires 10 Oct
 ├── Batch B → expires 15 Oct
 └── Batch C → expires 20 Oct
```

This architecture allows the system to identify exactly which stock is expired or approaching expiry.

---

# 20.16 FEFO Architecture

The system should support First-Expire, First-Out (FEFO) stock consumption where appropriate.

When an ingredient is required, the backend should:

1. Identify the inventory item.
2. Find eligible stock batches.
3. Exclude expired or unavailable stock.
4. Sort eligible batches by expiry date.
5. Consume the earliest-expiring stock first.
6. Continue to the next batch if necessary.
7. Create stock movement records.

Example:

```text
Required: 8 L Milk

Batch A → 3 L → expires 10 Oct
Batch B → 10 L → expires 15 Oct

Consumption:

Batch A → 3 L
Batch B → 5 L
```

---

# 20.17 Recipe Architecture

Recipes connect menu products to inventory items.

Example:

```text
Cappuccino
    │
    ├── Coffee
    └── Milk
```

Another product may use the same inventory item:

```text
Milk Tea
    │
    ├── Tea
    ├── Milk
    └── Sugar
```

This means one inventory item can be used by multiple products.

For example:

```text
Milk
 ├── Cappuccino
 ├── Milk Tea
 ├── Smoothie
 └── Other Products
```

This relationship is essential for accurate ingredient consumption.

---

# 20.18 Raw Materials and Ingredients

The inventory architecture must support both:

### Prepared/Menu Products

Products sold to customers, such as:

* Coffee
* Tea
* Sandwiches
* Cakes
* Smoothies
* Other cafe products

### Raw Materials / Ingredients

Items used to prepare products, such as:

* Milk
* Wheat flour
* Tomatoes
* Sugar
* Cooking oil
* Coffee
* Tea
* Eggs
* Vegetables
* Fruits
* Other ingredients

Raw materials are stored in inventory and can be linked to multiple recipes.

---

# 20.19 Made-to-Order Production

Board's Cafe may prepare certain products only after a customer places an order.

The architecture should therefore support production/ingredient consumption as part of the order workflow.

Example:

```text
Customer Order
      ↓
Order Confirmed
      ↓
Identify Ordered Products
      ↓
Retrieve Recipes
      ↓
Calculate Required Ingredients
      ↓
Check Available Stock
      ↓
Select Eligible Batches
      ↓
Consume Ingredients
      ↓
Prepare Product
      ↓
Complete Order
```

This avoids unnecessarily producing prepared products before there is a customer order.

---

# 20.20 Recipe-Based Consumption

Suppose one customer orders:

```text
2 × Sandwich
```

The recipe might require:

```text
2 slices bread
100 g flour
50 g tomatoes
20 g vegetables
```

The backend calculates:

```text
2 × recipe quantity
```

and determines the required inventory consumption.

The frontend should not manually calculate these values.

---

# 20.21 Shared Ingredient Architecture

The same inventory item can be used in multiple recipes.

Example:

```text
                 ┌── Cappuccino
                 │
Milk ────────────┼── Milk Tea
                 │
                 └── Smoothie
```

This means that selling any of these products can reduce the available milk stock.

The architecture must therefore maintain the relationship between:

```text
Menu Product
      ↓
Recipe
      ↓
Inventory Item
      ↓
Stock Batch
```

---

# 20.22 Order Architecture

Orders will connect customer purchases to menu products.

The basic relationship is:

```text
Order
  ↓
Order Items
  ↓
Menu Products
  ↓
Recipes
  ↓
Inventory Items
  ↓
Stock Batches
```

This creates traceability from a customer order to the inventory consumed to prepare it.

---

# 20.23 Transaction Management

Operations involving multiple database changes should use database transactions.

For example, completing an order may involve:

```text
Create/Update Order
        +
Create Order Items
        +
Calculate Ingredients
        +
Consume Stock
        +
Create Stock Movements
        +
Record Payment
        +
Create Audit Log
```

If a critical operation fails, the system should prevent a partially completed transaction where appropriate.

For example, it should not:

```text
Reduce stock
       ↓
Database error
       ↓
Order not completed
```

without properly handling the transaction.

---

# 20.24 Concurrency and Stock Protection

The system should consider concurrent stock operations.

For example:

```text
Cashier A → sells product
Cashier B → sells same product
```

Both operations may attempt to consume the same inventory at nearly the same time.

The backend should use appropriate database transaction and locking mechanisms to prevent stock from becoming incorrectly negative.

---

# 20.25 Purchase Architecture

Purchases provide stock to the cafe.

The general workflow is:

```text
Supplier
   ↓
Purchase
   ↓
Purchase Items
   ↓
Receive Stock
   ↓
Create Stock Batch
   ↓
Increase Available Stock
   ↓
Create Stock Movement
```

Where applicable, the received stock should include:

* Quantity
* Unit
* Cost
* Batch number
* Expiry date
* Supplier
* Receiving date

---

# 20.26 Waste Architecture

Waste is connected to inventory.

Example:

```text
Expired Milk
     ↓
Waste Record
     ↓
Stock Reduction
     ↓
Stock Movement
     ↓
Audit Log
```

Waste may be caused by:

* Expiry
* Spoilage
* Damage
* Spillage
* Preparation
* Other approved reasons

The system should maintain the reason for waste for reporting purposes.

---

# 20.27 Expiry Notification Architecture

The system should identify:

* Already expired batches.
* Batches approaching expiry.

The notification process may run periodically.

Example:

```text
Scheduled Check
      ↓
Find batches nearing expiry
      ↓
Create notification
      ↓
Notify authorized staff
```

The exact notification mechanism can be finalized during implementation.

---

# 20.28 Reporting Architecture

Reports should be generated from transactional data rather than manually entered summaries.

Examples:

```text
Orders ────────→ Sales Reports
Inventory ─────→ Inventory Reports
Batches ───────→ Expiry Reports
Waste ─────────→ Waste Reports
Purchases ─────→ Purchase Reports
Expenses ──────→ Expense Reports
Payments ──────→ Financial Reports
```

Reports should support filtering by relevant dates, categories, products, suppliers, and statuses.

---

# 20.29 Notification Architecture

Notifications may originate from events such as:

* Low stock.
* Expiring stock.
* Expired stock.
* Purchase received.
* Important order events.
* Other operational events.

Notifications should be targeted according to role and permission where appropriate.

For example:

```text
Low Stock
   ↓
Inventory Staff
Manager
Administrator
```

---

# 20.30 Audit Logging Architecture

Important actions should generate audit records.

Examples include:

* User creation.
* Role changes.
* Permission changes.
* Stock adjustments.
* Purchase receiving.
* Waste recording.
* Order cancellation.
* Expense creation.
* Important configuration changes.

Example:

```text
User: John
Action: STOCK_ADJUSTMENT
Resource: Milk Batch MILK-001
Time: 08 Oct 2026 10:30
```

Audit logs should generally be append-only from the application's normal user interface.

---

# 20.31 Data Flow

A typical order-to-inventory flow will be:

```text
Customer
   ↓
Cashier
   ↓
POS
   ↓
Order API
   ↓
Order Service
   ↓
Recipe Service
   ↓
Inventory Service
   ↓
FEFO Batch Selection
   ↓
Stock Consumption
   ↓
Stock Movement
   ↓
Order Completion
   ↓
Payment
   ↓
Audit Log
```

---

# 20.32 Inventory Data Flow

A purchase flow will be:

```text
Supplier
   ↓
Purchase
   ↓
Purchase Item
   ↓
Stock Receiving
   ↓
Batch Creation
   ↓
Inventory Quantity
   ↓
Stock Movement
   ↓
Expiry Monitoring
```

---

# 20.33 Expiry Data Flow

```text
Stock Batch Created
       ↓
Expiry Date Stored
       ↓
Periodic Expiry Check
       ↓
 ┌─────┴─────────┐
 ↓               ↓
Expired      Expiring Soon
 ↓               ↓
Alert           Alert
 ↓
Waste Recording
 ↓
Stock Movement
```

---

# 20.34 API and Database Separation

The frontend must never connect directly to PostgreSQL.

Correct:

```text
React
  ↓
REST API
  ↓
Django
  ↓
PostgreSQL
```

Incorrect:

```text
React
  ↓
PostgreSQL
```

All business operations should pass through the backend.

---

# 20.35 Configuration Management

Sensitive configuration should not be hard-coded into the source code.

Configuration may include:

* Database credentials.
* Secret keys.
* JWT settings.
* Email credentials.
* Notification credentials.
* Deployment-specific settings.

Environment variables or an appropriate secure configuration mechanism should be used.

---

# 20.36 Logging

The backend should maintain application logs for technical troubleshooting.

Logs may include:

* API errors.
* Authentication failures.
* System exceptions.
* Background task failures.
* Database errors.

Technical logs and business audit logs should be treated as separate concerns.

---

# 20.37 Error Handling Architecture

The backend should return consistent HTTP status codes.

Examples:

```text
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Unprocessable Entity
500 Internal Server Error
```

Business validation errors should be returned in a format that the frontend can display clearly.

---

# 20.38 Background Processing

Some operations may be performed outside normal user requests.

Potential background tasks include:

* Expiry checks.
* Low-stock checks.
* Notification generation.
* Periodic report preparation where needed.
* Other scheduled maintenance tasks.

The exact background task technology will be selected during implementation based on project requirements.

For the initial system, background processing should not be introduced unnecessarily if a simple scheduled mechanism is sufficient.

---

# 20.39 File and Image Storage

If the system later supports:

* Product images.
* User profile images.
* Supplier documents.
* Expense attachments.
* Other files.

These files should not be stored directly inside database fields as large binary objects unless there is a specific reason.

A suitable file-storage approach should be selected during implementation.

---

# 20.40 Deployment Architecture

A production deployment may use:

```text
                    Internet
                       │
                       ▼
                 HTTPS / Domain
                       │
                       ▼
              Reverse Proxy / Web Server
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
        React Frontend       Django API
                                 │
                                 ▼
                            PostgreSQL
```

The exact hosting provider and infrastructure will be determined before deployment.

---

# 20.41 Development Environment

Developers should be able to run the system locally.

Typical development setup:

```text
Developer Machine
       │
       ├── React Development Server
       │
       ├── Django Development Server
       │
       └── PostgreSQL
```

Environment-specific configuration should be separated from production configuration.

---

# 20.42 Version Control

Git will be used for source-code version control.

The repository should maintain:

* Main/production branch.
* Feature branches.
* Bug-fix branches where necessary.
* Documentation changes.
* Meaningful commits.

Sensitive information such as passwords, secret keys, and production credentials must never be committed to the repository.

---

# 20.43 Testing Architecture

The system should be tested at multiple levels.

### Unit Tests

Test individual functions and services.

Examples:

* Recipe ingredient calculation.
* FEFO selection.
* Permission checks.
* Stock calculations.

### API Tests

Test:

* Authentication.
* CRUD operations.
* Permissions.
* Validation.
* Error responses.

### Integration Tests

Test complete workflows.

Examples:

```text
Purchase → Receive → Batch → Inventory
```

and:

```text
Order → Recipe → Stock Consumption → Payment
```

### User Acceptance Testing

Staff should test real operational scenarios before the system is considered ready for production.

---

# 20.44 Security Architecture

Security should be applied at multiple levels.

```text
Browser
   ↓
HTTPS
   ↓
Authentication
   ↓
Authorization
   ↓
Input Validation
   ↓
Business Rules
   ↓
Database Constraints
   ↓
Audit Logging
```

Important security requirements are defined further in:

**Document 21 — Security Requirements**

---

# 20.45 Scalability Considerations

The initial architecture should be suitable for the operational needs of Board's Cafe while allowing future expansion.

Potential future additions may include:

* Multiple cafe branches.
* Mobile applications.
* Online ordering.
* Customer accounts.
* Delivery management.
* Advanced analytics.
* External payment integrations.
* Supplier integrations.

These should not complicate the initial implementation unnecessarily.

---

# 20.46 Architecture Principles

The implementation should follow these principles:

### Separation of Concerns

Each component should have a clear responsibility.

### Backend as Source of Truth

Important business rules must be enforced by the backend.

### Database Integrity

Critical relationships and constraints should be enforced at the database/model level.

### Least Privilege

Users should receive only the permissions required for their responsibilities.

### Auditability

Important business operations should be traceable.

### Transaction Safety

Related database operations should succeed or fail together where required.

### Simplicity

The architecture should avoid unnecessary technologies and complexity.

### Maintainability

Code should be organized so that future developers can understand and modify it.

---

# 20.47 Core System Architecture

The overall Board's Cafe architecture can be summarized as:

```text
                         BOARD'S CAFE
                              │
                              ▼
                     INTERNAL WEB APP
                              │
                         React / TS
                              │
                              ▼
                         REST API
                              │
                              ▼
                     Django REST Framework
                              │
          ┌───────────────────┼────────────────────┐
          │                   │                    │
          ▼                   ▼                    ▼
    Authentication       Authorization        Business Logic
          │                   │                    │
          └───────────────────┼────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
      Orders              Inventory             Finance
        │                     │                     │
        ▼                     ▼                     ▼
     Recipes              Batches               Payments
        │                     │
        ▼                     ▼
   Ingredients           Expiry / FEFO
        │                     │
        └───────────┬─────────┘
                    ▼
               PostgreSQL
                    │
        ┌───────────┼────────────┐
        ▼           ▼            ▼
      Reports   Notifications  Audit Logs
```

---

# 20.48 Final Architecture Decision

The Board's Cafe Management System will use a **React + TypeScript frontend, Django + Django REST Framework backend, and PostgreSQL database**, communicating through a versioned REST API.

The backend will be the central authority for:

* Authentication.
* Authorization.
* Roles and permissions.
* Orders.
* Recipe calculations.
* Inventory.
* Batch tracking.
* Expiry management.
* FEFO consumption.
* Purchases.
* Waste.
* Payments.
* Expenses.
* Notifications.
* Reports.
* Audit logging.

The architecture specifically supports the cafe's use of raw materials such as **milk, wheat flour, tomatoes, vegetables, sugar, coffee, and other ingredients** across multiple menu products.

For made-to-order products, the system can calculate ingredient requirements from recipes when an order is placed and consume the appropriate inventory batches according to the defined stock-consumption rules.

The system is intended primarily for **internal Board's Cafe staff**, with access controlled through the five defined roles:

```text
Administrator
Manager
Cashier
Inventory Staff
Finance Staff
```

---