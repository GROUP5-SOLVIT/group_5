# Board’s Cafe Management System

# 03 — Functional Requirements

## 3.1 Introduction

This document defines the functional requirements of the Board’s Cafe Management System.

The functional requirements describe what the system shall do to support the daily operations of Board’s Cafe.

The system is intended for internal staff and will provide role-based access to different functions.

The requirements are organized into the following functional areas:

1. Authentication and user access
2. User management
3. Roles and permissions
4. Dashboard
5. Menu product management
6. Recipe management
7. Inventory management
8. Batch and expiry management
9. POS and order management
10. Kitchen operations
11. Purchases and supplier management
12. Payment management
13. Expense management
14. Waste management
15. Reports
16. Notifications and alerts
17. Audit logging
18. System settings

---

# 3.2 Authentication Requirements

## FR-AUTH-001 — Staff Login

The system shall allow registered staff members to log in using valid authentication credentials.

## FR-AUTH-002 — Credential Validation

The system shall validate the credentials provided by a user before granting access.

## FR-AUTH-003 — Invalid Login

The system shall reject invalid login credentials and display an appropriate error message.

## FR-AUTH-004 — Account Status

The system shall prevent inactive or disabled users from logging into the system.

## FR-AUTH-005 — Logout

The system shall allow authenticated users to log out of the system.

## FR-AUTH-006 — Protected Resources

The system shall require authentication before allowing access to protected system functions.

## FR-AUTH-007 — Session Security

The system shall securely manage authenticated sessions or authentication tokens.

## FR-AUTH-008 — Password Security

The system shall store user passwords securely and shall never store passwords as plain text.

## FR-AUTH-009 — Password Change

The system shall allow authorized users to change their own passwords.

## FR-AUTH-010 — Password Reset

Authorized administrators shall be able to reset a user's password according to the system's password-management process.

---

# 3.3 User Management Requirements

## FR-USER-001 — Create User

An authorized administrator shall be able to create a staff account.

## FR-USER-002 — User Information

The system shall store relevant staff information such as:

* Name
* Username or email
* Contact information where required
* Account status
* Assigned role
* Creation date

## FR-USER-003 — View Users

Authorized administrators shall be able to view registered staff accounts.

## FR-USER-004 — Update User

Authorized administrators shall be able to update staff account information.

## FR-USER-005 — Activate User

An authorized administrator shall be able to activate a user account.

## FR-USER-006 — Deactivate User

An authorized administrator shall be able to deactivate a user account.

## FR-USER-007 — User Search

Authorized users shall be able to search for staff accounts where the permission is provided.

## FR-USER-008 — User History

The system shall preserve relevant historical records associated with a user even when that user becomes inactive.

## FR-USER-009 — User Role Assignment

An authorized administrator shall be able to assign a role to a staff member.

## FR-USER-010 — Role Change

An authorized administrator shall be able to change the role assigned to a staff member.

---

# 3.4 Role and Permission Requirements

The system shall use Role-Based Access Control (RBAC).

The basic access structure shall be:

```text
User
  ↓
Role
  ↓
Permission
  ↓
Allowed Action
```

## FR-RBAC-001 — Roles

The system shall support user roles.

## FR-RBAC-002 — Permissions

The system shall support individual permissions.

## FR-RBAC-003 — Role Permissions

A role shall be associated with one or more permissions.

## FR-RBAC-004 — User Roles

A user shall be associated with one or more roles where required by the system design.

## FR-RBAC-005 — Create Role

An authorized administrator shall be able to create a role.

## FR-RBAC-006 — Update Role

An authorized administrator shall be able to update a role.

## FR-RBAC-007 — Assign Permissions

An authorized administrator shall be able to assign permissions to a role.

## FR-RBAC-008 — Remove Permissions

An authorized administrator shall be able to remove permissions from a role.

## FR-RBAC-009 — Permission Enforcement

The system shall check a user's permissions before allowing protected actions.

## FR-RBAC-010 — Privilege Escalation Protection

