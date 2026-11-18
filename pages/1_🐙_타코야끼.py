
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 타코야끼 게임 - 화면 높이 최적화 버전
# ==========================================

st.markdown("""
<style>
.block-container {
    max-width: 100% !important;
    padding: 0.3rem 0.6rem !important;
}
[data-testid="stAppViewContainer"] {
    background: #fff0d8;
}
iframe {
    border: 0 !important;
    display: block;
}
</style>
""", unsafe_allow_html=True)

components.html(r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1">

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    font-family: "Malgun Gothic", sans-serif;
    color: #70422b;
    overflow: hidden;
}

button {
    font: inherit;
    cursor: pointer;
}

/* ==========================================
   전체 게임 화면
========================================== */

.game {
    position: relative;
    width: 100%;
    height: 680px;
    padding: 9px 13px;
    border-radius: 16px;
    overflow: hidden;
    background: linear-gradient(
        180deg,
        #617ca5 0%,
        #e7a9a2 35%,
        #f8d9a6 72%,
        #bf865c 100%
    );
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    min-height: 45px;
}

.logo {
    padding: 8px 13px;
    background: #fff0ce;
    border: 3px solid #a85d37;
    border-radius: 13px;
    color: #974b31;
    font-size: 19px;
    font-weight: 900;
    white-space: nowrap;
}

.stats {
    display: flex;
    gap: 7px;
}

.stat {
    min-width: 76px;
    padding: 5px 9px;
    text-align: center;
    border: 2px solid #f6d6a0;
    border-radius: 12px;
    background: #784d3d;
    color: #fff9e9;
    font-size: 16px;
    font-weight: 900;
}

.stat small {
    display: block;
    font-size: 10px;
    color: #ffe2bd;
}

.stat.timer {
    background: #c8584c;
}

/* ==========================================
   타코야끼 간판
========================================== */

.sign {
    width: fit-content;
    margin: 5px auto 9px;
    padding: 6px 25px;
    background: #934a35;
    border: 3px solid #f2ca87;
    border-radius: 13px;
    box-shadow: 0 4px #683b29;
    color: #fff6dc;
    font-size: 18px;
    font-weight: 900;
}

/* ==========================================
   손님 3명
========================================== */

.customers {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    max-width: 1050px;
    margin: 0 auto 11px;
}

.customer {
    min-height: 110px;
    padding: 8px 5px;
    border: 3px solid #d59d69;
    border-radius: 17px;
    background: #fff4de;
    box-shadow: 0 4px #9c693f;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    gap: 3px;
}

.face {
    font-size: 28px;
    line-height: 1.1;
}

.customer strong {
    font-size: 12px;
}

.order {
    font-size: 12px;
    font-weight: 900;
    line-height: 1.4;
}

.patience {
    width: 92%;
    height: 9px;
    border-radius: 10px;
    background: #dfc29d;
    overflow: hidden;
}

.patience span {
    display: block;
    width: 100%;
    height: 100%;
    background: #70b963;
}

/* ==========================================
   조리대
========================================== */

.counter {
    max-width: 1200px;
    margin: 0 auto;
    padding: 9px;
    border: 5px solid #8e5334;
    border-radius: 20px;
    box-shadow: 0 6px #643b28;
    background: repeating-linear-gradient(
        0deg,
        #b87648 0 20px,
        #c88958 20px 40px
    );
}

.counter h3 {
    margin: 0 0 7px;
    color: #fff5de;
    text-align: center;
    font-size: 16px;
    text-shadow: 0 2px #73472e;
}

.kitchen {
    display: grid;
    grid-template-columns: minmax(0, 2fr) minmax(145px, .85fr);
    gap: 9px;
}

.grills {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 7px;
    padding: 7px;
    background: #44434a;
    border: 4px solid #302e34;
    border-radius: 15px;
}

.grill {
    min-height: 145px;
    padding: 6px 3px;
    border: 2px solid #686268;
    border-radius: 13px;
    background: #28282c;
    color: #fff5da;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 5px;
    text-align: center;
}

.grill strong {
    font-size: 12px;
    pointer-events: none;
}

.grill small {
    font-size: 10px;
    pointer-events: none;
}

.holes {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 3px;
    width: min(105px, 95%);
    pointer-events: none;
}

.ball {
    aspect-ratio: 1;
    border: 2px solid #111219;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: #15161a;
    font-size: 15px;
}

