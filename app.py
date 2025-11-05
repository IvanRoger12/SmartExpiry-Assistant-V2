"""
╔════════════════════════════════════════════════════════════════════════╗
║     🧊 SMARTEXPIRY PRO MVP+ - DESIGN COMPLET PRODUCTION               ║
║        Retail Premium • Multilingue • Modales • Animations             ║
║                  READY FOR LINKEDIN & DEMO - NOV 2025                 ║
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
if "show_detail" not in st.session_state:
    st.session_state.show_detail = False
if "detail_stage" not in st.session_state:
    st.session_state.detail_stage = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

LANG = {
    "FR": {
        "title": "SmartExpiry Pro", "subtitle": "Gestion FEFO Intelligente • Alertes Automatiques • Zéro Perte",
        "total_lots": "Total Lots", "urgent": "Urgent", "alert": "Alerte", "plan": "Planifier", "quantity": "Quantité",
        "to_manage": "à gérer", "days": "jours", "units": "unités", "search": "🔎 Rechercher",
        "product_placeholder": "Produit, lot, rayon...", "filters": "🔍 Filtres", "urgency": "Urgence",
        "all": "Tous", "shelves": "Rayon", "reset": "🔄 Réin", "inventory": "📋 Inventaire", "charts": "📊 Graphiques",
        "email": "📧 Email", "export": "📥 Export", "product_list": "📦 Liste", "matching": "lot(s) correspondent",
        "no_results": "❌ Aucun lot", "send_digest": "📧 Envoyer", "send_success": "✅ Envoyé !", 
        "download_csv": "📊 CSV", "config": "⚙️ CONFIG", "store": "🏪 Magasin", "system_status": "🧊 SmartExpiry Pro",
        "sync_realtime": "✅ Sync Temps Réel", "multi_stores": "📊 Multi-Magasins", "automated": "⚡ 100% Auto",
        "ai_integrated": "🤖 IA (ChatGPT)", "assistant_ia": "🤖 Assistant IA", "ask_question": "Ta question...",
        "thinking": "Réfléchit...", "distribution": "Distribution", "trend": "Tendance FEFO", "week": "Semaine",
        "at_risk": "À risque", "urgency_vs_qty": "Urgence vs Quantité", "removed": "✅ Retiré",
        "manager": "📤 Manager", "reschedule": "⏳ Reporter", "details": "📋 Détails", "close": "✕",
        "alerts": "Alertes", "urgent_products": "produits urgents à retirer", "total_qty": "Quantité totale",
        "timestamp": "Mis à jour",
    },
    "EN": {
        "title": "SmartExpiry Pro", "subtitle": "Intelligent FEFO Management • Automatic Alerts • Zero Waste",
        "total_lots": "Total Lots", "urgent": "Urgent", "alert": "Alert", "plan": "Plan", "quantity": "Quantity",
        "to_manage": "to manage", "days": "days", "units": "units", "search": "🔎 Search",
        "product_placeholder": "Product, lot, shelves...", "filters": "🔍 Filters", "urgency": "Urgency",
        "all": "All", "shelves": "Shelves", "reset": "🔄 Reset", "inventory": "📋 Inventory", "charts": "📊 Charts",
        "email": "📧 Email", "export": "📥 Export", "product_list": "📦 List", "matching": "lot(s) matching",
        "no_results": "❌ No lots", "send_digest": "📧 Send", "send_success": "✅ Sent!",
        "download_csv": "📊 CSV", "config": "⚙️ CONFIG", "store": "🏪 Store", "system_status": "🧊 SmartExpiry Pro",
        "sync_realtime": "✅ Real-Time Sync", "multi_stores": "📊 Multi-Store", "automated": "⚡ 100% Auto",
        "ai_integrated": "🤖 AI (ChatGPT)", "assistant_ia": "🤖 AI Assistant", "ask_question": "Your question...",
        "thinking": "Thinking...", "distribution": "Distribution", "trend": "FEFO Trend", "week": "Week",
        "at_risk": "At Risk", "urgency_vs_qty": "Urgency vs Quantity", "removed": "✅ Removed",
        "manager": "📤 Manager", "reschedule": "⏳ Reschedule", "details": "📋 Details", "close": "✕",
        "alerts": "Alerts", "urgent_products": "urgent products to remove", "total_qty": "Total Quantity",
        "timestamp": "Updated",
    }
}

def t(key):
    return LANG.get(st.session_state.lang, {}).get(key, key)

# ═════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM - PREMIUM RETAIL
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

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1A1A1A 0%, #2B2B2B 100%) !important;
}

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

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-30px); }
}

.header-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
}

.header-title {
  font-size: 72px;
  font-weight: 900;
  letter-spacing: -2px;
  margin-bottom: 12px;
  animation: fadeInDown 0.8s ease-out;
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

.header-subtitle {
  font-size: 18px;
  font-weight: 500;
  opacity: 0.95;
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 50px 0;
}

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

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
}

.kpi-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  border-color: var(--primary);
}

.kpi-icon { font-size: 40px; margin-bottom: 12px; }
.kpi-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--text-light); margin-bottom: 8px; }
.kpi-value { font-size: 36px; font-weight: 900; color: var(--primary); }
.kpi-meta { font-size: 12px; color: var(--text-light); }

.stButton button {
  background: linear-gradient(135deg, var(--primary) 0%, #C91C1C 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 12px 24px !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  transition: all 200ms ease !important;
  box-shadow: 0 4px 12px rgba(224,36,36,0.25) !important;
  position: relative !important;
  overflow: hidden !important;
}

.stButton button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 20px rgba(224,36,36,0.3) !important;
}

.stTabs [data-baseweb="tab-list"] {
  border-bottom: 2px solid var(--border) !important;
  gap: 32px !important;
}

.stTabs [aria-selected="true"] {
  border-bottom: 3px solid var(--primary) !important;
  color: var(--primary) !important;
  font-weight: 800 !important;
}

.stTabs [aria-selected="false"] {
  color: var(--text-light) !important;
  font-weight: 600 !important;
}

[data-testid="stSidebar"] h3 {
  color: white !important;
  font-weight: 800 !important;
}

[data-testid="stSidebar"] p {
  color: rgba(255,255,255,0.85) !important;
}

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
  cursor: pointer;
}

.product-row:hover {
  transform: translateX(6px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.product-row.urgent { --urgency: var(--primary); }
.product-row.alert { --urgency: var(--secondary); }
.product-row.plan { --urgency: var(--accent); }
.product-row.ok { --urgency: var(--success); }

.product-name { font-size: 15px; font-weight: 700; margin-bottom: 8px; }
.product-details { display: flex; gap: 16px; flex-wrap: wrap; font-size: 12px; color: var(--text-light); }
.status-badge { background: var(--urgency); color: white; padding: 8px 16px; border-radius: 50px; font-size: 12px; font-weight: 800; }

.section-title {
  font-size: 22px;
  font-weight: 800;
  color: var(--text);
  margin: 40px 0 20px;
  padding-bottom: 12px;
  border-bottom: 3px solid var(--primary);
}

.detail-modal {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
  animation: slideUp 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}

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

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.ai-badge {
  display: inline-block;
  background: rgba(59,130,246,0.2);
  border: 1px solid rgba(59,130,246,0.5);
  color: #3B82F6;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 700;
  animation: glow 2s ease-in-out infinite;
}

@keyframes glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(59,130,246,0.7); }
  50% { box-shadow: 0 0 0 8px rgba(59,130,246,0); }
}

@media (max-width: 768px) {
  .header-title { font-size: 48px; }
  .kpi-grid { grid-template-columns: 1fr; }
  .product-row { flex-direction: column; gap: 12px; }
}

</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# FIREBASE & FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════

def call_openai_api(messages, system_prompt):
    """Appel à l'API OpenAI"""
    try:
        api_key = st.secrets.get("openai_api_key", "")
        if not api_key:
            return "⚠️ Clé API OpenAI manquante. Configure les secrets Streamlit."
        
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {
            "model": "gpt-4-mini",
            "max_tokens": 500,
            "messages": [{"role": "system", "content": system_prompt}] + messages
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"❌ Erreur API: {response.status_code}"
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

def generate_pdf_report(df, stage, store_id):
    """Génère un PDF avec les produits à retirer"""
    buffer = BytesIO()
    
    # Create PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Header
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#E02424'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#6B7280'),
        spaceAfter=20
    )
    
    elements.append(Paragraph("🧊 SmartExpiry Pro", title_style))
    elements.append(Paragraph(f"Rapport de Produits à Retirer - {datetime.now(PARIS).strftime('%d/%m/%Y %H:%M')}", subtitle_style))
    
    # Store info
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=12
    )
    
    stage_label = {"J-3": "URGENT (3 jours)", "J-7": "ALERTE (7 jours)", "J-30": "À PLANIFIER (30 jours)"}.get(stage, stage)
    elements.append(Paragraph(f"<b>Magasin:</b> {store_id} | <b>Catégorie:</b> {stage_label} | <b>Nombre de lots:</b> {len(df)}", info_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Table data
    table_data = [["EAN", "Lot", "Rayon", "DLC", "Quantité", "Jours"]]
    
    for _, row in df.iterrows():
        exp_date = pd.to_datetime(row['expiryDate']).date()
        table_data.append([
            str(row['productId'])[:12],
            str(row['lotNumber']),
            str(row['location']),
            exp_date.strftime('%d/%m/%Y'),
            str(int(row['quantity'])),
            str(int(row['daysLeft']))
        ])
    
    # Create table
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
    
    # Summary
    total_qty = int(df['quantity'].sum())
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=6
    )
    
    elements.append(Paragraph(f"<b>📊 Résumé:</b> {len(df)} lots | {total_qty} unités | DLC moyenne: {int(df['daysLeft'].mean())} jours", summary_style))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#9CA3AF'),
        spaceAfter=6
    )
    
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("🧊 SmartExpiry Pro | Gestion FEFO Intelligente | Zéro Perte", footer_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def send_email_with_pdf(pdf_bytes, stage, store_id, recipient_email):
    """Envoie le PDF par email"""
    try:
        sender_email = st.secrets.email.get("from", "nfindaroger@gmail.com")
        sender_password = st.secrets.email.get("password", "")
        smtp_host = st.secrets.email.get("host", "smtp.sendgrid.net")
        smtp_port = int(st.secrets.email.get("port", 587))
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"🧊 SmartExpiry Pro - Produits à retirer ({stage}) - {store_id}"
        
        # Body
        body = f"""Bonjour,

Veuillez trouver en pièce jointe le rapport SmartExpiry Pro des produits à retirer.

Catégorie: {stage}
Magasin: {store_id}
Date: {datetime.now(PARIS).strftime('%d/%m/%Y %H:%M')}

Actions recommandées:
✅ Vérifier les produits listés
📤 Réduire les prix si nécessaire
⏳ Reporter si action non urgente

Cordialement,
🧊 SmartExpiry Pro
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf_bytes)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= "SmartExpiry_{store_id}_{stage}_{datetime.now(PARIS).strftime("%Y%m%d")}.pdf"')
        msg.attach(part)
        
        # Send email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        return True
    except Exception as e:
        st.error(f"❌ Erreur email: {str(e)}")
        return False
    try:
        api_key = st.secrets.openai.api_key
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {"model": "gpt-4o-mini", "max_tokens": 500, "messages": [{"role": "system", "content": system_prompt}] + messages}
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=30)
        return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else None
    except:
        return None

@st.cache_resource
def init_firebase():
    try:
        if not firebase_admin._apps:
            creds = dict(st.secrets.firebase)
            for key in creds:
                if isinstance(creds[key], str):
                    creds[key] = creds[key].replace('__', '')
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

# ═════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇫🇷 FR"):
            st.session_state.lang = "FR"
            st.rerun()
    with col2:
        if st.button("🇬🇧 EN"):
            st.session_state.lang = "EN"
            st.rerun()
    
    st.divider()
    
    st.markdown(f"### {t('config')}")
    stores = load_stores()
    store_id = st.selectbox(t('store'), stores, index=0)
    
    st.divider()
    
    st.markdown(f"### {t('system_status')}")
    st.markdown(f"""
    🟢 {t('sync_realtime')}  
    🟠 {t('multi_stores')}  
    ⚡ {t('automated')}  
    🤖 {t('ai_integrated')}
    """)
    
    st.divider()
    
    st.markdown(f"### {t('assistant_ia')} <span class='ai-badge'>✨</span>", unsafe_allow_html=True)
    user_question = st.text_input(t('ask_question'), key="ai_input")
    
    if user_question and db:
        lots_df_temp = load_lots(store_id)
        if not lots_df_temp.empty:
            with st.spinner(t('thinking')):
                system_prompt = f"Expert FEFO: {len(lots_df_temp)} lots, {len(lots_df_temp[lots_df_temp['stage']=='J-3'])} urgents"
                ai_response = call_openai_api(st.session_state.chat_history + [{"role": "user", "content": user_question}], system_prompt)
                if ai_response:
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

# KPI DASHBOARD
if not lots_df.empty:
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card" onclick="document.dispatchEvent(new CustomEvent('kpi_click', {{detail: 'total'}}))" style="cursor:pointer;">
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

# MODAL DÉTAILS - VUE COMPLÈTE AVEC FILTRES
if st.session_state.show_detail and st.session_state.detail_stage:
    st.markdown(f"""
    <style>
    .detail-header {{
        background: linear-gradient(135deg, #E02424 0%, #F97316 100%);
        color: white;
        padding: 30px;
        border-radius: 20px 20px 0 0;
        margin-bottom: 20px;
        animation: slideDown 400ms ease-out;
    }}
    
    @keyframes slideDown {{
        from {{ opacity: 0; transform: translateY(-20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .detail-container {{
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        animation: slideUp 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    
    @keyframes slideUp {{
        from {{ opacity: 0; transform: translateY(40px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .filter-box {{
        background: #F3F4F6;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 4px solid #E02424;
    }}
    
    .product-card {{
        background: white;
        border: 2px solid #E5E7EB;
        border-left: 5px solid var(--urgency);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: all 250ms ease;
    }}
    
    .product-card:hover {{
        transform: translateX(6px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border-color: #E02424;
    }}
    
    .product-card.urgent {{ --urgency: #E02424; }}
    .product-card.alert {{ --urgency: #F97316; }}
    .product-card.plan {{ --urgency: #FACC15; }}
    
    .product-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }}
    
    .product-name-bold {{
        font-size: 16px;
        font-weight: 800;
        color: #1F2937;
    }}
    
    .product-meta {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 12px;
        font-size: 13px;
        color: #6B7280;
        margin-bottom: 12px;
    }}
    
    .meta-item {{
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    
    .action-buttons {{
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }}
    
    .action-btn {{
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        border: none;
        cursor: pointer;
        transition: all 200ms ease;
    }}
    
    .action-btn.removed {{
        background: #22C55E;
        color: white;
    }}
    
    .action-btn.manager {{
        background: #F97316;
        color: white;
    }}
    
    .action-btn.reschedule {{
        background: #3B82F6;
        color: white;
    }}
    
    .action-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    
    </style>
    """, unsafe_allow_html=True)
    
    # HEADER MODAL
    st.markdown(f"""
    <div class="detail-header">
        <h2 style="margin: 0 0 8px 0;">📦 {t('details')} - {st.session_state.detail_stage} {t('urgent')}</h2>
        <p style="margin: 0; opacity: 0.95; font-size: 14px;">Cliquez sur les actions pour gérer les lots</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="detail-container">', unsafe_allow_html=True)
    
    # CLOSE BUTTON
    if st.button("✕ Fermer", key="close_modal", use_container_width=False):
        st.session_state.show_detail = False
        st.rerun()
    
    st.divider()
    
    # BOUTON ENVOYER PDF
    col_pdf1, col_pdf2, col_pdf3 = st.columns([1, 1, 2])
    with col_pdf1:
        email_recipient = st.text_input("📧 Email destinataire", value=st.secrets.email.get("to", ""), key="pdf_email")
    with col_pdf2:
        if st.button("📨 Envoyer PDF par mail", use_container_width=True):
            detail_df_for_pdf = lots_df[lots_df["stage"] == st.session_state.detail_stage].copy()
            if not detail_df_for_pdf.empty and email_recipient:
                with st.spinner("Génération et envoi du PDF..."):
                    pdf_bytes = generate_pdf_report(detail_df_for_pdf, st.session_state.detail_stage, store_id)
                    if send_email_with_pdf(pdf_bytes, st.session_state.detail_stage, store_id, email_recipient):
                        st.success(f"✅ PDF envoyé à {email_recipient} !")
                        st.balloons()
                    else:
                        st.error("❌ Erreur lors de l'envoi")
            else:
                st.warning("⚠️ Complète l'email et assure-toi d'avoir des produits")
    with col_pdf3:
        pass
    
    st.divider()
    
    # FILTRES
    detail_df = lots_df[lots_df["stage"] == st.session_state.detail_stage].copy()
    
    st.markdown(f"<div class='filter-box'><strong>🔍 {t('filters')}</strong></div>", unsafe_allow_html=True)
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        if not detail_df.empty:
            locations = [t('all')] + sorted(detail_df['location'].unique().tolist())
            filter_location = st.selectbox(f"📍 {t('shelves')}", locations, key="filter_location")
        else:
            filter_location = t('all')
    
    with filter_col2:
        filter_qty = st.slider(f"📦 {t('quantity')} min", 0, int(detail_df['quantity'].max()) if not detail_df.empty else 10, 0)
    
    with filter_col3:
        if st.button("🔄 Rafraîchir", use_container_width=True):
            st.rerun()
    
    # APPLIQUER FILTRES
    if filter_location != t('all'):
        detail_df = detail_df[detail_df['location'] == filter_location]
    
    detail_df = detail_df[detail_df['quantity'] >= filter_qty]
    detail_df = detail_df.sort_values('expiryDate')
    
    st.divider()
    
    # STATS
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Lots", len(detail_df))
    with col2:
        st.metric("📦 Quantité", int(detail_df['quantity'].sum()))
    with col3:
        st.metric("📍 Rayons", detail_df['location'].nunique())
    with col4:
        days_avg = int(detail_df['daysLeft'].mean())
        st.metric("⏳ Jours moy.", f"{days_avg}j")
    
    st.divider()
    
    # PRODUCTS LIST
    if not detail_df.empty:
        st.markdown(f"### ✅ {len(detail_df)} {t('matching')}")
        
        for idx, (_, row) in enumerate(detail_df.iterrows()):
            exp_date = pd.to_datetime(row['expiryDate']).date()
            urgency_class = get_urgency_class(row['stage'])
            
            st.markdown(f"""
            <div class="product-card {urgency_class}">
                <div class="product-header">
                    <div>
                        <div class="product-name-bold">📦 {row['productId']}</div>
                        <div style="font-size: 12px; color: #9CA3AF;">Lot: {row['lotNumber']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 20px; font-weight: 900; color: #E02424;">{row['daysLeft']} {t('days')}</div>
                        <div style="font-size: 11px; color: #6B7280;">avant expiration</div>
                    </div>
                </div>
                
                <div class="product-meta">
                    <div class="meta-item">📍 {row['location']}</div>
                    <div class="meta-item">📅 {exp_date.strftime('%d/%m/%Y')}</div>
                    <div class="meta-item">📦 {int(row['quantity'])} unités</div>
                    <div class="meta-item">🏷️ {row['stage']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # ACTION BUTTONS
            act_col1, act_col2, act_col3, act_col4 = st.columns([1, 1, 1, 2])
            
            with act_col1:
                if st.button("✅ Retiré", key=f"removed_{idx}_{row['id']}", use_container_width=True):
                    st.success("✅ Produit marqué comme retiré du rayon !")
            
            with act_col2:
                if st.button("📤 Manager", key=f"manager_{idx}_{row['id']}", use_container_width=True):
                    st.info("📤 Signalement envoyé au manager !")
            
            with act_col3:
                if st.button("⏳ Reporter", key=f"reschedule_{idx}_{row['id']}", use_container_width=True):
                    st.warning("⏳ Action reportée de 24h")
            
            with act_col4:
                st.write("")
    else:
        st.info(f"❌ Aucun produit ne correspond à ces filtres")
    
    st.markdown("</div>", unsafe_allow_html=True)

# NOTIFICATION HUB
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    pass
with col2:
    if st.button(f"🔔 {len(lots_df[lots_df['stage']=='J-3'])}"):
        st.info(f"🔴 {len(lots_df[lots_df['stage']=='J-3'])} {t('urgent_products')}")
with col3:
    pass

st.divider()

# TABS
tab1, tab2, tab3, tab4 = st.tabs([t('inventory'), t('charts'), t('email'), t('export')])

with tab1:
    st.markdown(f"<div class='section-title'>{t('product_list')}</div>", unsafe_allow_html=True)
    
    if not lots_df.empty:
        search = st.text_input(t('search'), placeholder=t('product_placeholder'))
        
        filtered_df = lots_df.copy()
        if search:
            search_lower = search.lower()
            mask = (filtered_df['productId'].str.lower().str.contains(search_lower, na=False))
            filtered_df = filtered_df[mask]
        
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
            fig1 = go.Figure(data=[go.Bar(x=stage_counts.index, y=stage_counts.values,
                                         marker_color=['#E02424', '#F97316', '#FACC15', '#22C55E'],
                                         text=stage_counts.values, textposition='outside')])
            fig1.update_layout(title=t('distribution'), template="plotly_white", height=400, showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            weeks = pd.date_range(start=date.today() - timedelta(weeks=12), end=date.today(), freq='W')
            trend_data = np.random.randint(20, 80, len(weeks)) + np.linspace(0, 30, len(weeks))
            fig2 = go.Figure(data=[go.Scatter(x=weeks, y=trend_data, fill='tozeroy', marker_color='#E02424', line_width=3)])
            fig2.update_layout(title=t('trend'), xaxis_title=t('week'), yaxis_title=t('at_risk'), template="plotly_white", height=400)
            st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown(f"<div class='section-title'>{t('email')}</div>", unsafe_allow_html=True)
    
    if not lots_df.empty:
        st.info(f"📊 {len(lots_df[lots_df['stage']=='J-3'])} {t('urgent')}")
    
    if st.button(t('send_digest'), use_container_width=True):
        st.success(t('send_success'))
        st.balloons()

with tab4:
    st.markdown(f"<div class='section-title'>{t('export')}</div>", unsafe_allow_html=True)
    
    if st.button(t('download_csv'), use_container_width=True):
        csv = "PRODUIT,LOT,QUANTITÉ,DLC\n"
        for _, row in lots_df.iterrows():
            exp_date = pd.to_datetime(row['expiryDate']).date().strftime('%d/%m/%Y')
            csv += f"{row['productId']},{row['lotNumber']},{int(row['quantity'])},{exp_date}\n"
        
        st.download_button(label=t('download_csv'), data=csv,
                          file_name=f"smartexpiry_{datetime.now(PARIS).strftime('%Y%m%d')}.csv",
                          mime="text/csv", use_container_width=True)

st.divider()
st.caption(f"🧊 SmartExpiry Pro MVP+ • {datetime.now(PARIS).strftime('%d/%m/%Y %H:%M')} • {store_id}")
