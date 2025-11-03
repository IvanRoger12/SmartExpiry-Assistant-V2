"""
ENVOI AUTOMATIQUE DU RAPPORT QUOTIDIEN
À exécuter via GitHub Actions chaque matin à 8h
"""

import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, date
from dateutil import tz
import os
import json
import base64

# ═════════════════════════════════════════════════════════════════
# CONFIG
# ═════════════════════════════════════════════════════════════════

PARIS = tz.gettz("Europe/Paris")
STORE_ID = "naturalia_nanterre"

# Récupérer les secrets depuis les variables d'environnement
FIREBASE_CONFIG = json.loads(base64.b64decode(os.getenv("FIREBASE_CONFIG")))
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM = os.getenv("SENDGRID_FROM", "nfindaroger@gmail.com")
SENDGRID_TO = os.getenv("SENDGRID_TO", "timotonou@yahoo.com")

# ═════════════════════════════════════════════════════════════════
# HELPERS
# ═════════════════════════════════════════════════════════════════

def days_until(exp_date) -> int:
    try:
        expiry = pd.to_datetime(exp_date).date()
        return (expiry - date.today()).days
    except:
        return 999

def stage_from_days(days: int) -> str:
    if days <= 3: return "J-3"
    elif days <= 7: return "J-7"
    elif days <= 21: return "J-21"
    else: return "OK"

def stage_config(stage: str) -> dict:
    config = {
        "J-21": {"label": "À 3 semaines", "emoji": "📅", "color": "#3b82f6"},
        "J-7": {"label": "À 1 semaine", "emoji": "⏰", "color": "#f59e0b"},
        "J-3": {"label": "À 3 jours", "emoji": "🔴", "color": "#dc2626"},
        "OK": {"label": "> 3 semaines", "emoji": "✅", "color": "#10b981"}
    }
    return config.get(stage, config["OK"])

# ═════════════════════════════════════════════════════════════════
# FIREBASE
# ═════════════════════════════════════════════════════════════════

def init_firebase():
    """Initialise la connexion Firebase"""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CONFIG)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"❌ Erreur Firebase: {str(e)}")
        raise

# ═════════════════════════════════════════════════════════════════
# CHARGER LES DONNÉES
# ═════════════════════════════════════════════════════════════════

def load_lots(db, store_id: str) -> pd.DataFrame:
    """Charge les lots depuis Firebase"""
    lots = []
    try:
        for doc in db.collection("lots").stream():
            d = doc.to_dict()
            d["id"] = doc.id
            
            # Mapper les vrais champs
            d["expiryDate"] = d.get("dlc")
            d["productId"] = d.get("product_ean")
            d["lotNumber"] = d.get("lot_code")
            d["quantity"] = d.get("qty_current", 0)
            d["location"] = d.get("location", "")
            
            # Filtrer par magasin
            if d.get("store_id") == store_id:
                lots.append(d)
    except Exception as e:
        print(f"❌ Erreur chargement lots: {str(e)}")
        return pd.DataFrame()
    
    if not lots:
        return pd.DataFrame()
    
    df = pd.DataFrame(lots)
    df["expiryDate"] = pd.to_datetime(df["expiryDate"], errors='coerce')
    df = df.dropna(subset=["expiryDate"])
    df["daysLeft"] = df["expiryDate"].apply(days_until)
    df["stage"] = df["daysLeft"].apply(stage_from_days)
    df = df.sort_values("expiryDate")
    return df

# ═════════════════════════════════════════════════════════════════
# GÉNÉRER LE HTML DE L'EMAIL
# ═════════════════════════════════════════════════════════════════

