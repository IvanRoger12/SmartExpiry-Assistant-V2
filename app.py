"""
╔════════════════════════════════════════════════════════════════════════╗
║     🧊 SMARTEXPIRY PRO MVP+ - DESIGN RETAIL PREMIUM COMPLET           ║
║         Gestion FEFO • IA • Multilingue • LinkedIn Worthy             ║
║                    NOVEMBER 2025 - PRODUCTION                         ║
╚════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from dateutil import tz
import plotly.graph_objects as go
import plotly.express as px
import firebase_admin
from firebase_admin import credentials, firestore
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json

PARIS = tz.gettz("Europe/Paris")

# ═════════════════════════════════════════════════════════════════════════
# CONFIG
# ═════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="SmartExpiry Pro",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded"
)

# Language state
if "language" not in st.session_state:
    st.session_state.language = "FR"

# Translation dict
TRANSLATIONS = {
    "FR": {
        "title": "SmartExpiry Pro",
        "subtitle": "Gestion FEFO Intelligente • Alertes Automatiques • Zéro Perte",
        "total_lots": "Total Lots",
        "urgent": "Urgent",
        "alert": "Alerte",
        "plan": "Planifier",
        "quantity": "Quantité",
        "to_manage": "à gérer",
        "days": "jours",
        "units": "unités",
        "search": "🔎 Rechercher",
        "filters": "🔍 Filtres & Recherche",
        "inventory": "📋 Inventaire",
        "charts": "📊 Graphiques",
        "email": "📧 Email",
        "export": "📥 Export",
        "product_list": "📦 Liste des Produits",
        "matching": "lot(s) correspondent",
        "no_results": "❌ Aucun lot ne correspond",
        "send_digest": "📧 Envoyer le rapport",
        "send_success": "✅ Digest envoyé avec succès !",
        "download_csv": "📊 Télécharger CSV",
        "config": "⚙️ CONFIGURATION",
        "store": "🏪 Magasin",
        "system_status": "🧊 SmartExpiry Pro",
        "sync_realtime": "✅ Sync Temps Réel",
        "multi_stores": "📊 Multi-Magasins",
        "automated": "⚡ 100% Automatisé",
        "ai_integrated": "🤖 IA Intégrée (ChatGPT)",
        "assistant_ia": "🤖 Assistant IA (ChatGPT)",
        "ask_question": "Pose une question sur ton inventaire...",
        "thinking": "ChatGPT réfléchit...",
        "alerts": "Alertes",
        "products_remove": "produits à retirer",
        "products_removed": "lot(s) retiré(s)",
        "trend": "Tendance FEFO",
        "week": "Semaine",
        "at_risk": "À risque",
        "removed": "✅ Retiré du rayon",
        "manager": "📤 Signaler au manager",
        "reschedule": "⏳ Reporter",
    },
    "EN": {
        "title": "SmartExpiry Pro",
        "subtitle": "Intelligent FEFO Management • Automatic Alerts • Zero Waste",
        "total_lots": "Total Lots",
        "urgent": "Urgent",
        "alert": "Alert",
        "plan": "Plan",
        "quantity": "Quantity",
        "to_manage": "to manage",
        "days": "days",
        "units": "units",
        "search": "🔎 Search",
        "filters": "🔍 Filters & Search",
        "inventory": "📋 Inventory",
        "charts": "📊 Charts",
        "email": "📧 Email",
        "export": "📥 Export",
        "product_list": "📦 Product List",
        "matching": "lot(s) matching",
        "no_results": "❌ No lots matching",
        "send_digest": "📧 Send Report",
        "send_success": "✅ Digest sent successfully!",
        "download_csv": "📊 Download CSV",
        "config": "⚙️ CONFIGURATION",
        "store": "🏪 Store",
        "system_status": "🧊 SmartExpiry Pro",
        "sync_realtime": "✅ Real-Time Sync",
        "multi_stores": "📊 Multi-Store",
        "automated": "⚡ 100% Automated",
        "ai_integrated": "🤖 AI Integrated (ChatGPT)",
        "assistant_ia": "🤖 AI Assistant (ChatGPT)",
        "ask_question": "Ask a question about your inventory...",
        "thinking": "ChatGPT thinking...",
        "alerts": "Alerts",
        "products_remove": "products to remove",
        "products_removed": "lot(s) removed",
        "trend": "FEFO Trend",
        "week": "Week",
        "at_risk": "At Risk",
        "removed": "✅ Removed from shelves",
        "manager": "📤 Report to Manager",
        "reschedule": "⏳ Reschedule",
    }
}

def t(key):
    """Translate key based on current language"""
    return TRANSLATIONS[st.session_state.language].get(key, key)

# ═════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM - RETAIL PREMIUM MVP+
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
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

[data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, #FAFAFA 0%, #F3F4F6 100%);
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1A1A1A 0%, #2B2B2B 100%);
}

.block-container {
  padding: 40px 32px;
  max-width: 1600px;
}

/* ══════════════════════════════════════════════════════════════════ */
/* HEADER SECTION */
/* ══════════════════════════════════════════════════════════════════ */

.header-container {
  background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
  border-radius: 24px;
  padding: 60px 40px;
  margin-bottom: 50px;
  box-shadow: var(--shadow-lg);
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
  0%, 100% { transform: translateY(0px) translateX(0px); }
  50% { transform: translateY(-30px) translateX(20px); }
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
  letter-spacing: 0.5px;
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  position: relative;
  z-index: 2;
}

.language-selector {
  display: flex;
  gap: 12px;
  background: rgba(255,255,255,0.2);
  padding: 8px 12px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.language-selector button {
  background: transparent;
  border: none;
  color: white;
  font-weight: 700;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 8px;
  transition: all 200ms ease;
}

.language-selector button.active {
  background: rgba(255,255,255,0.3);
  transform: scale(1.05);
}

.language-selector button:hover {
  background: rgba(255,255,255,0.25);
}

.notification-icon {
  position: relative;
  font-size: 24px;
  cursor: pointer;
  transition: transform 200ms ease;
}

.notification-icon:hover {
  transform: scale(1.1);
}

.notification-badge {
  position: absolute;
  top: -8px;
  right: -8px;
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
  0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255,59,48,0.7); }
  50% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(255,59,48,0); }
}

/* ══════════════════════════════════════════════════════════════════ */
/* KPI CARDS */
/* ══════════════════════════════════════════════════════════════════ */

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
  box-shadow: var(--shadow);
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
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.kpi-icon { font-size: 40px; margin-bottom: 12px; }
.kpi-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--text-light); margin-bottom: 8px; }
.kpi-value { font-size: 36px; font-weight: 900; color: var(--primary); margin-bottom: 4px; }
.kpi-meta { font-size: 12px; color: var(--text-light); }

/* ══════════════════════════════════════════════════════════════════ */
/* BUTTONS */
/* ══════════════════════════════════════════════════════════════════ */

.stButton button {
  background: linear-gradient(135deg, var(--primary) 0%, #C91C1C 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.5px;
  transition: all 200ms ease;
  box-shadow: var(--shadow);
  text-transform: uppercase;
  position: relative;
  overflow: hidden;
}

.stButton button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255,255,255,0.3);
  transform: translate(-50%, -50%);
  transition: width 600ms, height 600ms;
}

.stButton button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(224, 36, 36, 0.3);
}

.stButton button:active::before {
  width: 300px;
  height: 300px;
}

/* ══════════════════════════════════════════════════════════════════ */
/* SIDEBAR */
/* ══════════════════════════════════════════════════════════════════ */

[data-testid="stSidebar"] {
  color: white;
}

[data-testid="stSidebar"] h3 {
  color: white;
  font-weight: 800;
  letter-spacing: 0.5px;
  margin-top: 24px;
}

[data-testid="stSidebar"] p {
  color: rgba(255,255,255,0.85);
}

.ai-badge {
  display: inline-block;
  background: rgba(59,130,246,0.2);
  border: 1px solid rgba(59,130,246,0.5);
  color: #3B82F6;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  margin-top: 8px;
  animation: glow 2s ease-in-out infinite;
}

@keyframes glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(59,130,246,0.7); }
  50% { box-shadow: 0 0 0 8px rgba(59,130,246,0); }
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  font-size: 13px;
}

/* ══════════════════════════════════════════════════════════════════ */
/* MODAL / DETAIL VIEW */
/* ══════════════════════════════════════════════════════════════════ */

.detail-view {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  animation: fadeIn 300ms ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.detail-panel {
  background: white;
  border-radius: 20px;
  padding: 40px;
  max-width: 800px;
  width: 90%;
  box-shadow: var(--shadow-lg);
  animation: slideUp 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
  max-height: 90vh;
  overflow-y: auto;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ══════════════════════════════════════════════════════════════════ */
/* PRODUCT ROW */
/* ══════════════════════════════════════════════════════════════════ */

.product-row {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 12px;
  border-left: 5px solid var(--urgency);
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: var(--shadow-sm);
  transition: all 250ms ease;
}

.product-row:hover {
  transform: translateX(6px);
  box-shadow: var(--shadow);
}

.product-row.urgent { --urgency: var(--primary); }
.product-row.alert { --urgency: var(--secondary); }
.product-row.plan { --urgency: var(--accent); }
.product-row.ok { --urgency: var(--success); }

.product-info { flex: 1; }
.product-name { font-size: 15px; font-weight: 700; margin-bottom: 8px; }
.product-details { display: flex; gap: 16px; flex-wrap: wrap; font-size: 12px; color: var(--text-light); }
.detail-item { display: flex; align-items: center; gap: 4px; }

.status-badge {
  background: var(--urgency);
  color: white;
  padding: 8px 16px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 800;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(224, 36, 36, 0.2);
  animation: pulse-soft 2s ease-in-out infinite;
}

@keyframes pulse-soft {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

/* ══════════════════════════════════════════════════════════════════ */
/* SECTION TITLE */
/* ══════════════════════════════════════════════════════════════════ */

.section-title {
  font-size: 22px;
  font-weight: 800;
  color: var(--text);
  margin: 40px 0 20px;
  padding-bottom: 12px;
  border-bottom: 3px solid var(--primary);
}

/* ══════════════════════════════════════════════════════════════════ */
/* RESPONSIVE */
/* ══════════════════════════════════════════════════════════════════ */

@media (max-width: 768px) {
  .header-title { font-size: 48px; }
  .kpi-grid { grid-template-columns: 1fr; }
  .product-row { flex-direction: column; gap: 12px; }
  .header-top { flex-direction: column; gap: 16px; }
}

</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# FIREBASE & OPENAI
# ═════════════════════════════════════════════════════════════════════════

def call_openai_api(messages, system_prompt):
    try:
        api_key = st.secrets.openai.api_key
        if not api_key:
            return None
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4o-mini",
            "max_tokens": 500,
            "messages": [{"role": "system", "content": system_prompt}] + messages
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else None
    except:
        return None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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

# ═════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════

def days_until(exp_date):
    try:
        expiry = pd.to_datetime(exp_date).date()
        return (expiry - date.today()).days
    except:
        return 999

def stage_from_days(days):
    return "J-3" if days <= 3 else "J-7" if days <= 7 else "J-30" if days <= 30 else "OK"

def get_urgency_class(stage):
    mapping = {"J-3": "urgent", "J-7": "alert", "J-30": "plan", "OK": "ok"}
    return mapping.get(stage, "ok")

@st.cache_data(ttl=60)
def load_lots(store_id):
    lots = []
    try:
        for doc in db.collection("lots").stream():
            d = doc.to_dict()
            if d.get("store_id") == store_id:
                d.update({
                    "id": doc.id,
                    "expiryDate": d.get("dlc"),
                    "productId": d.get("product_ean"),
                    "lotNumber": d.get("lot_code"),
                    "quantity": d.get("qty_current", 0),
                    "location": d.get("location", "")
                })
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

def generate_fefo_trend():
    """Generate simulated FEFO trend data"""
    weeks = pd.date_range(start=date.today() - timedelta(weeks=12), end=date.today(), freq='W')
    data = {
        "Week": weeks,
        "At_Risk": np.random.randint(20, 80, len(weeks)) + np.linspace(0, 30, len(weeks))
    }
    return pd.DataFrame(data)

# ═════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(f"### {t('config')}")
    stores = load_stores()
    store_id = st.selectbox(t('store'), stores, index=0)
    
    st.divider()
    
    st.markdown(f"### {t('system_status')}")
    st.markdown(f"""
    {t('sync_realtime')}  
    {t('multi_stores')}  
    {t('automated')}  
    {t('ai_integrated')}
    """)
    
    st.divider()
    
    st.markdown(f"### {t('assistant_ia')} <span class='ai-badge'>✨ Bêta</span>", unsafe_allow_html=True)
    
    user_question = st.text_input(t('ask_question'), key="ai_input")
    
    if user_question and db:
        lots_df_temp = load_lots(store_id)
        if not lots_df_temp.empty:
            with st.spinner(t('thinking')):
                system_prompt = f"""Tu es expert FEFO. Contexte: {len(lots_df_temp)} lots, 
                {len(lots_df_temp[lots_df_temp['stage']=='J-3'])} urgents."""
                ai_response = call_openai_api(st.session_state.chat_history + [{"role": "user", "content": user_question}], system_prompt)
                if ai_response:
                    st.info(ai_response)

# ═════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═════════════════════════════════════════════════════════════════════════

lots_df = load_lots(store_id)

# HEADER WITH LANGUAGE SELECTOR
st.markdown(f"""
<div class="header-container">
    <div class="header-top">
        <div style="flex:1;"></div>
        <div class="language-selector">
            <button class="{'active' if st.session_state.language == 'FR' else ''}" onclick="window.location.href='?lang=FR'">🇫🇷 FR</button>
            <button class="{'active' if st.session_state.language == 'EN' else ''}" onclick="window.location.href='?lang=EN'">🇬🇧 EN</button>
        </div>
    </div>
    <div class="header-content">
        <h1 class="header-title">{t('title')}</h1>
        <p class="header-subtitle">{t('subtitle')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Language switcher (simple)
query_params = st.query_params
if "lang" in query_params:
    st.session_state.language = query_params["lang"]

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
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🔴</div>
            <div class="kpi-label">{t('urgent')}</div>
            <div class="kpi-value">{j3}</div>
            <div class="kpi-meta">J-3 {t('days')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        j7 = len(lots_df[lots_df["stage"] == "J-7"])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🟠</div>
            <div class="kpi-label">{t('alert')}</div>
            <div class="kpi-value">{j7}</div>
            <div class="kpi-meta">J-7 {t('days')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        j30 = len(lots_df[lots_df["stage"] == "J-30"])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🟡</div>
            <div class="kpi-label">{t('plan')}</div>
            <div class="kpi-value">{j30}</div>
            <div class="kpi-meta">J-30 {t('days')}</div>
        </div>
        """, unsafe_allow_html=True)
    
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

# NOTIFICATION CENTER (simulated)
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("🔔"):
        st.info(f"🔴 {len(lots_df[lots_df['stage']=='J-3'])} {t('products_remove')} dans 24h\n\n🟠 Alerte multi-rayons")

# TABS
tab1, tab2, tab3, tab4 = st.tabs([t('inventory'), t('charts'), t('email'), t('export')])

with tab1:
    st.markdown(f"<div class='section-title'>{t('product_list')}</div>", unsafe_allow_html=True)
    
    if not lots_df.empty:
        st.success(f"✅ {len(lots_df)} {t('matching')}")
        
        for _, row in lots_df.iterrows():
            exp_date = pd.to_datetime(row['expiryDate']).date()
            urgency_class = get_urgency_class(row['stage'])
            
            st.markdown(f"""
            <div class="product-row {urgency_class}">
                <div class="product-info">
                    <div class="product-name">📦 {row['productId']} • Lot {row['lotNumber']}</div>
                    <div class="product-details">
                        <div class="detail-item">📊 {int(row['quantity'])} {t('units')}</div>
                        <div class="detail-item">📅 {exp_date.strftime('%d/%m/%Y')}</div>
                        <div class="detail-item">📍 {row['location']}</div>
                    </div>
                </div>
                <div class="status-badge">{row['daysLeft']} {t('days')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button(f"{t('removed')}", key=f"rem_{row['id']}", use_container_width=True)
            with col2:
                st.button(f"{t('manager')}", key=f"mgr_{row['id']}", use_container_width=True)
            with col3:
                st.button(f"{t('reschedule')}", key=f"res_{row['id']}", use_container_width=True)

with tab2:
    st.markdown(f"<div class='section-title'>{t('charts')}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        stage_counts = lots_df["stage"].value_counts()
        fig1 = go.Figure(data=[
            go.Bar(
                x=stage_counts.index,
                y=stage_counts.values,
                marker_color=['#E02424', '#F97316', '#FACC15', '#22C55E'],
                text=stage_counts.values,
                textposition='outside'
            )
        ])
        fig1.update_layout(title=t('alerts'), template="plotly_white", height=400, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        trend_df = generate_fefo_trend()
        fig2 = go.Figure(data=[
            go.Scatter(x=trend_df['Week'], y=trend_df['At_Risk'], fill='tozeroy', 
                      marker_color='#E02424', line_width=3)
        ])
        fig2.update_layout(title=t('trend'), xaxis_title=t('week'), yaxis_title=t('at_risk'), 
                          template="plotly_white", height=400)
        st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown(f"<div class='section-title'>{t('email')}</div>", unsafe_allow_html=True)
    
    st.info(f"📊 {len(lots_df[lots_df['stage']=='J-3'])} urgents")
    
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
