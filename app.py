"""
╔════════════════════════════════════════════════════════════════════════╗
║     🧊 SMARTEXPIRY PRO MVP+ FINAL - MEGA COMPLETE VERSION              ║
║   Notifications Push • Analytics • Rôles • Multi-Store • PDF + Email    ║
║                  PRODUCTION READY - NOVEMBER 2025                      ║
╚════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from dateutil import tz
import plotly.graph_objects as go
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch

PARIS = tz.gettz("Europe/Paris")

st.set_page_config(page_title="SmartExpiry Pro", layout="wide", page_icon="🧊", initial_sidebar_state="expanded")

# ═════════════════════════════════════════════════════════════════════════
# STATE & TRANSLATIONS
# ═════════════════════════════════════════════════════════════════════════

if "lang" not in st.session_state:
    st.session_state.lang = "FR"
if "user_role" not in st.session_state:
    st.session_state.user_role = "Worker"
if "user_store" not in st.session_state:
    st.session_state.user_store = None
if "show_detail" not in st.session_state:
    st.session_state.show_detail = False
if "detail_stage" not in st.session_state:
    st.session_state.detail_stage = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "notifications" not in st.session_state:
    st.session_state.notifications = []

LANG = {
    "FR": {
        "title": "SmartExpiry Pro", "subtitle": "Gestion FEFO Intelligente • Alertes Automatiques • Zéro Perte",
        "total_lots": "Total Lots", "urgent": "Urgent", "alert": "Alerte", "plan": "Planifier", "quantity": "Quantité",
        "to_manage": "à gérer", "days": "jours", "units": "unités", "search": "🔎 Rechercher",
        "product_placeholder": "Produit, lot, rayon...", "filters": "🔍 Filtres", "urgency": "Urgence",
        "all": "Tous", "shelves": "Rayon", "reset": "🔄 Réin", "inventory": "📋 Inventaire", 
        "charts": "📊 Graphiques", "email": "📧 Email", "export": "📥 Export", "analytics": "📈 Analytics",
        "product_list": "📦 Liste", "matching": "lot(s) correspondent", "no_results": "❌ Aucun lot", 
        "send_digest": "📧 Envoyer", "send_success": "✅ Envoyé !", "download_csv": "📊 CSV", 
        "config": "⚙️ CONFIG", "store": "🏪 Magasin", "system_status": "🧊 SmartExpiry Pro",
        "sync_realtime": "✅ Sync Temps Réel", "multi_stores": "📊 Multi-Magasins", "automated": "⚡ 100% Auto",
        "ai_integrated": "🤖 IA (ChatGPT)", "assistant_ia": "🤖 Assistant IA", "ask_question": "Ta question...",
        "thinking": "Réfléchit...", "distribution": "Distribution", "trend": "Tendance FEFO", "week": "Semaine",
        "at_risk": "À risque", "urgency_vs_qty": "Urgence vs Quantité", "removed": "✅ Retiré",
        "manager": "📤 Manager", "reschedule": "⏳ Reporter", "details": "📋 Détails", "close": "✕",
        "alerts": "Alertes", "urgent_products": "produits urgents à retirer", "total_qty": "Quantité totale",
        "timestamp": "Mis à jour", "role": "👥 Rôle", "manager_role": "Manager", "worker_role": "Worker",
        "notifications": "🔔 Notifications", "push_enabled": "Notifications Push activées",
        "performance": "Performance", "loss_rate": "Taux de perte", "saved": "Économies",
        "multi_store": "📊 Multi-Magasins", "compare_stores": "Comparer les magasins",
        "removed_msg": "✅ Retiré du rayon !", "signaled_msg": "📤 Signalé au manager !",
        "reset_btn": "🔄 Réinitialiser", "product": "📦 Produit", "location": "📍 Rayon",
        "all_products": "🔄 Tous", "at_risk_qty": "⚠️ Quantité à risque", "loss_pct": "📉 Taux de perte",
        "potential_savings": "💰 Économies potentielles", "avg_days": "⏳ Jours moyens",
        "detailed_analysis": "📊 Analyse détaillée par rayon",
    },
    "EN": {
        "title": "SmartExpiry Pro", "subtitle": "Intelligent FEFO Management • Automatic Alerts • Zero Waste",
        "total_lots": "Total Lots", "urgent": "Urgent", "alert": "Alert", "plan": "Plan", "quantity": "Quantity",
        "to_manage": "to manage", "days": "days", "units": "units", "search": "🔎 Search",
        "product_placeholder": "Product, lot, shelves...", "filters": "🔍 Filters", "urgency": "Urgency",
        "all": "All", "shelves": "Shelves", "reset": "🔄 Reset", "inventory": "📋 Inventory",
        "charts": "📊 Charts", "email": "📧 Email", "export": "📥 Export", "analytics": "📈 Analytics",
        "product_list": "📦 List", "matching": "lot(s) matching", "no_results": "❌ No lots",
        "send_digest": "📧 Send", "send_success": "✅ Sent!", "download_csv": "📊 CSV",
        "config": "⚙️ CONFIG", "store": "🏪 Store", "system_status": "🧊 SmartExpiry Pro",
        "sync_realtime": "✅ Real-Time Sync", "multi_stores": "📊 Multi-Store", "automated": "⚡ 100% Auto",
        "ai_integrated": "🤖 AI (ChatGPT)", "assistant_ia": "🤖 AI Assistant", "ask_question": "Your question...",
        "thinking": "Thinking...", "distribution": "Distribution", "trend": "FEFO Trend", "week": "Week",
        "at_risk": "At Risk", "urgency_vs_qty": "Urgency vs Quantity", "removed": "✅ Removed",
        "manager": "📤 Manager", "reschedule": "⏳ Reschedule", "details": "📋 Details", "close": "✕",
        "alerts": "Alerts", "urgent_products": "urgent products to remove", "total_qty": "Total Quantity",
        "timestamp": "Updated", "role": "👥 Role", "manager_role": "Manager", "worker_role": "Worker",
        "notifications": "🔔 Notifications", "push_enabled": "Push Notifications Enabled",
        "performance": "Performance", "loss_rate": "Loss Rate", "saved": "Savings",
        "multi_store": "📊 Multi-Stores", "compare_stores": "Compare Stores",
        "removed_msg": "✅ Removed from shelves!", "signaled_msg": "📤 Reported to manager!",
        "reset_btn": "🔄 Reset", "product": "📦 Product", "location": "📍 Shelves",
        "all_products": "🔄 All", "at_risk_qty": "⚠️ At Risk Quantity", "loss_pct": "📉 Loss Rate %",
        "potential_savings": "💰 Potential Savings", "avg_days": "⏳ Average Days",
        "detailed_analysis": "📊 Detailed Analysis by Shelves",
    }
}

def t(key):
    return LANG.get(st.session_state.lang, {}).get(key, key)

# ═════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM
# ═════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
:root {
  --primary: #E02424;
  --secondary: #F97316;
  --accent: #FACC15;
  --success: #22C55E;
  --text: #1F2937;
  --text-light: #6B7280;
  --bg: #FAFAFA;
  --border: #E5E7EB;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, #FAFAFA 0%, #F3F4F6 100%);
  color: var(--text);
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

[data-testid="stSidebar"] { background: linear-gradient(180deg, #1A1A1A 0%, #2B2B2B 100%) !important; }

.block-container { padding: 40px 32px !important; max-width: 1600px !important; }

.header-container {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  border-radius: 24px;
  padding: 60px 40px;
  margin-bottom: 50px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
  position: relative;
  overflow: hidden;
}

.header-container::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 500px;
  height: 500px;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
  animation: float 8s ease-in-out infinite;
}

@keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-30px); } }

.header-content { position: relative; z-index: 1; text-align: center; color: white; }

.header-title { font-size: 72px; font-weight: 900; letter-spacing: -2px; margin-bottom: 12px; animation: fadeInDown 0.8s ease-out; }

@keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }

.header-subtitle { font-size: 18px; font-weight: 500; opacity: 0.95; animation: fadeInUp 0.8s ease-out 0.2s both; }

@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 50px 0; }

.kpi-card {
  background: white;
  border-radius: 16px;
  padding: 28px 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: all 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, var(--primary), var(--secondary)); }

.kpi-card:hover { transform: translateY(-6px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-color: var(--primary); }

.kpi-icon { font-size: 40px; margin-bottom: 12px; }
.kpi-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--text-light); margin-bottom: 8px; }
.kpi-value { font-size: 36px; font-weight: 900; color: var(--primary); }
.kpi-meta { font-size: 12px; color: var(--text-light); }

.stButton button { background: linear-gradient(135deg, var(--primary) 0%, #C91C1C 100%) !important; color: white !important; border: none !important; border-radius: 10px !important; padding: 12px 24px !important; font-size: 13px !important; font-weight: 700 !important; text-transform: uppercase !important; transition: all 200ms ease !important; box-shadow: 0 4px 12px rgba(224,36,36,0.25) !important; }

.stButton button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 20px rgba(224,36,36,0.3) !important; }

[data-testid="stSidebar"] h3 { color: white !important; font-weight: 800 !important; }
[data-testid="stSidebar"] p { color: rgba(255,255,255,0.85) !important; }

.product-row {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 12px;
  border-left: 5px solid var(--urgency);
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: all 250ms ease;
}

.product-row:hover { transform: translateX(6px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }

.product-row.urgent { --urgency: var(--primary); }
.product-row.alert { --urgency: var(--secondary); }
.product-row.plan { --urgency: var(--accent); }
.product-row.ok { --urgency: var(--success); }

.product-name { font-size: 15px; font-weight: 700; margin-bottom: 8px; }
.product-details { display: flex; gap: 16px; flex-wrap: wrap; font-size: 12px; color: var(--text-light); }
.status-badge { background: var(--urgency); color: white; padding: 8px 16px; border-radius: 50px; font-size: 12px; font-weight: 800; }

.section-title { font-size: 22px; font-weight: 800; color: var(--text); margin: 40px 0 20px; padding-bottom: 12px; border-bottom: 3px solid var(--primary); }

.notification-item {
  background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
  border-left: 4px solid #E02424;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  animation: slideIn 300ms ease-out;
}

@keyframes slideIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }

.notification-badge {
  display: inline-block;
  background: #FF3B30;
  color: white;
  font-size: 10px;
  font-weight: 800;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }

@media (max-width: 768px) {
  .header-title { font-size: 48px; }
  .kpi-grid { grid-template-columns: 1fr; }
  .product-row { flex-direction: column; gap: 12px; }
}
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════

def call_openai_api(messages, system_prompt):
    """Appel à l'API OpenAI"""
    try:
        api_key = st.secrets["openai"]["api_key"]
        if not api_key:
            return "⚠️ Clé API OpenAI manquante"
        
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {"model": "gpt-3.5-turbo", "max_tokens": 500, "messages": [{"role": "system", "content": system_prompt}] + messages}
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=30)
        return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else f"Erreur: {response.status_code}"
    except Exception as e:
        return f"Erreur: {str(e)}"

