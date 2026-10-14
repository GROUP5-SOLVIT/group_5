# Board’s Cafe Management System

# 14 — Notifications & Alerts

## 14.1 Introduction

The Notifications & Alerts module provides timely information to Board’s Cafe staff when an action is required, an important event occurs, or a business condition needs attention.

The purpose of notifications is not to create unnecessary messages. Instead, the system should notify the appropriate staff member when something requires awareness or action.

Examples include:

* Products approaching expiry
* Products that have expired
* Low stock
* Out-of-stock items
* New customer orders
* Orders requiring attention
* Purchase orders requiring action
* Supplier deliveries received
* Waste requiring approval
* Expenses requiring approval
* Important system activities

Notifications should be based on the user's role and permissions.

---

# 14.2 Objectives

The Notifications & Alerts module shall:

1. Notify staff about important operational events.
2. Alert authorized users about expiring and expired stock.
3. Alert staff when inventory reaches low-stock levels.
4. Support order-related notifications.
5. Support purchasing and supplier notifications.
6. Support waste and approval notifications.
7. Reduce the chance of missed operational tasks.
8. Provide a history of notifications.
9. Allow users to mark notifications as read.
10. Respect user roles and permissions.
11. Avoid sending irrelevant notifications.
12. Support configurable notification rules where appropriate.

---

# 14.3 Notification Types

The system should support different types of notifications.

Suggested types include:

```text
INVENTORY
EXPIRY
ORDER
PURCHASE
SUPPLIER
WASTE
EXPENSE
PAYMENT
PRODUCTION
APPROVAL
SYSTEM
SECURITY
```

---

# 14.4 Notification Priority

Notifications should have different priority levels.

Suggested levels:

```text
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

Examples:

```text
INFO:
Purchase order received.

MEDIUM:
Milk will expire in 3 days.

HIGH:
Milk has expired.

CRITICAL:
A large amount of high-value stock has expired.
```

The actual priority should depend on Board’s Cafe's configured business rules.

---

# 14.5 In-App Notifications

The primary notification mechanism should be an in-app notification system.

A user may see:

```text
🔔 Notifications (3)

Milk batch MILK-001 expires tomorrow.

8 items are below reorder level.

New order #1052 requires attention.
```

Users should be able to open a notification and navigate to the relevant record.

---

# 14.6 Notification Center

The application should provide a notification center.

The notification center may contain:

```text
All
Unread
Inventory
Orders
Expiry
Purchases
Waste
```

Example:

```text
Notifications

● Milk batch MILK-001 expires tomorrow.
  10 L remaining.
  10 minutes ago.

● Tomatoes are below reorder level.
  4 kg remaining.
  1 hour ago.

○ Waste record #W-102 requires approval.
  Yesterday.
```

---

# 14.7 Read and Unread Status

Each notification should have a status.

Possible states:

```text
UNREAD
READ
```

Unread notifications should be visually distinguishable.

Example:

```text
Unread:  ●
Read:    ○
```

The system should maintain the read status for each user.

---

# 14.8 Mark as Read

Users should be able to:

* Mark one notification as read
* Mark all notifications as read
* Open a notification, which may automatically mark it as read

Reading a notification should not automatically complete the underlying business action.

For example:

```text
Notification:
"Milk has expired."

User opens notification.

Status:
READ

Milk:
Still requires expiry/waste processing.
```

---

# 14.9 Expiry Notifications

Expiry notifications are a key feature for Board’s Cafe.

The system should be able to notify authorized staff when stock is approaching expiry.

Example:

```text
⚠ Expiry Alert

Milk
Batch: MILK-20261006-A
Quantity: 12 L

Expiry:
10 Oct 2026

Action:
Inspect/use/process the batch.
```

---

# 14.10 Expiry Alert Thresholds

The cafe should be able to configure expiry alert thresholds.

For example:

```text
7 days before expiry
3 days before expiry
1 day before expiry
On expiry
```

The exact thresholds may be configured according to the type of product.

For example:

```text
Fresh milk:
1–3 days

Dry ingredients:
7–30 days
```

The system should support configurable thresholds rather than assuming every product has the same expiry-warning period.

---

# 14.11 Expired Stock Notification

When a batch reaches its expiry date, the system should notify authorized staff.

Example:

```text
🚨 Expired Stock

Milk
Batch: MILK-001
Quantity: 8 L

Expired:
08 Oct 2026

Action required:
Inspect and process the stock.
```

The notification should link to the relevant batch or expiry-management page.

---

# 14.12 Expired Stock Does Not Automatically Mean Waste

The notification system should distinguish between:

```text
Expired
```

and:

```text
Processed as Waste
```

For example:

```text
System detects expiry
        ↓
