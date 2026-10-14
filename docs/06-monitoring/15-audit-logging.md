# Board’s Cafe Management System

# 15 — Audit Logging

## 15.1 Introduction

The Audit Logging module records important activities performed within the Board’s Cafe Management System.

The purpose of audit logging is to provide accountability, traceability, and visibility into important actions performed by users and the system.

For example, if a staff member changes the quantity of milk in inventory, the system should be able to show:

```text
Who:
John

What:
Changed Milk inventory

Previous quantity:
20 L

New quantity:
15 L

Reason:
Damaged stock

When:
08 Oct 2026, 10:35 AM
```

Audit logs should help Board’s Cafe management investigate mistakes, unauthorized activities, inventory discrepancies, financial changes, and other important events.

---

# 15.2 Objectives

The Audit Logging module shall:

1. Record important user activities.
2. Provide accountability for staff actions.
3. Track changes to important business records.
4. Support investigation of inventory discrepancies.
5. Track administrative and permission changes.
6. Support financial accountability.
7. Record important approval and rejection actions.
8. Support security monitoring.
9. Provide historical activity information to authorized users.
10. Prevent unauthorized users from modifying audit records.
11. Preserve sufficient information to understand what happened.
12. Support compliance with Board’s Cafe internal policies.

---

# 15.3 What Is an Audit Log?

An audit log is a record of an important event that occurred within the system.

A typical audit record may answer:

```text
WHO?
    ↓
performed

WHAT?
    ↓
action

ON WHAT?
    ↓
record/resource

WHEN?
    ↓
date and time

WHERE?
    ↓
system/branch/device information where appropriate

WHAT CHANGED?
    ↓
old and new values where applicable
```

---

# 15.4 Audit Event Structure

A typical audit event may contain:

| Field         | Description                               |
| ------------- | ----------------------------------------- |
| Audit ID      | Unique audit record identifier            |
| User          | User who performed the action             |
| Action        | Action performed                          |
| Module        | System module involved                    |
| Resource Type | Type of record affected                   |
| Resource ID   | Identifier of affected record             |
| Description   | Human-readable explanation                |
| Previous Data | Previous values where applicable          |
| New Data      | New values where applicable               |
| Timestamp     | Date and time of the event                |
| IP Address    | Source IP where appropriate               |
| User Agent    | Client information where appropriate      |
| Branch        | Relevant branch/location where applicable |
| Metadata      | Additional structured information         |

The exact database structure will be finalized in the Database Design document.

---

# 15.5 Audit Actions

The system should support common audit actions such as:

```text
CREATE
VIEW
UPDATE
DELETE
LOGIN
LOGOUT
LOGIN_FAILED
APPROVE
REJECT
CANCEL
RESTORE
EXPORT
IMPORT
ADJUST
RECEIVE
TRANSFER
PROCESS
```

Not every action needs to be logged for every module.

The system should focus on actions that are important for accountability and traceability.

---

# 15.6 User Authentication Audit

Authentication events should be recorded.

Examples:

```text
User logged in
User logged out
Login failed
User account locked
User account unlocked
Password changed
Password reset
```

Example:

```text
LOGIN_FAILED

User:
adolphe

Time:
08 Oct 2026 08:42 AM

Reason:
Invalid credentials
```

Passwords must never be stored in audit logs.

---

# 15.7 User Creation Audit

When an administrator creates a user account, the system should record the action.

Example:

```text
CREATE USER

Created by:
Administrator

User:
John Doe

Role:
Cashier

Time:
08 Oct 2026 09:10 AM
```

Sensitive credentials should not be included in the audit record.

---

# 15.8 Role and Permission Audit

Changes to roles and permissions should be logged.

Examples:

```text
Role assigned
Role changed
Permission granted
Permission removed
User disabled
User enabled
```

Example:

```text
PERMISSION_UPDATED

User:
John Doe

Permission:
inventory.adjust

Previous:
Denied

New:
Allowed

Changed by:
Administrator
```

This is especially important because administrators control what staff can access and modify.

---

# 15.9 Inventory Audit Logging

Inventory changes should be carefully tracked.

Important events include:

* Stock received
* Stock issued
* Stock consumed
* Stock adjusted
* Stock transferred
* Stock returned
* Stock damaged
* Stock blocked
* Stock unblocked
* Stock written off
* Stock count completed

Example:

```text
INVENTORY_ADJUSTED

Item:
Milk

Batch:
MILK-001

Previous:
20 L

New:
15 L

Difference:
-5 L

Reason:
Damaged stock

Performed by:
Storekeeper

Time:
08 Oct 2026 10:35 AM
```

---

