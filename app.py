"""
╔════════════════════════════════════════════════════════════════════════╗
║         🧊 SMARTEXPIRY PRO - DESIGN PREMIUM RETAIL EDITION             ║
║              Gestion FEFO • ChatGPT • Design Ultra Pro                  ║
║                    LINKEDIN WORTHY - NOV 5, 2025                       ║
╚════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
from dateutil import tz
import plotly.graph_objects as go
import firebase_admin
from firebase_admin import credentials, firestore
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json

PARIS = tz.gettz("Europe/Paris")

st.set_page_config(
    page_title="SmartExpiry Pro",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded"
)

# ═════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM - ULTRA PREMIUM RETAIL
# ═════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
:root {
  --primary: #E30613;
  --secondary: #F39200;
  --accent: #00B050;
  --dark: #1A1A1A;
  --light: #F8F8F8;
  --border: #E5E5E5;
  --shadow: 0 8px 24px rgba(0,0,0,0.12);
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.08);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, #FAFAFA 0%, #F5F5F5 100%);
  color: var(--dark);
  font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
}

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, var(--dark) 0%, #2A2A2A 100%) !important;
}

.block-container {
  padding: 40px 32px !important;
  max-width: 1600px !important;
}

/* ═══════════════════════════════════════════════════════════════ */
/* HERO SECTION */
/* ═══════════════════════════════════════════════════════════════ */

.header-hero {
  background: linear-gradient(135deg, var(--primary) 0%, #C20410 50%, var(--secondary) 100%);
  border-radius: 20px;
  padding: 60px 40px;
  margin-bottom: 50px;
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
}

.header-hero::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.header-content {
  position: relative;
  z-index: 1;
  color: white;
  text-align: center;
}

.header-title {
  font-size: 56px;
  font-weight: 800;
  letter-spacing: -1.5px;
  margin-bottom: 12px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.header-subtitle {
  font-size: 18px;
  font-weight: 500;
  opacity: 0.95;
  letter-spacing: 0.5px;
}

/* ═══════════════════════════════════════════════════════════════ */
/* KPI CARDS - PREMIUM */
/* ═══════════════════════════════════════════════════════════════ */

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin: 50px 0;
}

.kpi-card {
  background: white;
  border-radius: 16px;
  padding: 32px 24px;
  box-shadow: var(--shadow-sm);
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
  transform: translateY(-8px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.15);
  border-color: var(--primary);
}

.kpi-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display: block;
}

.kpi-label {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: #888;
  margin-bottom: 12px;
}

.kpi-value {
  font-size: 42px;
  font-weight: 900;
  color: var(--primary);
  margin-bottom: 8px;
  line-height: 1;
}

.kpi-meta {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

/* ═══════════════════════════════════════════════════════════════ */
/* PRODUCT ROWS - PREMIUM */
/* ═══════════════════════════════════════════════════════════════ */

.product-row {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
  border-left: 5px solid var(--urgency-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: var(--shadow-sm);
  transition: all 250ms ease;
  position: relative;
}

.product-row::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 0;
  background: rgba(227, 6, 19, 0.05);
  border-radius: 0 0 12px 12px;
  transition: height 250ms ease;
}

.product-row:hover {
  transform: translateX(8px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.12);
}

.product-row.urgent { --urgency-color: #E30613; }
.product-row.alert { --urgency-color: #F39200; }
.product-row.plan { --urgency-color: #FFD700; }
.product-row.ok { --urgency-color: #00B050; }

.product-info {
  flex: 1;
  z-index: 1;
}

.product-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 12px;
}

.product-details {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  font-size: 13px;
  color: #666;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
}

.status-badge {
  background: linear-gradient(135deg, var(--urgency-color), var(--urgency-color));
  color: white;
  padding: 10px 18px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 800;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(227, 6, 19, 0.25);
  letter-spacing: 0.5px;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 4px 12px rgba(227, 6, 19, 0.25); }
  50% { box-shadow: 0 8px 20px rgba(227, 6, 19, 0.4); }
}

/* ═══════════════════════════════════════════════════════════════ */
/* BUTTONS */
/* ═══════════════════════════════════════════════════════════════ */

.stButton button {
  background: linear-gradient(135deg, var(--primary) 0%, #C20410 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 14px 28px !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  letter-spacing: 0.5px !important;
  transition: all 200ms cubic-bezier(0.34, 1.56, 0.64, 1) !important;
  box-shadow: 0 6px 20px rgba(227, 6, 19, 0.3) !important;
  min-height: 44px !important;
  text-transform: uppercase;
}

.stButton button:hover {
  transform: translateY(-3px) !important;
  box-shadow: 0 10px 32px rgba(227, 6, 19, 0.45) !important;
}

.stButton button:active {
  transform: translateY(-1px) !important;
}

/* ═══════════════════════════════════════════════════════════════ */
/* TABS */
/* ═══════════════════════════════════════════════════════════════ */

.stTabs [data-baseweb="tab-list"] {
  border-bottom: 2px solid var(--border) !important;
  gap: 32px !important;
  background: transparent !important;
  padding: 0 !important;
}

.stTabs [aria-selected="true"] {
  border-bottom: 3px solid var(--primary) !important;
  color: var(--primary) !important;
  font-weight: 800 !important;
  font-size: 16px !important;
}

.stTabs [aria-selected="false"] {
  color: #999 !important;
  font-weight: 600 !important;
  font-size: 15px !important;
}

/* ═══════════════════════════════════════════════════════════════ */
/* SIDEBAR */
/* ═══════════════════════════════════════════════════════════════ */

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
  color: white !important;
}

[data-testid="stSidebar"] h3 {
  color: white !important;
  font-weight: 800 !important;
  letter-spacing: 0.5px !important;
}

[data-testid="stSidebar"] p {
  color: rgba(255,255,255,0.85) !important;
}

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] select {
  background: rgba(255,255,255,0.1) !important;
  border: 1px solid rgba(255,255,255,0.2) !important;
  color: white !important;
  border-radius: 8px !important;
}

/* ═══════════════════════════════════════════════════════════════ */
/* SECTION TITLES */
/* ═══════════════════════════════════════════════════════════════ */

.section-title {
  font-size: 24px;
  font-weight: 800;
  color: var(--dark);
  margin: 40px 0 20px 0;
  padding-bottom: 16px;
  border-bottom: 3px solid var(--primary);
  letter-spacing: -0.5px;
}

/* ═══════════════════════════════════════════════════════════════ */
/* RESPONSIVE */
/* ═══════════════════════════════════════════════════════════════ */

@media (max-width: 768px) {
  .header-hero {
    padding: 40px 24px;
  }
  
  .header-title {
    font-size: 36px;
  }
  
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  
  .product-row {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .status-badge {
    margin-top: 12px;
    align-self: flex-end;
  }
  
  .product-details {
    gap: 12px;
  }
}

</style>
""", unsafe_allow_html=True)

