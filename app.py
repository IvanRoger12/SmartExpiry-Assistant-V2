import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from dateutil import tz
import plotly.express as px
import plotly.graph_objects as go
import smtplib
from email.mime.text import MIMEText
import io

# ═════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SmartExpiry — Gestion FEFO",
    layout="wide",
    page_icon="🧊",
    initial_sidebar_state="expanded"
)

# CSS PREMIUM - DESIGN SYSTEM COMPLET
st.markdown("""
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --primary: #2563eb;
  --primary-dark: #1e40af;
  --danger: #dc2626;
  --warning: #f59e0b;
  --success: #10b981;
  --bg: #f3f4f6;
  --border: #e5e7eb;
  --text: #111827;
  --muted: #6b7280;
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.block-container { 
  padding: 1.25rem 2rem !important;
  max-width: 1600px;
}

/* HERO SECTION */
.hero {
  background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #1e40af 100%);
  border-radius: 20px;
  padding: 2.5rem;
  color: white;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2), inset 0 0 0 1px rgba(255,255,255,.08);
  margin-bottom: 2rem;
  border: 1px solid rgba(255,255,255,.1);
  position: relative;
  overflow: hidden;
}

.hero h1 {
  font-size: 2.2rem;
  font-weight: 900;
  margin: 0.5rem 0;
  background: linear-gradient(90deg, #fff 0%, #dbeafe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.125rem;
  opacity: 0.9;
  margin-top: 0.75rem;
}

/* KPI CARDS */
.kpi {
  background: white;
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
  transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
  position: relative;
  overflow: hidden;
}

.kpi::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), #6366f1);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.kpi:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,.12);
  border-color: var(--primary);
}

.kpi:hover::before {
  transform: scaleX(1);
}

.kpi-label {
  font-size: 0.875rem;
  color: var(--muted);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 1rem;
}

.kpi-value {
  font-size: 2.8rem;
  font-weight: 900;
  color: var(--primary);
  line-height: 1;
}

.kpi-meta {
  font-size: 0.875rem;
  color: #9ca3af;
  margin-top: 0.5rem;
}

/* BADGES */
.badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  margin-right: 0.5rem;
}

.badge-j3 { background: #fee2e2; color: #b91c1c; }
.badge-j7 { background: #fed7aa; color: #92400e; }
.badge-j21 { background: #dbeafe; color: #1e40af; }
.badge-ok { background: #d1fae5; color: #065f46; }

/* STAGE CONTAINER */
.stage-container {
  background: white;
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
  margin-bottom: 2rem;
}

/* BUTTONS */
[data-testid="baseButton-primary"] {
  background: var(--primary) !important;
  color: white !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  transition: all 0.2s ease !important;
}

[data-testid="baseButton-primary"]:hover {
  background: var(--primary-dark) !important;
  box-shadow: 0 8px 16px rgba(37,99,235,.3) !important;
}

/* ALERTS */
[data-testid="stAlert"] {
  border-radius: 12px !important;
  border: 1px solid var(--border) !important;
}

hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# FIREBASE INIT
# ═════════════════════════════════════════════════════════════════════════
import firebase_admin
from firebase_admin import credentials, firestore

@st.cache_resource
def init_db():
    """Initialise Firebase avec gestion d'erreurs robuste."""
    if not firebase_admin._apps:
        try:
            config = st.secrets.get("firebase", {})
            
            # Gère les retours à la ligne échappés
            if "private_key" in config:
                pk = config["private_key"]
                if isinstance(pk, str) and "\\n" in pk:
                    config["private_key"] = pk.replace("\\n", "\n")
            
            # Validation
            required = ["type", "project_id", "private_key_id", "private_key", "client_email", "client_id"]
            missing = [k for k in required if not config.get(k)]
            if missing:
                st.error(f"❌ Secrets Firebase incomplets: {', '.join(missing)}")
                st.info("📋 Renseigne les secrets dans Streamlit Cloud → Settings → Secrets")
                st.stop()
            
            cred = credentials.Certificate(config)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"❌ Erreur Firebase: {str(e)}")
            st.stop()
    
    return firestore.client()

db = init_db()
PARIS = tz.gettz("Europe/Paris")

# ═════════════════════════════════════════════════════════════════════════
# HELPERS & UTILS
# ═════════════════════════════════════════════════════════════════════════

