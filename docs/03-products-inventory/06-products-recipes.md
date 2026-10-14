# 06 — Products & Recipes

## 1. Purpose

This document defines how Board’s Cafe manages its products, ingredients, recipes, units of measurement, and the relationship between products and inventory.

The purpose is to make sure the system can answer questions such as:

* What products does Board’s Cafe sell?
* What ingredients are required to make each product?
* How much of each ingredient is required?
* Which inventory items are shared by several products?
* How much stock is required when a customer places an order?
* Which stock batches should be consumed?
* Which ingredients have expired and therefore cannot be used?
* How does the system update inventory after production?

The Products & Recipes module is directly connected to:

* Inventory Management
* Batch & Expiry Management
* POS Order Management
* Kitchen/Production
* Purchases
* Waste Management
* Reports
* Notifications

---

# 2. Product Concept

A **product** is an item that Board’s Cafe can sell to a customer.

Examples may include:

* Cappuccino
* Coffee
* Tea
* Fresh Juice
* Pancakes
* Burger
* Sandwich
* Cake
* Other food and beverage items offered by the cafe

Products are normally customer-facing and have information such as:

* Product name
* Category
* Description
* Selling price
* Status
* Recipe
* Availability

A product may be prepared when a customer places an order.

For example:

```text
Customer orders Cappuccino
        ↓
System identifies Cappuccino recipe
        ↓
System calculates required ingredients
        ↓
Kitchen prepares Cappuccino
        ↓
Ingredients are consumed from inventory
        ↓
Order is completed
```

---

# 3. Product Categories

Products should be grouped into categories to make management and reporting easier.

Examples:

```text
Beverages
    ├── Coffee
    ├── Tea
    └── Juice

Food
    ├── Breakfast
    ├── Sandwiches
    ├── Burgers
    └── Snacks

Bakery
    ├── Cakes
    ├── Bread
    └── Pastries
```

The exact categories can be configured by authorized staff.

A category should contain information such as:

* Category ID
* Category name
* Description
* Status
* Created date
* Updated date

A category can contain many products.

```text
Category
   │
   └──< Product
```

---

# 4. Product Information

Each product should have at least the following information:

| Field         | Description                   |
| ------------- | ----------------------------- |
| Product ID    | Unique identifier             |
| Product Name  | Name displayed to staff       |
| Category      | Product category              |
| Description   | Optional product description  |
| Selling Price | Price charged to the customer |
| Status        | Active or inactive            |
| Recipe        | Ingredients required          |
| Created By    | Staff member who created it   |
| Created At    | Creation date/time            |
| Updated At    | Last modification date/time   |

Example:

```text
Product:
Cappuccino

Category:
Coffee

Selling Price:
2,000 RWF

Status:
Active
```

---

# 5. Product Status

Products should have a status so that the cafe can control whether they are available for sale.

Suggested statuses:

```text
ACTIVE
INACTIVE
```

### Active

An active product can normally be selected when creating an order.

### Inactive

An inactive product should not normally be available for new orders.

A product may be made inactive when:

* The cafe temporarily stops selling it.
* The product is permanently discontinued.
* Its recipe is being reviewed.
* Required ingredients are no longer available.
* Management decides to remove it from the menu.

Changing product status should require the appropriate permission.

---

# 6. Menu Product vs Inventory Item

The system must clearly distinguish between a **sellable product** and an **inventory item**.

They are related but they are not the same thing.

### Menu Product

A menu product is something the customer purchases.

Example:

```text
Cappuccino
Pancakes
Burger
Fresh Juice
```

### Inventory Item

An inventory item is something the cafe keeps in stock and uses for production or other operations.

Example:

```text
Milk
Wheat Flour
Eggs
Sugar
Coffee Beans
Cooking Oil
```

The relationship can be represented as:

```text
MENU PRODUCT
     │
     │ requires
     ▼
   RECIPE
     │
     │ uses
     ▼
INVENTORY ITEM
```

This distinction is important because customers normally order products, while the kitchen consumes inventory items.

---

# 7. Inventory Items Used as Ingredients

An inventory item can be used by many products.

For example:

```text
Milk
 │
 ├── Cappuccino
 ├── Latte
 ├── Tea with Milk
 └── Pancakes
```

Similarly:

