# Board's Cafe Management System

# 21. Security Requirements

## 21.1 Introduction

The Board's Cafe Management System will be used internally by authorized staff to manage cafe operations, including orders, inventory, purchases, expenses, payments, waste, reports, users, and other business activities.

Because the system will contain operational and financial information, appropriate security controls must be implemented to protect the confidentiality, integrity, and availability of the system and its data.

Security must be considered throughout the application, including the frontend, backend, API, database, authentication, authorization, and deployment environment.

---

# 21.2 Security Objectives

The system should protect:

* User accounts.
* Customer and order information.
* Inventory information.
* Supplier information.
* Purchase records.
* Payment records.
* Expense records.
* Business reports.
* User roles and permissions.
* Audit records.
* System configuration.

The main security objectives are:

1. Prevent unauthorized access.
2. Prevent unauthorized modification of business data.
3. Protect user credentials.
4. Enforce role and permission restrictions.
5. Maintain accurate inventory and financial records.
6. Track important security-sensitive activities.
7. Protect data transmitted between users and the system.
8. Protect the database from unauthorized access.
9. Detect and handle suspicious or invalid activities.
10. Maintain system availability and recoverability.

---

# 21.3 Confidentiality, Integrity and Availability

The system should follow the three fundamental information security principles.

## Confidentiality

Only authorized users should be able to access information.

For example:

* Cashiers should not access system administration.
* Inventory staff should not modify financial records.
* Finance staff should not modify recipes or stock.
* Users should not access another user's private account information.

## Integrity

Business information should remain accurate and should not be modified without authorization.

Examples include:

* Stock quantities.
* Purchase amounts.
* Payment records.
* Expenses.
* Orders.
* Recipes.
* User permissions.

## Availability

Authorized staff should be able to use the system when required for normal cafe operations.

The system should therefore include:

* Reliable deployment.
* Database backups.
* Error handling.
* Recovery procedures.
* Monitoring where appropriate.

---

# 21.4 Authentication

All users must authenticate before accessing protected system functions.

The login process should be:

```text id="y31o9a"
User
 ↓
Login
 ↓
Credential Verification
 ↓
Authentication Successful
 ↓
Access Token
 ↓
Protected API Access
```

Unauthenticated users should only have access to public authentication endpoints.

---

# 21.5 Password Security

Passwords must be securely handled.

The system must:

* Never store passwords as plain text.
* Use Django's secure password hashing.
* Never return passwords through API responses.
* Never include passwords in logs.
* Never expose passwords in audit records.

Users should be encouraged to use strong passwords.

---

# 21.6 Password Validation

The system should apply appropriate password validation rules.

A password should not be:

* Empty.
* Extremely short.
* A commonly used password.
* Easily associated with the user.

Django's password validation mechanisms should be used where appropriate.

---

# 21.7 JWT Security

The API will use JWT-based authentication.

The system should:

* Use short-lived access tokens.
* Use refresh tokens for obtaining new access tokens.
* Validate token expiration.
* Reject invalid tokens.
* Reject tampered tokens.
* Protect refresh-token handling.

Tokens should not be unnecessarily exposed to other users or stored insecurely.

---

# 21.8 Session and Token Management

When a user logs out, the application should clear the authentication state on the client.

Where refresh-token rotation or token blacklisting is implemented, revoked refresh tokens should not be accepted for continued authentication.

Authentication failures should not reveal unnecessary information about whether a particular username or email exists.

---

# 21.9 Role-Based Access Control

The system will use Role-Based Access Control (RBAC).

The five initial roles are:

```text id="l4s6la"
Administrator
Manager
Cashier
Inventory Staff
Finance Staff
```

Each role receives only the permissions required for its responsibilities.

---

# 21.10 Least Privilege

The system must follow the principle of least privilege.

Users should receive the minimum permissions necessary to perform their work.

For example:

### Cashier

Can create orders and process permitted payments but cannot modify stock.

### Inventory Staff

Can manage inventory and batches but cannot modify user roles.

