# Board’s Cafe Management System

# 04 — User Roles and Permissions

## 4.1 Introduction

The Board’s Cafe Management System is an internal staff system. Because different staff members have different responsibilities, the system shall use **Role-Based Access Control (RBAC)** to control access to system functions.

A user is assigned a role, and the role determines the permissions available to that user.

The access structure is:

```text
User
  ↓
Role
  ↓
Permissions
  ↓
System Actions
```

The system shall ensure that staff members can only perform actions that are permitted for their assigned role.

---

# 4.2 Objectives

The role and permission system shall:

* Protect sensitive business information.
* Prevent unauthorized actions.
* Separate responsibilities between staff members.
* Allow administrators to manage staff access.
* Support different levels of access.
* Make permissions easy to manage as the cafe grows.
* Provide an audit trail for important access-management actions.

---

# 4.3 User Account

A **User** represents an individual staff member who can access the system.

Each user account shall have information such as:

* Full name
* Username or email
* Password
* Account status
* Assigned role
* Date created
* Last login information where required

A user may be:

```text
Active
Inactive
```

Inactive users shall not be allowed to access protected system functions.

---

# 4.4 Roles

A **Role** represents a set of responsibilities within Board’s Cafe.

The initial roles are:

1. Administrator
2. Manager
3. Cashier
4. Waiter
5. Kitchen Staff
6. Storekeeper

The system should be designed so that additional roles can be introduced later without changing the core application architecture.

---

# 4.5 Administrator

The Administrator is responsible for system administration and access control.

### Main responsibilities

The Administrator can:

* Manage staff accounts.
* Assign roles.
* Manage permissions.
* Manage system settings.
* Manage products and recipes.
* Manage inventory.
* Manage purchases.
* Manage expenses.
* Manage waste.
* View reports.
* View audit logs.
* Manage other system functions according to assigned administrative permissions.

### Administrative permissions

```text
User Management
Role Management
Permission Management
System Settings
Audit Log Access
```

The Administrator shall have the highest level of system access.

However, administrative access should still be implemented through explicit permissions rather than relying only on a hard-coded "admin" condition.

---

# 4.6 Manager

The Manager is responsible for supervising cafe operations and monitoring business performance.

### Main responsibilities

The Manager can:

* View operational dashboards.
* Manage menu products where permitted.
* Manage recipes where permitted.
* Monitor inventory.
* Monitor expiring stock.
* Manage or review purchases.
* Monitor suppliers.
* Review expenses.
* Review waste.
* Monitor orders.
* Review payments.
* View operational and financial reports.
* Approve selected sensitive operations where configured.

The Manager should not automatically have access to system administration functions such as creating users or modifying security permissions unless explicitly granted.

---

# 4.7 Cashier

The Cashier primarily handles customer orders and payments.

### Main responsibilities

The Cashier can:

* Create orders.
* Add products to orders.
* Update an order before confirmation where permitted.
* Confirm orders.
* Process payments.
* View relevant order history.
* Search orders.
* Print or display receipts where supported.
* Cancel orders where authorized.

The Cashier should not normally:

* Manage users.
* Manage roles.
* Change permissions.
* Change recipes.
* Adjust inventory directly.
* Modify purchase records.
* Modify expenses.

---

# 4.8 Waiter

The Waiter primarily handles customer-facing order entry.

### Main responsibilities

The Waiter can:

* Create customer orders.
* Add menu products.
* Specify quantities.
* Add order notes where supported.
* Submit orders for preparation.
* View the status of their orders.
* View relevant product information.

The Waiter should not normally:

* Manage inventory.
* Manage recipes.
* Manage purchases.
* Manage expenses.
* Process refunds unless explicitly authorized.
* Manage users or permissions.

---

# 4.9 Kitchen Staff

Kitchen Staff are responsible for preparing customer orders.

### Main responsibilities

Kitchen Staff can:

* View confirmed orders.
* View order items.
* View preparation instructions.
* Start preparation.
* Update preparation status.
* Mark orders as ready.
* Report preparation-related waste where authorized.
* View relevant ingredient information.

Kitchen Staff should not normally:

