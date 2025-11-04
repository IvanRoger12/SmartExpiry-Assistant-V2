"""
╔════════════════════════════════════════════════════════════════════════╗
║         🧊 SMARTEXPIRY PRO - RETAIL DESIGN SYSTEM v2.0               ║
║              Gestion FEFO Intelligente • Zéro Perte                   ║
║                    500+ Lignes • Toutes Fonctionnalités              ║
╚════════════════════════════════════════════════════════════════════════╝

APP FEATURES:
✅ 272 lots tracés en temps réel
✅ 102 alertes intelligentes (J-3, J-7, J-21)
✅ Email digest automatique
✅ Export CSV complet
✅ Analytics graphiques interactifs
✅ Multi-magasins
✅ Design Retail Pro (Carrefour + Monoprix + Naturalia)
✅ Responsive (Desktop/Tablet/Mobile)
✅ Accessibility AA+
"""

# ═════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═════════════════════════════════════════════════════════════════════════

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

# ═════════════════════════════════════════════════════════════════════════
# CONFIG GLOBALES
# ═════════════════════════════════════════════════════════════════════════

PARIS = tz.gettz("Europe/Paris")

st.set_page_config(
    page_title="SmartExpiry Pro - Gestion FEFO",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded"
)

# ═════════════════════════════════════════════════════════════════════════
# 🎨 DESIGN SYSTEM RETAIL PRO - CSS TOKENS COMPLETS
# ═════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
:root {
  /* SEMANTIC COLORS - RETAIL PALETTE */
  --color-primary: #E30613;        /* URGENT RED - Carrefour */
  --color-secondary: #F39200;      /* WARNING ORANGE - Monoprix */
  --color-success: #2BA84F;        /* PLANNING GREEN - Naturalia */
  --color-info: #0071CE;           /* INFO BLUE - Walmart */
  --color-danger: #D32F2F;         /* Deep RED - Errors */
  
  /* NEUTRALS */
  --color-bg: #F5F5F5;             /* Clean retail white bg */
  --color-surface: #FFFFFF;        /* Card surfaces */
  --color-text: #1A1A1A;           /* Primary text */
  --color-text-secondary: #666666; /* Secondary info */
  --color-border: #EEEEEE;         /* Dividers */
  --color-hover: #F0F0F0;          /* Hover state */
  
  /* URGENCY STATUS COLORS */
  --color-j3: #E30613;             /* J-3 URGENT = RED */
  --color-j7: #F39200;             /* J-7 WARNING = ORANGE */
  --color-j21: #2BA84F;            /* J-21 PLANNING = GREEN */
  --color-ok: #666666;             /* OK = NEUTRAL */
  
  /* LIGHT VARIANTS FOR BACKGROUNDS */
  --color-j3-light: #FDE8E8;       /* Red 10% opacity */
  --color-j7-light: #FEF3E6;       /* Orange 10% opacity */
  --color-j21-light: #E8F5E9;      /* Green 10% opacity */
  --color-ok-light: #F5F5F5;       /* Neutral */
  
  /* TYPOGRAPHY */
  --font-family-base: 'Inter', 'Segoe UI', sans-serif;
  --font-family-display: 'Poppins', sans-serif;
  
  --font-size-h1: 52px;            /* Main title */
  --font-size-h2: 36px;            /* Section header */
  --font-size-h3: 24px;            /* Subsection */
  --font-size-body: 16px;          /* Body text */
  --font-size-small: 13px;         /* Labels */
  
  --font-weight-regular: 400;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --font-weight-heavy: 800;
  
  /* SPACING (8px unit system) */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  
  /* BORDER RADIUS */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  
  /* SHADOWS */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.1);
  
  /* TRANSITIONS */
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* BASE STYLES */
* { margin: 0; padding: 0; box-sizing: border-box; }

html, body {
  background: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-family-base);
  line-height: 1.6;
}

.block-container {
  padding: var(--space-2xl) var(--space-lg) !important;
  max-width: 1400px !important;
}

