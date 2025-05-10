from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "7652319795:AAHy47-PixCTdfm8CW8Dm-kPRJsDmdVmOHE"
CHAT_ID = "1477503070"

@app.route("/new-order", methods=["POST"])
def new_order():
    order = request.json
    products = "\n".join([f"- {item['title']} (Qty: {item['quantity']})" for item in order['line_items']])

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
        json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    )
    return "OK", 200