```text
Wheat Flour
 │
 ├── Pancakes
 ├── Bread
 ├── Cake
 └── Pastries
```

Therefore, the system must not store a single ingredient directly inside a product record.

Instead, the relationship should be managed through recipes.

---

# 8. Recipe Concept

A **recipe** defines the ingredients and quantities required to produce a product.

For example:

```text
Product: Cappuccino

Recipe:
    Coffee Beans → 20 g
    Milk         → 150 ml
    Sugar        → 10 g
```

Another product may use some of the same ingredients:

```text
Product: Latte

Recipe:
    Coffee Beans → 20 g
    Milk         → 200 ml
```

This allows the system to correctly manage shared ingredients.

---

# 9. Recipe Structure

A recipe should contain:

* Recipe ID
* Product
* Recipe name/version if required
* Yield quantity
* Yield unit
* Status
* Instructions
* Created by
* Created date
* Updated date

The recipe's individual ingredients should be stored separately.

Conceptually:

```text
Product
   │
   └── Recipe
          │
          ├── Recipe Ingredient
          ├── Recipe Ingredient
          └── Recipe Ingredient
```

---

# 10. Recipe Ingredients

A **recipe ingredient** connects a recipe to an inventory item.

It defines how much of an inventory item is required.

Example:

```text
Recipe: Pancakes

Ingredient                  Quantity
-------------------------------------
Wheat Flour                 100 g
Milk                        150 ml
Eggs                        1 piece
Sugar                       20 g
Cooking Oil                 10 ml
```

The system therefore needs a relationship such as:

```text
Recipe
   │
   └──< Recipe Ingredient >── Inventory Item
```

This structure allows one inventory item to appear in many recipes.

---

# 11. Example of Shared Ingredients

Consider three products.

### Cappuccino

```text
20 g Coffee Beans
150 ml Milk
10 g Sugar
```

### Latte

```text
20 g Coffee Beans
200 ml Milk
```

### Pancakes

```text
100 g Wheat Flour
150 ml Milk
1 Egg
20 g Sugar
10 ml Cooking Oil
```

Milk is therefore shared by several products.

```text
                  ┌── Cappuccino
                  │
Milk ─────────────┼── Latte
                  │
                  └── Pancakes
```

The database must support this relationship without duplicating the Milk inventory item.

---

# 12. Units of Measurement

The system should record quantities using appropriate units.

Examples:

### Weight

```text
g
kg
```

### Volume

```text
ml
L
```

### Count

```text
piece
unit
```

The unit should be associated with the inventory item or recipe requirement.

Examples:

```text
Milk       → ml / L
Wheat Flour → g / kg
Eggs       → piece
Sugar      → g / kg
Coffee Beans → g / kg
```

---

# 13. Unit Consistency

The system must be able to calculate quantities correctly when inventory and recipes use different but compatible units.

For example:

```text
Inventory:
Milk = 10 L

Recipe:
Milk = 150 ml per Cappuccino
```

The system should understand that:

```text
10 L = 10,000 ml
```

Therefore:

```text
10,000 ml ÷ 150 ml
≈ 66 Cappuccinos
```

The system should not allow incompatible units to be combined incorrectly.

For example:

```text
Milk: 150 ml
Eggs: 1 piece
```

These quantities should remain separate because they represent different measurement types.

---

# 14. Recipe Yield

Some recipes produce more than one unit of a product.

For example:

```text
Recipe: Pancake Batch

Yield:
10 pancakes
```

The recipe may require:

```text
500 g Wheat Flour
750 ml Milk
5 Eggs
100 g Sugar
```

If a customer orders 20 pancakes, the system should calculate the required quantities based on the recipe yield.

Example:

```text
Recipe yield = 10 pancakes

Customer order = 20 pancakes

Multiplier:
20 ÷ 10 = 2
```

Required ingredients:

```text
Wheat Flour = 500 g × 2 = 1,000 g
Milk        = 750 ml × 2 = 1,500 ml
Eggs        = 5 × 2 = 10 eggs
Sugar       = 100 g × 2 = 200 g
```

This calculation allows the kitchen and inventory system to determine the required stock before production.

---

# 15. Recipe Versioning

Recipes may change over time.

For example:

