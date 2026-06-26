import streamlit as st
import random
import json
import time

st.set_page_config(
    page_title="Street Racer",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Inline CSS + JS game engine ──────────────────────────────────────────────
GAME_HTML = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: #0a0a0f;
    font-family: 'Rajdhani', sans-serif;
    color: #e0e0e0;
    overflow: hidden;
  }

  #game-root {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 10px;
    background: radial-gradient(ellipse at top, #12121f 0%, #0a0a0f 100%);
  }

  /* ─── HUD ─────────────────────────────────────── */
  #hud {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 380px;
    padding: 8px 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,200,0,0.15);
    border-radius: 10px 10px 0 0;
    font-family: 'Orbitron', monospace;
    font-size: 11px;
    color: #aaa;
    letter-spacing: 0.05em;
  }

  .hud-val {
    font-size: 18px;
    font-weight: 700;
    color: #ffe033;
    display: block;
    line-height: 1.1;
  }

  .hud-val.speed-val { color: #33eeff; }
  .hud-val.lives-val { color: #ff4466; font-size: 16px; }

  /* ─── Canvas ──────────────────────────────────── */
  #gc {
    display: block;
    width: 380px;
    height: 560px;
    border-left: 1px solid rgba(255,200,0,0.12);
    border-right: 1px solid rgba(255,200,0,0.12);
    image-rendering: pixelated;
  }

  /* ─── Controls bar ────────────────────────────── */
  #controls {
    width: 380px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,200,0,0.15);
    border-radius: 0 0 10px 10px;
    padding: 10px 14px 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .btn-row {
    display: flex;
    gap: 8px;
    justify-content: center;
  }

  .ctrl-btn {
    width: 56px;
    height: 44px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 8px;
    color: #ddd;
    font-size: 20px;
    cursor: pointer;
    transition: background 0.1s, transform 0.08s;
    user-select: none;
    -webkit-user-select: none;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .ctrl-btn:active,
  .ctrl-btn.pressed {
    background: rgba(255,220,0,0.18);
    border-color: rgba(255,220,0,0.5);
    transform: scale(0.93);
  }

  .ctrl-btn.wide { width: 120px; }

  /* ─── Overlay screens ─────────────────────────── */
  #overlay {
    position: absolute;
    width: 380px;
    height: 560px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 18px;
    background: rgba(0,0,0,0.82);
    pointer-events: none;
  }

  #overlay.hidden { display: none; }

  .ov-title {
    font-family: 'Orbitron', monospace;
    font-size: 28px;
    font-weight: 900;
    color: #ffe033;
    text-shadow: 0 0 24px rgba(255,220,0,0.6);
    text-align: center;
    line-height: 1.2;
  }

  .ov-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: 14px;
    color: #aaa;
    text-align: center;
    line-height: 1.5;
  }

  .ov-score {
    font-family: 'Orbitron', monospace;
    font-size: 20px;
    color: #33eeff;
  }

  .ov-btn {
    pointer-events: all;
    padding: 12px 36px;
    background: #ffe033;
    color: #0a0a0f;
    border: none;
    border-radius: 8px;
    font-family: 'Orbitron', monospace;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    letter-spacing: 0.08em;
    transition: background 0.15s, transform 0.1s;
  }

  .ov-btn:hover { background: #ffd000; transform: scale(1.04); }

  #canvas-wrap {
    position: relative;
    width: 380px;
    height: 560px;
  }

  /* mobile hint */
  #key-hint {
    font-family: 'Rajdhani', sans-serif;
    font-size: 11px;
    color: #555;
    text-align: center;
    margin-top: 4px;
  }
</style>

