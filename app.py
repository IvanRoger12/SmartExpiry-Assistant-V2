
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from dateutil import tz
import plotly.express as px
import smtplib
from email.mime.text import MIMEText

# ---------- UI de base ----------
st.set_page_config(page_title="SmartExpiry Assistant — V2", layout="wide")

st.markdown("""
<style>
:root { --brand:#2563eb; }
.block-container { padding-top: 1rem; }
h1 {font-weight:900; letter-spacing:.2px;}
.hero {background:linear-gradient(135deg,#3b82f6 0%,#6366f1 100%); color:#fff; border-radius:16px; padding:18px; box-shadow:0 10px 24px rgba(0,0,0,.18);}
.kpi {background:#fff;border:1px solid #e5e7eb;border-radius:16px;padding:16px;box-shadow:0 8px 24px rgba(0,0,0,.06);transition:transform .15s, box-shadow .15s;}
.kpi:hover {transform:translateY(-2px); box-shadow:0 16px 36px rgba(0,0,0,.12);}
.col-card {background:#fff;border:1px solid #e5e7eb;border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,.06);}
.badge {display:inline-block;padding:2px 10px;border-radius:999px;font-size:12px;font-weight:800}
.badge.red{background:#fee2e2;color:#b91c1c}
.badge.orange{background:#ffedd5;color:#c2410c}
.badge.blue{background:#dbeafe;color:#1d4ed8}
.badge.green{background:#dcfce7;color:#166534}
.btn {border:none;border-radius:10px;padding:8px 12px;font-weight:700}
.btn-blue{background:#2563eb;color:#fff}
.btn-red{background:#dc2626;color:#fff}
.btn-amber{background:#f59e0b;color:#fff}
.btn-gray{background:#6b7280;color:#fff}
.small{color:#9ca3af;font-size:12px}
.table th{font-size:12px;color:#6b7280;text-transform:uppercase}
</style>
""", unsafe_allow_html=True)

# ---------- Firebase ----------
import firebase_admin
from firebase_admin import credentials, firestore

def init_db():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_db()
PARIS = tz.gettz("Europe/Paris")

# ---------- Helpers ----------
def mask_email(addr: str) -> str:
    if not addr or "@" not in addr: return "non défini"
    local, dom = addr.split("@", 1)
    dn, *rest = dom.split(".")
    return f"{local[0]}{'*'*(len(local)-1)}@{dn[0]}{'*'*(len(dn)-1)}{'.'+'.'.join(rest) if rest else ''}"

def ts_to_dt(v):
    if hasattr(v, "to_datetime"):
        return v.to_datetime()
    return v

def days_left(dt_: datetime) -> int:
    return (pd.to_datetime(dt_).date() - date.today()).days

def stage_for_days(d:int) -> str:
    if d <= 7: return "J-3"   # action immédiate
    if d <= 14: return "J-7"  # mise en avant / -20%
    if d <= 21: return "J-21" # planifier promo
    return "Hors tunnel"

def stage_label(stage:str) -> str:
    return {"J-21":"À 3 semaines — Planifier une promotion",
            "J-7":"À 1 semaine — Mettre en avant / -20%",
            "J-3":"À 3 jours — Action immédiate / -50%",
            "Hors tunnel":"> 3 semaines"}[stage]

def stage_badge(stage:str) -> str:
    return {"J-21":'<span class="badge blue">J-21</span>',
            "J-7": '<span class="badge orange">J-7</span>',
            "J-3": '<span class="badge red">J-3</span>',
            "Hors tunnel":'<span class="badge green">OK</span>'}[stage]

# ---------- Data load ----------
@st.cache_data(ttl=30)
def load_lots(store_id:str) -> pd.DataFrame:
    lots=[]
    # sous-collection
    try:
        for doc in db.collection("stores").document(store_id).collection("lots").stream():
            d=doc.to_dict(); d["id"]=doc.id
            d["expiryDate"]=ts_to_dt(d.get("expiryDate"))
            d["receivedAt"]=ts_to_dt(d.get("receivedAt"))
            lots.append(d)
    except Exception:
        pass
    # racine (fallback)
    if not lots:
        q=db.collection("lots")
        try: q=q.where("storeId","==",store_id)
        except: pass
        for doc in q.stream():
            d=doc.to_dict(); d["id"]=doc.id
            d["expiryDate"]=ts_to_dt(d.get("expiryDate"))
            d["receivedAt"]=ts_to_dt(d.get("receivedAt"))
            lots.append(d)
    df=pd.DataFrame(lots) if lots else pd.DataFrame(columns=["id","productId","lotNumber","quantity","expiryDate","location"])
    if not df.empty:
        df["expiryDate"]=pd.to_datetime(df["expiryDate"])
        df["days_left"]=df["expiryDate"].apply(days_left)
        df["stage"]=df["days_left"].apply(stage_for_days)
    return df

