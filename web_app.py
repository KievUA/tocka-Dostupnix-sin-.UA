import streamlit as st
import time

# Конфигурация страницы
st.set_page_config(page_title="Симулятор Миллионера 3.2", page_icon="💎", layout="wide")

# --- УЛУЧШЕННЫЙ ДИЗАЙН (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        color: #ffffff;
    }
    .money-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 2px solid #00d2ff;
        border-radius: 25px;
        padding: 25px;
        text-align: center;
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(0, 210, 255, 0.2);
    }
    .money-text {
        font-size: 70px;
        font-weight: bold;
        color: #00d2ff;
        text-shadow: 0 0 15px rgba(0, 210, 255, 0.5);
    }
    .shop-item {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: 0.3s ease;
    }
    .shop-item:hover {
        transform: scale(1.03);
        background: rgba(255, 255, 255, 0.07);
        border-color: #00d2ff;
    }
    .item-name {
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
    .inv-box {
        background: rgba(0, 210, 255, 0.1);
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        border-left: 6px solid #00d2ff;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ЛОГИКА ИГРЫ ---
if 'money' not in st.session_state: st.session_state.money = 0
if 'click' not in st.session_state: st.session_state.click = 200
if 'income' not in st.session_state: st.session_state.income = 0
if 'inventory' not in st.session_state: st.session_state.inventory = []
if 'last_tick' not in st.session_state: st.session_state.last_tick = time.time()

# Авто-доход
now = time.time()
diff = int(now - st.session_state.last_tick)
if diff >= 1:
    st.session_state.money += diff * st.session_state.income
    st.session_state.last_tick = now

# --- ВЕРХНЯЯ ПАНЕЛЬ ---
st.markdown(f"""
    <div class='money-card'>
        <div style='font-size: 18px; color: #888; letter-spacing: 2px;'>ВАШ КАПИТАЛ</div>
        <div class='money-text'>{st.session_state.money:,.0f} $</div>
    </div>
    """, unsafe_allow_html=True)

col_work, col_shop = st.columns([1, 2.3])

with col_work:
    st.header("💼 Карьера")
    if st.button("РАБОТАТЬ И ЗАРАБАТЫВАТЬ ⚡", use_container_width=True):
        st.session_state.money += st.session_state.click
        st.rerun()
    
    st.info(f"Клик: **{st.session_state.click}$** | Секунда: **{st.session_state.income}$**")
    
    st.write("---")
    st.header("🏠 Моё Имущество")
    if not st.session_state.inventory:
        st.write("Пока только мечты...")
    else:
        for item in st.session_state.inventory:
            st.markdown(f"<div class='inv-box'>🛒 {item}</div>", unsafe_allow_html=True)

with col_shop:
    st.header("🏪 Элитный Маркет")
    
    # НОВЫЕ ССЫЛКИ НА ФОТО (Pexels и Pixabay - самые надежные)
    items = [
        {"name": "Chevrolet Spark", "price": 10000, "img": "https://images.pexels.com/photos/170811/pexels-photo-170811.jpeg?auto=compress&cs=tinysrgb&w=600", "inc": 0},
        {"name": "Chevrolet Gentra", "price": 15000, "img": "https://images.pexels.com/photos/1149137/pexels-photo-1149137.jpeg?auto=compress&cs=tinysrgb&w=600", "inc": 0},
        {"name": "Chevrolet Malibu 2", "price": 30000, "img": "https://images.pexels.com/photos/210019/pexels-photo-210019.jpeg?auto=compress&cs=tinysrgb&w=600", "inc": 0},
        {"name": "Ресторан 'Prime'", "price": 85000, "img": "https://images.pexels.com/photos/262978/pexels-photo-262978.jpeg?auto=compress&cs=tinysrgb&w=600", "inc": 300},
        {"name": "Вилла Lux", "price": 250000, "img": "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg?auto=compress&cs=tinysrgb&w=600", "inc": 800},
        {"name": "Бизнес Центр", "price": 1000000, "img": "https://images.pexels.com/photos/3183197/pexels-photo-3183197.jpeg?auto=compress&cs=tinysrgb&w=600", "inc": 4000}
    ]

    cols = st.columns(2)
    for idx, item in enumerate(items):
        with cols[idx % 2]:
            st.markdown(f"<div class='shop-item'>", unsafe_allow_html=True)
            st.image(item['img'], use_container_width=True)
            st.markdown(f"<div class='item-name'>{item['name']}</div>", unsafe_allow_html=True)
            st.write(f"Цена: **{item['price']:,} $**")
            
            if st.button(f"Купить {item['name']}", key=f"shop_{idx}", use_container_width=True):
                if st.session_state.money >= item['price']:
                    st.session_state.money -= item['price']
                    st.session_state.inventory.append(item['name'])
                    st.session_state.income += item['inc']
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Нужно больше золота!")
            st.markdown("</div>", unsafe_allow_html=True)

# Сброс
st.sidebar.markdown("### ⚙️ Опции")
if st.sidebar.button("Начать заново 🔄"):
    st.session_state.clear()
    st.rerun()
