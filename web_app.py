import streamlit as st
import random
import time

# --- SUPREME ENGINE CONFIG ---
st.set_page_config(page_title="Brawl Stars: HYPER-DRIVE", page_icon="⚡", layout="wide")

# --- ULTRA NEON CSS (100% NO IMAGE NEEDED) ---
st.markdown("""
    <style>
    .stApp { background: #000814; color: #fff; font-family: 'Inter', sans-serif; }
    
    /* Global Neon Border */
    .neon-card {
        background: rgba(0, 20, 40, 0.8);
        border: 2px solid #00d2ff;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.2);
        margin-bottom: 20px;
    }
    
    /* Resource Bar */
    .resource-grid {
        display: flex; justify-content: space-around;
        background: linear-gradient(90deg, #001d3d, #003566);
        padding: 15px; border-radius: 50px;
        border: 2px solid #ffc300; margin-bottom: 25px;
    }
    .res-item { font-size: 20px; font-weight: 800; color: #ffc300; }

    /* Box Animations */
    @keyframes pulse { 0% {transform: scale(1);} 50% {transform: scale(1.05);} 100% {transform: scale(1);} }
    .box-btn {
        height: 180px; border-radius: 25px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; cursor: pointer;
        transition: 0.3s; border: 4px solid rgba(255,255,255,0.1);
        animation: pulse 3s infinite ease-in-out;
    }
    .box-btn:hover { transform: scale(1.1) rotate(2deg); border-color: #fff; }
    
    .big-b { background: linear-gradient(45deg, #ff0055, #ff5500); }
    .mega-b { background: linear-gradient(45deg, #0099ff, #00ccff); }
    .omega-b { background: linear-gradient(45deg, #ffcc00, #ff6600); box-shadow: 0 0 30px #ffcc00; }

    /* Brawler Badge */
    .mastery-badge {
        background: #ffc300; color: #000; padding: 2px 8px;
        border-radius: 5px; font-size: 10px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
BRAWLERS_DB = {
    "LEON": {"rarity": "Legendary", "icon": "🦎", "hp": 3200, "dmg": 480, "color": "#ffc300", "ability": "Invisibility"},
    "CROW": {"rarity": "Legendary", "icon": "🦅", "hp": 2400, "dmg": 320, "color": "#ffc300", "ability": "Poison Dagger"},
    "SPIKE": {"rarity": "Legendary", "icon": "🌵", "hp": 2400, "dmg": 560, "color": "#ffc300", "ability": "Cactus Grenade"},
    "MORTIS": {"rarity": "Mythic", "icon": "🦇", "hp": 3800, "dmg": 940, "color": "#ff0055", "ability": "Dash Attack"},
    "TARA": {"rarity": "Mythic", "icon": "🃏", "hp": 3200, "dmg": 460, "color": "#ff0055", "ability": "Black Hole"},
    "EDGAR": {"rarity": "Epic", "icon": "🧣", "hp": 3000, "dmg": 540, "color": "#9d4edd", "ability": "Vault jump"},
    "SURGE": {"rarity": "Chromatic", "icon": "🤖", "hp": 3300, "dmg": 480, "color": "#0099ff", "ability": "Upgrade"},
    "FANG": {"rarity": "Epic", "icon": "👟", "hp": 4300, "dmg": 520, "color": "#9d4edd", "ability": "Flying Kick"}
}

# --- STATE INITIALIZATION ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 5000, 'gems': 200, 'trophies': 0, 'pass_xp': 0,
        'inv': {"SHELLY": {"lvl": 1, "mastery": 0, "icon": "🔫", "pwr": 300}},
        'logs': ["Xush kelibsiz! Hyper-Drive tizimi faol."],
        'daily_claimed': False
    })

# --- UTILS ---
def open_box(b_type):
    costs = {"BIG": 500, "MEGA": 80, "OMEGA": 150}
    if b_type == "BIG": st.session_state.gold -= costs[b_type]
    else: st.session_state.gems -= costs[b_type]
    
    with st.spinner("📦 Quti ochilmoqda..."): time.sleep(1)
    
    luck = random.random()
    chances = {"BIG": 0.25, "MEGA": 0.5, "OMEGA": 0.8}
    
    if luck < chances[b_type]:
        name = random.choice(list(BRAWLERS_DB.keys()))
        if name not in st.session_state.inv:
            data = BRAWLERS_DB[name]
            st.session_state.inv[name] = {"lvl": 1, "mastery": 0, "icon": data['icon'], "pwr": data['dmg']}
            st.session_state.logs.insert(0, f"🌟 YANGI JANGCHI: {name}!")
            st.balloons()
        else:
            bonus = 2000 if BRAWLERS_DB[name]['rarity'] == "Legendary" else 1000
            st.session_state.gold += bonus
            st.session_state.logs.insert(0, f"💰 Dublikat {name}: +{bonus} Oltin")
    else:
        gains = random.randint(300, 1200)
        st.session_state.gold += gains
        st.session_state.logs.insert(0, f"📦 Resurslar: +{gains} oltin")

def play_match():
    player_force = sum(v['pwr'] for v in st.session_state.inv.values())
    enemy_force = random.randint(200, player_force + 500)
    
    with st.empty():
        for i in range(3):
            st.write(f"⚔️ Jang ketmoqda{'.'*(i+1)}")
            time.sleep(0.3)
            
    if player_force >= enemy_force:
        t_gain = random.randint(8, 15)
        st.session_state.trophies += t_gain
        st.session_state.gold += 150
        st.session_state.pass_exp += 60
        # Mastery oshirish
        b_name = random.choice(list(st.session_state.inv.keys()))
        st.session_state.inv[b_name]['mastery'] += 10
        st.success(f"G'ALABA! +{t_gain} Kubok, +150 Oltin. {b_name} mahorati oshdi!")
    else:
        t_loss = random.randint(4, 9)
        st.session_state.trophies = max(0, st.session_state.trophies - t_loss)
        st.error(f"MAG'LUBIYAT! -{t_loss} Kubok")

# --- UI START ---
st.markdown("<h1 style='text-align: center; color: #ffc300;'>⚡ BRAWL STARS: HYPER-DRIVE v13</h1>", unsafe_allow_html=True)

# Resource Bar
st.markdown(f"""
    <div class='resource-grid'>
        <span class='res-item'>💰 {st.session_state.gold:,}</span>
        <span class='res-item'>💎 {st.session_state.gems}</span>
        <span class='res-item'>🏆 {st.session_state.trophies}</span>
        <span class='res-item'>⭐ XP: {st.session_state.pass_exp}</span>
    </div>
    """, unsafe_allow_html=True)

# Main Grid
col_shop, col_arena, col_inv = st.columns([1.2, 1, 1.2])

with col_shop:
    st.subheader("🛒 HYPER SHOP")
    
    if st.button("🎁 DAILY GIFT", use_container_width=True, disabled=st.session_state.daily_claimed):
        st.session_state.gold += 500
        st.session_state.daily_claimed = True
        st.rerun()

    s1, s2 = st.columns(2)
    with s1:
        st.markdown("<div class='box-btn big-b'><h1>🎁</h1><b>BIG BOX</b></div>", unsafe_allow_html=True)
        if st.button("500 💰", key="b_big"):
            if st.session_state.gold >= 500: open_box("BIG"); st.rerun()
            
    with s2:
        st.markdown("<div class='box-btn mega-b'><h1>🔵</h1><b>MEGA BOX</b></div>", unsafe_allow_html=True)
        if st.button("80 💎", key="b_mega"):
            if st.session_state.gems >= 80: open_box("MEGA"); st.rerun()

    st.markdown("<div class='box-btn omega-b'><h1>🟣</h1><b>OMEGA BOX</b></div>", unsafe_allow_html=True)
    if st.button("150 💎", key="b_omega", use_container_width=True):
        if st.session_state.gems >= 150: open_box("OMEGA"); st.rerun()

with col_arena:
    st.subheader("🏟️ ARENA")
    if st.button("🔥 START MATCH (PLAY)", use_container_width=True, type="primary"):
        play_match()
        st.rerun()
    
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.write("📋 **Vazifalar (Quests)**")
    st.write(f"• 5000 Kubok yig'ish: {st.session_state.trophies}/5000")
    st.write(f"• 10 ta Brawler topish: {len(st.session_state.inv)}/10")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.subheader("🎫 BRAWL PASS")
    lvl = st.session_state.pass_exp // 1000
    progress = (st.session_state.pass_exp % 1000) / 1000
    st.progress(progress)
    st.caption(f"Pass Level: {lvl} | Keyingi darajaga {1000 - (st.session_state.pass_exp % 1000)} XP")

with col_inv:
    st.subheader("👤 COLLECTION")
    for name, data in st.session_state.inv.items():
        rarity_color = BRAWLERS_DB.get(name, {}).get('color', '#fff')
        st.markdown(f"""
            <div class='neon-card' style='border-color: {rarity_color}; padding: 10px;'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='font-size: 25px;'>{data['icon']} <b>{name}</b></span>
                    <span class='mastery-badge'>Rank {data['mastery'] // 50}</span>
                </div>
                <small>LVL {data['lvl']} | PWR {data['pwr']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Upgrade
        cost = data['lvl'] * 1200
        if st.button(f"UPGRADE ({cost} 💰)", key=f"up_{name}"):
            if st.session_state.gold >= cost:
                st.session_state.gold -= cost
                st.session_state.inv[name]['lvl'] += 1
                st.session_state.inv[name]['pwr'] += 80
                st.rerun()

# Logs
st.write("---")
st.subheader("📜 ACTIVITY LOG")
for log in st.session_state.logs[:5]:
    st.caption(log)

if st.sidebar.button("⚠️ RESET SYSTEM"):
    st.session_state.clear()
    st.rerun()