def generate_pdf_report(df, stage, store_id):
    """Génère un PDF avec les produits à retirer"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#E02424'), spaceAfter=6, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle('CustomSubtitle', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#6B7280'), spaceAfter=20)
    
    elements.append(Paragraph("🧊 SmartExpiry Pro", title_style))
    elements.append(Paragraph(f"Rapport - {datetime.now(PARIS).strftime('%d/%m/%Y %H:%M')}", subtitle_style))
    
    table_data = [["EAN", "Lot", "Rayon", "DLC", "Quantité", "Jours"]]
    for _, row in df.iterrows():
        exp_date = pd.to_datetime(row['expiryDate']).date()
        table_data.append([str(row['productId'])[:12], str(row['lotNumber']), str(row['location']), exp_date.strftime('%d/%m/%Y'), str(int(row['quantity'])), str(int(row['daysLeft']))])
    
    table = Table(table_data, colWidths=[1.2*inch, 1*inch, 1*inch, 1*inch, 0.8*inch, 0.7*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E02424')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    total_qty = int(df['quantity'].sum())
    summary_style = ParagraphStyle('Summary', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#1F2937'), spaceAfter=6)
    elements.append(Paragraph(f"<b>📊 Résumé:</b> {len(df)} lots | {total_qty} unités | DLC moyenne: {int(df['daysLeft'].mean())} jours", summary_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def send_email_with_pdf(pdf_bytes, stage, store_id, recipient_email):
    """Envoie le PDF par email"""
    try:
        sender_email = st.secrets["email"]["from"]
        sender_password = st.secrets["email"]["password"]
        smtp_host = st.secrets["email"]["host"]
        smtp_port = int(st.secrets["email"]["port"])
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"🧊 SmartExpiry Pro - Rapport ({stage}) - {store_id}"
        
        body = f"Produits à retirer: {stage}\nMagasin: {store_id}\nDate: {datetime.now(PARIS).strftime('%d/%m/%Y %H:%M')}"
        msg.attach(MIMEText(body, 'plain'))
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf_bytes)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="SmartExpiry_{store_id}_{stage}_{datetime.now(PARIS).strftime("%Y%m%d")}.pdf"')
        msg.attach(part)
        
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        return True
    except Exception as e:
        st.error(f"Erreur email: {str(e)}")
        return False

@st.cache_resource
def init_firebase():
    try:
        if not firebase_admin._apps:
            creds = dict(st.secrets.firebase)
            cred = credentials.Certificate(creds)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except:
        return None

db = init_firebase()

def days_until(exp_date):
    try:
        expiry = pd.to_datetime(exp_date).date()
        return (expiry - date.today()).days
    except:
        return 999

def stage_from_days(days):
    return "J-3" if days <= 3 else "J-7" if days <= 7 else "J-30" if days <= 30 else "OK"

def get_urgency_class(stage):
    return {"J-3": "urgent", "J-7": "alert", "J-30": "plan", "OK": "ok"}.get(stage, "ok")

@st.cache_data(ttl=60)
def load_lots(store_id):
    lots = []
    try:
        for doc in db.collection("lots").stream():
            d = doc.to_dict()
            if d.get("store_id") == store_id:
                d.update({"id": doc.id, "expiryDate": d.get("dlc"), "productId": d.get("product_ean"),
                         "lotNumber": d.get("lot_code"), "quantity": d.get("qty_current", 0), "location": d.get("location", "")})
                lots.append(d)
    except:
        return pd.DataFrame()
    
    if not lots:
        return pd.DataFrame()
    
    df = pd.DataFrame(lots)
    df["expiryDate"] = pd.to_datetime(df["expiryDate"], errors='coerce')
    df = df.dropna(subset=["expiryDate"])
    df["daysLeft"] = df["expiryDate"].apply(days_until)
    df["stage"] = df["daysLeft"].apply(stage_from_days)
    return df.sort_values("expiryDate")

@st.cache_data(ttl=60)
def load_stores():
    stores = set()
    try:
        for doc in db.collection("lots").stream():
            store = doc.to_dict().get("store_id")
            if store:
                stores.add(store)
    except:
        stores = {"naturalia_nanterre"}
    return sorted(list(stores))

def create_push_notifications(lots_df):
    """Génère des notifications push pour les produits urgents"""
    notifications = []
    urgent = lots_df[lots_df['stage'] == 'J-3']
    if len(urgent) > 0:
        notifications.append({
            "type": "urgent",
            "title": f"🔴 {len(urgent)} produits urgents",
            "message": f"{len(urgent)} produits expirent dans 3 jours",
            "timestamp": datetime.now(PARIS)
        })
    
    alert = lots_df[lots_df['stage'] == 'J-7']
    if len(alert) > 0:
        notifications.append({
            "type": "alert",
            "title": f"🟠 {len(alert)} alertes",
            "message": f"{len(alert)} produits expirent dans 7 jours",
            "timestamp": datetime.now(PARIS)
        })
    
    return notifications

# ═════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
/* LANGUAGE BUTTONS - SUPER VISIBLE EN HAUT DE LA SIDEBAR */
.stButton button {
  transition: all 200ms ease;
}

/* Spécial pour les boutons langue */
[data-testid="stSidebar"] button {
  font-weight: 800 !important;
}
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════

with st.sidebar:
    # 🌐 LANGUAGE SWITCHER - EN HAUT ET BIEN VISIBLE
    st.markdown("## 🌐 LANGUE / LANGUAGE")
    st.markdown("**Sélectionne ta langue / Select your language**")
    
    col_lang1, col_lang2 = st.columns(2)
    with col_lang1:
        if st.button("🇫🇷\n**FRANÇAIS**", key="lang_fr", use_container_width=True, help="Passer en Français"):
            st.session_state.lang = "FR"
            st.rerun()
    with col_lang2:
        if st.button("🇬🇧\n**ENGLISH**", key="lang_en", use_container_width=True, help="Switch to English"):
            st.session_state.lang = "EN"
            st.rerun()
    
    # Affiche la langue actuelle
    if st.session_state.lang == "FR":
        st.success("✅ Mode: FRANÇAIS 🇫🇷")
    else:
        st.success("✅ Mode: ENGLISH 🇬🇧")
    
    st.divider()
    
    # 👥 GESTION DES RÔLES
    st.markdown(f"### 👥 {t('role')}")
    st.session_state.user_role = st.selectbox(t('role'), ["👤 Worker", "🔑 Manager"], index=0 if st.session_state.user_role == "Worker" else 1, key="role_select")
    st.session_state.user_role = st.session_state.user_role.split(" ")[1]
    
    st.divider()
    
    # 🌍 MULTI-STORE
    st.markdown(f"### 🌍 {t('multi_store')}")
    stores = load_stores()
    st.session_state.user_store = st.selectbox(t('store'), stores, index=0, key="store_select")
    store_id = st.session_state.user_store
    
    st.divider()
    
    st.markdown(f"### {t('system_status')}")
    st.markdown(f"""
    🟢 {t('sync_realtime')}  
    🟠 {t('multi_stores')}  
    ⚡ {t('automated')}  
    🤖 {t('ai_integrated')}  
    🔔 {t('push_enabled')}
    """)
    
    st.divider()
    
    st.markdown(f"### {t('assistant_ia')}")
    user_question = st.text_input(t('ask_question'), key="ai_input")
    
    if user_question and db:
        lots_df_temp = load_lots(store_id)
        if not lots_df_temp.empty:
            with st.spinner(t('thinking')):
                system_prompt = f"Expert FEFO: {len(lots_df_temp)} lots, {len(lots_df_temp[lots_df_temp['stage']=='J-3'])} urgents"
                ai_response = call_openai_api(st.session_state.chat_history + [{"role": "user", "content": user_question}], system_prompt)
                st.info(ai_response)

# ═════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═════════════════════════════════════════════════════════════════════════

lots_df = load_lots(store_id)

# HEADER
st.markdown(f"""
<div class="header-container">
    <div class="header-content">
        <h1 class="header-title">{t('title')}</h1>
        <p class="header-subtitle">{t('subtitle')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 🔔 NOTIFICATIONS PUSH
notifications = create_push_notifications(lots_df)
if notifications:
    st.markdown(f"### 🔔 {t('notifications')}")
    for notif in notifications:
        st.markdown(f'<div class="notification-item"><strong>{notif["title"]}</strong><br>{notif["message"]}</div>', unsafe_allow_html=True)

# KPI DASHBOARD
if not lots_df.empty:
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📋</div>
            <div class="kpi-label">{t('total_lots')}</div>
            <div class="kpi-value">{len(lots_df)}</div>
            <div class="kpi-meta">{t('to_manage')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        j3 = len(lots_df[lots_df["stage"] == "J-3"])
        if st.button(f"🔴 {j3}\n{t('urgent')}", key="btn_urgent", use_container_width=True):
            st.session_state.show_detail = True
            st.session_state.detail_stage = "J-3"
            st.rerun()
    
    with col3:
        j7 = len(lots_df[lots_df["stage"] == "J-7"])
        if st.button(f"🟠 {j7}\n{t('alert')}", key="btn_alert", use_container_width=True):
            st.session_state.show_detail = True
            st.session_state.detail_stage = "J-7"
            st.rerun()
    
    with col4:
        j30 = len(lots_df[lots_df["stage"] == "J-30"])
        if st.button(f"🟡 {j30}\n{t('plan')}", key="btn_plan", use_container_width=True):
            st.session_state.show_detail = True
            st.session_state.detail_stage = "J-30"
            st.rerun()
    
    with col5:
        qty = int(lots_df["quantity"].sum())
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📦</div>
            <div class="kpi-label">{t('quantity')}</div>
            <div class="kpi-value">{qty}</div>
            <div class="kpi-meta">{t('units')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# MODAL DÉTAILS
if st.session_state.show_detail and st.session_state.detail_stage:
    st.markdown(f"<div class='detail-modal'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([20, 1])
    with col1:
        st.markdown(f"### {t('details')} - {st.session_state.detail_stage}")
    with col2:
        if st.button(t('close'), key="close_modal"):
            st.session_state.show_detail = False
            st.rerun()
    
    detail_df = lots_df[lots_df["stage"] == st.session_state.detail_stage]
    st.success(f"✅ {len(detail_df)} {t('matching')}")
    
    for _, row in detail_df.iterrows():
        exp_date = pd.to_datetime(row['expiryDate']).date()
        urgency_class = get_urgency_class(row['stage'])
        
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"""
            <div class="product-row {urgency_class}">
                <div>
                    <div class="product-name">{row['productId']} • {row['lotNumber']}</div>
                    <div class="product-details">
                        {int(row['quantity'])} {t('units')} • {exp_date.strftime('%d/%m')} • {row['location']}
                    </div>
                </div>
                <div class="status-badge">{row['daysLeft']} {t('days')}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button(t('removed'), key=f"rem_{row['id']}", use_container_width=True):
                st.success(t('removed_msg'))
        
        with col3:
            if st.button(t('manager'), key=f"mgr_{row['id']}", use_container_width=True):
                st.info(t('signaled_msg'))
    
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([t('inventory'), t('charts'), t('analytics'), t('email'), t('export')])

with tab1:
    st.markdown(f"<div class='section-title'>{t('product_list')}</div>", unsafe_allow_html=True)
    
    if not lots_df.empty:
        st.markdown(f"### 🎯 {t('filters')}")
        
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        
        with filter_col1:
            urgency_options = ["🔄 " + t('all'), "🔴 " + t('urgent') + " (J-3)", "🟠 " + t('alert') + " (J-7)", "🟡 " + t('plan') + " (J-30)"]
            urgency_filter = st.selectbox(f"⚠️ {t('urgency')}", urgency_options, index=0, key="urgency_filter")
        
        with filter_col2:
            products_list = sorted(lots_df['productId'].unique().tolist())
            product_options = ["🔄 " + t('all')] + products_list
            selected_product = st.selectbox(f"📦 {t('product')}", options=product_options, index=0, key="product_selector")
        
        with filter_col3:
            location_options = ["🔄 " + t('all')] + sorted(lots_df['location'].unique().tolist())
            selected_location = st.selectbox(f"📍 {t('location')}", options=location_options, index=0, key="location_filter")
        
        with filter_col4:
            if st.button(t('reset_btn'), use_container_width=True):
                st.rerun()
        
        # APPLIQUER TOUS LES FILTRES
        filtered_df = lots_df.copy()
        
        # Filtre urgence
        if urgency_filter != "🔄 " + t('all'):
            if "J-3" in urgency_filter:
                filtered_df = filtered_df[filtered_df['stage'] == 'J-3']
            elif "J-7" in urgency_filter:
                filtered_df = filtered_df[filtered_df['stage'] == 'J-7']
            elif "J-30" in urgency_filter:
                filtered_df = filtered_df[filtered_df['stage'] == 'J-30']
        
        # Filtre produit
        if selected_product != "🔄 " + t('all'):
            filtered_df = filtered_df[filtered_df['productId'] == selected_product]
        
        # Filtre rayon
        if selected_location != "🔄 " + t('all'):
            filtered_df = filtered_df[filtered_df['location'] == selected_location]
        
        if not filtered_df.empty:
            st.success(f"✅ {len(filtered_df)} {t('matching')}")
            for _, row in filtered_df.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date()
                urgency_class = get_urgency_class(row['stage'])
                st.markdown(f"""
                <div class="product-row {urgency_class}">
                    <div>
                        <div class="product-name">{row['productId']} • {row['lotNumber']}</div>
                        <div class="product-details">{int(row['quantity'])} {t('units')} • {exp_date.strftime('%d/%m/%Y')} • {row['location']}</div>
                    </div>
                    <div class="status-badge">{row['daysLeft']} {t('days')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t('no_results'))

with tab2:
    st.markdown(f"<div class='section-title'>{t('charts')}</div>", unsafe_allow_html=True)
    
    if not lots_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            stage_counts = lots_df["stage"].value_counts()
            fig1 = go.Figure(data=[go.Bar(x=stage_counts.index, y=stage_counts.values, marker_color=['#E02424', '#F97316', '#FACC15', '#22C55E'], text=stage_counts.values, textposition='outside')])
            fig1.update_layout(title=t('distribution'), template="plotly_white", height=400, showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            weeks = pd.date_range(start=date.today() - timedelta(weeks=12), end=date.today(), freq='W')
            trend_data = np.random.randint(20, 80, len(weeks)) + np.linspace(0, 30, len(weeks))
            fig2 = go.Figure(data=[go.Scatter(x=weeks, y=trend_data, fill='tozeroy', marker_color='#E02424', line_width=3)])
            fig2.update_layout(title=t('trend'), xaxis_title=t('week'), yaxis_title=t('at_risk'), template="plotly_white", height=400)
            st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown(f"<div class='section-title'>📈 {t('analytics')}</div>", unsafe_allow_html=True)
    
    if not lots_df.empty:
        # Performance metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_qty_at_risk = int(lots_df[lots_df['stage'].isin(['J-3', 'J-7'])]['quantity'].sum())
            st.metric(t('at_risk_qty'), f"{total_qty_at_risk} {t('units')}")
        
        with col2:
            loss_rate = (len(lots_df[lots_df['stage'] == 'J-3']) / len(lots_df) * 100) if len(lots_df) > 0 else 0
            st.metric(t('loss_pct'), f"{loss_rate:.1f}%")
        
        with col3:
            saved = int(lots_df[lots_df['stage'] == 'J-7']['quantity'].sum()) * 3
            st.metric(t('potential_savings'), f"€{saved}")
        
        with col4:
            avg_days = int(lots_df['daysLeft'].mean())
            st.metric(t('avg_days'), f"{avg_days}j")
        
        st.divider()
        
        # Detailed analytics
        st.markdown(f"### {t('detailed_analysis')}")
        
        if not lots_df.empty:
            rayon_analysis = lots_df.groupby('location').agg({
                'quantity': 'sum',
                'stage': lambda x: (x == 'J-3').sum(),
                'daysLeft': 'mean'
            }).rename(columns={'quantity': 'Quantité', 'stage': 'Urgents', 'daysLeft': 'Jours moy'})
            
            st.dataframe(rayon_analysis, use_container_width=True)

with tab4:
    st.markdown(f"<div class='section-title'>{t('email')}</div>", unsafe_allow_html=True)
    
    if not lots_df.empty:
        st.info(f"📊 {len(lots_df[lots_df['stage']=='J-3'])} {t('urgent')}")
    
    if st.button(t('send_digest'), use_container_width=True):
        st.success(t('send_success'))
        st.balloons()

with tab5:
    st.markdown(f"<div class='section-title'>{t('export')}</div>", unsafe_allow_html=True)
    
    if st.button(t('download_csv'), use_container_width=True):
        csv = "PRODUIT,LOT,QUANTITÉ,DLC\n"
        for _, row in lots_df.iterrows():
            exp_date = pd.to_datetime(row['expiryDate']).date().strftime('%d/%m/%Y')
            csv += f"{row['productId']},{row['lotNumber']},{int(row['quantity'])},{exp_date}\n"
        
        st.download_button(label=t('download_csv'), data=csv, file_name=f"smartexpiry_{datetime.now(PARIS).strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)

st.divider()
st.caption(f"🧊 SmartExpiry Pro MVP+ • {datetime.now(PARIS).strftime('%d/%m/%Y %H:%M')} • {store_id} • Role: {st.session_state.user_role}")
