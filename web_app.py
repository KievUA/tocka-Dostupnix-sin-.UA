import streamlit as st
import random
import time

# --- KONFIGURATSIYA ---
st.set_page_config(page_title="Brawl Stars: Legends", page_icon="⚔️", layout="wide")

# --- STYLING (Brawl Stars UI) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    .main-header {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 20px;
        padding: 20px;
        border: 3px solid #f1c40f;
        text-align: center;
        margin-bottom: 20px;
    }
    .brawler-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        border: 2px solid #555;
        transition: 0.3s;
    }
    .brawler-card:hover {
        border-color: #f1c40f;
        transform: scale(1.02);
    }
    .box-container {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 25px;
        padding: 20px;
        text-align: center;
        border: 1px solid #00d2ff;
    }
    .resource-val {
        font-size: 24px;
        font-weight: bold;
        color: #f1c40f;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZATION ---
if 'coins' not in st.session_state: st.session_state.coins = 200
if 'gems' not in st.session_state: st.session_state.gems = 20
if 'inventory' not in st.session_state: 
    st.session_state.inventory = [{"name": "Shelly", "rarity": "Common", "power": 1}]
if 'logs' not in st.session_state: st.session_state.logs = []

# --- BRAWLERS DATA ---
BRAWLERS = [
    {"name": "Colt", "rarity": "Rare", "img": "https://www.google.com/logos/fnbx/brawlstars/colt.png"},
    {"name": "El Primo", "rarity": "Rare", "img": "https://www.google.com/logos/fnbx/brawlstars/el_primo.png"},
    {"name": "Mortis", "rarity": "Mythic", "img": "https://www.google.com/logos/fnbx/brawlstars/mortis.png"},
    {"name": "Leon", "rarity": "Legendary", "img": "https://www.google.com/logos/fnbx/brawlstars/leon.png"},
    {"name": "Crow", "rarity": "Legendary", "img": "https://www.google.com/logos/fnbx/brawlstars/crow.png"},
    {"name": "Spike", "rarity": "Legendary", "img": "https://www.google.com/logos/fnbx/brawlstars/spike.png"}
]

# --- FUNCTIONS ---
def open_box(box_type):
    if box_type == "Mega":
        win_chance = 0.5 # 50% chance for new brawler
        reward_coins = random.randint(100, 300)
    else:
        win_chance = 0.2 # 20% chance
        reward_coins = random.randint(30, 80)
    
    st.session_state.coins += reward_coins
    
    if random.random() < win_chance:
        new_brawler = random.choice(BRAWLERS)
        if not any(b['name'] == new_brawler['name'] for b in st.session_state.inventory):
            st.session_state.inventory.append({"name": new_brawler['name'], "rarity": new_brawler['rarity'], "power": 1})
            st.session_state.logs.insert(0, f"⭐ НОВЫЙ БОЕЦ: {new_brawler['name']}!")
            st.balloons()
        else:
            st.session_state.logs.insert(0, f"💰 Выпало {reward_coins} монет и очки силы.")
    else:
        st.session_state.logs.insert(0, f"💰 Получено {reward_coins} монет.")

# --- UI LAYOUT ---
st.markdown("<div class='main-header'><h1>⭐ BRAWL STARS LOBBY</h1></div>", unsafe_allow_html=True)

# Resources bar
r1, r2, r3, r4 = st.columns(4)
r1.metric("💰 Монеты", f"{st.session_state.coins}")
r2.metric("💎 Гемы", f"{st.session_state.gems}")
r3.metric("👤 Бойцы", f"{len(st.session_state.inventory)}")
r4.button("⚡ ИГРАТЬ", on_click=lambda: st.session_state.update({"coins": st.session_state.coins + 25}))

st.write("---")

col_shop, col_inv = st.columns([1.5, 1])

with col_shop:
    st.subheader("🛒 МАГАЗИН ЯЩИКОВ")
    s1, s2 = st.columns(2)
    
    with s1:
        st.markdown("<div class='box-container'>", unsafe_allow_html=True)
        st.image("https://static.wikia.nocookie.net/brawlstars/images/5/5a/Big_Box.png/revision/latest?cb=20200514170450", width=100)
        st.write("### BIG BOX")
        if st.button("ОТКРЫТЬ (100 💰)", key="big"):
            if st.session_state.coins >= 100:
                st.session_state.coins -= 100
                open_box("Big")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with s2:
        st.markdown("<div class='box-container'>", unsafe_allow_html=True)
        st.image("https://static.wikia.nocookie.net/brawlstars/images/1/14/Mega_Box.png/revision/latest?cb=20200514170535", width=100)
        st.write("### MEGA BOX")
        if st.button("ОТКРЫТЬ (60 💎)", key="mega"):
            if st.session_state.gems >= 60:
                st.session_state.gems -= 60
                open_box("Mega")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📜 Последние события")
    for log in st.session_state.logs[:5]:
        st.write(log)

with col_inv:
    st.subheader("👤 МОИ БОЙЦЫ")
    for b in st.session_state.inventory:
        st.markdown(f"""
            <div class='brawler-card'>
                <h3>{b['name']}</h3>
                <p style='color: #f1c40f;'>{b['rarity']}</p>
                <progress value='{b['power']*10}' max='100' style='width: 100%;'></progress>
            </div>
        """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Настройки")
if st.sidebar.button("Сбросить аккаунт 🔄"):
    st.session_state.clear()
    st.rerun()