Send notification
        ↓
Staff inspects stock
        ↓
Staff records appropriate action
        ↓
Waste / other approved action
```

This prevents the notification system from incorrectly changing inventory by itself.

---

# 14.13 Low Stock Notifications

The system should notify authorized inventory staff when an item's usable stock reaches its reorder level.

Example:

```text
⚠ Low Stock

Tomatoes

Current:
4 kg

Reorder Level:
10 kg
```

The notification may link to the inventory item or purchasing module.

---

# 14.14 Out-of-Stock Notifications

When an item reaches zero usable stock, the system should generate an appropriate alert.

Example:

```text
🚨 Out of Stock

Chicken

Available:
0 kg

The item may require replenishment.
```

If the item is required by active menu products, the system may also alert authorized managers.

---

# 14.15 Order Notifications

Order-related notifications should help staff process customer orders.

Examples:

```text
New Order #1052 received.

Order #1052 is ready for preparation.

Order #1052 is ready for pickup.

Order #1052 has been cancelled.
```

The exact notifications depend on the order workflow implemented by Board’s Cafe.

---

# 14.16 Kitchen Notifications

Kitchen staff may receive notifications for new or updated orders.

Example:

```text
🍽 New Order

Order #1052

2 × Chicken Burger
1 × Cappuccino
```

The notification should contain enough information for staff to understand that an order requires attention without exposing unnecessary sensitive information.

---

# 14.17 Order Delay Alerts

Where order preparation times are tracked, the system may notify authorized staff when an order exceeds its expected preparation time.

Example:

```text
⚠ Order Delay

Order #1052

Expected preparation:
15 minutes

Elapsed:
25 minutes
```

This can help the cafe respond quickly to delayed orders.

---

# 14.18 Purchase Notifications

Purchase-related notifications may include:

* Purchase order created
* Purchase order submitted
* Purchase order approved
* Purchase order rejected
* Goods received
* Partial delivery received
* Purchase order cancelled

Example:

```text
Purchase Order #PO-102

Supplier:
Fresh Farm Supplies

Status:
Awaiting Approval
```

---

# 14.19 Supplier Notifications

Authorized staff may receive alerts related to supplier activities.

Examples:

```text
Supplier delivery received.

Supplier delivery has rejected items.

Supplier return recorded.

Supplier payment is due.
```

These notifications should be visible only to users who need the information.

---

# 14.20 Waste Notifications

Waste-related notifications may include:

* Waste recorded
* Waste requires approval
* High-value waste recorded
* Unusual waste detected
* Waste record corrected

Example:

```text
⚠ Waste Approval Required

Waste Record:
W-104

Item:
Milk

Quantity:
50 L

Estimated Cost:
50,000 RWF

Reason:
Expiry
```

A manager with the appropriate permission can review and approve it.

---

# 14.21 High-Value Waste Alert

If Board’s Cafe configures a waste approval threshold, the system should alert the appropriate manager.

Example:

```text
High-Value Waste

Estimated value:
150,000 RWF

Approval required.
```

The threshold should be configurable.

---

# 14.22 Expense Notifications

Expense notifications may include:

* Expense submitted
* Expense requires approval
* Expense approved
* Expense rejected
* Expense cancelled

Example:

```text
Expense Approval Required

Category:
Maintenance

Amount:
75,000 RWF

Submitted by:
Staff Member
```

Only authorized users should receive or view financial notifications.

---

# 14.23 Payment Notifications

Depending on the payment workflow, the system may notify authorized users about:

* Successful payment
* Failed payment
* Refunded payment
* Payment discrepancy
* Outstanding payment

Example:

```text
Payment Failed

Order:
#1052

Amount:
12,000 RWF
```

---

# 14.24 Production Notifications

Where production is used, the system may notify relevant staff about:

* Production task created
* Production started
* Production completed
* Production failed
* Production waste recorded
* Production requires attention

Example:

```text
Production Completed

Product:
Chicken Burger

Quantity:
50
```

---

# 14.25 Approval Notifications

The system should support notifications for actions requiring approval.

Examples:

```text
Waste requires approval.

Expense requires approval.

Purchase order requires approval.

Inventory adjustment requires approval.
```

Example:

```text
Approval Required

Inventory Adjustment:
ADJ-102

Item:
Milk

Adjustment:
-20 L

Reason:
Damaged stock
```

---

# 14.26 Notification Recipients

Notifications should be sent only to relevant users.

For example:

```text
Low Stock
   ↓
Storekeeper / Manager

New Order
   ↓
Kitchen / Order Staff

Expense Approval
   ↓
Authorized Manager

User Permission Change
   ↓