# 15.10 Inventory Adjustment Audit

Inventory adjustments are particularly sensitive because they can change the recorded quantity of stock.

Every adjustment should provide sufficient information to understand:

```text
Item
Batch
Previous quantity
New quantity
Difference
Reason
User
Date/time
```

Where approval is required, the audit trail should also record the approver.

Example:

```text
Adjustment Created
       ↓
Adjustment Approved
       ↓
Inventory Updated
```

---

# 15.11 Batch Audit Logging

Batch-related activities should be logged.

Examples:

```text
Batch created
Batch received
Batch quantity changed
Batch location changed
Batch blocked
Batch unblocked
Batch expired
Batch processed
Batch written off
```

Example:

```text
BATCH_STATUS_CHANGED

Batch:
MILK-001

Previous:
AVAILABLE

New:
EXPIRED

Time:
08 Oct 2026 00:01 AM
```

---

# 15.12 Expiry Audit Logging

Expiry processing is an important part of Board’s Cafe's inventory control.

The system should record:

* Expiry detection
* Expiry notification generation where appropriate
* Staff inspection
* Expired stock processing
* Waste creation
* Other authorized actions

Example:

```text
EXPIRY_PROCESSED

Item:
Milk

Batch:
MILK-001

Quantity:
8 L

Action:
Marked for waste

Processed by:
Storekeeper

Time:
08 Oct 2026 09:20 AM
```

The audit record should make it possible to trace the stock from receipt through expiry and final disposition.

---

# 15.13 Waste Audit Logging

Waste records should have a complete audit trail.

Important events include:

```text
Waste created
Waste updated
Waste approved
Waste rejected
Waste cancelled
Waste finalized
```

Example:

```text
WASTE_APPROVED

Waste:
W-104

Item:
Milk

Quantity:
50 L

Reason:
Expiry

Estimated value:
50,000 RWF

Approved by:
Manager

Time:
08 Oct 2026 11:05 AM
```

---

# 15.14 Purchase Audit Logging

Purchasing activities should be auditable.

Examples:

```text
Purchase order created
Purchase order updated
Purchase order submitted
Purchase order approved
Purchase order rejected
Purchase order cancelled
Goods received
Goods partially received
Goods returned
```

Example:

```text
PURCHASE_ORDER_APPROVED

Purchase Order:
PO-102

Supplier:
Fresh Farm Supplies

Approved by:
Manager

Time:
08 Oct 2026 09:45 AM
```

---

# 15.15 Supplier Audit Logging

Important supplier-related changes should be logged.

Examples:

```text
Supplier created
Supplier updated
Supplier disabled
Supplier payment information changed
Supplier status changed
```

Changes to sensitive supplier information should be especially traceable.

---

# 15.16 Product Audit Logging

Changes to products and menu items should be tracked.

Examples:

```text
Product created
Product updated
Product activated
Product deactivated
Product price changed
Product category changed
Product deleted/archived
```

Example:

```text
PRODUCT_PRICE_CHANGED

Product:
Chicken Burger

Previous Price:
4,500 RWF

New Price:
5,000 RWF

Changed by:
Manager

Time:
08 Oct 2026 12:15 PM
```

---

# 15.17 Recipe Audit Logging

Recipe changes are important because recipes determine ingredient consumption.

The system should log:

```text
Recipe created
Recipe updated
Recipe ingredient added
Recipe ingredient removed
Ingredient quantity changed
Recipe activated
Recipe deactivated
```

Example:

```text
RECIPE_UPDATED

Product:
Chicken Burger

Ingredient:
Tomatoes

Previous quantity:
40 g

New quantity:
50 g

Changed by:
Kitchen Manager

Time:
08 Oct 2026 01:10 PM
```

This helps explain changes in ingredient consumption.

---

# 15.18 Production Audit Logging

Where production is implemented, the system should record important production activities.

Examples:

```text
Production created
Production started
Production completed
Production cancelled
Production quantity changed
Production waste recorded
```

Example:

```text
PRODUCTION_COMPLETED

Product:
Chicken Burger

Quantity:
50

Completed by:
Kitchen Staff

Time:
08 Oct 2026 02:00 PM
```

---

# 15.19 Order Audit Logging

Important order events should be logged.

Examples:

```text
Order created
Order updated
Order confirmed
Order started
Order completed
Order cancelled
Order refunded
Order reopened
```

Example:

```text
ORDER_CANCELLED

Order:
#1052

Amount:
12,000 RWF

Cancelled by:
Cashier

Reason:
Customer cancellation

Time:
08 Oct 2026 02:30 PM
```

---

# 15.20 Payment Audit Logging

Payment activities should be traceable.

