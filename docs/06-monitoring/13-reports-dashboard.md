# Board’s Cafe Management System

# 13 — Reports & Dashboard

## 13.1 Introduction

The Reports & Dashboard module provides management and authorized staff with a clear view of the cafe's operational and financial activities.

The module collects information from different parts of the system and presents it through dashboards, summaries, tables, charts, and detailed reports.

The dashboard and reports should help Board’s Cafe answer questions such as:

* How much did the cafe sell today?
* How many orders were completed?
* Which products are selling the most?
* Which ingredients are running low?
* Which stock is approaching expiry?
* How much stock has expired?
* How much waste was recorded?
* What was purchased from suppliers?
* How much was spent on expenses?
* How much money was received through different payment methods?
* Which products or ingredients are causing high losses?
* How is the cafe performing over time?

---

# 13.2 Objectives

The Reports & Dashboard module shall:

1. Provide a quick overview of cafe operations.
2. Provide detailed operational reports.
3. Support sales analysis.
4. Support inventory analysis.
5. Support expiry monitoring.
6. Support waste analysis.
7. Support purchasing and supplier analysis.
8. Support expense and payment analysis.
9. Help management identify problems and trends.
10. Support informed business decisions.
11. Allow authorized users to filter reports.
12. Allow authorized users to export reports where permitted.
13. Protect sensitive financial and operational information through permissions.

---

# 13.3 Dashboard Users

Dashboard information should depend on the user's role and permissions.

For example:

```text
Administrator
    ↓
Full system dashboard

Manager
    ↓
Operational + financial dashboard

Cashier
    ↓
Sales/order-related dashboard

Kitchen Staff
    ↓
Kitchen/order-related information

Storekeeper
    ↓
Inventory/expiry-related dashboard
```

A user should only see information they are authorized to access.

---

# 13.4 Main Dashboard

The main management dashboard should provide a summary of important business activities.

Possible summary cards include:

```text
Today's Sales
Today's Orders
Pending Orders
Low Stock Items
Expiring Soon
Expired Stock
Today's Waste
Today's Expenses
```

Example:

```text
-----------------------------------------
        BOARD'S CAFE DASHBOARD
-----------------------------------------

Today's Sales       850,000 RWF
Orders              74
Pending Orders      6
Low Stock           8 items
Expiring Soon       12 batches
Expired Stock       3 batches
Today's Waste       35,000 RWF
Today's Expenses    75,000 RWF
-----------------------------------------
```

The actual dashboard values must come from system records.

---

# 13.5 Dashboard Date Range

The dashboard should support different reporting periods.

Possible options:

* Today
* Yesterday
* This week
* Last week
* This month
* Last month
* This year
* Custom date range

Example:

```text
Date Range:
01 Oct 2026 → 08 Oct 2026
```

Reports should use the selected date range consistently.

---

# 13.6 Sales Dashboard

The sales section should show information about customer sales.

Possible metrics include:

* Total sales
* Number of orders
* Average order value
* Paid orders
* Unpaid orders where supported
* Cancelled orders
* Refunded orders
* Sales by payment method
* Sales by product
* Sales by category

Example:

```text
Sales Summary

Total Sales:
5,850,000 RWF

Orders:
412

Average Order:
14,199 RWF
```

---

# 13.7 Sales by Product

Management should be able to identify the products that sell the most.

Example:

| Product        | Quantity Sold |       Sales |
| -------------- | ------------: | ----------: |
| Chicken Burger |           120 | 600,000 RWF |
| Beef Burger    |            95 | 570,000 RWF |
| Cappuccino     |           180 | 450,000 RWF |
| Sandwich       |            85 | 340,000 RWF |

This information can help management understand customer demand.

---

# 13.8 Sales by Category

Sales should also be grouped by menu category.

Example:

```text
Burgers       2,000,000 RWF
Beverages     1,500,000 RWF
Sandwiches      900,000 RWF
Breakfast       750,000 RWF
Desserts        700,000 RWF
```

The system should allow management to compare categories over different periods.

---

# 13.9 Sales by Payment Method

The system should provide a breakdown of payments.

Example:

```text
Cash:
2,500,000 RWF

Mobile Money:
1,800,000 RWF

Bank/Card:
1,550,000 RWF
```

This should be based on completed payment records rather than simply the order total.

---

# 13.10 Order Status Dashboard

The system should show the current state of customer orders.

Example:

