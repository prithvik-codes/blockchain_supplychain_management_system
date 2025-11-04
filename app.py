import os
import io
import csv
import time
import socket
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from blockchain import FoodTraceChain
import qrcode

app = Flask(__name__)
app.secret_key = "dev-secret"
chain = FoodTraceChain()

# --- Detect Local IP for QR generation ---
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # connect to Google DNS to get outbound IP
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

LOCAL_IP = get_local_ip()
SERVER_PORT = 5000

QR_DIR = os.path.join("static", "qr_codes")
os.makedirs(QR_DIR, exist_ok=True)


@app.template_filter("fmt_time")
def fmt_time(ts):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


@app.route("/")
def home():
    products = sorted({b.product_id for b in chain.all_blocks() if b.product_id != "GENESIS"})
    return render_template("index.html", products=products)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        product_id = request.form.get("product_id", "").strip()
        location = request.form.get("location", "").strip()
        action = request.form.get("action", "").strip()
        if not product_id or not location or not action:
            flash("All fields are required.", "danger")
            return redirect(url_for("add"))
        chain.add_record(product_id, location, action)

        # --- Generate QR with LAN IP (works on mobile) ---
        track_url = f"http://{LOCAL_IP}:{SERVER_PORT}" + url_for("track", product_id=product_id)
        img = qrcode.make(track_url)
        img_path = os.path.join(QR_DIR, f"{product_id}.png")
        img.save(img_path)
        print("✅ QR saved at:", img_path, "->", track_url)

        flash("Record added and QR generated.", "success")
        return redirect(url_for("track", product_id=product_id))
    return render_template("add_product.html")


@app.route("/track")
def track():
    product_id = request.args.get("product_id", "").strip()
    products = sorted({b.product_id for b in chain.all_blocks() if b.product_id != "GENESIS"})
    history = chain.track(product_id) if product_id else []
    qr_path = os.path.join(QR_DIR, f"{product_id}.png")
    qr_exists = os.path.exists(qr_path)
    return render_template("track.html", product_id=product_id, history=history, products=products, qr_exists=qr_exists)


@app.route("/all")
def view_all():
    return render_template("view_blockchain.html", blocks=chain.all_blocks())


@app.route("/validate")
def validate():
    return render_template("view_blockchain.html", blocks=chain.all_blocks(), valid=chain.is_valid())


@app.route("/export")
def export_csv():
    rows = chain.export_csv_rows()
    output = io.StringIO()
    csv.writer(output).writerows(rows)
    mem = io.BytesIO(output.getvalue().encode("utf-8"))
    mem.seek(0)
    return send_file(mem, mimetype="text/csv", as_attachment=True, download_name="blockchain.csv")


@app.route("/tamper", methods=["POST"])
def tamper():
    idx = int(request.form.get("index", "0"))
    if chain.tamper(idx):
        flash(f"Block {idx} tampered.", "warning")
    else:
        flash("Invalid block index.", "danger")
    return redirect(url_for("view_all"))


@app.route("/qr/<product_id>")
def serve_qr(product_id):
    img_path = os.path.join(QR_DIR, f"{product_id}.png")
    if os.path.exists(img_path):
        return send_file(img_path, mimetype="image/png")
    return "QR not found", 404


# preload demo data if only genesis exists
if len(chain.all_blocks()) <= 1:
    chain.add_record("AppleBatch001", "Farm A", "Harvested")
    chain.add_record("AppleBatch001", "Truck X", "Shipped")
    chain.add_record("AppleBatch001", "Warehouse B", "Stored")
    chain.add_record("AppleBatch001", "Store C", "Sold")
    chain.add_record("MilkBatchX", "Dairy D", "Processed")
    chain.add_record("MilkBatchX", "Truck Y", "Delivered")

if __name__ == "__main__":
    print(f"🌍 Server running at: http://{LOCAL_IP}:{SERVER_PORT}")
    print("📱 Scan QR codes with your phone (same Wi-Fi)")
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)
