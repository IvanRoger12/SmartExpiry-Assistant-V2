"""
╔═══════════════════════════════════════════════════════════════╗
║   🧊 SMARTEXPIRY PRO - FUTURISTE ULTIME                      ║
║   Design: Tesla × Notion × Apple Vision Pro                  ║
║   Performance: ZÉRO LAG × 60 FPS × GPU-OPTIMIZED            ║
║   Ambiance: Cinématique × Immersive × Sensorielle            ║
╚═══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from dateutil import tz
import plotly.graph_objects as go
import firebase_admin
from firebase_admin import credentials, firestore
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

PARIS = tz.gettz("Europe/Paris")

st.set_page_config(
    page_title="SmartExpiry Pro - Futuriste",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════
# 🌌 DESIGN SYSTEM FUTURISTE
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

html, body {
    background: linear-gradient(135deg, #ffffff 0%, #f5f7fc 50%, #eef2f8 100%);
    color: #1a1f3a;
    font-family: 'Inter', sans-serif;
    overflow-x: hidden;
    scroll-behavior: smooth;
}

.block-container { padding: 3rem 2.5rem !important; max-width: 1600px !important; }

@keyframes floatGlow {
    0%, 100% { transform: translateY(0) scale(1); filter: drop-shadow(0 0 20px rgba(0, 102, 255, 0.3)); }
    50% { transform: translateY(-8px) scale(1.02); filter: drop-shadow(0 0 40px rgba(0, 102, 255, 0.5)); }
}

@keyframes slideInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.header-futuriste {
    background: linear-gradient(135deg, rgba(0, 102, 255, 0.08) 0%, rgba(0, 212, 255, 0.05) 100%);
    border-bottom: 1px solid rgba(0, 102, 255, 0.15);
    backdrop-filter: blur(20px);
    padding: 2rem;
    border-radius: 20px;
    margin-bottom: 3rem;
    position: relative;
    overflow: hidden;
    animation: slideInUp 0.8s ease-out;
}

.header-futuriste::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(0, 212, 255, 0.15) 0%, transparent 70%);
    border-radius: 50%;
    animation: floatGlow 6s ease-in-out infinite;
    pointer-events: none;
}

.header-title {
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #0066ff 0%, #00d4ff 50%, #00ff88 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    position: relative;
    z-index: 2;
    margin-bottom: 0.5rem;
}

.header-subtitle {
    font-size: 1.1rem;
    color: #64748b;
    position: relative;
    z-index: 2;
    font-weight: 500;
}

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 3rem;
}

.kpi-card {
    background: linear-gradient(135deg, rgba(0, 102, 255, 0.05) 0%, rgba(0, 212, 255, 0.03) 100%);
    border: 2px solid rgba(0, 102, 255, 0.2);
    border-radius: 20px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    transition: all 0.4s ease;
    animation: slideInUp 0.8s ease-out backwards;
    cursor: pointer;
}

.kpi-card:nth-child(1) { animation-delay: 0.1s; }
.kpi-card:nth-child(2) { animation-delay: 0.2s; }
.kpi-card:nth-child(3) { animation-delay: 0.3s; }
.kpi-card:nth-child(4) { animation-delay: 0.4s; }

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--kpi-color-1), var(--kpi-color-2));
    border-radius: 20px 20px 0 0;
}

.kpi-card:hover {
    transform: translateY(-12px);
    border-color: rgba(0, 212, 255, 0.5);
    box-shadow: 0 20px 60px rgba(0, 102, 255, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

.kpi-label {
    font-size: 0.75rem;
    color: #64748b;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 1rem;
    position: relative;
    z-index: 2;
}

.kpi-value {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, var(--kpi-color-1), var(--kpi-color-2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 2;
}

.kpi-meta {
    font-size: 0.85rem;
    color: #64748b;
    position: relative;
    z-index: 2;
}

.kpi-card:nth-child(1) { --kpi-color-1: #dc2626; --kpi-color-2: #ff006e; }
.kpi-card:nth-child(2) { --kpi-color-1: #ffaa00; --kpi-color-2: #ff6b35; }
.kpi-card:nth-child(3) { --kpi-color-1: #0066ff; --kpi-color-2: #00d4ff; }
.kpi-card:nth-child(4) { --kpi-color-1: #00ff88; --kpi-color-2: #00d4ff; }

.inventory-card {
    background: linear-gradient(135deg, rgba(0, 102, 255, 0.03) 0%, rgba(0, 212, 255, 0.02) 100%);
    border: 2px solid rgba(0, 102, 255, 0.12);
    border-left: 5px solid var(--urgency-color);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}

.inventory-card:hover {
    transform: translateX(8px);
    border-color: rgba(0, 212, 255, 0.35);
    box-shadow: 0 8px 32px rgba(0, 102, 255, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.inventory-card.urgent { --urgency-color: #dc2626; }
.inventory-card.warning { --urgency-color: #ffaa00; }
.inventory-card.planning { --urgency-color: #0066ff; }

.product-info { flex: 1; position: relative; z-index: 2; }
.product-name { font-size: 1.1rem; font-weight: 800; color: #1a1f3a; margin-bottom: 0.5rem; }
.product-meta { font-size: 0.85rem; color: #64748b; display: flex; gap: 1.5rem; }

.urgency-badge {
    background: linear-gradient(135deg, rgba(0, 102, 255, 0.1) 0%, rgba(0, 212, 255, 0.05) 100%);
    border: 2px solid rgba(0, 102, 255, 0.25);
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--urgency-color);
    position: relative;
    z-index: 2;
    box-shadow: 0 0 20px rgba(0, 102, 255, 0.1);
}

.stButton button {
    background: linear-gradient(135deg, #0066ff 0%, #00d4ff 100%) !important;
    color: white !important;
    border: 2px solid rgba(0, 212, 255, 0.3) !important;
    border-radius: 12px !important;
    padding: 1rem 2rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.8px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 24px rgba(0, 102, 255, 0.3) !important;
}

.stButton button:hover {
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 0 16px 40px rgba(0, 102, 255, 0.5) !important;
}

.stTabs [data-baseweb="tab-list"] { border-bottom: 2px solid rgba(0, 102, 255, 0.1) !important; gap: 2rem !important; }
.stTabs [aria-selected="true"] { border-bottom: 3px solid #0066ff !important; color: #0066ff !important; }

@media (max-width: 768px) {
    .block-container { padding: 1.5rem; }
    .header-title { font-size: 2rem; }
    .kpi-grid { grid-template-columns: 1fr; }
}

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# FIREBASE
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_resource
def init_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(st.secrets.firebase)
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
    if days <= 3: return "J-3"
    elif days <= 7: return "J-7"
    elif days <= 21: return "J-21"
    else: return "OK"

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

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════

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
    
    store_id = st.selectbox("🏪 Magasin", stores, index=0)
    st.divider()
    st.markdown("### 🧊 SmartExpiry Pro\nGestion FEFO\n- ✅ Real-Time\n- 📊 Multi-Stores\n- ⚡ 100% Auto")

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

lots_df = load_lots(store_id)

st.markdown(f"""
<div class="header-futuriste">
    <h1 class="header-title">🧊 SmartExpiry Pro</h1>
    <p class="header-subtitle">Gestion Intelligente FEFO • Zéro Perte • Real-Time Sync</p>