### Finance Staff

Can manage permitted financial records but cannot modify inventory.

### Manager

Can oversee operational activities but cannot manage system-level roles and permissions.

### Administrator

Has system-wide administrative privileges.

---

# 21.11 Backend Authorization

Authorization must always be enforced by the backend.

The frontend may hide unauthorized buttons, menus, or pages, but this is not a security mechanism.

For example, the frontend may hide:

```text id="h4v7n2"
Users → Create User
```

from a Cashier.

However, the backend must also reject:

```text id="o8h1n4"
POST /api/v1/users/
```

when the authenticated user does not have the required permission.

---

# 21.12 Permission Management

Permissions should be specific enough to control individual operations.

Examples:

```text id="5tbxv5"
orders.view
orders.create
orders.update
orders.cancel

inventory.view
inventory.adjust
inventory.receive

batches.view
batches.adjust

purchases.view
purchases.create
purchases.receive

expenses.view
expenses.create
expenses.update

reports.sales.view
reports.inventory.view
reports.financial.view

users.view
users.create
users.update
users.deactivate

roles.view
roles.manage

audit_logs.view
```

The exact permission list may be expanded as implementation requirements become clearer.

---

# 21.13 Object-Level Authorization

Permission checks should also consider the specific resource being accessed where necessary.

For example, a user should not be able to modify a record simply because they can access the general endpoint.

The backend should verify:

```text id="4od5iy"
Authenticated User
        ↓
Has Permission?
        ↓
Allowed Resource?
        ↓
Allowed Action?
        ↓
Perform Operation
```

---

# 21.14 API Security

All protected API endpoints must require authentication and appropriate authorization.

The API should:

* Validate incoming requests.
* Reject malformed data.
* Validate object identifiers.
* Apply permission checks.
* Return appropriate HTTP status codes.
* Avoid exposing internal implementation details.
* Rate-limit sensitive endpoints where necessary.

---

# 21.15 Input Validation

All user-provided data must be validated before being processed.

Validation should apply to:

* Names.
* Quantities.
* Prices.
* Dates.
* Batch numbers.
* Expiry dates.
* Email addresses.
* Phone numbers.
* Descriptions.
* Payment amounts.
* Expense amounts.

Example:

```text id="4yyj1r"
Quantity = -5
```

must be rejected.

Similarly:

```text id="ydw2z7"
Expiry Date < Purchase Date
```

should be rejected where the business rule requires this.

---

# 21.16 SQL Injection Protection

The system must protect against SQL injection.

Django ORM and parameterized database operations should be used instead of constructing SQL queries from raw user input.

Unsafe practices such as directly concatenating user-provided values into SQL queries must be avoided.

---

# 21.17 Cross-Site Scripting Protection

The application should protect against Cross-Site Scripting (XSS).

User-provided text must not be rendered as executable HTML or JavaScript without appropriate sanitization and escaping.

The frontend should use safe rendering practices.

---

# 21.18 Cross-Site Request Forgery Protection

Appropriate CSRF protection must be applied where applicable to the authentication and API architecture.

The final implementation should ensure that authentication mechanisms cannot be exploited through unauthorized cross-site requests.

---

# 21.19 CORS Security

Cross-Origin Resource Sharing (CORS) should be configured explicitly.

Only trusted frontend origins should be allowed in production.

The system should avoid allowing unrestricted origins such as:

```text id="k6m7l4"
*
```

unless there is a specific and justified reason.

---

# 21.20 HTTPS

Production communication must use HTTPS.

The expected architecture is:

```text id="e6n3im"
Staff Browser
      │
      │ HTTPS
      ▼
Web Server / Reverse Proxy
      │
      ▼
Django API
      │
      ▼
PostgreSQL
```

Sensitive information such as credentials and authentication tokens must not be transmitted over unencrypted HTTP in production.

---

# 21.21 Secure HTTP Configuration

Production deployment should use appropriate HTTP security settings.

Where applicable:

