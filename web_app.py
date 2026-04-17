import streamlit as st
import random
import time

# --- SUPREME CONFIG ---
st.set_page_config(page_title="Brawl Stars SUPREME", page_icon="🔱", layout="wide")

# --- SUPREME ENGINE UI (No External Images Needed) ---
st.markdown("""
    <style>
    .stApp {
        background: #020b16;
        color: #f0f0f0;
    }
    /* Animated Header */
    @keyframes shine { 0% {color: #ffd700;} 50% {color: #fff;} 100% {color: #ffd700;} }
    .title-text {
        font-size: 50px; font-weight: 900; text-align: center;
        animation: shine 2s infinite; text-shadow: 0 0 20px #ffd700;
    }
    /* Supreme Box Design */
    .supreme-box {
        height: 200px; border-radius: 30px; margin: 15px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        cursor: pointer; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 4px solid rgba(255,255,255,0.1);
    }
    .supreme-box:hover { transform: scale(1.08) rotate(2deg); border-color: #ffd700; }
    .big-box { background: linear-gradient(135deg, #ff416c, #ff4b2b); box-shadow: 0 15px 35px rgba(255, 75, 43, 0.4); }
    .mega-box { background: linear-gradient(135deg, #4facfe, #00f2fe); box-shadow: 0 15px 35px rgba(79, 172, 254, 0.4); }
    .omega-box { background: linear-gradient(135deg, #667eea, #764ba2); box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4); }
    
    /* Stats Bar */
    .stats-container {
        display: flex; justify-content: space-around; background: rgba(255,255,255,0.05);
        padding: 20px; border-radius: 20px; border: 1px solid #333; margin-bottom: 30px;
    }
    .stat-item { font-size: 22px; font-weight: bold; color: #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'gold' not in st.session_state: st.session_state.gold = 15000
if 'gems' not in st.session_state: st.session_state.gems = 1000
if 'trophies' not in st.session_state: st.session_state.trophies = 0
if 'level' not in st.session_state: st.session_state.level = 1
if 'collection' not in st.session_state: st.session_state.collection = {}

BRAWLERS = {
    "LEON": {"rarity": "Legendary", "icon": "🦎", "color": "#ffd700", "pwr": 800},
    "SPIKE": {"rarity": "Legendary", "icon": "🌵", "color": "#ffd700", "pwr": 820},
    "CROW": {"rarity": "Legendary", "icon": "🦅", "color": "#ffd700", "pwr": 780},
    "MORTIS": {"rarity": "Mythic", "icon": "🦇", "color": "#ff4b2b", "pwr": 600},
    "SURGE": {"rarity": "Chromatic", "icon": "🤖", "color": "#00f2fe", "pwr": 750},
    "FANG": {"rarity": "Epic", "icon": "👟", "color": "#a18cd1", "pwr": 550}
}

# --- FUNCTIONS ---
def open_supreme_box(b_type):
    with st.spinner("🌀 Koinot energiyasi yig'ilmoqda..."):
        time.sleep(1)
    
    if b_type == "MEGA": st.session_state.gems -= 80
    elif b_type == "OMEGA": st.session_state.gems -= 150
    else: st.session_state.gold -= 1000

    luck = random.random()
    chance = 0.7 if b_type == "OMEGA" else (0.4 if b_type == "MEGA" else 0.2)
    
    if luck < chance:
        new = random.choice(list(BRAWLERS.keys()))
        if new not in st.session_state.collection:
            st.session_state.collection[new] = BRAWLERS[new]
            st.session_state.collection[new]['lvl'] = 1
            st.balloons()
            st.toast(f"🎉 {new} OCHILDI!", icon="🔥")
        else:
            st.session_state.gold += 3000
            st.toast(f"💰 Dublikat {new}: +3000 Oltin", icon="💵")
    else:
        bonus = random.randint(500, 2000)
        st.session_state.gold += bonus
        st.toast(f"📦 Qutidan {bonus} oltin chiqdi")

# --- MAIN UI ---
st.markdown("<div class='title-text'>BRAWL STARS: SUPREME 🔱</div>", unsafe_allow_html=True)

# Stats Bar
st.markdown(f"""
    <div class='stats-container'>
        <div class='stat-item'>💰 {st.session_state.gold:,}</div>
        <div class='stat-item'>💎 {st.session_state.gems}</div>
        <div class='stat-item'>🏆 {st.session_state.trophies}</div>
        <div class='stat-item'>🎖️ LVL: {st.session_state.level}</div>
    </div>
    """, unsafe_allow_html=True)

col_shop, col_battle = st.columns([1.5, 1])

with col_shop:
    st.subheader("🏛️ SUPREME SHOP")
    s1, s2, s3 = st.columns(3)
    
    with s1:
        st.markdown("<div class='supreme-box big-box'><h1>🎁</h1><h3>BIG BOX</h3></div>", unsafe_allow_html=True)
        if st.button("1,000 OLTIN", use_container_width=True):
            if st.session_state.gold >= 1000: open_supreme_box("BIG")
            else: st.error("Mablag' yetarli emas!")
            st.rerun()

    with s2:
        st.markdown("<div class='supreme-box mega-box'><h1>🔵</h1><h3>MEGA BOX</h3></div>", unsafe_allow_html=True)
        if st.button("80 GEM", use_container_width=True):
            if st.session_state.gems >= 80: open_supreme_box("MEGA")
            else: st.error("Gemlar yetarli emas!")
            st.rerun()

    with s3:
        st.markdown("<div class='supreme-box omega-box'><h1>🟣</h1><h3>OMEGA BOX</h3></div>", unsafe_allow_html=True)
        if st.button("150 GEM", use_container_width=True):
            if st.session_state.gems >= 150: open_supreme_box("OMEGA")
            else: st.error("Gemlar yetarli emas!")
            st.rerun()

    st.write("---")
    st.subheader("⚔️ MULTIVERSE BATTLE")
    if st.button("🔥 JANGGA KIRISH (PLAY)", use_container_width=True):
        res = random.randint(-10, 30)
        st.session_state.trophies = max(0, st.session_state.trophies + res)
        if res > 0: 
            st.success(f"G'alaba! +{res} Kubok")
            st.session_state.gold += 200
        else: st.error(f"Mag'lubiyat! {res} Kubok")
        st.rerun()

with col_battle:
    st.subheader("👤 SUPREME COLLECTION")
    if not st.session_state.collection:
        st.info("Kolleksiya bo'sh. Quti ochishni boshlang!")
    else:
        for name, data in st.session_state.collection.items():
            st.markdown(f"""
                <div style='background: rgba(255,255,255,0.05); border-left: 5px solid {data['color']}; 
                padding: 15px; border-radius: 15px; margin-bottom: 10px;'>
                    <span style='font-size: 30px;'>{data['icon']}</span>
                    <b style='color: {data['color']}; font-size: 20px;'>{name}</b><br>
                    <small>{data['rarity']} | Power: {data['pwr']}</small>
                </div>
            """, unsafe_allow_html=True)

# Footer
if st.sidebar.button("♻️ FULL RESET"):
    st.session_state.clear()
    st.rerun()
