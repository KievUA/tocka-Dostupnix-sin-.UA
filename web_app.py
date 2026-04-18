import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars: Mega Update", page_icon="⭐", layout="wide")

# --- 2. ADVANCED CSS ---
st.markdown("""
    <style>
    .stApp { background: #000d1a; color: #ffffff; }
    .main-header { text-align: center; color: #ffcc00; text-shadow: 2px 2px #ff3300; font-size: 40px; font-weight: bold; }
    .status-bar { background: rgba(0,0,0,0.85); border: 2px solid #ffcc00; border-radius: 20px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 25px; }
    .brawler-card { background: linear-gradient(180deg, #1a1a1a 0%, #000000 100%); border: 1px solid #444; border-radius: 12px; padding: 10px; text-align: center; transition: 0.3s; }
    .brawler-card:hover { border-color: #ffcc00; transform: scale(1.05); }
    .legendary { border: 2px solid #ffcc00 !important; color: #ffcc00; box-shadow: 0 0 10px #ffcc00; }
    .mythic { border: 2px solid #ff00ff !important; color: #ff00ff; }
    .epic { border: 2px solid #9900ff !important; color: #9900ff; }
    .pass-container { background: #050505; border-left: 10px solid #6200ff; border-radius: 15px; padding: 20px; height: 600px; overflow-y: scroll; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BRAWLERS DATA WITH RARITY ---
BRAWLERS = {
    "Шелли": "Common", "Кольт": "Common", "Эль Примо": "Rare", "Поко": "Rare",
    "Биби": "Epic", "Пайпер": "Epic", "Фрэнк": "Epic",
    "Мортис": "Mythic", "Тара": "Mythic", "Джин": "Mythic",
    "Леон": "Legendary", "Ворон": "Legendary", "Спайк": "Legendary", "Сириус": "Legendary"
}

# --- 4. SESSION STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 500, 'gems': 50, 'xp': 0, 'trophies': 0,
        'inv': ["Шелли"], 'claimed': [], 'pass_type': 'Free'
    })

# --- 5. LOGIC ---
def process_box(cost, b_chance, g_chance):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        res = random.random()
        if res < b_chance:
            available = [b for b in BRAWLERS.keys() if b not in st.session_state.inv]
            if available:
                new_b = random.choice(available)
                st.session_state.inv.append(new_b)
                st.balloons(); st.success(f"🎊 НОВЫЙ БОЕЦ: {new_b}!")
        elif res < g_chance:
            reward = random.randint(10, 30)
            st.session_state.gems += reward; st.info(f"💎 ГЕМЫ: +{reward}")
        else:
            st.session_state.gold += int(cost * 0.4); st.toast("💰 Кэшбэк!")
    else: st.error("Недостаточно золота!")

# --- 6. UI ---
st.markdown("<div class='main-header'>BRAWL STARS 2026: MEGA UPDATE</div>", unsafe_allow_html=True)

st.markdown(f"""<div class="status-bar">
    <span style="color:#f1c40f">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span style="color:#00d2ff">💎 ГЕМЫ: {st.session_state.gems:,}</span>
    <span style="color:#ffffff">🏆 КУБКИ: {st.session_state.trophies:,}</span>
</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1.3])

with col1:
    st.header("🏪 МАГАЗИН")
    with st.expander("📦 ЯЩИКИ", expanded=True):
        if st.button("МАЛЫЙ ЯЩИК (1,000 💰)", use_container_width=True):
            process_box(1000, 0.05, 0.15); st.rerun()
        if st.button("МЕГА ЯЩИК (5,000 💰)", use_container_width=True):
            process_box(5000, 0.15, 0.30); st.rerun()
    
    st.write("---")
    if st.button("⚔️ ИГРАТЬ (БОЙ)", use_container_width=True, type="primary"):
        st.session_state.gold += random.randint(50, 100)
        st.session_state.xp += 200
        st.session_state.trophies += 8; st.rerun()

    promo = st.text_input("Ввести Промокод:")
    if st.button("АКТИВИРОВАТЬ"):
        if promo == "APRIL2026" and "Сириус" not in st.session_state.inv:
            st.session_state.inv.append("Сириус"); st.balloons()
        st.rerun()

with col2:
    st.header("💾 СОХРАНЕНИЕ")
    if st.button("СКОПИРОВАТЬ КОД"):
        data = {'g': st.session_state.gold, 'm': st.session_state.gems, 'x': st.session_state.xp, 't': st.session_state.trophies, 'i': st.session_state.inv, 'c': st.session_state.claimed, 'p': st.session_state.pass_type}
        st.code(base64.b64encode(json.dumps(data).encode()).decode())
    
    in_code = st.text_input("ВСТАВИТЬ КОД:")
    if st.button("ЗАГРУЗИТЬ"):
        try:
            d = json.loads(base64.b64decode(in_code).decode())
            st.session_state.update({'gold':d['g'], 'gems':d['m'], 'xp':d['x'], 'trophies':d['t'], 'inv':d['i'], 'claimed':d['c'], 'pass_type':d['p']})
            st.success("Данные загружены!"); st.rerun()
        except: st.error("Ошибка!")

    st.write("---")
    st.header("👥 КОЛЛЕКЦИЯ")
    c_cols = st.columns(2)
    for i, name in enumerate(st.session_state.inv[-4:]):
        rarity = BRAWLERS.get(name, "Common")
        with c_cols[i % 2]:
            st.markdown(f"<div class='brawler-card {rarity.lower()}'>{name}<br><small>{rarity}</small></div>", unsafe_allow_html=True)

with col3:
    st.header("🎫 BRAWL PASS (50 LVL)")
    current_lvl = st.session_state.xp // 15000
    st.progress(min(current_lvl/50, 1.0))
    
    if st.session_state.pass_type == 'Free':
        if st.button("💎 КУПИТЬ PLUS (499 ГЕМОВ)", use_container_width=True):
            if st.session_state.gems >= 499:
                st.session_state.gems -= 499; st.session_state.pass_type = 'Plus'; st.rerun()
    
    st.markdown("<div class='pass-container'>", unsafe_allow_html=True)
    for i in range(1, 51):
        unlocked = current_lvl >= i
        claimed = i in st.session_state.claimed
        status = "✅" if claimed else ("🎁" if unlocked else "🔒")
        
        st.markdown(f"**Уровень {i}** | {status}")
        if unlocked and not claimed:
            if st.button(f"ЗАБРАТЬ {i}", key=f"lvl_{i}"):
                st.session_state.gold += 800
                st.session_state.gems += 5
                if st.session_state.pass_type == 'Plus':
                    st.session_state.gold += 2500
                    st.session_state.gems += 20
                st.session_state.claimed.append(i); st.rerun()
        st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)
