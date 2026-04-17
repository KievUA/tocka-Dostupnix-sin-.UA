import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars Stable", page_icon="🔱", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    .stApp { background: #00050a; color: #00ffcc; font-family: 'sans-serif'; }
    .status-bar { background: rgba(0,210,255,0.1); border: 2px solid #00ffcc; border-radius: 20px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 20px; }
    .brawler-card { background: #000; border: 1px solid #00ffcc; border-radius: 10px; padding: 10px; text-align: center; }
    .sirius-glow { border: 2px solid #00d2ff !important; box-shadow: 0 0 15px #00d2ff; color: #00d2ff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 5000, 'gems': 100, 'xp': 0,
        'inv': {"Шелли": "🔫"},
        'claimed': [], 'plus': False
    })

# --- 4. FUNCTIONS ---
def open_mega_ultra():
    if st.session_state.gold >= 10000:
        st.session_state.gold -= 10000
        time.sleep(0.5)
        rand = random.random()
        if rand < 0.20: # 20% Gems
            st.session_state.gems += random.randint(50, 150)
            st.balloons()
        elif rand < 0.35: # 15% Sirius or Others
            b = random.choice(["SIRIUS", "Леон", "Ворон", "Спайк"])
            if b not in st.session_state.inv:
                st.session_state.inv[b] = "🌟"
                st.balloons()
        else:
            st.session_state.gold += 12000
    else: st.error("Недостаточно золота!")

# --- 5. UI ---
st.title("🔱 BRAWL STARS: SIRIUS v20.2")

st.markdown(f"""<div class="status-bar">
    <span>💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span>💎 ГЕМЫ: {st.session_state.gems}</span>
    <span>⭐ XP: {st.session_state.xp}</span>
</div>""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1.2])

with c1:
    st.header("🛒 МАГАЗИН")
    if st.button("💎 МЕГА УЛЬТРА (10k)", use_container_width=True):
        open_mega_ultra(); st.rerun()
    
    if st.button("🔥 БОЙ (+150 XP)", use_container_width=True):
        st.session_state.gold += 100
        st.session_state.xp += 150; st.rerun()

with c2:
    st.header("💾 АККАУНТ")
    # Kodni qisqartirilgan holatda ko'rsatish
    if st.button("ПОЛУЧИТЬ КОД"):
        data = {
            'g': st.session_state.gold,
            'm': st.session_state.gems,
            'x': st.session_state.xp,
            'i': list(st.session_state.inv.keys()),
            'p': st.session_state.plus
        }
        res_code = base64.b64encode(json.dumps(data).encode()).decode()
        st.code(res_code)
    
    in_code = st.text_input("ВСТАВИТЬ КОД:")
    if st.button("ЗАГРУЗИТЬ"):
        try:
            d = json.loads(base64.b64decode(in_code).decode())
            st.session_state.gold = d.get('g', 0)
            st.session_state.gems = d.get('m', 0)
            st.session_state.xp = d.get('x', 0)
            st.session_state.inv = {name: "🔥" for name in d.get('i', ["Шелли"])}
            st.session_state.plus = d.get('p', False)
            st.success("Аккаунт загружен!"); st.rerun()
        except: st.error("Xato! Kodni to'liq nusxalaganingizni tekshiring.")

with c3:
    st.header("🎫 BRAWL PASS")
    lvl = st.session_state.xp // 5000
    st.write(f"Ваш уровень: {lvl}/30")
    if not st.session_state.plus and st.button("КУПИТЬ PLUS (200 💎)"):
        if st.session_state.gems >= 200:
            st.session_state.gems -= 200; st.session_state.plus = True; st.rerun()
    
    st.write("---")
    st.header("👤 БОЙЦЫ")
    cols = st.columns(2)
    for i, (name, icon) in enumerate(st.session_state.inv.items()):
        with cols[i % 2]:
            st.markdown(f"<div class='brawler-card {'sirius-glow' if name == 'SIRIUS' else ''}'>{icon}<br>{name}</div>", unsafe_allow_html=True)