* Secure cookies.
* HTTP Strict Transport Security (HSTS).
* Appropriate Content Security Policy.
* X-Content-Type-Options.
* Referrer-Policy.
* Clickjacking protection.

The exact configuration should be determined during deployment.

---

# 21.22 Database Security

The PostgreSQL database must not be directly exposed to the public internet.

The preferred architecture is:

```text id="phv1bd"
Internet
   ↓
Frontend / API
   ↓
Django Backend
   ↓
Private Database Connection
   ↓
PostgreSQL
```

Database credentials must be stored securely.

---

# 21.23 Database Permissions

The application database user should have only the permissions required by the application.

Administrative database credentials should not be used by the normal application runtime.

Database access should be restricted to trusted application services and administrators.

---

# 21.24 Data Integrity

The system should use database constraints and application validation to maintain data integrity.

Examples include:

* Unique usernames/emails where required.
* Valid foreign-key relationships.
* Positive quantities.
* Positive monetary values where applicable.
* Valid dates.
* Required relationships.
* Appropriate status transitions.

---

# 21.25 Inventory Security

Inventory data is sensitive because unauthorized changes can result in financial losses.

Important inventory operations should require appropriate permissions.

Examples:

* Stock adjustments.
* Stock receiving.
* Batch creation.
* Waste recording.
* Inventory corrections.

Unauthorized users must not be able to directly modify inventory quantities.

---

# 21.26 Batch and Expiry Protection

Batch information should be protected against unauthorized modification.

Important fields include:

* Batch number.
* Quantity.
* Expiry date.
* Received date.
* Supplier.
* Stock status.

Changes to sensitive batch information should be recorded in audit logs where appropriate.

---

# 21.27 Protection Against Expired Stock Consumption

The backend must prevent expired stock from being consumed through normal inventory operations.

Before stock consumption, the system should verify:

```text id="qz2q3j"
Batch Exists?
     ↓
Available Quantity?
     ↓
Not Expired?
     ↓
Eligible for Consumption?
     ↓
Consume Stock
```

The frontend should not be trusted to enforce this rule.

---

# 21.28 Recipe Security

Only authorized users should be able to create or modify recipes.

Recipes directly affect inventory consumption, so unauthorized changes could cause incorrect stock calculations.

For example, changing:

```text id="x8b2y9w"
Milk = 200 ml
```

to:

```text id="qf6v8m"
Milk = 2 ml
```

could produce inaccurate inventory records.

Therefore recipe modification should be permission-controlled and auditable.

---

# 21.29 Order Security

Orders should be protected from unauthorized modification.

The system should enforce valid order states.

For example:

```text id="0x4j5r"
Draft
  ↓
Confirmed
  ↓
Preparing
  ↓
Completed
```

An already completed order should not normally be freely edited.

Cancellation or reversal of completed orders should require appropriate permission and should be audited.

---

# 21.30 Payment Security

Payment information must be protected.

The system should:

* Restrict payment operations to authorized users.
* Validate payment amounts.
* Prevent invalid payment values.
* Prevent unauthorized modification of completed payments.
* Audit important payment changes.

If external payment providers are introduced in the future, sensitive payment credentials should be handled according to the provider's security requirements.

---

# 21.31 Financial Data Protection

Financial information should be accessible only to authorized users.

This includes:

* Sales totals.
* Payment records.
* Expenses.
* Purchase costs.
* Financial reports.

The UI and API should both respect financial permissions.

---

# 21.32 User Management Security

Only authorized administrators should be able to manage users.

User-management functions include:

* Creating users.
* Activating/deactivating accounts.
* Assigning roles.
* Changing permissions.
* Resetting credentials where applicable.

A user must not be able to elevate their own privileges.

For example:

```text id="1e5kkv"
Cashier
   ↓
Cannot assign self
   ↓
Administrator
```

---

# 21.33 Privilege Escalation Protection

The system must prevent horizontal and vertical privilege escalation.

### Vertical Privilege Escalation

A Cashier must not become an Administrator by modifying an API request.

### Horizontal Privilege Escalation

