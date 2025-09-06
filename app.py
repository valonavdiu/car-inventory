
from flask import Flask, render_template, jsonify, request, abort, Response, url_for
import json, os
from datetime import datetime

app = Flask(__name__)

ROOT = os.path.dirname(__file__)
CARS_PATH = os.path.join(ROOT, "data", "cars.json")
BUSINESS_PATH = os.path.join(ROOT, "data", "business.json")

def load_cars():
    with open(CARS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_business():
    with open(BUSINESS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

BUSINESS = load_business()

@app.context_processor
def inject_business():
    return dict(business=BUSINESS)

@app.route("/")
def home():
    return render_template("home.html", title=f"{BUSINESS['name']} — Rentals & Sales")

@app.route("/inventory")
def inventory():
    tab = request.args.get("tab", "rent")
    return render_template("inventory.html", active_tab=tab, title=f"Inventory — {BUSINESS['name']}")

@app.route("/cars/<car_id>")
def car_detail(car_id):
    car = next((c for c in load_cars() if c.get("id")==car_id), None)
    if not car: abort(404)
    return render_template("car_detail.html", car=car, title=f"{car.get('year','')} {car.get('make','')} {car.get('model','')} — {BUSINESS['name']}")

@app.route("/about")
def about():
    return render_template("about.html", title=f"About — {BUSINESS['name']}")

@app.route("/contact")
def contact():
    return render_template("contact.html", title=f"Contact — {BUSINESS['name']}")

# API
@app.route("/api/cars")
def api_cars():
    cars = load_cars()
    q = request.args.get("q","").lower()
    t = request.args.get("type","").lower()
    def matches(c):
        if t and c.get("type","").lower()!=t: return False
        if not q: return True
        hay = " ".join([str(c.get(k,"")) for k in ["make","model","year","fuel","color","transmission"]]).lower()
        return q in hay
    return jsonify([c for c in cars if matches(c)])

# robots & sitemap
@app.route("/robots.txt")
def robots():
    lines = ["User-agent: *","Allow: /"]
    dom = BUSINESS.get("domain","").strip()
    lines.append("Sitemap: " + (f"https://{dom}/sitemap.xml" if dom else f"{request.url_root.rstrip('/')}/sitemap.xml"))
    return Response("\n".join(lines), mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap():
    cars = load_cars()
    pages = [
        (url_for('home', _external=True), datetime.utcnow()),
        (url_for('inventory', _external=True), datetime.utcnow()),
        (url_for('about', _external=True), datetime.utcnow()),
        (url_for('contact', _external=True), datetime.utcnow()),
    ]
    for c in cars:
        pages.append((url_for('car_detail', car_id=c.get('id'), _external=True), datetime.utcnow()))
    xml = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc,dt in pages:
        xml.append(f"<url><loc>{loc}</loc><lastmod>{dt.strftime('%Y-%m-%d')}</lastmod></url>")
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")

@app.errorhandler(404)
def nf(e):
    return render_template("404.html", title="Not found"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