.ball.cooking {
    background: radial-gradient(
        circle at 25% 25%,
        #fff1b0,
        #d9ab65
    );
    animation: fry .8s infinite alternate;
}

.ball.ready {
    background: radial-gradient(
        circle at 25% 25%,
        #f8d27a,
        #ad692b
    );
}

.ball.burnt {
    background: #493024;
}

@keyframes fry {
    to {
        transform: scale(1.05);
    }
}

.bar {
    width: 80%;
    height: 7px;
    background: #151515;
    border-radius: 10px;
    overflow: hidden;
    pointer-events: none;
}

.bar span {
    display: block;
    width: 0%;
    height: 100%;
    background: #efc456;
}

.right {
    display: flex;
    flex-direction: column;
    gap: 7px;
}

.plate-zone, .trash {
    border: 3px solid #e5bd8f;
    border-radius: 13px;
    background: #fff1d9;
    text-align: center;
    padding: 6px;
}

.plate-zone {
    min-height: 112px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
}

.plate-zone strong {
    font-size: 12px;
}

.plate {
    width: 69px;
    height: 69px;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        white 0 48%,
        #b7d6e2 50% 60%,
        white 62%
    );
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 27px;
    font-weight: 900;
}

.plate small {
    font-size: 9px;
}

#plate-help {
    font-size: 10px;
}

.trash {
    min-height: 44px;
    font-size: 12px;
    font-weight: 900;
    display: grid;
    place-items: center;
    background: #f9d6c7;
}

/* ==========================================
   재료와 토핑
========================================== */

.supplies {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    max-width: 1200px;
    margin: 13px auto 7px;
}

.supply {
    padding: 8px;
    background: #fff1da;
    border: 3px solid #be8454;
    border-radius: 15px;
}

.supply h3 {
    margin: 0 0 6px;
    font-size: 13px;
}

.items {
    display: flex;
    gap: 6px;
}

.item {
    flex: 1;
    min-width: 0;
    padding: 6px 3px;
    border: 2px solid #e5c49a;
    border-radius: 11px;
    background: #fffaf1;
    text-align: center;
    font-size: 12px;
    font-weight: 900;
    line-height: 1.3;
}

.item span {
    display: block;
    font-size: 25px;
    margin-bottom: 2px;
}

.help {
    max-width: 1200px;
    margin: 0 auto;
    padding: 6px;
    background: #fff4da;
    border: 2px solid #d8ab75;
    border-radius: 10px;
    text-align: center;
    font-size: 12px;
    font-weight: 800;
}

/* ==========================================
   드래그 앤 드롭
========================================== */

[data-source] {
    cursor: grab;
    touch-action: none;
    user-select: none;
}

[data-source]:active {
    cursor: grabbing;
}

.dragging-original {
    opacity: .45;
}

.drop-over {
    outline: 4px solid #ffe47c;
    outline-offset: 2px;
    filter: brightness(1.08);
}

.ghost {
    position: fixed;
    z-index: 1000;
    pointer-events: none;
    min-width: 65px;
    padding: 9px;
    background: #fff8e7;
    border: 3px solid #d9a16b;
    border-radius: 14px;
    box-shadow: 0 5px 12px #0004;
    font-size: 28px;
    text-align: center;
}

.ghost small {
    display: block;
    font-size: 11px;
    font-weight: 900;
}

/* ==========================================
   알림 및 게임 시작 창
========================================== */

.toast {
    position: absolute;
    z-index: 30;
    left: 50%;
    bottom: 12px;
    transform: translateX(-50%);
    max-width: 90%;
    padding: 9px 20px;
    border-radius: 14px;
    background: #71432f;
    color: white;
    font-size: 13px;
    font-weight: 900;
    opacity: 0;
    pointer-events: none;
    transition: opacity .2s;
    text-align: center;
}

.toast.show {
    opacity: 1;
}

.overlay {
    position: absolute;
    z-index: 35;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #241b20b8;
    padding: 15px;
}

.overlay.hidden {
    display: none;
}

.start-panel {
    width: min(460px, 95%);
    padding: 32px 20px;
    background: #fff4d9;
    border: 6px solid #bc7950;
    border-radius: 25px;
    text-align: center;
    box-shadow: 0 10px #7c4d37;
}

.panel-icon {
    font-size: 60px;
}

.start-panel h2 {
    margin: 10px 0;
    color: #954a33;
    font-size: 26px;
}