One staff member must not access or modify another user's restricted information without authorization.

All role and permission changes must be validated by the backend.

---

# 21.34 Account Deactivation

When an employee no longer needs access to the system, their account should be deactivated rather than immediately deleted where historical records depend on that account.

This allows existing:

* Orders.
* Expenses.
* Stock movements.
* Audit logs.

to remain associated with the user.

---

# 21.35 Audit Logging

Important business and security events should be recorded.

Examples include:

* Login attempts.
* Successful logins.
* Failed login attempts.
* User creation.
* User deactivation.
* Role assignment.
* Permission changes.
* Stock adjustments.
* Waste records.
* Purchase receiving.
* Order cancellation.
* Expense changes.
* Important configuration changes.

---

# 21.36 Audit Log Protection

Audit logs must not be freely editable by normal users.

The system should prevent users from:

* Modifying audit history.
* Deleting audit records.
* Changing the recorded user.
* Changing the original timestamp.

Only authorized administrators may have controlled access to audit records.

---

# 21.37 Logging Sensitive Information

Logs must not contain sensitive information unnecessarily.

The system should avoid recording:

* Passwords.
* Authentication tokens.
* Secret keys.
* Full payment credentials.
* Other sensitive security information.

---

# 21.38 Failed Login Protection

The system should monitor repeated failed login attempts.

Where necessary, appropriate controls may include:

* Rate limiting.
* Temporary account protection.
* Login monitoring.
* Additional verification mechanisms.

The exact implementation should balance security with the needs of internal cafe staff.

---

# 21.39 API Rate Limiting

Rate limiting should be considered for sensitive endpoints, particularly:

* Login.
* Token refresh.
* Password changes.
* User management.
* Other security-sensitive operations.

This helps reduce automated abuse and brute-force attempts.

---

# 21.40 Session Timeout

Authentication sessions should not remain active indefinitely.

The system should use reasonable token lifetimes and require re-authentication when appropriate.

This is particularly important for shared or unattended staff computers.

---

# 21.41 Shared Computer Security

Because the system is intended for internal staff, some users may access it from shared computers.

Staff should:

* Log out after completing their work.
* Avoid sharing passwords.
* Avoid saving credentials on shared machines.
* Lock the workstation when temporarily leaving it unattended.

The system should provide a clear logout function.

---

# 21.42 Error Message Security

Error messages should provide useful information without exposing internal system details.

The user should not receive:

```text id="k8f1qy"
DatabaseError: relation inventory_stock_batch does not exist...
```

Instead:

```text id="3j1s1k"
Unable to complete the operation. Please try again.
```

Detailed technical information should remain in controlled server-side logs.

---

# 21.43 File Upload Security

If the application supports file uploads in the future, uploaded files must be validated.

Controls should include:

* Allowed file types.
* Maximum file size.
* Secure file names.
* Malware/security scanning where appropriate.
* Restricted storage locations.
* Prevention of executable file uploads.

---

# 21.44 Backup Security

The database should be backed up regularly.

Backups should be:

* Protected from unauthorized access.
* Stored securely.
* Tested periodically.
* Retained according to business requirements.

Backup credentials must be protected.

---

# 21.45 Disaster Recovery

The project should define a basic recovery process.

In the event of database failure:

```text id="4gqf7h"
System Failure
      ↓
Identify Problem
      ↓
Restore Database
      ↓
Verify Data Integrity
      ↓
Restore Application
      ↓
Test Core Operations
      ↓
Return System to Service
```

The recovery procedure should be tested before production use.

---

# 21.46 Security Updates

The technologies used by the system should be kept reasonably up to date.

Security updates should be applied to:

* Django.
* Django REST Framework.
* React dependencies.
* PostgreSQL.
* Operating system.
* Web server.
* Other production dependencies.

Updates should be tested before being applied to the production environment.

---

# 21.47 Dependency Security

Only necessary third-party packages should be added.

Before adding a dependency, developers should consider:

* Whether it is necessary.
* Whether it is actively maintained.
* Whether known security vulnerabilities exist.
* Whether a simpler built-in solution is available.

Unused dependencies should not be kept unnecessarily.

---

# 21.48 Environment Security

Development and production environments should be separated.

Production secrets must not be placed directly in source code.

Examples include:

```text id="3os7qd"
SECRET_KEY
DATABASE_PASSWORD
JWT_SECRET
EMAIL_PASSWORD
API_KEYS
```

These should be managed through secure environment configuration.

---

# 21.49 Source Code Security

The Git repository must not contain:

* Passwords.
* API keys.
* Database credentials.
* JWT secrets.
* Production configuration secrets.
* Private certificates.

A `.gitignore` file should be configured appropriately.

---

# 21.50 Frontend Security

The frontend should:

* Avoid exposing secrets.
* Validate user input for usability.
* Handle authentication state securely.
* Avoid rendering untrusted HTML.
* Hide unauthorized navigation options.
* Handle expired authentication sessions.
* Avoid storing sensitive information unnecessarily.

Frontend restrictions must always be backed by backend authorization.

---

# 21.51 API Response Security

API responses should contain only the information necessary for the requesting user.

For example, a user-management response should not expose:

* Password hashes.
* Authentication tokens.
* Internal security configuration.
* Unnecessary private information.

Serializers should explicitly control which fields are returned.

---

# 21.52 Security Headers

Production responses should include appropriate security headers.

These may include:

```text id="x8q8hl"
Content-Security-Policy
X-Content-Type-Options
X-Frame-Options
Referrer-Policy
Strict-Transport-Security
```

The exact configuration should be reviewed during deployment.

---

# 21.53 Monitoring

The production system should monitor important events where practical.

Monitoring may include:

* Server availability.
* API errors.
* Database availability.
* Authentication failures.
* Background-task failures.
* Unexpected application errors.

Monitoring should not expose sensitive user information.

---

# 21.54 Security Testing

Before production deployment, the system should undergo security testing.

Testing should include:

### Authentication Testing

* Invalid credentials.
* Expired tokens.
* Invalid tokens.
* Logout behavior.

### Authorization Testing

Test each role against protected endpoints.

Example:

```text id="e5h7qd"
Cashier → Try to adjust stock
       ↓
Expected: 403 Forbidden
```

### Input Validation Testing

Test:

* Invalid quantities.
* Invalid prices.
* Invalid dates.
* Invalid IDs.
* Missing required fields.

### Injection Testing

Test protection against:

* SQL injection.
* XSS.
* Other malicious input.

### Business Rule Testing

Test:

* Expired stock consumption.
* Negative stock.
* Unauthorized order changes.
* Unauthorized financial changes.
* Unauthorized role changes.

---

# 21.55 Security Testing by Role

The following should be tested:

| Role            | Security Test                                           |
| --------------- | ------------------------------------------------------- |
| Administrator   | Verify full authorized access                           |
| Manager         | Verify operational access without system administration |
| Cashier         | Verify restriction from inventory administration        |
| Inventory Staff | Verify restriction from financial/user administration   |
| Finance Staff   | Verify restriction from inventory modification          |

Testing should confirm that both the frontend and backend behave correctly.

---

# 21.56 Security Incident Handling

If suspicious activity or a security incident occurs, the responsible administrator should:

1. Identify the incident.
2. Restrict affected accounts or systems.
3. Review audit logs.
4. Determine affected data.
5. Correct the vulnerability.
6. Restore affected services if necessary.
7. Change compromised credentials.
8. Document the incident.
9. Take measures to prevent recurrence.

---

# 21.57 Data Retention

Important operational records should be retained according to Board's Cafe business requirements.

Historical records such as:

* Orders.
* Payments.
* Purchases.
* Expenses.
* Stock movements.
* Waste.
* Audit logs.

should not be casually deleted because they may be required for reporting and accountability.

Where records should no longer be accessible through normal operations, deactivation or archival should be preferred where appropriate.

---

# 21.58 Secure Deletion