A user shall not be able to grant themselves permissions they do not have.

## FR-RBAC-011 — Administrative Protection

Only users with the required administrative permission shall be able to manage users, roles, and permissions.

---

# 3.5 Dashboard Requirements

## FR-DASH-001 — Dashboard Access

The system shall provide a dashboard to authorized users.

## FR-DASH-002 — Sales Summary

The dashboard shall display permitted sales information.

## FR-DASH-003 — Order Summary

The dashboard shall display relevant order information.

## FR-DASH-004 — Inventory Summary

The dashboard shall display relevant inventory information.

## FR-DASH-005 — Expiry Summary

The dashboard shall display:

* Expiring-soon stock
* Expired stock

## FR-DASH-006 — Low Stock

The dashboard shall identify inventory items that have reached their configured low-stock level.

## FR-DASH-007 — Waste Summary

Authorized users shall be able to view relevant waste information.

## FR-DASH-008 — Pending Orders

Authorized users shall be able to see orders that require attention.

## FR-DASH-009 — Role-Based Dashboard

Dashboard information shall be limited according to the user's permissions.

---

# 3.6 Menu Category Requirements

## FR-CAT-001 — Create Category

Authorized users shall be able to create a menu category.

## FR-CAT-002 — View Categories

Authorized users shall be able to view menu categories.

## FR-CAT-003 — Update Category

Authorized users with the required permission shall be able to update a category.

## FR-CAT-004 — Deactivate Category

Authorized users shall be able to deactivate a category where permitted.

## FR-CAT-005 — Category Products

The system shall allow menu products to be associated with menu categories.

---

# 3.7 Menu Product Requirements

## FR-PROD-001 — Create Product

Authorized users shall be able to create a menu product.

## FR-PROD-002 — Product Information

A menu product shall support information such as:

* Product name
* Category
* Description
* Selling price
* Availability status
* Product image where required

## FR-PROD-003 — View Products

Authorized users shall be able to view menu products.

## FR-PROD-004 — Update Product

Authorized users shall be able to update menu product information.

## FR-PROD-005 — Product Price

Authorized users with the required permission shall be able to change a product's selling price.

## FR-PROD-006 — Product Availability

Authorized users shall be able to mark a product as available or unavailable.

## FR-PROD-007 — Product Deactivation

The system shall allow a product to be deactivated without unnecessarily deleting historical order information.

## FR-PROD-008 — Product Search

Authorized users shall be able to search menu products.

---

# 3.8 Recipe Requirements

## FR-REC-001 — Create Recipe

Authorized users shall be able to create a recipe for a menu product.

## FR-REC-002 — Recipe Ingredients

A recipe shall allow multiple ingredients to be defined.

## FR-REC-003 — Ingredient Quantity

The system shall record the quantity of each ingredient required by a recipe.

## FR-REC-004 — Measurement Unit

The system shall record the appropriate measurement unit for recipe quantities.

Examples include:

* g
* kg
* ml
* L
* piece

## FR-REC-005 — Shared Ingredients

The system shall allow the same inventory ingredient to be used in multiple recipes.

For example:

```text
Milk
 ├── Cappuccino
 ├── Latte
 ├── Pancake
 └── Cake
```

## FR-REC-006 — Recipe Update

Authorized users shall be able to update a recipe.

## FR-REC-007 — Recipe Validation

The system shall validate that required recipe ingredients and quantities are provided.

## FR-REC-008 — Recipe Usage

The system shall use the configured recipe to determine the ingredients required for preparation.

## FR-REC-009 — Recipe Traceability

The system should maintain sufficient information to determine which recipe configuration was used for a relevant preparation or consumption transaction.

---

# 3.9 Inventory Item Requirements

## FR-INV-001 — Create Inventory Item

Authorized users shall be able to create an inventory item.

## FR-INV-002 — Inventory Information

An inventory item shall support information such as:

* Name
* Description
* Unit of measurement
* Minimum stock level
* Active status

## FR-INV-003 — View Inventory

Authorized users shall be able to view inventory.