```text
Old Cappuccino Recipe
Milk = 150 ml

New Cappuccino Recipe
Milk = 180 ml
```

The system should avoid silently changing historical production information.

Where recipe versioning is implemented, each version should have:

* Version number
* Effective date
* Status
* Ingredients
* Quantities
* Created by
* Approved by, where required

Example:

```text
Cappuccino
   │
   ├── Recipe Version 1
   │      Milk = 150 ml
   │
   └── Recipe Version 2
          Milk = 180 ml
```

The active recipe version should be used for new orders.

Historical orders and production records should retain the recipe/quantity information used at the time.

---

# 16. Recipe Creation Workflow

Only authorized staff should create recipes.

The workflow is:

```text
Open Product
      ↓
Create Recipe
      ↓
Select Inventory Item
      ↓
Enter Quantity
      ↓
Select Unit
      ↓
Add More Ingredients
      ↓
Define Yield
      ↓
Save Recipe
      ↓
Validate Recipe
      ↓
Activate Recipe
```

The system should validate that:

* The product exists.
* The inventory item exists.
* Required quantities are greater than zero.
* Units are valid.
* The recipe contains at least the required ingredients.
* Duplicate ingredients are not accidentally added to the same recipe.
* The recipe can be activated only when its required information is complete.

---

# 17. Product Creation Workflow

The product creation process should be:

```text
Create Product
      ↓
Select Category
      ↓
Enter Product Details
      ↓
Set Selling Price
      ↓
Save Product
      ↓
Create Recipe
      ↓
Add Ingredients
      ↓
Set Quantities
      ↓
Validate Recipe
      ↓
Activate Product
```

Depending on Board’s Cafe's workflow, a product may be created before its recipe is completed.

However, a product that requires production should not normally be made available for production until its recipe is properly configured.

---

# 18. Product Price Management

Each sellable product should have a selling price.

Example:

```text
Product: Cappuccino
Price: 2,000 RWF
```

Authorized users may update prices.

Price changes should be controlled because they directly affect sales and financial reports.

The system should record:

* Previous price
* New price
* User who changed the price
* Date/time
* Reason, where required

Historical orders should retain the price that was actually charged.

For example:

```text
Old price = 2,000 RWF
New price = 2,500 RWF
```

An old order should still show:

```text
Unit Price = 2,000 RWF
```

rather than changing to 2,500 RWF.

---

# 19. Product Availability and Inventory

A product may be active but temporarily unavailable if its required ingredients cannot be produced.

For example:

```text
Cappuccino
    ↓
Requires Milk
    ↓
Milk unavailable
    ↓
Cappuccino cannot currently be produced
```

The system should help staff identify this situation.

However, product availability should not be determined simply by whether one ingredient has low stock.

The system should calculate whether enough usable inventory exists for the requested quantity.

Importantly:

> Expired inventory must not be considered available for production.

---

# 20. Product Availability Calculation

When a customer orders a product, the system should determine whether the required ingredients are available.

Example:

```text
Order:
5 Cappuccinos
```

Recipe:

```text
20 g Coffee Beans
150 ml Milk
10 g Sugar
```

Required:

```text
Coffee Beans = 100 g
Milk         = 750 ml
Sugar        = 50 g
```

The system checks usable inventory for each ingredient.

```text
Coffee Beans → Available
Milk         → Available
Sugar        → Available
```

If all required ingredients are available:

```text
Production can proceed.
```

If one is unavailable:

```text
Production cannot proceed normally.
```

---

# 21. Expired Ingredients

Expired inventory must never be treated as usable ingredients.

Example:

```text
Milk Batch A
Expiry: 10 October
Quantity: 5 L

Current Date:
12 October
```

The batch is expired.

Therefore:

```text
Usable Milk = 0 L from Batch A
```

The system should prevent normal production from consuming this batch.

The expired quantity should instead be handled through the Waste Management process.

---

# 22. FEFO and Recipes

Recipes define **what** ingredients are needed.

Inventory and batch management determine **which stock** is consumed.

The system should use FEFO:

> First-Expire, First-Out.

Example:

```text
Milk Batch A
Expiry: 10 Oct
Quantity: 5 L

Milk Batch B
Expiry: 15 Oct
Quantity: 10 L

Milk Batch C
Expiry: 20 Oct
Quantity: 8 L
```

