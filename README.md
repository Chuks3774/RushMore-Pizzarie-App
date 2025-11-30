

# 🍕 Rushmore Pizzeria App (Interactive Python Ordering System)  
![alt text](image-3.png)
A JSON-based CLI application for real-time pizza ordering, cart management, receipts, and staff analytics.  
This project implements a fully interactive command-line pizza ordering app for RushMore Pizzeria.
Customers can order pizzas by slice or box, discounts are applied based on quantities, review their cart, receipts are generated and saved all orders in a persistent JSON database. Staff can also view real-time sales reports and order summaries.

It demonstrates clean Python programming, modular functions, basic data persistence, and user-friendly CLI design, forming the foundation for a scalable restaurant management system.


---

##  Features
#### Customer Ordering System

- Order pizzas by box (with bulk discounts)

- Order by slice (with slice-based discount)

- Automatic price calculation and validation (e.g., max 16 slices per order)

- Add multiple items to cart

- Real-time cart preview and editing  
### Checkout and Receipt Generation

Generate customer receipts with:

- Itemized list

- Discounts applied

- Final total

- Timestamped order history
### Persistent Storage

- All transactions are saved in pizza_orders.json

This ensures:

- Orders are stored even after program closes

- Staff can analyze historical data

- No SQL required, lightweight + easy portability
### Staff Sales Summary

- Total revenue

- Units sold per menu item

- Sales grouped by “box” or “slice”

- Order history (timestamps, quantities, prices)

---
### Sample Code Snippet
This logic powers discounts and price calculations for slices and boxes.
```python
def calculate_payment(price, quantity, discount_rate=0.0):
    total = price * quantity
    discount = total * discount_rate
    return total - discount
```
## Sample Screenshot
### 🛒 Cart View
![Cart Screenshot](./images/cart.png)

### 🧾 Receipt View
![Receipt Screenshot](./images/receipt.png)

### 📊 Sales Summary
![Sales Summary Screenshot](./images/sales_summary.png)
### How It Works

1 Select a pizza

Press a number (1–9) to choose from the menu.

2 Choose ordering type

B → Box

S → Slice
Discounts are applied automatically.

3 Add multiple items to the cart and View or edit cart anytime.

4 Checkout

Your order is saved to JSON and a receipt is printed.

5 Staff Mode

Use the m key to view total sales and item breakdown.

Tech Stack

Programming Language -	   Python
Persistence  -	JSON Storage
Libraries  -	json, datetime, os
Interface Type  -	CLI (Command Line Interface)

IDE  -	VS Code / PyCharm
Version Control  -	Git + GitHub
### Skills Demonstrated
(1) Python Programming

- Modular function design

- Error handling

- CLI input management

- Loops, conditions, data structures

(2) Data Persistence

- JSON-based storage

- Reading/writing files safely

- Handling JSONDecodeError

- Timestamped order logging

(3) Business Logic Implementation

- Pricing models (slice vs box)

- Dynamic discount rules

- Cart & checkout simulation

- Realistic receipt formatting

(4) Reporting and Analytics

- Summaries for staff

- Revenue calculations

- Product-level analytics

(5) Software Design Concepts

- Separation of concerns

- Reusable functions

- Simple, scalable architecture

- User-friendly CLI design
### Challenges and How I Solved Them
#### 1 JSON File Corruption During Write

Sometimes the JSON file could become unreadable if the app closed mid-write.

Solution:
I used truncate() and seek(0) to ensure clean file overwrites.

#### 2 Input Validation for Non-Numeric Values

Users could type “ten slices” instead of “10”.

Solution:
 I added isdigit() checks and validation loops.

#### 3 Sales Summary Needing Both Revenue and Quantity Aggregation

Staff summary had to track both item counts and revenue.

Solution:
I used dictionary grouping by (pizza_type, order_type).

### Conclusion

The RushMore Pizzeria CLI Ordering System is a practical demonstration of:

clean Python development

user-driven command-line interfaces

persistent JSON storage

business logic modeling

receipt generation

staff analytics

While lightweight, it captures the full flow of a small restaurant’s digital ordering system and lays the groundwork for future expansions such as SQL databases, web interfaces, or cloud integration.