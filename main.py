from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7652319795:AAHy47-PixCTdfm8CW8Dm-kPRJsDmdVmOHE"
CHAT_ID = "1477503070"

@app.route("/new-order", methods=["POST"])
def new_order():
    order = request.json
    line_items = order.get("line_items", [])
    
    # Filter out invalid or spam items like 'pics'
    products = "\n".join([
        f"- {item['title']} (Qty: {item['quantity']})"
        for item in line_items
        if item.get('title') and item['title'].strip().lower() != 'pics'
    ])

    message = f"""
🔔 *New Shopify Order!*
*Name:* {order['billing_address']['first_name']} {order['billing_address']['last_name']}
*Email:* {order['email']}
*Total:* ${order['total_price']}
*Product(s):*
{products}
    """

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": message.strip(), "parse_mode": "Markdown"}
    )
    return "OK", 200
@app.route("/abandoned-cart", methods=["POST"])
def abandoned_cart():
    cart = request.json
    customer_email = cart.get("email", "Unknown")
    created_at = cart.get("created_at", "")
    line_items = cart.get("line_items", [])

    products = "\n".join([
        f"- {item['title']} (Qty: {item['quantity']})"
        for item in line_items
    ])

    message = f"""
⚠️ *Abandoned Cart Alert!*
*Email:* {customer_email}
*Created At:* {created_at}
*Product(s):*
{products}
    """

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": message.strip(), "parse_mode": "Markdown"}
    )

    return "OK", 200
