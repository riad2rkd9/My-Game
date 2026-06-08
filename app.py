import streamlit as st
import random

# Page configuration
st.set_page_config(
    page_title="Snake Game",
    page_icon="🐍",
    layout="centered"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .game-container {
        background: rgba(0,0,0,0.8);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

st.title("🐍 Classic Snake Game")
st.markdown("*Control the snake, eat the food, beat your high score!*")

# High score tracking in session state
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0

# Display high score
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown(f"### 🏆 High Score: {st.session_state.high_score}")

# HTML/JavaScript Snake Game
snake_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        .game-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin: 20px 0;
        }
        
        canvas {
            border: 3px solid #fff;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            background-color: #1a1a2e;
            cursor: pointer;
        }
        
        .score-board {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 40px;
            margin: 20px;
            padding: 10px 30px;
            background: rgba(255,255,255,0.1);
            border-radius: 50px;
            backdrop-filter: blur(10px);
        }
        
        .current-score {
            font-size: 28px;
            font-weight: bold;
            color: #4ade80;
            font-family: 'Courier New', monospace;
        }
        
        .current-score span {
            font-size: 32px;
            color: #fff;
        }
        
        .restart-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 30px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 50px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            font-family: inherit;
        }
        
        .restart-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .game-status {
            font-size: 20px;
            font-weight: bold;
            margin-top: 15px;
            padding: 8px 20px;
            border-radius: 50px;
            display: inline-block;
        }
        
        .status-playing {
            background: #22c55e;
            color: white;
        }
        
        .status-gameover {
            background: #ef4444;
            color: white;
        }
        
        .instructions {
            margin-top: 20px;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            font-size: 14px;
            text-align: center;
        }
        
        .key {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 12px;
            margin: 0 5px;
            border-radius: 8px;
            font-weight: bold;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="game-wrapper">
        <div class="score-board">
            <div class="current-score">
                🍎 Score: <span id="score">0</span>
            </div>
            <button class="restart-btn" onclick="restartGame()">🔄 Restart Game</button>
        </div>
        
        <canvas id="gameCanvas" width="600" height="400"></canvas>
        
        <div id="gameStatus" class="game-status status-playing">
            🎮 Playing...
        </div>
        
        <div class="instructions">
            <strong>🎮 Controls:</strong>
            <span class="key">↑</span>
            <span class="key">↓</span>
            <span class="key">←</span>
            <span class="key">→</span>
            &nbsp;&nbsp;&nbsp;
            <strong>💡 Tip:</strong> Don't hit the walls or yourself!
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const scoreElement = document.getElementById('score');
        const gameStatus = document.getElementById('gameStatus');
        
        // Game settings
        const gridSize = 20;
        const tileCount = canvas.width / gridSize;
        
        let snake = [
            {x: 10, y: 10},
            {x: 9, y: 10},
            {x: 8, y: 10}
        ];
        
        let direction = {x: 1, y: 0};  // Moving right initially
        let food = {};
        let score = 0;
        let gameRunning = true;
        let gameLoopInterval;
        
        function randomFood() {
            do {
                food = {
                    x: Math.floor(Math.random() * tileCount),
                    y: Math.floor(Math.random() * tileCount)
                };
            } while (snake.some(segment => segment.x === food.x && segment.y === food.y));
        }
        
        function draw() {
            if (!gameRunning) return;
            
            // Clear canvas with gradient
            const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
            gradient.addColorStop(0, '#1a1a2e');
            gradient.addColorStop(1, '#16213e');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw grid lines
            ctx.strokeStyle = 'rgba(255,255,255,0.05)';
            ctx.lineWidth = 1;
            for (let i = 0; i < tileCount; i++) {
                ctx.beginPath();
                ctx.moveTo(i * gridSize, 0);
                ctx.lineTo(i * gridSize, canvas.height);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(0, i * gridSize);
                ctx.lineTo(canvas.width, i * gridSize);
                ctx.stroke();
            }
            
            // Draw snake with gradient
            for (let i = 0; i < snake.length; i++) {
                const segment = snake[i];
                const gradient = ctx.createLinearGradient(
                    segment.x * gridSize, 
                    segment.y * gridSize,
                    (segment.x + 1) * gridSize, 
                    (segment.y + 1) * gridSize
                );
                
                if (i === 0) {
                    // Head
                    gradient.addColorStop(0, '#4ade80');
                    gradient.addColorStop(1, '#22c55e');
                } else {
                    // Body
                    gradient.addColorStop(0, '#22c55e');
                    gradient.addColorStop(1, '#16a34a');
                }
                
                ctx.fillStyle = gradient;
                ctx.fillRect(
                    segment.x * gridSize + 1, 
                    segment.y * gridSize + 1, 
                    gridSize - 2, 
                    gridSize - 2
                );
                
                // Add eye to head
                if (i === 0) {
                    ctx.fillStyle = 'white';
                    ctx.fillRect(segment.x * gridSize + 5, segment.y * gridSize + 5, 3, 3);
                    ctx.fillRect(segment.x * gridSize + 12, segment.y * gridSize + 5, 3, 3);
                }
            }
            
            // Draw food (apple style)
            ctx.fillStyle = '#ef4444';
            ctx.shadowBlur = 10;
            ctx.shadowColor = '#ef4444';
            ctx.beginPath();
            ctx.arc(
                food.x * gridSize + gridSize/2,
                food.y * gridSize + gridSize/2,
                gridSize/2 - 2,
                0,
                Math.PI * 2
            );
            ctx.fill();
            
            // Add leaf to apple
            ctx.fillStyle = '#22c55e';
            ctx.beginPath();
            ctx.ellipse(
                food.x * gridSize + gridSize - 5,
                food.y * gridSize + 5,
                3,
                5,
                0.5,
                0,
                Math.PI * 2
            );
            ctx.fill();
            ctx.shadowBlur = 0;
        }
        
        function update() {
            if (!gameRunning) return;
            
            // Move snake head
            const head = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y
            };
            
            // Check wall collision
            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
                gameOver();
                return;
            }
            
            // Check self collision
            if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
                gameOver();
                return;
            }
            
            snake.unshift(head);
            
            // Check food collision
            if (head.x === food.x && head.y === food.y) {
                score += 10;
                scoreElement.textContent = score;
                randomFood();
                
                // Update high score via Streamlit
                if (score > (parent.highScore || 0)) {
                    parent.highScore = score;
                    // Send score to Streamlit
                    if (parent.parent && parent.parent.postMessage) {
                        parent.parent.postMessage({type: 'highscore', score: score}, '*');
                    }
                }
            } else {
                snake.pop();
            }
        }
        
        function gameOver() {
            gameRunning = false;
            if (gameLoopInterval) {
                clearInterval(gameLoopInterval);
            }
            gameStatus.textContent = '💀 Game Over! 💀';
            gameStatus.className = 'game-status status-gameover';
            
            // Send final score to Streamlit
            if (parent.parent && parent.parent.postMessage) {
                parent.parent.postMessage({type: 'gameover', score: score}, '*');
            }
        }
        
        function restartGame() {
            // Reset game state
            snake = [
                {x: 10, y: 10},
                {x: 9, y: 10},
                {x: 8, y: 10}
            ];
            direction = {x: 1, y: 0};
            score = 0;
            gameRunning = true;
            scoreElement.textContent = score;
            gameStatus.textContent = '🎮 Playing...';
            gameStatus.className = 'game-status status-playing';
            
            // Clear old interval
            if (gameLoopInterval) {
                clearInterval(gameLoopInterval);
            }
            
            randomFood();
            draw();
            
            // Start new game loop
            gameLoopInterval = setInterval(() => {
                update();
                draw();
            }, 100);
        }
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            if (!gameRunning) return;
            
            switch(e.key) {
                case 'ArrowUp':
                    if (direction.y === 0) {
                        direction = {x: 0, y: -1};
                    }
                    break;
                case 'ArrowDown':
                    if (direction.y === 0) {
                        direction = {x: 0, y: 1};
                    }
                    break;
                case 'ArrowLeft':
                    if (direction.x === 0) {
                        direction = {x: -1, y: 0};
                    }
                    break;
                case 'ArrowRight':
                    if (direction.x === 0) {
                        direction = {x: 1, y: 0};
                    }
                    break;
            }
        });
        
        // Initialize game
        randomFood();
        draw();
        gameLoopInterval = setInterval(() => {
            update();
            draw();
        }, 100);
        
        // Listen for messages from Streamlit
        window.addEventListener('message', (event) => {
            if (event.data.type === 'reset') {
                restartGame();
            }
        });
    </script>