# OpenAI API call
def call_openai_api(messages, system_prompt):
    """Appel direct à l'API OpenAI via requests"""
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
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            st.error(f"❌ Erreur OpenAI: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"❌ Erreur OpenAI: {str(e)}")
        return None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Firebase
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
    except Exception as e:
        st.error(f"❌ Erreur Firebase: {str(e)}")
        return None

db = init_firebase()

# Utility functions
def days_until(exp_date):
    try:
        expiry = pd.to_datetime(exp_date).date()
        return (expiry - date.today()).days
    except:
        return 999

def stage_from_days(days):
    if days <= 3:
        return "J-3"
    elif days <= 7:
        return "J-7"
    elif days <= 30:
        return "J-30"
    else:
        return "OK"

def get_urgency_class(stage):
    if stage == "J-3":
        return "urgent"
    elif stage == "J-7":
        return "alert"
    elif stage == "J-30":
        return "plan"
    else:
        return "ok"

@st.cache_data(ttl=60)
def load_lots(store_id):
    lots = []
    try:
        for doc in db.collection("lots").stream():
            d = doc.to_dict()
            d["id"] = doc.id
            d["expiryDate"] = d.get("dlc")
            d["productId"] = d.get("product_ean")
            d["lotNumber"] = d.get("lot_code")
            d["quantity"] = d.get("qty_current", 0)
            d["location"] = d.get("location", "")
            
            if d.get("store_id") == store_id:
                lots.append(d)
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")
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

def filter_lots(df, search, urgency, location):
    result = df.copy()
    
    if search:
        search_lower = search.lower()
        mask = (
            result['productId'].str.lower().str.contains(search_lower, na=False) |
            result['lotNumber'].str.lower().str.contains(search_lower, na=False) |
            result['location'].str.lower().str.contains(search_lower, na=False)
        )
        result = result[mask]
    
    if urgency != "Tous":
        result = result[result['stage'] == urgency]
    
    if location != "Tous":
        result = result[result['location'] == location]
    
    return result

def chat_with_gpt(user_message, lots_data_context):
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_message
    })
    
    system_prompt = f"""Tu es un expert en gestion d'inventaire FEFO pour les supermarchés.
Tu analyzes les données d'inventaire et donnes des recommandations intelligentes.

CONTEXTE ACTUEL DE L'INVENTAIRE:
- Total lots: {len(lots_data_context)}
- Lots urgent (J-3): {len(lots_data_context[lots_data_context['stage'] == 'J-3'])}
- Lots alerte (J-7): {len(lots_data_context[lots_data_context['stage'] == 'J-7'])}
- Lots à planifier (J-30): {len(lots_data_context[lots_data_context['stage'] == 'J-30'])}
- Quantité totale: {int(lots_data_context['quantity'].sum())} unités

Réponds en français, de manière concise et actionnable.
Donne des recommandations pratiques immédiates."""
    
    assistant_message = call_openai_api(st.session_state.chat_history, system_prompt)
    
    if assistant_message:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        return assistant_message
    else:
        st.error("❌ ChatGPT non disponible")
        return None

