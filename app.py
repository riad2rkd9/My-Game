import streamlit as st
import numpy as np
import time

# Page Configuration
st.set_page_config(
    page_title="Thar 4x4 Off-Road Simulator",
    page_icon="🚗",
    layout="centered"
)

# Custom Styling for Retro Arcade Vibe
st.markdown("""
    <style>
    .reportview-container { background: #1e1e1e; }
    h1 { color: #FF4B4B; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 Thar 4x4 Off-Road Sandbox")
st.caption("A retro 2D grid simulator built specifically for Streamlit. Control your Thar, avoid obstacles, and survive the terrain!")

# Game Configuration Constants
GRID_SIZE = 10
EMPTY = "⬜"
THAR = "🚜"  # Using tractor icon to capture that rugged 4x4 Tochan look
OBSTACLE = "🪨"
FINISH = "🏆"

# Initialize Session State Variables for Game Engine
if 'thar_x' not in st.session_state:
    st.session_state.thar_x = 0
    st.session_state.thar_y = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.moves = 0
    
    # Generate random static obstacle coordinates
    np.random.seed(42)  # Consistent map layout
    obstacles = []
    while len(obstacles) < 15:
        obs = (np.random.randint(0, GRID_SIZE), np.random.randint(0, GRID_SIZE))
        if obs != (0,0) and obs != (GRID_SIZE-1, GRID_SIZE-1) and obs not in obstacles:
            obstacles.append(obs)
    st.session_state.obstacles = obstacles

# Helper function to process movement physics
def move_thar(dx, dy):
    if st.session_state.game_over:
        return
    
    new_x = max(0, min(GRID_SIZE - 1, st.session_state.thar_x + dx))
    new_y = max(0, min(GRID_SIZE - 1, st.session_state.thar_y + dy))
    
    st.session_state.moves += 1
    
    # Check for Collisions
    if (new_x, new_y) in st.session_state.obstacles:
        st.session_state.game_over = True
        st.error("💥 BOOM! You crashed your Thar into a massive off-road boulder! Game Over.")
    elif new_x == GRID_SIZE - 1 and new_y == GRID_SIZE - 1:
        st.session_state.game_over = True
        st.session_state.score += 100
        st.success("🏆 VICTORY! You navigated through the rough terrain safely!")
    else:
        st.session_state.thar_x = new_x
        st.session_state.thar_y = new_y
        st.session_state.score += 10

# Reset Engine
def reset_game():
    st.session_state.thar_x = 0
    st.session_state.thar_y = 0
    st.session_state.score = 0
    st.session_state.moves = 0
    st.session_state.game_over = False

# Layout - Dashboard Statistics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Score", value=st.session_state.score)
with col2:
    st.metric(label="Total Moves", value=st.session_state.moves)
with col3:
    status = "🔴 Crashed" if st.session_state.game_over else "🟢 Driving"
    st.metric(label="Engine Status", value=status)

# Render the 2D Driving Grid Array
grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Place Objects on map
for (ox, oy) in st.session_state.obstacles:
    grid[oy][ox] = OBSTACLE
grid[GRID_SIZE-1][GRID_SIZE-1] = FINISH
grid[st.session_state.thar_y][st.session_state.thar_x] = THAR

# Display Map Graphic
map_string = ""
for row in grid:
    map_string += " ".join(row) + "\n"
st.text(map_string)

# Controller Dashboard Layout
st.markdown("### 🎮 Vehicle Controls")
c_up, c_down, c_left, c_right, c_reset = st.columns(5)

with c_up:
    if st.button("🔼 Forward", use_container_width=True):
        move_thar(0, -1)
        st.rerun()

with c_down:
    if st.button("🔽 Reverse", use_container_width=True):
        move_thar(0, 1)
        st.rerun()

with c_left:
    if st.button("◀️ Steer Left", use_container_width=True):
        move_thar(-1, 0)
        st.rerun()

with c_right:
    if st.button("▶️ Steer Right", use_container_width=True):
        move_thar(1, 0)
        st.rerun()

with c_reset:
    if st.button("🔄 Reset Thar", use_container_width=True, type="primary"):
        reset_game()
        st.rerun()

st.info("💡 **Objective:** Move the Thar (🚜) from the top-left (0,0) corner down to the Trophy destination (🏆) at the bottom-right while steering completely clear of the boulders (🪨).")