.start-panel p {
    font-weight: 900;
    font-size: 15px;
    line-height: 1.8;
}

.start-button {
    margin-top: 10px;
    padding: 14px 25px;
    background: #e8734c;
    color: white;
    border: 0;
    border-radius: 15px;
    box-shadow: 0 5px #aa4c30;
    font-size: 20px;
    font-weight: 900;
}

.countdown {
    position: absolute;
    z-index: 40;
    inset: 0;
    display: none;
    align-items: center;
    justify-content: center;
    background: #2d1e29ba;
    color: #fff2bc;
    font-size: clamp(75px, 15vw, 150px);
    font-weight: 900;
    text-shadow: 0 8px #82432e;
}

.countdown.show {
    display: flex;
}

/* ==========================================
   작은 화면 대응
========================================== */

@media (max-width: 800px) {
    .game {
        padding: 7px;
    }

    .logo {
        font-size: 12px;
        padding: 6px;
    }

    .stats {
        gap: 3px;
    }

    .stat {
        min-width: 48px;
        font-size: 12px;
        padding: 4px;
    }

    .stat small {
        font-size: 8px;
    }

    .sign {
        font-size: 15px;
    }

    .customers {
        gap: 5px;
    }

    .customer {
        padding: 5px 2px;
    }

    .face {
        font-size: 23px;
    }

    .order {
        font-size: 10px;
    }

    .kitchen {
        grid-template-columns: minmax(0, 1.8fr) minmax(100px, .7fr);
        gap: 5px;
    }

    .grills {
        gap: 3px;
        padding: 4px;
    }

    .grill {
        padding: 3px 1px;
    }

    .ball {
        font-size: 11px;
        border-width: 1px;
    }

    .plate {
        width: 55px;
        height: 55px;
        font-size: 23px;
    }

    .supply {
        padding: 5px;
    }

    .supply h3 {
        font-size: 11px;
    }

    .item {
        font-size: 10px;
        padding: 5px 2px;
    }

    .item span {
        font-size: 20px;
    }
}
</style>
</head>

<body>

<div class="game">

    <div class="header">
        <div class="logo">
            🏮 와글와글 포장마차
        </div>

        <div class="stats">
            <div class="stat">
                <small>레벨</small>
                <span id="level">1</span>/5
            </div>
            <div class="stat timer">
                <small>남은 시간</small>
                <span id="time">90</span>초
            </div>
            <div class="stat">
                <small>목숨</small>
                <span id="lives">❤️❤️❤️</span>
            </div>
            <div class="stat">
                <small>점수</small>
                <span id="score">0</span>
            </div>
        </div>
    </div>

    <div class="sign">
        🐙 타코야끼 가게 🐙
    </div>

    <div class="customers" id="customers"></div>

    <div class="counter">
        <h3>🍳 타코야끼 조리대</h3>

        <div class="kitchen">
            <div class="grills" id="grills"></div>

            <div class="right">
                <div class="plate-zone" data-drop="plate">
                    <strong>🍽️ 완성 접시</strong>
                    <div class="plate" id="plate">🍽️</div>
                    <small id="plate-help">
                        익은 타코야끼를 올려 주세요
                    </small>
                </div>

                <div class="trash" data-drop="trash">
                    🗑️ 음식 버리기
                </div>
            </div>
        </div>
    </div>

    <div class="supplies">
        <div class="supply">
            <h3>🥣 속재료를 조리판으로 드래그</h3>
            <div class="items" id="fillings"></div>
        </div>

        <div class="supply">
            <h3>✨ 토핑을 완성 접시로 드래그</h3>
            <div class="items" id="toppings"></div>
        </div>
    </div>

    <div class="help">
        재료 → 조리판 → 완성 접시 → 토핑 → 손님 |
        필요 없는 음식은 휴지통에 버리세요!
    </div>

    <div class="toast" id="toast"></div>

    <div class="overlay" id="overlay">
        <div class="start-panel">
            <div class="panel-icon" id="panel-icon">🐙</div>
            <h2 id="panel-title">타코야끼 가게</h2>
            <p id="panel-description">
                주문에 맞춰 타코야끼를 완성하세요!<br>
                ❤️ 목숨 3개 · 총 5레벨<br>
                5레벨까지 살아남으면 승리합니다!
            </p>
            <button
                class="start-button"
                id="start-button"
                onclick="beginCountdown()">
                🎮 타코야끼 만들기
            </button>
        </div>
    </div>

    <div class="countdown" id="countdown">
        <span id="count-text">3</span>
    </div>