# SIDEBAR
with st.sidebar:
    st.markdown("### ⚙️ CONFIGURATION")
    stores = load_stores()
    store_id = st.selectbox("🏪 Magasin", stores, index=0)
    
    st.divider()
    
    st.markdown("""
    ### 🧊 SmartExpiry Pro
    
    **Gestion FEFO Intelligente**
    
    ✅ Sync Real-Time  
    📊 Multi-Magasins  
    ⚡ 100% Automatisé  
    🤖 IA Intégrée (ChatGPT)
    """)
    
    st.divider()
    
    st.markdown("### 🤖 Assistant IA (ChatGPT)")
    
    user_question = st.text_input(
        "Pose une question sur ton inventaire...",
        placeholder="Ex: Quels produits je dois retirer demain ?",
        key="ai_input"
    )
    
    if user_question and db:
        lots_df_temp = load_lots(store_id)
        if not lots_df_temp.empty:
            with st.spinner("ChatGPT réfléchit..."):
                try:
                    ai_response = chat_with_gpt(user_question, lots_df_temp)
                    st.info(ai_response)
                except Exception as e:
                    st.error(f"❌ Erreur ChatGPT: {str(e)}")
        else:
            st.warning("Pas de données disponibles")

# MAIN CONTENT
lots_df = load_lots(store_id)