If the kitchen needs 6 L:

```text
Consume Batch A → 5 L
Consume Batch B → 1 L
```

The recipe does not choose the batch.

The inventory/production process chooses the appropriate batch using FEFO.

---

# 23. Production on Customer Order

Board’s Cafe may prepare products when customers place orders.

The system should therefore support:

```text
Customer Order
      ↓
Order Items
      ↓
Recipe Lookup
      ↓
Ingredient Calculation
      ↓
Inventory Availability Check
      ↓
FEFO Batch Selection
      ↓
Kitchen Preparation
      ↓
Ingredient Consumption
      ↓
Product Ready
      ↓
Order Completion
```

This is important because stock consumption may happen as part of production rather than when the product is first added to the menu.

---

# 24. Multiple Products in One Order

A customer may order several products.

Example:

```text
Order #1001

2 Cappuccinos
1 Pancake
1 Fresh Juice
```

The system calculates the ingredients required for every order item.

Example:

```text
Cappuccino × 2
    Coffee Beans → 40 g
    Milk         → 300 ml
    Sugar        → 20 g

Pancake × 1
    Wheat Flour  → 100 g
    Milk         → 150 ml
    Egg          → 1
    Sugar        → 20 g

Fresh Juice × 1
    Fruit        → required quantity
```

The system should aggregate shared ingredients.

Therefore:

```text
Total Milk
= 300 ml + 150 ml
= 450 ml
```

Instead of treating the two Milk requirements independently.

---

# 25. Ingredient Requirement Calculation

The system should calculate:

```text
Required Quantity =
Recipe Quantity × Ordered Quantity
```

Where recipes have yields greater than one, the calculation should also account for the recipe yield.

The final requirement should be grouped by inventory item.

Example:

```text
Order:
2 Cappuccinos
1 Pancake

Requirements:

Coffee Beans → 40 g
Milk         → 450 ml
Sugar        → 40 g
Wheat Flour  → 100 g
Eggs         → 1 piece
```

This aggregated requirement can then be checked against inventory.

---

# 26. Ingredient Consumption

Once production is approved and the product is prepared, the system records the inventory consumption.

Example:

```text
Milk required = 450 ml

Milk Batch A = 300 ml available
Milk Batch B = 1 L available
```

Using FEFO:

```text
Consume 300 ml from Batch A
Consume 150 ml from Batch B
```

The system should create appropriate stock movement/consumption records.

---

# 27. Inventory Quantity vs Recipe Quantity

The system should not confuse:

```text
Inventory Quantity
```

with:

```text
Recipe Quantity
```

Example:

```text
Inventory:
Milk = 20 L

Recipe:
Milk = 150 ml per Cappuccino
```

The recipe tells the system how much is needed per product.

The inventory tells the system how much is currently available.

They work together during production.

---

# 28. Product Without a Recipe

Not every record necessarily needs a recipe.

For example, a product that is directly sold without production may not require ingredient consumption through a recipe.

However, any product that is produced from ingredients should have a valid recipe before it can be produced through the normal production workflow.

The system should clearly identify whether a product is:

```text
DIRECT SALE
```

or:

```text
RECIPE-BASED
```

This classification should be defined during product setup.

---

# 29. Direct-Sale Products

A direct-sale product is sold without the system calculating ingredient consumption from a recipe.

Example:

```text
Bottled Water
```

If Board’s Cafe purchases bottled water and sells it directly, the stock item itself may be sold.

The workflow can be:

```text
Purchase
   ↓
Receive Stock
   ↓
Store
   ↓
Customer Order
   ↓
Sell Product
   ↓
Reduce Stock
```

This is different from:

```text
Milk
   ↓
Used in Cappuccino
   ↓
Production
   ↓
Customer receives Cappuccino
```

The system should support both cases if required by the cafe's operations.

---

# 30. Prepared or Intermediate Products

Board’s Cafe may have items that are prepared in advance and then used in other products.

For example:

```text
Ingredient:
Tomatoes + Onions + Oil
        ↓
Prepared Sauce
        ↓
Used in Burger
```

If Board’s Cafe uses this type of process, the system can support an intermediate/prepared product with its own recipe.

Conceptually:

```text
Raw Ingredients
      ↓
Prepared Product
      ↓
Final Product
```