Examples:

```text
Payment created
Payment completed
Payment failed
Payment cancelled
Payment refunded
Payment adjusted
```

Example:

```text
PAYMENT_COMPLETED

Order:
#1052

Amount:
12,000 RWF

Payment Method:
Mobile Money

Reference:
PAY-10245

Time:
08 Oct 2026 02:35 PM
```

Sensitive payment credentials must never be stored in audit logs.

---

# 15.21 Expense Audit Logging

Expense activities should be recorded.

Examples:

```text
Expense created
Expense updated
Expense submitted
Expense approved
Expense rejected
Expense cancelled
```

Example:

```text
EXPENSE_APPROVED

Expense:
EXP-104

Category:
Maintenance

Amount:
75,000 RWF

Approved by:
Manager

Time:
08 Oct 2026 03:00 PM
```

---

# 15.22 Cash Session Audit Logging

Where cash sessions are implemented, important activities should be recorded.

Examples:

```text
Cash session opened
Cash session closed
Cash adjustment
Cash counted
Cash variance recorded
```

Example:

```text
CASH_SESSION_CLOSED

Opening:
100,000 RWF

Expected:
500,000 RWF

Actual:
495,000 RWF

Variance:
-5,000 RWF

Closed by:
Cashier

Time:
08 Oct 2026 06:00 PM
```

---

# 15.23 Report Audit Logging

Sensitive report activities should be auditable.

Examples:

```text
Report generated
Report exported
Financial report exported
Inventory report exported
Waste report exported
```

Example:

```text
REPORT_EXPORTED

Report:
Monthly Sales Report

Period:
01 Oct – 08 Oct 2026

Format:
Excel

Exported by:
Manager

Time:
08 Oct 2026 04:15 PM
```

The system should not necessarily log every simple dashboard view, unless required by Board’s Cafe policy.

---

# 15.24 Notification Audit Logging

Notifications and audit logs are separate concepts, but important notification events may be recorded.

Examples:

```text
Notification created
Notification read
Notification dismissed
```

However, reading a normal notification does not necessarily need to become a permanent audit event.

Sensitive notifications may require stronger tracking.

---

# 15.25 Administrative Audit Logging

Administrative activities should be recorded.

Examples:

```text
User created
User updated
Role changed
Permission changed
User disabled
User enabled
System configuration changed
Notification rule changed
Expiry threshold changed
```

Example:

```text
SYSTEM_SETTING_UPDATED

Setting:
Expiry Alert Threshold

Previous:
5 days

New:
7 days

Changed by:
Administrator

Time:
08 Oct 2026 04:30 PM
```

---

# 15.26 Delete Operations

Deletion of important business records should be carefully controlled and logged.

Where possible, the system should prefer:

```text
ACTIVE
INACTIVE
ARCHIVED
CANCELLED
```

over permanently deleting important historical records.

If a deletion is permitted, the audit log should record:

```text
Who deleted it
What was deleted
Record ID
Reason where required
Date/time
```

Example:

```text
DELETE

Resource:
Supplier

ID:
SUP-102

Deleted by:
Administrator

Reason:
Duplicate supplier record

Time:
08 Oct 2026 05:00 PM
```

---

# 15.27 Soft Deletion

For important records, the system should consider soft deletion or archival instead of permanent deletion.

For example:

```text
Product
    ↓
Deactivate
    ↓
No longer available for new sales
    ↓
Historical sales remain intact
```

This protects historical reports and auditability.

---

# 15.28 Audit Log Immutability

Normal users must not be able to modify or delete audit logs.

Audit logs should be treated as historical records.

For example:

```text
Staff User
    ↓
Can create business transaction
    ↓
Audit record created

Staff User
    X
Cannot edit audit record
    X
Cannot delete audit record
```

Even administrators should have restricted capabilities regarding audit records.

---

# 15.29 Audit Log Access

Access to audit logs should be permission-based.

Possible permissions include:

```text
audit.view
audit.export
audit.view_sensitive
```

Not every staff member should have access to the complete audit history.

---

# 15.30 Audit Log Search

Authorized users should be able to search audit records.

Possible search fields:

```text
User
Action
Module
Resource
Resource ID
Date
Branch
```

Example:

```text
Search:
Milk
```

The system may return:

```text
Milk received
Milk adjusted
Milk expired
Milk written off
Milk used in production
Milk waste recorded
```

---

# 15.31 Audit Log Filters

The audit log should support filters such as:

* Date range
* User
* Action
* Module
* Resource type
* Branch
* Severity where applicable

Example:

```text
Date:
01 Oct – 08 Oct

Module:
Inventory

Action:
ADJUST
```

