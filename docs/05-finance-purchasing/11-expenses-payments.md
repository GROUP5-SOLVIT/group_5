# 11 — Expenses & Payments

## 1. Purpose

The Expenses & Payments module manages the financial transactions that occur within Board’s Cafe.

The module is responsible for recording and tracking:

* Customer payments for orders
* Supplier payments
* Operating expenses
* Other business expenses
* Refunds
* Partial payments
* Payment methods
* Payment status
* Financial references
* Payment history

The module must integrate with:

* POS & Order Management
* Purchases & Suppliers
* Inventory Management
* Reports & Dashboard
* Audit Logging

The system should keep customer sales payments, supplier payments, and general expenses logically separate while allowing management reports to combine them when appropriate.

---

# 2. Financial Transaction Types

Board’s Cafe should distinguish between different financial transaction types.

The main categories are:

```text
CUSTOMER PAYMENT
SUPPLIER PAYMENT
EXPENSE
REFUND
ADJUSTMENT
```

### Customer Payment

Money received from a customer for an order.

### Supplier Payment

Money paid to a supplier for purchased goods or services.

### Expense

Money spent by the cafe for operational purposes.

### Refund

Money returned to a customer.

### Adjustment

A controlled financial correction made by an authorized user.

---

# 3. Customer Payments

Customer payments originate from the POS module.

Example:

```text
Order #1052
Total: 15,000 RWF

Payment:
Cash
15,000 RWF
```

The payment should be linked to the order.

The system should not create a payment without a valid financial reason or reference.

---

# 4. Payment Methods

The system should support configurable payment methods.

Possible methods include:

* Cash
* Mobile Money
* Bank/Card
* Bank Transfer
* Other configured methods

The cafe should be able to enable or disable payment methods according to its operations.

---

# 5. Customer Payment Information

A payment record may contain:

| Field          | Description                  |
| -------------- | ---------------------------- |
| Payment ID     | Unique payment identifier    |
| Order          | Related customer order       |
| Amount         | Amount paid                  |
| Payment Method | Cash, Mobile Money, etc.     |
| Reference      | Transaction/reference number |
| Status         | Payment status               |
| Paid At        | Date and time                |
| Received By    | Staff member                 |
| Notes          | Additional information       |

The actual payment record should remain available for historical reporting.

---

# 6. Payment Status

Suggested payment statuses include:

```text
PENDING
COMPLETED
FAILED
CANCELLED
REFUNDED
PARTIALLY_REFUNDED
```

For example:

```text
Order Total: 20,000 RWF

Payment:
12,000 RWF

Status:
PARTIALLY_PAID
```

The overall order payment status can be determined from its payment records.

---

# 7. Partial Payments

The system should support partial payments if Board’s Cafe allows them.

Example:

```text
Order Total:
30,000 RWF

Payment 1:
Cash → 10,000 RWF

Payment 2:
Mobile Money → 20,000 RWF
```

Total paid:

```text
30,000 RWF
```

The order becomes fully paid.

Multiple payment records should be linked to the same order rather than replacing the original payment.

---

# 8. Cash Payments

For cash transactions, the POS should record:

* Amount due
* Amount received
* Change
* Staff member
* Date/time

Example:

```text
Order Total:     8,000 RWF
Cash Received:  10,000 RWF
Change:           2,000 RWF
```

The backend should validate the payment calculation.

---

# 9. Mobile Money and Electronic Payments

For electronic payments, the system should support a transaction reference where available.

Example:

```text
Payment Method:
Mobile Money

Amount:
15,000 RWF

Reference:
MM123456789
```

The reference should help staff reconcile the payment later.

The system should not mark an electronic payment as successful merely because a staff member entered a reference. Where payment integration is available, confirmation should come from the payment provider.

---

# 10. Supplier Payments

Supplier payments originate from purchases.

The relationship is:

```text
Supplier
   ↓
Purchase Order
   ↓
Goods Received
   ↓
Supplier Invoice
   ↓
Amount Payable
   ↓
Supplier Payment
```

Example:

```text
Supplier Invoice:
100,000 RWF

Paid:
60,000 RWF

Remaining:
40,000 RWF
```

The system should show the outstanding balance.

---

# 11. Supplier Payment Status

Supplier invoices or payable records may have:

```text
UNPAID
PARTIALLY_PAID
PAID
OVERDUE
CANCELLED
```

Example:

```text
Invoice:
INV-2026-001

Total:
250,000 RWF

Paid:
150,000 RWF

Outstanding:
100,000 RWF

Status:
PARTIALLY_PAID
```

---

# 12. Supplier Payment Information

A supplier payment may contain:

