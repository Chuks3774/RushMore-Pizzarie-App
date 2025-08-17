import json
from datetime import datetime
import os

pizza_data = {
    "1": {"name": "Classic", "price": 3.4},
    "2": {"name": "Chicken", "price": 4.5},
    "3": {"name": "Pepperoni", "price": 4.0},
    "4": {"name": "Deluxe", "price": 6.0},
    "5": {"name": "Vegetable", "price": 4.0},
    "6": {"name": "Chocolate", "price": 12.0},
    "7": {"name": "Cheese", "price": 5.0},
    "8": {"name": "Hawaiian", "price": 7.0},
    "9": {"name": "Greek", "price": 8.0}
}

ORDERDB_FILE = 'pizza_orders.json'
cart = []

def save_order_to_json_batch(order_list):
    timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    for order in order_list:
        order['order_datetime'] = timestamp

    if os.path.exists(ORDERDB_FILE):
        with open(ORDERDB_FILE, 'r+', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
            data.extend(order_list)
            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=4)
    else:
        with open(ORDERDB_FILE, 'w', encoding='utf-8') as file:
            json.dump(order_list, file, indent=4)
    print(f"\n Order successfully saved to '{ORDERDB_FILE}'!\n")

def print_receipt(order_list):
    print("\n========== RUSHMORE PIZZERIA RECEIPT ==========")
    total_cost = 0
    for item in order_list:
        print(f"{item['quantity']} x {item['pizza_type']} ({item['order_type']}) - ${item['total_price']:.2f} (Discount: {item['discount_applied']})")
        total_cost += item['total_price']
    print(f"TOTAL PAID: ${total_cost:.2f}")
    print("Thank you for ordering with RushMore Pizzeria!")
    print("===============================================\n")

def view_cart():
    if not cart:
        print("\nCart is currently empty.")
        return
    print("\n--- CURRENT CART ---")
    for idx, item in enumerate(cart, 1):
        print(f"{idx}. {item['quantity']} x {item['pizza_type']} ({item['order_type']}) - ${item['total_price']:.2f} (Discount: {item['discount_applied']})")
    print("----------------------")

def edit_cart():
    view_cart()
    if not cart:
        return
    while True:
        choice = input("\nEnter item number to remove, 'c' to clear cart, or 'b' to go back: ").strip().lower()
        if choice == 'b':
            break
        elif choice == 'c':
            cart.clear()
            print("Cart cleared.")
            break
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(cart):
                removed = cart.pop(idx)
                print(f"Removed {removed['pizza_type']} ({removed['order_type']}) from cart.")
                break
            else:
                print("Invalid item number.")
        else:
            print("Invalid input.")

def checkout():
    view_cart()
    if not cart:
        return
    confirm = input("\nWould you like to place the order? (yes/no): ").strip().lower()
    if confirm == 'yes':
        save_order_to_json_batch(cart)
        print_receipt(cart)
        cart.clear()
    else:
        print("Order cancelled.")

def calculate_payment(price, quantity, discount_rate=0.0):
    total = price * quantity
    discount = total * discount_rate
    return total - discount

def handle_box_order(pizza_name, price):
    while True:
        qty_input = input("How many Box(es) do you want? (or type 'q' to cancel): ").strip()
        if qty_input.lower() == 'q':
            print('Box Order Cancelled')
            return
        elif qty_input.isdigit():
            quantity = int(qty_input)
            break
        else:
            print("Please enter a valid number.")

    discount_rate = 0.10 if 5 <= quantity < 10 else 0.20 if quantity >= 10 else 0.0
    total = calculate_payment(price=price, quantity=quantity, discount_rate=discount_rate)
    print(f"Added to cart: {quantity} x {pizza_name} Box(es) - ${total:.2f}")
    cart.append({
        'pizza_type': pizza_name,
        'order_type': 'Box',
        'quantity': quantity,
        'total_price': total,
        'discount_applied': f"{int(discount_rate * 100)}%"
    })