def tasks_col(store_id:str):
    return db.collection("stores").document(store_id).collection("tasks")

def task_id_for(lot_id:str, stage:str)->str:
    return f"TASK_{lot_id}_{stage}"

def ensure_tasks_for_store(store_id:str, df:pd.DataFrame)->int:
    if df.empty: return 0
    col=tasks_col(store_id)
    count=0
    for _, r in df.iterrows():
        if r["stage"]=="Hors tunnel": continue
        tid=task_id_for(r["id"], r["stage"])
        payload={
            "id": tid,
            "lotId": r["id"],
            "productId": r.get("productId"),
            "lotNumber": r.get("lotNumber"),
            "stage": r["stage"],
            "stageLabel": stage_label(r["stage"]),
            "daysLeft": int(r["days_left"]),
            "quantity": int(r.get("quantity",0)) if pd.notna(r.get("quantity")) else 0,
            "expiryDate": r["expiryDate"].to_pydatetime(),
            "location": r.get("location",""),
            "status": "open",
            "snoozedUntil": None,
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP,
        }
        col.document(tid).set(payload, merge=True)
        count+=1
    return count

def get_tasks(store_id:str)->pd.DataFrame:
    docs=list(tasks_col(store_id).stream())
    if not docs: return pd.DataFrame(columns=["id","stage","status"])
    rec=[d.to_dict()|{"id":d.id} for d in docs]
    df=pd.DataFrame(rec)
    if "expiryDate" in df.columns:
        df["expiryDate"]=pd.to_datetime(df["expiryDate"].apply(lambda x: x if isinstance(x,datetime) else ts_to_dt(x)))
    return df

def update_task_status(store_id:str, tid:str, status:str, snooze_days:int=None):
    ref=tasks_col(store_id).document(tid)
    data={"status":status, "updatedAt":firestore.SERVER_TIMESTAMP}
    if snooze_days is not None:
        data["snoozedUntil"]=datetime.now(PARIS)+timedelta(days=snooze_days)
    ref.set(data, merge=True)

# ---------- Emails ----------
def send_email(subject:str, html:str):
    cfg=st.secrets["email"]
    msg=MIMEText(html,"html","utf-8")
    msg["Subject"]=subject
    msg["From"]=cfg.get("from")
    msg["To"]=cfg.get("to")
    with smtplib.SMTP(cfg.get("host"), int(cfg.get("port"))) as s:
        if cfg.get("use_tls", True): s.starttls()
        if cfg.get("username") and cfg.get("password"): s.login(cfg["username"], cfg["password"])
        s.sendmail(msg["From"], [msg["To"]], msg.as_string())

def masked_to(): return mask_email(st.secrets["email"].get("to"))

def email_html_digest(store_id:str, tasks_df:pd.DataFrame)->str:
    rows=[]
    for stage in ["J-21","J-7","J-3"]:
        sub=tasks_df[(tasks_df["stage"]==stage)&(tasks_df["status"]=="open")]
        if sub.empty: continue
        rows.append(f"<h3>{stage_label(stage)}</h3>")
        rows.append("<table style='width:100%;border-collapse:collapse;border:1px solid #e5e7eb;border-radius:8px;overflow:hidden;'>"
                    "<thead><tr style='background:#f9fafb'>"
                    "<th style='padding:10px;text-align:left;font-size:12px;color:#6b7280'>Produit</th>"
                    "<th style='padding:10px;text-align:left;font-size:12px;color:#6b7280'>Lot</th>"
                    "<th style='padding:10px;text-align:left;font-size:12px;color:#6b7280'>Qté</th>"
                    "<th style='padding:10px;text-align:left;font-size:12px;color:#6b7280'>DLC</th>"
                    "<th style='padding:10px;text-align:left;font-size:12px;color:#6b7280'>Jours</th>"
                    "<th style='padding:10px;text-align:left;font-size:12px;color:#6b7280'>Rayon</th>"
                    "</tr></thead><tbody>")
        for _, r in sub.sort_values("expiryDate").iterrows():
            rows.append(f"<tr style='border-bottom:1px solid #e5e7eb'>"
                        f"<td style='padding:10px'>{r.get('productId','')}</td>"
                        f"<td style='padding:10px;font-weight:700;color:#111827'>{r.get('lotNumber','')}</td>"
                        f"<td style='padding:10px'>{int(r.get('quantity',0))}</td>"
                        f"<td style='padding:10px'>{pd.to_datetime(r['expiryDate']).date().strftime('%d/%m/%Y')}</td>"
                        f"<td style='padding:10px'>{int(r.get('daysLeft',0))}</td>"
                        f"<td style='padding:10px'>{r.get('location','')}</td>"
                        "</tr>")
        rows.append("</tbody></table><br/>")
    body="".join(rows) if rows else "<p>Toutes les tâches sont à jour ✅</p>"
    return f"""
    <!doctype html><html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f3f4f6;margin:0;">
      <div style="max-width:640px;margin:0 auto;background:#fff;">
        <div style="background:linear-gradient(135deg,#3b82f6 0%,#6366f1 100%);padding:22px;color:#fff;border-radius:0;">
          <h2 style="margin:0">SmartExpiry Assistant — Digest quotidien</h2>
          <div style="opacity:.9">Magasin: {store_id}</div>
        </div>
        <div style="padding:20px">{body}
          <div style="text-align:center;margin-top:18px;">
            <a href="#" style="display:inline-block;background:#2563eb;color:#fff;padding:10px 18px;border-radius:8px;text-decoration:none;font-weight:800">Ouvrir le workflow →</a>
          </div>
        </div>
        <div style="background:#f9fafb;padding:14px;text-align:center;color:#6b7280;font-size:12px;border-top:1px solid #e5e7eb">
          SmartExpiry · Optimisation FEFO & marges
        </div>
      </div>
    </body></html>
    """