def mask_email(addr: str) -> str:
    """Masque un email pour l'affichage."""
    if not addr or "@" not in addr:
        return "non renseigné"
    local, domain = addr.split("@", 1)
    dom, *ext = domain.split(".")
    return f"{local[0]}{'*'*(len(local)-1)}@{dom[0]}{'*'*(len(dom)-1)}{'.' + '.'.join(ext) if ext else ''}"

def ts_to_dt(value):
    """Convertit un Firestore Timestamp en datetime."""
    try:
        if hasattr(value, "to_datetime"):
            return value.to_datetime()
    except:
        pass
    return value

def days_until(exp_date) -> int:
    """Calcule les jours restants jusqu'à la DLC."""
    expiry = pd.to_datetime(exp_date).date()
    return (expiry - date.today()).days

def stage_from_days(days: int) -> str:
    """Détermine l'étape du tunnel selon les jours restants."""
    if days <= 3:
        return "J-3"
    elif days <= 7:
        return "J-7"
    elif days <= 21:
        return "J-21"
    else:
        return "OK"

def stage_label(stage: str) -> str:
    """Label lisible pour chaque étape."""
    labels = {
        "J-21": "À 3 semaines — Planifier une promo",
        "J-7": "À 1 semaine — Mise en avant / -20%",
        "J-3": "À 3 jours — Action immédiate / -50%",
        "OK": "> 3 semaines — Stock régulier"
    }
    return labels.get(stage, stage)

def stage_badge_html(stage: str) -> str:
    """HTML badge pour chaque étape."""
    badges = {
        "J-21": '<span class="badge badge-j21">J-21</span>',
        "J-7": '<span class="badge badge-j7">J-7</span>',
        "J-3": '<span class="badge badge-j3">J-3</span>',
        "OK": '<span class="badge badge-ok">OK</span>'
    }
    return badges.get(stage, "")

# ═════════════════════════════════════════════════════════════════════════
# DATA LAYER
# ═════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=60)
def load_lots(store_id: str) -> pd.DataFrame:
    """Charge les lots depuis Firestore."""
    lots = []
    
    # Essaie sous-collection stores/{store}/lots
    try:
        for doc in db.collection("stores").document(store_id).collection("lots").stream():
            d = doc.to_dict()
            d["id"] = doc.id
            d["expiryDate"] = ts_to_dt(d.get("expiryDate"))
            d["receivedAt"] = ts_to_dt(d.get("receivedAt"))
            lots.append(d)
    except:
        pass
    
    # Fallback: collection racine filtrée par storeId
    if not lots:
        try:
            for doc in db.collection("lots").where("storeId", "==", store_id).stream():
                d = doc.to_dict()
                d["id"] = doc.id
                d["expiryDate"] = ts_to_dt(d.get("expiryDate"))
                d["receivedAt"] = ts_to_dt(d.get("receivedAt"))
                lots.append(d)
        except:
            pass
    
    if not lots:
        return pd.DataFrame(columns=["id", "productId", "lotNumber", "quantity", "expiryDate", "location"])
    
    df = pd.DataFrame(lots)
    if not df.empty:
        df["expiryDate"] = pd.to_datetime(df["expiryDate"])
        df["daysLeft"] = df["expiryDate"].apply(days_until)
        df["stage"] = df["daysLeft"].apply(stage_from_days)
        df = df.sort_values("expiryDate")
    
    return df

def get_tasks_col(store_id: str):
    """Référence à la collection tasks pour un magasin."""
    return db.collection("stores").document(store_id).collection("tasks")

def task_id(lot_id: str, stage: str) -> str:
    """ID unique pour une tâche."""
    return f"TASK_{lot_id}_{stage}"

def ensure_tasks(store_id: str, lots_df: pd.DataFrame) -> int:
    """Génère les tâches manquantes pour les lots d'un magasin."""
    if lots_df.empty:
        return 0
    
    col = get_tasks_col(store_id)
    count = 0
    
    for _, row in lots_df.iterrows():
        if row["stage"] == "OK":
            continue
        
        tid = task_id(row["id"], row["stage"])
        payload = {
            "id": tid,
            "lotId": row["id"],
            "productId": row.get("productId", ""),
            "lotNumber": row.get("lotNumber", ""),
            "stage": row["stage"],
            "stageLabel": stage_label(row["stage"]),
            "daysLeft": int(row["daysLeft"]),
            "quantity": int(row.get("quantity", 0)) if pd.notna(row.get("quantity")) else 0,
            "expiryDate": row["expiryDate"].to_pydatetime(),
            "location": row.get("location", ""),
            "status": "open",
            "snoozedUntil": None,
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP,
        }
        
        col.document(tid).set(payload, merge=True)
        count += 1
    
    return count