This helps management investigate inventory changes quickly.

---

# 15.32 Audit Log Details

Opening an audit record should provide more information.

Example:

```text
Audit Event

Action:
INVENTORY_ADJUSTED

User:
John Doe

Module:
Inventory

Item:
Milk

Batch:
MILK-001

Previous Quantity:
20 L

New Quantity:
15 L

Reason:
Damaged stock

Branch:
Main Branch

Date:
08 Oct 2026

Time:
10:35 AM
```

---

# 15.33 Before and After Values

For update operations, the audit system should record previous and new values where appropriate.

Example:

```text
BEFORE

Reorder Level:
10 kg


AFTER

Reorder Level:
15 kg
```

This is particularly useful for:

* Product prices
* Reorder levels
* Recipe quantities
* User permissions
* Roles
* Inventory adjustments
* System settings

Sensitive information should be excluded or masked.

---

# 15.34 Sensitive Information

Audit logs must not store sensitive information unnecessarily.

The system must not record:

```text
Passwords
Password hashes
Authentication tokens
JWT tokens
Full payment credentials
Other secrets
```

Where sensitive values must be referenced, they should be masked or represented safely.

---

# 15.35 Audit Log Retention

Board’s Cafe should define how long audit records are retained.

Because audit logs provide historical accountability, they should normally be retained longer than ordinary notifications.

Example:

```text
Notifications:
Shorter retention

Audit Logs:
Long-term retention
```

The exact retention period should be determined by Board’s Cafe management and applicable policies.

---

# 15.36 System-Generated Audit Events

Not every audit event must be caused directly by a human user.

The system may generate audit events.

Examples:

```text
Automatic expiry detected
Scheduled notification generated
Automatic stock status changed
Scheduled report generated
System job failed
```

Example:

```text
EXPIRY_DETECTED

Item:
Milk

Batch:
MILK-001

Expiry Date:
08 Oct 2026

Detected by:
System

Time:
08 Oct 2026 00:01 AM
```

---

# 15.37 Audit Logging for Automated Processes

When a scheduled or automated process changes data, the audit record should identify the source as the system rather than incorrectly attributing the action to a human user.

Example:

```text
Actor:
SYSTEM

Action:
EXPIRY_STATUS_UPDATED
```

This provides accurate accountability.

---

# 15.38 Audit Log and Notifications

Audit logging and notifications should work together but remain separate.

Example:

```text
Milk Expires
     ↓
System detects expiry
     ├──────────────→ Notification
     │                  ↓
     │             Storekeeper informed
     │
     └──────────────→ Audit Log
                        ↓
                  Event recorded
```

The notification informs people.

The audit log records history.

---

# 15.39 Audit Log and Inventory

Inventory activities should create an understandable chain of events.

For example:

```text
Purchase Received
       ↓
Batch Created
       ↓
Stock Increased
       ↓
Stock Used
       ↓
Stock Adjusted
       ↓
Stock Expires
       ↓
Waste Recorded
```

The audit trail should make it possible to investigate the movement of stock through these stages.

---

# 15.40 Audit Log and Financial Transactions

Financial actions should be traceable.

Example:

```text
Order Created
       ↓
Payment Received
       ↓
Payment Completed
       ↓
Sale Included in Report
```

If a payment is refunded:

```text
Payment Completed
       ↓
Refund Created
       ↓
Refund Approved
       ↓
Financial Records Updated
       ↓
Audit Trail
```

---

# 15.41 Audit Log and User Permissions

Permission changes are particularly sensitive.

Example:

```text
Administrator
      ↓
Changes Staff Permission
      ↓
User:
John Doe

Old:
inventory.adjust = DENIED

New:
inventory.adjust = ALLOWED
      ↓
Audit Log
```

This makes it possible to determine who granted a sensitive permission and when.

---

# 15.42 Audit Log and Approval Workflows

Actions requiring approval should create a traceable sequence.

Example:

```text
Expense Submitted
       ↓
Approval Requested
       ↓
Manager Reviews
       ↓
Approved
       ↓
Audit Log
```

The system should preserve the identity of the person who submitted and the person who approved the transaction.

---

# 15.43 Audit Log Dashboard

Authorized administrators may have an audit dashboard showing summary information.

Example:

```text
Audit Activity

Today's Events:
245

Inventory Changes:
48

User Changes:
12

Financial Actions:
65

Security Events:
8

Failed Logins:
5
```

The dashboard should link to detailed audit records.

---

# 15.44 Security Monitoring

Audit logs may help identify suspicious behavior.

Examples:

```text
Multiple failed login attempts
Frequent inventory adjustments
Unusual high-value waste
Unexpected permission changes
Repeated payment reversals
Unusual report exports
```