<div id="game-root">
  <div id="hud">
    <div>
      <span>SCORE</span>
      <span class="hud-val" id="h-score">0</span>
    </div>
    <div style="text-align:center">
      <span>SPEED</span>
      <span class="hud-val speed-val" id="h-speed">0</span>
    </div>
    <div>
      <span>BEST</span>
      <span class="hud-val" id="h-best">0</span>
    </div>
    <div style="text-align:right">
      <span>LIVES</span>
      <span class="hud-val lives-val" id="h-lives">❤️❤️❤️</span>
    </div>
  </div>

  <div id="canvas-wrap">
    <canvas id="gc" width="380" height="560"></canvas>
    <div id="overlay">
      <div class="ov-title" id="ov-title">STREET<br>RACER</div>
      <div class="ov-sub" id="ov-sub">Dodge traffic · Collect coins<br>Survive as long as you can!</div>
      <div class="ov-score hidden" id="ov-score"></div>
      <button class="ov-btn" id="ov-btn" onclick="startGame()">START RACE</button>
    </div>
  </div>

  <div id="controls">
    <div class="btn-row">
      <button class="ctrl-btn" id="btn-up" ontouchstart="keys.ArrowUp=true" ontouchend="keys.ArrowUp=false">⬆️</button>
    </div>
    <div class="btn-row">
      <button class="ctrl-btn" id="btn-left" ontouchstart="keys.ArrowLeft=true" ontouchend="keys.ArrowLeft=false">⬅️</button>
      <button class="ctrl-btn wide" id="btn-brake" ontouchstart="keys.Space=true" ontouchend="keys.Space=false">🛑 BRAKE</button>
      <button class="ctrl-btn" id="btn-right" ontouchstart="keys.ArrowRight=true" ontouchend="keys.ArrowRight=false">➡️</button>
    </div>
    <div class="btn-row">
      <button class="ctrl-btn" id="btn-down" ontouchstart="keys.ArrowDown=true" ontouchend="keys.ArrowDown=false">⬇️</button>
    </div>
  </div>
  <div id="key-hint">Keyboard: ← → accelerate · ↑↓ change lane · SPACE brake</div>
</div>

<script>
// ═══════════════════════════════════════════════════════════
//  STREET RACER — Dr Driving 2 inspired
// ═══════════════════════════════════════════════════════════

const canvas = document.getElementById('gc');
const ctx    = canvas.getContext('2d');
const W = 380, H = 560;

// ── palette ──────────────────────────────────────────────
const PAL = {
  road:      '#1c1c22',
  roadLine:  '#3a3a42',
  lane:      '#2a2a32',
  kerb1:     '#cc2222',
  kerb2:     '#eeeeee',
  grass:     '#1a3020',
  dashLine:  '#d4b800',
  coin:      '#ffe033',
  coinGlow:  '#ffec80',
  shadow:    'rgba(0,0,0,0.35)',
};

// ── road geometry ─────────────────────────────────────────
const ROAD_LEFT  = 60;
const ROAD_RIGHT = 320;
const ROAD_W     = ROAD_RIGHT - ROAD_LEFT;
const NUM_LANES  = 4;
const LANE_W     = ROAD_W / NUM_LANES;
const LANE_CENTERS = Array.from({length: NUM_LANES}, (_, i) =>
  ROAD_LEFT + LANE_W * i + LANE_W / 2
);

// ── game state ────────────────────────────────────────────
let state = 'menu';       // menu | playing | dead | gameover
let score, best, lives;
let gameSpeed, frameCount, combo;
let playerX, playerY, playerVX, playerTargetLane, playerLane;
let particles;
let trafficCars, coins, roadMarks;
let invincible, invincibleTimer;
let shakeTimer;
let animId;

// ── keyboard ──────────────────────────────────────────────
const keys = {};
document.addEventListener('keydown', e => { keys[e.code] = true;  e.preventDefault(); });
document.addEventListener('keyup',   e => { keys[e.code] = false; });

