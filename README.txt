# SmartExpiry Assistant — V2 (Streamlit + Firestore + Emails auto)

## Lancer l'app (local)
```bash
pip install -r requirements.txt
streamlit run app.py
```
Renseigne d'abord `.streamlit/secrets.toml` avec ta **clé de service Firebase** et ta **config SMTP** (SendGrid).

## Déployer le CRON 08:00 (Firebase Functions)
1) Installer et connecter la CLI
```bash
npm i -g firebase-tools
firebase login
```

2) Initialiser les configs d'envoi (dans le dossier `functions/`)
```bash
firebase functions:config:set sendgrid.key="SG.XXXX"
firebase functions:config:set email.from="alerts@smartexpiry.app"
firebase functions:config:set email.to="timotonou@yahoo.com"  # fallback si store.managerEmail absent
```

3) Installer deps et déployer
```bash
cd functions
npm install
firebase deploy --only functions
```

## Firestore attendu
- Lots : `stores/{storeId}/lots/{lotId}` **ou** collection racine `lots` avec champ `storeId`
  - Champs : `productId`, `lotNumber`, `quantity`, `expiryDate` (Timestamp), `location`
- Tâches (créées automatiquement par l'app) : `stores/{storeId}/tasks/{taskId}`
- Logs email : `emailLogs/{DIGEST_storeId_YYYY-MM-DD}`

## Destinataire du digest
- UI Streamlit : masqué mais réel (`[email].to` dans secrets)
- Cron functions : `stores/{storeId}.digestEmail` **ou** `stores/{storeId}.managerEmail` **ou** config globale `email.to`
