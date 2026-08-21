import os
import sys

# Permettre l'import du package src lorsque Gunicorn démarre depuis la racine.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS

from src.models.user import db
from src.routes.gmail import gmail_bp
from src.routes.inscription import inscription_bp
from src.routes.mobile_money import mobile_money_bp
from src.routes.n8n_webhook import n8n_webhook_bp
from src.routes.paypal import paypal_bp
from src.routes.user import user_bp


BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
LOCAL_DATABASE = os.path.join(BASE_DIR, "database", "app.db")

app = Flask(__name__, static_folder=STATIC_DIR)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-change-this-secret")

# Railway peut fournir une URL commençant par postgres://.
database_url = os.getenv("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url or f"sqlite:///{LOCAL_DATABASE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
db.init_app(app)

app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(inscription_bp)
app.register_blueprint(paypal_bp)
app.register_blueprint(gmail_bp)
app.register_blueprint(n8n_webhook_bp)
app.register_blueprint(mobile_money_bp)

with app.app_context():
    os.makedirs(os.path.dirname(LOCAL_DATABASE), exist_ok=True)
    db.create_all()


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path == "admin":
        return send_from_directory(STATIC_DIR, "admin.html")
    if path and os.path.isfile(os.path.join(STATIC_DIR, path)):
        return send_from_directory(STATIC_DIR, path)
    return send_from_directory(STATIC_DIR, "index.html")


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
