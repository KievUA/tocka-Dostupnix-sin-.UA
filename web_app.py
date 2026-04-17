import streamlit as st
import time

# Конфигурация страницы
st.set_page_config(page_title="Симулятор Миллионера 3.0", page_icon="💎", layout="wide")

# --- СУПЕР ДИЗАЙН (CSS) ---
st.markdown("""
    <style>
    /* Общий фон страницы */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }
    
    /* Дисплей с деньгами */
    .money-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid #00ffcc;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
    }
    .money-text {
        font-size: 65px;
        font-weight: bold;
        color: #00ffcc;
        text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
    }

    /* Карточки товаров */
    .shop-item {
        background: rgba(0, 0, 0, 0.4);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.4s;
        text-align: center;
    }
    .shop-item:hover {
        border-color: #00ffcc;
        transform: translateY(-5px);
        background: rgba(0, 0, 0, 0.6);
    }

    /* Стиль изображений */
    .item-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    /* Инвентарь */
    .inv-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 8px;
        border-left: 4px solid #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ЛОГИКА ИГРЫ ---
if 'money' not in st.session_state: st.session_state.money = 0
if 'click' not in st.session_state: st.session_state.click = 100
if 'income' not in st.session_state: st.session_state.income = 0
if 'inventory' not in st.session_state: st.session_state.inventory = []
if 'last_tick' not in st.session_state: st.session_state.last_tick = time.time()

# Пассивный доход (обновление)
now = time.time()
diff = int(now - st.session_state.last_tick)
if diff >= 1:
    st.session_state.money += diff * st.session_state.income
    st.session_state.last_tick = now

# --- ВЕРХНЯЯ ЧАСТЬ ---
st.markdown(f"""
    <div class='money-card'>
        <div style='font-size: 20px; color: #aaa;'>Ваш Баланс</div>
        <div class='money-text'>{st.session_state.money:,.0f} $</div>
    </div>
    """, unsafe_allow_html=True)

col_work, col_shop = st.columns([1, 2.5])

# --- ЛЕВАЯ КОЛОНКА: РАБОТА И ИМУЩЕСТВО ---
with col_work:
    st.header("💼 Карьера")
    if st.button("РАБОТАТЬ 👷‍♂️", use_container_width=True):
        st.session_state.money += st.session_state.click
        st.rerun()
    
    st.write(f"Доход за клик: **{st.session_state.click} $**")
    st.write(f"Доход в секунду: **{st.session_state.income} $**")
    
    st.write("---")
    st.header("🏠 Моё Имущество")
    if not st.session_state.inventory:
        st.write("У вас пока ничего нет.")
    else:
        for item in st.session_state.inventory:
            st.markdown(f"<div class='inv-box'>✅ {item}</div>", unsafe_allow_html=True)

# --- ПРАВАЯ КОЛОНКА: МАГАЗИН ---
with col_shop:
    st.header("🏪 Элитный Маркет")
    
    # Список товаров (Исправленные ссылки на фото)
    items = [
        {"name": "Chevrolet Spark", "price": 11000, "img": "https://raw.githubusercontent.com/Sabir568/images/main/spark.jpg", "inc": 0},
        {"name": "Chevrolet Gentra", "price": 16000, "img": "https://raw.githubusercontent.com/Sabir568/images/main/gentra.jpg", "inc": 0},
        {"name": "Chevrolet Malibu 2", "price": 33000, "img": "https://raw.githubusercontent.com/Sabir568/images/main/malibu.jpg", "inc": 0},
        {"name": "Ресторан 'Sky Lounge'", "price": 90000, "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=500", "inc": 200},
        {"name": "Вилла в Ташкенте", "price": 250000, "img": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=500", "inc": 600},
        {"name": "Небоскреб City", "price": 1000000, "img": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=500", "inc": 3000}
    ]

    # Сетка магазина
    rows = [st.columns(2), st.columns(2), st.columns(2)]
    for idx, item in enumerate(items):
        col = rows[idx // 2][idx % 2]
        with col:
            st.markdown(f"""
                <div class='shop-item'>
                    <img src='{item['img']}' class='item-img'>
                    <h3>{item['name']}</h3>
                    <p style='color: #00ffcc; font-weight: bold;'>Цена: {item['price']:,} $</p>
                    {f"<p style='color: #55ff55;'>Доход: +{item['inc']}$/сек</p>" if item['inc'] > 0 else ""}
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Купить {item['name']}", key=f"btn_{idx}"):
                if st.session_state.money >= item['price']:
                    st.session_state.money -= item['price']
                    st.session_state.inventory.append(item['name'])
                    st.session_state.income += item['inc']
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Недостаточно денег!")

# Сброс
st.sidebar.title("Меню")
if st.sidebar.button("Сбросить прогресс 🔄"):
    st.session_state.clear()
    st.rerun()
