import streamlit as st
import time

# Sayt sozlamalari
st.set_page_config(page_title="Oltin Konchisi 💰", page_icon="⛏️", layout="centered")

# --- STYLING ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 100px;
        font-size: 40px !important;
        background-color: #FFD700;
        border: 5px solid #DAA520;
        border-radius: 20px;
    }
    .stats-box {
        background-color: #1E1E1E;
        color: #FFD700;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- O'YIN HOLATI ---
if 'gold' not in st.session_state:
    st.session_state.gold = 0
if 'click_power' not in st.session_state:
    st.session_state.click_power = 1
if 'auto_miners' not in st.session_state:
    st.session_state.auto_miners = 0
if 'last_time' not in st.session_state:
    st.session_state.last_time = time.time()

# Avtomatik oltin yig'ish hisob-kitobi
current_time = time.time()
time_diff = current_time - st.session_state.last_time
if time_diff >= 1:
    st.session_state.gold += int(time_diff * st.session_state.auto_miners)
    st.session_state.last_time = current_time

# --- INTERFEYS ---
st.title("⛏️ Oltin Konchisi Imperiyasi")

# Oltin ko'rsatkichi
st.markdown(f"<div class='stats-box'>Sizning Oltinlaringiz: {st.session_state.gold} 💰</div>", unsafe_allow_html=True)

# ASOSIY TUGMA
if st.button("URISH! 🔨"):
    st.session_state.gold += st.session_state.click_power
    st.rerun()

st.write("---")

# DO'KON (UPGRADES)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Do'kon 🛒")