## FR-INV-004 — Update Inventory Item

Authorized users shall be able to update inventory item information.

## FR-INV-005 — Inventory Search

Authorized users shall be able to search inventory items.

## FR-INV-006 — Inventory Quantity

The system shall provide the available quantity of inventory items.

## FR-INV-007 — Low Stock Detection

The system shall identify inventory items whose available quantity is below the configured minimum stock level.

## FR-INV-008 — Inventory Status

The system shall provide appropriate inventory status information.

---

# 3.10 Inventory Batch Requirements

## FR-BATCH-001 — Create Batch

The system shall allow an inventory batch to be recorded when stock is received.

## FR-BATCH-002 — Batch Number

The system shall support batch numbers where applicable.

## FR-BATCH-003 — Batch Quantity

The system shall record the quantity received for each batch.

## FR-BATCH-004 — Remaining Quantity

The system shall maintain or calculate the remaining usable quantity of each batch.

## FR-BATCH-005 — Received Date

The system shall record the date on which a batch was received.

## FR-BATCH-006 — Expiry Date

The system shall record the expiry date for items that have an expiry date.

## FR-BATCH-007 — Unit Cost

The system shall record the applicable unit cost for received stock.

## FR-BATCH-008 — Batch Status

The system shall maintain the status of a batch.

Possible statuses include:

* Valid
* Expiring Soon
* Expired
* Depleted
* Blocked

## FR-BATCH-009 — Multiple Batches

The system shall allow one inventory item to have multiple batches.

## FR-BATCH-010 — Batch Traceability

The system shall maintain the relationship between a batch and the transaction through which it was received.

---

# 3.11 Expiry Management Requirements

## FR-EXP-001 — Expiry Monitoring

The system shall monitor expiry dates for inventory batches.

## FR-EXP-002 — Expiring Soon

The system shall identify batches approaching their expiry date.

## FR-EXP-003 — Expired Stock

The system shall identify batches whose expiry date has passed.

## FR-EXP-004 — Expired Stock Protection

The system shall prevent expired inventory from being selected for normal recipe consumption.

## FR-EXP-005 — Expiry Warning

The system shall notify authorized staff when stock is approaching expiry according to the configured warning period.

## FR-EXP-006 — Expired Notification

The system shall notify authorized staff when stock becomes expired.

## FR-EXP-007 — Expiry Report

Authorized users shall be able to view a list of expired and expiring-soon batches.

## FR-EXP-008 — Expiry Value

Where sufficient cost information exists, the system shall calculate the estimated value of stock at risk from expiry.

## FR-EXP-009 — FEFO Selection

When inventory is consumed, the system shall prioritize valid batches according to the earliest expiry date where applicable.

## FR-EXP-010 — Expiry Waste

Authorized staff shall be able to record expired stock as waste.

---

# 3.12 Stock Movement Requirements

## FR-STK-001 — Record Stock Movement

The system shall record important inventory quantity changes as stock movements.

## FR-STK-002 — Stock Addition

The system shall record stock received through purchases.

## FR-STK-003 — Stock Consumption

The system shall record stock consumed during preparation.

## FR-STK-004 — Stock Waste

The system shall record stock removed because of waste.

## FR-STK-005 — Stock Adjustment

Authorized users shall be able to perform stock adjustments.

## FR-STK-006 — Movement Quantity

Each stock movement shall record the quantity affected.

## FR-STK-007 — Movement Type

Each stock movement shall have an appropriate movement type.

Examples:

* Purchase
* Consumption
* Waste
* Adjustment
* Return
* Correction

## FR-STK-008 — Movement Reference

Where applicable, a stock movement shall reference the business transaction that caused it.

## FR-STK-009 — Movement User

The system shall record the staff member responsible for an applicable manual stock movement.

## FR-STK-010 — Movement Timestamp

The system shall record when a stock movement occurred.

---

# 3.13 POS and Order Requirements

## FR-ORD-001 — Create Order

Authorized staff shall be able to create a customer order.

## FR-ORD-002 — Add Order Items

