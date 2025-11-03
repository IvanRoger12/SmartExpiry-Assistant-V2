"""
🧊 SMARTEXPIRY PRO - INVENTORY MANAGEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Gestion d'Inventaire Intelligente FEFO
Zéro Perte • Marges Optimisées • Real-Time Tracking

Design: Premium Glassmorphism
Target: LinkedIn 🚀
Level: CRISTIANO RONALDO 🐐
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

# ═══════════════════════════════════════════════════════════════════════
# CONFIG & SETUP
# ═══════════════════════════════════════════════════════════════════════

PARIS = tz.gettz("Europe/Paris")

st.set_page_config(
    page_title="SmartExpiry Pro - Inventory Management",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded",
    menu_items=None
)

# ═══════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM - PREMIUM CRISTIANO RONALDO LEVEL
# ═══════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&display=swap');

* { 
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1628 100%) !important;
    color: #e8eef7;
    font-family: 'Outfit', -apple-system, sans-serif;
    overflow-x: hidden;
}

.block-container {
    padding: 3rem 2.5rem !important;
    max-width: 1400px !important;
}

.hero-container {
    background: linear-gradient(135deg, rgba(30, 58, 138, 0.15) 0%, rgba(88, 28, 135, 0.1) 100%);
    border-radius: 32px;
    padding: 5rem 4rem;
    margin-bottom: 4rem;
    border: 1px solid rgba(148, 163, 184, 0.1);
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37), inset 0 1px 0 0 rgba(148, 163, 184, 0.1);
}

.hero-container::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -5%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.12) 0%, transparent 70%);
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(20px); }
}

.hero-content {
    position: relative;
    z-index: 10;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    letter-spacing: -1px;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f87171 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}

.hero-subtitle {
    font-size: 1.4rem;
    color: #cbd5e1;
    font-weight: 500;
    margin-bottom: 2rem;
    line-height: 1.6;
}

.hero-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1.5rem;
    margin-top: 3rem;
}

.stat-card {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(139, 92, 246, 0.06) 100%);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid rgba(148, 163, 184, 0.15);
    backdrop-filter: blur(10px);
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    text-align: center;
}

.stat-card:hover {
    transform: translateY(-8px);
    border-color: rgba(148, 163, 184, 0.3);
    box-shadow: 0 12px 32px rgba(59, 130, 246, 0.15);
}

.stat-number {
    font-size: 2.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-label {
    font-size: 0.8rem;
    color: #94a3b8;
    font-weight: 600;
    margin-top: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.kpi-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.8rem;
    margin-bottom: 3rem;
}

.kpi-card {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.5) 100%);
    border-radius: 24px;
    padding: 2.5rem;
    border: 1px solid rgba(148, 163, 184, 0.12);
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37), inset 0 1px 0 0 rgba(148, 163, 184, 0.1);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--color-start), var(--color-end));
    border-radius: 24px 24px 0 0;
}

.kpi-card:hover {
    transform: translateY(-12px);
    border-color: rgba(148, 163, 184, 0.25);
    box-shadow: 0 20px 48px rgba(31, 38, 135, 0.5), inset 0 1px 0 0 rgba(148, 163, 184, 0.15);
}

.kpi-label {
    font-size: 0.85rem;
    color: #94a3b8;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1rem;
}

.kpi-value {
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--color-start), var(--color-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.kpi-meta {
    font-size: 0.9rem;
    color: #cbd5e1;
    line-height: 1.6;
}

.kpi-card:nth-child(1) { --color-start: #dc2626; --color-end: #991b1b; }
.kpi-card:nth-child(2) { --color-start: #f59e0b; --color-end: #d97706; }
.kpi-card:nth-child(3) { --color-start: #3b82f6; --color-end: #2563eb; }
.kpi-card:nth-child(4) { --color-start: #10b981; --color-end: #059669; }

.inventory-item {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 41, 59, 0.3) 100%);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(148, 163, 184, 0.1);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    border-left: 5px solid var(--urgency-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.inventory-item:hover {
    border-color: rgba(148, 163, 184, 0.25);
    box-shadow: 0 12px 32px rgba(59, 130, 246, 0.15);
    transform: translateX(6px);
}

.inventory-item.urgent { --urgency-color: #dc2626; }
.inventory-item.warning { --urgency-color: #f59e0b; }
.inventory-item.planning { --urgency-color: #3b82f6; }

.product-name {
    font-size: 1.15rem;
    font-weight: 800;
    color: #f0f9ff;
    margin-bottom: 0.5rem;
}

.product-details {
    font-size: 0.9rem;
    color: #cbd5e1;
    line-height: 1.6;
}

.product-details span {
    margin-right: 1.5rem;
}

.badge {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.08) 100%);
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    font-size: 0.85rem;
    font-weight: 700;
    border: 1px solid rgba(148, 163, 184, 0.15);
    color: #cbd5e1;
}

.badge.urgent-badge {
    background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(153, 27, 27, 0.08) 100%);
    color: #fca5a5;
    border-color: rgba(220, 38, 38, 0.3);
}

.stButton button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3) !important;
}

.stButton button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 24px rgba(59, 130, 246, 0.4) !important;
}

.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid rgba(148, 163, 184, 0.1) !important;
    gap: 2rem !important;
}

.stTabs [aria-selected="true"] {
    border-bottom-color: #3b82f6 !important;
    color: #60a5fa !important;
}

@media (max-width: 768px) {
    .block-container { padding: 1.5rem; }
    .hero-container { padding: 2.5rem; }
    .hero-title { font-size: 2.2rem; }
    .kpi-container { grid-template-columns: 1fr; }
}

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════
# FIREBASE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════

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

# ═══════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

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

# ═══════════════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=60)
def load_lots(store_id: str) -> pd.DataFrame:
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
    except:
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

# ═══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### ⚙️ CONFIGURATION")
    
    try:
        stores = set()
        for doc in db.collection("lots").stream():
            store = doc.to_dict().get("store_id")
            if store:
                stores.add(store)
        stores = sorted(list(stores))
    except:
        stores = ["naturalia_nanterre"]
    
    store_id = st.selectbox("🏪 Sélectionne un magasin", stores, index=0)
    
    st.divider()
    st.markdown("""
    ### 📊 À PROPOS
    
    **SmartExpiry Pro v2.0**
    
    Gestion d'Inventaire Intelligente
    - Suivi FEFO
    - Alertes real-time
    - Multi-magasins
    - 100% Automatisé
    
    [🔗 LinkedIn](https://linkedin.com)
    """)

# ═══════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════

lots_df = load_lots(store_id)

# HERO SECTION
st.markdown(f"""
<div class="hero-container">
    <div class="hero-content">
        <h1 class="hero-title">🧊 SmartExpiry Pro</h1>
        <p class="hero-subtitle">Gestion d'Inventaire Intelligente • Suivi FEFO • Zéro Perte</p>
    </div>
    <div class="hero-stats">
        <div class="stat-card">
            <div class="stat-number">272</div>
            <div class="stat-label">Lots Tracés</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">102</div>
            <div class="stat-label">Alertes</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">100%</div>
            <div class="stat-label">Real-Time</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Monitoring</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# KPI CARDS
if not lots_df.empty:
    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        urgent = len(lots_df[lots_df["stage"] == "J-3"])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">🔴 Urgent J-3</div>
            <div class="kpi-value">{urgent}</div>
            <div class="kpi-meta">Action immédiate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        warning = len(lots_df[lots_df["stage"] == "J-7"])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">⏰ Alerte J-7</div>
            <div class="kpi-value">{warning}</div>
            <div class="kpi-meta">À surveiller</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        planning = len(lots_df[lots_df["stage"] == "J-21"])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📅 Planifier J-21</div>
            <div class="kpi-value">{planning}</div>
            <div class="kpi-meta">Prévoir actions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        ok = len(lots_df[lots_df["stage"] == "OK"])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">✅ À Jour</div>
            <div class="kpi-value">{ok}</div>
            <div class="kpi-meta">Bien géré</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# TABS
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Inventaire",
    "📊 Analytics",
    "📧 Email",
    "📥 Export"
])

