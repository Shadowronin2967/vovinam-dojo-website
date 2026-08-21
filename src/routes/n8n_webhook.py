from flask import Blueprint, request, jsonify

n8n_webhook_bp = Blueprint("n8n_webhook", __name__)

@n8n_webhook_bp.route("/webhook/new_inscription", methods=["POST"])
def new_inscription_webhook():
    try:
        data = request.get_json()
        # Ici, vous pouvez traiter les données reçues de n8n
        # Par exemple, les logger, les envoyer à un autre service, etc.
        print(f"Webhook n8n reçu pour une nouvelle inscription: {data}")
        # Vous pouvez ajouter ici la logique pour envoyer ces données à d'autres services
        # ou les stocker d'une manière spécifique pour n8n.
        return jsonify({"status": "success", "message": "Webhook received"}), 200
    except Exception as e:
        print(f"Erreur lors de la réception du webhook n8n: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
