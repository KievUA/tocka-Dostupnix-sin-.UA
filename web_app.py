import streamlit as st
import random
import time
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars OMNI RU", page_icon="💣", layout="wide")

# --- 2. ULTIMATE NEON CSS ---
st.markdown("""
    <style>
    .stApp { background: #010101; color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .main-card {
        background: rgba(0, 20, 40, 0.9);
        border: 2px solid #00ffcc; border-radius: 25px;
        padding: 25px; box-shadow: 0 0 30px rgba(0, 255, 204, 0.3);
    }
    .resource-bar {
        display: flex; justify-content: space-around;
        background: #000; border: 2px solid #00ffcc;
        border-radius: 50px; padding: 15px; margin-bottom: 20px;
    }
    .box-card {
        background: #0a0a0a; border: 2px solid #333;
        border-radius: 15px; padding: 15px; text-align: center;
        transition: 0.3s; margin-bottom: 10px;
    }
    .box-card:hover { border-color: #ff0055; transform: translateY(-5px); }
    .brawler-box {
        background: #050505; border: 1px solid #333;
        border-radius: 15px; padding: 15px; transition: 0.3s;
    }
    .plus-banner {
        background: linear-gradient(135deg, #6200ff, #ff0055);
        color: white; border-radius: 15px; padding: 10px; text-align: center;
        font-weight: bold; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE INITIALIZATION ---
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
    "Мортис": {"rarity": "Мифический", "pwr": 500, "icon": "🦇"},
    "Вольт": {"rarity": "Хроматический", "pwr": 550, "icon": "🤖"}
}

PASS_TIERS = {
    1: {"xp": 500, "reward": "1,000 Золота", "val": 1000, "type": "gold"},
    3: {"xp": 5000, "reward": "100 Гемов", "val": 100, "type": "gems"},
    10: {"xp": 100000, "reward": "PLUS: 50,000 Золота", "val": 50000, "type": "gold"},
    15: {"xp": 400000, "reward": "ФИНАЛ: 400,000 ЗОЛОТА", "val": 400000, "type": "gold"}
}

# --- 4. FUNCTIONS ---
def open_box(cost, chance):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        with st.spinner("📦 Открытие ящика..."):
            time.sleep(0.8)
            if random.random() < chance:
                name = random.choice(list(BRAWLERS_DB.keys()))
                if name not in st.session_state.inv:
                    st.session_state.inv[name] = BRAWLERS_DB[name]
                    st.session_state.inv[name]['lvl'] = 1
                    st.balloons()
                    st.success(f"🔥 НОВЫЙ БОЕЦ: {name.upper()}!")
                else:
                    refund = cost * 2
                    st.session_state.gold += refund
                    st.info(f"💰 Дубликат! Возвращено {refund} золота.")
            else:
                gain = random.randint(int(cost*0.2), int(cost*0.8))
                st.session_state.gold += gain
                st.toast(f"📦 Награда: +{gain} золота")
    else:
        st.error("Недостаточно золота!")

def save_game():
    data = {
        "gold": st.session_state.gold, "gems": st.session_state.gems,
        "trophies": st.session_state.trophies, "xp": st.session_state.xp,
        "inv": st.session_state.inv, "claimed": st.session_state.claimed,
        "plus": st.session_state.plus
    }
    st.session_state.save_code = base64.b64encode(str(data).encode()).decode()

# --- 5. UI LAYOUT ---
st.markdown("<h1 style='text-align: center;'>💣 BRAWL STARS: OMNI v18.2 💣</h1>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="resource-bar">
        <span>💰 ЗОЛОТО: {st.session_state.gold:,}</span>
        <span>💎 ГЕМЫ: {st.session_state.gems}</span>
        <span>🏆 КУБКИ: {st.session_state.trophies}</span>
    </div>
    """, unsafe_allow_html=True)

col_shop, col_battle, col_pass = st.columns([1, 1, 1.2])

with col_shop:
    st.header("🛒 Магазин")
    
    # 500 Coin Box
    st.markdown("<div class='box-card'><h3>📦 Малый ящик</h3><p>500 💰</p></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ (500)", key="b500", use_container_width=True):
        open_