</div>

<script>
// ==========================================
// 기본 게임 설정
// ==========================================

const LEVEL_TIMES = [90, 120, 120, 150, 150];

const CUSTOMER_WAIT = [
    [40, 45],
    [30, 35],
    [22, 27],
    [15, 20],
    [10, 13]
];

const COOK_MS = 2700;
const BURN_MS = 6700;

const fillings = [
    {name: '문어', emoji: '🐙'},
    {name: '치즈', emoji: '🧀'},
    {name: '새우', emoji: '🦐'}
];

const toppings = [
    {name: '소스', emoji: '🍯'},
    {name: '마요네즈', emoji: '🥛'},
    {name: '가쓰오부시', emoji: '🍥'}
];

const faces = ['🐱', '🐰', '🐻', '🦊', '🐼', '🐸'];

const el = id => document.getElementById(id);
const now = () => performance.now();

const pick = arr =>
    arr[Math.floor(Math.random() * arr.length)];

let game = null;
let drag = null;
let highlighted = null;
let toastTimer = null;
let countdownActive = false;

// ==========================================
// 게임 시작 카운트다운
// ==========================================

async function beginCountdown() {
    if (countdownActive) return;

    countdownActive = true;

    el('overlay').classList.add('hidden');
    el('countdown').classList.add('show');

    for (const number of ['3', '2', '1']) {
        el('count-text').textContent = number;

        await new Promise(resolve =>
            setTimeout(resolve, 1000)
        );
    }

    el('count-text').textContent = 'START!';

    await new Promise(resolve =>
        setTimeout(resolve, 700)
    );

    el('countdown').classList.remove('show');
    countdownActive = false;

    startGame();
}

// ==========================================
// 새 손님
// ==========================================

function newCustomer() {
    const [min, max] = CUSTOMER_WAIT[game.level - 1];

    return {
        face: pick(faces),
        fill: pick(fillings),
        top: pick(toppings),
        born: now(),
        patience: (
            min + Math.random() * (max - min)
        ) * 1000
    };
}

// ==========================================
// 게임 시작
// ==========================================

function startGame() {
    game = {
        level: 1,
        levelStart: now(),
        lives: 3,
        score: 0,
        combo: 0,
        served: 0,
        missed: 0,
        plate: null,
        grills: [
            {state: 'empty'},
            {state: 'empty'},
            {state: 'empty'}
        ],
        customers: [],
        ended: false
    };

    game.customers = [
        newCustomer(),
        newCustomer(),
        newCustomer()
    ];

    renderAll();
    tell('영업 시작! 주문을 만들어 주세요!');
}

// ==========================================
// 알림
// ==========================================

function tell(message) {
    const box = el('toast');

    box.textContent = message;
    box.classList.add('show');

    clearTimeout(toastTimer);

    toastTimer = setTimeout(() => {
        box.classList.remove('show');
    }, 1700);
}

// ==========================================
// 상단 정보
// ==========================================

function updateHud() {
    if (!game) return;

    el('level').textContent = game.level;
    el('lives').textContent = '❤️'.repeat(game.lives);
    el('score').textContent = game.score;
}

// ==========================================
// 손님 표시
// ==========================================

function renderCustomers() {
    if (!game) {
        el('customers').innerHTML = '';
        return;
    }

    el('customers').innerHTML =
        game.customers.map((c, i) => `
        <div class="customer"
             data-drop="customer"
             data-index="${i}">

            <span class="face">${c.face}</span>

            <strong>손님 ${i + 1}</strong>

            <div class="order">
                ${c.fill.emoji} ${c.fill.name}
                +
                ${c.top.emoji} ${c.top.name}
            </div>

            <div class="patience">
                <span id="patience-${i}"></span>
            </div>
        </div>
        `).join('');
}

// ==========================================
// 조리판 표시
// ==========================================

