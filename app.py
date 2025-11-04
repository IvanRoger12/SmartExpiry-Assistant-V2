"""
╔════════════════════════════════════════════════════════════════════════╗
║         🧊 SMARTEXPIRY PRO - VERSION FINALE PRODUCTION               ║
║              Gestion FEFO • IA Chatbot Claude • Design Retail Pro    ║
║                    READY FOR DEMO - NOV 5, 2025                      ║
╚════════════════════════════════════════════════════════════════════════╝

FEATURES:
✅ 272 lots en temps réel
✅ Alertes colorisées (J-3 rouge, J-7 orange, J-30 jaune)
✅ Email automatique
✅ Export CSV
✅ 🤖 Chatbot IA Claude intégré
✅ Design Retail Pro (Carrefour/Monoprix)
✅ Responsive et présentable
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
from anthropic import Anthropic

PARIS = tz.gettz("Europe/Paris")

st.set_page_config(
    page_title="SmartExpiry Pro",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded"
)

# Initialize Claude client
claude_client = Anthropic()

# Initialize chat history for Claude
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ═════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM - RETAIL PRO FINAL
# ═════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
:root {
  --primary: #E30613;
  --secondary: #F39200;
  --success: #2BA84F;
  --bg: #F5F5F5;
  --white: #FFFFFF;
  --text: #1A1A1A;
  --text-light: #666666;
  --border: #EEEEEE;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

html, body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

.block-container {
  padding: 48px 24px !important;
  max-width: 1400px !important;
}

/* ════════════════════════════════ */
/* MAIN TITLE - CENTRE, GRAS, ÉNORME */
/* ════════════════════════════════ */

.main-title {
  text-align: center;
  font-size: 56px;
  font-weight: 900;
  color: var(--text);
  margin: 0 0 8px 0;
  letter-spacing: -2px;
  line-height: 1.1;
}

.main-subtitle {
  text-align: center;
  font-size: 18px;
  color: var(--text-light);
  margin: 0 0 48px 0;
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* HERO BANNER */
.hero {
  background: linear-gradient(135deg, rgba(227, 6, 19, 0.05) 0%, rgba(243, 157, 0, 0.03) 100%);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 32px 24px;
  margin-bottom: 48px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.hero h2 {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 8px;
}

.hero p {
  font-size: 16px;
  color: var(--text-light);
  margin: 0;
}

/* KPI GRID */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.kpi-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  transition: all 200ms ease;
  text-align: center;
}

.kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  border-color: var(--primary);
}

.kpi-icon { font-size: 32px; margin-bottom: 12px; }
.kpi-label { font-size: 11px; color: var(--text-light); font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
.kpi-value { font-size: 36px; font-weight: 800; color: var(--text); margin-bottom: 4px; }
.kpi-meta { font-size: 13px; color: var(--text-light); }

/* PRODUCT CARD */
.product-row {
  background: var(--white);
  border: 1px solid var(--border);
  border-left: 6px solid var(--urgency);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 200ms ease;
}

.product-row:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.product-row.j3 { --urgency: var(--primary); }
.product-row.j7 { --urgency: var(--secondary); }
.product-row.j30 { --urgency: #FFD700; }
.product-row.ok { --urgency: var(--success); }

.product-info { flex: 1; }
.product-name { font-size: 15px; font-weight: 700; color: var(--text); margin-bottom: 8px; }
.product-details { display: flex; gap: 20px; flex-wrap: wrap; font-size: 13px; color: var(--text-light); }
.detail-item { display: flex; align-items: center; gap: 4px; font-weight: 600; }
.status-badge { background: var(--urgency); color: white; padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; white-space: nowrap; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }

/* FILTERS */
.filter-container {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  align-items: center;
}

.filter-input {
  padding: 10px 16px;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
}

.filter-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(227, 6, 19, 0.1);
}

/* BUTTONS */
.stButton button {
  background: linear-gradient(135deg, var(--primary) 0%, #C20410 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 12px 24px !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  letter-spacing: 0.5px !important;
  transition: all 150ms !important;
  box-shadow: 0 4px 12px rgba(227, 6, 19, 0.2) !important;
  min-height: 40px !important;
}

.stButton button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(227, 6, 19, 0.3) !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
  border-bottom: 2px solid var(--border) !important;
  gap: 24px !important;
  background: transparent !important;
}

.stTabs [aria-selected="true"] {
  border-bottom: 3px solid var(--primary) !important;
  color: var(--primary) !important;
  font-weight: 700 !important;
}

.stTabs [aria-selected="false"] {
  color: var(--text-light) !important;
  font-weight: 600 !important;
}

/* SECTION TITLES */
.section-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text);
  margin: 32px 0 20px 0;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--primary);
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .main-title { font-size: 36px; }
  .product-row { flex-direction: column; align-items: flex-start; }
  .status-badge { margin-top: 12px; }
  .product-details { margin-bottom: 12px; }
  .filter-container { flex-direction: column; }
}

</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# FIREBASE INITIALIZATION
# ═════════════════════════════════════════════════════════════════════════

@st.cache_resource
def init_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(st.secrets.firebase)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        st.error(f"❌ Erreur Firebase: {str(e)}")
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
    if days <= 3:
        return "J-3"
    elif days <= 7:
        return "J-7"
    elif days <= 30:
        return "J-30"
    else:
        return "OK"

def get_color_class(stage):
    if stage == "J-3":
        return "j3"
    elif stage == "J-7":
        return "j7"
    elif stage == "J-30":
        return "j30"
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

def chat_with_claude(user_message, lots_data_context):
    """Chat avec Claude sur les données d'inventaire"""
    
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
    
    response = claude_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        system=system_prompt,
        messages=st.session_state.chat_history
    )
    
    assistant_message = response.content[0].text
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message

