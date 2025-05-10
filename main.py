@app.route("/new-order", methods=["POST"])
def new_order():
    order = request.json
    line_items = order.get("line_items", [])
    
    # Remove garbage titles like 'pics'
    products = "\n".join([
        f"- {item['title']} (Qty: {item['quantity']})"
        for item in line_items
        if item.get('title') and item['title'].lower() != 'pics'
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
