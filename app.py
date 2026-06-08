import streamlit as st
import json

# Page configuration
st.set_page_config(
    page_title="Epic Fighting Game",
    page_icon="🥊",
    layout="wide"
)

# Custom CSS for arcade look and feel
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
        font-size: 2.5em;
        color: #ffcc00;
        text-align: center;
        text-shadow: 0 0 10px #ff0000;
        margin-top: 15px;
    }
    .character-select {
        background: rgba(0,0,0,0.8);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 2px solid #ffcc00;
        color: white;
        font-family: monospace;
    }
    .character-select h3 {
        color: #ffcc00;
        font-family: 'Press Start 2P', monospace;
        font-size: 14px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ EPIC FIGHTING GAME ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title" style="font-size: 0.9em;">Arcade Engine | Dynamic Combos | AI Scaling</div>', unsafe_allow_html=True)

# Character Roster
CHARACTERS = {
    "Dragon Fist": {
        "health": 100,
        "damage": 12,
        "special_name": "DRAGON PUNCH 🔥",
        "color": "#ff4444",
        "icon": "🐉",
    },
    "Shadow Ninja": {
        "health": 90,
        "damage": 10,
        "special_name": "SHADOW STRIKE 🌑",
        "color": "#8844ff",
        "icon": "🥷",
    },
    "Thunder God": {
        "health": 120,
        "damage": 11,
        "special_name": "THUNDER BOLT ⚡",
        "color": "#ffaa00",
        "icon": "⚡",
    },
    "Ice Warrior": {
        "health": 105,
        "damage": 9,
        "special_name": "ICE FREEZE ❄️",
        "color": "#44aaff",
        "icon": "❄️",
    }
}

# Setup state management 
if 'game_active' not in st.session_state:
    st.session_state.game_active = False

# Character Selection Layout
col1, space, col3 = st.columns([2, 1, 2])

with col1:
    st.markdown("### 🎮 PLAYER 1")
    player_char = st.selectbox(
        "Choose your character:",
        list(CHARACTERS.keys()),
        key="p1_select",
        format_func=lambda x: f"{CHARACTERS[x]['icon']} {x}"
    )
    p_data = CHARACTERS[player_char]
    st.markdown(f"""
    <div class="character-select">
        <h3>{p_data['icon']} {player_char.upper()}</h3>
        <p>❤️ HP Pool: <b>{p_data['health']}</b></p>
        <p>👊 Base DMG: <b>{p_data['damage']}</b></p>
        <p>✨ Ultimate: <span style="color:{p_data['color']}">{p_data['special_name']}</span></p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("### 👾 CPU OPPONENT")
    opponent_char = st.selectbox(
        "Choose opponent:",
        list(CHARACTERS.keys()),
        index=1,
        key="cpu_select",
        format_func=lambda x: f"{CHARACTERS[x]['icon']} {x}"
    )
    o_data = CHARACTERS[opponent_char]
    st.markdown(f"""
    <div class="character-select">
        <h3>{o_data['icon']} {opponent_char.upper()}</h3>
        <p>❤️ HP Pool: <b>{o_data['health']}</b></p>
        <p>👊 Base DMG: <b>{o_data['damage']}</b></p>
        <p>✨ Ultimate: <span style="color:{o_data['color']}">{o_data['special_name']}</span></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="vs-text">VS</div>', unsafe_allow_html=True)

# Start / Reset Match Control
if st.button("🥊 INITIALIZE MATCH", use_container_width=True, type="primary"):
    st.session_state.game_active = True

# Inject configuration data safely into our interactive iframe game application
if st.session_state.game_active:
    game_config = {
        "player": {"name": player_char, **CHARACTERS[player_char]},
        "opponent": {"name": opponent_char, **CHARACTERS[opponent_char]}
    }
    
    # Injecting complete game logic inside an iframe container
    fighting_game_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; user-select: none; }}
            body {{
                background: #111;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                font-family: 'Press Start 2P', monospace;
                color: #fff;
                padding: 10px;
            }}
            .game-container {{
                position: relative;
                width: 1000px;
                height: 500px;
                background: linear-gradient(180deg, #0e1111 0%, #1c1d21 70%, #2a2c31 100%);
                border: 4px solid #ffcc00;
                border-radius: 10px;
                overflow: hidden;
            }}
            canvas {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
            }}
            .hud {{
                position: absolute;
                top: 15px;
                left: 15px;
                right: 15px;
                display: flex;
                justify-content: space-between;
                gap: 40px;
                z-index: 10;
                pointer-events: none;
            }}
            .hud-panel {{
                flex: 1;
                background: rgba(0, 0, 0, 0.75);
                padding: 12px;
                border-radius: 6px;
                border: 1px solid #444;
            }}
            .name-label {{ font-size: 11px; margin-bottom: 6px; color: #fff; letter-spacing: 1px; }}
            .bar-bg {{ background: #331111; height: 20px; border-radius: 3px; overflow: hidden; border: 1px solid #000; }}
            .hp-fill {{ height: 100%; background: #00ff66; width: 100%; transition: width 0.1s linear; }}
            .sp-bg {{ background: #111133; height: 10px; margin-top: 5px; border-radius: 2px; overflow: hidden; }}
            .sp-fill {{ height: 100%; background: #9900ff; width: 0%; transition: width 0.1s ease; }}
            .on-screen-controls {{
                margin-top: 15px;
                display: flex;
                gap: 15px;
                justify-content: center;
                width: 1000px;
            }}
            .btn {{
                background: #222;
                border: 2px solid #ffcc00;
                color: #ffcc00;
                font-family: 'Press Start 2P', monospace;
                padding: 12px 20px;
                font-size: 11px;
                cursor: pointer;
                border-radius: 5px;
                transition: transform 0.1s;
            }}
            .btn:active {{ transform: scale(0.95); background: #ffcc00; color: #000; }}
            .keyboard-guide {{
                margin-top: 10px;
                font-size: 9px;
                color: #888;
                text-align: center;
            }}
        </style>
    </head>
    <body>

        <div class="game-container">
            <div class="hud">
                <div class="hud-panel">
                    <div class="name-label" id="p1-name">PLAYER 1</div>
                    <div class="bar-bg"><div class="hp-fill" id="p1-hp"></div></div>
                    <div class="sp-bg"><div class="sp-fill" id="p1-sp"></div></div>
                </div>
                <div class="hud-panel" style="text-align: right;">
                    <div class="name-label" id="p2-name">CPU OPPONENT</div>
                    <div class="bar-bg"><div class="hp-fill" id="p2-hp" style="float: right;"></div></div>
                    <div class="sp-bg"><div class="sp-fill" id="p2-sp" style="float: right;"></div></div>
                </div>
            </div>
            <canvas id="stage"></canvas>
        </div>

        <div class="on-screen-controls">
            <button class="btn" onclick="triggerAction('left')">⬅️ LEFT (A)</button>
            <button class="btn" onclick="triggerAction('right')">➡️ RIGHT (D)</button>
            <button class="btn" onclick="triggerAction('punch')">👊 PUNCH (J)</button>
            <button class="btn" onclick="triggerAction('kick')">🦶 KICK (K)</button>
            <button class="btn" onclick="triggerAction('special')">⚡ ULTIMATE (L)</button>
        </div>
        <div class="keyboard-guide">Desktop players can click inside the window and use their physical keyboard directly!</div>

        <script>
            const config = {json.dumps(game_config)};
            
            const canvas = document.getElementById('stage');
            const ctx = canvas.getContext('2d');
            canvas.width = 1000;
            canvas.height = 500;

            // Initialize Combatant Statuses
            let p1 = {{
                x: 250, y: 400,
                maxHp: config.player.health, hp: config.player.health,
                sp: 0, dmg: config.player.damage,
                color: config.player.color, name: config.player.name,
                state: 'idle', stateTimer: 0, direction: 1
            }};

            let p2 = {{
                x: 750, y: 400,
                maxHp: config.opponent.health, hp: config.opponent.health,
                sp: 0, dmg: config.opponent.damage,
                color: config.opponent.color, name: config.opponent.name,
                state: 'idle', stateTimer: 0, direction: -1
            }};

            let particles = [];
            let combatTexts = [];
            let comboCount = 0;
            let comboTimer = 0;
            let matchOver = false;
            let winnerText = "";

            // Set up HUD elements
            document.getElementById('p1-name').innerText = p1.name.toUpperCase();
            document.getElementById('p2-name').innerText = p2.name.toUpperCase();

            function spawnParticles(x, y, color, count=8) {{
                for(let i=0; i<count; i++) {{
                    particles.push({{
                        x: x, y: y,
                        vx: (Math.random() - 0.5) * 8,
                        vy: (Math.random() - 0.5) * 8 - 2,
                        alpha: 1,
                        color: color,
                        size: Math.random() * 4 + 2
                    }});
                }}
            }}

            function spawnText(x, y, text, color="#ff0000") {{
                combatTexts.push({{ x, y, text, color, alpha: 1, vy: -2 }});
            }}

            function executeAttack(attacker, defender, type) {{
                if (matchOver || attacker.state !== 'idle') return;

                attacker.state = type;
                attacker.stateTimer = 12; // animation frame length

                // Standard range threshold checks
                let distance = Math.abs(attacker.x - defender.x);
                let hitRange = type === 'kick' ? 110 : 80;
                let calculatedDmg = Math.floor(attacker.dmg * (type === 'kick' ? 1.2 : 0.85));
                
                if (type === 'special') {{
                    if (attacker.sp < 100) {{
                        spawnText(attacker.x, attacker.y - 80, "NO GAUGE!", "#ffaa00");
                        attacker.state = 'idle';
                        return;
                    }}
                    hitRange = 300; // Far-reaching blast wave range
                    calculatedDmg = attacker.dmg * 2.5;
                    attacker.sp = 0;
                }}

                if (distance <= hitRange) {{
                    // Target Hit registered
                    defender.hp = Math.max(0, defender.hp - calculatedDmg);
                    attacker.sp = Math.min(100, attacker.sp + 15);
                    defender.sp = Math.min(100, defender.sp + 10);
                    
                    if (attacker === p1) {{
                        comboCount++;
                        comboTimer = 90;
                    }}

                    spawnParticles(defender.x, defender.y - 40, attacker.color, 12);
                    spawnText(defender.x, defender.y - 80, `-${{calculatedDmg}}`, "#ff3333");
                    
                    if (type === 'special') {{
                        spawnText(defender.x, defender.y - 120, "💥 CRITICAL!", "#ffcc00");
                    }}
                }} else {{
                    // Whiffed attack
                    if (type === 'special') {{
                         // Even if it misses up close, energy wave travels forward
                         spawnParticles(attacker.x + (attacker.direction * 150), attacker.y - 40, attacker.color, 6);
                    }}
                }}
            }}

            // Interface bridging both mobile buttons and standard keyboard loops cleanly
            function triggerAction(action) {{
                if (matchOver) return;
                if (action === 'left') p1.x = Math.max(50, p1.x - 35);
                if (action === 'right') p1.x = Math.min(p2.x - 40, p1.x + 35);
                if (action === 'punch') executeAttack(p1, p2, 'punch');
                if (action === 'kick') executeAttack(p1, p2, 'kick');
                if (action === 'special') executeAttack(p1, p2, 'special');
            }}

            window.addEventListener('keydown', (e) => {{
                const key = e.key.toLowerCase();
                if (key === 'a') triggerAction('left');
                if (key === 'd') triggerAction('right');
                if (key === 'j') triggerAction('punch');
                if (key === 'k') triggerAction('kick');
                if (key === 'l') triggerAction('special');
            }});

            // Simple Dynamic AI Loop 
            function runAI() {{
                if (matchOver || p2.state !== 'idle') return;

                let distance = Math.abs(p2.x - p1.x);

                if (p2.sp >= 100) {{
                    executeAttack(p2, p1, 'special');
                }} else if (distance > 80) {{
                    // Advance towards target position
                    p2.x -= 2.5; 
                }} else {{
                    // Random combat action calculation
                    let choice = Math.random();
                    if (choice < 0.07) executeAttack(p2, p1, 'punch');
                    else if (choice < 0.12) executeAttack(p2, p1, 'kick');
                }}
            }}

            function checkWinConditions() {{
                if (matchOver) return;
                if (p1.hp <= 0) {{
                    matchOver = true;
                    winnerText = `${{p2.name.toUpperCase()}} WINS`;
                }} else if (p2.hp <= 0) {{
                    matchOver = true;
                    winnerText = `${{p1.name.toUpperCase()}} WINS`;
                }}
            }}

            function update() {{
                // Advance timers
                if (p1.stateTimer > 0) {{ p1.stateTimer--; if(p1.stateTimer===0) p1.state = 'idle'; }}
                if (p2.stateTimer > 0) {{ p2.stateTimer--; if(p2.stateTimer===0) p2.state = 'idle'; }}
                
                if (comboTimer > 0) {{
                    comboTimer--;
                    if (comboTimer === 0) comboCount = 0;
                }}

                runAI();
                checkWinConditions();

                // Physics Engine Simulation for particle arrays
                particles.forEach((p, idx) => {{
                    p.x += p.vx;
                    p.y += p.vy;
                    p.alpha -= 0.02;
                    if(p.alpha <= 0) particles.splice(idx, 1);
                }});

                // Text UI array cleanups
                combatTexts.forEach((t, idx) => {{
                    t.y += t.vy;
                    t.alpha -= 0.02;
                    if(t.alpha <= 0) combatTexts.splice(idx, 1);
                }});

                // Dynamic UI updates for health and special meters
                document.getElementById('p1-hp').style.width = `${{(p1.hp / p1.maxHp) * 100}}%`;
                document.getElementById('p2-hp').style.width = `${{(p2.hp / p2.maxHp) * 100}}%`;
                document.getElementById('p1-sp').style.width = `${{p1.sp}}%`;
                document.getElementById('p2-sp').style.width = `${{p2.sp}}%`;
            }}

            function drawFighter(fighter) {{
                ctx.save();
                ctx.translate(fighter.x, fighter.y);

                // Body rendering logic
                ctx.fillStyle = fighter.color;
                ctx.fillRect(-25, -75, 50, 75);

                // Head drawing logic
                ctx.fillStyle = "#ffccaa";
                ctx.beginPath();
                ctx.arc(0, -90, 20, 0, Math.PI * 2);
                ctx.fill();

                // Eyes positioning 
                ctx.fillStyle = "#000";
                let eyeOffset = fighter.direction * 7;
                ctx.fillRect(eyeOffset - 2, -94, 4, 4);

                // Fighting Stance Animations Display
                ctx.fillStyle = "#fff";
                if (fighter.state === 'punch') {{
                    ctx.fillRect(fighter.direction * 25, -60, 35, 12);
                }} else if (fighter.state === 'kick') {{
                    ctx.fillRect(fighter.direction * 25, -35, 45, 14);
                }} else if (fighter.state === 'special') {{
                    ctx.fillStyle = "#ff00ff";
                    ctx.beginPath();
                    ctx.arc(fighter.direction * 45, -55, 25, 0, Math.PI*2);
                    ctx.fill();
                }}

                ctx.restore();
            }}

            function render() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Stage Floor Rendering
                ctx.fillStyle = "#442222";
                ctx.fillRect(0, 400, canvas.width, 100);
                ctx.fillStyle = "#221111";
                ctx.fillRect(0, 400, canvas.width, 8);

                // Core entities processing
                p1.direction = p1.x < p2.x ? 1 : -1;
                p2.direction = p2.x < p1.x ? 1 : -1;

                drawFighter(p1);
                drawFighter(p2);

                // Draw standard particle effects
                particles.forEach(p => {{
                    ctx.save();
                    ctx.globalAlpha = p.alpha;
                    ctx.fillStyle = p.color;
                    ctx.fillRect(p.x, p.y, p.size, p.size);
                    ctx.restore();
                }});

                // Dynamic Damage HUD tracking overhead
                combatTexts.forEach(t => {{
                    ctx.save();
                    ctx.globalAlpha = t.alpha;
                    ctx.font = 'bold 14px "Press Start 2P"';
                    ctx.fillStyle = t.color;
                    ctx.fillText(t.text, t.x - 20, t.y);
                    ctx.restore();
                }});

                // Global Combo Text Tracker
                if (comboCount > 1) {{
                    ctx.font = '24px "Press Start 2P"';
                    ctx.fillStyle = '#ffcc00';
                    ctx.fillText(`${{comboCount}} HIT COMBO`, 380, 160);
                }}

                // Game Over Display Banner
                if (matchOver) {{
                    ctx.fillStyle = "rgba(0,0,0,0.6)";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);

                    ctx.font = '36px "Press Start 2P"';
                    ctx.fillStyle = '#ff0000';
                    ctx.textAlign = "center";
                    ctx.fillText(winnerText, canvas.width/2, canvas.height/2);
                    
                    ctx.font = '14px "Press Start 2P"';
                    ctx.fillStyle = '#ffffff';
                    ctx.fillText("CLICK 'INITIALIZE MATCH' ABOVE TO REMATCH", canvas.width/2, canvas.height/2 + 50);
                }}
            }}

            function mainLoop() {{
                update();
                render();
                requestAnimationFrame(mainLoop);
            }}

            // Start Game Loop Engine
            mainLoop();
        </script>
    </body>
    </html>
    """
    
    # Render Canvas inside unified framework
    st.components.v1.html(fighting_game_html, height=580, scrolling=False)

# Game Manual Footer Details
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #ffcc00; font-family: monospace; font-size: 13px;'>
    <p>⚡ <b>Combat Guide:</b> Landing simple punches/kicks builds up your deep-purple <b>Ultimate Energy Bar</b>.</p>
    <p>🔥 Once it hits 100%, trigger your character's explicit ultimate move for devastating un-blockable damage bursts!</p>
</div>
""", unsafe_allow_html=True)
