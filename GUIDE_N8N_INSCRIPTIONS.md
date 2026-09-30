# Guide n8n — Inscriptions Vovinam Việt Võ Đạo

Ce guide explique comment connecter le formulaire d'inscription du site à n8n afin de recevoir les données et d'envoyer automatiquement des emails de confirmation.

## 1. Fonctionnement général

Le workflow recommandé est le suivant :

```text
Webhook → Edit Fields / Set → Gmail
                         ├── Email au candidat
                         └── Email au responsable du dojo
```

Le site envoie automatiquement les informations de chaque nouvelle inscription à n8n avec une requête HTTP `POST`.

## 2. Adresse de votre espace n8n

Votre espace n8n est accessible ici :

<https://skyhook.app.n8n.cloud/assistant>

Attention : cette adresse est l'interface n8n. Elle ne doit pas être utilisée comme adresse webhook dans Railway.

L'adresse webhook de production aura plutôt cette forme :

```text
https://skyhook.app.n8n.cloud/webhook/nouvelle-inscription
```

## 3. Créer le workflow n8n

1. Ouvrez votre espace n8n.
2. Créez un nouveau workflow.
3. Cliquez sur **Add first step**.
4. Recherchez et ajoutez le nœud **Webhook**.
5. Configurez-le ainsi :

| Paramètre | Valeur |
|---|---|
| HTTP Method | `POST` |
| Path | `nouvelle-inscription` |
| Respond | `Immediately` |

n8n affiche deux adresses :

- **Test URL** : utilisée pendant la configuration et les essais.
- **Production URL** : utilisée par le site lorsque le workflow est actif.

## 4. Tester la réception des données

Pendant la configuration :

1. Ouvrez le nœud **Webhook**.
2. Cliquez sur **Listen for test event**.
3. Copiez temporairement la **Test URL** dans Railway.

La Test URL ressemble à ceci :

```text
https://skyhook.app.n8n.cloud/webhook-test/nouvelle-inscription
```

Après l'envoi d'une inscription depuis le site, n8n devrait recevoir des données similaires à celles-ci :

```json
{
  "nom": "Nom du candidat",
  "email": "candidat@example.com",
  "telephone": "+221 75 229 03 69",
  "age": 25,
  "niveau": "Débutant",
  "message": "Je souhaite rejoindre le dojo"
}
```

Dans n8n, les données reçues par le Webhook sont généralement accessibles ainsi :

```text
$json.body.nom
$json.body.email
$json.body.telephone
$json.body.age
$json.body.niveau
$json.body.message
```

## 5. Configurer le nœud Edit Fields / Set

Ajoutez un nœud **Edit Fields** ou **Set** après le Webhook.

Ajoutez les champs suivants en mode **Expression** :

| Nom du champ | Expression |
|---|---|
| `nom` | `{{ $json.body.nom }}` |
| `email` | `{{ $json.body.email }}` |
| `telephone` | `{{ $json.body.telephone }}` |
| `age` | `{{ $json.body.age }}` |
| `niveau` | `{{ $json.body.niveau }}` |
| `message` | `{{ $json.body.message }}` |

Ce nœud simplifie l'utilisation des informations dans Gmail.

## 6. Connecter Gmail à n8n

1. Ajoutez un nœud **Gmail** après le nœud **Edit Fields / Set**.
2. Choisissez l'opération **Message → Send**.
3. Dans **Credential**, sélectionnez votre compte Google.
4. Si aucun compte n'est proposé, cliquez sur **Create New Credential** et connectez votre compte Google.

### Email de confirmation au candidat

Configurez le destinataire avec l'expression suivante :

```text
{{ $json.email }}
```

Sujet :

```text
Confirmation de votre demande d'inscription au Vovinam Việt Võ Đạo
```

Corps du message :

```text
Bonjour {{ $json.nom }},

Nous avons bien reçu votre demande d'inscription au dojo de Vovinam Việt Võ Đạo.

Voici les informations transmises :

Nom : {{ $json.nom }}
Téléphone : {{ $json.telephone }}
Âge : {{ $json.age }}
Niveau : {{ $json.niveau }}

Notre équipe vous contactera prochainement pour confirmer votre inscription et vous communiquer les prochaines étapes.

Pour toute question, vous pouvez nous joindre au :
+221 75 229 03 69

Cordialement,

Le dojo de Vovinam Việt Võ Đạo
Dakar, Sénégal
```

