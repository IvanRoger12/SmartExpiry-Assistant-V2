rm /mnt/user-data/outputs/app.py && cat > /mnt/user-data/outputs/app.py << 'EOF'
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from dateutil import tz

st.set_page_config(page_title="SmartExpiry", layout="wide", page_icon="🧊")

st.markdown("""
<style>
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.hero { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); 
        border-radius: 12px; padding: 2rem; color: white; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# HERO
# ═════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
  <h1>🧊 SmartExpiry — Gestion FEFO</h1>
  <p>De 3 semaines à 3 jours : Zéro perte, Marge optimisée</p>
</div>
""", unsafe_allow_html=True)

st.write("**Vérification des connexions...**")

# ═════════════════════════════════════════════════════════════════════════
# TEST FIREBASE
# ═════════════════════════════════════════════════════════════════════════

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    st.write("✅ Firebase admin importé")
    
    if not firebase_admin._apps:
        try:
            config = dict(st.secrets["firebase"])
            
            # Fix private_key
            if "private_key" in config:
                pk = config["private_key"]
                if isinstance(pk, str):
                    pk = pk.replace("\\n", "\n")
                    config["private_key"] = pk
            
            cred = credentials.Certificate(config)
            firebase_admin.initialize_app(cred)
            st.write("✅ Firebase initialisé")
            
            db = firestore.client()
            st.write("✅ Firestore connecté")
            
            # Test simple
            stores = list(db.collection("stores").limit(1).stream())
            st.write(f"✅ Stores trouvés: {len(stores)}")
            
        except Exception as e:
            st.error(f"❌ Firebase error: {str(e)}")
            st.stop()
    else:
        db = firestore.client()
        st.write("✅ Firebase déjà initialisé")
    
except Exception as e:
    st.error(f"❌ Import error: {str(e)}")
    st.stop()

# ═════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════

st.sidebar.title("⚙️ SmartExpiry V2")
store_id = st.sidebar.text_input("Magasin", st.secrets.get("app", {}).get("default_store", "naturalia_nanterre"))

st.write(f"**Magasin sélectionné:** `{store_id}`")

# ═════════════════════════════════════════════════════════════════════════
# KPIs
# ═════════════════════════════════════════════════════════════════════════

st.write("---")
st.subheader("📊 KPIs")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tâches ouvertes", "90")

with col2:
    st.metric("J-3 (URGENT)", "30", delta="-5")

with col3:
    st.metric("Pipeline", "60")

st.write("---")

st.success("✅ App démarrée avec succès!")
st.info("👉 Prochaine étape: Charger les données depuis Firestore")

EOF
cat /mnt/user-data/outputs/app.py | head -50
Sortie

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from dateutil import tz

st.set_page_config(page_title="SmartExpiry", layout="wide", page_icon="🧊")

st.markdown("""
<style>
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
.hero { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); 
        border-radius: 12px; padding: 2rem; color: white; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════
# HERO
# ═════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
  <h1>🧊 SmartExpiry — Gestion FEFO</h1>
  <p>De 3 semaines à 3 jours : Zéro perte, Marge optimisée</p>
</div>
""", unsafe_allow_html=True)

st.write("**Vérification des connexions...**")

# ═════════════════════════════════════════════════════════════════════════
# TEST FIREBASE
# ═════════════════════════════════════════════════════════════════════════

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    st.write("✅ Firebase admin importé")
    
    if not firebase_admin._apps:
        try:
            config = dict(st.secrets["firebase"])
            
            # Fix private_key
            if "private_key" in config:
                pk = config["private_key"]
                if isinstance(pk, str):
                    pk = pk.replace("\\n", "\n")
                    config["private_key"] = pk
            
            cred = credentials.Certificate(config)
