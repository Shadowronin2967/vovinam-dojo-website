# 🥋 Vovinam Dojo - Site Web Professionnel

Bienvenue sur le dépôt officiel du site web du dojo de Vovinam Việt Võ Đạo !

## 🚀 Déployer en 5 Minutes

Cliquez sur le bouton ci-dessous pour déployer votre site en un clic :

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/import?repo=https://github.com/Shadowronin2967/vovinam-dojo-website)

Ou consultez le guide ultra-simple : **[DEPLOY_IN_5_MINUTES.md](./DEPLOY_IN_5_MINUTES.md)**

## 📋 Contenu du Projet

### Pages Disponibles
- 🏠 **Accueil** : Présentation du dojo
- 📝 **Inscription** : Formulaire d'inscription
- 💳 **Paiement** : 3 modes de paiement (PayPal, Wave, Orange Money)
- 🔧 **Administration** : Gestion des inscriptions

### Fonctionnalités
- ✅ Formulaire d'inscription complet
- ✅ Système de paiement multi-modes
- ✅ Tableau de bord d'administration
- ✅ Emails de confirmation automatiques
- ✅ Base de données PostgreSQL persistante
- ✅ Webhook n8n pour automatisation
- ✅ Intégration PayPal

## 🛠️ Stack Technique

| Composant | Technologie |
|-----------|-------------|
| Frontend | HTML5, Tailwind CSS, JavaScript |
| Backend | Flask (Python 3.11) |
| Base de Données | PostgreSQL |
| Hébergement | Railway |
| Versioning | GitHub |

## 📦 Structure du Projet

```
vovinam-dojo-website/
├── src/
│   ├── static/           # Fichiers HTML/CSS/JS
│   │   ├── index.html    # Page d'accueil
│   │   ├── payment.html  # Page de paiement
│   │   └── admin.html    # Tableau de bord
│   ├── models/           # Modèles de base de données
│   ├── routes/           # Routes API
│   └── main.py           # Application Flask
├── Procfile              # Configuration Railway
├── requirements.txt      # Dépendances Python
└── DEPLOY_IN_5_MINUTES.md # Guide de déploiement
```

## 🔐 Variables d'Environnement

```
SECRET_KEY=votre_clé_secrète
FLASK_ENV=production
DATABASE_URL=postgresql://...
```

## 📞 Informations de Contact

- **Téléphone** : +221 75 229 03 69
- **Email** : contact@vovinam-dojo.com
- **Localisation** : Dakar, Sénégal

## 🎯 Modes de Paiement

1. **PayPal** - Paiement international sécurisé
2. **Wave** - Paiement mobile Sénégal
3. **Orange Money** - Paiement mobile Orange

## 📚 Documentation

- [DEPLOY_IN_5_MINUTES.md](./DEPLOY_IN_5_MINUTES.md) - Guide de déploiement rapide
- [RAILWAY_DEPLOYMENT_GUIDE.md](./RAILWAY_DEPLOYMENT_GUIDE.md) - Guide détaillé Railway
- [ADMIN_GUIDE.md](./ADMIN_GUIDE.md) - Guide d'administration
- [FINAL_SUMMARY.md](./FINAL_SUMMARY.md) - Résumé complet du projet

## 🚀 Démarrage Rapide

### Développement Local

```bash
# Cloner le dépôt
git clone https://github.com/Shadowronin2967/vovinam-dojo-website.git
cd vovinam-dojo-website

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python src/main.py
```

L'application sera accessible à `http://localhost:5000`

### Déploiement Production

Consultez [DEPLOY_IN_5_MINUTES.md](./DEPLOY_IN_5_MINUTES.md) pour un guide étape par étape.

## 🔄 Mises à Jour

Pour mettre à jour le site en production :

```bash
git add .
git commit -m "Description de vos changements"
git push origin master
```

Railway redéploiera automatiquement votre site !

## 📊 Tableau de Bord d'Administration

Accédez à `/admin` pour :
- 📋 Voir toutes les inscriptions
- 💳 Suivre les paiements
- ✏️ Changer les statuts
- 📊 Voir les statistiques

## ⚙️ Configuration

### Fichiers Importants

- `src/main.py` - Application Flask principale
- `src/models/inscription.py` - Modèle de données
- `src/routes/` - Routes API
- `src/static/` - Fichiers frontend

### Variables d'Environnement

Voir `.env.example` pour la liste complète des variables.

## 🐛 Troubleshooting

### Le site affiche une erreur 500
- Vérifiez les logs Railway
- Assurez-vous que `DATABASE_URL` est configurée

### La base de données ne se connecte pas
- Vérifiez que PostgreSQL est bien ajouté
- Vérifiez que `DATABASE_URL` est correctement définie

### Les fichiers statiques ne se chargent pas
- Vérifiez que le dossier `src/static/` existe
- Vérifiez que les fichiers HTML sont présents

## 📈 Prochaines Étapes

- [ ] Déployer sur Railway
- [ ] Configurer un domaine personnalisé
- [ ] Activer les emails Gmail
- [ ] Configurer PayPal
- [ ] Ajouter des témoignages
- [ ] Partager sur les réseaux sociaux

## 🤝 Contribution

Pour contribuer au projet :
1. Fork le dépôt
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Commitez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT.

## 🎉 Remerciements

Créé avec ❤️ par Manus AI pour le dojo de Vovinam Việt Võ Đạo.

---

**Besoin d'aide ?** Consultez la documentation ou les guides fournis.

**Bonne chance avec votre dojo ! 🥋**