For the initial implementation, this should only be introduced if Board’s Cafe actually needs it. It should not unnecessarily complicate the first version of the system.

---

# 31. Recipe Validation

Before a recipe becomes active, the system should validate it.

Validation should check:

### Product

* Product exists.
* Product is valid.
* Product is not deleted.

### Ingredients

* Inventory item exists.
* Inventory item is active.
* Ingredient quantity is greater than zero.
* Unit is valid.
* Ingredient is not duplicated unnecessarily.

### Recipe

* Recipe contains required ingredients.
* Yield is valid.
* Yield quantity is greater than zero.
* Recipe status is valid.

---

# 32. Updating Recipes

Authorized staff may update recipes.

For example:

```text
Before:
Milk = 150 ml

After:
Milk = 180 ml
```

Recipe changes can significantly affect inventory consumption and product costs.

Therefore, important recipe changes should be audited.

The system should record:

```text
Who changed the recipe?
What changed?
When was it changed?
What was the previous value?
What is the new value?
```

---

# 33. Deleting Products and Recipes

Products and recipes should not normally be physically deleted when they have already been used in historical transactions.

Instead, they should normally be deactivated or archived.

For example:

```text
Product:
Chocolate Cake

Status:
INACTIVE
```

This allows historical orders and reports to remain understandable.

The same principle applies to recipes that have been used for previous production.

---

# 34. Historical Accuracy

Historical sales and production records must remain accurate even when product information changes later.

Example:

```text
1 January
Cappuccino price = 2,000 RWF
```

An order placed on 1 January should retain:

```text
Cappuccino
Quantity: 1
Unit Price: 2,000 RWF
```

If the price later changes to:

```text
2,500 RWF
```

the old order should not change.

Similarly, historical production records should preserve the quantities actually consumed.

---

# 35. Cost Consideration

Recipes can also support product cost calculation.

For example:

```text
Cappuccino

Coffee Beans = 20 g
Milk         = 150 ml
Sugar        = 10 g
```

If the system knows the cost of the consumed inventory, it can estimate:

```text
Ingredient Cost
        ↓
Product Cost
        ↓
Selling Price
        ↓
Estimated Margin
```

This can support management reports.

However, the exact costing method should be defined in the Inventory/Financial requirements and should remain consistent with the selected inventory valuation approach.

---

# 36. Product and Recipe Permissions

Access to product and recipe functions should be controlled through the RBAC system.

Examples:

```text
products.view
products.create
products.update
products.delete
products.change_price
products.change_status

recipes.view
recipes.create
recipes.update
recipes.delete
```

Only users with the appropriate permissions should perform these operations.

Sensitive changes such as price and recipe changes should be audited.

---

# 37. Relationship with Orders

The relationship between products and orders is:

```text
Customer
    ↓
Order
    ↓
Order Item
    ↓
Product
```

An order can contain multiple order items.

Example:

```text
Order #1001

2 × Cappuccino
1 × Pancake
1 × Fresh Juice
```

Each order item identifies:

* Product
* Quantity
* Unit price
* Subtotal

The order item should preserve the price used when the order was created.

---

# 38. Relationship with Inventory

For recipe-based products:

```text
Product
   ↓
Recipe
   ↓
Recipe Ingredient
   ↓
Inventory Item
   ↓
Inventory Batch
```

This allows the system to trace:

```text
What was sold?
       ↓
What was produced?
       ↓
What ingredients were required?
       ↓
Which inventory items were used?
       ↓
Which batches were consumed?
```

This traceability is important for stock control and expiry management.

---

# 39. Product-to-Inventory Example

Consider:

```text
Product:
Pancakes
```

Recipe:

```text
100 g Wheat Flour
150 ml Milk
1 Egg
20 g Sugar
10 ml Cooking Oil
```

Inventory:

```text
Wheat Flour
Milk
Eggs
Sugar
Cooking Oil
```

When a customer orders:

```text
3 Pancakes
```

The system calculates:

```text
Wheat Flour → 300 g
Milk        → 450 ml
Eggs        → 3
Sugar       → 60 g
Cooking Oil → 30 ml
```

The system then checks usable batches and consumes stock according to the inventory rules.

---

# 40. Product-to-Production Example

The complete process is:

