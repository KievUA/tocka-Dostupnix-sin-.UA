import streamlit as st
import random
import time
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars OMNI RU", page_icon="💣", layout="wide")

# --- 2. SUPREME NEON CSS ---
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; font-family: 'Orbitron', sans-serif; }
    .status-bar {
        background: rgba(30, 41, 59, 0.8);
        border: 2px solid #00ffcc; border-radius: 15px; padding: 15px;
        display: flex; justify-content: space-around; margin-bottom: 25px;
    }
    .box-card {
        background: #1e293b; border: 2px solid #334155;
        border-radius: 15px; padding: 15px; text-align: center;
        transition: 0.3s; margin-bottom: 10px;
    }
    .box-card:hover { border-color: #ff0055; transform: scale(1.02); }
    .pass-container {
        background: rgba(15, 23, 42, 0.9);
        border: 2px solid #6200ff; border-radius: 20px; padding: 20px;
    }
    .tier-card {
        background: #0f172a; border-radius: 10px; padding: 10px;
        margin-bottom: 10px; border-left: 5px solid #6200ff;
    }
    .brawler-card {
        background: #0f172a; border: 1px solid #1e293b;
        border-radius: 12px; padding: 10px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INITIAL STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'trophies': 0, 'xp': 0,
        'inv': {"Шелли": {"lvl": 1, "pwr": 300, "icon": "🔫", "rarity": "Начальный"}},
        'claimed': [], 'plus': False
    })

BRAWLERS_DB = {
    "Леон": {"rarity": "Легендарный", "pwr": 600, "icon": "🦎"},
    "Ворон": {"rarity": "Легендарный", "pwr": 580, "icon": "🦅"},
    "Спайк": {"rarity": "Легендарный", "pwr": 620, "icon": "🌵"},
    "Мортис": {"rarity": "Мифический", "pwr": 500, "icon": "🦇"}
}

# 15 ta darajali Brawl Pass (Oxiri 400,000 Gold)
PASS_TIERS = {
    1: {"xp": 500, "reward": "1,000 Золота", "val": 1000, "type": "gold"},
    2: {"xp": 2000, "reward": "50 Гемов", "val": 50, "type": "gems"},
    3: {"xp": 5000, "reward": "2,500 Золота", "val": 2500, "type": "gold"},
    5: {"xp": 15000, "reward": "100 Гемов", "val": 100, "type": "gems"},
    7: {"xp": 40000, "reward": "5,000 Золота", "val": 5000, "type": "gold"},
    10: {"xp": 100000, "reward": "PLUS: 20,000 Золота", "val": 20000, "type": "gold"},
    12: {"xp": 200000, "reward": "PLUS: 50,000 Золота", "val": 50000, "type": "gold"},
    15: {"xp": 400000, "reward": "ФИНАЛ PLUS: 400,000 ЗОЛОТА", "val": 400000, "type": "gold"}
}

# --- 4. LOGIC ---
def open_box(cost, brawler_chance):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        with st.spinner("📦 Открытие..."):
            time.sleep(0.7)
            if random.random() < brawler_chance:
                name = random.choice(list(BRAWLERS_DB.keys()))
                if name not in st.session_state.inv:
                    st.session_state.inv[name] = BRAWLERS_DB[name]
                    st.session_state.inv[name]['lvl'] = 1
                    st.balloons()
                    st.success(f"🔥 НОВЫЙ БОЕЦ: {name}!")
                else:
                    st.session_state.gold += (cost * 2)
                    st.info(f"💰 Дубли