* Change product selling prices.
* Manage users.
* Manage roles.
* Manage suppliers.
* Create purchases.
* Manage financial records.

---

# 4.10 Storekeeper

The Storekeeper is responsible for physical stock and inventory operations.

### Main responsibilities

The Storekeeper can:

* View inventory.
* Receive stock.
* Record inventory batches.
* Record batch expiry dates.
* Monitor expiring stock.
* Record stock movements.
* Perform authorized stock adjustments.
* Record waste.
* Monitor low stock.
* View suppliers and purchases where required.

The Storekeeper should not normally:

* Manage users.
* Change roles.
* Process customer payments.
* Change menu prices.
* Modify financial records unless explicitly authorized.

---

# 4.11 Permission Model

Permissions shall be separated from roles.

A permission represents a specific action that a user is allowed to perform.

The basic CRUD permissions are:

```text
View
Create
Update
Delete
```

However, business operations require additional permissions.

Therefore, the system shall also support permissions such as:

```text
Approve
Cancel
Receive
Consume
Adjust
Refund
Export
Manage
```

For example:

```text
inventory.view
inventory.create
inventory.update
inventory.adjust
inventory.receive
inventory.consume
inventory.delete
```

This provides more precise access control than simply giving a user access to an entire module.

---

# 4.12 Permission Naming Convention

Permissions should follow a consistent structure:

```text
module.action
```

Examples:

```text
users.view
users.create
users.update
users.deactivate

products.view
products.create
products.update
products.delete

recipes.view
recipes.create
recipes.update
recipes.delete

inventory.view
inventory.receive
inventory.adjust
inventory.consume

orders.view
orders.create
orders.update
orders.cancel

payments.view
payments.create
payments.refund
```

This structure will also make the permissions easier to use in the API.

---

# 4.13 User Management Permissions

| Permission             | Purpose                  |
| ---------------------- | ------------------------ |
| `users.view`           | View staff accounts      |
| `users.create`         | Create staff accounts    |
| `users.update`         | Update staff information |
| `users.deactivate`     | Disable staff accounts   |
| `users.activate`       | Activate staff accounts  |
| `users.reset_password` | Reset a staff password   |
| `users.assign_role`    | Assign a role to a user  |

---

# 4.14 Role and Permission Management

| Permission                 | Purpose                                 |
| -------------------------- | --------------------------------------- |
| `roles.view`               | View roles                              |
| `roles.create`             | Create roles                            |
| `roles.update`             | Update roles                            |
| `roles.delete`             | Delete/deactivate roles where permitted |
| `roles.assign_permissions` | Assign permissions to roles             |
| `permissions.view`         | View available permissions              |
| `permissions.manage`       | Manage the permission configuration     |

Only highly authorized administrators should have these permissions.

---

# 4.15 Product Permissions

| Permission               | Purpose                      |
| ------------------------ | ---------------------------- |
| `products.view`          | View menu products           |
| `products.create`        | Create products              |
| `products.update`        | Update products              |
| `products.delete`        | Delete/deactivate products   |
| `products.change_price`  | Change selling price         |
| `products.change_status` | Activate/deactivate products |

---

# 4.16 Category Permissions

| Permission          | Purpose                      |
| ------------------- | ---------------------------- |
| `categories.view`   | View categories              |
| `categories.create` | Create categories            |
| `categories.update` | Update categories            |
| `categories.delete` | Delete/deactivate categories |

---

# 4.17 Recipe Permissions

| Permission       | Purpose                   |
| ---------------- | ------------------------- |
| `recipes.view`   | View recipes              |
| `recipes.create` | Create recipes            |
| `recipes.update` | Update recipes            |
| `recipes.delete` | Delete/deactivate recipes |

Changing recipes can affect ingredient consumption, so recipe modification should be restricted to authorized staff.

---

# 4.18 Inventory Permissions