```text
New          5
Confirmed    8
Preparing    6
Ready        4
Completed   51
Cancelled    2
```

This is particularly useful for monitoring kitchen operations.

---

# 13.11 Inventory Dashboard

The inventory dashboard should provide a quick overview of stock.

Possible information includes:

* Total inventory items
* Available stock
* Low-stock items
* Out-of-stock items
* Expiring stock
* Expired stock
* Blocked stock
* Recent stock receipts
* Recent stock consumption
* Recent stock adjustments
* Recent waste

Example:

```text
Inventory Overview

Inventory Items:       85
Low Stock:              8
Out of Stock:            3
Expiring Soon:          12
Expired:                 4
```

---

# 13.12 Low Stock Report

The low-stock report should identify items whose usable quantity has reached or fallen below their configured reorder level.

Example:

| Item     | Usable Stock | Reorder Level | Status |
| -------- | -----------: | ------------: | ------ |
| Tomatoes |         4 kg |         10 kg | Low    |
| Milk     |          6 L |          15 L | Low    |
| Flour    |        12 kg |         20 kg | Low    |
| Eggs     |       25 pcs |        50 pcs | Low    |

This report can help the storekeeper and manager decide when to purchase more stock.

---

# 13.13 Out-of-Stock Report

The system should identify inventory items with no usable stock.

Example:

```text
Out of Stock

Milk
Cheese
Chicken
Coffee Beans
```

Expired, damaged, spoiled, or blocked stock should not be incorrectly counted as usable stock.

---

# 13.14 Expiry Dashboard

Expiry monitoring is one of the most important parts of the Board’s Cafe dashboard.

The system should show:

* Items expiring soon
* Items already expired
* Expiry dates
* Batch numbers
* Remaining quantities
* Locations
* Estimated stock value

Example:

```text
Expiry Monitoring

Expiring in 1 day:       3 batches
Expiring in 3 days:      7 batches
Expiring in 7 days:     12 batches
Already expired:         4 batches
```

---

# 13.15 Expiring Stock Report

Example:

| Item     | Batch    | Quantity | Expiry Date | Status   |
| -------- | -------- | -------: | ----------- | -------- |
| Milk     | MILK-001 |     10 L | 09 Oct      | Expiring |
| Tomatoes | TOM-004  |     5 kg | 10 Oct      | Expiring |
| Yogurt   | YOG-002  |   20 pcs | 12 Oct      | Expiring |

The report should allow authorized staff to filter by:

* Product
* Category
* Batch
* Expiry period
* Location
* Supplier

---

# 13.16 Expired Stock Report

The expired-stock report should show stock that has passed its expiry date.

Example:

```text
Expired Stock

Milk
Batch: MILK-001
Quantity: 8 L
Expiry: 07 Oct 2026

Tomatoes
Batch: TOM-003
Quantity: 3 kg
Expiry: 08 Oct 2026
```

The system should distinguish **expired stock** from stock that has already been processed as **waste**.

This distinction is important because an expired item may still be awaiting physical inspection and waste processing.

---

# 13.17 Waste Dashboard

The waste dashboard should help management understand inventory losses.

Possible metrics:

* Total waste
* Waste cost
* Expired stock waste
* Spoilage waste
* Damage waste
* Production waste
* Overproduction waste
* Customer-return waste
* Supplier-rejection waste

Example:

```text
Waste This Month

Expiry             85,000 RWF
Spoilage           45,000 RWF
Production         60,000 RWF
Damage             20,000 RWF
Overproduction     35,000 RWF

Total             245,000 RWF
```

---

# 13.18 Waste by Product

The system should identify products and ingredients generating the highest waste.

Example:

| Item     | Waste Quantity | Waste Cost |
| -------- | -------------: | ---------: |
| Milk     |           25 L | 25,000 RWF |
| Tomatoes |          15 kg | 15,000 RWF |
| Bread    |         20 pcs | 20,000 RWF |
| Chicken  |           8 kg | 40,000 RWF |

This can help management investigate the causes.

---

# 13.19 Waste by Reason

Management should be able to compare waste reasons.

Example:

```text
Expiry             35%
Spoilage            25%
Production          20%
Damage              10%
Overproduction       7%
Other                3%
```

The system should calculate these figures from actual waste records.

---

# 13.20 Waste Trend

The system should allow management to see waste over time.

Example:

```text
Week 1:
120,000 RWF

Week 2:
95,000 RWF

Week 3:
75,000 RWF

Week 4:
60,000 RWF
```

This can help determine whether waste-reduction measures are working.

---

# 13.21 Purchasing Dashboard

The purchasing section should summarize purchasing activity.

Possible information:

* Total purchases
* Number of purchase orders
* Pending purchases
* Received purchases
* Partially received purchases
* Supplier spending
* Recent purchases
* Outstanding supplier payments

Example:

```text
Purchases This Month:
3,250,000 RWF

Purchase Orders:
28

Suppliers:
12
```

---

# 13.22 Supplier Report

The system should provide supplier-related reports.

Possible information:

* Supplier
* Number of purchases
* Total purchase value
* Amount paid
* Amount outstanding
* Returned goods
* Rejected goods

Example:

| Supplier   | Purchases |  Amount | Outstanding |
| ---------- | --------: | ------: | ----------: |
| Supplier A |         8 | 900,000 |     150,000 |
| Supplier B |         5 | 650,000 |           0 |
| Supplier C |         7 | 800,000 |     200,000 |

---

# 13.23 Supplier Performance

Where sufficient data is available, management may monitor:

* Delivery reliability
* Rejected quantities
* Damaged deliveries
* Expired goods received
* Purchase prices
* Return frequency

This can help Board’s Cafe make better supplier decisions.

---

# 13.24 Expense Dashboard

The expense dashboard should summarize operating expenses.

Possible metrics:

* Today's expenses
* Weekly expenses
* Monthly expenses
* Expenses by category
* Expenses by payment method
* Pending approvals
* Highest expenses

Example:

```text
Expenses This Month

Rent             500,000 RWF
Utilities        280,000 RWF
Transport        120,000 RWF
Maintenance       90,000 RWF
Marketing        150,000 RWF
Other             60,000 RWF

Total           1,200,000 RWF
```

---

# 13.25 Expenses by Category

Management should be able to identify where the business is spending money.

Possible categories include:

```text
Rent
Utilities
Transport
Maintenance
Cleaning
Marketing
Internet
Software
Office Supplies
Staff Expenses
Other
```

Reports should support filtering by date and category.

---

# 13.26 Payment Report

The payment report should show money received from customers.

Possible fields include:

* Order
* Payment amount
* Payment method
* Payment reference
* Payment status
* Date
* Staff member

The report should distinguish successful payments from failed, cancelled, or refunded payments.

---

# 13.27 Cash Report

Where cash sessions are implemented, management should be able to review:

* Opening cash
* Cash sales
* Cash refunds
* Cash expenses
* Cash adjustments
* Expected closing cash
* Actual closing cash
* Variance

Example:

```text
Opening Cash:          100,000 RWF
Cash Sales:            450,000 RWF
Cash Refunds:           20,000 RWF
Cash Expenses:          30,000 RWF
Expected Closing:      500,000 RWF

Actual Closing:        495,000 RWF

Variance:               -5,000 RWF
```

---

# 13.28 Production Reports

If Board’s Cafe uses production workflows, the system should provide production-related information.

Possible reports include:

* Products produced
* Production quantity
* Ingredients consumed
* Production waste
* Failed production
* Overproduction
* Production cost where supported

Example:

```text
Production

Chicken Burger:
Produced: 100
Sold: 92
Waste: 8
```

This information can help management compare production with actual demand.

---

# 13.29 Ingredient Consumption Report

Because one ingredient may be used by many products, the system should be able to show its total consumption.

For example:

```text
Tomatoes

Burger:
12 kg

Sandwich:
8 kg

Pizza:
10 kg

Salad:
5 kg

Total Consumption:
35 kg
```

This is important because the cafe purchases and stores **one inventory item called Tomatoes**, even though many recipes use it.

---

# 13.30 Recipe/Product Performance

The system may combine sales and recipe information to provide useful operational analysis.

For example:

```text
Chicken Burger

Sold:
120

Estimated ingredient consumption:

Flour/Bun:   120 pcs
Chicken:      15 kg
Tomatoes:      6 kg
Onions:        3 kg
Sauce:         2 L
```

This helps management understand how sales affect inventory consumption.

---

# 13.31 Management Performance Indicators

The dashboard may provide indicators such as:

### Sales

```text
Total Sales
Order Count
Average Order Value
```

### Inventory

```text
Low Stock
Out of Stock
Expiring Soon
Expired
```

### Waste