## 7. Recevoir aussi une notification du dojo

Pour recevoir une notification personnelle à chaque inscription :

1. Ajoutez un deuxième nœud **Gmail** après le nœud **Edit Fields / Set**.
2. Dans **To**, saisissez votre adresse Gmail.
3. Configurez le sujet suivant :

```text
Nouvelle demande d'inscription - {{ $json.nom }}
```

Corps du message :

```text
Une nouvelle demande d'inscription vient d'être reçue.

Nom : {{ $json.nom }}
Email : {{ $json.email }}
Téléphone : {{ $json.telephone }}
Âge : {{ $json.age }}
Niveau : {{ $json.niveau }}
Message : {{ $json.message }}
```

Le workflow complet devient :

```text
                 ┌── Gmail : confirmation au candidat
Webhook → Set ───┤
                 └── Gmail : notification au responsable
```

## 8. Configurer Railway avec l'URL webhook

Pendant les tests, utilisez temporairement la Test URL :

```text
N8N_WEBHOOK_URL=https://skyhook.app.n8n.cloud/webhook-test/nouvelle-inscription
```

Une fois les tests terminés :

1. Activez le workflow avec le bouton **Active**.
2. Copiez l'**URL Production** du nœud Webhook.
3. Dans Railway, ouvrez votre projet.
4. Allez dans **Variables**.
5. Ajoutez ou modifiez la variable suivante :

```text
N8N_WEBHOOK_URL=https://skyhook.app.n8n.cloud/webhook/nouvelle-inscription
```

Important : en production, utilisez `/webhook/` et non `/webhook-test/`.

## 9. Tester avec une inscription réelle

Après avoir activé le workflow :

1. Ouvrez le site du dojo.
2. Remplissez le formulaire d'inscription.
3. Envoyez le formulaire.
4. Vérifiez l'exécution dans n8n.
5. Vérifiez la réception de l'email du candidat.
6. Vérifiez la réception de votre notification.
7. Vérifiez que l'inscription apparaît dans `/admin`.

Vous pouvez également tester le webhook avec cette commande :

```bash
curl -X POST "https://skyhook.app.n8n.cloud/webhook/nouvelle-inscription" \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Test Dojo",
    "email": "votre-adresse-email@example.com",
    "telephone": "+221 75 229 03 69",
    "age": 25,
    "niveau": "Débutant",
    "message": "Test de confirmation"
  }'
```

Remplacez `votre-adresse-email@example.com` par une adresse que vous pouvez consulter.

## 10. Vérifications en cas de problème

### Le webhook affiche une erreur 404

- Vérifiez que le chemin est exactement `nouvelle-inscription`.
- Vérifiez que le workflow est actif pour utiliser l'URL Production.
- Vérifiez que l'URL contient `/webhook/` et non `/assistant`.
- Vérifiez que Railway utilise la bonne variable `N8N_WEBHOOK_URL`.

### Le Webhook reçoit les données mais Gmail n'envoie rien

- Vérifiez que le compte Google est bien connecté dans les credentials n8n.
- Vérifiez le champ destinataire : `{{ $json.email }}`.
- Vérifiez les exécutions n8n et le message d'erreur du nœud Gmail.
- Vérifiez les dossiers Spam et Promotions.

### Le candidat ne reçoit pas le message

- Vérifiez que l'adresse email saisie dans le formulaire est correcte.
- Vérifiez que le champ Gmail utilise bien `{{ $json.email }}`.
- Faites un test avec votre propre adresse email.

## 11. Résumé de la configuration finale

La configuration finale doit respecter les éléments suivants :

```text
Webhook : POST /nouvelle-inscription
       ↓
Edit Fields / Set
       ↓
Gmail → email au candidat
Gmail → notification au responsable
```

Dans Railway :

```text
N8N_WEBHOOK_URL=https://skyhook.app.n8n.cloud/webhook/nouvelle-inscription
```

Le site utilise cette variable pour transmettre les nouvelles inscriptions à n8n. Si la variable n'est pas définie, les inscriptions restent enregistrées dans le site, mais aucun workflow n8n n'est appelé.

## Documentation officielle

- [Documentation n8n Webhook](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook)
- [Documentation n8n Gmail](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail)
- [Espace n8n du dojo](https://skyhook.app.n8n.cloud/assistant)
