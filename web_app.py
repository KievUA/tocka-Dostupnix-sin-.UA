import streamlit as st
import random
import time

# --- SETUP ---
st.set_page_config(page_title="Brawl Stars 9.0", page_icon="⚡", layout="wide")

# --- ULTRA NEON DESIGN ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle, #000428, #004e92, #000);
        color: #fff;
    }
    .stat-box {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid #00d2ff;
        border-radius: 15px;
        padding: 10px;
        text-align: center;
        font-weight: bold;
    }
    .box-clicker {
        background: linear-gradient(135deg, #f1c40f 0%, #d35400 100%);
        border-radius: 30px;
        padding: 50px;
        text-align: center;
        cursor: pointer;
        border: 4px solid #fff;
        box-shadow: 0 0 30px rgba(241, 196, 15, 0.5);
        transition: 0.3s;
    }
    .box-clicker:active {
        transform: scale(0.9);
    }
    .mega-clicker {
        background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
        box-shadow: 0 0 30px rgba(52, 152, 219, 0.5);
    }
    .brawler-card {
        background: rgba(255,255,255,0.05);
        border-left: 8px solid;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- STATE ---
if 'coins' not in st.session_state: st.session_state.coins = 1000
if 'gems' not in st.session_state: st.session_state.gems = 100
if 'inv' not in st.session_state: st.session_state.inv = []
if 'history' not in st.session_state: st.session_state.history = []

BRAWLERS = {
    "LEON": {"color": "#f1c40f", "rarity": "LEGENDARY"},
    "CROW": {"color": "#f1c40f", "rarity": "LEGENDARY"},
    "SPIKE": {"color": "#f1c40f", "rarity": "LEGENDARY"},
    "MORTIS": {"color": "#e74c3c", "rarity": "MYTHIC"},
    "TARA": {"color": "#e74c3c", "rarity": "MYTHIC"},
    "EDGAR": {"color": "#9b59b6", "rarity": "EPIC"}
}

# --- FUNCTIONS ---
def open_box(box_type):
    with st.spinner("📦 Qutilar silkinmoqda..."):
        time.sleep(1.2)
    
    chance = 0.5 if box_type == "MEGA" else 0.25
    if random.random() < chance:
        name = random.choice(list(BRAWLERS.keys()))
        if name not in st.session_state.inv:
            st.session_state.inv.append(name)
            st.session_state.history.insert(0, f"🌟 YANGI: {name}!")
            st.balloons()
        else:
            st.session_state.coins += 500
            st.session_state.history.insert(0, f"💰 Dublikat {name}: +500!")
    else:
        gain = random.randint(100, 400)
        st.session_state.coins += gain
        st.session_state.history.insert(0, f"💵 Olingan: +{gain} tanga")

# --- UI ---
st.title("⚡ BRAWL STARS: HYPERCHARGE v9.0")

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='stat-box'>💰 TANGALAR: {st.session_state.coins}</div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-box'>💎 GEMLAR: {st.session_state.gems}</div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-box'>👤 JANGCHILAR: {len(st.session_state.inv)}</div>", unsafe_allow_html=True)

st.write("---")

col_play, col_inv = st.columns([1.5, 1])

with col_play:
    st.subheader("📦 QUTI OCHISH (Ustiga bos!)")
    
    b1, b2 = st.columns(2)
    
    with b1:
        st.markdown("<div class='box-clicker'>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 80px;'>🎁</h1>", unsafe_allow_html=True)
        st.write("### BIG BOX")
        if st.button("400 Tanga Sarflash", use_container_width=True):
            if st.session_state.coins >= 400:
                st.session_state.coins -= 400
                open_box("BIG")
                st.rerun()
            else: st.error("Tanga yetarli emas!")
        st.markdown("</div>", unsafe_allow_html=True)

    with b2:
        st.markdown("<div class='box-clicker mega-clicker'>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 80px;'>🔵</h1>", unsafe_allow_html=True)
        st.write("### MEGA BOX")
        if st.button("60 Gem Sarflash", use_container_width=True):
            if st.session_state.gems >= 60:
                st.session_state.gems -= 60
                open_box("MEGA")
                st.rerun()
            else: st.error("Gemlar yetarli emas!")
        st.markdown("</div>", unsafe_allow_