Staff shall be able to add one or more menu products to an order.

## FR-ORD-003 — Quantity

Staff shall be able to specify the quantity of each ordered product.

## FR-ORD-004 — Price

The system shall record the applicable selling price for each order item.

## FR-ORD-005 — Order Total

The system shall calculate the order total.

## FR-ORD-006 — Order Status

The system shall maintain the status of an order.

Possible statuses include:

* Draft
* Confirmed
* Preparing
* Ready
* Completed
* Cancelled
* Refunded

## FR-ORD-007 — Confirm Order

Authorized staff shall be able to confirm an order.

## FR-ORD-008 — Cancel Order

Authorized staff shall be able to cancel an order according to their permissions.

## FR-ORD-009 — Order History

Authorized users shall be able to view relevant order history.

## FR-ORD-010 — Order Search

Authorized users shall be able to search orders.

## FR-ORD-011 — Order User

The system shall record the staff member responsible for creating an order.

## FR-ORD-012 — Order Timestamp

The system shall record the relevant order dates and times.

---

# 3.14 Kitchen Requirements

## FR-KIT-001 — View Incoming Orders

Authorized kitchen staff shall be able to view confirmed orders requiring preparation.

## FR-KIT-002 — Start Preparation

Kitchen staff with the required permission shall be able to mark an order as being prepared.

## FR-KIT-003 — Preparation Status

The system shall display the preparation status of relevant orders.

## FR-KIT-004 — Mark Ready

Kitchen staff shall be able to mark a prepared order as ready.

## FR-KIT-005 — Recipe Requirements

The system shall use the appropriate recipe to determine ingredient requirements for preparation.

## FR-KIT-006 — Ingredient Availability

Before consuming inventory, the system should check whether sufficient valid ingredients are available.

## FR-KIT-007 — Inventory Consumption

When the defined consumption event occurs, the system shall record the required ingredient consumption.

## FR-KIT-008 — Batch Selection

Where multiple valid batches exist, the system shall select stock according to FEFO where applicable.

---

# 3.15 Ingredient Consumption Requirements

This is an important connection between the **sales process and inventory process**.

## FR-CONS-001 — Calculate Consumption

The system shall calculate required ingredient quantities based on the recipe and ordered quantity.

For example:

```text
Cappuccino Recipe
Milk = 150 ml

Order Quantity = 3

Required Milk:
150 ml × 3
= 450 ml
```

## FR-CONS-002 — Multiple Ingredients

The system shall calculate all required ingredients for the ordered products.

## FR-CONS-003 — Shared Ingredient Calculation

The system shall combine consumption of the same ingredient when multiple ordered products use that ingredient.

## FR-CONS-004 — Valid Stock

The system shall consume only valid inventory.

## FR-CONS-005 — Expired Stock Exclusion

Expired batches shall not be used for normal consumption.

## FR-CONS-006 — Batch-Level Consumption

Where applicable, consumption shall identify the inventory batch from which the stock was taken.

## FR-CONS-007 — Consumption Record

The system shall create a record of ingredient consumption.

## FR-CONS-008 — Consumption Reference

Ingredient consumption should be traceable to the relevant order or preparation transaction.

---

# 3.16 Purchase Requirements

## FR-PUR-001 — Create Supplier

Authorized users shall be able to create a supplier.

## FR-PUR-002 — Supplier Information

The system shall store relevant supplier information.

## FR-PUR-003 — View Suppliers

Authorized users shall be able to view suppliers.

## FR-PUR-004 — Update Supplier

Authorized users shall be able to update supplier information.

## FR-PUR-005 — Create Purchase

Authorized users shall be able to create a purchase.

## FR-PUR-006 — Purchase Items

A purchase shall contain one or more purchased items.

## FR-PUR-007 — Purchase Quantity

The system shall record the quantity purchased.

## FR-PUR-008 — Purchase Cost

The system shall record the applicable purchase cost.

## FR-PUR-009 — Receive Stock

Authorized users shall be able to record received stock.