* Payment ID
* Supplier
* Invoice/payable reference
* Amount
* Payment method
* Transaction reference
* Payment date
* Staff member
* Notes

Supplier payments should remain connected to the original purchase records.

---

# 13. Operating Expenses

An operating expense is a cost incurred by Board’s Cafe that is not necessarily a purchase of inventory for production or resale.

Examples include:

* Rent
* Electricity
* Water
* Internet
* Staff-related expenses where applicable
* Transport
* Cleaning services
* Equipment maintenance
* Repairs
* Advertising
* Software subscriptions
* Office supplies
* Other operating costs

The system should allow authorized staff to record these expenses.

---

# 14. Expense Categories

Expenses should be categorized.

Possible categories include:

```text
RENT
UTILITIES
TRANSPORT
MAINTENANCE
CLEANING
MARKETING
INTERNET
SOFTWARE
OFFICE_SUPPLIES
STAFF_EXPENSE
OTHER
```

The exact categories should be configurable.

This allows management to generate useful financial reports.

---

# 15. Expense Record

An expense record may contain:

| Field          | Description              |
| -------------- | ------------------------ |
| Expense ID     | Unique identifier        |
| Category       | Expense category         |
| Description    | Reason for expense       |
| Amount         | Expense amount           |
| Payment Method | How it was paid          |
| Reference      | Receipt/reference number |
| Date           | Expense date             |
| Paid By        | Staff member             |
| Vendor         | Optional supplier/vendor |
| Notes          | Additional information   |
| Status         | Recorded/approved/etc.   |

---

# 16. Example Expense

Suppose the cafe pays an electricity bill.

```text
Expense Category:
Utilities

Description:
Electricity bill — September 2026

Amount:
85,000 RWF

Payment Method:
Bank Transfer

Reference:
BANK-98231
```

The system records the expense and includes it in the appropriate financial reports.

---

# 17. Expense Approval

Depending on the cafe's internal policy, certain expenses may require approval.

For example:

```text
Staff
   ↓
Creates Expense
   ↓
Manager Reviews
   ↓
Approved
   ↓
Payment Recorded
```

The system should support approval permissions.

Higher-value expenses may require additional authorization.

The exact approval thresholds should be configurable rather than hard-coded.

---

# 18. Recurring Expenses

Some expenses occur regularly.

Examples:

* Rent
* Internet
* Software subscription
* Security service
* Cleaning service

The system may support recurring expense definitions.

For example:

```text
Internet
Amount: 30,000 RWF
Frequency: Monthly
```

A recurring expense should still create individual financial records for each period.

The system should not store one permanent transaction representing all future payments.

---

# 19. Expense Attachments

Where supported, staff may attach supporting documents such as:

* Receipts
* Invoices
* Bills
* Payment confirmations

Attachments should be linked to the relevant financial record.

Access to financial documents should be permission-controlled.

---

# 20. Refunds

Refunds represent money returned to customers.

A refund must be connected to the original payment or order.

Example:

```text
Original Order:
20,000 RWF

Refund:
5,000 RWF

Remaining Sale Value:
15,000 RWF
```

The original order should not be deleted.

Instead, the system creates a refund record.

---

# 21. Full Refund

A full refund occurs when the entire eligible amount is returned.

Example:

```text
Order:
15,000 RWF

Refund:
15,000 RWF

Remaining customer payment:
0 RWF
```

The system should record:

* Original order
* Original payment
* Refund amount
* Refund reason
* Refund method
* Staff member
* Date/time
* Authorization

---

# 22. Partial Refund

A partial refund returns only part of the amount.

Example:

```text
Order:
25,000 RWF

Refund:
5,000 RWF

Net amount:
20,000 RWF
```

Multiple refunds may be allowed only if the total refunded amount does not exceed the refundable amount.

---

# 23. Refund Permissions

Refunds should be restricted to authorized users.

For example:

```text
Cashier:
May request refund

Manager:
May approve/process refund

Admin:
May approve/process refund
```

The exact permission structure should follow the User Roles & Permissions document.

---

# 24. Financial Adjustments

Sometimes a financial record may need correction.

Examples:

* Incorrect amount entered
* Duplicate payment record
* Incorrect payment method
* Accounting correction

The system should not allow staff to silently edit historical financial transactions without a trace.

Instead, an adjustment should:

* Require appropriate permission
* Record the reason
* Identify the user
* Record the date/time
* Preserve the original information where appropriate
* Create an audit record

---

# 25. Cash Register / Till

If Board’s Cafe uses a physical cash register, the system should support cash-session tracking.

A cash session may include:

```text
Opening Cash
      ↓
Cash Sales
      ↓
Cash Refunds
      ↓
Cash Expenses
      ↓
Cash Adjustments
      ↓
Expected Closing Cash
      ↓
Actual Closing Cash
```

