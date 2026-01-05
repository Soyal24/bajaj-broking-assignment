from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

instruments = [
    {"symbol": "AAPL", "exchange": "NASDAQ", "instrumentType": "EQUITY", "lastTradedPrice": 180},
    {"symbol": "GOOGL", "exchange": "NASDAQ", "instrumentType": "EQUITY", "lastTradedPrice": 140}
]

orders = {}
trades = []
portfolio = {}

@app.route("/api/v1/instruments", methods=["GET"])
def get_instruments():
    return jsonify(instruments), 200

@app.route("/api/v1/orders", methods=["POST"])
def place_order():
    data = request.json

    if data["quantity"] <= 0:
        return jsonify({"error": "Quantity must be > 0"}), 400

    order_id = str(uuid.uuid4())
    order = {
        "orderId": order_id,
        "symbol": data["symbol"],
        "side": data["side"],
        "orderType": data["orderType"],
        "quantity": data["quantity"],
        "status": "EXECUTED"
    }

    orders[order_id] = order

    trades.append({
        "orderId": order_id,
        "symbol": data["symbol"],
        "quantity": data["quantity"],
        "price": 180
    })

    portfolio[data["symbol"]] = {
        "symbol": data["symbol"],
        "quantity": data["quantity"],
        "averagePrice": 180,
        "currentValue": data["quantity"] * 180
    }

    return jsonify(order), 201

@app.route("/api/v1/orders/<order_id>", methods=["GET"])
def order_status(order_id):
    if order_id not in orders:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(orders[order_id]), 200

@app.route("/api/v1/trades", methods=["GET"])
def get_trades():
    return jsonify(trades), 200

@app.route("/api/v1/portfolio", methods=["GET"])
def get_portfolio():
    return jsonify(list(portfolio.values())), 200

if __name__ == "__main__":
    app.run(debug=True)





