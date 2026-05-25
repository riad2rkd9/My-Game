import streamlit as st
import sqlite3
import random

# --- DATABASE SETUP ---
DB_FILE = "driving_game.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            username TEXT PRIMARY KEY,
            money REAL,
            miles_driven REAL
        )
    ''')
    conn.commit()
    conn.close()

def get_player(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT money, miles_driven FROM players WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"money": row[0], "miles": row[1]}
    return None

def save_player(username, money, miles):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO players (username, money, miles_driven)
        VALUES (?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            money = excluded.money,
            miles_driven = excluded.miles_driven
    ''', (username, money, miles))
    conn.commit()
    conn.close()

# Initialize Database
init_db()

# --- STREAMLIT PAGE SETUP ---
st.set_page_config(page_title="Multiverse Driving Simulator", page_icon="🚗", layout="centered")
st.title("🚗 Multiverse Driving Simulator 🌊")
st.write("Manage your speed, gears, and steering to survive the tracks and earn cash.")

# --- GAME STATE MANAGEMENT ---
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "game_active" not in st.session_state:
    st.session_state.game_active = False

# --- LOGIN / PROFILE SECTION ---
if not st.session_state.logged_in:
    st.subheader("Profile Login")
    name_input = st.text_input("Enter Driver Profile Name:", max_chars=15).strip()
    if st.button("Load / Create Profile"):
        if name_input:
            st.session_state.player_name = name_input
            st.session_state.logged_in = True
            
            data = get_player(name_input)
            if data:
                st.session_state.money = data["money"]
                st.session_state.miles = data["miles"]
                st.success(f"Welcome back, Driver {name_input}!")
            else:
                st.session_state.money = 100.0  # Starting cash
                st.session_state.miles = 0.0
                save_player(name_input, st.session_state.money, st.session_state.miles)
                st.info(f"Created a new profile for {name_input}!")
            st.rerun()
        else:
            st.error("Please enter a valid profile name.")
    st.stop()

# Display Persistent Dashboard
st.sidebar.markdown(f"### 👤 Driver: **{st.session_state.player_name}**")
st.sidebar.metric("Balance", f"${st.session_state.money:.2f}")
st.sidebar.metric("Career Distance", f"{st.session_state.miles:.1f} miles")
if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.rerun()

# --- SETUP NEW MISSION ---
if not st.session_state.game_active:
    st.subheader("🏁 Configure Your Next Trip")
    
    col1, col2 = st.columns(2)
    with col1:
        vehicle = st.selectbox("Select Your Ride:", ["Sedan Car", "4x4 Jeep", "Heavy Truck", "Speed Boat"])
        track = st.selectbox("Select Terrain:", ["Open Highway", "Rocky Hill Tracks", "Deep Water Route"])
    with col2:
        difficulty = st.radio("Risk Level:", ["Easy (Safe pacing)", "Risky (High hazard, 2x reward)"])
        
    if st.button("Start Engine 🔑"):
        # Basic validation rule
        if vehicle == "Speed Boat" and track != "Deep Water Route":
            st.error("❌ Boats can only navigate the Deep Water Route!")
        elif vehicle != "Speed Boat" and track == "Deep Water Route":
            st.error("❌ Land vehicles will sink in Deep Water! Select the Boat.")
        else:
            # Initialize trip variables
            st.session_state.game_active = True
            st.session_state.vehicle = vehicle
            st.session_state.track = track
            st.session_state.difficulty = difficulty
            st.session_state.progress = 0  # 0 to 100%
            st.session_state.speed = 0
            st.session_state.gear = "N"
            st.session_state.logs = ["Engine started. Safe travels!"]
            st.rerun()
    st.stop()

# --- ACTIVE SIMULATOR INTERFACE ---
st.header(f"Driving: {st.session_state.vehicle} on {st.session_state.track}")
st.caption(f"Risk Setting: {st.session_state.difficulty}")

# Base metrics
progress_bar = st.progress(st.session_state.progress / 100)
st.write(f"**Trip Progress:** {st.session_state.progress}% Complete")

# Columns for controls
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("### 🕹️ Cockpit Controls")
    
    # Steering & Braking inputs
    steering = st.slider("Steering Alignment", -10, 10, 0, help="Keep it centered around sharp curves!")
    brake = st.checkbox("Apply Brake")
    
    # Gear configuration
    gear_options = ["R", "N", "1", "2", "3", "4"] if st.session_state.vehicle != "Speed Boat" else ["R", "N", "Half Throttle", "Full Throttle"]
    gear = st.selectbox("Gear Box", gear_options, index=1)

with col_right:
    st.markdown("### 🛣️ Windshield & Environment")
    
    # Process turn actions
    if st.button("Advance 10% Progress ➡️"):
        hazard = random.randint(1, 10)
        risk_multiplier = 2 if st.session_state.difficulty == "Risky" else 1
        
        # Physics engine math emulation
        if gear in ["N", "R"]:
            current_speed = 0
            st.session_state.logs.append("You are idling or reversing. No forward progress made.")
        else:
            current_speed = random.randint(30, 50) if "1" in gear or "Half" in gear else random.randint(65, 90)
            if brake:
                current_speed = max(0, current_speed - 40)
            
            # Handle track specific hurdles
            crash = False
            if st.session_state.track == "Rocky Hill Tracks" and current_speed > 50 and steering == 0:
                crash = True
                fail_msg = "💥 Rolled over a sharp hill ledge due to excess speed without steering corrections!"
            elif hazard > (8 - risk_multiplier):
                # Hazard triggered
                if abs(steering) < 4 and not brake:
                    crash = True
                    fail_msg = f"💥 Obstacle appeared! Failed to steer/brake in time on the {st.session_state.track}."
            
            if crash:
                # Calculate Partial Payout
                payout = 0.0
                if st.session_state.progress >= 50:
                    payout = 15.0 * risk_multiplier
                    st.session_state.money += payout
                    st.session_state.logs.append(f"Halfway benchmark cleared before crash! Received partial recovery payout: ${payout}")
                
                st.error(fail_msg)
                st.session_state.game_active = False
                save_player(st.session_state.player_name, st.session_state.money, st.session_state.miles)
                if st.button("Return to Garage"):
                    st.rerun()
                st.stop()
            else:
                # Successful tick
                st.session_state.progress += 10
                st.session_state.miles += (current_speed / 10)
                st.session_state.logs.append(f"Cruising safely at {current_speed} mph. Steering stable.")
        
        # Check Win Condition
        if st.session_state.progress >= 100:
            base_reward = 50.0
            total_payout = base_reward * risk_multiplier
            st.session_state.money += total_payout
            save_player(st.session_state.player_name, st.session_state.money, st.session_state.miles)
            
            st.balloons()
            st.success(f"🎉 Destination reached safely! You earned a full payout of ${total_payout}!")
            st.session_state.game_active = False
            if st.button("Claim Rewards & Leave"):
                st.rerun()
            st.stop()
            
        st.rerun()

# Log display console
st.text_area("Radio & Telemetry Logs", value="\n".join(st.session_state.logs[-4:]), height=120)

if st.button("Abandon Run 🚨"):
    st.session_state.game_active = False
    st.rerun()