Example:

```text
Opening Cash:
100,000 RWF

Cash Sales:
350,000 RWF

Cash Refunds:
20,000 RWF

Cash Expenses:
30,000 RWF

Expected Closing:
400,000 RWF
```

The actual physical cash can then be compared with the expected amount.

---

# 26. Cash Variance

If the actual cash differs from the expected cash, the system should record the variance.

Example:

```text
Expected:
400,000 RWF

Actual:
395,000 RWF

Variance:
-5,000 RWF
```

The staff member should provide a reason where required.

The variance should not simply be overwritten.

---

# 27. Cash Session Permissions

Suggested permissions include:

```text
cash_session.open
cash_session.close
cash_session.view
cash_session.record_adjustment
cash_session.approve_variance
```

Managers or administrators may have additional permissions for approving cash differences.

---

# 28. Financial Transaction Relationships

The system should maintain clear relationships between financial records.

### Customer Sale

```text
Order
  ↓
Payment
  ↓
Receipt
```

### Purchase

```text
Purchase
  ↓
Supplier Invoice
  ↓
Payable
  ↓
Supplier Payment
```

### Operating Expense

```text
Expense
  ↓
Payment
```

### Refund

```text
Original Order
  ↓
Original Payment
  ↓
Refund
```

---

# 29. Separation of Sales and Expenses

The system should not treat all money movements as the same type of transaction.

For example:

```text
Customer pays 50,000 RWF
```

is revenue/payment received from a sale.

While:

```text
Cafe pays 50,000 RWF for electricity
```

is an operating expense.

Although both involve 50,000 RWF, they have different business meanings.

The database should therefore distinguish them.

---

# 30. Financial Transaction Ledger

The system may maintain a financial transaction record or ledger that references the underlying transaction.

Example:

```text
Date       Type              Amount
------------------------------------------------
08 Oct     Customer Sale     +25,000
08 Oct     Supplier Payment  -80,000
08 Oct     Electricity       -30,000
08 Oct     Customer Refund   -5,000
```

This can support financial reporting without replacing the detailed source records.

The detailed records should remain in their respective modules.

---

# 31. Payment Reconciliation

Authorized users should be able to compare system records with actual financial transactions.

Examples:

### Cash

```text
POS Cash Sales
        vs
Physical Cash
```

### Mobile Money

```text
System Payments
        vs
Mobile Money Statement
```

### Bank

```text
System Payments
        vs
Bank Statement
```

Differences should be investigated and recorded rather than silently corrected.

---

# 32. Daily Financial Closing

At the end of a business day, an authorized staff member or manager may review:

* Total sales
* Cash sales
* Electronic payments
* Refunds
* Discounts
* Expenses
* Supplier payments
* Cash balance
* Variances

Example:

```text
Daily Summary

Sales:
850,000 RWF

Refunds:
20,000 RWF

Operating Expenses:
75,000 RWF

Supplier Payments:
300,000 RWF

Cash Sales:
450,000 RWF

Mobile Money:
280,000 RWF

Bank/Card:
120,000 RWF
```

The exact accounting interpretation should be handled according to Board’s Cafe's financial procedures.

---

# 33. Financial Dashboard

Authorized managers may see:

* Today's sales
* Today's expenses
* Supplier amounts payable
* Supplier payments
* Refunds
* Cash balance
* Payment-method totals
* Outstanding expenses
* Daily/weekly/monthly financial summaries

Financial information must be restricted according to user permissions.

---

# 34. Reports

The system should support reports such as:

### Sales Payment Report

* Total customer payments
* Payment method
* Date
* Staff member
* Order

### Supplier Payment Report

* Supplier
* Invoice
* Amount
* Paid amount
* Outstanding amount

### Expense Report

* Expense category
* Amount
* Date
* Vendor
* Payment method

### Refund Report

* Original order
* Refund amount
* Reason
* Staff member
* Date

### Cash Report

* Opening cash
* Cash sales
* Cash expenses
* Refunds
* Adjustments
* Expected closing cash
* Actual closing cash
* Variance

---

# 35. Permissions

Suggested permissions include:

```text
payments.view
payments.create
payments.update
payments.cancel

supplier_payments.view
supplier_payments.create
supplier_payments.approve

expenses.view
expenses.create
expenses.update
expenses.approve
expenses.cancel

refunds.view
refunds.create
refunds.approve
refunds.process

financial_reports.view
financial_reports.export

cash_session.open
cash_session.close
cash_session.view
cash_session.adjust
cash_session.approve_variance
```

Permissions should be assigned according to staff responsibilities.

---