```text
Waste Quantity
Waste Cost
Waste Rate
```

### Purchasing

```text
Purchase Value
Supplier Count
Outstanding Supplier Payments
```

### Expenses

```text
Operating Expenses
Expense by Category
```

The exact KPIs should be finalized based on Board’s Cafe's actual management needs.

---

# 13.32 Dashboard Alerts

The dashboard should highlight important conditions.

Examples:

```text
⚠ 8 inventory items are below reorder level.

⚠ 12 batches are approaching expiry.

⚠ 4 batches have expired.

⚠ Waste increased by 18% compared with the previous period.

⚠ 3 supplier invoices are overdue.
```

These alerts should lead staff toward the relevant module where they can take action.

---

# 13.33 Drill-Down

Dashboard numbers should be clickable where appropriate.

For example:

```text
Expiring Soon: 12
       ↓
Click
       ↓
Expiring Stock Report
       ↓
View Batch
       ↓
View Inventory Item
```

Similarly:

```text
Today's Sales: 850,000 RWF
       ↓
Click
       ↓
Sales Report
       ↓
View Orders
       ↓
View Order Details
```

This allows users to move from summary information to the underlying records.

---

# 13.34 Report Filters

Reports should support appropriate filters.

Common filters include:

* Date range
* Product
* Category
* Batch
* Supplier
* Staff member
* Payment method
* Waste category
* Order status
* Branch/location where applicable

Filters should be relevant to each report rather than forcing every report to contain every filter.

---

# 13.35 Report Search

Where appropriate, users should be able to search reports.

Examples:

```text
Search:
Milk
```

or:

```text
Search:
TOM-2026-001
```

or:

```text
Search:
Order #1052
```

Search results must respect the user's permissions.

---

# 13.36 Report Export

Authorized users may be allowed to export reports.

Possible formats include:

* PDF
* Excel
* CSV

Examples:

```text
Sales Report → PDF
Inventory Report → Excel
Waste Report → CSV
```

Export permissions should be controlled because reports may contain sensitive financial information.

---

# 13.37 Report Accuracy

Reports must be generated from reliable underlying records.

For example:

```text
Sales Report
    ↓
Completed Sales / Payment Records

Inventory Report
    ↓
Inventory + Stock Movements

Waste Report
    ↓
Waste Records

Expense Report
    ↓
Expense Records

Purchase Report
    ↓
Purchase Records
```

The system should avoid maintaining duplicate manually entered totals that can become inconsistent with the underlying transactions.

---

# 13.38 Historical Reporting

Reports should preserve historical information.

For example, if the price of a menu product changes:

```text
January:
Product Price = 3,000 RWF

March:
Product Price = 3,500 RWF
```

January sales records should continue to reflect the price applicable to the January transaction.

Historical reports should not change simply because the current product configuration has changed.

---

# 13.39 Dashboard Data Refresh

The dashboard should display sufficiently current information.

Depending on the implementation, information may be updated:

* Immediately after a transaction
* When the page is refreshed
* Periodically
* Through real-time updates where useful

For operational information such as pending kitchen orders, near-real-time updates may be useful.

---

# 13.40 Role-Based Dashboard Visibility

Different users should see different information.

### Administrator

May access:

```text
Sales
Inventory
Purchases
Suppliers
Expenses
Payments
Waste
Reports
Users
Audit Information
```

### Manager

May access:

```text
Sales
Inventory
Purchases
Suppliers
Expenses
Payments
Waste
Management Reports
```

### Cashier

May primarily access:

```text
Orders
Sales
Payments
Relevant Sales Reports
```

### Kitchen Staff

May primarily access:

```text
Orders
Preparation Status
Production Information
Relevant Waste
```

### Storekeeper

May primarily access:

```text
Inventory
Batches
Expiry
Purchases
Receiving
Waste
Stock Reports
```

Actual access must be controlled by permissions rather than only by the role name.

---

# 13.41 Financial Information Protection

Financial reports may contain sensitive information.

Therefore, the system should restrict access to:

* Revenue
* Expenses
* Supplier payments
* Profit-related information
* Cash balances
* Financial exports

Only authorized users should be able to access these reports.

---

# 13.42 Auditability

Important report-related actions should be logged where appropriate.

Examples:

```text
Report Generated
Report Exported
Dashboard Accessed
Financial Report Exported
```

The audit record may contain:

* User
* Report type
* Date/time
* Filters used
* Export format where applicable

This is particularly useful for sensitive financial reports.

---

# 13.43 Example Management Dashboard

A possible Board’s Cafe management dashboard could be structured as:

```text
┌─────────────────────────────────────────────────────┐
│                 BOARD'S CAFE                        │
│              Management Dashboard                   │
├──────────────┬──────────────┬───────────────────────┤
│ Today's Sale │ Orders       │ Avg. Order            │
│ 850,000 RWF  │ 74           │ 11,486 RWF            │
├──────────────┼──────────────┼───────────────────────┤
│ Low Stock    │ Expiring     │ Expired               │
│ 8            │ 12 batches   │ 4 batches             │
├──────────────┼──────────────┼───────────────────────┤
│ Waste Today  │ Expenses     │ Pending Orders        │
│ 35,000 RWF   │ 75,000 RWF   │ 6                    │
└──────────────┴──────────────┴───────────────────────┘

Sales Trend
──────────────────────────────────────────────────────

Top Selling Products
──────────────────────────────────────────────────────

Expiry Alerts
──────────────────────────────────────────────────────

Low Stock Alerts
──────────────────────────────────────────────────────

Waste Summary
──────────────────────────────────────────────────────
```

This is an example of the information structure. The final UI design will be defined in the UI/UX requirements document.

---

# 13.44 Relationship With Other Modules

The Reports & Dashboard module receives information from other modules.

```text
                    ┌──────────────┐
                    │     POS      │
                    └──────┬───────┘
                           │
                           ↓
                    ┌──────────────┐
                    │   REPORTS    │
                    │  DASHBOARD   │
                    └──────────────┘
                           ↑
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        │                  │                  │
   INVENTORY           PURCHASES          EXPENSES
        │                  │                  │
        ↓                  ↓                  ↓
   Stock Reports     Supplier Reports   Expense Reports

        │                  │                  │
        └──────────────┬───┴──────────────────┘
                       ↓
                    MANAGEMENT
```

Additional information comes from:

```text
Batch & Expiry
       ↓
Expiry Reports

Waste
       ↓
Waste Reports

Payments
       ↓
Payment Reports

Production
       ↓
Production Reports

Audit Logs
       ↓
Activity / Audit Reports
```

---

# 13.45 Important Business Rules

The Reports & Dashboard module should follow these rules:

1. Dashboard information must be based on actual system records.
2. Users should only see reports they are authorized to access.
3. Financial reports must be permission-controlled.
4. Historical transaction information must remain accurate.
5. Cancelled transactions should not be incorrectly counted as completed sales.
6. Failed payments should not be counted as successful payments.
7. Refunded transactions should be represented correctly in financial reports.
8. Expired stock should be distinguished from stock already recorded as waste.
9. Waste reports should use finalized waste records.
10. Inventory reports should consider usable stock rather than only physical quantity where appropriate.
11. Low-stock reports should use configured reorder levels.
12. Report filters must be applied consistently.
13. Exported reports must respect the same permissions as on-screen reports.
14. Dashboard figures should update according to the underlying transaction state.
15. Reports should not modify operational records.
16. Historical reports should remain stable even when current product prices or configurations change.
17. Important report exports and sensitive financial access should be auditable.
18. The system should avoid unnecessary duplicate summary data that can become inconsistent with source records.
19. Reports should support appropriate date ranges.
20. Management dashboards should highlight conditions that require action, such as low stock, expiry, waste, and outstanding payments.

---

# 13.46 Summary

The Reports & Dashboard module provides Board’s Cafe with a central view of business performance.

The main information flow is:

```text
POS
        ┐
Inventory
        │
Purchases
        │
Suppliers
        │
Payments
        ├──────→ REPORTS & DASHBOARD
Expenses │
        │
Waste
        │
Batch/Expiry
        │
Production
        ┘
```

The dashboard provides the **summary**, while detailed reports provide the **evidence behind the summary**.

For example:

```text
Dashboard
"12 batches are expiring soon"
        ↓
Expiry Report
"Milk — Batch MILK-001 — 10 L — expires 09 Oct"
        ↓
Batch Details
"Received from Supplier A on 02 Oct"
        ↓
Inventory / Action
"Use this batch first or process it according to expiry workflow"
```

This approach ensures that the Board’s Cafe dashboard is not only a display of numbers but also a practical tool for **monitoring operations, identifying problems, and taking action**.