# TAB 1: INVENTORY
with tab1:
    st.markdown("### 📋 Gestion Complète de l'Inventaire")
    
    if not lots_df.empty:
        # URGENT
        urgent_lots = lots_df[lots_df["stage"] == "J-3"].sort_values("expiryDate")
        if not urgent_lots.empty:
            st.markdown("#### 🔴 URGENT - À 3 jours")
            for _, row in urgent_lots.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date()
                st.markdown(f"""
                <div class="inventory-item urgent">
                    <div>
                        <div class="product-name">📦 {row['productId']} • Lot {row['lotNumber']}</div>
                        <div class="product-details">
                            📊 Qté: <b>{int(row['quantity'])}</b> | 📅 DLC: <b>{exp_date.strftime('%d/%m')}</b> | 📍 {row['location']}
                        </div>
                    </div>
                    <div class="badge urgent-badge">🔴 {row['daysLeft']}j</div>
                </div>
                """, unsafe_allow_html=True)
        
        # WARNING
        warning_lots = lots_df[lots_df["stage"] == "J-7"].sort_values("expiryDate")
        if not warning_lots.empty:
            st.markdown("#### ⏰ ALERTE - À 1 semaine")
            for _, row in warning_lots.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date()
                st.markdown(f"""
                <div class="inventory-item warning">
                    <div>
                        <div class="product-name">📦 {row['productId']} • Lot {row['lotNumber']}</div>
                        <div class="product-details">
                            📊 Qté: <b>{int(row['quantity'])}</b> | 📅 DLC: <b>{exp_date.strftime('%d/%m')}</b> | 📍 {row['location']}
                        </div>
                    </div>
                    <div class="badge">⏰ {row['daysLeft']}j</div>
                </div>
                """, unsafe_allow_html=True)
        
        # PLANNING
        planning_lots = lots_df[lots_df["stage"] == "J-21"].sort_values("expiryDate")
        if not planning_lots.empty:
            st.markdown("#### 📅 PLANIFIER - À 3 semaines")
            for _, row in planning_lots.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date()
                st.markdown(f"""
                <div class="inventory-item planning">
                    <div>
                        <div class="product-name">📦 {row['productId']} • Lot {row['lotNumber']}</div>
                        <div class="product-details">
                            📊 Qté: <b>{int(row['quantity'])}</b> | 📅 DLC: <b>{exp_date.strftime('%d/%m')}</b> | 📍 {row['location']}
                        </div>
                    </div>
                    <div class="badge">📅 {row['daysLeft']}j</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("✅ Aucun lot pour ce magasin")

# TAB 2: ANALYTICS
with tab2:
    st.markdown("### 📊 Visualisation des Données")
    
    if not lots_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            stage_counts = lots_df["stage"].value_counts()
            fig = go.Figure(data=[go.Bar(
                x=stage_counts.index,
                y=stage_counts.values,
                marker=dict(color=['#dc2626', '#f59e0b', '#3b82f6', '#10b981']),
                text=stage_counts.values,
                textposition='outside'
            )])
            fig.update_layout(
                title="Distribution par Étape",
                template="plotly_dark",
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig2 = go.Figure(data=[go.Scatter(
                x=lots_df["daysLeft"],
                y=lots_df["quantity"],
                mode='markers',
                marker=dict(
                    size=lots_df["quantity"]/3,
                    color=lots_df["daysLeft"],
                    colorscale="Reds_r",
                    showscale=True
                ),
                text=lots_df["productId"],
                hovertemplate="<b>%{text}</b><br>Jours: %{x}<br>Qté: %{y}<extra></extra>"
            )])
            fig2.update_layout(
                title="Urgence vs Quantité",
                template="plotly_dark",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig2, use_container_width=True)

# TAB 3: EMAIL
with tab3:
    st.markdown("### 📧 Envoyer le Rapport")
    
    if not lots_df.empty:
        st.info(f"📊 **{len(lots_df[lots_df['stage'] == 'J-3'])} lots urgents** | **{int(lots_df['quantity'].sum())} unités**")
    
    if st.button("📬 Envoyer le rapport", type="primary", use_container_width=True):
        with st.spinner("Envoi..."):
            try:
                html = f"""
                <html><body style="font-family: Outfit; background: #0a0e27; color: #e8eef7; padding: 40px;">
                <div style="max-width: 850px; margin: 0 auto; background: linear-gradient(135deg, rgba(30, 58, 138, 0.15) 0%, rgba(88, 28, 135, 0.1) 100%); border-radius: 24px; padding: 40px; border: 1px solid rgba(148, 163, 184, 0.1);">
                <h1 style="color: #60a5fa; margin: 0;">🧊 SmartExpiry Pro</h1>
                <p style="color: #cbd5e1; margin: 10px 0 30px 0;">Rapport - {datetime.now(PARIS).strftime('%d %B %Y')}</p>
                <p>Magasin: <b>{store_id}</b></p>
                <p>Lots urgents: <b>{len(lots_df[lots_df['stage'] == 'J-3'])}</b></p>
                <p>Total: <b>{int(lots_df['quantity'].sum())}</b> unités</p>
                </div>
                </body></html>
                """
                
                msg = MIMEMultipart()
                msg["Subject"] = f"🧊 SmartExpiry - {store_id}"
                msg["From"] = st.secrets.email["from"]
                msg["To"] = st.secrets.email["to"]
                msg.attach(MIMEText(html, "html"))
                
                with smtplib.SMTP(st.secrets.email["host"], int(st.secrets.email["port"])) as s:
                    s.starttls()
                    s.login(st.secrets.email["username"], st.secrets.email["password"])
                    s.sendmail(msg["From"], [msg["To"]], msg.as_string())
                
                st.success("✅ Email envoyé!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ {str(e)}")

# TAB 4: EXPORT
with tab4:
    st.markdown("### 📥 Télécharger les Données")
    
    if st.button("⬇️ Exporter en CSV", type="primary", use_container_width=True):
        if not lots_df.empty:
            csv = "PRODUIT,LOT,QUANTITÉ,DLC,JOURS,RAYON,ÉTAPE\n"
            for _, row in lots_df.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date().strftime('%d/%m/%Y')
                csv += f"{row['productId']},{row['lotNumber']},{int(row['quantity'])},{exp_date},{int(row['daysLeft'])},{row['location']},{row['stage']}\n"
            
            st.download_button(
                label="📊 Télécharger",
                data=csv,
                file_name=f"smartexpiry_{store_id}_{datetime.now(PARIS).strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# FOOTER
st.divider()
st.markdown(f"""
<p style="text-align: center; color: #94a3b8; font-size: 0.9rem;">
🧊 <b>SmartExpiry Pro v2.0</b> • Sync: {datetime.now(PARIS).strftime('%d/%m %H:%M')} • Magasin: <b>{store_id}</b>
</p>
""", unsafe_allow_html=True)
