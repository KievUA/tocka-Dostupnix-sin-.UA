import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars: Hardcore", page_icon="⚔️", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    .stApp { background: #000814; color: #ffffff; font-family: 'Arial'; }
    .status-bar { background: rgba(0,0,0,0.8); border: 2px solid #00ffcc; border-radius: 15px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 20px; font-weight: bold; }
    .box-card { background: linear-gradient(135deg, #1a1a1a 0, #2d2d2d 100%); border: 1px solid #444; border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 10px; }
    .pass-panel { background: #0a0a0a; border: 2px solid #6200ff; border-radius: 15px; padding: 15px; height: 500px; overflow-y: scroll; }
    .brawler-item { background: #111; border: 1px solid #333; border-radius: 8px; padding: 8px; text-align: center; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BRAWLERS DATABASE (78 Total) ---
B_DB = [
    "Шелли", "Нита", "Кольт", "Булл", "Брок", "Эль Примо", "Барли", "Поко", "Роза", "Рико", "Дэррил", "Пенни", "Карл", "Джекки", 
    "Пайпер", "Пэм", "Фрэнк", "Биби", "Беа", "Нани", "Эдгар", "Грифф", "Гром", "Бонни", "Мортис", "Тара", "Джин", "Макс", 
    "Мистер П.", "Спраут", "Байрон", "Скуик", "Спайк", "Ворон", "Леон", "Сэнди", "Амбер", "Мэг", "Гейл", "Вольт", "Колетт", 
    "Лу", "Гавс", "Белль", "Базз", "Эш", "Лола", "Фэнг", "Ева", "Джанет", "Отис", "Сэм", "Бастер", "Мэнди", "Р-Т", "Мэйси", 
    "Хэнк", "Корделиус", "Даг", "Чак", "Мико", "Кит", "Ларри", "Лоури", "Анджело", "Мелоди", "Лили", "Драко", "Клэнси", 
    "Берри", "Кэндзи", "Мо", "Сириус", "Джуджу", "Шад", "Гас", "Честер", "Грей"
]

# --- 4. SESSION STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'xp': 0,
        'inv': ["Шелли"],
        'claimed': [], 'pass_type': 'Free' # Free, Plus
    })

# --- 5. LOGIC FUNCTIONS ---
def open_box(cost):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        rand = random.random()
        
        if cost == 1000:
            if rand < 0.05: # Brawler
                new = random.choice([b for b in B_DB if b not in st.session_state.inv])
                st.session_state.inv.append(new); st.balloons(); st.success(f"НОВЫЙ БОЕЦ: {new}")
            elif rand < 0.15: # 10% XP
                st.session_state.xp += 500; st.info("+500 XP")
            else: # 85% Cashback
                st.session_state.gold += 250; st.toast("+250 Золота")
        
        elif cost == 5000:
            if rand < 0.15: # Brawler
                new = random.choice([b for b in B_DB if b not in st.session_state.inv])
                st.session_state.inv.append(new); st.balloons(); st.success(f"НОВЫЙ БОЕЦ: {new}")
            elif rand < 0.30: # 15% XP
                st.session_state.xp += 1500; st.info("+1500 XP")
            else: # 70% Cashback
                st.session_state.gold += 2000; st.toast("+2000 Золота")
    else: st.error("Недостаточно золота!")

# --- 6. UI ---
st.markdown("<h1 style='text-align:center;'>🔱 BRAWL STARS: RELOADED</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class="status-bar">
    <span style="color:#f1c40f">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span style="color:#00d2ff">💎 ГЕМЫ: {st.session_state.gems:,}</span>
    <span style="color:#ffffff">🏆 XP: {st.session_state.xp:,}</span>
</div>""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1.2])

with c1:
    st.header("🛒 МАГАЗИН")
    # Box 1
    st.markdown("<div class='box-card'><h4>МАЛЫЙ ЯЩИК</h4><h3>1,000 💰</h3><small>Боец: 5% | Опыт: 10%</small></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ (1,000)", use_container_width=True):
        open_box(1000); st.rerun()
    
    # Box 2
    st.markdown("<div class='box-card'><h4>БОЛЬШОЙ ЯЩИК</h4><h3>5,000 💰</h3><small>Боец: 15% | Опыт: 15%</small></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ (5,000)", use_container_width=True):
        open_box(5000); st.rerun()
    
    st.write("---")
    if st.button("⚔️ В БОЙ (+100 💰 | +250 XP)", use_container_width=True, type="primary"):
        st.session_state.gold += 100
        st.session_state.xp += 250; st.rerun()

with c2:
    st.header("💾 АККАУНТ")
    if st.button("СОХРАНИТЬ (CODE)"):
        data = {'g': st.session_state.gold, 'm': st.session_state.gems, 'x': st.session_state.xp, 'i': st.session_state.inv, 'c': st.session_state.claimed, 'p': st.session_state.pass_type}
        st.code(base64.b64encode(json.dumps(data).encode()).decode())
    
    in_code = st.text_input("ВСТАВИТЬ КОД:")
    if st.button("ЗАГРУЗИТЬ"):
        try:
            d = json.loads(base64.b64decode(in_code).decode())
            st.session_state.update({'gold':d['g'], 'gems':d['m'], 'xp':d['x'], 'inv':d['i'], 'claimed':d['c'], 'pass_type':d['p']})
            st.success("Данные загружены!"); st.rerun()
        except: st.error("Ошибка кода!")

    st.write("---")
    st.header("🎫 BRAWL PASS")
    st.write(f"Тип: **{st.session_state.pass_type}**")
    if st.session_state.pass_type == 'Free':
        if st.button("КУПИТЬ PLUS (499 💎)", use_container_width=True):
            if st.session_state.gems >= 499:
                st.session_state.gems -= 499; st.session_state.pass_type = 'Plus'; st.rerun()
            else: st.error("Недостаточно гемов!")
    
    st.button("PREMIUM ($)", disabled=True, help="Недоступно в вашем регионе")

with c3:
    st.header("👤 БОЙЦЫ & ПРОГРЕСС")
    lvl = st.session_state.xp // 5000
    st.progress(min((st.session_state.xp % 5000) / 5000, 1.0))
    st.write(f"Уровень Pass: {lvl} / 30")
    
    st.markdown("<div class='pass-panel'>", unsafe_allow_html=True)
    for i in range(1, 31):
        unlocked = lvl >= i
        claimed = i in st.session_state.claimed
        st.write(f"Lvl {i}: {'✅' if claimed else ('🎁' if unlocked else '🔒')}")
        if unlocked and not claimed:
            if st.button(f"Забрать {i}", key=f"get_{i}"):
                st.session_state.gold += 1000; st.session_state.gems += 50
                st.session_state.claimed.append(i); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.subheader(f"КОЛЛЕКЦИЯ ({len(st.session_state.inv)}/78)")
b_cols = st.columns(6)
for i, name in enumerate(st.session_state.inv):
    with b_cols[i % 6]:
        st.markdown(f"<div class='brawler-item'>{name}</div>", unsafe_allow_html=True)
