import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars FIX", page_icon="🔱", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #001220 0%, #000000 100%); color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .status-bar { background: rgba(0,0,0,0.8); border: 2px solid #00ffcc; border-radius: 50px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 20px;}
    .box-card { background: rgba(10,10,10,0.9); border: 1px solid #333; border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 10px; }
    .event-card { background: linear-gradient(135deg, #ff0055 0%, #6200ff 100%); border-radius: 20px; padding: 20px; text-align: center; border: 2px solid white; margin-bottom: 15px;}
    .brawler-card { background: #050505; border: 1px solid #00ffcc; border-radius: 10px; padding: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'gold' not in st.session_state:
    st.session_state.gold = 0
    st.session_state.gems = 0
    st.session_state.trophies = 0
    st.session_state.xp = 0
    st.session_state.inv = {"Шелли": {"lvl": 1, "pwr": 300, "icon": "🔫", "rank": "BRONZE III"}}
    st.session_state.claimed = []
    st.session_state.plus = False

# --- 4. CORE FUNCTIONS ---
def open_box(cost, chance):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        with st.spinner("📦..."):
            time.sleep(0.5)
            if random.random() < chance:
                st.balloons()
                st.success("🔥 НОВЫЙ БОЕЦ!")
                st.session_state.gold += 500 
            else:
                gain = random.randint(int(cost*0.4), int(cost*0.8))
                st.session_state.gold += gain
                st.toast(f"+{gain} 💰")
    else:
        st.error(f"Нужно {cost} золота!")

# --- 5. UI ---
st.markdown("<h1 style='text-align: center;'>BRAWL STARS v19.0</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class="status-bar">
    <span>💰 {st.session_state.gold:,}</span>
    <span>💎 {st.session_state.gems}</span>
    <span>🏆 {st.session_state.trophies}</span>
</div>""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1.3])

with c1:
    st.header("🛒 SHOP")
    # Mega Box (10,000)
    st.markdown("<div class='event-card'><h3>MEGA ULTRA</h3><p>10,000 💰</p><small>24 ЧАСА</small></div>", unsafe_allow_html=True)
    if st.button("OPEN MEGA", use_container_width=True):
        open_box(10000, 0.6)
        st.rerun()
    
    # Standard Boxes
    for cost in [500, 1000, 3000]:
        st.markdown(f"<div class='box-card'><h3>BOX {cost}</h3></div>", unsafe_allow_html=True