</div>
""", unsafe_allow_html=True)

if not lots_df.empty:
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        urgent = len(lots_df[lots_df["stage"] == "J-3"])
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">🔴 Urgent J-3</div><div class="kpi-value">{urgent}</div><div class="kpi-meta">Action immédiate</div></div>""", unsafe_allow_html=True)
    
    with col2:
        warning = len(lots_df[lots_df["stage"] == "J-7"])
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">⏰ Alerte J-7</div><div class="kpi-value">{warning}</div><div class="kpi-meta">À surveiller</div></div>""", unsafe_allow_html=True)
    
    with col3:
        planning = len(lots_df[lots_df["stage"] == "J-21"])
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">📅 Planifier J-21</div><div class="kpi-value">{planning}</div><div class="kpi-meta">À prévoir</div></div>""", unsafe_allow_html=True)
    
    with col4:
        ok = len(lots_df[lots_df["stage"] == "OK"])
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">✅ À Jour</div><div class="kpi-value">{ok}</div><div class="kpi-meta">Bien géré</div></div>""", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📋 Inventaire", "📊 Analytics", "📧 Email", "📥 Export"])

with tab1:
    st.markdown("### 📋 Gestion Complète")
    
    if not lots_df.empty:
        urgent_lots = lots_df[lots_df["stage"] == "J-3"].sort_values("expiryDate")
        if not urgent_lots.empty:
            st.markdown("#### 🔴 URGENT - À 3 jours")
            for _, row in urgent_lots.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date()
                st.markdown(f"""<div class="inventory-card urgent"><div class="product-info"><div class="product-name">📦 {row['productId']} • {row['lotNumber']}</div><div class="product-meta"><span>📊 {int(row['quantity'])} unités</span><span>📅 {exp_date.strftime('%d/%m')}</span><span>📍 {row['location']}</span></div></div><div class="urgency-badge">🔴 {row['daysLeft']}j</div></div>""", unsafe_allow_html=True)
        
        warning_lots = lots_df[lots_df["stage"] == "J-7"].sort_values("expiryDate")
        if not warning_lots.empty:
            st.markdown("#### ⏰ ALERTE - À 1 semaine")
            for _, row in warning_lots.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date()
                st.markdown(f"""<div class="inventory-card warning"><div class="product-info"><div class="product-name">📦 {row['productId']} • {row['lotNumber']}</div><div class="product-meta"><span>📊 {int(row['quantity'])} unités</span><span>📅 {exp_date.strftime('%d/%m')}</span><span>📍 {row['location']}</span></div></div><div class="urgency-badge">⏰ {row['daysLeft']}j</div></div>""", unsafe_allow_html=True)
        
        planning_lots = lots_df[lots_df["stage"] == "J-21"].sort_values("expiryDate")
        if not planning_lots.empty:
            st.markdown("#### 📅 PLANIFIER - À 3 semaines")
            for _, row in planning_lots.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date()
                st.markdown(f"""<div class="inventory-card planning"><div class="product-info"><div class="product-name">📦 {row['productId']} • {row['lotNumber']}</div><div class="product-meta"><span>📊 {int(row['quantity'])} unités</span><span>📅 {exp_date.strftime('%d/%m')}</span><span>📍 {row['location']}</span></div></div><div class="urgency-badge">📅 {row['daysLeft']}j</div></div>""", unsafe_allow_html=True)