# 36. Important Business Rules

The Expenses & Payments module should follow these rules:

1. Every payment must have a valid business reference.
2. Customer payments must be linked to an order.
3. Supplier payments must be linked to a supplier payable or purchase reference.
4. Expenses must have an expense category.
5. Financial transactions must preserve historical records.
6. Completed payments should not simply be deleted.
7. Refunds must reference the original transaction.
8. A refund cannot exceed the refundable amount.
9. Partial payments must be supported where configured.
10. Payment amounts must be validated by the backend.
11. Electronic payment references should be recorded where applicable.
12. Financial corrections must be audited.
13. Only authorized staff can approve refunds and financial adjustments.
14. Cash variances must be recorded rather than hidden.
15. Supplier payments must remain connected to supplier records.
16. Operating expenses must remain separate from inventory purchases.
17. Financial records should support reconciliation.
18. Historical transaction amounts should not change because current prices or configurations change.
19. Financial information must be protected by role-based permissions.
20. Important financial actions must be included in the audit log.

---

# 37. Example: Complete Financial Flow

A customer orders food worth 20,000 RWF.

```text
Customer Order
      ↓
POS
      ↓
Order Total = 20,000 RWF
      ↓
Customer Payment
      ↓
Mobile Money
      ↓
20,000 RWF
      ↓
Payment Completed
      ↓
Receipt
      ↓
Sales Report
```

Later, the cafe pays a supplier:

```text
Supplier
      ↓
Purchase
      ↓
Invoice
      ↓
Amount Payable = 100,000 RWF
      ↓
Supplier Payment
      ↓
Bank Transfer
      ↓
100,000 RWF
```

The cafe also pays electricity:

```text
Electricity Provider
      ↓
Operating Expense
      ↓
Utilities
      ↓
85,000 RWF
      ↓
Bank Transfer
```

These are three different financial events and should remain distinguishable.

---

# 38. Relationship With Other Modules

The module connects to the system as follows:

```text
                    ┌──────────────┐
                    │     POS      │
                    └──────┬───────┘
                           ↓
                    Customer Payment
                           ↓
                    ┌──────────────┐
                    │   Payments   │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
       Receipts          Reports          Refunds
```

Purchasing:

```text
Supplier
   ↓
Purchase
   ↓
Invoice
   ↓
Payable
   ↓
Supplier Payment
```

Expenses:

```text
Expense
   ↓
Approval
   ↓
Payment
   ↓
Financial Report
```

Cash:

```text
Cash Session
   ↓
Sales
   ↓
Refunds
   ↓
Expenses
   ↓
Closing
   ↓
Variance
```

---

# 39. Data Integrity Requirements

The system should maintain consistency between:

* Orders
* Payments
* Refunds
* Purchases
* Supplier invoices
* Supplier payments
* Expenses
* Cash sessions
* Financial reports
* Audit logs

For example, the system should prevent:

```text
Order Total:
20,000 RWF

Payment:
25,000 RWF
```

unless the additional amount is intentionally supported by the configured payment workflow.

Similarly:

```text
Supplier Invoice:
100,000 RWF

Supplier Payments:
120,000 RWF
```

should not be accepted as a normal payment without an appropriate adjustment or other valid reason.

---

# 40. Security and Audit Requirements

Financial information is sensitive and should receive stronger access controls.

The system should record important actions such as:

* Payment creation
* Payment cancellation
* Refund creation
* Refund approval
* Expense creation
* Expense approval
* Supplier payment
* Cash adjustment
* Cash variance approval
* Financial correction

Each audit record should identify:

* User
* Action
* Entity
* Entity ID
* Date/time
* Relevant information
* Previous value where applicable
* New value where applicable

---

# 41. Summary

The Expenses & Payments module provides Board’s Cafe with a controlled way to track money entering and leaving the business.

The main financial flows are:

```text
CUSTOMER SALES

Customer
   ↓
Order
   ↓
Payment
   ↓
Receipt
   ↓
Sales Report
```

```text
SUPPLIER PURCHASES

Supplier
   ↓
Purchase
   ↓
Invoice
   ↓
Payable
   ↓
Supplier Payment
```

```text
OPERATING EXPENSES

Business Need
   ↓
Expense
   ↓
Approval
   ↓
Payment
   ↓
Expense Report
```

```text
REFUNDS

Original Order
   ↓
Original Payment
   ↓
Refund Request
   ↓
Approval
   ↓
Refund
   ↓
Audit Log
```

The key design principle is that **every financial movement should be traceable to its source and should not be silently changed or deleted**.

This gives Board’s Cafe a reliable foundation for daily cash management, supplier settlement, expense tracking, reconciliation, and management reporting.