The system may flag such activity for administrator review.

The system should not automatically assume that unusual activity is malicious without appropriate investigation.

---

# 15.45 Audit Log Export

Authorized users may be able to export audit records.

Possible formats:

```text
PDF
Excel
CSV
```

Exports should respect the user's permissions.

Exporting sensitive audit information should itself be logged.

Example:

```text
Audit Report Exported
       ↓
Audit Log
       ↓
"Manager exported inventory audit report."
```

---

# 15.46 Audit Log Pagination

Because a cafe can generate a large number of audit events, the audit interface should use pagination or another efficient loading mechanism.

Example:

```text
Events 1–50
       ↓
Next
       ↓
Events 51–100
```

The system should not attempt to load thousands of audit records at once.

---

# 15.47 Audit Log Performance

Audit logging should not significantly slow down normal cafe operations.

For example:

```text
Cashier completes sale
       ↓
Sale processed normally
       ↓
Audit event recorded
```

The implementation should be designed so that audit recording does not unnecessarily delay order processing.

---

# 15.48 Important Business Rules

The Audit Logging module should follow these rules:

1. Important business activities must be auditable.
2. Audit records must identify the actor where applicable.
3. System-generated events must identify the actor as the system.
4. Audit records must contain accurate timestamps.
5. Audit logs must not contain passwords or authentication secrets.
6. Sensitive financial information must be protected.
7. Normal users must not modify audit records.
8. Normal users must not delete audit records.
9. Audit log access must be permission-controlled.
10. Important inventory adjustments must be recorded.
11. Expiry-related actions must be traceable.
12. Waste approvals and finalization must be traceable.
13. Purchase approvals must be traceable.
14. Payment and refund activities must be traceable.
15. User and permission changes must be recorded.
16. Important product and recipe changes must be recorded.
17. Before-and-after values should be recorded for important changes where appropriate.
18. Deleted or archived important records should remain traceable.
19. Audit exports must respect permissions.
20. Sensitive audit exports should themselves be logged.
21. Audit logs and notifications must remain separate concepts.
22. Audit records should be retained according to Board’s Cafe's retention policy.
23. Audit logging should not unnecessarily interfere with normal cafe operations.
24. Audit records should support investigation of inventory and financial discrepancies.
25. The audit trail should provide enough information to reconstruct important business events.

---

# 15.49 Example — Complete Inventory Audit Trail

A typical milk batch may produce the following audit trail:

```text
08 Oct 08:00
Purchase Received
        ↓
Milk Batch Created
        ↓
Quantity: 50 L

08 Oct 10:00
Stock Consumed
        ↓
Quantity: 45 L

09 Oct 09:00
Stock Consumed
        ↓
Quantity: 20 L

10 Oct 00:01
Expiry Detected
        ↓
Batch Marked Expired

10 Oct 09:00
Waste Recorded
        ↓
Quantity: 5 L

10 Oct 11:00
Waste Approved
        ↓
Manager Approved
```

Management can therefore understand what happened to the stock from receipt through final disposal.

---

# 15.50 Example — Complete User Permission Audit Trail

```text
Administrator Creates User
        ↓
User:
John Doe

Role:
Cashier
        ↓
Audit Log

Administrator Grants:
sales.refund
        ↓
Audit Log

Administrator Removes:
sales.refund
        ↓
Audit Log

User Disabled
        ↓
Audit Log
```

This provides a complete history of access-related changes.

---

# 15.51 Example — Complete Financial Audit Trail

```text
Order Created
       ↓
Payment Completed
       ↓
Sale Recorded
       ↓
Report Includes Sale
       ↓
Refund Requested
       ↓
Refund Approved
       ↓
Payment Refunded
       ↓
Audit Trail
```

This allows management to trace financial events rather than relying only on the current balance.

---

# 15.52 Summary

The Audit Logging module provides accountability throughout the Board’s Cafe Management System.

The main concept is:

```text
USER / SYSTEM
      ↓
BUSINESS ACTION
      ↓
RECORD CHANGED
      ↓
AUDIT EVENT CREATED
      ↓
AUDIT HISTORY
```

The audit trail should particularly protect and track:

```text
User Management
Roles & Permissions
Inventory
Batches
Expiry
Waste
Products
Recipes
Production
Orders
Payments
Purchases
Suppliers
Expenses
Cash
Reports
Security Events
System Configuration
```

The most important principle is:

> **Every important change should be traceable to the person or system process that caused it, without storing unnecessary sensitive information.**

This audit trail will also support the later **Database Design, API Documentation, Security Requirements, and ERD** documents.