def handle_slice_order(pizza_name, slice_price):
    while True:
        qty_input = input("How many slices do you want? (or type 'q' to cancel): ").strip()
        if qty_input.lower() == 'q':
            print('Slice Order Cancelled')
            return
        elif qty_input.isdigit():
            quantity = int(qty_input)
            if quantity > 16:
                print("Maximum of 16 slices per order. Please try again.")
                continue
            break
        else:
            print("Please enter a valid number.")

    discount_rate = 0.05 if quantity >= 8 else 0.0
    total = calculate_payment(price=slice_price, quantity=quantity, discount_rate=discount_rate)
    print(f"Added to cart: {quantity} x {pizza_name} Slice(s) - ${total:.2f}")
    cart.append({
        'pizza_type': pizza_name,
        'order_type': 'Slice',
        'quantity': quantity,
        'total_price': total,
        'discount_applied': f"{int(discount_rate * 100)}%"
    })

def view_customer_summary():
    if not os.path.exists(ORDERDB_FILE):
        print("No orders found.")
        return
    with open(ORDERDB_FILE, 'r', encoding='utf-8') as file:
        try:
            orders = json.load(file)
        except json.JSONDecodeError:
            print("Error reading order data.")
            return

    print("\n====== CUSTOMER ORDER SUMMARY ======")
    for order in orders:
        print(f"{order['quantity']} x {order['pizza_type']} ({order['order_type']}) - ${order['total_price']:.2f} on {order['order_datetime']}")
    print("====================================")

def view_staff_summary():
    if not os.path.exists(ORDERDB_FILE):
        print("No orders found.")
        return
    with open(ORDERDB_FILE, 'r', encoding='utf-8') as file:
        try:
            orders = json.load(file)
        except json.JSONDecodeError:
            print("Error reading order data.")
            return

    print("\n====== STAFF SALES REPORT ======")
    total_sales = 0
    item_summary = {}
    for order in orders:
        key = (order['pizza_type'], order['order_type'])
        item_summary[key] = item_summary.get(key, 0) + order['quantity']
        total_sales += order['total_price']

    for (pizza, order_type), quantity in item_summary.items():
        print(f"{pizza} ({order_type}): {quantity} units")
    print(f"TOTAL SALES: ${total_sales:.2f}")
    print("==================================")

def pizza_selection_order(pizza_type):
    if pizza_type in pizza_data:
        pizza = pizza_data[pizza_type]
        name = pizza["name"]
        price = pizza['price']
        slice_price = round(price / 8, 2)
        print(f"You selected {name}\nPrice - ${price} per box | ${slice_price} per slice")
        while True:
            choice = input("Select 'B' for Box or 'S' for Slice (or 'q' to cancel): ").strip().upper()
            if choice == 'B':
                handle_box_order(pizza_name=name, price=price)
                break
            elif choice == 'S':
                handle_slice_order(pizza_name=name, slice_price=slice_price)
                break
            elif choice == 'Q':
                print("Order Cancelled!")
                break
            else:
                print("Select either B, S or Q")
    else:
        print("We do not have this Pizza Flavour for now, maybe later")

def main_system():
    while True:
        print("\nWelcome to RushMore Pizzeria\nTake a look at our Menu: ")
        for key, value in pizza_data.items():
            print(f"{key}: {value['name']} - ${value['price']}")
        print("\nType the number (1–9) to add pizza to your cart.")
        print("Type 'v' to view cart, 'e' to edit cart, 'c' to checkout")
        print("Type 'r' to view customer summary, 'm' for staff report")
        print("Type 'q' to quit:")

        choice = input("What do you want to pick? ").strip().lower()

        if choice == 'q':
            print("Goodbye and Have a nice day!\n\tCome back another time...")
            break
        elif choice == 'v':
            view_cart()
        elif choice == 'e':
            edit_cart()
        elif choice == 'c':
            checkout()
        elif choice == 'r':
            view_customer_summary()
        elif choice == 'm':
            view_staff_summary()
        elif choice in pizza_data:
            pizza_selection_order(choice)
        else:
            print("Invalid Input, Please Try Again!")

if __name__ == "__main__":
    main_system()
