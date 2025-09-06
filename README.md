
# AutoHub — Car Rentals & Sales (Flask)

A simple, phone-friendly website for your car rental and dealership.
- Browse inventory (filters + search)
- Car detail pages with WhatsApp/Call buttons
- JSON data file for easy updates
- Free hosting on Render (with GitHub)

## Quick Start (local)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
python app.py
# open http://localhost:5000
```

## Deploy on Render
1. Push these files to a **public GitHub** repo (e.g., `car-inventory`).
2. On https://render.com: **New → Web Service** → connect the repo.
3. Environment: Python
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Plan: Free
4. Render gives you a public link like `https://car-inventory.onrender.com`.

## Update cars
Edit `data/cars.json` (or use the CSV tool):
- Rentals use `"type": "rent"` and `price_per_day`.
- Sales use `"type": "sale"` and `price`.
- Add multiple images in `"images": [ ... ]`.
- Set your phone/email in `"contact"`.

CSV route (optional):
```bash
python tools/csv_to_json.py --csv tools/cars_template.csv --out data/cars.json
```

## Custom domain (optional)
In Render service → Settings → **Custom Domains**, add your domain and follow DNS steps.