// ── car shapes (pixel art via path) ──────────────────────
function drawCar(cx, cy, w, h, bodyColor, topColor, isPlayer) {
  const hw = w/2, hh = h/2;
  ctx.save();
  ctx.translate(cx, cy);

  // shadow
  ctx.fillStyle = PAL.shadow;
  ctx.beginPath();
  ctx.ellipse(2, hh+4, hw*0.9, 5, 0, 0, Math.PI*2);
  ctx.fill();

  // body
  ctx.fillStyle = bodyColor;
  ctx.beginPath();
  ctx.roundRect(-hw, -hh, w, h, [4, 4, 6, 6]);
  ctx.fill();

  // roof / cabin
  ctx.fillStyle = topColor;
  ctx.beginPath();
  ctx.roundRect(-hw*0.62, -hh+h*0.18, w*0.62, h*0.38, 4);
  ctx.fill();

  // windshields
  ctx.fillStyle = isPlayer ? '#b8f0ff' : '#aaccdd';
  ctx.globalAlpha = 0.85;
  ctx.beginPath();
  ctx.roundRect(-hw*0.55, -hh+h*0.2, w*0.5, h*0.16, 2);
  ctx.fill();
  ctx.beginPath();
  ctx.roundRect(-hw*0.55, -hh+h*0.5, w*0.5, h*0.14, 2);
  ctx.fill();
  ctx.globalAlpha = 1;

  // wheels
  const wy = [-hh+h*0.12, hh-h*0.12];
  const wx = [-hw-2, hw-4];
  ctx.fillStyle = '#111';
  for (const wyi of wy) for (const wxi of wx) {
    ctx.beginPath();
    ctx.roundRect(wxi, wyi, 7, 11, 2);
    ctx.fill();
  }

  // headlights / taillights
  if (isPlayer) {
    // headlights (top)
    ctx.fillStyle = '#fff9cc';
    ctx.shadowColor = '#fff5aa';
    ctx.shadowBlur = 6;
    ctx.beginPath(); ctx.ellipse(-hw*0.5, -hh+3, 4, 2.5, 0, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse( hw*0.5-2, -hh+3, 4, 2.5, 0, 0, Math.PI*2); ctx.fill();
    ctx.shadowBlur = 0;
    // taillights (bottom)
    ctx.fillStyle = '#ff2244';
    ctx.shadowColor = '#ff2244';
    ctx.shadowBlur = keys.Space ? 10 : 3;
    ctx.beginPath(); ctx.ellipse(-hw*0.5, hh-3, 4, 2.5, 0, 0, Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse( hw*0.5-2, hh-3, 4, 2.5, 0, 0, Math.PI*2); ctx.fill();
    ctx.shadowBlur = 0;
  }

  ctx.restore();
}

// ── traffic car palette ───────────────────────────────────
const TRAFFIC_COLORS = [
  ['#e03030','#8b1a1a'], ['#3070e0','#1a3a8b'],
  ['#30b060','#1a6030'], ['#c0c030','#707010'],
  ['#c06020','#7a3010'], ['#9030c0','#4a1070'],
  ['#e0e0e0','#aaaaaa'], ['#202040','#101020'],
];

// ── road marks (white dashes scrolling down) ──────────────
function initRoadMarks() {
  roadMarks = [];
  for (let i = 0; i < 12; i++) {
    roadMarks.push({ y: i * 60 });
  }
}

// ── spawn a traffic car ───────────────────────────────────
function spawnTraffic() {
  const lane = Math.floor(Math.random() * NUM_LANES);
  const cx = LANE_CENTERS[lane];
  const pal = TRAFFIC_COLORS[Math.floor(Math.random() * TRAFFIC_COLORS.length)];
  const relSpeed = (Math.random() * 0.4 + 0.5); // 0.5–0.9× game speed
  trafficCars.push({
    x: cx, y: -60,
    lane,
    w: 32, h: 54,
    body: pal[0], top: pal[1],
    relSpeed,
    alive: true,
  });
}

// ── spawn a coin ──────────────────────────────────────────
function spawnCoin() {
  const lane = Math.floor(Math.random() * NUM_LANES);
  coins.push({ x: LANE_CENTERS[lane], y: -20, r: 9, alive: true });
}

// ── particle system ───────────────────────────────────────
function spawnParticles(x, y, color, n=10) {
  for (let i = 0; i < n; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = Math.random() * 4 + 1;
    particles.push({
      x, y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      life: 1, decay: Math.random() * 0.03 + 0.025,
      r: Math.random() * 4 + 2,
      color,
    });
  }
}

// ── reset / start ─────────────────────────────────────────
function startGame() {
  score      = 0;
  lives      = 3;
  gameSpeed  = 3.5;
  frameCount = 0;
  combo      = 0;

  playerLane       = 1;
  playerTargetLane = 1;
  playerX          = LANE_CENTERS[playerLane];
  playerY          = H - 90;
  playerVX         = 0;

  trafficCars = [];
  coins       = [];
  particles   = [];
  invincible  = false;
  invincibleTimer = 0;
  shakeTimer  = 0;

  initRoadMarks();

  document.getElementById('overlay').classList.add('hidden');
  state = 'playing';

  updateHUD();
  if (animId) cancelAnimationFrame(animId);
  loop();
}

function showMenu(isGameOver) {
  state = isGameOver ? 'gameover' : 'menu';
  const ov   = document.getElementById('overlay');
  const title = document.getElementById('ov-title');
  const sub   = document.getElementById('ov-sub');
  const sc    = document.getElementById('ov-score');
  const btn   = document.getElementById('ov-btn');

  ov.classList.remove('hidden');

  if (isGameOver) {
    title.textContent = 'GAME OVER';
    sub.textContent   = 'You ran out of lives!';
    sc.textContent    = `Score: ${score}  |  Best: ${best}`;
    sc.classList.remove('hidden');
    btn.textContent   = 'TRY AGAIN';
  } else {
    title.innerHTML   = 'STREET<br>RACER';
    sub.innerHTML     = 'Dodge traffic · Collect coins<br>Survive as long as you can!';
    sc.classList.add('hidden');
    btn.textContent   = 'START RACE';
  }
}

// ── draw road ─────────────────────────────────────────────
function drawRoad(scroll) {
  // grass
  ctx.fillStyle = PAL.grass;
  ctx.fillRect(0, 0, W, H);

  // road surface
  ctx.fillStyle = PAL.road;
  ctx.fillRect(ROAD_LEFT, 0, ROAD_W, H);

  // kerb stripes
  const KERB = 6;
  const stripeH = 24;
  const numStripes = Math.ceil(H / stripeH) + 2;
  for (let i = 0; i < numStripes; i++) {
    const ky = (i * stripeH - (scroll % stripeH));
    ctx.fillStyle = (i % 2 === 0) ? PAL.kerb1 : PAL.kerb2;
    ctx.fillRect(ROAD_LEFT - KERB, ky, KERB, stripeH);
    ctx.fillRect(ROAD_RIGHT,       ky, KERB, stripeH);
  }

  // lane dividers (dashed)
  for (let l = 1; l < NUM_LANES; l++) {
    const lx = ROAD_LEFT + LANE_W * l;
    ctx.setLineDash([28, 20]);
    ctx.strokeStyle = PAL.dashLine;
    ctx.globalAlpha = 0.35;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(lx, -28 + (scroll % 48));
    ctx.lineTo(lx, H + 28);
    ctx.stroke();
  }
  ctx.setLineDash([]);
  ctx.globalAlpha = 1;
}

// ── draw coins ────────────────────────────────────────────
function drawCoins(t) {
  for (const c of coins) {
    if (!c.alive) continue;
    const pulse = 0.85 + 0.15 * Math.sin(t * 0.12 + c.x);
    ctx.save();
    ctx.translate(c.x, c.y);
    ctx.scale(pulse, pulse);
    // glow
    ctx.shadowColor = PAL.coinGlow;
    ctx.shadowBlur  = 12;
    ctx.fillStyle   = PAL.coin;
    ctx.beginPath();
    ctx.arc(0, 0, c.r, 0, Math.PI * 2);
    ctx.fill();
    // inner shine
    ctx.fillStyle = '#fff9cc';
    ctx.globalAlpha = 0.5;
    ctx.beginPath();
    ctx.arc(-2, -2, c.r * 0.4, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 1;
    ctx.shadowBlur = 0;
    // $ symbol
    ctx.fillStyle = '#8a6000';
    ctx.font = 'bold 9px Rajdhani, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('$', 0, 0);
    ctx.restore();
  }
}

// ── draw particles ────────────────────────────────────────
function drawParticles() {
  for (const p of particles) {
    ctx.globalAlpha = p.life;
    ctx.fillStyle = p.color;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r * p.life, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
}

// ── speed trails ──────────────────────────────────────────
let trailPoints = [];
function drawSpeedTrails() {
  if (gameSpeed < 6) return;
  ctx.save();
  ctx.strokeStyle = 'rgba(100,220,255,0.18)';
  ctx.lineWidth = 2;
  for (let i = 0; i < 5; i++) {
    const tx = ROAD_LEFT + Math.random() * ROAD_W;
    const ty = Math.random() * H;
    const len = gameSpeed * 4;
    ctx.beginPath();
    ctx.moveTo(tx, ty);
    ctx.lineTo(tx, ty + len);
    ctx.stroke();
  }
  ctx.restore();
}

// ── HUD update ────────────────────────────────────────────
function updateHUD() {
  document.getElementById('h-score').textContent = score;
  document.getElementById('h-speed').textContent = Math.round(gameSpeed * 30);
  document.getElementById('h-best').textContent  = best || 0;
  const livesStr = '❤️'.repeat(Math.max(0, lives)) + '🖤'.repeat(Math.max(0, 3 - lives));
  document.getElementById('h-lives').textContent = livesStr;
}

// ── collision (AABB) ──────────────────────────────────────
function collides(ax, ay, aw, ah, bx, by, bw, bh) {
  return Math.abs(ax - bx) < (aw + bw) / 2 &&
         Math.abs(ay - by) < (ah + bh) / 2;
}

// ── main loop ─────────────────────────────────────────────
let scroll = 0;
let frameT = 0;

function loop() {
  animId = requestAnimationFrame(loop);
  frameT++;
  if (state !== 'playing') return;

  frameCount++;
  gameSpeed = Math.min(3.5 + frameCount * 0.0012, 11);
  scroll   += gameSpeed;

  // ── input ──
  const brake = keys.Space || keys.KeyS;
  const accel = !brake;

  if ((keys.ArrowLeft  || keys.KeyA) && playerLane > 0) {
    playerTargetLane = Math.max(playerLane - 1, 0);
    playerLane = playerTargetLane;
  }
  if ((keys.ArrowRight || keys.KeyD) && playerLane < NUM_LANES - 1) {
    playerTargetLane = Math.min(playerLane + 1, NUM_LANES - 1);
    playerLane = playerTargetLane;
  }

  const targetX = LANE_CENTERS[playerTargetLane];
  playerX += (targetX - playerX) * 0.18;

  // vertical movement (relative to road)
  if (keys.ArrowUp && playerY > H * 0.35)    playerY -= 2.2;
  if (keys.ArrowDown && playerY < H - 60)    playerY += 2.2;

  // ── spawn ──
  const spawnRate = Math.max(55 - Math.floor(gameSpeed * 4), 22);
  if (frameCount % spawnRate === 0) spawnTraffic();
  if (frameCount % 90 === 0)        spawnCoin();

  // ── update traffic ──
  for (const car of trafficCars) {
    car.y += gameSpeed * car.relSpeed;
    if (car.y > H + 80) car.alive = false;

    if (!invincible && car.alive &&
        collides(playerX, playerY, 28, 50, car.x, car.y, car.w-4, car.h-6)) {
      // collision!
      car.alive = false;
      lives--;
      invincible = true;
      invincibleTimer = 120;
      shakeTimer = 18;
      spawnParticles(playerX, playerY, '#ff4466', 18);
      spawnParticles(car.x, car.y, '#ff8833', 12);
      combo = 0;
      updateHUD();
      if (lives <= 0) {
        if (!best || score > best) best = score;
        showMenu(true);
        return;
      }
    }
  }
  trafficCars = trafficCars.filter(c => c.alive);

  // ── update coins ──
  for (const c of coins) {
    c.y += gameSpeed;
    if (c.y > H + 20) c.alive = false;
    if (c.alive && Math.hypot(playerX - c.x, playerY - c.y) < c.r + 16) {
      c.alive = false;
      combo++;
      const gain = 10 * (combo >= 5 ? 2 : 1);
      score += gain;
      spawnParticles(c.x, c.y, PAL.coinGlow, 8);
    }
  }
  coins = coins.filter(c => c.alive);

  // survival score
  if (frameCount % 20 === 0) {
    score += 1;
    updateHUD();
  }

  // ── invincible timer ──
  if (invincible) {
    invincibleTimer--;
    if (invincibleTimer <= 0) invincible = false;
  }

  // ── particles ──
  for (const p of particles) {
    p.x += p.vx; p.y += p.vy;
    p.vx *= 0.92; p.vy *= 0.92;
    p.life -= p.decay;
  }
  particles = particles.filter(p => p.life > 0);

  // ── shake ──
  if (shakeTimer > 0) shakeTimer--;
  const sx = shakeTimer > 0 ? (Math.random()-0.5)*8 : 0;
  const sy = shakeTimer > 0 ? (Math.random()-0.5)*8 : 0;

  // ── draw ──
  ctx.save();
  ctx.translate(sx, sy);

  drawRoad(scroll);
  drawSpeedTrails();

  // coins behind cars
  drawCoins(frameT);

  // traffic cars
  for (const car of trafficCars) {
    drawCar(car.x, car.y, car.w, car.h, car.body, car.top, false);
  }

  // player (blink when invincible)
  const showPlayer = !invincible || (invincibleTimer % 10 < 6);
  if (showPlayer) {
    drawCar(playerX, playerY, 32, 54, '#ffe033', '#c8920a', true);
  }

  drawParticles();

  // speed blur vignette
  if (gameSpeed > 7) {
    const alpha = Math.min((gameSpeed - 7) / 4, 0.4);
    const grad = ctx.createRadialGradient(W/2, H/2, H*0.3, W/2, H/2, H*0.7);
    grad.addColorStop(0, 'rgba(0,0,0,0)');
    grad.addColorStop(1, `rgba(0,20,40,${alpha})`);
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);
  }

  ctx.restore();

  // speed ticker on HUD every 30 frames
  if (frameCount % 30 === 0) {
    document.getElementById('h-speed').textContent = Math.round(gameSpeed * 30);
    document.getElementById('h-score').textContent = score;
  }
}

// ── init ──────────────────────────────────────────────────
best = 0;
showMenu(false);
loop();

// btn highlight helpers (desktop touch)
['btn-up','btn-down','btn-left','btn-right','btn-brake'].forEach(id => {
  const el = document.getElementById(id);
  const map = {
    'btn-up':'ArrowUp','btn-down':'ArrowDown',
    'btn-left':'ArrowLeft','btn-right':'ArrowRight',
    'btn-brake':'Space'
  };
  el.addEventListener('mousedown',  () => { keys[map[id]] = true;  el.classList.add('pressed'); });
  el.addEventListener('mouseup',    () => { keys[map[id]] = false; el.classList.remove('pressed'); });
  el.addEventListener('mouseleave', () => { keys[map[id]] = false; el.classList.remove('pressed'); });
});
</script>
"""

# ─── Page layout ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Remove default Streamlit padding */
section.main > div { padding-top: 0 !important; padding-bottom: 0 !important; }
header { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
body { background: #0a0a0f !important; }
.stApp { background: #0a0a0f !important; }
</style>
""", unsafe_allow_html=True)

st.components.v1.html(GAME_HTML, height=720, scrolling=False)