function renderGrills() {
    if (!game) {
        el('grills').innerHTML = '';
        return;
    }

    const messages = {
        empty: '재료를 넣어 주세요',
        cooking: '조리 중...',
        ready: '다 익었어요!',
        burnt: '음식이 탔어요!'
    };

    el('grills').innerHTML =
        game.grills.map((g, i) => {

            let icon = '';

            if (g.state === 'cooking') icon = '🟡';
            if (g.state === 'ready') icon = '🟤';
            if (g.state === 'burnt') icon = '⚫';

            const source = (
                g.state === 'ready' ||
                g.state === 'burnt'
            )
                ? `data-source="grill"
                   data-index="${i}"
                   data-emoji="🐙"
                   data-label="타코야끼"`
                : '';

            return `
            <div class="grill"
                 data-drop="grill"
                 data-index="${i}"
                 ${source}>

                <div class="holes">
                    ${Array.from(
                        {length: 6},
                        () => `
                        <div class="ball ${g.state}">
                            ${icon}
                        </div>
                        `
                    ).join('')}
                </div>

                <strong>${i + 1}번 조리판</strong>

                <div class="bar">
                    <span id="cook-${i}"></span>
                </div>

                <small>${messages[g.state]}</small>
            </div>
            `;
        }).join('');
}

// ==========================================
// 접시 표시
// ==========================================

function renderPlate() {
    const plate = el('plate');

    if (!game || !game.plate) {
        plate.innerHTML = '🍽️';
        plate.removeAttribute('data-source');

        el('plate-help').textContent =
            '익은 타코야끼를 올려 주세요';

        return;
    }

    plate.innerHTML = `
        🍡
        <small>
            ${game.plate.fill.name}
            ${game.plate.top
                ? ' + ' + game.plate.top.name
                : ''}
        </small>
    `;

    plate.setAttribute('data-source', 'plate');
    plate.setAttribute('data-emoji', '🍡');
    plate.setAttribute('data-label', '완성 음식');

    el('plate-help').textContent =
        game.plate.top
            ? '손님에게 서빙하세요'
            : '토핑을 올려 주세요';
}

// ==========================================
// 재료 표시
// ==========================================

function renderSupplies() {
    el('fillings').innerHTML =
        fillings.map((f, i) => `
        <div class="item"
             data-source="filling"
             data-index="${i}"
             data-emoji="${f.emoji}"
             data-label="${f.name}">
            <span>${f.emoji}</span>
            ${f.name}
        </div>
        `).join('');

    el('toppings').innerHTML =
        toppings.map((t, i) => `
        <div class="item"
             data-source="topping"
             data-index="${i}"
             data-emoji="${t.emoji}"
             data-label="${t.name}">
            <span>${t.emoji}</span>
            ${t.name}
        </div>
        `).join('');
}

function renderAll() {
    updateHud();
    renderCustomers();
    renderGrills();
    renderPlate();
    renderSupplies();
}

// ==========================================
// 목숨 감소
// ==========================================

function loseLife(message) {
    if (!game || game.ended) return;

    game.lives--;
    game.combo = 0;

    updateHud();

    if (game.lives <= 0) {
        endGame(false);
    } else {
        tell(
            `${message} 남은 목숨 ${game.lives}개`
        );
    }
}

// ==========================================
// 주문 서빙
// ==========================================

function serveCustomer(index) {
    if (!game || game.ended) return;

    const customer = game.customers[index];
    const plate = game.plate;

    if (!plate || !plate.top) {
        tell('토핑까지 완성한 음식을 서빙하세요!');
        return;
    }

    const correct = (
        plate.fill.name === customer.fill.name &&
        plate.top.name === customer.top.name
    );

    game.plate = null;
    renderPlate();

    if (correct) {
        game.combo++;
        game.served++;

        game.score += 100 + Math.min(
            game.combo * 10,
            100
        );

        tell('주문 성공! +점수');

        game.customers[index] = newCustomer();
        renderCustomers();
        updateHud();
    } else {
        game.missed++;

        loseLife('주문이 틀렸어요!');

        if (!game.ended) {
            game.customers[index] = newCustomer();
            renderCustomers();
        }
    }
}

// ==========================================
// 드롭 동작 처리
// ==========================================