| Permission           | Purpose                                             |
| -------------------- | --------------------------------------------------- |
| `inventory.view`     | View inventory                                      |
| `inventory.create`   | Create inventory items                              |
| `inventory.update`   | Update inventory information                        |
| `inventory.receive`  | Receive stock                                       |
| `inventory.adjust`   | Adjust stock                                        |
| `inventory.consume`  | Record inventory consumption                        |
| `inventory.transfer` | Transfer stock where supported                      |
| `inventory.delete`   | Delete/deactivate inventory records where permitted |

Direct stock adjustment should be treated as a sensitive operation.

---

# 4.19 Batch and Expiry Permissions

| Permission              | Purpose                                  |
| ----------------------- | ---------------------------------------- |
| `batches.view`          | View batches                             |
| `batches.create`        | Create batches                           |
| `batches.update`        | Update batch information                 |
| `batches.expiry.view`   | View expiry information                  |
| `batches.expiry.manage` | Manage expiry-related information        |
| `batches.block`         | Block a batch from normal use            |
| `batches.release`       | Release a blocked batch where authorized |

The system shall not allow ordinary staff to bypass expiry controls.

---

# 4.20 Stock Movement Permissions

| Permission                | Purpose                       |
| ------------------------- | ----------------------------- |
| `stock_movements.view`    | View stock movements          |
| `stock_movements.create`  | Create permitted movements    |
| `stock_movements.adjust`  | Perform stock adjustments     |
| `stock_movements.approve` | Approve sensitive adjustments |

Stock movement records should not normally be deleted because they form part of the inventory history.

---

# 4.21 Order Permissions

| Permission            | Purpose                           |
| --------------------- | --------------------------------- |
| `orders.view`         | View orders                       |
| `orders.create`       | Create orders                     |
| `orders.update`       | Update orders                     |
| `orders.confirm`      | Confirm orders                    |
| `orders.cancel`       | Cancel orders                     |
| `orders.complete`     | Complete orders                   |
| `orders.refund`       | Initiate or process order refunds |
| `orders.view_history` | View historical orders            |

---

# 4.22 Kitchen Permissions

| Permission                  | Purpose                           |
| --------------------------- | --------------------------------- |
| `kitchen.view_orders`       | View orders requiring preparation |
| `kitchen.start_preparation` | Start preparation                 |
| `kitchen.update_status`     | Update preparation status         |
| `kitchen.mark_ready`        | Mark an order ready               |
| `kitchen.report_waste`      | Report preparation waste          |

---

# 4.23 Purchase Permissions

| Permission          | Purpose                          |
| ------------------- | -------------------------------- |
| `purchases.view`    | View purchases                   |
| `purchases.create`  | Create purchases                 |
| `purchases.update`  | Update purchases                 |
| `purchases.cancel`  | Cancel purchases where permitted |
| `purchases.receive` | Receive purchased stock          |
| `purchases.approve` | Approve purchases where required |

---

# 4.24 Supplier Permissions

| Permission         | Purpose                     |
| ------------------ | --------------------------- |
| `suppliers.view`   | View suppliers              |
| `suppliers.create` | Create suppliers            |
| `suppliers.update` | Update supplier information |
| `suppliers.delete` | Deactivate suppliers        |

---

# 4.25 Payment Permissions

| Permission              | Purpose                                      |
| ----------------------- | -------------------------------------------- |
| `payments.view`         | View payments                                |
| `payments.create`       | Record payments                              |
| `payments.update`       | Correct payment information where authorized |
| `payments.refund`       | Process refunds                              |
| `payments.view_history` | View payment history                         |

Refunds should be restricted because they directly affect financial records.

---

# 4.26 Expense Permissions

| Permission         | Purpose                                 |
| ------------------ | --------------------------------------- |
| `expenses.view`    | View expenses                           |
| `expenses.create`  | Record expenses                         |
| `expenses.update`  | Update expenses                         |
| `expenses.delete`  | Delete/correct expenses where permitted |
| `expenses.approve` | Approve expenses                        |

---

# 4.27 Waste Permissions

| Permission           | Purpose                          |
| -------------------- | -------------------------------- |
| `waste.view`         | View waste records               |
| `waste.create`       | Record waste                     |
| `waste.update`       | Update waste before finalization |
| `waste.approve`      | Approve waste where required     |
| `waste.view_history` | View historical waste            |