```text
Customer
   ↓
Orders Pancakes
   ↓
Order Created
   ↓
Recipe Retrieved
   ↓
Ingredient Requirements Calculated
   ↓
Inventory Checked
   ↓
FEFO Batches Selected
   ↓
Kitchen Receives Production Task
   ↓
Pancakes Prepared
   ↓
Ingredients Consumed
   ↓
Stock Updated
   ↓
Pancakes Marked Ready
   ↓
Order Completed
```

---

# 41. Business Rules

The Products & Recipes module should follow these rules:

1. Every product must have a unique identifier.
2. Every product should belong to a valid category where categories are required.
3. Product prices must be greater than or equal to zero according to the cafe's pricing rules.
4. Only active products should normally be available for new orders.
5. Recipe-based products must have a valid active recipe before normal production.
6. Recipe quantities must be greater than zero.
7. An inventory item may be used by many recipes.
8. A recipe may contain many inventory items.
9. The same inventory item should not be unnecessarily duplicated within one recipe.
10. Expired inventory must not be used for production.
11. Inventory batches must be selected according to FEFO where applicable.
12. Customer order quantities must be used to calculate ingredient requirements.
13. Shared ingredients must be aggregated when calculating total requirements.
14. Product price changes must not change historical order prices.
15. Historical production records must remain unchanged when recipes are later modified.
16. Important product and recipe changes must be audited.
17. Deactivation should normally be preferred over deletion for records already used in transactions.
18. Only authorized users may create, update, deactivate, or delete products and recipes.
19. Units must be compatible when calculating ingredient quantities.
20. The system must not consume stock from blocked or expired batches.

---

# 42. Main Entities Introduced

This document introduces the following important entities for the later database design:

```text
Category
Product
Recipe
RecipeIngredient
InventoryItem
```

These entities will connect with entities introduced in other modules.

The broader relationship will eventually look like:

```text
Category
   │
   └──< Product
            │
            └──< Recipe
                    │
                    └──< RecipeIngredient >── InventoryItem
                                                     │
                                                     └──< Batch
```

Orders will connect to products:

```text
Order
   │
   └──< OrderItem >── Product
```

Inventory consumption will connect production/order activity to batches:

```text
Order
   ↓
Production
   ↓
Ingredient Consumption
   ↓
Batch
```

---

# 43. Module Summary

The Products & Recipes module provides the foundation for connecting what Board’s Cafe sells with what it keeps in stock.

The core model is:

```text
PRODUCT
   ↓
RECIPE
   ↓
RECIPE INGREDIENT
   ↓
INVENTORY ITEM
   ↓
BATCH
```

When a customer orders a recipe-based product:

```text
ORDER
  ↓
PRODUCT
  ↓
RECIPE
  ↓
CALCULATE INGREDIENTS
  ↓
CHECK USABLE STOCK
  ↓
SELECT FEFO BATCHES
  ↓
PRODUCE
  ↓
CONSUME INGREDIENTS
  ↓
UPDATE INVENTORY
```

This design allows Board’s Cafe to manage shared ingredients such as milk, wheat flour, sugar, eggs, coffee beans, and cooking oil without duplicating inventory records.

It also provides the foundation for expiry tracking, stock consumption, production, waste reduction, and accurate reporting.

---

# 44. Preparation for the Next Modules

The Products & Recipes module provides the foundation for the next documentation areas.

### Inventory Management

Will define:

* Inventory items
* Stock quantities
* Stock locations
* Stock movements
* Receiving
* Consumption
* Adjustments
* Transfers

### Batch & Expiry Management

Will define:

* Batches
* Batch quantities
* Expiry dates
* FEFO
* Expiry alerts
* Expired stock
* Blocked batches
* Waste handling

### POS Order Management

Will define:

* Customer orders
* Order items
* Order status
* Order confirmation
* Kitchen workflow
* Order completion
* Cancellation
* Refunds

Together, these modules will provide the complete connection:

```text
PRODUCT
   ↓
RECIPE
   ↓
INGREDIENT
   ↓
INVENTORY
   ↓
BATCH
   ↓
EXPIRY
   ↓
ORDER
   ↓
PRODUCTION
   ↓
CONSUMPTION
   ↓
STOCK UPDATE
```

This relationship will later be reflected in the final database design and ERD.
