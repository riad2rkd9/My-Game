import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="Epic Fighting Game",
    page_icon="🥊",
    layout="wide"
)

# Custom CSS for fighting game style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1a0000 0%, #2d0000 50%, #1a0000 100%);
    }
    .main-title {
        text-align: center;
        font-family: 'Press Start 2P', monospace;
        background: linear-gradient(135deg, #ff0000, #ff6600, #ffcc00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .vs-text {
        font-family: 'Press Start 2P', monospace;
        font-size: 2em;
        color: #ffcc00;
        text-align: center;
        text-shadow: 0 0 10px #ff0000;
    }
    .character-select {
        background: rgba(0,0,0,0.8);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border: 2px solid #ffcc00;
    }
    .health-bar-container {
        background: #330000;
        border-radius: 10px;
        height: 30px;
        overflow: hidden;
        margin: 5px 0;
    }
    .health-bar {
        height: 100%;
        transition: width 0.3s ease;
        background: linear-gradient(90deg, #00ff00, #ffff00, #ff0000);
    }
    .special-bar-container {
        background: #1a0033;
        border-radius: 10px;
        height: 15px;
        overflow: hidden;
        margin: 5px 0;
    }
    .special-bar {
        height: 100%;
        background: linear-gradient(90deg, #6600ff, #cc00ff);
        transition: width 0.3s ease;
    }
    .combo-text {
        font-family: 'Press Start 2P', monospace;
        color: #ff6600;
        text-align: center;
        font-size: 1.2em;
        text-shadow: 2px 2px 0px #000;
        animation: fadeOut 1s ease-out;
    }
    @keyframes fadeOut {
        0% { opacity: 1; transform: scale(1.5); }
        100% { opacity: 0; transform: scale(1); }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    .shake {
        animation: shake 0.3s ease-in-out;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ EPIC FIGHTING GAME ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title" style="font-size: 1em;">Street Fighter Style | Special Moves | Combos</div>', unsafe_allow_html=True)

# Character classes
CHARACTERS = {
    "Dragon Fist": {
        "health": 100,
        "damage": 12,
        "special": 25,
        "special_name": "DRAGON PUNCH 🔥",
        "color": "#ff4444",
        "icon": "🐉",
        "special_cost": 30
    },
    "Shadow Ninja": {
        "health": 90,
        "damage": 10,
        "special": 30,
        "special_name": "SHADOW STRIKE 🌑",
        "color": "#8844ff",
        "icon": "🥷",
        "special_cost": 25
    },
    "Thunder God": {
        "health": 110,
        "damage": 11,
        "special": 22,
        "special_name": "THUNDER BOLT ⚡",
        "color": "#ffaa00",
        "icon": "⚡",
        "special_cost": 35
    },
    "Ice Warrior": {
        "health": 95,
        "damage": 9,
        "special": 28,
        "special_name": "ICE FREEZE ❄️",
        "color": "#44aaff",
        "icon": "❄️",
        "special_cost": 28
    }
}

# Initialize session state
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'player_character' not in st.session_state:
    st.session_state.player_character = "Dragon Fist"
if 'opponent_character' not in st.session_state:
    st.session_state.opponent_character = "Shadow Ninja"
if 'player_health' not in st.session_state:
    st.session_state.player_health = 100
if 'opponent_health' not in st.session_state:
    st.session_state.opponent_health = 100
if 'player_special' not in st.session_state:
    st.session_state.player_special = 0
if 'opponent_special' not in st.session_state:
    st.session_state.opponent_special = 0
if 'combo' not in st.session_state:
    st.session_state.combo = 0
if 'last_damage' not in st.session_state:
    st.session_state.last_damage = 0
if 'round' not in st.session_state:
    st.session_state.round = 1
if 'player_wins' not in st.session_state:
    st.session_state.player_wins = 0
if 'opponent_wins' not in st.session_state:
    st.session_state.opponent_wins = 0

# Game HTML/JavaScript
fighting_game_html = """
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
            font-family: 'Press Start 2P', monospace;
            overflow: hidden;
        }
        
        .game-container {
            position: relative;
            width: 1200px;
            height: 600px;
            background: linear-gradient(180deg, #0a0a2a 0%, #1a0a0a 50%, #0a0505 100%);
            border: 3px solid #ffcc00;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(255,204,0,0.3);
        }
        
        canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        
        .hud {
            position: absolute;
            top: 20px;
            left: 0;
            right: 0;
            padding: 20px;
            z-index: 10;
            pointer-events: none;
        }
        
        .health-bars {
            display: flex;
            justify-content: space-between;
            gap: 100px;
            margin-bottom: 20px;
        }
        
        .health-panel {
            flex: 1;
            background: rgba(0,0,0,0.7);
            padding: 10px;
            border-radius: 10px;
            backdrop-filter: blur(5px);
        }
        
        .health-label {
            color: white;
            font-size: 14px;
            margin-bottom: 5px;
            font-family: monospace;
        }
        
        .health-bar-bg {
            background: #330000;
            border-radius: 10px;
            height: 30px;
            overflow: hidden;
        }
        
        .health-bar-fill {
            height: 100%;
            transition: width 0.2s ease;
            background: linear-gradient(90deg, #00ff00, #ffff00, #ff0000);
        }
        
        .special-bar-bg {
            background: #1a0033;
            border-radius: 10px;
            height: 12px;
            margin-top: 5px;
            overflow: hidden;
        }
        
        .special-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #6600ff, #cc00ff);
            transition: width 0.2s ease;
        }
        
        .combo-display {
            position: absolute;
            bottom: 100px;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #ff6600;
            text-shadow: 3px 3px 0 #000;
            pointer-events: none;
            z-index: 10;
            font-family: monospace;
            animation: comboPop 0.3s ease;
        }
        
        @keyframes comboPop {
            0% { transform: scale(0.5); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .damage-number {
            position: absolute;
            font-size: 24px;
            font-weight: bold;
            color: #ff0000;
            text-shadow: 2px 2px 0 #000;
            pointer-events: none;
            animation: floatUp 1s ease-out forwards;
            font-family: monospace;
            z-index: 20;
        }
        
        @keyframes floatUp {
            0% { opacity: 1; transform: translateY(0); }
            100% { opacity: 0; transform: translateY(-50px); }
        }
        
        .controls-info {
            position: absolute;
            bottom: 20px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: center;
            gap: 30px;
            background: rgba(0,0,0,0.8);
            padding: 10px;
            border-radius: 10px;
            font-size: 10px;
            color: #ccc;
            z-index: 10;
            pointer-events: none;
        }
        
        .control-key {
            background: #333;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
            color: #ffcc00;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <canvas id="gameCanvas"></canvas>
        
        <div class="hud">
            <div class="health-bars">
                <div class="health-panel">
                    <div class="health-label" id="playerName">PLAYER</div>
                    <div class="health-bar-bg">
                        <div class="health-bar-fill" id="playerHealthBar" style="width: 100%"></div>
                    </div>
                    <div class="special-bar-bg">
                        <div class="special-bar-fill" id="playerSpecialBar" style="width: 0%"></div>
                    </div>
                </div>
                <div class="health-panel">
                    <div class="health-label" id="opponentName">OPPONENT</div>
                    <div class="health-bar-bg">
                        <div class="health-bar-fill" id="opponentHealthBar" style="width: 100%"></div>
                    </div>
                    <div class="special-bar-bg">
                        <div class="special-bar-fill" id="opponentSpecialBar" style="width: 0%"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="controls-info">
            <div><span class="control-key">A</span> <span class="control-key">D</span> - Move</div>
            <div><span class="control-key">J</span> - Punch</div>
            <div><span class="control-key">K</span> - Kick</div>
            <div><span class="control-key">L</span> - Special Move</div>
            <div><span class="control-key">SPACE</span> - Block</div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        let canvasWidth = 1200;
        let canvasHeight = 600;
        canvas.width = canvasWidth;
        canvas.height = canvasHeight;
        
        // Game state
        let gameRunning = true;
        let playerHealth = 100;
        let opponentHealth = 100;
        let playerSpecial = 0;
        let opponentSpecial = 0;
        let combo = 0;
        let canAttack = true;
        let attackCooldown = 0;
        let blockActive = false;
        let blockDuration = 0;
        
        // Character positions
        let playerX = 200;
        let opponentX = 900;
        let playerY = 400;
        let opponentY = 400;
        
        // Animation states
        let playerState = 'idle';
        let opponentState = 'idle';
        let animationTimer = 0;
        let hitEffect = { active: false, x: 0, y: 0 };
        
        // Damage numbers
        let damageNumbers = [];
        
        // Visual effects
        let particles = [];
        
        class Particle {
            constructor(x, y, color) {
                this.x = x;
                this.y = y;
                this.vx = (Math.random() - 0.5) * 5;
                this.vy = (Math.random() - 0.5) * 5 - 3;
                this.life = 1;
                this.color = color;
            }
            
            update() {
                this.x += this.vx;
                this.y += this.vy;
                this.life -= 0.02;
            }
            
            draw() {
                ctx.fillStyle = this.color;
                ctx.globalAlpha = this.life;
                ctx.fillRect(this.x, this.y, 4, 4);
                ctx.globalAlpha = 1;
            }
        }
        
        function drawCharacter(x, y, isPlayer, state) {
            // Body
            if (isPlayer) {
                ctx.fillStyle = '#ff4444';
            } else {
                ctx.fillStyle = '#8844ff';
            }
            
            // Body rectangle
            ctx.fillRect(x - 25, y - 60, 50, 80);
            
            // Head
            ctx.fillStyle = '#ffcc99';
            ctx.beginPath();
            ctx.arc(x, y - 75, 25, 0, Math.PI * 2);
            ctx.fill();
            
            // Eyes
            ctx.fillStyle = '#000';
            ctx.fillRect(x - 12, y - 82, 6, 6);
            ctx.fillRect(x + 6, y - 82, 6, 6);
            
            // Fighting stance based on state
            if (state === 'punch' && isPlayer) {
                ctx.fillStyle = '#ff6666';
                ctx.fillRect(x + 20, y - 50, 30, 15);
            } else if (state === 'kick' && isPlayer) {
                ctx.fillStyle = '#ff6666';
                ctx.fillRect(x + 25, y - 30, 35, 15);
            } else if (state === 'special' && isPlayer) {
                ctx.fillStyle = '#ffaa00';
                ctx.beginPath();
                ctx.arc(x + 40, y - 60, 25, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Bandana/headband
            ctx.fillStyle = '#ff0000';
            ctx.fillRect(x - 28, y - 85, 56, 8);
            
            // Gloves
            ctx.fillStyle = '#cc6633';
            ctx.fillRect(x - 30, y - 45, 15, 20);
            ctx.fillRect(x + 15, y - 45, 15, 20);
        }
        
        function drawBackground() {
            // Ground
            ctx.fillStyle = '#2a1a0a';
            ctx.fillRect(0, canvasHeight - 100, canvasWidth, 100);
            
            // Stadium lights
            for (let i = 0; i < 10; i++) {
                ctx.fillStyle = `rgba(255, 200, 100, ${0.3 + Math.sin(Date.now() / 1000 + i) * 0.1})`;
                ctx.fillRect(100 + i * 110, 50, 10, 30);
            }
            
            // Audience silhouettes
            ctx.fillStyle = '#1a1a1a';
            for (let i = 0; i < 20; i++) {
                ctx.fillRect(50 + i * 55, canvasHeight - 120, 30, 50);
            }
            
            // VS text
            ctx.font = 'bold 48px "Press Start 2P"';
            ctx.fillStyle = 'rgba(255, 204, 0, 0.3)';
            ctx.textAlign = 'center';
            ctx.fillText('VS', canvasWidth/2, canvasHeight/2 - 50);
        }
        
        function updateUI() {
            document.getElementById('playerHealthBar').style.width = `${playerHealth}%`;
            document.getElementById('opponentHealthBar').style.width = `${opponentHealth}%`;
            document.getElementById('playerSpecialBar').style.width = `${playerSpecial}%`;
            document.getElementById('opponentSpecialBar').style.width = `${opponentSpecial}%`;
        }
        
        function addDamageNumber(x, y, damage, isPlayer) {
            damageNumbers.push({
                x: x,
                y: y,
                damage: damage,
                isPlayer: isPlayer,
                life: 1
            });
        }
        
        function dealDamage(target, damage, isSpecial = false) {
            if (target === 'player') {
                playerHealth = Math.max(0, playerHealth - damage);
                addDamageNumber(opponentX, opponentY - 50, damage, true);
                
                // Add hit particles
                for (let i = 0; i < 10; i++) {
                    particles.push(new Particle(opponentX, opponentY - 40, '#ff0000'));
                }
                
                if (isSpecial) {
                    opponentSpecial = Math.min(100, opponentSpecial + 5);
                }
            } else {
                let finalDamage = damage;
                if (blockActive && target === 'opponent') {
                    finalDamage = Math.floor(damage * 0.3);
                    addDamageNumber(opponentX, opponentY - 50, finalDamage, false);
                } else {
                    opponentHealth = Math.max(0, opponentHealth - finalDamage);
                    addDamageNumber(opponentX, opponentY - 50, finalDamage, false);
                    
                    // Increase combo and special gauge
                    combo++;
                    playerSpecial = Math.min(100, playerSpecial + (isSpecial ? 0 : 10));
                    
                    // Add hit particles
                    for (let i = 0; i < 10; i++) {
                        particles.push(new Particle(opponentX, opponentY - 40, '#ff6600'));
                    }
                }
                
                if (isSpecial) {
                    playerSpecial = Math.max(0, playerSpecial - 30);
                }
            }
            
            updateUI();
            
            // Check for KO
            if (playerHealth <= 0 || opponentHealth <= 0) {
                gameRunning = false;
                setTimeout(() => {
                    if (window.parent && window.parent.postMessage) {
                        window.parent.postMessage({
                            type: 'gameover',
                            winner: playerHealth <= 0 ? 'opponent' : 'player'
                        }, '*');
                    }
                }, 100);
            }
        }
        
        function attack(attackType) {
            if (!gameRunning) return false;
            if (!canAttack) return false;
            
            let damage = 0;
            let isSpecial = false;
            
            switch(attackType) {
                case 'punch':
                    damage = 8 + Math.floor(combo / 5);
                    playerState = 'punch';
                    break;
                case 'kick':
                    damage = 12 + Math.floor(combo / 5);
                    playerState = 'kick';
                    break;
                case 'special':
                    if (playerSpecial >= 30) {
                        damage = 25 + combo;
                        isSpecial = true;
                        playerState = 'special';
                    } else {
                        return false;
                    }
                    break;
            }
            
            dealDamage('opponent', damage, isSpecial);
            canAttack = false;
            attackCooldown = 20;
            
            // Reset combo after 1 second
            setTimeout(() => {
                if (combo > 0) combo = 0;
            }, 2000);
            
            return true;
        }
        
        function opponentAI() {
            if (!gameRunning) return;
            if (Math.random() < 0.02) {
                let attackType = Math.random();
                if (attackType < 0.6) {
                    opponentState = 'punch';
                    let damage = 8;
                    dealDamage('player', damage);
                } else if (attackType < 0.9 && opponentSpecial >= 30) {
                    opponentState = 'special';
                    let damage = 22;
                    dealDamage('player', damage, true);
                    opponentSpecial = Math.max(0, opponentSpecial - 30);
                }
                
                setTimeout(() => {
                    opponentState = 'idle';
                }, 200);
            }
        }
        
        function update() {
            if (attackCooldown > 0) {
                attackCooldown--;
                if (attackCooldown === 0) canAttack = true;
            }
            
            if (blockDuration > 0) {
                blockDuration--;
                if (blockDuration === 0) blockActive = false;
            }
            
            // Update animations
            if (playerState !== 'idle') {
                animationTimer++;
                if (animationTimer > 10) {
                    playerState = 'idle';
                    animationTimer = 0;
                }
            }
            
            if (opponentState !== 'idle') {
                animationTimer++;
                if (animationTimer > 10) {
                    opponentState = 'idle';
                    animationTimer = 0;
                }
            }
            
            // Update particles
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                if (particles[i].life <= 0) {
                    particles.splice(i, 1);
                    i--;
                }
            }
            
            // Update damage numbers
            for (let i = 0; i < damageNumbers.length; i++) {
                damageNumbers[i].life -= 0.02;
                damageNumbers[i].y -= 1;
                if (damageNumbers[i].life <= 0) {
                    damageNumbers.splice(i, 1);
                    i--;
                }
            }
            
            opponentAI();
        }
        
        function draw() {
            drawBackground();
            
            // Draw characters
            drawCharacter(playerX, playerY, true, playerState);
            drawCharacter(opponentX, opponentY, false, opponentState);
            
            // Draw particles
            for (let p of particles) {
                p.draw();
            }
            
            // Draw damage numbers
            for (let dn of damageNumbers) {
                ctx.font = 'bold 24px monospace';
                ctx.fillStyle = dn.isPlayer ? '#ff4444' : '#ffaa44';
                ctx.globalAlpha = dn.life;
                ctx.fillText(dn.damage, dn.x, dn.y);
                ctx.globalAlpha = 1;
            }
            
            // Draw combo counter
            if (combo > 1) {
                ctx.font = 'bold 32px "Press Start 2P"';
                ctx.fillStyle = '#ff6600';
                ctx.textAlign = 'center';
                ctx.shadowBlur = 5;
                ctx.shadowColor = '#000';
                ctx.fillText(`${combo} HIT COMBO!`, canvasWidth/2, 150);
                ctx.shadowBlur = 0;
            }
            
            // Draw block indicator
            if (blockActive) {
                ctx.font = 'bold 20px monospace';
                ctx.fillStyle = '#44aaff';
                ctx.fillText('BLOCKING', playerX - 30, playerY - 100);
            }
            
            // Game over text
            if (!gameRunning) {
                ctx.font = 'bold 48px "Press Start 2P"';
                ctx.fillStyle = '#ffcc00';
                ctx.textAlign = 'center';
                ctx.fillText('FIGHT!', canvasWidth/2, canvasHeight/2);
            }
        }
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            const key = e.key.toLowerCase();
            
            if (key === 'j') {
                attack('punch');
                e.preventDefault();
            } else if (key === 'k') {
                attack('kick');
                e.preventDefault();
            } else if (key === 'l') {
                attack('special');
                e.preventDefault();
            } else if (key === ' ') {
                blockActive = true;
                blockDuration = 30;
                e.preventDefault();
            } else if (key === 'a') {
                playerX = Math.max(100, playerX - 20);
                e.preventDefault();
            } else if (key === 'd') {
                playerX = Math.min(500, playerX + 20);
                e.preventDefault();
            }
        });
        
        // Game loop
        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }
        
        gameLoop();
        
        // Set character names
        const playerName = window.parent.playerName || 'PLAYER';
        const opponentName = window.parent.opponentName || 'OPPONENT';
        document.getElementById('playerName').innerHTML = playerName;
        document.getElementById('opponentName').innerHTML = opponentName;
    </script>
</body>
</html>
"""

# Character selection interface
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("### 🎮 SELECT YOUR FIGHTER")
    player_char = st.selectbox(
        "Choose your character:",
        list(CHARACTERS.keys()),
        format_func=lambda x: f"{CHARACTERS[x]['icon']} {x}"
    )
    
    if player_char:
        st.markdown(f"""
        <div class="character-select">
            <h3>{CHARACTERS[player_char]['icon']} {player_char}</h3>
            <p>❤️ Health: {CHARACTERS[player_char]['health']}</p>
            <p>👊 Damage: {CHARACTERS[player_char]['damage']}</p>
            <p>⚡ Special: {CHARACTERS[player_char]['special']}</p>
            <p>✨ Special Move: {CHARACTERS[player_char]['special_name']}</p>
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown("### 👾 SELECT OPPONENT")
    opponent_char = st.selectbox(
        "Choose opponent:",
        list(CHARACTERS.keys()),
        index=1,
        format_func=lambda x: f"{CHARACTERS[x]['icon']} {x}"
    )
    
    if opponent_char:
        st.markdown(f"""
        <div class="character-select">
            <h3>{CHARACTERS[opponent_char]['icon']} {opponent_char}</h3>
            <p>❤️ Health: {CHARACTERS[opponent_char]['health']}</p>
            <p>👊 Damage: {CHARACTERS[opponent_char]['damage']}</p>
            <p>⚡ Special: {CHARACTERS[opponent_char]['special']}</p>
            <p>✨ Special Move: {CHARACTERS[opponent_char]['special_name']}</p>
        </div>
        """, unsafe_allow_html=True)

# Game controls and start button
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown('<div class="vs-text">VS</div>', unsafe_allow_html=True)
    
    if st.button("🥊 START FIGHT!", use_container_width=True):
        st.session_state.game_active = True
        st.session_state.player_character = player_char
        st.session_state.opponent_character = opponent_char
        st.session_state.player_health = CHARACTERS[player_char]['health']
        st.session_state.opponent_health = CHARACTERS[opponent_char]['health']
        st.session_state.player_special = 0
        st.session_state.opponent_special = 0
        st.rerun()

# Display game when active
if st.session_state.game_active:
    st.markdown("---")
    
    # Game stats display
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        st.metric("❤️ PLAYER HEALTH", f"{st.session_state.player_health}%")
    with col_stats2:
        st.metric("⚡ SPECIAL GAUGE", f"{st.session_state.player_special}%")
    with col_stats3:
        st.metric("🎯 COMBO", "0")
    
    # Embed the game
    st.components.v1.html(fighting_game_html, height=650, scrolling=False)
    
    # Control buttons for mobile
    st.markdown("### 🎮 MOBILE CONTROLS")
    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)
    
    with col_btn1:
        if st.button("👊 PUNCH", use_container_width=True):
            st.markdown('<script>document.dispatchEvent(new KeyboardEvent("keydown", {key: "j"}));</script>', unsafe_allow_html=True)
    with col_btn2:
        if st.button("🦶 KICK", use_container_width=True):
            st.markdown('<script>document.dispatchEvent(new KeyboardEvent("keydown", {key: "k"}));</script>', unsafe_allow_html=True)
    with col_btn3:
        if st.button("⚡ SPECIAL", use_container_width=True):
            st.markdown('<script>document.dispatchEvent(new KeyboardEvent("keydown", {key: "l"}));</script>', unsafe_allow_html=True)
    with col_btn4:
        if st.button("🛡️ BLOCK", use_container_width=True):
            st.markdown('<script>document.dispatchEvent(new KeyboardEvent("keydown", {key: " "}));</script>', unsafe_allow_html=True)
    with col_btn5:
        if st.button("⬅️ ➡️ MOVE", use_container_width=True):
            st.info("Use A/D keys or on-screen buttons")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #ffcc00; padding: 20px;'>
    <p>🥊 Special Moves | Combo System | Blocking | AI Opponent 🥊</p>
    <p style='font-size: 12px;'>Master the controls, build your combo, unleash special moves!</p>
</div>
""", unsafe_allow_html=True)
