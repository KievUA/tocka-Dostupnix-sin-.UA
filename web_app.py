import streamlit as st
import random
import time

# --- 1. KONFIGURATSIYA (Eng tepada turishi shart) ---
try:
    st.set_page_config(page_title="Brawl Stars PRO", page_icon="⚡", layout="wide")
except:
    pass

# --- 2. USLUB (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-box {
        background: linear-gradient(145deg, #1e1e2f, #11111d);
        border-radius: 20px; padding: 25px; border: 1px solid #333;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .stat-text { font-size: 20px; font-weight: bold; color: #f1c40f; }
    .brawler-item {
        background: #1a1a1a; border-radius: 12px; padding: 10px;
        margin-bottom: 8px; border-left: 4px solid #f1c40f;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MA'LUMOTLARNI SAQLASH ---
# Xatolik chiqmasligi uchun har bir o'zgaruvchini tekshirib chiqamiz
if 'gold' not in st.session_state: st.session_state.gold = 2000
if 'gems' not in st.session_state: st.session_state.gems = 100
if 'trophies' not in st.session_state: st.session_state.trophies = 0
if 'my_brawlers' not in st.session_state: 
    st.session_state.my_brawlers = {"SHELLY": {"lvl": 1, "pwr": 300, "rarity": "Common"}}
if 'log_history' not in st.session_state: st.session_state.log_history = []

BRAWLERS_LIST = {
    "LEON": {"rarity": "Legendary", "pwr": 500},
    "CROW": {"rarity": "Legendary", "pwr": 480},
    "SPIKE": {"rarity": "Legendary", "pwr": 520},
    "MORTIS": {"rarity": "Mythic", "pwr": 420},
    "EDGAR": {"rarity": "Epic", "pwr": 380}
}

# --- 4. O'YIN FUNKSIYALARI ---
def add_to_log(text):
    st.session_state.log_history.insert(0, f"{time.strftime('%H:%M')} - {text}")

def open_case(cost_type):
    if cost_type == "gold":
        if st.session_state.gold >= 500:
            st.session_state.gold -= 500
        else:
            st.error("Oltin yetarli emas!")
            return
    else:
        if st.session_state.gems >= 80:
            st.session_state.gems -= 80
        else:
            st.error("Gemlar yetarli emas!")
            return

    with st.spinner("📦 Ochilmoqda..."):
        time.sleep(0.5)
        
    luck = random.random()
    if luck < 0.4: # 40% imkoniyat
        new_name = random.choice(list(BRAWLERS_LIST.keys()))
        if new_name not in st.session_state.my_brawlers:
            st.session_state.my_brawlers[new_name] = {
                "lvl": 1, 
                "pwr": BRAWLERS_LIST[new_name]["pwr"],
                "rarity": BRAWLERS_LIST[new_name]["rarity"]
            }
            add_to_log(f"🔥 YANGI: {new_name}!")
            st.balloons()
        else:
            st.session_state.gold += 1000
            add_to_log(f"💰 Dublikat {new_name}: +1000 Oltin")
    else:
        gain = random.randint(100, 500)
        st.session_state.gold += gain
        add_to_log(f"💵 Qutidan {gain} oltin chiqdi.")

# --- 5. ASOSIY INTERFEYS ---
st.title("⚡ BRAWL STARS GOD ENGINE v14")

# Resurslar paneli
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='main-box'><p class='stat-text'>💰 OLTIN</p><h2>{st.session_state.gold}</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='main-box'><p class='stat-text'>💎 GEMLAR</p><h2>{st.session_state.gems}</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='main-box'><p class='stat-text'>🏆 KUBOKLAR</p><h2>{st.session_state.trophies}</h2></div>", unsafe_allow_html=True)

st.write("---")

col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.header("🎁 DO'KON")
    b1, b2 = st.columns(2)
    
    with b1:
        st.subheader("📦 BIG BOX")
        if st.button("500 OLTIN BILAN OCHISH", use_container_width=True):
            open_case("gold")
            st.rerun()
            
    with b2:
        st.subheader("🔵 MEGA BOX")
        if st.button("80 GEM BILAN OCHISH", use_container_width=True):
            open_case("gems")
            st.rerun()

    st.write("---")
    st.header("⚔️ JANG MAYDONI")
    if st.button("🚀 JANGGA KIRISH (PLAY)", use_container_width=True, type="primary"):
        win = random.choice([True, False, True]) # Yutish ehtimoli ko'proq
        if win:
            st.session_state.trophies += 10
            st.session_state.gold += 50
            st.success("G'alaba! +10 Kubok")
        else:
            st.session_state.trophies = max(0, st.session_state.trophies - 5)
            st.error("Mag'lubiyat! -5 Kubok")
        st.rerun()

with col_right:
    st.header("👤 KOLLEKSIYA")
    for name, data in st.session_state.my_brawlers.items():
        st.markdown(f"""
            <div class='brawler-item'>
                <b>{name}</b> ({data['rarity']})<br>
                <small>Power: {data['pwr']} | Level: {data['lvl']}</small>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("---")
    st.header("📜 JURNAL")
    for log in st.session_state.log_history[:5]:
        st.caption(log)

# RESET
if st.sidebar.button("♻️ RESET DATA"):
    st.session_state.clear()
    st.rerun()
