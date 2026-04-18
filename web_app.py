import streamlit as st
import random
import time
import base64
import json
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars: Supreme Edition", page_icon="🔱", layout="wide")

# --- 2. PROFESSIONAL CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background: linear-gradient(135deg, #000428 0%, #004e92 100%); color: #ffffff; font-family: 'Orbitron', sans-serif; }
    
    .main-title { font-family: 'Black Ops One', cursive; font-size: 60px; text-align: center; color: #ffcc00; text-shadow: 4px 4px #ff3300; margin-bottom: 10px; }
    
    .status-bar { background: rgba(0, 0, 0, 0.8); border: 3px solid #00ffcc; border-radius: 30px; padding: 20px; display: flex; justify-content: space-around; margin-bottom: 30px; box-shadow: 0 0 20px #00ffcc; }
    
    .card { background: rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px); text-align: center; transition: 0.3s; }
    .card:hover { transform: translateY(-5px); border-color: #ffcc00; }
    
    .mega-ultra-box { background: linear-gradient(45deg, #8e2de2, #4a00e0); border: 4px solid gold; box-shadow: 0 0 30px gold; animation: pulse 2s infinite; }
    
    @keyframes pulse { 0% {box-shadow: 0 0 10px gold;} 50% {box-shadow: 0 0 40px gold;} 100% {box-shadow: 0 0 10px gold;} }
    
    .brawler-slot { background: #000; border: 2px solid #555; border-radius: 15px; padding: 15px; margin: 10px; min-height: 150px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .legendary-slot { border-color: gold !important; color: gold !important; box-shadow: 0 0 15px gold; }
    
    .pass-scroll { background: rgba(0,0,0,0.5); border-radius: 20px; padding: 20px; height: 650px; overflow-y: scroll; border: 2px solid #6200ff; }
    .level-item { background: #111; border-radius: 12px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; border-left: 8px solid #6200ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BRAWLER DATABASE (Full 78) ---
ALL_BRAWLERS = [
    "Шелли", "Нита", "Кольт", "Булл", "Брок", "Эль Примо", "Барли", "Поко", "Роза", "Рико", "Дэррил", "Пенни", "Карл", "Джекки", 
    "Пайпер", "Пэм", "Фрэнк", "Биби", "Беа", "Нани", "Эдгар", "Грифф", "Гром", "Бонни", "Мортис", "Тара", "Джин", "Макс", 
    "Мистер П.", "Спраут", "Байрон", "Скуик", "Спайк", "Ворон", "Леон", "Сэнди", "Амбер", "Мэг", "Гейл", "Вольт", "Колетт", 
    "Лу", "Гавс", "Белль", "Базз", "Эш", "Лола", "Фэнг", "Ева", "Джанет", "Отис", "Сэм", "Бастер", "Мэнди", "Р-Т", "Мэйси", 
    "Хэнк", "Корделиус", "Даг", "Чак", "Мико", "Кит", "Ларри", "Лоури", "Анджело", "Мелоди", "Лили", "Драко", "Клэнси", 
    "Берри", "Кэндзи", "Мо", "Сириус", "Джуджу", "Шад", "Гас", "Честер", "Грей"
]

# --- 4. SESSION INITIALIZATION ---
if 'init' not in st.session_state:
    st.session_state.update({
        'init': True, 'gold': 1000, 'gems': 50, 'xp': 0, 'trophies': 0,
        'inv': ["Шелли"], 'claimed': [], 'pass_type': 'Free', 'last_box': 'None'
    })

# --- 5. CORE LOGIC FUNCTIONS ---
def get_save_code():
    data = {
        "v": 2.0, "g": st.session_state.gold, "m": st.session_state.gems,
        "x": st.session_state.xp, "t": st.session_state.trophies,
        "i": st.session_state.inv, "c": st.session_state.claimed, "p": st.session_state.pass_type
    }
    return base64.b64encode(json.dumps(data).encode()).decode()

def load_save_code(code):
    try:
        decoded = json.loads(base64.b64decode(code).decode())
        st.session_state.update({
            'gold': decoded['g'], 'gems': decoded['m'], 'xp': decoded['x'],
            'trophies': decoded['t'], 'inv': decoded['i'], 'claimed': decoded['c'],
            'pass_type': decoded['p']
        })
        return True
    except: return False

def open_box_supreme(type_box):
    costs = {"small": 1000, "big": 5000, "mega": 10000}
    chances = {"small": 0.08, "big": 0.15, "mega": 0.30}
    
    cost = costs[type_box]
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        res = random.random()
        if res < chances[type_box]:
            possible = [b for b in ALL_BRAWLERS if b not in st.session_state.inv]
            if possible:
                new_b = random.choice(possible)
                st.session_state.inv.append(new_b)
                st.session_state.last_box = f"🎉 ВЫПАЛ: {new_b}!"
                st.balloons()
            else:
                st.session_state.gold += cost * 2
                st.session_state.last_box = "💰 ВСЕ БОЙЦЫ ЕСТЬ! КЭШБЭК x2"
        else:
            st.session_state.gold += int(cost * 0.4)
            st.session_state.last_box = "💎 ПУСТО (Кэшбэк 40%)"
    else: st.error("Недостаточно золота!")

# --- 6. MAIN INTERFACE ---
st.markdown("<div class='main-title'>BRAWL STARS SUPREME</div>", unsafe_allow_html=True)

# STATUS BAR
st.markdown(f"""
<div class="status-bar">
    <div style="text-align:center"><span style="color:#f1c40f; font-size:24px">💰</span><br>{st.session_state.gold:,}</div>
    <div style="text-align:center"><span style="color:#00d2ff; font-size:24px">💎</span><br>{st.session_state.gems:,}</div>
    <div style="text-align:center"><span style="color:#ffffff; font-size:24px">🏆</span><br>{st.session_state.trophies:,}</div>
    <div style="text-align:center"><span style="color:#ff00ff; font-size:24px">⭐</span><br>XP: {st.session_state.xp:,}</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.2, 1, 1.3])

# --- COLUMN 1: SHOP & BATTLE ---
with col1:
    st.header("🏪 МАГАЗИН")
    
    # Mega Ultra Box UI
    st.markdown("""<div class='card mega-ultra-box'>
        <h2 style='color:gold'>🔥 MEGA ULTRA BOX</h2>
        <h3 style='margin:0'>10,000 💰</h3>
        <p>Шанс на бойца: <b>30%</b></p>
        <p style='font-size:12px; opacity:0.8'>⏳ АКЦИЯ 24 ЧАСА</p>
    </div>""", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ MEGA ULTRA", use_container_width=True):
        open_box_supreme("mega"); st.rerun()
    
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("МАЛЫЙ (1k)", use_container_width=True): open_box_supreme("small"); st.rerun()
    with c2:
        if st.button("БОЛЬШОЙ (5k)", use_container_width=True): open_box_supreme("big"); st.rerun()
        
    st.markdown(f"<div style='text-align:center; color:#ffcc00; padding:10px'>{st.session_state.last_box}</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.header("⚔️ АРЕНА")
    if st.button("🔥 НАЧАТЬ БОЙ (+150 💰 | +300 XP)", use_container_width=True, type="primary"):
        st.session_state.gold += 150
        st.session_state.xp += 300
        st.session_state.trophies += random.randint(8, 12)
        st.rerun()

# --- COLUMN 2: DATA & COLLECTION ---
with col2:
    st.header("💾 СОХРАНЕНИЕ")
    if st.button("📝 СОЗДАТЬ КОД ВОССТАНОВЛЕНИЯ", use_container_width=True):
        st.code(get_save_code())
        st.info("Скопируйте и сохраните этот код.")
        
    input_code = st.text_input("Вставьте код сюда:")
    if st.button("📥 ЗАГРУЗИТЬ АККАУНТ", use_container_width=True):
        if load_save_code(input_code): st.success("Данные успешно загружены!"); st.rerun()
        else: st.error("Неверный код!")
        
    st.write("---")
    st.header("🎫 ПРОМОКОД")
    promo = st.text_input("Введите секретный код:", placeholder="...").strip()
    if st.button("АКТИВИРОВАТЬ CODE"):
        if promo == "APRIL2026":
            if "Сириус" not in st.session_state.inv:
                st.session_state.inv.append("Сириус")
                st.balloons(); st.success("🌟 SIRIUS РАЗБЛОКИРОВАН!")
            else: st.warning("Уже есть!")
        elif promo == "GEMS999":
            st.session_state.gems += 999; st.rerun()
        else: st.error("Код не найден.")

# --- COLUMN 3: BRAWL PASS ---
with col3:
    st.header("🎫 BRAWL PASS (50 LVL)")
    curr_lvl = st.session_state.xp // 15000
    progress = (st.session_state.xp % 15000) / 15000
    
    st.write(f"Уровень: **{curr_lvl} / 50**")
    st.progress(min(progress, 1.0))
    
    if st.session_state.pass_type == 'Free':
        if st.button("💎 КУПИТЬ PLUS (499 GEMS)", use_container_width=True):
            if st.session_state.gems >= 499:
                st.session_state.gems -= 499
                st.session_state.pass_type = 'Plus'; st.rerun()
            else: st.error("Нужно 499 гемов!")
    else:
        st.success("👑 BRAWL PASS PLUS АКТИВИРОВАН")
        
    st.markdown("<div class='pass-scroll'>", unsafe_allow_html=True)
    for i in range(1, 51):
        is_unlocked = curr_lvl >= i
        is_claimed = i in st.session_state.claimed
        status = "✅" if is_claimed else ("🎁" if is_unlocked else "🔒")
        
        st.markdown(f"""
        <div class="level-item">
            <span>LVL {i}</span>
            <span>{status}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if is_unlocked and not is_claimed:
            if st.button(f"ЗАБРАТЬ {i}", key=f"cl_{i}"):
                st.session_state.gold += 1000
                st.session_state.gems += 15
                if st.session_state.pass_type == 'Plus':
                    st.session_state.gold += 2500
                    st.session_state.gems += 40
                    if i % 10 == 0:
                        new_r = random.choice(ALL_BRAWLERS)
                        if new_r not in st.session_state.inv: st.session_state.inv.append(new_r)
                st.session_state.claimed.append(i); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER: INVENTORY ---
st.write("---")
st.header(f"👤 МОИ БОЙЦЫ ({len(st.session_state.inv)} / 78)")
inv_cols = st.columns(6)
for idx, b_name in enumerate(st.session_state.inv):
    with inv_cols[idx % 6]:
        style = "legendary-slot" if b_name in ["Сириус", "Леон", "Спайк", "Ворон"] else ""
        st.markdown(f"<div class='brawler-slot {style}'><b>{b_name}</b></div>", unsafe_allow_html=True)