Administrator
```

The system should not send every notification to every employee.

---

# 14.27 Role-Based Notification Rules

Notification delivery should consider:

* User role
* User permissions
* Assigned branch/location where applicable
* Assigned responsibilities
* Notification preferences

For example, a cashier does not normally need detailed supplier-payment alerts.

---

# 14.28 Branch and Location Notifications

If Board’s Cafe operates multiple branches or locations, notifications should be scoped appropriately.

Example:

```text
Branch A

Milk is below reorder level.
```

The system should not notify a user responsible only for Branch B unless that user has broader access.

---

# 14.29 Notification Preferences

Users may be allowed to configure certain notification preferences.

Possible preferences:

```text
Expiry alerts
Low-stock alerts
Order alerts
Purchase alerts
Waste alerts
Approval alerts
System alerts
```

However, mandatory operational or security notifications should not be disabled by users who are required to receive them.

---

# 14.30 Notification Channels

The initial implementation should prioritize:

```text
In-App Notifications
```

Additional channels may be supported later:

```text
Email
SMS
Push Notifications
WhatsApp
```

External notification channels should only be enabled where they are technically and operationally appropriate.

---

# 14.31 Scheduled Notifications

Some notifications are generated based on scheduled checks.

For example:

```text
Every morning
       ↓
Check expiry dates
       ↓
Find batches expiring soon
       ↓
Create notifications
```

Another example:

```text
Every day
       ↓
Check low-stock items
       ↓
Create alerts where required
```

The system should avoid repeatedly generating the same notification unnecessarily.

---

# 14.32 Duplicate Notification Prevention

The system should prevent notification spam.

For example, if:

```text
Milk batch MILK-001
expires tomorrow
```

the system should not create hundreds of identical notifications during repeated scheduled checks.

Instead, it may create one appropriate alert per configured threshold.

Example:

```text
7 days before → one notification
3 days before → one notification
1 day before  → one notification
Expired       → one notification
```

---

# 14.33 Notification Lifecycle

A notification may follow this lifecycle:

```text
EVENT OCCURS
     ↓
Notification Rule Evaluated
     ↓
Recipient Identified
     ↓
Notification Created
     ↓
Unread
     ↓
User Opens
     ↓
Read
```

For actionable notifications:

```text
Notification
     ↓
User Opens
     ↓
User Performs Action
     ↓
Underlying Record Updated
```

Reading the notification and completing the action are separate events.

---

# 14.34 Notification Data

A notification record may contain:

| Field                | Description                       |
| -------------------- | --------------------------------- |
| Notification ID      | Unique identifier                 |
| Recipient            | User receiving notification       |
| Type                 | Notification category             |
| Priority             | Notification priority             |
| Title                | Short notification title          |
| Message              | Notification content              |
| Status               | Read/unread                       |
| Related Object       | Related business record           |
| Related Object ID    | Identifier of related record      |
| Created At           | Creation date/time                |
| Read At              | Date/time read                    |
| Action URL/Reference | Destination for action            |
| Expiry               | Optional notification expiration  |
| Metadata             | Additional structured information |

The exact database structure will be finalized in the Database Design document.

---

# 14.35 Linking Notifications to Records

Notifications should link back to the relevant business record where possible.

Example:

```text
Notification
     ↓
Milk batch MILK-001
     ↓
Batch Details
```

Another example:

```text
Notification
     ↓
Waste Record W-104
     ↓
Waste Details
```

Another:

```text
Notification
     ↓
Order #1052
     ↓
Order Details
```

This reduces the time required for staff to find the item requiring attention.

---

# 14.36 Dashboard Notification Indicators

The main application interface should display notification indicators.

Example:

```text
Dashboard       Orders       Inventory       🔔 5
```

The notification count should normally represent unread notifications relevant to the current user.

---

# 14.37 Notification History

Users with appropriate permissions should be able to review notification history.

The system may store:

* Notification type
* Recipient
* Message
* Created date
* Read status
* Related record

This provides traceability and helps users review previous alerts.

---

# 14.38 Notification Search and Filtering

The notification center may support filtering by:

* Read/unread
* Type
* Priority
* Date
* Related module

Example:

```text
Filter:
Unread + Expiry
```

This would show only unread expiry-related notifications.

---

# 14.39 Notification Retention

Notifications should not necessarily be stored forever.

Board’s Cafe should define an appropriate retention period.

For example:

```text
Recent notifications:
Displayed normally

Older notifications:
Archived

Very old notifications:
Removed according to retention policy
```

Important audit records should remain subject to the separate Audit Logging policy.

---

# 14.40 Security Notifications

Security-related events may generate notifications for administrators.

Examples:

```text
New user account created.

User role changed.

User permissions changed.

User account disabled.