Expired inventory should be recorded as waste through a controlled process.

---

# 4.28 Reports Permissions

| Permission          | Purpose                |
| ------------------- | ---------------------- |
| `reports.view`      | View reports           |
| `reports.sales`     | View sales reports     |
| `reports.inventory` | View inventory reports |
| `reports.expiry`    | View expiry reports    |
| `reports.purchases` | View purchase reports  |
| `reports.expenses`  | View expense reports   |
| `reports.waste`     | View waste reports     |
| `reports.payments`  | View payment reports   |
| `reports.export`    | Export reports         |

---

# 4.29 Notification Permissions

| Permission                | Purpose                           |
| ------------------------- | --------------------------------- |
| `notifications.view`      | View notifications                |
| `notifications.mark_read` | Mark notifications as read        |
| `notifications.manage`    | Manage notification configuration |

---

# 4.30 Audit Log Permissions

| Permission          | Purpose              |
| ------------------- | -------------------- |
| `audit_logs.view`   | View audit records   |
| `audit_logs.export` | Export audit records |

Audit logs should normally be read-only for users who are allowed to access them.

---

# 4.31 System Settings Permissions

| Permission           | Purpose                           |
| -------------------- | --------------------------------- |
| `settings.view`      | View system settings              |
| `settings.update`    | Update system settings            |
| `settings.expiry`    | Configure expiry warning settings |
| `settings.inventory` | Configure inventory settings      |
| `settings.payment`   | Configure payment settings        |

---

# 4.32 Initial Role-Permission Matrix

The following matrix defines the initial access level for the main Board’s Cafe roles.

**Legend:**

* **✓** = Allowed
* **—** = Not normally allowed
* **A** = Allowed for administration/management
* **V** = View only

| Module / Function   | Administrator | Manager | Cashier | Waiter | Kitchen | Storekeeper |
| ------------------- | ------------: | ------: | ------: | -----: | ------: | ----------: |
| Users               |             ✓ |       — |       — |      — |       — |           — |
| Roles & Permissions |             ✓ |       — |       — |      — |       — |           — |
| Products            |             ✓ |       ✓ |       V |      V |       V |           — |
| Categories          |             ✓ |       ✓ |       V |      V |       V |           — |
| Recipes             |             ✓ |       ✓ |       V |      V |       V |           V |
| Inventory           |             ✓ |       ✓ |       — |      — |       V |           ✓ |
| Stock Receiving     |             ✓ |       ✓ |       — |      — |       — |           ✓ |
| Stock Adjustment    |             ✓ |       A |       — |      — |       — |          ✓* |
| Batch Management    |             ✓ |       ✓ |       — |      — |       V |           ✓ |
| Expiry Management   |             ✓ |       ✓ |       — |      — |       V |           ✓ |
| Orders              |             ✓ |       V |       ✓ |      ✓ |       V |           — |
| Kitchen             |             ✓ |       V |       — |      V |       ✓ |           — |
| Purchases           |             ✓ |       ✓ |       — |      — |       — |           V |
| Suppliers           |             ✓ |       ✓ |       — |      — |       — |           V |
| Payments            |             ✓ |       ✓ |       ✓ |      — |       — |           — |
| Refunds             |             ✓ |       A |       — |      — |       — |           — |
| Expenses            |             ✓ |       ✓ |       — |      — |       — |           — |
| Waste               |             ✓ |       ✓ |       — |      — |      ✓* |           ✓ |
| Reports             |             ✓ |       ✓ |       V |      V |       V |           V |
| Notifications       |             ✓ |       ✓ |       ✓ |      ✓ |       ✓ |           ✓ |
| Audit Logs          |             ✓ |       V |       — |      — |       — |           — |
| System Settings     |             ✓ |       — |       — |      — |       — |           — |

`*` Subject to the specific permission assigned. Sensitive actions may require approval.

---

# 4.33 Separation of Duties

The system should separate responsibilities for sensitive operations.

For example:

```text
Purchase
   ↓
Receive Stock
   ↓
Inventory Batch
```

The person responsible for ordering stock does not necessarily need to be the same person responsible for receiving it.