def generate_email_html(store_id: str, lots_df: pd.DataFrame) -> str:
    """Génère le HTML du digest email"""
    
    # Compter par étape
    urgent_count = len(lots_df[(lots_df["stage"] == "J-3")])
    warning_count = len(lots_df[(lots_df["stage"] == "J-7")])
    planning_count = len(lots_df[(lots_df["stage"] == "J-21")])
    
    rows = []
    
    # Tableau par étape
    for stage in ["J-3", "J-7", "J-21"]:
        sub = lots_df[lots_df["stage"] == stage].sort_values("expiryDate")
        if sub.empty:
            continue
        
        cfg = stage_config(stage)
        rows.append(f"<h3 style='margin: 24px 0 12px; color: #1f2937; font-size: 18px; font-weight: 800;'>{cfg['emoji']} {cfg['label']}</h3>")
        rows.append("""<table style='width:100%;border-collapse:collapse;border:1px solid #d1d5db; margin-bottom: 20px;'><tr style='background:#f3f4f6;'><th style='padding:14px;text-align:left;border:1px solid #d1d5db;font-weight:700;'>PRODUIT</th><th style='padding:14px;text-align:left;border:1px solid #d1d5db;font-weight:700;'>LOT</th><th style='padding:14px;text-align:center;border:1px solid #d1d5db;font-weight:700;'>QTÉ</th><th style='padding:14px;text-align:center;border:1px solid #d1d5db;font-weight:700;'>DLC</th><th style='padding:14px;text-align:center;border:1px solid #d1d5db;font-weight:700;'>JOURS</th><th style='padding:14px;text-align:left;border:1px solid #d1d5db;font-weight:700;'>RAYON</th></tr>""")
        
        for _, r in sub.iterrows():
            exp_date = pd.to_datetime(r['expiryDate']).date().strftime('%d/%m/%Y')
            days_left = int(r.get('daysLeft', 0))
            qty = int(r.get('quantity', 0))
            color = "#dc2626" if days_left <= 3 else "#f59e0b"
            
            rows.append(f"""<tr style='border-bottom:1px solid #e5e7eb;'><td style='padding:12px;border:1px solid #d1d5db;'>{r.get('productId', 'N/A')}</td><td style='padding:12px;border:1px solid #d1d5db;font-weight:700;color:#3b82f6;'>{r.get('lotNumber', '')}</td><td style='padding:12px;border:1px solid #d1d5db;text-align:center;font-weight:700;'>{qty}</td><td style='padding:12px;border:1px solid #d1d5db;text-align:center;'>{exp_date}</td><td style='padding:12px;border:1px solid #d1d5db;text-align:center;color:{color};font-weight:900;font-size:15px;'>{days_left}j</td><td style='padding:12px;border:1px solid #d1d5db;'>{r.get('location', '')}</td></tr>""")
        
        rows.append("</table>")
    
    body = "".join(rows) if rows else "<p style='text-align:center;color:#6b7280;padding:2rem;'>✅ Aucun produit n'expire bientôt</p>"
    
    html = f"""<!doctype html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:'Inter', Arial, sans-serif;background:#f8fafc;margin:0;padding:20px;color:#0f172a;">
<div style="max-width:850px;margin:0 auto;background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.15);">

<div style="background:linear-gradient(135deg,#3b82f6 0%,#2563eb 100%);padding:40px;color:#fff;text-align:center;">
<h1 style="margin:0;font-size:32px;font-weight:900;">🧊 SmartExpiry</h1>
<h2 style="margin:12px 0 0;font-size:20px;font-weight:700;">Rapport Quotidien</h2>
<div style="opacity:.9;margin-top:14px;font-size:14px;">
  Magasin: <strong>{store_id}</strong> • {datetime.now(PARIS).strftime('%d %B %Y à %H:%M')}
</div>
</div>

<div style="padding:40px;">
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:30px;">
  <div style="background:#fef2f2;border-left:4px solid #dc2626;padding:15px;border-radius:8px;">
    <div style="font-size:28px;font-weight:900;color:#dc2626;">{urgent_count}</div>
    <div style="font-size:12px;color:#6b7280;margin-top:5px;">🔴 J-3 URGENT</div>
  </div>
  <div style="background:#fffbeb;border-left:4px solid #f59e0b;padding:15px;border-radius:8px;">
    <div style="font-size:28px;font-weight:900;color:#f59e0b;">{warning_count}</div>
    <div style="font-size:12px;color:#6b7280;margin-top:5px;">⏰ J-7 ALERTE</div>
  </div>
  <div style="background:#dbeafe;border-left:4px solid #3b82f6;padding:15px;border-radius:8px;">
    <div style="font-size:28px;font-weight:900;color:#3b82f6;">{planning_count}</div>
    <div style="font-size:12px;color:#6b7280;margin-top:5px;">📅 J-21 PLANIFIER</div>
  </div>
</div>

{body}

<div style="text-align:center;margin-top:32px;">
  <a href="https://share.streamlit.io/ivanroger12/smartexpiry-assistant-v2" style="display:inline-block;background:#3b82f6;color:#fff;padding:16px 40px;border-radius:12px;text-decoration:none;font-weight:800;text-transform:uppercase;letter-spacing:0.5px;">
    👉 Ouvrir l'application
  </a>
</div>
</div>

<div style="background:#f1f5f9;padding:24px;text-align:center;color:#64748b;font-size:12px;border-top:1px solid #e2e8f0;">
<strong>SmartExpiry Pro</strong> • Gestion FEFO Intelligente<br/>
Zéro perte • Marges optimisées • Efficacité maximale<br/>
{datetime.now(PARIS).strftime('%d/%m/%Y à %H:%M:%S')}
</div>

</div>
</body>
</html>"""
    
    return html