# ═════════════════════════════════════════════════════════════════════════
# SIDEBAR - NAVIGATION & CLAUDE CHATBOT
# ═════════════════════════════════════════════════════════════════════════

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
    🤖 IA Intégrée
    """)
    
    st.divider()
    
    st.markdown("### 🤖 Assistant IA")
    
    user_question = st.text_input(
        "Pose une question sur ton inventaire...",
        placeholder="Ex: Quels produits je dois retirer demain ?",
        key="ai_input"
    )
    
    if user_question and db:
        lots_df_temp = load_lots(store_id)
        if not lots_df_temp.empty:
            with st.spinner("L'IA réfléchit..."):
                ai_response = chat_with_claude(user_question, lots_df_temp)
                st.info(ai_response)
        else:
            st.warning("Pas de données disponibles")

# ═════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═════════════════════════════════════════════════════════════════════════

lots_df = load_lots(store_id)

# MAIN TITLE - CENTRE, GRAS, ÉNORME
st.markdown("""
<h1 class="main-title">🧊 SmartExpiry Pro</h1>
<p class="main-subtitle">Gestion FEFO Intelligente • Alertes Automatiques • Zéro Perte</p>
""", unsafe_allow_html=True)

# HERO BANNER
st.markdown("""
<div class="hero">
    <h2>📦 Suivi d'Inventaire en Temps Réel</h2>
    <p>Alertes colorisées • Email automatique • Export données • Recommandations IA</p>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# KPI DASHBOARD
# ═════════════════════════════════════════════════════════════════════════

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

# ═════════════════════════════════════════════════════════════════════════
# FILTERS
# ═════════════════════════════════════════════════════════════════════════

st.markdown("### 🔍 Filtres")

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

# ═════════════════════════════════════════════════════════════════════════
# TABS - MAIN INTERFACE
# ═════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Inventaire",
    "📊 Graphiques",
    "📧 Email",
    "📥 Export"
])