@st.cache_data(ttl=60)
def load_tasks(store_id: str) -> pd.DataFrame:
    """Charge les tâches depuis Firestore."""
    docs = list(get_tasks_col(store_id).stream())
    
    if not docs:
        return pd.DataFrame(columns=["id", "stage", "status", "expiryDate"])
    
    records = [doc.to_dict() | {"id": doc.id} for doc in docs]
    df = pd.DataFrame(records)
    
    if "expiryDate" in df.columns:
        df["expiryDate"] = pd.to_datetime(
            df["expiryDate"].apply(
                lambda x: x if isinstance(x, datetime) else ts_to_dt(x)
            )
        )
    
    return df

def update_task(store_id: str, task_id_val: str, status: str, snooze_days: int = None):
    """Met à jour le statut d'une tâche."""
    ref = get_tasks_col(store_id).document(task_id_val)
    data = {
        "status": status,
        "updatedAt": firestore.SERVER_TIMESTAMP
    }
    
    if snooze_days is not None:
        data["snoozedUntil"] = datetime.now(PARIS) + timedelta(days=snooze_days)
    
    ref.set(data, merge=True)

# ═════════════════════════════════════════════════════════════════════════
# EMAIL FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════

def send_email(subject: str, html: str) -> tuple:
    """Envoie un email via SMTP."""
    try:
        cfg = st.secrets.get("email", {})
        
        if not all(cfg.get(k) for k in ["host", "port", "from", "to"]):
            return False, "Config email incomplète"
        
        msg = MIMEText(html, "html", "utf-8")
        msg["Subject"] = subject
        msg["From"] = cfg["from"]
        msg["To"] = cfg["to"]
        
        with smtplib.SMTP(cfg["host"], int(cfg["port"])) as s:
            if cfg.get("use_tls", True):
                s.starttls()
            if cfg.get("username") and cfg.get("password"):
                s.login(cfg["username"], cfg["password"])
            s.sendmail(msg["From"], [msg["To"]], msg.as_string())
        
        return True, "Email envoyé ✅"
    except Exception as e:
        return False, f"Erreur SMTP: {str(e)}"

def get_email_recipient() -> str:
    """Email destinataire (masqué)."""
    return mask_email(st.secrets.get("email", {}).get("to", ""))

def email_digest_html(store_id: str, tasks_df: pd.DataFrame) -> str:
    """Génère le HTML du digest email."""
    rows = []
    
    for stage in ["J-21", "J-7", "J-3"]:
        sub = tasks_df[(tasks_df["stage"] == stage) & (tasks_df["status"] == "open")]
        if sub.empty:
            continue
        
        rows.append(f"<h3 style='margin:16px 0 12px 0; color:#111827;'>{stage_label(stage)}</h3>")
        rows.append("""<table style='width:100%;border-collapse:collapse;border:1px solid #e5e7eb;border-radius:8px;overflow:hidden;'>
            <thead><tr style='background:#f9fafb;'>
            <th style='padding:12px;text-align:left;font-size:12px;font-weight:700;color:#6b7280;'>Produit</th>
            <th style='padding:12px;text-align:left;font-size:12px;font-weight:700;color:#6b7280;'>Lot</th>
            <th style='padding:12px;text-align:left;font-size:12px;font-weight:700;color:#6b7280;'>Qté</th>
            <th style='padding:12px;text-align:left;font-size:12px;font-weight:700;color:#6b7280;'>DLC</th>
            <th style='padding:12px;text-align:left;font-size:12px;font-weight:700;color:#6b7280;'>J</th>
            <th style='padding:12px;text-align:left;font-size:12px;font-weight:700;color:#6b7280;'>Rayon</th>
            </tr></thead><tbody>""")
        
        for _, r in sub.sort_values("expiryDate").iterrows():
            rows.append(f"""<tr style='border-bottom:1px solid #e5e7eb;'>
                <td style='padding:12px;'>{r.get('productId','')}</td>
                <td style='padding:12px;font-weight:700;color:#111827;'>{r.get('lotNumber','')}</td>
                <td style='padding:12px;'>{int(r.get('quantity',0))}</td>
                <td style='padding:12px;'>{pd.to_datetime(r['expiryDate']).date().strftime('%d/%m/%Y')}</td>
                <td style='padding:12px;'>{int(r.get('daysLeft',0))}</td>
                <td style='padding:12px;font-size:0.875rem;color:#6b7280;'>{r.get('location','')}</td>
            </tr>""")
        
        rows.append("</tbody></table><br/>")
    
    body = "".join(rows) if rows else "<p style='color:#6b7280;'>✅ Toutes les tâches sont à jour</p>"
    
    return f"""<!doctype html><html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f3f4f6;margin:0;padding:20px;">
        <div style="max-width:680px;margin:0 auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 10px 25px rgba(0,0,0,.1);">
          <div style="background:linear-gradient(135deg,#3b82f6 0%,#6366f1 100%);padding:28px;color:#fff;">
            <h2 style="margin:0;font-size:24px;font-weight:900;">SmartExpiry — Digest quotidien</h2>
            <div style="opacity:.9;margin-top:6px;font-size:14px;">Magasin: {store_id}</div>
          </div>
          <div style="padding:28px;">{body}
            <div style="text-align:center;margin-top:24px;">
              <a href="#" style="display:inline-block;background:#2563eb;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:800;font-size:14px;">Ouvrir le dashboard →</a>
            </div>
          </div>
          <div style="background:#f9fafb;padding:16px;text-align:center;color:#6b7280;font-size:12px;border-top:1px solid #e5e7eb;">
            SmartExpiry · Optimisation FEFO & Marges · {datetime.now(PARIS).strftime('%d/%m/%Y')}
          </div>
        </div>
      </body></html>"""