def should_send_today(store_id:str)->bool:
    today=datetime.now(PARIS).strftime("%Y-%m-%d")
    doc_id=f"DIGEST_{store_id}_{today}"
    ref=db.collection("emailLogs").document(doc_id)
    if ref.get().exists: return False
    ref.set({"storeId":store_id,"date":today,"createdAt":firestore.SERVER_TIMESTAMP,"source":"streamlit","status":"scheduled"})
    return True

def mark_sent(store_id:str, ok:bool, err:str=""):
    today=datetime.now(PARIS).strftime("%Y-%m-%d")
    doc_id=f"DIGEST_{store_id}_{today}"
    db.collection("emailLogs").document(doc_id).set({
        "sentAt":firestore.SERVER_TIMESTAMP,"status":"sent" if ok else "error","error":err
    }, merge=True)

# ---------- Sidebar ----------
brand=st.secrets["app"].get("brand","SmartExpiry Assistant")
default_store=st.secrets["app"].get("default_store","store-demo")
daily_hour=int(st.secrets["app"].get("daily_send_hour",8))

st.sidebar.title(brand)
store_id=st.sidebar.text_input("Magasin (storeId)", default_store)
st.sidebar.write(f"📧 Destinataire: **{masked_to()}** (masqué)")
auto_toggle=st.sidebar.toggle("Envoi auto du digest (quand l'app est ouverte après l'heure)", value=True)

