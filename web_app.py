import streamlit as st
import time

# Sayt sozlamalari (Vizual rejim)
st.set_page_config(page_title="Samarqand Magnati 2.0 🏰", page_icon="💰", layout="wide")

# --- CUSTOM CSS (Dizaynni chiroyli qilish) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .gold-display {
        font-size: 70px; font-weight: bold; color: #00FF00;
        text-align: center; border: 3px solid #00FF00;
        border-radius: 25px; padding: 15px; margin-bottom: 25px;
        text-shadow: 2px 2px 4px #000;
    }
    .shop-card {
        background-color: #1E1E1E; padding: 15px;
        border-radius: 15px; border: 1px solid #333;
        margin-bottom: 20px; text-align: center;
        transition: 0.3s;
    }
    .shop-card:hover { transform: scale(1.02); border-color: #00FF00; }
    .prop-img { border-radius: 10px; margin-bottom: 10px; width: 100%; height: 150px; object-fit: cover; }
    .stat-box { background-color: #262730; padding: 20px; border-radius: 15px; border-left: 5px solid #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

# --- O'YIN HOLATINI BOSHQARISH ---
if 'money' not in st.session_state: st.session_state.money = 0
if 'click_power' not in st.session_state: st.session_state.click_power = 50  # Boshlanishiga kattaroq
if 'passive_income' not in st.session_state: st.session_state.passive_income = 0
if 'inventory' not in st.session_state: st.session_state.inventory = []
if 'last_time' not in st.session_state: st.session_state.last_time = time.time()

# Avtomatik daromadni hisoblash
now = time.time()
diff = now - st.session_state.last_time
if diff >= 1:
    st.session_state.money += int(diff * st.session_state.passive_income)
    st.session_state.last_time = now

# --- ASOSIY EKRAN ---
st.markdown(f"<div class='gold-display'>{st.session_state.money:,.0f} $</div>", unsafe_allow_html=True)

col_work, col_shop = st.columns([1, 2])

# --- 1. ISHLASH BO'LIMI ---
with col_work:
    st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
    st.subheader("Biznesni boshqarish 📈")
    st.write(f"Har bir bosish: **{st.session_state.click_power:,.0f} $**")
    st.write(f"Avtomatik daromad: **{st.session_state.passive_income:,.0f} $/sek**")
    
    if st.button("PUL QAZIB OLISH ⛏️", use_container_width=True):
        st.session_state.money += st.session_state.click_power
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")
    # INVENTAR
    st.subheader("Mening Mulklarim 📦")
    if not st.session_state.inventory:
        st.write("Hozircha faqat orzular bor...")
    else:
        for item in st.session_state.inventory:
            st.write(f"✅ {item}")

# --- 2. VIZUAL DO'KON BO'LIMI ---
with col_shop:
    st.header("Premium Bozori 🛍️")
    
    # MULKLAR RO'YXATI (RASMLAR BILAN)
    # Eslatma: Rasmlar internetdan olingan namuna havolalar.
    properties = [
        {"nomi": "Spark (Oq)", "narxi": 12000, "img": "https://img.images.uz/2023/10/26/16983053644485.jpg", "turi": "moshina", "daromad": 0},
        {"nomi": "Gentra (Qora)", "narxi": 18000, "img": "https://avtoelon.uz/m/posts/6561579b76c898a96e5793e2/image-1.jpg", "turi": "moshina", "daromad": 0},
        {"nomi": "Malibu 2 Turbo", "narxi": 35000, "img": "https://motor.uz/files/cache/motor.uz/uploads/malibu/original/5e3b5e4368153_main_image.jpg", "turi": "moshina", "daromad": 0},
        {"nomi": "Toshkent City (Xonadon)", "narxi": 150000, "img": "https://tashkentcity.uz/storage/photos/shares/banners/banner_3.jpg", "turi": "uy", "daromad": 100},
        {"nomi": "Hovli (G'azalkent)", "narxi": 300000, "img": "https://img.images.uz/2022/10/27/16668744577815.jpg", "turi": "uy", "daromad": 250},
    ]

    # Kartochkalarni 2 ta ustunga bo'lish
    shop_cols = st.columns(2)
    
    for i, prop in enumerate(properties):
        col_idx = i % 2 # 0 yoki 1
        with shop_cols[col_idx]:
            st.markdown(f"<div class='shop-card'>", unsafe_allow_html=True)
            # Rasm
            st.markdown(f"<img src='{prop['img']}' class='prop-img'>", unsafe_allow_html=True)
            # Ma'lumot
            st.write(f"### {prop['nomi']}")
            st.write(f"Narxi: **{prop['narxi']:,} $**")
            if prop['daromad'] > 0:
                st.write(f"Daromad: **+{prop['daromad']} $/sek**")
            
            # Sotib olish tugmasi
            if st.button(f"Sotib olish ({prop['nomi']})", key=prop['nomi']):
                if st.session_state.money >= prop['narxi']:
                    st.session_state.money -= prop['narxi']
                    st.session_state.inventory.append(f"{prop['nomi']}")
                    st.session_state.passive_income += prop['daromad']
                    st.balloons()
                    st.success("Tabriklaymiz! Muvaffaqiyatli xarid.")
                    st.rerun()
                else:
                    st.error("Mablag' yetarli emas!")
            st.markdown("</div>", unsafe_allow_html=True)

# Yon panel
st.sidebar.title("Sozlamalar")
if st.sidebar.button("O'yinni noldan boshlash (Reset)"):
    st.session_state.clear()
    st.rerun()