function handleDrop(kind, index, target, targetIndex) {
    if (!game || game.ended) return;

    // 속재료 -> 조리판
    if (kind === 'filling' && target === 'grill') {
        const grill = game.grills[targetIndex];

        if (grill.state !== 'empty') {
            tell('이미 사용 중인 조리판입니다!');
            return;
        }

        game.grills[targetIndex] = {
            state: 'cooking',
            fill: fillings[index],
            born: now()
        };

        renderGrills();
        return;
    }

    // 익은 음식 -> 접시
    if (kind === 'grill' && target === 'plate') {
        const grill = game.grills[index];

        if (grill.state !== 'ready') {
            tell('다 익은 음식만 접시에 담을 수 있어요!');
            return;
        }

        if (game.plate) {
            tell('접시가 이미 차 있습니다!');
            return;
        }

        game.plate = {
            fill: grill.fill,
            top: null
        };

        game.grills[index] = {state: 'empty'};

        renderGrills();
        renderPlate();
        return;
    }

    // 토핑 -> 접시
    if (kind === 'topping' && target === 'plate') {
        if (!game.plate) {
            tell('먼저 타코야끼를 접시에 담아 주세요!');
            return;
        }

        if (game.plate.top) {
            tell('이미 토핑이 올라가 있습니다!');
            return;
        }

        game.plate.top = toppings[index];

        renderPlate();
        return;
    }

    // 완성된 접시 -> 손님
    if (kind === 'plate' && target === 'customer') {
        serveCustomer(targetIndex);
        return;
    }

    // 음식 -> 휴지통
    if (target === 'trash') {
        if (kind === 'plate') {
            game.plate = null;
            renderPlate();
            tell('접시의 음식을 버렸습니다.');
            return;
        }

        if (kind === 'grill') {
            game.grills[index] = {
                state: 'empty'
            };

            renderGrills();
            tell('조리판을 비웠습니다.');
            return;
        }
    }

    tell('올바른 위치에 재료를 놓아 주세요!');
}

// ==========================================
// 드래그 앤 드롭
// ==========================================

function moveGhost(e) {
    if (!drag) return;

    drag.ghost.style.left =
        (e.clientX + 12) + 'px';

    drag.ghost.style.top =
        (e.clientY + 12) + 'px';

    const target = document.elementFromPoint(
        e.clientX,
        e.clientY
    )?.closest('[data-drop]');

    if (highlighted) {
        highlighted.classList.remove('drop-over');
    }

    highlighted = target;

    if (highlighted) {
        highlighted.classList.add('drop-over');
    }
}

document.addEventListener('pointerdown', e => {
    if (!game || game.ended || drag) return;

    const source = e.target.closest('[data-source]');

    if (!source) return;

    e.preventDefault();

    const ghost = document.createElement('div');
    ghost.className = 'ghost';

    ghost.innerHTML = `
        ${source.dataset.emoji || '🍡'}
        <small>
            ${source.dataset.label || ''}
        </small>
    `;

    document.body.appendChild(ghost);

    drag = {
        pointerId: e.pointerId,
        source,
        kind: source.dataset.source,
        index: Number(source.dataset.index || 0),
        ghost
    };

    source.classList.add('dragging-original');

    moveGhost(e);
});

document.addEventListener(
    'pointermove',
    e => {
        if (
            drag &&
            drag.pointerId === e.pointerId
        ) {
            e.preventDefault();
            moveGhost(e);
        }
    },
    {passive: false}
);

function releaseDrag(e) {
    if (!drag || drag.pointerId !== e.pointerId) {
        return;
    }

    const current = drag;

    const target = document.elementFromPoint(
        e.clientX,
        e.clientY
    )?.closest('[data-drop]');

    current.ghost.remove();

    if (current.source.isConnected) {
        current.source.classList.remove(
            'dragging-original'
        );
    }

    if (highlighted) {
        highlighted.classList.remove('drop-over');
    }

    highlighted = null;
    drag = null;

    if (target) {
        handleDrop(
            current.kind,
            current.index,
            target.dataset.drop,
            Number(target.dataset.index || 0)
        );
    }
}

document.addEventListener('pointerup', releaseDrag);

document.addEventListener('pointercancel', e => {
    if (!drag || drag.pointerId !== e.pointerId) {
        return;
    }

    drag.ghost.remove();

    if (drag.source.isConnected) {
        drag.source.classList.remove(
            'dragging-original'
        );
    }

    if (highlighted) {
        highlighted.classList.remove('drop-over');
    }

    highlighted = null;
    drag = null;
});

// ==========================================
// 레벨 전환
// ==========================================

function nextLevel() {
    if (game.level === 5) {
        endGame(true);
        return;
    }

    game.level++;
    game.levelStart = now();

    game.grills = [
        {state: 'empty'},
        {state: 'empty'},
        {state: 'empty'}
    ];

    game.plate = null;

    game.customers = [
        newCustomer(),
        newCustomer(),
        newCustomer()
    ];

    renderAll();

    tell(`LEVEL ${game.level} 시작!`);
}

