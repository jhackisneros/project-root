from io import BytesIO
from urllib.parse import urlparse

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import qrcode
from qrcode.image.pil import PilImage

app = Flask(__name__)
# Allow only the frontend dev origin
CORS(app, origins=["http://localhost:5173"])

def validate_url(raw_url: str):
    if raw_url is None:
        return False, "La URL no puede estar vacía."
    url = raw_url.strip()
    if not url:
        return False, "La URL no puede estar vacía."
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False, "La URL debe comenzar con http:// o https://."
    if not parsed.netloc:
        return False, "La URL debe contener un dominio válido."
    return True, url

@app.route("/qr", methods=["GET"])
def qr():
    raw_url = request.args.get("url", None)
    ok, result = validate_url(raw_url)
    if not ok:
        return jsonify({"error": result}), 400

    url = result
    # Generate QR in memory
    qr_obj = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr_obj.add_data(url)
    qr_obj.make(fit=True)
    img: PilImage = qr_obj.make_image(fill_color="black", back_color="white")

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    # Return PNG (not as attachment) so it can be displayed in <img>
    return send_file(buf, mimetype="image/png")
    
if __name__ == "__main__":
    # For dev: run on port 5000
    app.run(host="127.0.0.1", port=5000, debug=True)
