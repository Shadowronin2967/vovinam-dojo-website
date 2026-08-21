from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.inscription import Inscription
import re
import os
import requests

inscription_bp = Blueprint('inscription', __name__)

def validate_email(email):
    """Valide le format de l'email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Valide le format du téléphone (format international ou local)"""
    # Supprime les espaces et caractères spéciaux
    clean_phone = re.sub(r'[^\d+]', '', phone)
    # Vérifie si c'est un numéro valide (au moins 8 chiffres)
    return len(clean_phone) >= 8

@inscription_bp.route('/api/inscription', methods=['POST'])
def create_inscription():
    try:
        data = request.get_json()
        
        # Validation des champs obligatoires
        required_fields = ['nom', 'email', 'telephone']
        for field in required_fields:
            if not data.get(field) or not data.get(field).strip():
                return jsonify({'error': f'Le champ {field} est obligatoire'}), 400
        
        # Validation de l'email
        if not validate_email(data['email']):
            return jsonify({'error': 'Format d\'email invalide'}), 400
        
        # Validation du téléphone
        if not validate_phone(data['telephone']):
            return jsonify({'error': 'Format de téléphone invalide'}), 400
        
        # Validation de l'âge si fourni
        if data.get('age'):
            try:
                age = int(data['age'])
                if age < 5 or age > 99:
                    return jsonify({'error': 'L\'âge doit être entre 5 et 99 ans'}), 400
            except ValueError:
                return jsonify({'error': 'L\'âge doit être un nombre'}), 400
        
        # Vérification si l'email existe déjà
        existing_inscription = Inscription.query.filter_by(email=data['email']).first()
        if existing_inscription:
            return jsonify({'error': 'Une inscription avec cet email existe déjà'}), 409
        
        # Création de la nouvelle inscription
        nouvelle_inscription = Inscription(
            nom=data['nom'].strip(),
            email=data['email'].strip().lower(),
            telephone=data['telephone'].strip(),
            age=int(data['age']) if data.get('age') else None,
            niveau=data.get('niveau', '').strip() if data.get('niveau') else None,
            message=data.get('message', '').strip() if data.get('message') else None
        )
        
        db.session.add(nouvelle_inscription)
        db.session.commit()

        # Envoi vers n8n pour automatisation
        n8n_url = os.getenv("N8N_WEBHOOK_URL", "https://fallou1997.app.n8n.cloud/webhook/nouvelle-inscription")
        if n8n_url:
            try:
                requests.post(n8n_url, json=nouvelle_inscription.to_dict(), timeout=5)
            except Exception as e:
                print(f"Erreur envoi n8n: {e}")
        
        return jsonify({
            'message': 'Inscription créée avec succès',
            'inscription': nouvelle_inscription.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur interne du serveur'}), 500

@inscription_bp.route('/api/inscriptions', methods=['GET'])
def get_inscriptions():
    """Récupère toutes les inscriptions (pour l'administration)"""
    try:
        inscriptions = Inscription.query.order_by(Inscription.date_inscription.desc()).all()
        return jsonify([inscription.to_dict() for inscription in inscriptions]), 200
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la récupération des inscriptions'}), 500

@inscription_bp.route('/api/inscription/<int:inscription_id>', methods=['GET'])
def get_inscription(inscription_id):
    """Récupère une inscription spécifique"""
    try:
        inscription = Inscription.query.get_or_404(inscription_id)
        return jsonify(inscription.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Inscription non trouvée'}), 404

@inscription_bp.route('/api/inscription/<int:inscription_id>/statut', methods=['PUT'])
def update_statut(inscription_id):
    """Met à jour le statut d'une inscription"""
    try:
        data = request.get_json()
        statut = data.get('statut')
        
        if statut not in ['en_attente', 'contacte', 'accepte', 'refuse']:
            return jsonify({'error': 'Statut invalide'}), 400
        
        inscription = Inscription.query.get_or_404(inscription_id)
        inscription.statut = statut
        db.session.commit()
        
        return jsonify({
            'message': 'Statut mis à jour avec succès',
            'inscription': inscription.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la mise à jour'}), 500