Similarly:

```text
Stock Adjustment
      ↓
Request / Record
      ↓
Approval
      ↓
Final Adjustment
```

Where Board’s Cafe requires stronger control, sensitive operations should use an approval process.

---

# 4.34 Sensitive Operations

The following operations shall be treated as sensitive:

* Changing product prices.
* Changing recipes.
* Adjusting inventory.
* Blocking a batch.
* Releasing a blocked batch.
* Cancelling completed orders.
* Processing refunds.
* Approving expenses.
* Approving waste.
* Managing users.
* Assigning roles.
* Assigning permissions.
* Changing system settings.

These operations should be restricted to users with the appropriate permissions and should be recorded in the audit log.

---

# 4.35 Permission Enforcement

Permissions shall be enforced on the backend.

The frontend shall not be considered a security boundary.

For example, hiding the "Delete" button from a Cashier is useful for the user interface, but the API must also reject a delete request from a Cashier who does not have the required permission.

The enforcement model shall therefore be:

```text
User Request
     ↓
Authentication
     ↓
Identify User
     ↓
Identify Role
     ↓
Check Permission
     ↓
Allowed?
   ↙     ↘
 YES      NO
  ↓        ↓
Action   Reject
```

---

# 4.36 Unauthorized Access

When a user attempts to perform an action without the required permission, the system shall reject the operation.

The system should return an appropriate authorization error without exposing sensitive information.

---

# 4.37 Role Changes

When an administrator changes a user's role:

1. The previous role shall no longer provide access.
2. The new role shall determine the user's permissions.
3. The change shall be recorded in the audit log.
4. Existing historical transactions shall remain associated with the user.

Example:

```text
John
  ↓
Cashier
  ↓
Role changed
  ↓
Manager
```

John's previous orders and payments must not lose their historical association simply because his role changed.

---

# 4.38 User Deactivation

When a staff member leaves Board’s Cafe or should no longer use the system, the administrator should deactivate the account instead of deleting historical records associated with that user.

```text
Active User
     ↓
Deactivate
     ↓
Cannot Login
     ↓
Historical Records Preserved
```

---

# 4.39 Permission Changes

Changes to roles and permissions shall be auditable.

The system should record:

* Who made the change.
* Which role was changed.
* Which permission was added or removed.
* Date and time of the change.

---

# 4.40 RBAC Business Rule

The fundamental access-control rule is:

> **A staff member can perform an action only when the user's assigned role provides the required permission for that action.**

This means access should not depend only on the job title.

For example:

```text
Manager
   ↓
May normally approve expenses

BUT

Manager without
expenses.approve
   ↓
Cannot approve expenses
```

This makes the system more flexible and secure.

---

# 4.41 Future Role Support

The system shall allow Board’s Cafe to introduce additional roles in the future without redesigning the entire permission system.

Possible future roles could include:

* Accountant
* Procurement Officer
* Branch Manager
* Inventory Controller
* Supervisor
* Auditor

These roles should be created by combining existing permissions.

---

# 4.42 RBAC Summary

The final access-control structure is:

```text
                         ┌───────────────┐
                         │     USER      │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │     ROLE      │
                         └───────┬───────┘
                                 │
                                 ▼
                      ┌────────────────────┐
                      │    PERMISSIONS     │
                      └─────────┬──────────┘
                                │
             ┌──────────────────┼──────────────────┐
             ▼                  ▼                  ▼
          PRODUCTS           ORDERS           INVENTORY
             │                  │                  │
             ▼                  ▼                  ▼
          Recipes            Payments          Batches
                                                   │
                                                   ▼
                                               Expiry
```

The permission model is intentionally separated from the role model so that Board’s Cafe can change staff responsibilities without changing the underlying application architecture.

---

# 4.43 Initial Roles

The initial production roles for Board’s Cafe are:

```text
1. Administrator
2. Manager
3. Cashier
4. Waiter
5. Kitchen Staff
6. Storekeeper
```

The Administrator is responsible for managing users, roles, permissions, and system configuration.

All other roles receive only the permissions required for their operational responsibilities.