# ---------- Header ----------
st.markdown(f"""
<div class="hero">
  <div style="display:flex;justify-content:space-between;align-items:center;">
    <div>
      <div style="opacity:.9;font-weight:700">Assistant V2 — Tunnel d'actions</div>
      <h1 style="margin:6px 0 0 0;">De 3 semaines à 3 jours : zéro perte, marge optimisée</h1>
      <div class="small">Workflow : J-21 → J-7 → J-3, Snooze & Rappels automatiques</div>
    </div>
    <div style="font-weight:800;">{datetime.now(PARIS).strftime('%d %b %Y — %H:%M')}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- Lots -> Tâches ----------
lots_df=load_lots(store_id)
_ = ensure_tasks_for_store(store_id, lots_df)
tasks_df=get_tasks(store_id)

# KPI
open_tasks=len(tasks_df[(tasks_df["status"]=="open") & (tasks_df["stage"]!="Hors tunnel")]) if not tasks_df.empty else 0
urgent_now=len(tasks_df[(tasks_df["stage"]=="J-3") & (tasks_df["status"]=="open")]) if not tasks_df.empty else 0
pipeline=len(tasks_df[(tasks_df["stage"].isin(["J-21","J-7"])) & (tasks_df["status"]=="open")]) if not tasks_df.empty else 0

c1,c2,c3=st.columns(3)
with c1: st.markdown(f'<div class="kpi"><div class="small">Tâches ouvertes</div><div class="v">{open_tasks}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="kpi"><div class="small">Action immédiate (J-3)</div><div class="v">{urgent_now}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="kpi"><div class="small">En préparation (J-21/J-7)</div><div class="v">{pipeline}</div></div>', unsafe_allow_html=True)

st.divider()

# ---------- Colonnes par étape ----------
def stage_block(stage_key:str, snoozes:list):
    st.markdown(f"### {stage_badge(stage_key)} {stage_label(stage_key)}", unsafe_allow_html=True)
    sub=tasks_df[(tasks_df["stage"]==stage_key)]
    if sub.empty:
        st.info("Aucune tâche.")
        return
    sub=sub.sort_values("expiryDate")
    for _, r in sub.iterrows():
        status = r.get("status","open")
        if status=="done":
            st.markdown(f"✅ **{r.get('productId','')}** · Lot **{r.get('lotNumber','')}** — *Terminé*")
            continue
        if status=="snoozed" and r.get("snoozedUntil"):
            until=pd.to_datetime(r["snoozedUntil"]).strftime("%d/%m %H:%M")
            st.markdown(f"🕒 **{r.get('productId','')}** · Lot **{r.get('lotNumber','')}** — *Rappel le {until}*")
            continue

        colA,colB,colC=st.columns([3,2,2])
        with colA:
            st.markdown(f"**{r.get('productId','')}** · Lot **{r.get('lotNumber','')}**")
            st.caption(f"DLC {pd.to_datetime(r['expiryDate']).date().strftime('%d/%m/%Y')} • {int(r.get('daysLeft',0))} j • {r.get('location','')}")
        with colB:
            if st.button("Terminé", key=f"done_{r['id']}", type="primary"):
                update_task_status(store_id, r["id"], "done")
                st.toast("Tâche terminée ✅"); st.rerun()
        with colC:
            for label, d in snoozes:
                if st.button(f"Snooze {label}", key=f"sno_{label}_{r['id']}"):
                    update_task_status(store_id, r["id"], "snoozed", snooze_days=d)
                    st.toast(f"Rappel dans {label} ⏰"); st.rerun()
        st.markdown("---")

col1,col2,col3=st.columns(3)
with col1:
    stage_block("J-21",[("7j",7),("3j",3)])
with col2:
    stage_block("J-7",[("2j",2),("1j",1)])
with col3:
    stage_block("J-3",[("12h",0),("1j",1)])

st.divider()

# ---------- Vue tableau urgences + chart ----------
if not lots_df.empty:
    urg=lots_df[lots_df["days_left"]<=7].copy().sort_values("expiryDate")
    if not urg.empty:
        show=urg[["productId","lotNumber","quantity","expiryDate","days_left","location"]].rename(
            columns={"productId":"Produit","lotNumber":"Lot","quantity":"Qté","expiryDate":"DLC","days_left":"Jours","location":"Rayon"}
        )
        show["DLC"]=pd.to_datetime(show["DLC"]).dt.date
        show["Jours"]=show["Jours"].astype(int).astype(str)+" j"
        st.subheader("📋 Lots ≤ 7 jours (FEFO)")
        st.dataframe(show, use_container_width=True, height=320)

        st.subheader("📈 Jours restants par lot")
        fig=px.bar(urg, x="lotNumber", y="days_left", text="quantity", color="days_left", color_continuous_scale="RdYlGn_r",
                   labels={"lotNumber":"Lot","days_left":"Jours restants"})
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

# ---------- Emails : digest manuel + auto ----------
st.subheader("📧 Digest email")
st.caption(f"Destinataire (masqué) : **{masked_to()}**")
digest_btn=st.button("Envoyer le digest maintenant")
open_df=tasks_df[(tasks_df["status"]=="open") & (tasks_df["stage"].isin(["J-21","J-7","J-3"]))]

if digest_btn:
    try:
        html=email_html_digest(store_id, open_df)
        send_email(f"SmartExpiry Assistant — Digest ({len(open_df)} tâches ouvertes)", html)
        st.success("Email envoyé ✅")
    except Exception as e:
        st.error(f"Échec envoi : {e}")

# auto (si app ouverte après daily_hour)
now=datetime.now(PARIS)
auto_toggle = st.session_state.get("auto_toggle", True)
if auto_toggle and len(open_df)>0 and now.hour>=int(daily_hour):
    # éviter doublons via log Firestore
    def should_send_today(store_id:str)->bool:
        today=datetime.now(PARIS).strftime("%Y-%m-%d")
        doc_id=f"DIGEST_{store_id}_{today}"
        ref=db.collection("emailLogs").document(doc_id)
        if ref.get().exists: return False
        ref.set({"storeId":store_id,"date":today,"createdAt":firestore.SERVER_TIMESTAMP,"source":"streamlit","status":"scheduled"})
        return True

    if should_send_today(store_id):
        try:
            html=email_html_digest(store_id, open_df)
            send_email(f"SmartExpiry Assistant — Digest ({len(open_df)} tâches ouvertes)", html)
            st.success("📧 Digest auto envoyé pour aujourd’hui ✅")
        except Exception as e:
            st.warning(f"Auto-envoi non réalisé : {e}")