st.markdown("""
<div class="header-hero">
    <div class="header-content">
        <h1 class="header-title">🧊 SmartExpiry Pro</h1>
        <p class="header-subtitle">Gestion FEFO Intelligente • Alertes Automatiques • Zéro Perte</p>
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
            <div class="kpi-label">Total Lots</div>
            <div class="kpi-value">{len(lots_df)}</div>
            <div class="kpi-meta">à gérer</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        j3 = len(lots_df[lots_df["stage"] == "J-3"])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🔴</div>
            <div class="kpi-label">Urgent</div>
            <div class="kpi-value">{j3}</div>
            <div class="kpi-meta">J-3 jours</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        j7 = len(lots_df[lots_df["stage"] == "J-7"])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🟠</div>
            <div class="kpi-label">Alerte</div>
            <div class="kpi-value">{j7}</div>
            <div class="kpi-meta">J-7 jours</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        j30 = len(lots_df[lots_df["stage"] == "J-30"])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🟡</div>
            <div class="kpi-label">Planifier</div>
            <div class="kpi-value">{j30}</div>
            <div class="kpi-meta">J-30 jours</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        qty = int(lots_df["quantity"].sum())
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📦</div>
            <div class="kpi-label">Quantité</div>
            <div class="kpi-value">{qty}</div>
            <div class="kpi-meta">unités</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# FILTERS
st.markdown("<div class='section-title'>🔍 Filtres & Recherche</div>", unsafe_allow_html=True)

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([2, 1, 1, 1])

with filter_col1:
    search = st.text_input("🔎 Rechercher", placeholder="Produit, lot, rayon...")

with filter_col2:
    urgency = st.selectbox("Urgence", ["Tous", "J-3", "J-7", "J-30", "OK"])

with filter_col3:
    if not lots_df.empty:
        locations = ["Tous"] + sorted(lots_df['location'].unique().tolist())
        location = st.selectbox("Rayon", locations)
    else:
        location = "Tous"

with filter_col4:
    if st.button("🔄 Réinitialiser", use_container_width=True):
        st.rerun()

if not lots_df.empty:
    filtered_df = filter_lots(lots_df, search, urgency, location)
else:
    filtered_df = pd.DataFrame()

# TABS
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Inventaire",
    "📊 Graphiques",
    "📧 Email",
    "📥 Export"
])

with tab1:
    st.markdown("<div class='section-title'>📦 Liste des Produits</div>", unsafe_allow_html=True)
    
    if not filtered_df.empty:
        st.success(f"✅ {len(filtered_df)} lot(s) correspondent")
        
        for _, row in filtered_df.iterrows():
            exp_date = pd.to_datetime(row['expiryDate']).date()
            urgency_class = get_urgency_class(row['stage'])
            
            st.markdown(f"""
            <div class="product-row {urgency_class}">
                <div class="product-info">
                    <div class="product-name">📦 {row['productId']} • Lot {row['lotNumber']}</div>
                    <div class="product-details">
                        <div class="detail-item">📊 {int(row['quantity'])} unités</div>
                        <div class="detail-item">📅 DLC: {exp_date.strftime('%d/%m/%Y')}</div>
                        <div class="detail-item">📍 {row['location']}</div>
                    </div>
                </div>
                <div class="status-badge">{row['daysLeft']} jours</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("❌ Aucun lot ne correspond")

with tab2:
    st.markdown("<div class='section-title'>📊 Visualisations</div>", unsafe_allow_html=True)
    
    if not filtered_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            stage_counts = filtered_df["stage"].value_counts()
            fig1 = go.Figure(data=[
                go.Bar(
                    x=stage_counts.index,
                    y=stage_counts.values,
                    marker=dict(
                        color=['#E30613', '#F39200', '#FFD700', '#00B050'],
                        line=dict(color='white', width=2)
                    ),
                    text=stage_counts.values,
                    textposition='outside',
                    textfont=dict(size=14, color='#1A1A1A')
                )
            ])
            fig1.update_layout(
                title="Distribution par Urgence",
                template="plotly_white",
                height=400,
                showlegend=False,
                font=dict(family="Segoe UI", size=12),
                plot_bgcolor='rgba(248,248,248,1)',
                paper_bgcolor='white'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = go.Figure(data=[
                go.Scatter(
                    x=filtered_df["daysLeft"],
                    y=filtered_df["quantity"],
                    mode='markers',
                    marker=dict(
                        size=filtered_df["quantity"] / 2.5,
                        color=filtered_df["daysLeft"],
                        colorscale=[[0, '#E30613'], [0.5, '#F39200'], [1, '#00B050']],
                        showscale=True,
                        line=dict(color='white', width=1)
                    ),
                    text=filtered_df["productId"],
                    hovertemplate='<b>%{text}</b><br>Jours: %{x}<br>Quantité: %{y}<extra></extra>'
                )
            ])
            fig2.update_layout(
                title="Urgence vs Quantité",
                xaxis_title="Jours restants",
                yaxis_title="Quantité (unités)",
                template="plotly_white",
                height=400,
                font=dict(family="Segoe UI", size=12),
                plot_bgcolor='rgba(248,248,248,1)',
                paper_bgcolor='white'
            )
            st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown("<div class='section-title'>📧 Envoyer Rapport Email</div>", unsafe_allow_html=True)
    
    if not lots_df.empty:
        st.info(f"📊 {len(lots_df[lots_df['stage'] == 'J-3'])} urgents | {len(lots_df)} lots total")
    
    if st.button("📬 Envoyer le rapport", use_container_width=True):
        with st.spinner("Envoi..."):
            try:
                html = f"""<html><body style="font-family: 'Segoe UI', Arial; background: #F5F5F5; padding: 20px;">
                <div style="max-width: 600px; background: white; border-radius: 16px; padding: 40px; margin: 0 auto; box-shadow: 0 8px 24px rgba(0,0,0,0.12);">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #E30613; font-size: 32px; margin: 0 0 8px 0;">🧊 SmartExpiry Pro</h1>
                        <p style="color: #666; font-size: 14px;">Rapport - {datetime.now(PARIS).strftime('%d %B %Y à %H:%M')}</p>
                    </div>
                    <hr style="border: none; border-top: 2px solid #E5E5E5; margin: 30px 0;">
                    <div style="background: #F8F8F8; padding: 20px; border-radius: 12px; margin: 20px 0;">
                        <p style="margin: 10px 0;"><strong>🏪 Magasin:</strong> {store_id}</p>
                        <p style="margin: 10px 0;"><strong>🔴 Lots urgents (J-3):</strong> {len(lots_df[lots_df['stage'] == 'J-3'])}</p>
                        <p style="margin: 10px 0;"><strong>🟠 Alertes (J-7):</strong> {len(lots_df[lots_df['stage'] == 'J-7'])}</p>
                        <p style="margin: 10px 0;"><strong>🟡 À planifier (J-30):</strong> {len(lots_df[lots_df['stage'] == 'J-30'])}</p>
                        <p style="margin: 10px 0;"><strong>📦 Quantité totale:</strong> {int(lots_df['quantity'].sum())} unités</p>
                    </div>
                </div>
                </body></html>"""
                
                msg = MIMEMultipart()
                msg["Subject"] = f"🧊 SmartExpiry Pro - {store_id}"
                msg["From"] = st.secrets.email.get("from", "nfindaroger@gmail.com")
                msg["To"] = st.secrets.email.get("to", "timotonou@yahoo.com")
                msg.attach(MIMEText(html, "html"))
                
                with smtplib.SMTP(st.secrets.email.host, int(st.secrets.email.port)) as server:
                    server.starttls()
                    server.login(st.secrets.email.username, st.secrets.email.password)
                    server.sendmail(msg["From"], [msg["To"]], msg.as_string())
                
                st.success("✅ Email envoyé avec succès !")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

with tab4:
    st.markdown("<div class='section-title'>📥 Exporter Données</div>", unsafe_allow_html=True)
    
    if st.button("⬇️ Télécharger CSV", use_container_width=True):
        if not filtered_df.empty:
            csv = "PRODUIT,LOT,QUANTITÉ,DLC,JOURS,RAYON,URGENCE\n"
            for _, row in filtered_df.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date().strftime('%d/%m/%Y')
                csv += f"{row['productId']},{row['lotNumber']},{int(row['quantity'])},{exp_date},{int(row['daysLeft'])},{row['location']},{row['stage']}\n"
            
            st.download_button(
                label="📊 Télécharger",
                data=csv,
                file_name=f"smartexpiry_{store_id}_{datetime.now(PARIS).strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.success(f"✅ {len(filtered_df)} lots prêts à télécharger")

st.divider()
st.caption(f"🧊 SmartExpiry Pro • {datetime.now(PARIS).strftime('%d/%m/%Y %H:%M')} • {store_id}")
