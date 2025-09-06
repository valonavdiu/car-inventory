
from flask import Flask, render_template, jsonify, request, abort
import json
import os

app = Flask(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "cars.json")

def load_cars():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/inventory")
def inventory():
    # optional type filter via query (?type=rent/sale)
    car_type = request.args.get("type")
    return render_template("inventory.html", car_type=car_type)

@app.route("/cars/<car_id>")
def car_detail(car_id):
    cars = load_cars()
    car = next((c for c in cars if c.get("id") == car_id), None)
    if not car:
        abort(404)
    return render_template("car_detail.html", car=car)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# Simple JSON API with filters: ?q=... & type=rent|sale
@app.route("/api/cars")
def api_cars():
    cars = load_cars()
    q = request.args.get("q", "").strip().lower()
    type_filter = request.args.get("type", "").strip().lower()

    def matches(car):
        if type_filter and car.get("type","").lower() != type_filter:
            return False
        if not q:
            return True
        hay = " ".join([
            str(car.get("make","")),
            str(car.get("model","")),
            str(car.get("year","")),
            str(car.get("fuel","")),
            str(car.get("color","")),
            str(car.get("transmission","")),
        ]).lower()
        return q in hay

    filtered = [c for c in cars if matches(c)]
    return jsonify(filtered)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