Multiple failed login attempts.

Important security setting changed.
```

These notifications should only be visible to authorized administrators.

---

# 14.41 User Management Notifications

When administrators create or change users, appropriate notifications may be generated.

Examples:

```text
New staff account created.

Staff role assigned.

Staff permissions updated.

Staff account disabled.
```

The exact notification content should avoid exposing passwords or other sensitive credentials.

---

# 14.42 Notification and Audit Log

Notifications and audit logs serve different purposes.

### Notification

Used to tell a user:

```text
"You need to know or act on this."
```

### Audit Log

Used to record:

```text
"This event happened and must be traceable."
```

For example:

```text
Waste Approved
     ↓
Notification → informs relevant staff
     ↓
Audit Log → permanently records the action
```

A notification should never replace the audit log.

---

# 14.43 Notification and Reports

Notifications highlight immediate issues.

Reports provide historical analysis.

For example:

```text
Notification:
"12 batches are approaching expiry."

Reports:
"Expiry losses increased by 15% this month."
```

Both modules should work together.

---

# 14.44 Important Business Rules

The Notifications & Alerts module should follow these rules:

1. Notifications must be sent only to appropriate users.
2. Notification visibility must respect permissions.
3. Notifications must not expose information the recipient is not authorized to see.
4. Expiry notifications must identify the relevant item and batch where applicable.
5. Low-stock notifications must use usable inventory quantities.
6. Expired stock notifications must not automatically mean the stock has been recorded as waste.
7. Reading a notification must not automatically complete the underlying business action.
8. Notifications should link to the relevant record where possible.
9. Scheduled notifications must avoid unnecessary duplicates.
10. Notification priority should reflect the importance of the event.
11. High-value waste and other configurable approval events should notify the appropriate approver.
12. Financial notifications must be restricted to authorized users.
13. Security notifications must be restricted to authorized administrators.
14. Notification preferences must not disable mandatory operational or security alerts where applicable.
15. Notifications should maintain read/unread status per user.
16. Notification creation should not modify the underlying business transaction unless explicitly designed to do so.
17. Notifications and audit logs must remain separate concepts.
18. Notification history should be available according to the configured retention policy.
19. Branch-specific notifications should be sent only to relevant users where branches are implemented.
20. The system should prevent notification spam.

---

# 14.45 Example — Complete Expiry Notification Flow

```text
Batch Created
      ↓
Milk
Batch: MILK-001
Expiry: 10 Oct
      ↓
System checks expiry
      ↓
7 days before expiry
      ↓
Expiry Notification
      ↓
Storekeeper / Manager
      ↓
3 days before expiry
      ↓
Second Alert
      ↓
1 day before expiry
      ↓
Urgent Alert
      ↓
Expiry Date Reached
      ↓
Expired Stock Alert
      ↓
Staff Inspects Stock
      ↓
Waste / Other Authorized Action
      ↓
Inventory Updated
      ↓
Audit Log
```

---

# 14.46 Example — Low Stock Flow

```text
Inventory:
Tomatoes

Current:
4 kg

Reorder Level:
10 kg
      ↓
System detects low stock
      ↓
Low Stock Notification
      ↓
Storekeeper / Manager
      ↓
Review Inventory
      ↓
Create Purchase Order if required
```

---

# 14.47 Example — Waste Approval Flow

```text
Staff Records Waste
       ↓
Waste Value:
150,000 RWF
       ↓
Approval Required
       ↓
Manager Notification
       ↓
Manager Reviews
       ↓
Approve / Reject
       ↓
Inventory Action
       ↓
Audit Log
```

---

# 14.48 Example — New Order Flow

```text
Customer Places Order
       ↓
Order Created
       ↓
Kitchen Notification
       ↓
Kitchen Opens Order
       ↓
Preparation
       ↓
Order Status Updated
       ↓
Relevant Staff Notified
```

---

# 14.49 Summary

The Notifications & Alerts module helps Board’s Cafe staff stay aware of important events without requiring them to constantly check every part of the system.

The core concept is:

```text
BUSINESS EVENT
      ↓
SYSTEM CHECKS RULE
      ↓
RELEVANT USER IDENTIFIED
      ↓
NOTIFICATION CREATED
      ↓
USER IS INFORMED
      ↓
USER TAKES ACTION
      ↓
BUSINESS RECORD UPDATED
      ↓
AUDIT LOG
```

The most important notification areas for Board’s Cafe are:

```text
Expiry
Low Stock
Out of Stock
Orders
Purchases
Suppliers
Waste
Expenses
Payments
Production
Approvals
Security
```

Notifications should remain **action-oriented, role-based, traceable, and controlled**, so that staff receive useful information rather than unnecessary alerts.