def should_auto_send(store_id: str) -> bool:
    """Vérifie si le digest auto doit être envoyé aujourd'hui."""
    today = datetime.now(PARIS).strftime("%Y-%m-%d")
    doc_id = f"DIGEST_{store_id}_{today}"
    
    ref = db.collection("emailLogs").document(doc_id)
    
    if ref.get().exists:
        return False
    
    ref.set({
        "storeId": store_id,
        "date": today,
        "createdAt": firestore.SERVER_TIMESTAMP,
        "source": "streamlit",
        "status": "scheduled"
    })
    
    return True

def mark_email_sent(store_id: str, success: bool, err: str = ""):
    """Enregistre l'envoi d'email."""
    today = datetime.now(PARIS).strftime("%Y-%m-%d")
    doc_id = f"DIGEST_{store_id}_{today}"
    
    db.collection("emailLogs").document(doc_id).set({
        "sentAt": firestore.SERVER_TIMESTAMP,
        "status": "sent" if success else "error",
        "error": err
    }, merge=True)

# ═════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════

brand = st.secrets.get("app", {}).get("brand", "SmartExpiry V2")
default_store = st.secrets.get("app", {}).get("default_store", "naturalia_nanterre")
daily_hour = int(st.secrets.get("app", {}).get("daily_send_hour", 8))

st.sidebar.title(f"⚙️ {brand}")
st.sidebar.write("---")

store_id = st.sidebar.text_input("📍 Magasin (storeId)", default_store)
st.sidebar.caption(f"📧 Digest → **{get_email_recipient()}** (masqué)")
auto_toggle = st.sidebar.toggle("🤖 Auto-digest (après {daily_hour:02d}h)", value=True)

st.session_state["auto_toggle"] = auto_toggle

st.sidebar.write("---")
st.sidebar.markdown(f"""
### 📚 À propos
**{brand}** — Tunnel FEFO intelligent
- J-21: Planifier promo
- J-7: Mise en avant -20%
- J-3: Action -50%

Zéro perte, marge optimisée.
""")

# ═════════════════════════════════════════════════════════════════════════
# HERO
# ═════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="hero">
  <div style="position:relative;z-index:1;">
    <div style="font-weight:700;opacity:0.85;margin-bottom:0.5rem;">⏰ Tunnel d'actions FEFO</div>
    <h1>De 3 semaines à 3 jours : Zéro perte, Marge optimisée</h1>
    <div class="hero-subtitle">
      Workflow: J-21 → J-7 → J-3 | Snooze & Rappels auto | Digest quotidien
    </div>
  </div>
  <div style="position:absolute;top:1.5rem;right:2.5rem;font-size:0.95rem;opacity:0.8;">
    {datetime.now(PARIS).strftime('%d %b %Y — %H:%M')} (Paris)
  </div>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# LOAD & PREPARE DATA
# ═════════════════════════════════════════════════════════════════════════

lots_df = load_lots(store_id)
_ = ensure_tasks(store_id, lots_df)
tasks_df = load_tasks(store_id)

