import streamlit as st
import time

# Sayt sozlamalari
st.set_page_config(page_title="Boylik Simulyatori 🏰", page_icon="💰", layout="wide")

# --- STYLING (Haqiqiy biznes dizayn) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .gold-display {
        font-size: 60px; font-weight: bold; color: #00FF00;
        text-align: center; border: 2px solid #00FF00;
        border-radius: 20px; padding: 10px; margin-bottom: 20px;
    }
    .stat-card {
        background-color: #1E1E1E; padding: 15px;
        border-radius: 10px; border-bottom: 4px solid #FF4B4B;
        text-align: center;
    }
    .buy-card {
        background-color: #262730; padding: 20px;
        border-radius: 15px; border: 1px solid #444;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- O'YIN HOLATI ---
if 'money' not in st.session_state:
    st.session_state.money = 0
if 'click_power' not in st.session_state:
    st.session_state.click_power = 10
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'last_time' not in st.session_state:
    st.session_state.last_time = time.time()

# --- ASOSIY QISM ---
col_main, col_inv = st.columns([2, 1])

with col_main:
    st.markdown(f"<div class='gold-display'>{st.session_state.money:,.0f} $</div>", unsafe_allow_html=True)
    
    if st.button("PUL ISHLASH (10 $)", use_container_width=True):
        st.session_state.money += st.session_state.click_power
        st.rerun()

    st.write("---")
    st.header("Avtosalon va Ko'chmas Mulk 🛍️")
    
    # DO'KON BUYUMLARI
    items = [
        {"nomi": "Spark", "narxi": 10000, "icon": "🚗", "turi": "Moshina"},
        {"nomi": "Gentra", "narxi": 15000, "icon": "🚘", "turi": "Moshina"},
        {"nomi": "Malibu 2", "narxi": 30000, "icon": "🏎️", "turi": "Moshina"},
        {"nomi": "Toshkent City (Xonadon)", "narxi": 100000, "icon": "🏢", "turi": "Uy"},
        {"nomi": "Hovli (G'azalkent)", "narxi": 250000, "icon": "🏰", "turi": "Uy"},
        {"nomi": "Xususiy Orol", "narxi": 1000000, "icon": "🏝️", "turi": "Mulk"}
    ]

    for item in items:
        with st.container():
            st.markdown(f"<div class='buy-card'>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1, 2, 1])
            with c1: st.write(f"## {item['icon']}")
            with c2: 
                st.write(f"**{item['nomi']}**")
                st.write(f"Narxi: {item['narxi']:,} $")
            with c3:
                if st.button(f"Sotib olish", key=item['nomi']):
                    if st.session_state.money >= item['narxi']:
                        st.session_state.money -= item['narxi']
                        st.session_state.inventory.append(f"{item['icon']} {item['nomi']}")
                        st.balloons()
                        st.success("Tabriklaymiz! Xarid qilindi.")
                        st.rerun()
                    else:
                        st.error("Pul yetarli emas!")
            st.markdown("</div>", unsafe_allow_html=True)

with col_inv:
    st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
    st.subheader("Mening Mulklarim 📦")
    if not st.session_state.inventory:
        st.write("Hozircha hech narsa yo'q. Ishlang va boying!")
    else:
        for i in st.session_state.inventory:
            st.write(f"✅ {i}")
    st.markdown("</div>", unsafe_allow_html=True)

# Reset tugmasi
if st.sidebar.button("Hammasini sotish va Kambag'allikka qaytish"):
    st.session_state.clear()
    st.rerun()