// ==========================================
// 게임 종료
// ==========================================

function endGame(won) {
    if (!game || game.ended) return;

    game.ended = true;

    el('panel-icon').textContent =
        won ? '🏆' : '💔';

    el('panel-title').textContent =
        won ? '5레벨 클리어!' : '영업 종료!';

    el('panel-description').innerHTML = `
        최종 점수: ${game.score}점<br>
        성공한 주문: ${game.served}개<br>
        ${won
            ? '축하합니다! 모든 레벨을 통과했어요!'
            : '다시 도전해 보세요!'}
    `;

    el('start-button').textContent =
        '🔄 다시 도전하기';

    el('overlay').classList.remove('hidden');
}

// ==========================================
// 게임 타이머
// ==========================================

function tick() {
    if (!game || game.ended) return;

    const current = now();

    const elapsed =
        (current - game.levelStart) / 1000;

    const remaining = Math.max(
        0,
        LEVEL_TIMES[game.level - 1] - elapsed
    );

    el('time').textContent = Math.ceil(remaining);

    // 레벨 제한 시간이 끝나면 이동
    if (remaining <= 0) {
        nextLevel();
        return;
    }

    // 손님별 대기 시간 확인
    let customersChanged = false;

    for (let i = 0; i < game.customers.length; i++) {
        const customer = game.customers[i];

        const passed = current - customer.born;

        if (passed >= customer.patience) {
            game.missed++;

            loseLife('손님이 기다리다 떠났어요!');

            if (game.ended) return;

            game.customers[i] = newCustomer();

            customersChanged = true;
        }
    }

    if (customersChanged) {
        renderCustomers();
    }

    // 손님 기다림 게이지
    game.customers.forEach((customer, i) => {
        const passed = current - customer.born;

        const percent = Math.max(
            0,
            100 * (1 - passed / customer.patience)
        );

        const bar = el(`patience-${i}`);

        if (bar) {
            bar.style.width = percent + '%';

            bar.style.background =
                percent > 55
                    ? '#70b963'
                    : percent > 25
                        ? '#e8b64a'
                        : '#dc6753';
        }
    });

    // 조리판 상태 확인
    let grillsChanged = false;

    game.grills.forEach(grill => {
        if (
            grill.state !== 'cooking' &&
            grill.state !== 'ready'
        ) {
            return;
        }

        const passed = current - grill.born;

        if (
            grill.state === 'cooking' &&
            passed >= COOK_MS
        ) {
            grill.state = 'ready';
            grillsChanged = true;
        }

        if (
            grill.state === 'ready' &&
            passed >= BURN_MS
        ) {
            grill.state = 'burnt';
            grillsChanged = true;
        }
    });

    if (grillsChanged) {
        renderGrills();
    }

    // 조리 진행 게이지
    game.grills.forEach((grill, i) => {
        const bar = el(`cook-${i}`);

        if (!bar) return;

        let percent = 0;

        if (grill.state === 'cooking') {
            percent = Math.min(
                100,
                100 * (
                    current - grill.born
                ) / COOK_MS
            );
        }

        if (grill.state === 'ready') {
            percent = 100;
        }

        if (grill.state === 'burnt') {
            percent = 100;
            bar.style.background = '#9d5950';
        }

        bar.style.width = percent + '%';
    });
}

// ==========================================
// 처음 화면 초기화
// ==========================================

function initializeScreen() {
    renderSupplies();

    el('customers').innerHTML = Array.from(
        {length: 3},
        (_, i) => `
        <div class="customer">
            <span class="face">🐱</span>
            <strong>손님 ${i + 1}</strong>
            <div class="order">
                게임 시작 후 주문이 나타나요!
            </div>
            <div class="patience"></div>
        </div>
        `
    ).join('');

    el('grills').innerHTML = Array.from(
        {length: 3},
        (_, i) => `
        <div class="grill">
            <div class="holes">
                ${'<div class="ball"></div>'.repeat(6)}
            </div>
            <strong>${i + 1}번 조리판</strong>
            <div class="bar"></div>
            <small>게임을 시작해 주세요</small>
        </div>
        `
    ).join('');
}

initializeScreen();

// 0.1초마다 게임 상태 갱신
setInterval(tick, 100);

</script>
</body>
</html>
""", height=700, scrolling=False)