# KPIs
open_tasks = len(tasks_df[(tasks_df["status"] == "open") & (tasks_df["stage"] != "OK")]) if not tasks_df.empty else 0
urgent = len(tasks_df[(tasks_df["stage"] == "J-3") & (tasks_df["status"] == "open")]) if not tasks_df.empty else 0
pipeline = len(tasks_df[(tasks_df["stage"].isin(["J-21", "J-7"])) & (tasks_df["status"] == "open")]) if not tasks_df.empty else 0

# Display KPIs
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi">
      <div class="kpi-label">📋 Tâches Ouvertes</div>
      <div class="kpi-value">{open_tasks}</div>
      <div class="kpi-meta">à traiter</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi">
      <div class="kpi-label">🔴 Action Immédiate (J-3)</div>
      <div class="kpi-value" style="color:var(--danger);">{urgent}</div>
      <div class="kpi-meta">à moins de 3 jours</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi">
      <div class="kpi-label">📦 En Préparation (J-21/J-7)</div>
      <div class="kpi-value" style="color:var(--warning);">{pipeline}</div>
      <div class="kpi-meta">à planifier</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ═════════════════════════════════════════════════════════════════════════
# TABS
# ═════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📊 Analyse", "⚙️ Paramètres"])

# ════════════ TAB 1: DASHBOARD ════════════
with tab1:
    st.write("")
    
    def render_stage(stage_key: str, snoozes: list):
        """Affiche une étape du tunnel."""
        st.markdown(f"""
        <div style="margin-bottom:1rem;">
            <div style="font-size:1.125rem;font-weight:800;color:#111827;margin-bottom:1rem;">
                {stage_badge_html(stage_key)} {stage_label(stage_key)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if tasks_df.empty:
            st.info("📭 Aucune tâche.")
            return
        
        sub = tasks_df[tasks_df["stage"] == stage_key].sort_values("expiryDate")
        
        if sub.empty:
            st.info("✅ Aucune tâche à cette étape.")
            return
        
        for _, row in sub.iterrows():
            status = row.get("status", "open")
            
            if status == "done":
                st.markdown(f"✅ **{row.get('productId','')}** — Lot **{row.get('lotNumber','')}** (*Terminé*)")
                continue
            
            if status == "snoozed" and row.get("snoozedUntil"):
                until = pd.to_datetime(row["snoozedUntil"]).strftime("%d/%m %H:%M")
                st.markdown(f"⏰ **{row.get('productId','')}** — Lot **{row.get('lotNumber','')}** (*Rappel le {until}*)")
                continue
            
            col_a, col_b, col_c = st.columns([2, 2, 2])
            
            with col_a:
                st.markdown(f"""
                <div class="task-product">{row.get('productId','')}</div>
                <div class="task-meta">
                    Lot: <strong>{row.get('lotNumber','')}</strong> | 
                    DLC: {pd.to_datetime(row['expiryDate']).date().strftime('%d/%m/%Y')} | 
                    {int(row.get('daysLeft',0))}j | 
                    {row.get('location','')}
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                if st.button("✅ Terminé", key=f"done_{row['id']}", use_container_width=True):
                    update_task(store_id, row["id"], "done")
                    st.toast("Tâche terminée ✅")
                    st.rerun()
            
            with col_c:
                snooze_label = snoozes[0][0] if snoozes else "Snooze"
                snooze_days = snoozes[0][1] if snoozes else 1
                if st.button(f"⏰ {snooze_label}", key=f"sno_{snooze_label}_{row['id']}", use_container_width=True):
                    update_task(store_id, row["id"], "snoozed", snooze_days)
                    st.toast(f"Rappel dans {snooze_label} ⏰")
                    st.rerun()
            
            st.divider()
    
    # Display stages in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='stage-container'>", unsafe_allow_html=True)
        render_stage("J-21", [("7j", 7), ("3j", 3)])
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='stage-container'>", unsafe_allow_html=True)
        render_stage("J-7", [("2j", 2), ("1j", 1)])
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='stage-container'>", unsafe_allow_html=True)
        render_stage("J-3", [("12h", 0), ("1j", 1)])
        st.markdown("</div>", unsafe_allow_html=True)

# ════════════ TAB 2: ANALYSE ════════════
with tab2:
    st.write("")
    st.subheader("🚨 Lots ≤ 7 jours (FEFO — URGENT)")
    
    if not lots_df.empty:
        urg = lots_df[lots_df["daysLeft"] <= 7].copy().sort_values("expiryDate")
        
        if not urg.empty:
            col_a, col_b = st.columns([2, 1])
            with col_a:
                show = urg[["productId", "lotNumber", "quantity", "expiryDate", "daysLeft", "location"]].rename(
                    columns={
                        "productId": "Produit",
                        "lotNumber": "Lot",
                        "quantity": "Qté",
                        "expiryDate": "DLC",
                        "daysLeft": "Jours",
                        "location": "Rayon"
                    }
                )
                show["DLC"] = pd.to_datetime(show["DLC"]).dt.date
                show["Jours"] = show["Jours"].astype(int).astype(str) + " j"
                
                st.dataframe(show, use_container_width=True, height=300, hide_index=True)
            
            with col_b:
                st.metric("Lots urgents", len(urg))
                st.metric("Valeur à risque", f"€ {urg['quantity'].sum() * 2.5:.0f}")
            
            st.write("")
            st.subheader("📈 Distribution des jours restants")
            fig = px.bar(
                urg,
                x="lotNumber",
                y="daysLeft",
                color="daysLeft",
                color_continuous_scale="RdYlGn_r",
                labels={"lotNumber": "Lot", "daysLeft": "Jours restants"},
                height=400
            )
            fig.update_traces(text=urg["quantity"], textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ Aucun lot critique (tous > 7 jours)")
    else:
        st.warning("⚠️ Aucune donnée de lots pour ce magasin")
    
    st.write("")
    st.divider()
    st.write("")
    
    st.subheader("📧 Digest Email")
    st.caption(f"Destinataire (masqué): **{get_email_recipient()}**")
    
    open_df = tasks_df[(tasks_df["status"] == "open") & (tasks_df["stage"].isin(["J-21", "J-7", "J-3"]))] if not tasks_df.empty else pd.DataFrame()
    
    col_email1, col_email2 = st.columns([3, 1])
    
    with col_email1:
        if st.button("📬 Envoyer le digest maintenant", use_container_width=True, type="primary"):
            try:
                html = email_digest_html(store_id, open_df)
                ok, msg = send_email(f"SmartExpiry — Digest ({len(open_df)} tâches)", html)
                if ok:
                    st.success(msg)
                    mark_email_sent(store_id, True)
                else:
                    st.error(f"❌ {msg}")
                    mark_email_sent(store_id, False, msg)
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
                mark_email_sent(store_id, False, str(e))
    
    with col_email2:
        st.metric("Tâches à envoyer", len(open_df))
    
    # Auto-send
    now = datetime.now(PARIS)
    auto_toggle_val = st.session_state.get("auto_toggle", True)
    
    if auto_toggle_val and not open_df.empty and now.hour >= int(daily_hour):
        if should_auto_send(store_id):
            try:
                html = email_digest_html(store_id, open_df)
                ok, msg = send_email(f"SmartExpiry — Digest Auto ({len(open_df)} tâches)", html)
                if ok:
                    st.success(f"📧 Auto-digest envoyé pour aujourd'hui ✅")
                    mark_email_sent(store_id, True)
                else:
                    st.warning(f"Auto-digest non envoyé: {msg}")
                    mark_email_sent(store_id, False, msg)
            except Exception as e:
                st.warning(f"Auto-digest erreur: {str(e)}")
                mark_email_sent(store_id, False, str(e))

# ════════════ TAB 3: PARAMÈTRES ════════════
with tab3:
    st.subheader("⚙️ Paramètres & Configuration")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown("### 📊 Configuration Active")
        st.write(f"**Magasin**: `{store_id}`")
        st.write(f"**Heure digest**: `{daily_hour:02d}:00` (Paris)")
        st.write(f"**Email**: `{get_email_recipient()}`")
    
    with col_p2:
        st.markdown("### 🔗 Stockage Firestore")
        st.caption("Collections utilisées:")
        st.code("""
stores/{storeId}/lots
stores/{storeId}/tasks
emailLogs/
        """)
    
    st.write("")
    st.divider()
    st.write("")
    
    st.markdown("### 📚 Secrets Streamlit Cloud")
    st.info("""
**À configurer dans Streamlit Cloud → Settings → Secrets:**
Voir le fichier secrets.toml fourni
    """)
    
    st.write("")
    st.markdown("### 💡 Tips")
    st.caption("• Utilise la sidebar pour changer de magasin")
    st.caption("• Les tâches se créent automatiquement au chargement")
    st.caption("• Email digest : manuel ou auto (après l'heure)")
    st.caption("• Snooze pour reporter une tâche (avec rappel)")
