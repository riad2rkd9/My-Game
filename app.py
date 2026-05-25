from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# --- WINDOW SETUP ---
window.title = "Ultimate 3D Driving Simulator"
window.fps_counter.enabled = True
window.exit_button.visible = False

# --- GAME VARIABLES ---
current_vehicle_idx = 0
vehicles_data = [
    {"name": "Car", "color": color.red, "scale": (1.5, 1, 2.5), "speed": 25},
    {"name": "Jeep", "color": color.orange, "scale": (1.8, 1.5, 2.8), "speed": 20},
    {"name": "Truck", "color": color.blue, "scale": (2.2, 2.5, 5), "speed": 12},
    {"name": "Boat", "color": color.cyan, "scale": (1.6, 1.2, 3), "speed": 18}
]

money = 100
current_track = "Highway"

# --- 3D ENVIRONMENT CREATION ---
# Sky
Sky()

# Ground / Track
ground = Entity(model='plane', scale=(500, 1, 500), texture='grass', collider='box')

# Simple 3D Hills (Obstacles)
hills = []
def generate_hills():
    global hills
    for h in hills:
        destroy(h)
    hills.clear()
    
    # Generate some random 3D blocks representing terrain/hills
    for _ in range(40):
        h = Entity(
            model='cube', 
            position=(random.uniform(-100, 100), 2, random.uniform(-100, 100)),
            scale=(random.uniform(5, 15), random.uniform(2, 10), random.uniform(5, 15)),
            color=color.dark_grey,
            collider='box'
        )
        hills.append(h)

generate_hills()

# --- THE VEHICLE ENTITY ---
v_meta = vehicles_data[current_vehicle_idx]
player_vehicle = Entity(
    model='cube', 
    color=v_meta["color"], 
    scale=v_meta["scale"], 
    position=(0, 1, 0), 
    collider='box'
)

# Attach Camera smoothly behind the vehicle
camera.parent = player_vehicle
camera.position = (0, 5, -10)
camera.rotation_x = 20

# --- SCREEN UI DISPLAY ---
ui_text = Text(
    text=f'Vehicle: {v_meta["name"]} | Track: {current_track} | Money: ${money}\nControls: WASD/Arrows to Drive | SPACE to Brake | V to Change Vehicle | T to Change Terrain',
    position=(-0.7, 0.45),
    scale=1.5,
    color=color.yellow
)

# --- GAME ENGINE LOOP (Runs 60+ FPS) ---
speed = 0
def update():
    global speed, current_track, money
    v_meta = vehicles_data[current_vehicle_idx]
    
    # 1. Steering & Driving Physics Mechanics
    max_speed = v_meta["speed"]
    
    # Acceleration / Forward
    if held_keys['w'] or held_keys['up arrow']:
        speed = min(speed + 20 * time.dt, max_speed)
    # Reverse / Brake
    elif held_keys['s'] or held_keys['down arrow']:
        speed = max(speed - 20 * time.dt, -max_speed/2)
    # Natural Friction deceleration
    else:
        if speed > 0: speed = max(0, speed - 10 * time.dt)
        if speed < 0: speed = min(0, speed + 10 * time.dt)
        
    # Spacebar for Emergency Hard Hand-Brake
    if held_keys['space']:
        if speed > 0: speed = max(0, speed - 40 * time.dt)
        if speed < 0: speed = min(0, speed + 40 * time.dt)

    # Steering turning angles
    if held_keys['a'] or held_keys['left arrow']:
        player_vehicle.rotation_y -= 60 * time.dt * (speed / max_speed)
    if held_keys['d'] or held_keys['right arrow']:
        player_vehicle.rotation_y += 60 * time.dt * (speed / max_speed)

    # Move vehicle forward based on its current rotation angle
    player_vehicle.position += player_vehicle.forward * speed * time.dt

    # Simple Check Bounds / Rewards loop simulation
    if player_vehicle.z > 200:
        money += 50
        player_vehicle.z = -200 # Loop map back around
        ui_text.text = f'Vehicle: {v_meta["name"]} | Track: {current_track} | Money: ${money}\nControls: WASD/Arrows | SPACE to Brake | V to Change Vehicle | T to Change Terrain'

# --- INPUT HANDLING ---
def input(key):
    global current_vehicle_idx, current_track
    
    # Switch Vehicles instantly via key 'v'
    if key == 'v':
        current_vehicle_idx = (current_vehicle_idx + 1) % len(vehicles_data)
        v = vehicles_data[current_vehicle_idx]
        player_vehicle.model = 'cube'
        player_vehicle.color = v["color"]
        player_vehicle.scale = v["scale"]
        
    # Switch Tracks / Difficulty visually via key 't'
    if key == 't':
        if current_track == "Highway":
            current_track = "Risky Hill Tracks"
            ground.color = color.brown
            generate_hills()
        else:
            current_track = "Highway"
            ground.color = color.green
            # Remove objects for flat clear highway
            for h in hills: destroy(h)
            hills.clear()

app.run()
