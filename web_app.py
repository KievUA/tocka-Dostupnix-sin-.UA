import streamlit as st
import time

# Sayt sozlamalari
st.set_page_config(page_title="Oltin Magnati 2.0 💎", page_icon="💰", layout="centered")

# --- STYLING (Professional ko'rinish) ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .gold-text { color: #FFD700; font-size: 50px; font-weight: bold; text-align: center; text-shadow: 2px 2px #DAA520; }
    .stButton>button {
        width: 100%; border-radius: 50px; height: 80px; font-size: 25px !important;
        font-weight: bold; transition: 0.3s; border: 3px solid #FFD700;
    }
    .stButton>button:hover { transform: scale(1.05); background-color: #FFD700; color: black; }
    .shop-card { background-color: #262730; padding: 15px; border-radius: 15px; border-left: 5px solid #FFD700; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- O'YIN HOLATINI BOSHQARISH ---
if 'gold' not in st.session_state:
    st.session_state.gold = 0
if 'multiplier' not in st.session_state:
    st.session_state.multiplier = 1
if 'auto_income' not in st.session_state:
    st.session_state.auto_income = 0
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# Avtomatik hisoblash
now = time.time()
diff = now - st.session_state.last_update
if diff >= 1:
    st.session_state.gold += int(diff * st.session_state.auto_income)
    st.session_state.last_update = now

# --- ASOSIY EKRAN ---
st.markdown(f"<p class='gold-text'>{st.session_state.gold} 💰</p>", unsafe_allow_html=True)

# Progress bar (Maqsad: 1 million oltin)
progress = min(st.session_state.gold / 1000000, 1.0)
st.write(f"Millonergacha progress: {int(progress*100)}%")
st.progress(progress)

if st.button("OLTIN QAZIB OLISH ⛏️"):
    st.session_state.gold += (1 * st.session_state.multiplier)
    st.rerun()

st.write("---")

# --- DO'KON (UPGRADES) ---
st.header("Sotib olish va Kuchaytirish 🛒")
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='shop-card'>", unsafe_allow_html=True)
    st.subheader("X2 Multiplikator ⚡")
    x2_cost = 100 * st.session_state.multiplier
    st.write(f"Har bir bosishni {st.session_state.multiplier * 2} marta kuchaytiradi.")
    if st.button(f"{x2_cost} 💰 bilan olish"):
        if st.session_state.gold >= x2_cost:
            st.session_state.gold -= x2_cost
            st.session_state.multiplier *= 2
            st.balloons()
            st.rerun()
        else:
            st.error("Pul yetarli emas!")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='shop-card'>", unsafe_allow_html=True)
    st.subheader("Avto-Kombayn 🚜")
    auto_cost = 50 * (st.session_state.auto_income + 1)
    st.write(f"Sekundiga +{st.session_state.auto_income + 1} oltin keltiradi.")
    if st.button(f"{auto_cost} 💰 bilan yollash"):
        if st.session_state.gold >= auto_cost:
            st.session_state.gold -= auto_cost
            st.session_state.auto_income += 5
            st.snow()
            st.rerun()
        else:
            st.error("Pul yetarli emas!")
    st.markdown("</div>", unsafe_allow_html=True)

# --- STATISTIKA (YON PANEL) ---
st.sidebar.title("Sizning Biznesingiz 💼")
st.sidebar.metric("Har bir bosish", f"{st.session_state.multiplier} 💰")
st.sidebar.metric("Avto-daromad", f"{st.session_state.auto_income} 💰/sek")

if st.sidebar.button("Hamma narsani sotish (Reset)"):
    st.session_state.clear()
    st.rerun()
