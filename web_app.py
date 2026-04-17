import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars: Hardcore v21.1", page_icon="⚔️", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    .stApp { background: #000814; color: #ffffff; font-family: 'Arial'; }
    .status-bar { background: rgba(0,0,0,0.9); border: 2px solid #00ffcc; border-radius: 15px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 20px; font-weight: bold; }
    .box-card { background: linear-gradient(135deg, #1a1a1a 0, #2d2d2d 100%); border: 1px solid #444; border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 10px; }
    .pass-panel { background: #050505; border: 2px solid #6200ff; border-radius: 15px; padding: 15px; height: 500px; overflow-y: scroll; }
    .brawler-item { background: #111; border: 1px solid #333; border-radius: 8px; padding: 5px; text-align: center; font-size: 11px; margin-bottom: 5px; }
    .promo-section { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; margin-top: 20px; border: 1px dashed #444; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BRAWLERS DATABASE ---
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
        'claimed': [], 'pass_type': 'Free'
    })

# --- 5. LOGIC FUNCTIONS ---
def open_box(cost):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        rand = random.random()
        if cost == 1000:
            if rand < 0.05:
                new = random.choice([b for b in B_DB if b not in st.session_state.inv])
                if new: st.session_state.inv.append(new); st.balloons()
            elif rand < 0.15: st.session_state.xp += 300
            else: st.session_state.gold += 250
        elif cost == 5000:
            if rand < 0.15:
                new = random.choice([b for b in B_DB if b not in st.session_state.inv])
                if new: st.session_state.inv.append(new); st.balloons()
            elif rand < 0.30: st.session_state.xp += 1000
            else: st.session_state.gold += 2000
    else: st.error("Недостаточно золота!")

# --- 6. UI ---
st.markdown("<h1 style='text-align:center;'>🔱 BRAWL STARS: HARDCORE 2026</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class="status-bar">
    <span style="color:#f1c40f">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span style="color:#00d2ff">💎 ГЕМЫ: {st.session_state.gems:,}</span>
    <span style="color:#ffffff">🏆 XP: {st.session_state.xp:,}</span>
</div>""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1.2])

with c1:
    st.header("🛒 МАГАЗИН")
    st.markdown("<div class='box-card'><h4>МАЛЫЙ ЯЩИК</h4><h3>1,000 💰</h3></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ (1,000)", use_container_width=True):
        open_box(1000); st.rerun()
    
    st.markdown("<div class='box-card'><h4>БОЛЬШОЙ ЯЩИК</h4><h3>5,000 💰</h3></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ (5,000)", use_container_width=True):
        open_box(5000); st.rerun()
    
    st.write("---")
    if st.button("⚔️ В БОЙ (+80 💰 | +150 XP)", use_container_width=True, type="primary"):
        st.session_state.gold += 80
        st.session_state.xp += 150; st.rerun()

with c2:
    st.header("💾 СОХРАНЕНИЕ")
    if st.button("ГЕНЕРИРОВАТЬ КОД", use_container_width=True):
        # Hamma ma'lumotlarni lug'atga yig'ish
        save_data = {
            'gold': st.session_state.gold,
            'gems': st.session_state.gems,
            'xp': st.session_state.xp,
            'inv': st.session_state.inv,
            'claimed': st.session_state.claimed,
            'pass': st.session_state.pass_type
        }
        # Lug'atni JSON qilib keyin Base64 ga o'tkazish
        b64_code = base64.b64encode(json.dumps(save_data).encode()).decode()
        st.code(b64_code)
        st.success("Код создан! Сохраните его.")

    in_code = st.text_input("ВСТАВИТЬ КОД ДЛЯ ЗАГРУЗКИ:")
    if st.button("ЗАГРУЗИТЬ АККАУНТ", use_container_width=True):
        try:
            decoded = json.loads(base64.b64decode(in_code).decode())
            st.session_state.gold = decoded['gold']
            st.session_state.gems = decoded['gems']
            st.session_state.xp = decoded['xp']
            st.session_state.inv = decoded['inv']
            st.session_state.claimed = decoded['claimed']
            st.session_state.pass_type = decoded['pass']
            st.success("✅ Аккаунт успешно загружен!"); st.rerun()
        except: st.error("❌ Ошибка: Код неверный или поврежден!")

    # PROMO SECTION
    st.markdown("<div class='promo-section'>", unsafe_allow_html=True)
    st.subheader("🎫 ПРОМОКОД")
    promo = st.text_input("Введите секретный код:", key="promo_input")
    if st.button("АКТИВИРОВАТЬ"):
        if promo == "APRIL2026":
            if "Сириус" not in st.session_state.inv:
                st.session_state.inv.append("Сириус")
                st.balloons(); st.success("🌟 SIRIUS РАЗБЛОКИРОВАН!")
            else: st.warning("У вас уже есть этот боец.")
        else: st.error("Неверный код.")
    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    st.header("🎫 BRAWL PASS")
    # Har bir level uchun 15,000 XP
    current_lvl = st.session_state.xp // 15000
    progress = (st.session_state.xp % 15000) / 15000
    st.write(f"Уровень: **{current_lvl} / 30**")
    st.progress(min(progress, 1.0))
    
    if st.session_state.pass_type == 'Free':
        if st.button("💎 PLUS (499 ГЕМОВ)", use_container_width=True):
            if st.session_state.gems >= 499:
                st.session_state.gems -= 499; st.session_state.pass_type = 'Plus'; st.rerun()
    st.button("PREMIUM ($)", disabled=True)

    st.markdown("<div class='pass-panel'>", unsafe_allow_html=True)
    for i in range(1, 31):
        unlocked = current_lvl >= i
        claimed = i in st.session_state.claimed
        status = "✅" if claimed else ("🎁" if unlocked else "🔒")
        st.write(f"Уровень {i}: {status}")
        if unlocked and not claimed:
            if st.button(f"Забрать {i}", key=f"cl_{i}"):
                # Kristallar miqdori 50 tadan 10 taga tushirildi
                st.session_state.gold += 800; st.session_state.gems += 10
                st.session_state.claimed.append(i); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.subheader(f"КОЛЛЕКЦИЯ ({len(st.session_state.inv)}/78)")
cols = st.columns(6)
for i, name in enumerate(st.session_state.inv):
    with cols[i % 6]:
        st.markdown(f"<div class='brawler-item'>{name}</div>", unsafe_allow_html=True)