## FR-PUR-010 — Batch Creation

Receiving applicable stock shall create or record the corresponding inventory batch.

## FR-PUR-011 — Expiry on Receipt

Where applicable, the expiry date shall be captured when stock is received.

## FR-PUR-012 — Inventory Update

Receiving stock shall increase the appropriate inventory quantity.

## FR-PUR-013 — Purchase History

Authorized users shall be able to view purchase history.

---

# 3.17 Payment Requirements

## FR-PAY-001 — Record Payment

Authorized staff shall be able to record a payment for an order.

## FR-PAY-002 — Payment Amount

The system shall record the payment amount.

## FR-PAY-003 — Payment Method

The system shall record the payment method.

## FR-PAY-004 — Payment Status

The system shall maintain payment status.

Possible statuses include:

* Pending
* Paid
* Partially Paid
* Failed
* Refunded

## FR-PAY-005 — Payment Date

The system shall record the payment date and time.

## FR-PAY-006 — Payment User

The system shall record the staff member who recorded the payment.

## FR-PAY-007 — Order Relationship

Each payment shall remain linked to its associated order.

## FR-PAY-008 — Multiple Payments

The system should support multiple payments for one order if Board’s Cafe requires partial or split payments.

---

# 3.18 Refund Requirements

## FR-REF-001 — Refund Authorization

Only authorized users shall be able to process refunds.

## FR-REF-002 — Original Order

A refund shall reference the original order.

## FR-REF-003 — Refund Amount

The system shall record the refunded amount.

## FR-REF-004 — Refund Reason

The system shall record the reason for the refund.

## FR-REF-005 — Refund Traceability

Refund activity shall be recorded for audit purposes.

---

# 3.19 Expense Requirements

## FR-EXPENSE-001 — Create Expense

Authorized users shall be able to record an expense.

## FR-EXPENSE-002 — Expense Category

Each expense shall be associated with an expense category.

## FR-EXPENSE-003 — Expense Amount

The system shall record the expense amount.

## FR-EXPENSE-004 — Expense Date

The system shall record the date of the expense.

## FR-EXPENSE-005 — Expense Description

The system shall allow staff to provide an expense description or note.

## FR-EXPENSE-006 — Expense User

The system shall record the staff member who recorded the expense.

## FR-EXPENSE-007 — Expense History

Authorized users shall be able to view expense history.

## FR-EXPENSE-008 — Expense Reports

Authorized users shall be able to generate expense reports.

---

# 3.20 Waste Requirements

## FR-WASTE-001 — Record Waste

Authorized staff shall be able to record wasted inventory.

## FR-WASTE-002 — Waste Item

The waste record shall identify the affected inventory item.

## FR-WASTE-003 — Waste Batch

Where applicable, the waste record shall identify the affected batch.

## FR-WASTE-004 — Waste Quantity

The system shall record the quantity wasted.

## FR-WASTE-005 — Waste Reason

The system shall record the reason for waste.

Possible reasons include:

* Expired
* Spoiled
* Damaged
* Incorrect preparation
* Accidental loss
* Other

## FR-WASTE-006 — Inventory Reduction

Recording confirmed waste shall reduce the appropriate available inventory quantity.

## FR-WASTE-007 — Stock Movement

The system shall create a corresponding stock movement for confirmed waste.

## FR-WASTE-008 — Waste User

The system shall record the staff member who recorded the waste.

## FR-WASTE-009 — Waste Reports

Authorized users shall be able to view waste reports.

---

# 3.21 Reporting Requirements

## FR-REPORT-001 — Sales Reports

The system shall provide sales reports.

## FR-REPORT-002 — Order Reports

The system shall provide order reports.

## FR-REPORT-003 — Inventory Reports

The system shall provide inventory reports.

## FR-REPORT-004 — Stock Movement Reports

The system shall provide stock movement reports.

## FR-REPORT-005 — Expiry Reports

The system shall provide expiry reports.

## FR-REPORT-006 — Purchase Reports

The system shall provide purchase reports.