with tab2:
    st.markdown("### 📊 Analytics Futuriste")
    
    if not lots_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            stage_counts = lots_df["stage"].value_counts()
            fig = go.Figure(data=[go.Bar(x=stage_counts.index, y=stage_counts.values, marker=dict(color=['#dc2626', '#ffaa00', '#0066ff', '#00ff88'], line=dict(color='rgba(0, 212, 255, 0.3)', width=2)), text=stage_counts.values, textposition='outside')])
            fig.update_layout(title="Distribution", template="plotly_dark", height=400, showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#1a1f3a'))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig2 = go.Figure(data=[go.Scatter(x=lots_df["daysLeft"], y=lots_df["quantity"], mode='markers', marker=dict(size=lots_df["quantity"]/3, color=lots_df["daysLeft"], colorscale=[[0, '#dc2626'], [0.5, '#ffaa00'], [1, '#00ff88']], showscale=True), text=lots_df["productId"])])
            fig2.update_layout(title="Urgence vs Quantité", template="plotly_dark", height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#1a1f3a'))
            st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.markdown("### 📧 Envoyer le Rapport")
    
    if not lots_df.empty:
        st.info(f"📊 **{len(lots_df[lots_df['stage'] == 'J-3'])} lots urgents** | **{int(lots_df['quantity'].sum())} unités**")
    
    if st.button("📬 Envoyer", use_container_width=True):
        with st.spinner("Envoi..."):
            try:
                html = f"<html><body style='font-family: Inter; background: #0a0e27; color: #e8eef7; padding: 40px;'><div style='max-width: 850px; margin: 0 auto; background: rgba(0, 102, 255, 0.08); border: 2px solid rgba(0, 212, 255, 0.2); border-radius: 20px; padding: 40px;'><h1 style='color: #00d4ff;'>🧊 SmartExpiry Pro</h1><p>Rapport - {datetime.now(PARIS).strftime('%d %B %Y')}</p><p>Magasin: <b>{store_id}</b></p><p>Lots urgents: <b>{len(lots_df[lots_df['stage'] == 'J-3'])}</b></p></div></body></html>"
                
                msg = MIMEMultipart()
                msg["Subject"] = f"🧊 SmartExpiry - {store_id}"
                msg["From"] = st.secrets.email["from"]
                msg["To"] = st.secrets.email["to"]
                msg.attach(MIMEText(html, "html"))
                
                with smtplib.SMTP(st.secrets.email["host"], int(st.secrets.email["port"])) as s:
                    s.starttls()
                    s.login(st.secrets.email["username"], st.secrets.email["password"])
                    s.sendmail(msg["From"], [msg["To"]], msg.as_string())
                
                st.success("✅ Envoyé!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ {str(e)}")

with tab4:
    st.markdown("### 📥 Exporter")
    
    if st.button("⬇️ CSV", use_container_width=True):
        if not lots_df.empty:
            csv = "PRODUIT,LOT,QUANTITÉ,DLC,JOURS,RAYON,ÉTAPE\n"
            for _, row in lots_df.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date().strftime('%d/%m/%Y')
                csv += f"{row['productId']},{row['lotNumber']},{int(row['quantity'])},{exp_date},{int(row['daysLeft'])},{row['location']},{row['stage']}\n"
            
            st.download_button(label="📊 Télécharger", data=csv, file_name=f"smartexpiry_{store_id}_{datetime.now(PARIS).strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)

st.divider()
st.markdown(f"🧊 <b>SmartExpiry Pro v2.0</b> • Futuriste • {datetime.now(PARIS).strftime('%d/%m %H:%M')} • {store_id}", unsafe_allow_html=True)