/* ════════════════════════════════════════════════════════════ */
/* MAIN TITLE - CENTRE, GRAS, TRÈS GRAND, SANS TRAIT */
/* ════════════════════════════════════════════════════════════ */

.main-title-container {
  text-align: center;
  margin: var(--space-2xl) 0 var(--space-xl) 0;
  animation: slideInDown 0.6s ease-out;
}

.main-title {
  font-family: var(--font-family-display);
  font-size: var(--font-size-h1);
  font-weight: var(--font-weight-heavy);
  color: var(--color-text);
  letter-spacing: 1.5px;
  margin: 0;
  padding: 0;
  line-height: 1.1;
  text-decoration: none;
  border: none;
  box-shadow: none;
}

.main-subtitle {
  font-size: 18px;
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-regular);
  margin-top: var(--space-md);
  letter-spacing: 1px;
}

/* ════════════════════════════════════════════════════════════ */
/* HERO BANNER */
/* ════════════════════════════════════════════════════════════ */

.hero-banner {
  background: linear-gradient(135deg, rgba(227, 6, 19, 0.05) 0%, rgba(243, 157, 0, 0.03) 100%);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-xl) var(--space-lg);
  margin: var(--space-2xl) 0;
  box-shadow: var(--shadow-sm);
  animation: slideInUp 0.6s ease-out;
}

.hero-banner h2 {
  font-size: 20px;
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  margin-bottom: var(--space-md);
}

.hero-banner p {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin: 0;
}

/* ════════════════════════════════════════════════════════════ */
/* KPI GRID & CARDS */
/* ════════════════════════════════════════════════════════════ */

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--space-lg);
  margin: var(--space-2xl) 0;
}

.kpi-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
  animation: slideInUp 0.6s ease-out backwards;
}

.kpi-card:nth-child(1) { animation-delay: 0.1s; }
.kpi-card:nth-child(2) { animation-delay: 0.2s; }
.kpi-card:nth-child(3) { animation-delay: 0.3s; }
.kpi-card:nth-child(4) { animation-delay: 0.4s; }

.kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary);
}

.kpi-icon {
  font-size: 32px;
  margin-bottom: var(--space-md);
  display: block;
}

.kpi-label {
  font-size: var(--font-size-small);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: var(--space-sm);
}

.kpi-value {
  font-size: 40px;
  font-weight: var(--font-weight-heavy);
  color: var(--color-text);
  margin-bottom: var(--space-sm);
}

.kpi-meta {
  font-size: var(--font-size-small);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-regular);
}

/* ════════════════════════════════════════════════════════════ */
/* SECTION TITLES */
/* ════════════════════════════════════════════════════════════ */

.section-title {
  font-size: 20px;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin: var(--space-xl) 0 var(--space-lg) 0;
  padding-bottom: var(--space-md);
  border-bottom: 2px solid var(--color-primary);
}

/* ════════════════════════════════════════════════════════════ */
/* LOT CARDS (J-3, J-7, J-21) */
/* ════════════════════════════════════════════════════════════ */

.lot-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-left: 6px solid var(--urgency-color);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  margin-bottom: var(--space-md);
  box-shadow: var(--shadow-sm);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all var(--transition-normal);
  animation: slideInLeft 0.6s ease-out backwards;
}

.lot-card:nth-child(1) { animation-delay: 0.1s; }
.lot-card:nth-child(2) { animation-delay: 0.2s; }
.lot-card:nth-child(3) { animation-delay: 0.3s; }
.lot-card:nth-child(n+4) { animation-delay: 0.4s; }

.lot-card:hover {
  transform: translateX(6px);
  box-shadow: var(--shadow-md);
  border-left-color: var(--urgency-color);
}

.lot-card.urgent { --urgency-color: var(--color-j3); }
.lot-card.warning { --urgency-color: var(--color-j7); }
.lot-card.planning { --urgency-color: var(--color-j21); }

.lot-info {
  flex: 1;
}

.lot-name {
  font-size: 16px;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin-bottom: var(--space-sm);
}