## FR-REPORT-007 — Supplier Reports

The system shall provide supplier-related reports.

## FR-REPORT-008 — Expense Reports

The system shall provide expense reports.

## FR-REPORT-009 — Waste Reports

The system shall provide waste reports.

## FR-REPORT-010 — Payment Reports

The system shall provide payment reports.

## FR-REPORT-011 — Ingredient Consumption Reports

The system shall provide ingredient consumption information.

## FR-REPORT-012 — Date Filtering

Authorized users shall be able to filter reports by relevant date ranges.

## FR-REPORT-013 — Product Filtering

Authorized users shall be able to filter applicable reports by product.

## FR-REPORT-014 — Inventory Filtering

Authorized users shall be able to filter applicable reports by inventory item.

## FR-REPORT-015 — Export

Authorized users may be able to export reports in supported formats.

---

# 3.22 Notification Requirements

## FR-NOTIF-001 — Create Notification

The system shall create notifications for configured business events.

## FR-NOTIF-002 — Expiry Notification

The system shall notify authorized staff when inventory approaches expiry.

## FR-NOTIF-003 — Expired Notification

The system shall notify authorized staff when inventory becomes expired.

## FR-NOTIF-004 — Low Stock Notification

The system shall notify authorized staff when inventory reaches a configured low-stock threshold.

## FR-NOTIF-005 — Order Notification

The system shall notify relevant staff when a new order requires their attention.

## FR-NOTIF-006 — Notification Status

The system shall maintain whether a notification has been read.

## FR-NOTIF-007 — Notification Recipient

Each notification shall identify its intended recipient or target staff group.

---

# 3.23 Audit Logging Requirements

## FR-AUDIT-001 — Record Sensitive Actions

The system shall record important and sensitive user actions.

## FR-AUDIT-002 — User Identification

An audit record shall identify the user who performed the action where applicable.

## FR-AUDIT-003 — Action

The audit record shall identify the action performed.

## FR-AUDIT-004 — Timestamp

The audit record shall contain the date and time of the action.

## FR-AUDIT-005 — Affected Record

Where applicable, the audit record shall identify the affected business record.

## FR-AUDIT-006 — Stock Audit

Stock adjustments, waste, and other sensitive inventory changes shall be auditable.

## FR-AUDIT-007 — Access Management Audit

Changes to users, roles, and permissions shall be auditable.

## FR-AUDIT-008 — Financial Audit

Important financial activities such as refunds and expense changes shall be auditable.

---

# 3.24 Search and Filtering Requirements

## FR-SEARCH-001 — Global Module Search

Where appropriate, authorized users shall be able to search records within system modules.

## FR-SEARCH-002 — Product Search

Staff shall be able to search menu products.

## FR-SEARCH-003 — Inventory Search

Staff shall be able to search inventory items.

## FR-SEARCH-004 — Order Search

Authorized staff shall be able to search orders.

## FR-SEARCH-005 — Supplier Search

Authorized users shall be able to search suppliers.

## FR-SEARCH-006 — Date Filtering

Transactions shall support date-based filtering where appropriate.

## FR-SEARCH-007 — Status Filtering

Users shall be able to filter applicable records by status.

---

# 3.25 System Settings Requirements

## FR-SET-001 — Business Configuration

Authorized administrators shall be able to configure applicable system settings.

## FR-SET-002 — Expiry Warning Period

Authorized administrators shall be able to configure the period used to identify stock approaching expiry.

## FR-SET-003 — Low Stock Threshold

The system shall support configurable minimum stock levels.

## FR-SET-004 — Payment Methods

Authorized administrators shall be able to configure supported payment methods where required.

## FR-SET-005 — Waste Reasons

Authorized administrators may configure supported waste reasons.

## FR-SET-006 — Measurement Units

The system shall support appropriate inventory and recipe measurement units.

---

# 3.26 Data Validation Requirements

## FR-VAL-001 — Required Fields

The system shall validate required fields before saving records.

## FR-VAL-002 — Numeric Values

