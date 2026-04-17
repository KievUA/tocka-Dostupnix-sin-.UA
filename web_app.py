import streamlit as st
import random
import time

# --- 1. ENGINE CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars GOD ENGINE", page_icon="🔱", layout="wide")

# --- 2. THE "SUPREME" VISUALS (CSS) ---
st.markdown("""
    <style>
    .stApp { background: #000428; color: white; font-family: 'Tahoma', sans-serif; }
    
    /* Stats Header */
    .header-card {
        background: linear-gradient(90deg, #004e92, #000428);
        padding: 20px; border-radius: 20px; border: 2px solid #00d2ff;
        text-align: center; box-shadow: 0 0 20px rgba(0, 210, 255, 0.4);
    }
    .stat-val { font-size: 24px; font-weight: bold; color: #f1c40f; margin: 0 15px; }

    /* Brawl Pass Section */
    .pass-container {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #9b59b6; border-radius: 15px; padding: 15px;
    }
    .pass-tier {
        background: #1a1a1a; padding: 10px; margin: 5px 0;
        border-radius: 10px; border-left: 5px solid #9b59b6;
        display: flex; justify-content: space-between; align-items: center;
    }
    .tier-claimed { border-left-color: #2ecc71; opacity: 0.6; }

    /* Brawler Cards */
    .b-card {
        background: #0d1117; border: 2px solid #30363d;
        border-radius: 15px; padding: 15px; margin-bottom: 10px;
        transition: 0.3s;
    }
    .b-card:hover { border-color: #f1c40f; transform: translateY(-5px); }
    .legendary { border-color: #f1c40f; box-shadow: 0 0 10px #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SYSTEM CORE ---
if 'gold' not in st.session_state: st.session_state.gold = 3000
if 'gems' not in st.session_state: st.session_state.gems = 150
if 'trophies' not in st.session_state: st.session_state.trophies = 0
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'inv' not in st.session_state: 
    st.session_state.inv = {"Shelly": {"lvl": 1, "pwr": 300, "rarity": "Common", "icon": "🔫"}}
if 'claimed_tiers' not in st.session_state: st.session_state.claimed_tiers = []

BRAWLERS_DB = {
    "Leon": {"rarity": "Legendary", "pwr": 550, "icon": "🦎"},
    "Crow": {"rarity": "Legendary", "pwr": 520, "icon": "🦅"},
    "Mortis": {"rarity": "Mythic", "pwr": 450, "icon": "🦇"},
    "Tara": {"rarity": "Mythic", "pwr": 430, "icon": "🃏"},
    "Edgar": {"rarity": "Epic", "pwr": 400, "icon": "🧣"}
}

PASS_REWARDS = {
    1: {"xp": 500, "reward": "500 Gold", "type": "gold", "amt": 500},
    2: {"xp": 1200, "reward": "50 Gems", "type": "gems", "amt": 50},
    3: {"xp": 2500, "reward": "Mega Box", "type": "box", "amt": 1},
    4: {"xp": 4000, "reward": "1000 Gold", "type": "gold", "amt": 1000},
    5: {"xp": 6000, "reward": "Legendary Brawler", "type": "brawler", "amt": 1}
}

# --- 4. GAME LOGIC ---
def open_box(box_type):
    if box_type == "Mega":
        st.session_state.gems -= 80
        chance = 0.5
    else:
        st.session_state.gold -= 500
        chance = 0.2
    
    with st.spinner("📦 Quti ochilmoqda..."):
        time.sleep(1)
        if random.random() < chance:
            name = random.choice(list(BRAWLERS_DB.keys()))
            if name not in st.session_state.inv:
                data = BRAWLERS_DB[name]
                st.session_state.inv[name] = {"lvl": 1, "pwr": data['pwr'], "rarity": data['rarity'], "icon": data['icon']}
                st.balloons()
                return f"🔥 YANGI JANGCHI: {name}!"
            else:
                st.session_state.gold += 1500
                return f"💰 Dublikat {name}: +1500 Gold"
        else:
            gain = random.randint(200, 600)
            st.session_state.gold += gain
            return f"💵 Resurslar: +{gain} Gold"

# --- 5. INTERFACE ---
st.markdown(f"""
    <div class='header-card'>
        <h1>🔱 BRAWL STARS: GOD ENGINE v15 🔱</h1>
        <span class='stat-val'>💰 {st.session_state.gold:,}</span>
        <span class='stat-val'>💎 {st.session_state.gems}</span>
        <span class='stat-val'>🏆 {st.session_state.trophies}</span>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

col_left, col_mid, col_right = st.columns([1, 1.2, 1])

# --- CHAP KOLONNA: SHOP & BATTLE ---
with col_left:
    st.header("🛒 Market & Arena")
    if st.button("🚀 PLAY BATTLE (Jang)", use_container_width=True, type="primary"):
        win = random.choice([True, False, True])
        if win:
            st.session_state.trophies += 10
            st.session_state.gold += 100
            st.session_state.xp += 250
            st.success("G'alaba! +10 🏆, +250 XP")
        else:
            st.session_state.trophies = max(0, st.session_state.trophies - 5)
            st.error("Mag'lubiyat! -5 🏆")
        st.rerun()
    
    st.write("---")
    st.subheader("📦 Boxes")
    if st.button("Big Box (500 💰)", use_container_width=True):
        if st.session_state.gold >= 500:
            msg = open_box("Big")
            st.toast(msg)
            st.rerun()
    
    if st.button("Mega Box (80 💎)", use_container_width=True):
        if st.session_state.gems >= 80:
            msg = open_box("Mega")
            st.toast(msg)
            st.rerun()

# --- O'RTA KOLONNA: BRAWL PASS ---
with col_mid:
    st.header("🎫 Brawl Pass")
    st.write(f"Umumiy XP: **{st.session_state.xp}**")
    st.progress(min(st.session_state.xp / 6000, 1.0))
    
    st.markdown("<div class='pass-container'>", unsafe_allow_html=True)
    for tier, data in PASS_REWARDS.items():
        claimed = tier in st.session_state.claimed_tiers
        status_css = "tier-claimed" if claimed else ""
        btn_label = "Olingan" if claimed else ("OLISH" if st.session_state.xp >= data['xp'] else "Yopiq")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
                <div class='pass-tier {status_css}'>
                    <span><b>Tier {tier}:</b> {data['reward']}</span>
                    <small>{data['xp']} XP kerak</small>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            if not claimed and st.session_state.xp >= data['xp']:
                if st.button(btn_label, key=f"tier_{tier}"):
                    if data['type'] == "gold": st.session_state.gold += data['amt']
                    elif data['type'] == "gems": st.session_state.gems += data['amt']
                    elif data['type'] == "brawler":
                        name = "Leon" # Pass brawleri
                        st.session_state.inv[name] = {"lvl": 1, "pwr": 600, "rarity": "Legendary", "icon": "🦎"}
                    st.session_state.claimed_tiers.append(tier)
                    st.rerun()
            else:
                st.button(btn_label, key=f"dis_{tier}", disabled=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- O'NG KOLONNA: COLLECTION ---
with col_right:
    st.header("👤 Collection")
    for name, data in st.session_state.inv.items():
        leg_css = "legendary" if data['rarity'] == "Legendary" else ""
        st.markdown(f"""
            <div class='b-card {leg_css}'>
                <span style='font-size: 30px;'>{data['icon']}</span>
                <b>{name}</b><br>
                <small>LVL {data['lvl']} | PWR {data['pwr']}</small>
            </div>
        """, unsafe_allow_html=True)
        
        cost = data['lvl'] * 800
        if st.button(f"Upgrade ({cost} 💰)", key=f"up_{name}"):
            if st.session_state.gold >= cost:
                st.session_state.gold -= cost
                st.session_state.inv[name]['lvl'] += 1
                st.session_state.inv[name]['pwr'] += 100
                st.rerun()

# Sidebar reset
if st.sidebar.button("♻️ RESET EVERYTHING"):
    st.session_state.clear()
    st.rerun()