When sensitive information must be removed, deletion should follow an appropriate process.

However, records required for:

* Financial accountability.
* Audit history.
* Inventory traceability.
* Legal/business requirements.

should not be deleted simply to remove them from the interface.

---

# 21.59 Privacy

The system should collect only information necessary for Board's Cafe operations.

Staff and customer information should not be exposed unnecessarily.

Access to personal information should follow the user's role and business responsibilities.

---

# 21.60 Security Acceptance Criteria

The system will be considered secure enough for initial production use when:

* Users must authenticate before accessing protected functions.
* Passwords are securely hashed.
* JWT authentication is correctly implemented.
* Access tokens expire appropriately.
* Backend permissions are enforced.
* The five defined roles have correct access scopes.
* Users cannot elevate their own privileges.
* Unauthorized API requests are rejected.
* Input validation is implemented.
* SQL injection protections are in place.
* XSS protections are in place.
* CSRF protections are appropriately configured.
* Production communication uses HTTPS.
* Database access is protected.
* Expired stock cannot be consumed through normal inventory operations.
* Important inventory and financial operations are auditable.
* Audit logs cannot be modified by normal users.
* Sensitive credentials are not stored in source control.
* Production secrets are protected.
* Database backups are configured.
* Security-sensitive errors do not expose technical details.
* Basic security testing has been completed.

---

# 21.61 Security Principles

The Board's Cafe system should follow these principles:

### Least Privilege

Give users only the permissions they need.

### Defense in Depth

Do not depend on a single security control.

### Secure by Default

Default behavior should favor security.

### Backend Enforcement

Security rules must be enforced by the backend.

### Data Integrity

Business records must not be changed without authorization.

### Auditability

Important actions should be traceable.

### Minimal Exposure

Do not expose unnecessary information.

### Secure Configuration

Production systems must use secure configuration.

### Regular Updates

Dependencies and infrastructure should receive appropriate security updates.

---

# 21.62 Final Security Architecture

The security model can be summarized as:

```text id="r2k6c4"
                     Staff User
                         │
                         ▼
                       HTTPS
                         │
                         ▼
                    Login / JWT
                         │
                         ▼
                  Authentication
                         │
                         ▼
                 Role + Permission
                     Verification
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       Input Validation       Business Rules
              │                     │
              └──────────┬──────────┘
                         ▼
                  Django Backend
                         │
                 Transaction Safety
                         │
                         ▼
                    PostgreSQL
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          Audit Logs  Backups   Monitoring
```

---

# 21.63 Final Security Decision

Board's Cafe will use a **defense-in-depth security approach**.

Authentication will identify users, while role-based permissions will determine what each user is allowed to do.

The backend will remain the final authority for all access-control decisions.

The system will protect critical operations such as:

* Order management.
* Inventory management.
* Batch and expiry management.
* Recipe modification.
* Stock consumption.
* Purchases.
* Payments.
* Expenses.
* Waste.
* User management.
* Role and permission management.

Particular attention will be given to preventing unauthorized inventory changes, unauthorized financial changes, privilege escalation, and consumption of expired stock.

All important operations should be traceable through audit logging.

The system will therefore provide the foundation required for a secure internal cafe management platform while keeping the architecture practical and appropriate for the size and needs of Board's Cafe.

---

# 21.64 Documentation Set Completion

The current Board's Cafe documentation set is now complete:

```text id="4qv6gj"
01  Project Overview
02  Business Requirements
03  Functional Requirements
04  User Roles & Permissions
05  Business Workflows

06  Products & Recipes
07  Inventory Management
08  Batch & Expiry Management
09  POS & Order Management
10  Purchases & Suppliers
11  Expenses & Payments
12  Waste Management
13  Reports & Dashboard
14  Notifications & Alerts
15  Audit Logging

16  Database Design
17  ERD
18  API Documentation
19  UI/UX Requirements
20  Technical Architecture
21  Security Requirements
```

These documents now form the **functional and technical baseline** for implementation.

---