Quantities and monetary values shall accept only valid numeric values.

## FR-VAL-003 — Positive Quantities

Inventory, recipe, purchase, and order quantities shall not accept invalid negative values unless the operation explicitly represents a stock reduction or adjustment.

## FR-VAL-004 — Expiry Date

Where applicable, the system shall validate expiry dates.

## FR-VAL-005 — Duplicate Records

The system shall prevent inappropriate duplicate records where uniqueness is required.

## FR-VAL-006 — Referential Integrity

The system shall maintain valid relationships between related records.

---

# 3.27 Transaction Integrity Requirements

## FR-TRANS-001 — Atomic Inventory Operations

Operations that change multiple related inventory records shall be processed consistently.

For example:

```text
Consume Ingredient
      ↓
Reduce Batch Quantity
      ↓
Create Consumption Record
      ↓
Create Stock Movement
```

These operations should not leave the database in a partially completed state.

## FR-TRANS-002 — Purchase Receipt

Receiving stock shall consistently update:

* Purchase information.
* Batch information.
* Inventory quantity.
* Stock movement.

## FR-TRANS-003 — Waste Confirmation

Confirming waste shall consistently update:

* Waste record.
* Batch quantity.
* Inventory availability.
* Stock movement.

## FR-TRANS-004 — Order Consumption

Ingredient consumption shall consistently update:

* Consumption record.
* Inventory batch quantity.
* Stock movement.

---

# 3.28 Historical Data Requirements

## FR-HIST-001 — Preserve Transactions

Completed transactions shall not be unnecessarily deleted.

## FR-HIST-002 — Inactive Products

A deactivated menu product shall remain available in historical orders.

## FR-HIST-003 — Inactive Users

Deactivated staff accounts shall remain associated with historical records where appropriate.

## FR-HIST-004 — Stock History

Stock movement history shall remain available to authorized users.

## FR-HIST-005 — Financial History

Completed financial records shall remain available according to the system's retention rules.

---

# 3.29 Functional Requirement Summary

The Board’s Cafe Management System shall connect its major operations as follows:

```text
                         ┌──────────────┐
                         │    USERS     │
                         └──────┬───────┘
                                │
                         Roles & Permissions
                                │
                                ▼
┌─────────────┐          ┌─────────────┐
│   PRODUCTS  │─────────►│   RECIPES   │
└──────┬──────┘          └──────┬──────┘
       │                        │
       │                        ▼
       │                ┌───────────────┐
       │                │   INGREDIENTS │
       │                └───────┬───────┘
       │                        │
       │                        ▼
       │                ┌───────────────┐
       │                │    BATCHES    │
       │                └───────┬───────┘
       │                        │
       │                  Expiry / FEFO
       │                        │
       ▼                        ▼
┌─────────────┐          ┌───────────────┐
│    ORDER    │─────────►│  CONSUMPTION  │
└──────┬──────┘          └───────┬───────┘
       │                         │
       ├────────► PAYMENT        ▼
       │                  STOCK MOVEMENT
       │
       ▼
   KITCHEN
       │
       ▼
   COMPLETED


SUPPLIER
    │
    ▼
 PURCHASE
    │
    ▼
 RECEIVED STOCK
    │
    ▼
 INVENTORY / BATCH


INVENTORY
    │
    ├──► EXPIRY
    ├──► WASTE
    └──► STOCK MOVEMENT


ALL IMPORTANT ACTIVITIES
           │
           ▼
       AUDIT LOGS
           │
           ▼
        REPORTS
```

---

# 3.30 Core Functional Principle

The most important functional relationship in the system is:

**Customer Order → Menu Product → Recipe → Ingredient → Valid Batch → Consumption → Stock Movement**

This ensures that when Board’s Cafe sells a prepared product, the system can determine what ingredients were required and what stock was consumed.

At the same time, the inventory system continuously monitors:

**Available Stock → Batch → Expiry Date → FEFO → Alerts → Waste**

This allows Board’s Cafe to identify and act on expiring products before they become unnecessary losses.
