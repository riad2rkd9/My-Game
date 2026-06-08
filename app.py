import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="Jungle Bridge Highway - Premium Driving",
    page_icon="🏞️",
    layout="wide"
)

# Custom CSS for premium look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a2f0a 0%, #1a4a1a 50%, #0a2f0a 100%);
    }
    .main-title {
        text-align: center;
        font-family: 'Orbitron', monospace;
        background: linear-gradient(135deg, #ffd700, #ff8c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #ffd700;
        font-size: 1.2em;
        margin-bottom: 20px;
        font-family: 'Orbitron', monospace;
    }
    .dashboard {
        background: rgba(0,0,0,0.8);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #ffd700;
        backdrop-filter: blur(10px);
    }
    .gauge {
        background: #000;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        color: #0f0;
        font-family: 'Orbitron', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0
if 'total_distance' not in st.session_state:
    st.session_state.total_distance = 0

st.markdown('<div class="main-title">🏞️ JUNGLE BRIDGE HIGHWAY 🚗</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Premium Driving Experience | Realistic Physics | Full Controls</div>', unsafe_allow_html=True)

# Create layout with columns
left_col, main_col, right_col = st.columns([1, 3, 1])

with left_col:
    st.markdown("### 📊 VEHICLE STATUS")
    
    # Stats display
    stats_container = st.container()
    with stats_container:
        st.metric("🏆 HIGH SCORE", st.session_state.high_score)
        st.metric("📏 TOTAL DISTANCE", f"{st.session_state.total_distance} km")
        
    st.markdown("---")
    st.markdown("### 🎮 CONTROLS GUIDE")
    st.markdown("""
    **KEYBOARD:**
    - **← →** : Steering
    - **↑** : Accelerator
    - **↓** : Brake
    - **G** : Shift Up
    - **B** : Shift Down
    - **R** : Restart
    
    **GEARS:**
    - 1st: 0-40 km/h
    - 2nd: 40-80 km/h
    - 3rd: 80-120 km/h
    - 4th: 120-160 km/h
    - 5th: 160+ km/h
    """)

# Main game HTML
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            user-select: none;
        }
        
        body {
            background: transparent;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Orbitron', monospace;
        }
        
        .game-wrapper {
            background: linear-gradient(180deg, #0a2f0a 0%, #063306 100%);
            padding: 20px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        }
        
        canvas {
            border: 3px solid #ffd700;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(255,215,0,0.3);
            background: #1a3a1a;
            cursor: none;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-top: 20px;
            padding: 15px;
            background: rgba(0,0,0,0.8);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .gauge {
            text-align: center;
            padding: 10px;
            background: #000;
            border-radius: 10px;
            border: 1px solid #ffd700;
        }
        
        .gauge-label {
            color: #ffd700;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .gauge-value {
            color: #0f0;
            font-size: 24px;
            font-weight: bold;
            font-family: monospace;
        }
        
        .gear-indicator {
            text-align: center;
            padding: 10px;
            background: linear-gradient(135deg, #ffd700, #ff8c00);
            border-radius: 10px;
            font-weight: bold;
            font-size: 28px;
        }
        
        button {
            background: linear-gradient(135deg, #ffd700, #ff8c00);
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: scale(1.05);
        }
        
        @keyframes engineVibration {
            0% { transform: translateX(0px); }
            25% { transform: translateX(1px); }
            75% { transform: translateX(-1px); }
            100% { transform: translateX(0px); }
        }
        
        .vibrate {
            animation: engineVibration 0.05s infinite;
        }
        
        .control-panel {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 15px;
        }
        
        .control-btn {
            background: #333;
            color: white;
            padding: 8px 20px;
            border-radius: 8px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="game-wrapper">
        <canvas id="gameCanvas" width="1000" height="500"></canvas>
        
        <div class="dashboard">
            <div class="gauge">
                <div class="gauge-label">🏁 SPEED</div>
                <div class="gauge-value" id="speedValue">0</div>
                <div class="gauge-label">km/h</div>
            </div>
            <div class="gauge">
                <div class="gauge-label">⚙️ GEAR</div>
                <div class="gear-indicator" id="gearValue">N</div>
            </div>
            <div class="gauge">
                <div class="gauge-label">🔄 RPM</div>
                <div class="gauge-value" id="rpmValue">0</div>
                <div class="gauge-label">x1000</div>
            </div>
            <div class="gauge">
                <div class="gauge-label">⛽ FUEL</div>
                <div class="gauge-value" id="fuelValue">100</div>
                <div class="gauge-label">%</div>
            </div>
        </div>
        
        <div class="control-panel">
            <div class="control-btn">🔼 ACCEL (↑)</div>
            <div class="control-btn">🔽 BRAKE (↓)</div>
            <div class="control-btn">⚙️ SHIFT UP (G)</div>
            <div class="control-btn">⚙️ SHIFT DOWN (B)</div>
            <div class="control-btn">🔄 RESTART (R)</div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        // Game dimensions
        const ROAD_WIDTH = 600;
        const ROAD_X = (canvas.width - ROAD_WIDTH) / 2;
        const LANE_COUNT = 3;
        const LANE_WIDTH = ROAD_WIDTH / LANE_COUNT;
        
        // Car dimensions
        const CAR_WIDTH = 50;
        const CAR_HEIGHT = 80;
        
        // Player position
        let playerLane = 1;
        let playerX = ROAD_X + (playerLane * LANE_WIDTH) + (LANE_WIDTH / 2) - CAR_WIDTH / 2;
        
        // Physics variables
        let speed = 0;
        let gear = 1;
        let rpm = 0;
        let fuel = 100;
        let score = 0;
        let distance = 0;
        let gameRunning = true;
        
        // Input states
        let acceleratorPressed = false;
        let brakePressed = false;
        
        // Road objects
        let obstacles = [];
        let trees = [];
        let bridges = [];
        let frameCount = 0;
        let roadOffset = 0;
        
        // Weather effects
        let particles = [];
        
        // Gear ratios and max speeds
        const gearRatios = {
            1: { maxSpeed: 40, minSpeed: 0, ratio: 0.8 },
            2: { maxSpeed: 80, minSpeed: 40, ratio: 1.2 },
            3: { maxSpeed: 120, minSpeed: 80, ratio: 1.6 },
            4: { maxSpeed: 160, minSpeed: 120, ratio: 2.0 },
            5: { maxSpeed: 220, minSpeed: 160, ratio: 2.4 }
        };
        
        class Obstacle {
            constructor(type, lane) {
                this.type = type; // 'car', 'rock', 'tree'
                this.lane = lane;
                this.x = ROAD_X + (lane * LANE_WIDTH) + (LANE_WIDTH / 2) - 30;
                this.y = -60;
                this.width = 60;
                this.height = 80;
                this.speed = 3 + Math.random() * 3;
            }
            
            update() {
                this.y += this.speed + (speed / 50);
                this.x = ROAD_X + (this.lane * LANE_WIDTH) + (LANE_WIDTH / 2) - this.width / 2;
            }
            
            draw() {
                if (this.type === 'car') {
                    // Enemy car
                    ctx.fillStyle = '#8B0000';
                    ctx.fillRect(this.x, this.y, this.width, this.height);
                    ctx.fillStyle = '#C0C0C0';
                    ctx.fillRect(this.x + 10, this.y + 15, 12, 20);
                    ctx.fillRect(this.x + this.width - 22, this.y + 15, 12, 20);
                } else if (this.type === 'rock') {
                    ctx.fillStyle = '#696969';
                    ctx.beginPath();
                    ctx.ellipse(this.x + this.width/2, this.y + this.height/2, 25, 20, 0, 0, Math.PI*2);
                    ctx.fill();
                } else {
                    // Tree
                    ctx.fillStyle = '#8B4513';
                    ctx.fillRect(this.x + 20, this.y + 40, 20, 40);
                    ctx.fillStyle = '#228B22';
                    ctx.beginPath();
                    ctx.arc(this.x + 30, this.y + 30, 25, 0, Math.PI*2);
                    ctx.fill();
                }
            }
            
            getBounds() {
                return {
                    x: this.x,
                    y: this.y,
                    width: this.width,
                    height: this.height
                };
            }
        }
        
        class Particle {
            constructor(x, y) {
                this.x = x;
                this.y = y;
                this.vx = (Math.random() - 0.5) * 2;
                this.vy = (Math.random() - 0.5) * 2 - 2;
                this.life = 1;
            }
            
            update() {
                this.x += this.vx;
                this.y += this.vy;
                this.life -= 0.02;
            }
            
            draw() {
                ctx.fillStyle = `rgba(255, 100, 0, ${this.life})`;
                ctx.fillRect(this.x, this.y, 3, 3);
            }
        }
        
        function updateRoad() {
            roadOffset += speed / 10;
            
            // Draw road
            ctx.fillStyle = '#2c3e50';
            ctx.fillRect(ROAD_X, 0, ROAD_WIDTH, canvas.height);
            
            // Road markings
            ctx.strokeStyle = '#ffd700';
            ctx.lineWidth = 3;
            ctx.setLineDash([20, 30]);
            
            for (let i = 1; i < LANE_COUNT; i++) {
                const laneX = ROAD_X + i * LANE_WIDTH;
                ctx.beginPath();
                ctx.moveTo(laneX, 0);
                ctx.lineTo(laneX, canvas.height);
                ctx.stroke();
            }
            
            // Center line animation
            ctx.setLineDash([]);
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 4;
            for (let i = 0; i < 20; i++) {
                const y = (roadOffset + i * 40) % canvas.height;
                ctx.beginPath();
                ctx.moveTo(ROAD_X + ROAD_WIDTH/2, y);
                ctx.lineTo(ROAD_X + ROAD_WIDTH/2, y + 20);
                ctx.stroke();
            }
            
            // Jungle scenery
            ctx.fillStyle = '#0a5a0a';
            ctx.fillRect(0, 0, ROAD_X, canvas.height);
            ctx.fillRect(ROAD_X + ROAD_WIDTH, 0, canvas.width - (ROAD_X + ROAD_WIDTH), canvas.height);
            
            // Draw trees in jungle
            for (let i = 0; i < 10; i++) {
                const treeX = (i * 80 + frameCount) % (ROAD_X - 50);
                ctx.fillStyle = '#228B22';
                ctx.fillRect(treeX, canvas.height - 100, 15, 80);
                ctx.beginPath();
                ctx.arc(treeX + 7.5, canvas.height - 110, 20, 0, Math.PI*2);
                ctx.fill();
                
                const treeX2 = ROAD_X + ROAD_WIDTH + i * 80;
                ctx.fillRect(treeX2, canvas.height - 100, 15, 80);
                ctx.beginPath();
                ctx.arc(treeX2 + 7.5, canvas.height - 110, 20, 0, Math.PI*2);
                ctx.fill();
            }
            
            // Bridge sections
            if (Math.floor(distance / 500) % 2 === 0) {
                ctx.fillStyle = 'rgba(139, 69, 19, 0.8)';
                for (let i = 0; i < 5; i++) {
                    ctx.fillRect(ROAD_X, canvas.height - 50 + i * 10, ROAD_WIDTH, 5);
                }
                // Bridge cables
                ctx.beginPath();
                ctx.strokeStyle = '#8B4513';
                ctx.lineWidth = 2;
                for (let i = 0; i < 3; i++) {
                    ctx.moveTo(ROAD_X + i * 200, 0);
                    ctx.lineTo(ROAD_X + i * 200 + 100, canvas.height);
                    ctx.stroke();
                }
            }
        }
        
        function drawCar() {
            // Calculate car position
            playerX = ROAD_X + (playerLane * LANE_WIDTH) + (LANE_WIDTH / 2) - CAR_WIDTH / 2;
            
            // Car body with gradient
            const gradient = ctx.createLinearGradient(playerX, canvas.height - CAR_HEIGHT - 20, 
                                                      playerX + CAR_WIDTH, canvas.height - 20);
            gradient.addColorStop(0, '#FF4500');
            gradient.addColorStop(1, '#FF6347');
            ctx.fillStyle = gradient;
            ctx.fillRect(playerX, canvas.height - CAR_HEIGHT - 20, CAR_WIDTH, CAR_HEIGHT);
            
            // Windows
            ctx.fillStyle = '#1a2632';
            ctx.fillRect(playerX + 8, canvas.height - CAR_HEIGHT - 15, 12, 25);
            ctx.fillRect(playerX + CAR_WIDTH - 20, canvas.height - CAR_HEIGHT - 15, 12, 25);
            
            // Headlights
            ctx.fillStyle = '#ffff00';
            ctx.fillRect(playerX + 5, canvas.height - 15, 8, 6);
            ctx.fillRect(playerX + CAR_WIDTH - 13, canvas.height - 15, 8, 6);
            
            // Taillights
            ctx.fillStyle = '#ff0000';
            ctx.fillRect(playerX + 5, canvas.height - CAR_HEIGHT - 10, 8, 6);
            ctx.fillRect(playerX + CAR_WIDTH - 13, canvas.height - CAR_HEIGHT - 10, 8, 6);
            
            // Wheels
            ctx.fillStyle = '#333';
            ctx.fillRect(playerX + 5, canvas.height - 10, 10, 10);
            ctx.fillRect(playerX + CAR_WIDTH - 15, canvas.height - 10, 10, 10);
            ctx.fillRect(playerX + 5, canvas.height - CAR_HEIGHT - 15, 10, 10);
            ctx.fillRect(playerX + CAR_WIDTH - 15, canvas.height - CAR_HEIGHT - 15, 10, 10);
            
            // Speed effect (motion blur)
            if (speed > 100) {
                ctx.fillStyle = `rgba(255,255,255,${(speed-100)/100})`;
                ctx.fillRect(playerX - 10, canvas.height - CAR_HEIGHT - 20, 5, CAR_HEIGHT);
                ctx.fillRect(playerX + CAR_WIDTH + 5, canvas.height - CAR_HEIGHT - 20, 5, CAR_HEIGHT);
            }
        }
        
        function updatePhysics() {
            // Accelerator
            if (acceleratorPressed && fuel > 0 && gameRunning) {
                let acceleration = (gearRatios[gear].ratio * 0.5);
                speed += acceleration;
                fuel -= 0.05;
                
                // Create exhaust particles
                if (frameCount % 5 === 0) {
                    particles.push(new Particle(playerX + CAR_WIDTH/2, canvas.height - 15));
                }
            }
            
            // Brake
            if (brakePressed && gameRunning) {
                speed -= 1.5;
                if (speed < 0) speed = 0;
            }
            
            // Natural deceleration
            if (!acceleratorPressed && speed > 0) {
                speed -= 0.3;
                if (speed < 0) speed = 0;
            }
            
            // Gear limits
            if (speed > gearRatios[gear].maxSpeed) {
                speed = gearRatios[gear].maxSpeed;
            }
            if (speed < gearRatios[gear].minSpeed && gear > 1) {
                speed = gearRatios[gear].minSpeed;
            }
            
            // Calculate RPM
            rpm = (speed / gearRatios[gear].maxSpeed) * 7 + 1;
            if (rpm > 8) rpm = 8;
            if (rpm < 1) rpm = 1;
            
            // Update score and distance
            if (gameRunning) {
                distance += speed / 1000;
                score = Math.floor(distance * 10);
                
                // Update Streamlit stats
                if (window.parent && window.parent.postMessage) {
                    window.parent.postMessage({
                        type: 'update',
                        score: score,
                        distance: Math.floor(distance)
                    }, '*');
                }
            }
            
            // Update UI elements
            document.getElementById('speedValue').innerHTML = Math.floor(speed);
            document.getElementById('rpmValue').innerHTML = rpm.toFixed(1);
            document.getElementById('gearValue').innerHTML = gear;
            document.getElementById('fuelValue').innerHTML = Math.floor(fuel);
        }
        
        function spawnObstacle() {
            if (!gameRunning) return;
            
            const types = ['car', 'car', 'rock', 'tree'];
            const type = types[Math.floor(Math.random() * types.length)];
            const lane = Math.floor(Math.random() * LANE_COUNT);
            
            // Check if lane is empty
            let laneEmpty = true;
            for (let obs of obstacles) {
                if (obs.lane === lane && obs.y > canvas.height - 200) {
                    laneEmpty = false;
                    break;
                }
            }
            
            if (laneEmpty && obstacles.length < 6) {
                obstacles.push(new Obstacle(type, lane));
            }
        }
        
        function checkCollision() {
            const carBounds = {
                x: playerX,
                y: canvas.height - CAR_HEIGHT - 20,
                width: CAR_WIDTH,
                height: CAR_HEIGHT
            };
            
            for (let i = 0; i < obstacles.length; i++) {
                const obs = obstacles[i];
                const obsBounds = obs.getBounds();
                
                if (carBounds.x < obsBounds.x + obsBounds.width &&
                    carBounds.x + carBounds.width > obsBounds.x &&
                    carBounds.y < obsBounds.y + obsBounds.height &&
                    carBounds.y + carBounds.height > obsBounds.y) {
                    gameRunning = false;
                    if (window.parent && window.parent.postMessage) {
                        window.parent.postMessage({
                            type: 'gameover',
                            score: score
                        }, '*');
                    }
                    return true;
                }
            }
            return false;
        }
        
        function updateGame() {
            if (!gameRunning) return;
            
            // Update obstacles
            for (let i = 0; i < obstacles.length; i++) {
                obstacles[i].update();
                if (obstacles[i].y > canvas.height) {
                    obstacles.splice(i, 1);
                    i--;
                }
            }
            
            // Spawn obstacles based on speed
            frameCount++;
            let spawnRate = Math.max(40, 80 - Math.floor(speed / 5));
            if (frameCount > spawnRate) {
                spawnObstacle();
                frameCount = 0;
            }
            
            // Update particles
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                if (particles[i].life <= 0) {
                    particles.splice(i, 1);
                    i--;
                }
            }
            
            // Fuel consumption
            if (fuel <= 0) {
                gameRunning = false;
            }
            
            checkCollision();
        }
        
        function drawGame() {
            updateRoad();
            
            // Draw obstacles
            for (let obs of obstacles) {
                obs.draw();
            }
            
            drawCar();
            
            // Draw particles
            for (let p of particles) {
                p.draw();
            }
            
            // Game over overlay
            if (!gameRunning) {
                ctx.fillStyle = 'rgba(0,0,0,0.7)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#ffd700';
                ctx.font = 'bold 48px Orbitron';
                ctx.textAlign = 'center';
                ctx.fillText('GAME OVER', canvas.width/2, canvas.height/2);
                ctx.font = '24px Orbitron';
                ctx.fillStyle = '#fff';
                ctx.fillText('Press R to Restart', canvas.width/2, canvas.height/2 + 60);
            }
            
            // HUD
            ctx.fillStyle = '#fff';
            ctx.font = '20px Orbitron';
            ctx.textAlign = 'left';
            ctx.fillText(`SCORE: ${score}`, 20, 50);
            ctx.fillText(`DISTANCE: ${Math.floor(distance)}m`, 20, 80);
            
            // Warning for low fuel
            if (fuel < 20 && gameRunning) {
                ctx.fillStyle = '#ff0000';
                ctx.font = 'bold 16px Orbitron';
                ctx.fillText('⚠️ LOW FUEL!', canvas.width - 150, 50);
            }
        }
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowUp') {
                acceleratorPressed = true;
                e.preventDefault();
            } else if (e.key === 'ArrowDown') {
                brakePressed = true;
                e.preventDefault();
            } else if (e.key === 'ArrowLeft' && gameRunning) {
                playerLane = Math.max(0, playerLane - 1);
                e.preventDefault();
            } else if (e.key === 'ArrowRight' && gameRunning) {
                playerLane = Math.min(LANE_COUNT - 1, playerLane + 1);
                e.preventDefault();
            } else if (e.key === 'g' || e.key === 'G') {
                if (gear < 5 && speed >= gearRatios[gear].maxSpeed * 0.8) {
                    gear++;
                }
                e.preventDefault();
            } else if (e.key === 'b' || e.key === 'B') {
                if (gear > 1 && speed <= gearRatios[gear].minSpeed + 10) {
                    gear--;
                }
                e.preventDefault();
            } else if (e.key === 'r' || e.key === 'R') {
                restartGame();
                e.preventDefault();
            }
        });
        
        document.addEventListener('keyup', (e) => {
            if (e.key === 'ArrowUp') {
                acceleratorPressed = false;
            } else if (e.key === 'ArrowDown') {
                brakePressed = false;
            }
        });
        
        function restartGame() {
            speed = 0;
            gear = 1;
            fuel = 100;
            score = 0;
            distance = 0;
            obstacles = [];
            particles = [];
            frameCount = 0;
            playerLane = 1;
            gameRunning = true;
            acceleratorPressed = false;
            brakePressed = false;
            
            document.getElementById('speedValue').innerHTML = '0';
            document.getElementById('rpmValue').innerHTML = '1.0';
            document.getElementById('gearValue').innerHTML = '1';
            document.getElementById('fuelValue').innerHTML = '100';
        }
        
        // Game loop
        function gameLoop() {
            updatePhysics();
            updateGame();
            drawGame();
            requestAnimationFrame(gameLoop);
        }
        
        gameLoop();
        
        // Spawn initial obstacles
        setInterval(() => {
            if (gameRunning && obstacles.length < 3) {
                spawnObstacle();
            }
        }, 3000);
    </script>
</body>
</html>
"""

# Display game
with main_col:
    st.components.v1.html(game_html, height=750, scrolling=False)
    
    # Touch controls for mobile
    st.markdown("---")
    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns(5)
    with col_t1:
        if st.button("⬅️ LEFT", use_container_width=True):
            st.markdown('<script>document.dispatchEvent(new KeyboardEvent("keydown", {key: "ArrowLeft"}));</script>', unsafe_allow_html=True)
    with col_t2:
        if st.button("⬆️ ACCEL", use_container_width=True):
            st.markdown('<script>document.dispatchEvent(new KeyboardEvent("keydown", {key: "ArrowUp"}));</script>', unsafe_allow_html=True)
    with col_t3:
        if st.button("⬇️ BRAKE", use_container_width=True):
            st.markdown('<script>document.dispatchEvent(new KeyboardEvent("keydown", {key: "ArrowDown"}));</script>', unsafe_allow_html=True)
    with col_t4:
        if st.button("➡️ RIGHT", use_container_width=True):
            st.markdown('<script>document.dispatchEvent(new KeyboardEvent("keydown", {key: "ArrowRight"}));</script>', unsafe_allow_html=True)
    with col_t5:
        if st.button("🔄 RESTART", use_container_width=True):
            st.markdown('<script>document.dispatchEvent(new KeyboardEvent("keydown", {key: "r"}));</script>', unsafe_allow_html=True)

with right_col:
    st.markdown("### 🚗 VEHICLE INFO")
    st.info("""
    **Engine:** V8 Turbo  
    **Horsepower:** 450 HP  
    **Drivetrain:** AWD  
    **0-100 km/h:** 4.2s  
    **Top Speed:** 220 km/h  
    """)
    
    st.markdown("---")
    st.markdown("### 🏞️ TRACK INFO")
    st.markdown("""
    **Location:** Jungle Bridge Highway  
    **Length:** ∞ Endless  
    **Difficulty:** Progressive  
    **Weather:** Dynamic  
    """)
    
    st.markdown("---")
    st.markdown("### 💡 PRO TIPS")
    st.markdown("""
    1. **Shift up at high RPM** for better acceleration
    2. **Use engine braking** by downshifting
    3. **Conserve fuel** for longer runs
    4. **Watch for obstacles** in your lane
    5. **Bridge sections** have better grip
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #ffd700; padding: 20px;'>
    <p>🏁 Premium Driving Experience | Realistic Physics | Full Manual Controls 🏁</p>
    <p style='font-size: 12px;'>Use keyboard for best experience | Gear up for maximum speed!</p>
</div>
""", unsafe_allow_html=True)
