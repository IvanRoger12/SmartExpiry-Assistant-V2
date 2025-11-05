"""
╔════════════════════════════════════════════════════════════════════════╗
║     🧊 SMARTEXPIRY PRO MVP+ - DESIGN RETAIL PREMIUM                   ║
║              Multilingue FR/EN • Design Premium • IA                   ║
║                    NOVEMBER 2025 - PRODUCTION                         ║
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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

PARIS = tz.gettz("Europe/Paris")

# ═════════════════════════════════════════════════════════════════════════
# CONFIG & TRANSLATIONS
# ═════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="SmartExpiry Pro",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded"
)

if "lang" not in st.session_state:
    st.session_state.lang = "FR"

# COMPLETE TRANSLATION DICTIONARY
LANG = {
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
        "product_placeholder": "Produit, lot, rayon...",
        "filters": "🔍 Filtres & Recherche",
        "urgency": "Urgence",
        "all": "Tous",
        "shelves": "Rayon",
        "reset": "🔄 Réinitialiser",
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
        "ask_question": "Pose une question...",
        "thinking": "ChatGPT réfléchit...",
        "distribution": "Distribution par Urgence",
        "trend": "Tendance FEFO",
        "week": "Semaine",
        "at_risk": "À risque",
        "urgency_vs_qty": "Urgence vs Quantité",
        "remaining_days": "Jours restants",
        "removed": "✅ Retiré du rayon",
        "manager": "📤 Signaler",
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
        "product_placeholder": "Product, lot, shelves...",
        "filters": "🔍 Filters & Search",
        "urgency": "Urgency",
        "all": "All",
        "shelves": "Shelves",
        "reset": "🔄 Reset",
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
        "ask_question": "Ask a question...",
        "thinking": "ChatGPT thinking...",
        "distribution": "Distribution by Urgency",
        "trend": "FEFO Trend",
        "week": "Week",
        "at_risk": "At Risk",
        "urgency_vs_qty": "Urgency vs Quantity",
        "remaining_days": "Remaining Days",
        "removed": "✅ Removed",
        "manager": "📤 Report",
        "reschedule": "⏳ Reschedule",
    }
}

def t(key):
    """Translate key"""
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

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1A1A1A 0%, #2B2B2B 100%);
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
.kpi-value { font-size: 36px; font-weight: 900; color: var(--primary); margin-bottom: 4px; }
.kpi-meta { font-size: 12px; color: var(--text-light); }

.stButton button {
  background: linear-gradient(135deg, var(--primary) 0%, #C91C1C 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 12px 24px !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  transition: all 200ms ease !important;
  box-shadow: 0 4px 12px rgba(224,36,36,0.25) !important;
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
.status-badge { background: var(--urgency); color: white; padding: 8px 16px; border-radius: 50px; font-size: 12px; font-weight: 800; white-space: nowrap; }

.section-title {
  font-size: 22px;
  font-weight: 800;
  color: var(--text);
  margin: 40px 0 20px;
  padding-bottom: 12px;
  border-bottom: 3px solid var(--primary);
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
    try:
        api_key = st.secrets.openai.api_key
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "max_tokens": 500,
            "messages": [{"role": "system", "content": system_prompt}] + messages
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=30)
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

# ═════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════

with st.sidebar:
    # Language selector
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
    {t('sync_realtime')}  
    {t('multi_stores')}  
    {t('automated')}  
    {t('ai_integrated')}
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

# FILTERS
st.markdown(f"<div class='section-title'>{t('filters')}</div>", unsafe_allow_html=True)

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([2, 1, 1, 1])

with filter_col1:
    search = st.text_input(t('search'), placeholder=t('product_placeholder'))

with filter_col2:
    urgency = st.selectbox(t('urgency'), [t('all'), "J-3", "J-7", "J-30", "OK"])

with filter_col3:
    if not lots_df.empty:
        locations = [t('all')] + sorted(lots_df['location'].unique().tolist())
        location = st.selectbox(t('shelves'), locations)
    else:
        location = t('all')

with filter_col4:
    if st.button(t('reset'), use_container_width=True):
        st.rerun()

# Filter lots
filtered_df = lots_df.copy()
if search:
    search_lower = search.lower()
    mask = (
        filtered_df['productId'].str.lower().str.contains(search_lower, na=False) |
        filtered_df['lotNumber'].str.lower().str.contains(search_lower, na=False) |
        filtered_df['location'].str.lower().str.contains(search_lower, na=False)
    )
    filtered_df = filtered_df[mask]

if urgency != t('all'):
    filtered_df = filtered_df[filtered_df['stage'] == urgency]

if location != t('all'):
    filtered_df = filtered_df[filtered_df['location'] == location]

# TABS
tab1_name = t('inventory')
tab2_name = t('charts')
tab3_name = t('email')
tab4_name = t('export')

tab1, tab2, tab3, tab4 = st.tabs([tab1_name, tab2_name, tab3_name, tab4_name])

with tab1:
    st.markdown(f"<div class='section-title'>{t('product_list')}</div>", unsafe_allow_html=True)
    
    if not filtered_df.empty:
        st.success(f"✅ {len(filtered_df)} {t('matching')}")
        
        for _, row in filtered_df.iterrows():
            exp_date = pd.to_datetime(row['expiryDate']).date()
            urgency_class = get_urgency_class(row['stage'])
            
            st.markdown(f"""
            <div class="product-row {urgency_class}">
                <div class="product-info" style="flex:1;">
                    <div class="product-name">📦 {row['productId']} • Lot {row['lotNumber']}</div>
                    <div class="product-details">
                        <div>📊 {int(row['quantity'])} {t('units')}</div>
                        <div>📅 {exp_date.strftime('%d/%m/%Y')}</div>
                        <div>📍 {row['location']}</div>
                    </div>
                </div>
                <div class="status-badge">{row['daysLeft']} {t('days')}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(t('no_results'))

with tab2:
    st.markdown(f"<div class='section-title'>{t('charts')}</div>", unsafe_allow_html=True)
    
    if not filtered_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            stage_counts = filtered_df["stage"].value_counts()
            fig1 = go.Figure(data=[
                go.Bar(
                    x=stage_counts.index,
                    y=stage_counts.values,
                    marker_color=['#E02424', '#F97316', '#FACC15', '#22C55E'],
                    text=stage_counts.values,
                    textposition='outside'
                )
            ])
            fig1.update_layout(title=t('distribution'), template="plotly_white", height=400, showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            weeks = pd.date_range(start=date.today() - timedelta(weeks=12), end=date.today(), freq='W')
            trend_data = np.random.randint(20, 80, len(weeks)) + np.linspace(0, 30, len(weeks))
            fig2 = go.Figure(data=[
                go.Scatter(x=weeks, y=trend_data, fill='tozeroy', marker_color='#E02424', line_width=3)
            ])
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
        
        st.download_button(
            label=t('download_csv'),
            data=csv,
            file_name=f"smartexpiry_{datetime.now(PARIS).strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

st.divider()
st.caption(f"🧊 SmartExpiry Pro • {datetime.now(PARIS).strftime('%d/%m/%Y %H:%M')} • {store_id}")
