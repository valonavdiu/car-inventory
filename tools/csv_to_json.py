
import csv, json, argparse

def main(csv_path, out_path):
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            # split images by ;
            imgs = [u.strip() for u in (r.get("images","").split(";") if r.get("images") else []) if u.strip()]
            row = {
                "id": r.get("id","").strip(),
                "type": r.get("type","").strip(),
                "make": r.get("make","").strip(),
                "model": r.get("model","").strip(),
                "year": int(r["year"]) if r.get("year") else None,
                "fuel": r.get("fuel","").strip(),
                "transmission": r.get("transmission","").strip(),
                "seats": int(r["seats"]) if r.get("seats") else None,
                "color": r.get("color","").strip(),
                "odometer": int(r["odometer"]) if r.get("odometer") else None,
                "price_per_day": int(r["price_per_day"]) if r.get("price_per_day") else None,
                "price": int(r["price"]) if r.get("price") else None,
                "images": imgs,
                "contact": {
                    "name": r.get("contact_name","").strip(),
                    "phone": r.get("contact_phone","").strip(),
                    "email": r.get("contact_email","").strip()
                }
            }
            rows.append(row)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
    print(f"Wrote {len(rows)} cars to {out_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", default="data/cars.json")
    args = ap.parse_args()
    main(args.csv, args.out)