# ═════════════════════════════════════════════════════════════════
# ENVOYER L'EMAIL
# ═════════════════════════════════════════════════════════════════

def send_email(subject: str, html: str) -> bool:
    """Envoie l'email via SendGrid SMTP"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SENDGRID_FROM
        msg["To"] = SENDGRID_TO
        
        msg.attach(MIMEText(html, "html"))
        
        with smtplib.SMTP("smtp.sendgrid.net", 587) as server:
            server.starttls()
            server.login("apikey", SENDGRID_API_KEY)
            server.sendmail(SENDGRID_FROM, [SENDGRID_TO], msg.as_string())
        
        print(f"✅ Email envoyé à {SENDGRID_TO}")
        return True
    except Exception as e:
        print(f"❌ Erreur envoi email: {str(e)}")
        return False

# ═════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print(f"🚀 RAPPORT QUOTIDIEN SmartExpiry")
    print(f"📅 {datetime.now(PARIS).strftime('%d/%m/%Y à %H:%M:%S')}")
    print("="*60 + "\n")
    
    try:
        # 1. Initialiser Firebase
        print("1️⃣ Connexion à Firebase...")
        db = init_firebase()
        print("   ✅ Connecté")
        
        # 2. Charger les données
        print("2️⃣ Chargement des lots...")
        lots_df = load_lots(db, STORE_ID)
        print(f"   ✅ {len(lots_df)} lots chargés")
        
        if lots_df.empty:
            print("   ⚠️ Aucun lot trouvé")
            return
        
        # 3. Générer l'email
        print("3️⃣ Génération du rapport...")
        html = generate_email_html(STORE_ID, lots_df)
        print("   ✅ Rapport généré")
        
        # 4. Envoyer l'email
        print("4️⃣ Envoi de l'email...")
        subject = f"🧊 SmartExpiry - Rapport quotidien {datetime.now(PARIS).strftime('%d/%m/%Y')}"
        if send_email(subject, html):
            print("   ✅ Email envoyé")
        else:
            print("   ❌ Erreur lors de l'envoi")
        
        print("\n" + "="*60)
        print("✅ RAPPORT QUOTIDIEN TERMINÉ")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}\n")
        raise

if __name__ == "__main__":
    main()