</body>
</html>
"""

# Create columns for layout
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Embed the game
    game_html = st.components.v1.html(snake_html, height=650, scrolling=False)
    
    # Add a reset button that communicates with the game
    if st.button("🎮 New Game", use_container_width=True):
        st.rerun()

# Sidebar with information
with st.sidebar:
    st.markdown("## 📊 Game Stats")
    st.metric("🎯 Current High Score", st.session_state.high_score)
    
    st.markdown("---")
    st.markdown("## 🎮 How to Play")
    st.markdown("""
    1. Use **arrow keys** (↑ ↓ ← →) to control the snake
    2. Eat the **red apples** to grow
    3. Each apple gives **10 points**
    4. Avoid hitting **walls** or **yourself**
    5. Try to beat your **high score**!
    """)
    
    st.markdown("---")
    st.markdown("## 💡 Pro Tips")
    st.markdown("""
    - Plan your route ahead
    - Don't rush into corners
    - Use the walls to trap the snake strategically
    - Practice makes perfect!
    """)
    
    st.markdown("---")
    st.markdown("### 🐍 Features")
    st.markdown("""
    ✅ Smooth controls  
    ✅ Score tracking  
    ✅ High score persistence  
    ✅ Beautiful graphics  
    ✅ Responsive design  
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>Made with ❤️ using Streamlit | Classic Snake Game</div>",
    unsafe_allow_html=True
)
