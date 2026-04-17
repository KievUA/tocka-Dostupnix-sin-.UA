import streamlit as st
import random

# Saytni kengroq formatda ochamiz
st.set_page_config(page_title="Emoji Labirinti", page_icon="🕵️", layout="centered")

# --- O'YIN SOZLAMALARI ---
WIDTH = 7
HEIGHT = 5

def initialize_game():
    st.session_state.player_pos = [0, 0]
    st.session_state.treasure_pos = [random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)]
    # Xazina o'yinchi ustiga tushib qolmasligi uchun
    while st.session_state.treasure_pos == st.session_state.player_pos:
        st.session_state.treasure_pos = [random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)]
    st.session_state.moves = 0
    st.session_state.game_over = False

if 'player_pos' not in st.session_state:
    initialize_game()

# --- HARAKAT FUNKSIYALARI ---
def move_player(direction):
    if st.session_state.game_over: return
    
    st.session_state.moves += 1
    if direction == "Yuqoriga" and st.session_state.player_pos[1] > 0:
        st.session_state.player_pos[1] -= 1
    elif direction == "Pastga" and st.session_state.player_pos[1] < HEIGHT - 1:
        st.session_state.player_pos[1] += 1
    elif direction == "Chapga" and st.session_state.player_pos[0] > 0:
        st.session_state.player_pos[0] -= 1
    elif direction == "O'ngga" and st.session_state.player_pos[0] < WIDTH - 1:
        st.session_state.player_pos[0] += 1

# --- INTERFEYS ---
st.title("🕵️ Xazinani topish o'yini!")
st.write(f"Qadamlar soni: **{st.session_state.moves}**")

# Haritani chizish
grid = ""
for y in range(HEIGHT):
    row = ""
    for x in range(WIDTH):
        if [x, y] == st.session_state.player_pos:
            row += " 🧑‍🚀 " # O'yinchi
        elif [x, y] == st.session_state.treasure_pos and st.session_state.game_over:
            row += " 💎 " # Topilgan xazina
        else:
            row += " ⬛ " # Bo'sh joy
    grid += row + "\n\n"

st.markdown(f"```\n{grid}\n```")

# Boshqaruv tugmalari
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("⬆️ Yuqoriga"): move_player("Yuqoriga"); st.rerun()

col_a, col_b, col_c = st.columns([1, 1, 1])
with col_a:
    if st.button("⬅️ Chapga"): move_player("Chapga"); st.rerun()
with col_b:
    if st.button("♻️ Yangilash"): initialize_game(); st.rerun()
with col_c:
    if st.button("➡️ O'ngga"): move_player("O'ngga"); st.rerun()

with col2:
    if st.button("⬇️ Pastga"): move_player("Pastga"); st.rerun()

# G'alaba sharti
if st.session_state.player_pos == st.session_state.treasure_pos:
    st.session_state.game_over = True
    st.balloons()
    st.success(f"TABRIKLAYMIZ! 💎 Xazinani {st.session_state.moves} ta qadamda topdingiz!")
    if st.button("Yangi o'yin boshlash"):
        initialize_game()
        st.rerun()

st.info("Maslahat: Qora kvadratlar bo'ylab yuring va yashirin xazinani qidiring!")