with tab1:
    st.markdown("### 📋 Liste des Produits")
    
    if not filtered_df.empty:
        st.success(f"✅ {len(filtered_df)} lot(s) correspondent")
        
        for _, row in filtered_df.iterrows():
            exp_date = pd.to_datetime(row['expiryDate']).date()
            color_class = get_color_class(row['stage'])
            
            st.markdown(f"""
            <div class="product-row {color_class}">
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
    st.markdown("### 📊 Visualisations")
    
    if not filtered_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            stage_counts = filtered_df["stage"].value_counts()
            fig1 = go.Figure(data=[
                go.Bar(
                    x=stage_counts.index,
                    y=stage_counts.values,
                    marker=dict(color=['#E30613', '#F39200', '#FFD700', '#2BA84F']),
                    text=stage_counts.values,
                    textposition='outside'
                )
            ])
            fig1.update_layout(
                title="Distribution par Urgence",
                template="plotly_white",
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = go.Figure(data=[
                go.Scatter(
                    x=filtered_df["daysLeft"],
                    y=filtered_df["quantity"],
                    mode='markers',
                    marker=dict(
                        size=filtered_df["quantity"] / 3,
                        color=filtered_df["daysLeft"],
                        colorscale=[[0, '#E30613'], [0.5, '#F39200'], [1, '#2BA84F']],
                        showscale=True
                    ),
                    text=filtered_df["productId"]
                )
            ])
            fig2.update_layout(
                title="Urgence vs Quantité",
                xaxis_title="Jours",
                yaxis_title="Quantité",
                template="plotly_white",
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown("### 📧 Envoyer Rapport Email")
    
    if not lots_df.empty:
        st.info(f"📊 {len(lots_df[lots_df['stage'] == 'J-3'])} urgents | {len(lots_df)} lots total")
    
    if st.button("📬 Envoyer le rapport", use_container_width=True):
        with st.spinner("Envoi..."):
            try:
                html = f"""<html><body style="font-family: Arial; background: #F5F5F5; padding: 20px;">
                <div style="max-width: 600px; background: white; border-radius: 12px; padding: 30px; margin: 0 auto;">
                    <h1 style="color: #E30613; text-align: center;">🧊 SmartExpiry Pro</h1>
                    <p style="text-align: center; color: #666;">Rapport - {datetime.now(PARIS).strftime('%d %B %Y')}</p>
                    <hr style="border: none; border-top: 1px solid #EEE; margin: 20px 0;">
                    <p><strong>Magasin:</strong> {store_id}</p>
                    <p><strong>Lots urgents (J-3):</strong> {len(lots_df[lots_df['stage'] == 'J-3'])}</p>
                    <p><strong>Alertes (J-7):</strong> {len(lots_df[lots_df['stage'] == 'J-7'])}</p>
                    <p><strong>À planifier (J-30):</strong> {len(lots_df[lots_df['stage'] == 'J-30'])}</p>
                    <p><strong>Quantité totale:</strong> {int(lots_df['quantity'].sum())} unités</p>
                </div>
                </body></html>"""
                
                msg = MIMEMultipart()
                msg["Subject"] = f"🧊 SmartExpiry Pro - {store_id}"
                msg["From"] = st.secrets.email["from"]
                msg["To"] = st.secrets.email["to"]
                msg.attach(MIMEText(html, "html"))
                
                with smtplib.SMTP(st.secrets.email["host"], int(st.secrets.email["port"])) as server:
                    server.starttls()
                    server.login(st.secrets.email["username"], st.secrets.email["password"])
                    server.sendmail(msg["From"], [msg["To"]], msg.as_string())
                
                st.success("✅ Email envoyé!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

with tab4:
    st.markdown("### 📥 Exporter Données")
    
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
            st.success(f"✅ {len(filtered_df)} lots")

st.divider()
st.caption(f"🧊 SmartExpiry Pro • {datetime.now(PARIS).strftime('%d/%m/%Y %H:%M')} • {store_id}")