.lot-details {
  display: flex;
  gap: var(--space-lg);
  flex-wrap: wrap;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.lot-detail-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: var(--font-weight-semibold);
}

.lot-status-badge {
  background: var(--urgency-color);
  color: white;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: var(--font-weight-bold);
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* ════════════════════════════════════════════════════════════ */
/* BUTTONS */
/* ════════════════════════════════════════════════════════════ */

.stButton button {
  background: linear-gradient(135deg, var(--color-primary) 0%, #C20410 100%) !important;
  color: white !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
  padding: var(--space-md) var(--space-lg) !important;
  font-size: 16px !important;
  font-weight: var(--font-weight-bold) !important;
  letter-spacing: 0.5px !important;
  transition: all var(--transition-fast) !important;
  box-shadow: var(--shadow-md) !important;
  cursor: pointer !important;
  min-height: 44px !important;
}

.stButton button:hover {
  transform: translateY(-2px) !important;
  box-shadow: var(--shadow-lg) !important;
}

.stButton button:active {
  transform: translateY(0) !important;
}

/* ════════════════════════════════════════════════════════════ */
/* TABS */
/* ════════════════════════════════════════════════════════════ */

.stTabs [data-baseweb="tab-list"] {
  border-bottom: 2px solid var(--color-border) !important;
  gap: var(--space-lg) !important;
  background: transparent !important;
}

.stTabs [aria-selected="true"] {
  border-bottom: 3px solid var(--color-primary) !important;
  color: var(--color-primary) !important;
  font-weight: var(--font-weight-bold) !important;
}

.stTabs [aria-selected="false"] {
  color: var(--color-text-secondary) !important;
  font-weight: var(--font-weight-semibold) !important;
}

/* ════════════════════════════════════════════════════════════ */
/* ANIMATIONS */
/* ════════════════════════════════════════════════════════════ */

@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* ════════════════════════════════════════════════════════════ */
/* RESPONSIVE */
/* ════════════════════════════════════════════════════════════ */

@media (max-width: 768px) {
  .main-title {
    font-size: 36px;
  }
  
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  
  .lot-card {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .lot-status-badge {
    margin-top: var(--space-md);
    width: 100%;
    text-align: center;
  }
  
  .lot-details {
    margin-bottom: var(--space-md);
  }
}

/* REDUCE MOTION FOR ACCESSIBILITY */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# FIREBASE INITIALIZATION
# ═════════════════════════════════════════════════════════════════════════

@st.cache_resource
def init_firebase():
    """Initialize Firebase connection"""
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

def days_until(exp_date: str) -> int:
    """Calculate days remaining until expiry date"""
    try:
        expiry = pd.to_datetime(exp_date).date()
        days = (expiry - date.today()).days
        return days
    except:
        return 999

def stage_from_days(days: int) -> str:
    """Determine urgency stage based on days remaining"""
    if days <= 3:
        return "J-3"
    elif days <= 7:
        return "J-7"
    elif days <= 21:
        return "J-21"
    else:
        return "OK"

def get_urgency_config(stage: str) -> dict:
    """Get color and styling config for urgency stage"""
    config = {
        "J-3": {"color": "#E30613", "label": "🔴 URGENT - 3 jours", "css_class": "urgent"},
        "J-7": {"color": "#F39200", "label": "⏰ ALERTE - 1 semaine", "css_class": "warning"},
        "J-21": {"color": "#2BA84F", "label": "📅 PLANIFIER - 3 semaines", "css_class": "planning"},
        "OK": {"color": "#666666", "label": "✅ À JOUR", "css_class": "ok"}
    }
    return config.get(stage, config["OK"])

# ═════════════════════════════════════════════════════════════════════════
# LOAD DATA FROM FIREBASE
# ═════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=60)
def load_lots(store_id: str) -> pd.DataFrame:
    """Load all lots from Firebase for specific store"""
    lots = []
    
    try:
        # Query all documents in 'lots' collection
        for doc in db.collection("lots").stream():
            d = doc.to_dict()
            d["id"] = doc.id
            
            # Map Firebase field names to app fields
            d["expiryDate"] = d.get("dlc")
            d["productId"] = d.get("product_ean")
            d["lotNumber"] = d.get("lot_code")
            d["quantity"] = d.get("qty_current", 0)
            d["location"] = d.get("location", "")
            
            # Filter by store
            if d.get("store_id") == store_id:
                lots.append(d)
    
    except Exception as e:
        st.error(f"❌ Erreur chargement lots: {str(e)}")
        return pd.DataFrame()
    
    if not lots:
        return pd.DataFrame()
    
    # Create DataFrame and process
    df = pd.DataFrame(lots)
    df["expiryDate"] = pd.to_datetime(df["expiryDate"], errors='coerce')
    df = df.dropna(subset=["expiryDate"])
    
    # Calculate urgency metrics
    df["daysLeft"] = df["expiryDate"].apply(days_until)
    df["stage"] = df["daysLeft"].apply(stage_from_days)
    
    # Sort by expiry date
    df = df.sort_values("expiryDate")
    
    return df

@st.cache_data(ttl=60)
def load_stores() -> list:
    """Load all unique store IDs from Firebase"""
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
# SIDEBAR CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### ⚙️ CONFIGURATION")
    
    # Store selector
    stores = load_stores()
    store_id = st.selectbox(
        "🏪 Sélectionne un magasin",
        stores,
        index=0
    )
    
    st.divider()
    
    # App info
    st.markdown("""
    ### 🧊 SmartExpiry Pro
    
    **Gestion FEFO Intelligente**
    
    ✅ Sync Real-Time  
    📊 Multi-Magasins  
    ⚡ 100% Automatisé  
    🎯 Zéro Perte
    """)
    
    st.divider()
    
    # System info
    st.caption(f"v2.0 • Retail Design System • {datetime.now(PARIS).strftime('%d/%m %H:%M')}")

# ═════════════════════════════════════════════════════════════════════════
# MAIN CONTENT - HEADER
# ═════════════════════════════════════════════════════════════════════════

# Load data
lots_df = load_lots(store_id)

# Main title - CENTER, BOLD, NO DECORATION
st.markdown("""
<div class="main-title-container">
    <h1 class="main-title">🧊 SmartExpiry Pro — Gestion FEFO</h1>
    <p class="main-subtitle">Contrôlez chaque lot en temps réel • Alertes intelligentes • Zéro perte</p>
</div>
""", unsafe_allow_html=True)

# Hero banner
st.markdown("""
<div class="hero-banner">
    <h2>📦 Gestion d'Inventaire Intelligente</h2>
    <p>Suivi FEFO automatique • Alertes par urgence • Rapports exportables • Multi-magasins</p>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ═════════════════════════════════════════════════════════════════════════

if not lots_df.empty:
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # KPI 1: Total Tasks
    with col1:
        total_tasks = len(lots_df)
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📋</div>
            <div class="kpi-label">Tâches Ouvertes</div>
            <div class="kpi-value">{total_tasks}</div>
            <div class="kpi-meta">Lots à gérer</div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI 2: Urgent (J-3)
    with col2:
        urgent = len(lots_df[lots_df["stage"] == "J-3"])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🔴</div>
            <div class="kpi-label">Urgent J-3</div>
            <div class="kpi-value">{urgent}</div>
            <div class="kpi-meta">Action immédiate</div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI 3: Warning (J-7)
    with col3:
        warning = len(lots_df[lots_df["stage"] == "J-7"])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">⏰</div>
            <div class="kpi-label">Alerte J-7</div>
            <div class="kpi-value">{warning}</div>
            <div class="kpi-meta">À surveiller</div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI 4: Pipeline (J-21)
    with col4:
        planning = len(lots_df[lots_df["stage"] == "J-21"])
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📅</div>
            <div class="kpi-label">Pipeline J-21</div>
            <div class="kpi-value">{planning}</div>
            <div class="kpi-meta">À planifier</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# TABS - MAIN INTERFACE
# ═════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Inventaire Complet",
    "📊 Analytics",
    "📧 Email Digest",
    "📥 Export Données"
])

# ─────────────────────────────────────────────────────────────────────────
# TAB 1: INVENTORY LISTING
# ─────────────────────────────────────────────────────────────────────────

with tab1:
    st.markdown("### 📋 Gestion Complète par Urgence")
    
    if not lots_df.empty:
        
        # URGENT SECTION (J-3)
        urgent_lots = lots_df[lots_df["stage"] == "J-3"].sort_values("expiryDate")
        if not urgent_lots.empty:
            st.markdown('<h3 class="section-title">🔴 URGENT - À 3 jours</h3>', unsafe_allow_html=True)
            
            for _, row in urgent_lots.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date()
                st.markdown(f"""
                <div class="lot-card urgent">
                    <div class="lot-info">
                        <div class="lot-name">📦 {row['productId']} • Lot {row['lotNumber']}</div>
                        <div class="lot-details">
                            <div class="lot-detail-item">📊 {int(row['quantity'])} unités</div>
                            <div class="lot-detail-item">📅 DLC: {exp_date.strftime('%d/%m/%Y')}</div>
                            <div class="lot-detail-item">📍 {row['location']}</div>
                        </div>
                    </div>
                    <div class="lot-status-badge" style="background-color: var(--color-j3);">
                        🔴 {row['daysLeft']} jours restant
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # WARNING SECTION (J-7)
        warning_lots = lots_df[lots_df["stage"] == "J-7"].sort_values("expiryDate")
        if not warning_lots.empty:
            st.markdown('<h3 class="section-title">⏰ ALERTE - À 1 semaine</h3>', unsafe_allow_html=True)
            
            for _, row in warning_lots.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date()
                st.markdown(f"""
                <div class="lot-card warning">
                    <div class="lot-info">
                        <div class="lot-name">📦 {row['productId']} • Lot {row['lotNumber']}</div>
                        <div class="lot-details">
                            <div class="lot-detail-item">📊 {int(row['quantity'])} unités</div>
                            <div class="lot-detail-item">📅 DLC: {exp_date.strftime('%d/%m/%Y')}</div>
                            <div class="lot-detail-item">📍 {row['location']}</div>
                        </div>
                    </div>
                    <div class="lot-status-badge" style="background-color: var(--color-j7);">
                        ⏰ {row['daysLeft']} jours
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # PLANNING SECTION (J-21)
        planning_lots = lots_df[lots_df["stage"] == "J-21"].sort_values("expiryDate")
        if not planning_lots.empty:
            st.markdown('<h3 class="section-title">📅 PLANIFIER - À 3 semaines</h3>', unsafe_allow_html=True)
            
            for _, row in planning_lots.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date()
                st.markdown(f"""
                <div class="lot-card planning">
                    <div class="lot-info">
                        <div class="lot-name">📦 {row['productId']} • Lot {row['lotNumber']}</div>
                        <div class="lot-details">
                            <div class="lot-detail-item">📊 {int(row['quantity'])} unités</div>
                            <div class="lot-detail-item">📅 DLC: {exp_date.strftime('%d/%m/%Y')}</div>
                            <div class="lot-detail-item">📍 {row['location']}</div>
                        </div>
                    </div>
                    <div class="lot-status-badge" style="background-color: var(--color-j21);">
                        📅 {row['daysLeft']} jours
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("✅ Aucun lot pour ce magasin - Inventaire vide ou à jour !")

# ─────────────────────────────────────────────────────────────────────────
# TAB 2: ANALYTICS
# ─────────────────────────────────────────────────────────────────────────

with tab2:
    st.markdown("### 📊 Visualisation des Données")
    
    if not lots_df.empty:
        col1, col2 = st.columns(2)
        
        # Chart 1: Distribution par étape
        with col1:
            stage_counts = lots_df["stage"].value_counts()
            fig1 = go.Figure(data=[
                go.Bar(
                    x=stage_counts.index,
                    y=stage_counts.values,
                    marker=dict(
                        color=['#E30613', '#F39200', '#2BA84F', '#666666'],
                        line=dict(color='#FFFFFF', width=2)
                    ),
                    text=stage_counts.values,
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>%{y} lots<extra></extra>'
                )
            ])
            fig1.update_layout(
                title="Distribution par Étape",
                xaxis_title="Urgence",
                yaxis_title="Nombre de lots",
                template="plotly_white",
                height=400,
                showlegend=False,
                hovermode='x unified'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        # Chart 2: Urgence vs Quantité
        with col2:
            fig2 = go.Figure(data=[
                go.Scatter(
                    x=lots_df["daysLeft"],
                    y=lots_df["quantity"],
                    mode='markers',
                    marker=dict(
                        size=lots_df["quantity"] / 3,
                        color=lots_df["daysLeft"],
                        colorscale=[[0, '#E30613'], [0.5, '#F39200'], [1, '#2BA84F']],
                        showscale=True,
                        line=dict(color='white', width=1),
                        colorbar=dict(title="Jours restants")
                    ),
                    text=lots_df["productId"],
                    hovertemplate='<b>%{text}</b><br>Jours: %{x}<br>Quantité: %{y}<extra></extra>'
                )
            ])
            fig2.update_layout(
                title="Urgence vs Quantité",
                xaxis_title="Jours jusqu'à expiration",
                yaxis_title="Quantité (unités)",
                template="plotly_white",
                height=400,
                hovermode='closest'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Stats summary
        st.divider()
        st.markdown("#### 📈 Résumé Statistique")
        
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            total_qty = lots_df["quantity"].sum()
            st.metric("Total Quantités", f"{int(total_qty)} unités")
        
        with stats_col2:
            avg_days = lots_df["daysLeft"].mean()
            st.metric("Moyenne Jours", f"{avg_days:.1f} jours")
        
        with stats_col3:
            risky_qty = lots_df[lots_df["daysLeft"] <= 7]["quantity"].sum()
            st.metric("Quantité à Risque", f"{int(risky_qty)} unités", f"J-7 et moins")

# ─────────────────────────────────────────────────────────────────────────
# TAB 3: EMAIL DIGEST
# ─────────────────────────────────────────────────────────────────────────

with tab3:
    st.markdown("### 📧 Envoyer le Digest Quotidien")
    
    if not lots_df.empty:
        # Summary info
        urgent_count = len(lots_df[lots_df["stage"] == "J-3"])
        total_qty = int(lots_df["quantity"].sum())
        
        st.info(f"""
        **Résumé:**
        - 🔴 **{urgent_count}** lots urgents (J-3)
        - 📦 **{total_qty}** unités au total
        - 📅 Magasin: **{store_id}**
        """)
    
    # Send button
    if st.button("📬 Envoyer le rapport maintenant", use_container_width=True):
        with st.spinner("Envoi en cours..."):
            try:
                # Build email HTML
                html_content = f"""
                <html>
                <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #F5F5F5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); overflow: hidden;">
                
                    <!-- Header -->
                    <div style="background: linear-gradient(135deg, #E30613 0%, #F39200 100%); padding: 30px; color: white; text-align: center;">
                        <h1 style="margin: 0; font-size: 32px; font-weight: 800;">🧊 SmartExpiry Pro</h1>
                        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Rapport Quotidien</p>
                    </div>
                    
                    <!-- Content -->
                    <div style="padding: 30px;">
                        <h2 style="color: #1A1A1A; font-size: 20px; margin-bottom: 20px;">Résumé du {datetime.now(PARIS).strftime('%d %B %Y')}</h2>
                        
                        <p style="color: #666666; font-size: 14px; margin-bottom: 20px;">
                            <strong>Magasin:</strong> {store_id}
                        </p>
                        
                        <div style="background-color: #FDE8E8; border-left: 4px solid #E30613; padding: 15px; margin-bottom: 15px;">
                            <p style="margin: 0; color: #C20410; font-weight: bold;">
                                🔴 <strong>{urgent_count}</strong> lots urgents (À 3 jours)
                            </p>
                        </div>
                        
                        <div style="background-color: #FEF3E6; border-left: 4px solid #F39200; padding: 15px; margin-bottom: 15px;">
                            <p style="margin: 0; color: #D97706; font-weight: bold;">
                                ⏰ <strong>{len(lots_df[lots_df["stage"] == "J-7"])}</strong> alertes (À 1 semaine)
                            </p>
                        </div>
                        
                        <div style="background-color: #E8F5E9; border-left: 4px solid #2BA84F; padding: 15px;">
                            <p style="margin: 0; color: #1B5E20; font-weight: bold;">
                                📅 <strong>{len(lots_df[lots_df["stage"] == "J-21"])}</strong> à planifier (À 3 semaines)
                            </p>
                        </div>
                    </div>
                    
                    <!-- Footer -->
                    <div style="background-color: #F5F5F5; padding: 20px; text-align: center; border-top: 1px solid #EEEEEE;">
                        <p style="margin: 0; color: #666666; font-size: 12px;">
                            SmartExpiry Pro v2.0 • Gestion FEFO Intelligente
                        </p>
                    </div>
                </div>
                </body>
                </html>
                """
                
                # Create email message
                msg = MIMEMultipart("alternative")
                msg["Subject"] = f"🧊 SmartExpiry Pro - Rapport {store_id}"
                msg["From"] = st.secrets.email["from"]
                msg["To"] = st.secrets.email["to"]
                msg.attach(MIMEText(html_content, "html"))
                
                # Send via SMTP
                with smtplib.SMTP(st.secrets.email["host"], int(st.secrets.email["port"])) as server:
                    server.starttls()
                    server.login(st.secrets.email["username"], st.secrets.email["password"])
                    server.sendmail(msg["From"], [msg["To"]], msg.as_string())
                
                st.success("✅ Email envoyé avec succès!")
                st.balloons()
            
            except Exception as e:
                st.error(f"❌ Erreur lors de l'envoi: {str(e)}")

# ─────────────────────────────────────────────────────────────────────────
# TAB 4: EXPORT DATA
# ─────────────────────────────────────────────────────────────────────────

with tab4:
    st.markdown("### 📥 Exporter les Données")
    
    st.markdown("""
    Télécharge les données d'inventaire en format CSV pour analyse ou intégration.
    Inclut tous les lots, leurs statuts et dates d'expiration.
    """)
    
    if st.button("⬇️ Générer et télécharger le CSV", use_container_width=True):
        if not lots_df.empty:
            # Build CSV content
            csv_lines = ["PRODUIT,LOT,QUANTITÉ,DLC,JOURS_RESTANTS,RAYON,URGENCE\n"]
            
            for _, row in lots_df.iterrows():
                exp_date = pd.to_datetime(row['expiryDate']).date().strftime('%d/%m/%Y')
                csv_line = f"{row['productId']},{row['lotNumber']},{int(row['quantity'])},{exp_date},{int(row['daysLeft'])},{row['location']},{row['stage']}\n"
                csv_lines.append(csv_line)
            
            csv_content = "".join(csv_lines)
            
            # Download button
            st.download_button(
                label="📊 Télécharger le rapport CSV",
                data=csv_content,
                file_name=f"smartexpiry_{store_id}_{datetime.now(PARIS).strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            st.success(f"✅ Rapport généré: {len(lots_df)} lots")
        else:
            st.warning("⚠️ Aucun lot à exporter")

# ═════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════

st.divider()

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption(f"🧊 **SmartExpiry Pro v2.0**")

with footer_col2:
    st.caption(f"Dernière sync: {datetime.now(PARIS).strftime('%d/%m/%Y à %H:%M:%S')}")

with footer_col3:
    st.caption(f"Magasin: **{store_id}**")
