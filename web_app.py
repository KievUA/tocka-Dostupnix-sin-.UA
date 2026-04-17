import streamlit as st
import random
import time
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars CYBER", page_icon="🔱", layout="wide")

# --- 2. ELITE CYBER BACKGROUND & CSS ---
st.markdown("""
    <style>
    /* Daxshatli Kiberpank Fon */
    .stApp {
        background: radial-gradient(circle at center, #001220 0%, #000000 100%);
        background-attachment: fixed;
        color: #00ffcc;
        font-family: 'Orbitron', sans-serif;
    }
    
    /* Neon Chiziqlar */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(rgba(0, 255, 204, 0.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0, 255, 204, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        z-index: -1;
    }

    .status-bar {
        background: rgba(0, 0, 0, 0.8);
        border: 2px solid #00ffcc;
        border-radius: 50px; padding: 15px;
        display: flex; justify-content: space-around;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4);
        margin-bottom: 30px;
    }

    .box-card {
        background: rgba(10, 10, 10, 0.9);
        border: 2px solid #333; border-radius: 20px;
        padding: 20px; text-align: center;
        transition: 0.4s; margin-bottom: 15px;
    }
    .box-card:hover { 
        border-color: #ff0055; 
        transform: translateY(-10px);
        box-shadow: 0 10px 20px rgba(255, 0, 85, 0.3);
    }

    .brawler-card {
        background: #050505; border: 1px solid #00ffcc;
        border-radius: 15px; padding: 15px; text-align: center;
        box-shadow: 0 5px 15px rgba(0, 255, 204, 0.1);
    }
    
    .rank-badge {
        background: #cd7f32; color: white;
        padding: 2px 8px; border-radius: 5px;
        font-size: 10px; font-weight: bold;
        text-transform: uppercase;
    }

    .pass-panel {
        background: rgba(10, 0, 30, 0.8);
        border: 2px solid #6200ff; border-radius: 25px;
        padding: 20px; box-shadow: 0 0 25px rgba(98, 0, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INITIAL STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'trophies': 0, 'xp': 0,
        'inv': {"Шелли": {"lvl": 1, "pwr": 300, "icon": "🔫", "rank": "BRONZE III"}},
        'claimed': [], 'plus': False
    })

BRAWLERS_DB = {
    "Леон": {"pwr": 600, "icon": "🦎", "rank": "SILVER I"},
    "Ворон": {"pwr": 580, "icon": "🦅", "rank": "BRONZE II"},
    "Спайк": {"pwr": 620, "icon": "🌵", "rank": "GOLD I"},
    "Мортис": {"pwr": 500, "icon": "🦇", "rank": "BRONZE III"}
}

PASS_TIERS = {
    1: {"xp": 500, "reward": "1,000 Золота", "val": 1000, "type": "gold"},
    5: {"xp": 15000, "reward": "100 Гемов", "val": 100, "type": "gems"},
    10: {"xp": 100000, "reward": "PLUS: 50,000 Золота", "val": 50000, "type": "gold"},
    15: {"xp": 400000, "reward": "ФИНАЛ: 400,000 ЗОЛОТА", "val": 400000, "type": "gold"}
}

# --- 4. LOGIC ---
def open_box(cost, brawler_chance):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        with st.spinner("📦 СИНХРОНИЗАЦИЯ..."):
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
                    st.info(f"💰 ДУБЛИКАТ! +{cost*2} Золота")
            else:
                gain = random.randint(int(cost*0.4), int(cost*0.9))
                st.session_state.gold += gain
                st.toast(f"📦 ДОБЫЧА: +{gain} ЗОЛОТА")
    else:
        st.error("НЕДОСТАТОЧНО ЗОЛОТА!")

def save_game():
    data = {k: v for k, v in st.session_state.items() if k != 'save_code'}
    return base64.b64encode(str(data).encode()).decode()

def load_game(code):
    try:
        decoded = eval(base64.b64decode(code).decode())
        st.session_state.update(decoded)
        st.success("✅ ДАННЫЕ ВОССТАНОВЛЕНЫ!")
        time.sleep(0.5); st.rerun()
    except: st.error("❌ ОШИБКА КОДА!")

# --- 5. UI LAYOUT ---
st.markdown("<h1 style='text-align: center; color: #00ffcc; text-shadow: 0 0 10px #00ffcc;'>🔱 BRAWL STARS: ELITE CYBER v18.5 🔱</h1>", unsafe_allow_html=True)

# Status Bar
st.markdown(f"""
    <div class="status-bar">
        <span style="color: #f1c40f;">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
        <span style="color: #00d2ff;">💎 ГЕМЫ: {st.session_state.gems}</span>
        <span style="color: #ffffff;">🏆 КУБКИ: {st.session_state.trophies}</span>
    </div>
    """, unsafe_allow_html=True)

col_shop, col_arena, col_pass = st.columns([1, 1, 1.4])

with col_shop:
    st.header("🛒 SHOP")
    for cost, name, color in [(500, "SMALL", "#333"), (1000, "BIG", "#00d2ff"), (3000, "ULTRA", "#ff0055")]:
        st.markdown(f"<div class='box-card' style='border-color: {color};'><h3>{name} BOX</h3><p>{cost} ЗОЛОТА</p></div>", unsafe_allow_html=True)
        if st.button(f"ОТКРЫТЬ {name}", key=f"b_{cost}", use_container_width=True):
            chance = 0.05 if cost == 500 else (0.15 if cost == 1000 else 0.35)
            open_box(cost, chance); st.rerun()

with col_arena:
    st.header("⚔️ ARENA")
    if st.button("🔥 START SUPREME BATTLE", use_container_width=True, type="primary"):
        with st.spinner("БОЙ..."):
            time.sleep(0.5)
            st.session_state.gold += 300
            st.session_state.xp += 1200
            st.session_state.trophies += 25
            st.rerun()
    
    st.write("---")
    st.subheader("💾 DATA")
    if st.button("SAVE CODE (СОХРАНИТЬ)", use_container_width=True):
        st.code(save_game())
    
    in_code = st.text_input("LOAD CODE (ЗАГРУЗИТЬ):")
    if st.button("LOAD DATA", use_container_width=True):
        load_game(in_code)

with col_pass:
    st.markdown("<div class='pass-panel'>", unsafe_allow_html=True)
    st.header("🎫 BRAWL PASS")
    st.write(f"XP PROGRESS: **{st.session_state.xp:,} / 400,000**")
    st.progress(min(st.session_state.xp / 400000, 1.0))
    
    if not st.session_state.plus:
        if st.button("BUY PLUS (200 💎)", use_container_width=True):
            if st.session_state.gems >= 200:
                st.session_state.gems -= 200
                st.session_state.plus = True
                st.rerun()

    for t, d in PASS_TIERS.items():
        is_plus = t >= 10
        claimed = t in st.session_state.claimed
        unlocked = st.session_state.xp >= d['xp']
        
        status_icon = "✅" if claimed else ("🔓" if unlocked else "🔒")
        
        st.markdown(f"""
            <div style='padding: 10px; border-bottom: 1px solid #333; display: flex; justify-content: space-between;'>
                <span>Tier {t}: {d['reward']}</span>
                <span>{status_icon}</span>
            </div>
            """, unsafe_allow_html=True)
        
        if unlocked and not claimed:
            if is_plus and not st.session_state.plus:
                st.button("PLUS REQUIRED", key=f"l_{t}", disabled=True, use_container_width=True)
            else:
                if st.button(f"CLAIM {d['reward']}", key=f"c_{t}", use_container_width=True):
                    if d['type'] == 'gold': st.session_state.gold += d['val']
                    elif d['type'] == 'gems': st.session_state.gems += d['val']
                    st.session_state.claimed.append(t)
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. COLLECTION ---
st.write("---")
st.header("👤 MY BRAWLERS")
b_cols = st.columns(5)
for i, (name, data) in enumerate(st.session_state.inv.items()):
    with b_cols[i % 5]:
        st.markdown(f"""
            <div class='brawler-card'>
                <div class='rank-badge'>{data.get('rank', 'BRONZE I')}</div>
                <h2 style='margin: 10px 0;'>{data['icon']}</h2>
                <b>{name}</b><br>
                <small style='color: #00ffcc;'>POWER: {data['pwr']}</small>
            </div>
            """, unsafe_allow_html=True)

if st.sidebar.button("♻️ FULL RESET"):
    st.session_state.clear(); st.rerun()
