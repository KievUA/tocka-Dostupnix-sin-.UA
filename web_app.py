import streamlit as st
import random
import time

# --- KONFIGURATSIYA ---
st.set_page_config(page_title="Brawl Stars GOD MODE", page_icon="👑", layout="wide")

# --- ULTRA PREMIUM CSS (Base64 va Neon Effektlar) ---
st.markdown("""
    <style>
    .stApp {
        background: #0a0a0a;
        color: #00ffcc;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Neon ramkalar */
    .stat-card {
        background: rgba(0, 255, 204, 0.05);
        border: 2px solid #00ffcc;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px #00ffcc;
    }
    
    /* Boxlar uchun maxsus dizayn (Rasm o'rniga vizual blok) */
    .box-visual {
        height: 150px;
        background: linear-gradient(45deg, #f1c40f, #d35400);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 80px;
        border: 5px solid #fff;
        box-shadow: 0 0 25px #f1c40f;
        margin-bottom: 10px;
    }
    .mega-visual {
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        box-shadow: 0 0 25px #00d2ff;
    }
    
    /* Jangchi kartochkalari */
    .brawler-card {
        background: #1a1a1a;
        border: 2px solid #555;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        text-align: center;
    }
    .legendary { border-color: #f1c40f; box-shadow: 0 0 10px #f1c40f; }
    .mythic { border-color: #e74c3c; box-shadow: 0 0 10px #e74c3c; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA ---
if 'gold' not in st.session_state: st.session_state.gold = 10000
if 'gems' not in st.session_state: st.session_state.gems = 500
if 'trophies' not in st.session_state: st.session_state.trophies = 0
if 'my_brawlers' not in st.session_state: st.session_state.my_brawlers = {}
if 'event_log' not in st.session_state: st.session_state.event_log = []

BRAWLERS_DB = {
    "LEON": {"rarity": "legendary", "power": 500, "icon": "🦎"},
    "SPIKE": {"rarity": "legendary", "power": 520, "icon": "🌵"},
    "CROW": {"rarity": "legendary", "power": 480, "icon": "🦅"},
    "MORTIS": {"rarity": "mythic", "power": 400, "icon": "🦇"},
    "TARA": {"rarity": "mythic", "power": 390, "icon": "🃏"},
    "EDGAR": {"rarity": "epic", "power": 350, "icon": "🧣"}
}

# --- LOGIKA ---
def open_box(type):
    # Animatsiya simulyatsiyasi
    placeholder = st.empty()
    for i in range(3):
        placeholder.warning(f"📦 Quti silkinmoqda{'.' * (i+1)}")
        time.sleep(0.4)
    placeholder.empty()

    if type == "MEGA":
        chance = 0.6
        st.session_state.gems -= 80
    else:
        chance = 0.25
        st.session_state.gold -= 500

    if random.random() < chance:
        name = random.choice(list(BRAWLERS_DB.keys()))
        if name not in st.session_state.my_brawlers:
            st.session_state.my_brawlers[name] = BRAWLERS_DB[name]
            st.session_state.event_log.insert(0, f"🌟 {name} OCHILDI!")
            st.balloons()
        else:
            st.session_state.gold += 2000
            st.session_state.event_log.insert(0, f"💰 Dublikat {name}: +2000 Oltin!")
    else:
        money = random.randint(300, 800)
        st.session_state.gold += money
        st.session_state.event_log.insert(0, f"💵 Qutidan {money} oltin chiqdi.")

# --- INTERFEYS ---
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>👑 BRAWL STARS: GOD MODE 10.0</h1>", unsafe_allow_html=True)

# Resurslar
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='stat-card'>💰 OLTIN: {st.session_state.gold:,}</div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-card'>💎 GEMLAR: {st.session_state.gems}</div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-card'>🏆 KUBOKLAR: {st.session_state.trophies}</div>", unsafe_allow_html=True)

st.write("---")

col_main, col_inv = st.columns([2, 1])

with col_main:
    st.header("🛒 DO'KON VA JANG")
    
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("<div class='box-visual'>📦</div>", unsafe_allow_html=True)
        if st.button("BIG BOX (500 💰)", use_container_width=True):
            if st.session_state.gold >= 500: open_box("BIG")
            else: st.error("Mablag' yetarli emas!")
            st.rerun()

    with b2:
        st.markdown("<div class='box-visual mega-visual'>🔵</div>", unsafe_allow_html=True)
        if st.button("MEGA BOX (80 💎)", use_container_width=True):
            if st.session_state.gems >= 80: open_box("MEGA")
            else: st.error("Gemlar yetarli emas!")
            st.rerun()

    st.write("---")
    if st.button("🚀 JANGGA KIRISH (PLAY)", use_container_width=True):
        win = random.choice([True, False])
        if win:
            st.session_state.trophies += 10
            st.session_state.gold += 100
            st.success("G'ALABA! +10 Kubok")
        else:
            st.session_state.trophies = max(0, st.session_state.trophies - 5)
            st.error("MAG'LUBIYAT! -5 Kubok")
        st.rerun()

with col_inv:
    st.header("👤 JANGCHILAR")
    if not st.session_state.my_brawlers:
        st.info("Quti oching!")
    else:
        for name, data in st.session_state.my_brawlers.items():
            st.markdown(f"""
                <div class='brawler-card {data['rarity']}'>
                    <h1 style='margin:0;'>{data['icon']}</h1>
                    <h3>{name}</h3>
                    <p>Power: {data['power']}</p>
                </div>
            """, unsafe_allow_html=True)

# Oxirgi voqealar
st.write("---")
st.subheader("📜 VOQEALAR")
for log in st.session_state.event_log[:5]:
    st.text(log)

if st.sidebar.button("RESET ALL"):
    st.session_state.clear()
    st.rerun()
