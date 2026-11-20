
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json

# ==========================================
# 와글와글 포장마차 - 타코야끼
# 사람 손님 캐릭터 및 주문 말풍선 적용
# ==========================================

# ==========================================
# 1. 꾸미기 설정 불러오기
# ==========================================

CUSTOMER_THEMES = {
    "🎆 축제 손님": "festival",
    "🎒 학생": "student",
    "💼 직장인": "office",
    "👕 캐주얼": "casual",
}

BUBBLE_THEMES = {
    "💭 둥근 말풍선": "round",
    "💥 코믹 말풍선": "comic",
    "▫️ 심플 말풍선": "simple",
}

saved_theme = st.session_state.get(
    "saved_customer_style",
    "🎆 축제 손님",
)

saved_bubble = st.session_state.get(
    "saved_bubble_style",
    "💭 둥근 말풍선",
)

theme_code = CUSTOMER_THEMES.get(
    saved_theme,
    "festival",
)

bubble_code = BUBBLE_THEMES.get(
    saved_bubble,
    "round",
)


# ==========================================
# 2. GitHub PNG 이미지 읽기
# ==========================================

ROOT = Path(__file__).resolve().parent.parent

ASSET_DIR = (
    ROOT
    / "assets"
    / "customers"
    / theme_code
)

EXPRESSIONS = [
    "normal",
    "waiting",
    "angry",
    "happy",
]


def load_customer_images():
    images = {}
    missing = []

    for number in range(1, 6):
        for expression in EXPRESSIONS:

            filename = (
                f"{theme_code}_{number:02d}_"
                f"{expression}.png"
            )

            filepath = ASSET_DIR / filename

            if filepath.is_file():
                encoded = base64.b64encode(
                    filepath.read_bytes()
                ).decode("ascii")

                images[
                    f"{number}_{expression}"
                ] = (
                    "data:image/png;base64,"
                    + encoded
                )

            else:
                missing.append(str(filepath))

    return images, missing


customer_images, missing_images = (
    load_customer_images()
)

if missing_images:
    st.error(
        "손님 캐릭터 이미지를 찾지 못했어요. "
        "GitHub의 assets/customers 폴더를 "
        "확인해 주세요."
    )

    with st.expander("찾지 못한 이미지"):
        for path in missing_images:
            st.code(path)

    st.stop()


# ==========================================
# 3. Streamlit 화면 설정
# ==========================================

st.html("""
<style>
[data-testid="stAppViewContainer"] {
    background: #fff0d8;
}

.block-container {
    max-width: 100% !important;
    padding: 0.3rem 0.6rem !important;
}

iframe {
    border: none !important;
    display: block;
}
</style>
""")


# ==========================================
# 4. 게임 HTML
# ==========================================

GAME_HTML = r"""
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
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
    font-family: "Malgun Gothic", sans-serif;
    color: #70422b;
}

button {
    font: inherit;
    cursor: pointer;
}

/* =====================================
   게임 전체 화면
===================================== */

.game {
    position: relative;
    width: 100%;
    height: 680px;
    padding: 8px 12px;
    overflow: hidden;
    border-radius: 17px;

    background: linear-gradient(
        180deg,
        #718aab 0%,
        #e7aaa5 35%,
        #f8d9a6 75%,
        #c28a61 100%
    );
}

/* =====================================
   상단 상태 표시
===================================== */

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    min-height: 43px;
}

.logo {
    padding: 7px 12px;
    border: 3px solid #a85d37;
    border-radius: 13px;
    background: #fff0ce;
    color: #974b31;
    font-size: 17px;
    font-weight: 900;
    white-space: nowrap;
}

.stats {
    display: flex;
    gap: 6px;
}

.stat {
    min-width: 73px;
    padding: 5px 8px;
    text-align: center;
    border: 2px solid #f6d6a0;
    border-radius: 11px;
    background: #784d3d;
    color: white;
    font-size: 15px;
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

.sign {
    width: fit-content;
    margin: 5px auto 9px;
    padding: 6px 24px;
    border: 3px solid #f2ca87;
    border-radius: 13px;
    background: #934a35;
    box-shadow: 0 4px #683b29;
    color: #fff6dc;
    font-size: 17px;
    font-weight: 900;
}

/* =====================================
   사람 손님 3명
===================================== */

.customers {
    display: grid;
    grid-template-columns: repeat(
        3,
        minmax(0, 1fr)
    );

    gap: 9px;
    max-width: 1100px;
    margin: 0 auto 11px;
}

.customer {
    position: relative;
    height: 189px;
    padding: 6px 8px;

    display: flex;
    flex-direction: column;
    align-items: center;

    border: 3px solid #d7a06c;
    border-radius: 19px;

    background: linear-gradient(
        180deg,
        #fff7e8 0%,
        #ffebd1 100%
    );

    box-shadow: 0 4px #a16a43;
    text-align: center;
}

/* 주문 말풍선 */

.order-bubble {
    position: relative;
    z-index: 2;

    display: flex;
    align-items: center;
    justify-content: center;

    width: 94%;
    max-width: 290px;
    min-height: 49px;

    margin-bottom: 3px;
    padding: 6px 8px;

    background: white;
    color: #805139;

    font-size: 12px;
    font-weight: 900;
    line-height: 1.35;
}

.order-bubble.round {
    border: 3px solid #d9ab83;
    border-radius: 19px;
}

.order-bubble.round::after {
    content: "";
    position: absolute;
    left: 48%;
    bottom: -10px;

    width: 15px;
    height: 15px;

    background: white;
    border-right: 3px solid #d9ab83;
    border-bottom: 3px solid #d9ab83;
    transform: rotate(45deg);
}

.order-bubble.comic {
    border: 3px solid #d28b54;
    border-radius: 13px;
    background: #fff2b7;
    box-shadow: 3px 3px #e7b06e;
}

.order-bubble.comic::after {
    content: "";
    position: absolute;
    left: 48%;
    bottom: -12px;
    border-left: 11px solid transparent;
    border-right: 6px solid transparent;
    border-top: 13px solid #d28b54;
}

.order-bubble.simple {
    border: 2px solid #d8c1aa;
    border-radius: 9px;
    background: #fffdf8;
}

/* 캐릭터 이미지 */

.avatar-area {
    height: 100px;
    width: 100%;

    display: flex;
    align-items: center;
    justify-content: center;

    overflow: visible;
    pointer-events: none;
}

.avatar {
    display: block;
    width: 125px;
    height: 100px;
    object-fit: contain;
    object-position: center bottom;
    pointer-events: none;
    user-select: none;
}

.customer.happy {
    background: #fff5cb;
}

.customer.urgent {
    border-color: #d9655b;
}

.customer-label {
    font-size: 10px;
    font-weight: 900;
    color: #986344;
    margin: 1px 0 3px;
}

/* 손님 대기 게이지 */

.patience {
    width: 94%;
    height: 10px;
    overflow: hidden;

    border: 2px solid #d7b28b;
    border-radius: 999px;
    background: #e7cfaf;
}

.patience span {
    display: block;
    height: 100%;
    width: 100%;
    background: #76c66b;
}

/* =====================================
   조리대
===================================== */

.counter {
    max-width: 1200px;
    margin: 0 auto;

    padding: 8px;
    border: 5px solid #8e5334;
    border-radius: 20px;

    background: repeating-linear-gradient(
        0deg,
        #b87648 0 20px,
        #c88958 20px 40px
    );

    box-shadow: 0 6px #643b28;
}

.counter h3 {
    margin: 0 0 6px;
    color: #fff5de;
    text-align: center;
    font-size: 15px;
    text-shadow: 0 2px #73472e;
}

.kitchen {
    display: grid;
    grid-template-columns:
        minmax(0, 2fr)
        minmax(145px, .85fr);

    gap: 9px;
}

.grills {
    display: grid;
    grid-template-columns: repeat(
        3,
        minmax(0, 1fr)
    );

    gap: 7px;
    padding: 7px;

    background: #44434a;
    border: 4px solid #302e34;
    border-radius: 15px;
}

.grill {
    min-height: 137px;
    padding: 5px 3px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 5px;

    border: 2px solid #686268;
    border-radius: 13px;

    background: #28282c;
    color: #fff5da;
    text-align: center;
}

.grill strong {
    font-size: 11px;
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
    display: grid;
    place-items: center;

    border: 2px solid #111219;
    border-radius: 50%;

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
    overflow: hidden;
    border-radius: 10px;
    background: #151515;
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

.plate-zone,
.trash {
    padding: 6px;
    border: 3px solid #e5bd8f;
    border-radius: 13px;
    background: #fff1d9;
    text-align: center;
}

.plate-zone {
    min-height: 108px;

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
    width: 67px;
    height: 67px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    border-radius: 50%;

    background: radial-gradient(
        circle,
        white 0 48%,
        #b7d6e2 50% 60%,
        white 62%
    );

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
    min-height: 42px;
    display: grid;
    place-items: center;

    background: #f9d6c7;
    font-size: 12px;
    font-weight: 900;
}

/* =====================================
   재료 및 토핑
===================================== */

.supplies {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 9px;

    max-width: 1200px;
    margin: 11px auto 7px;
}

.supply {
    padding: 7px;

    border: 3px solid #be8454;
    border-radius: 15px;
    background: #fff1da;
}

.supply h3 {
    margin: 0 0 6px;
    font-size: 12px;
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
    margin-bottom: 2px;
    font-size: 24px;
}

.help {
    max-width: 1200px;
    margin: 0 auto;
    padding: 6px;

    border: 2px solid #d8ab75;
    border-radius: 10px;
    background: #fff4da;

    text-align: center;
    font-size: 11px;
    font-weight: 800;
}

/* =====================================
   드래그 앤 드롭
===================================== */

[data-source] {
    cursor: grab;
    touch-action: none;
    user-select: none;
}

[data-source]:active {
    cursor: grabbing;
}

.dragging-original {
    opacity: 0.45;
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

    border: 3px solid #d9a16b;
    border-radius: 14px;
    background: #fff8e7;
    box-shadow: 0 5px 12px #0004;

    font-size: 28px;
    text-align: center;
}

.ghost small {
    display: block;
    font-size: 11px;
    font-weight: 900;
}

/* =====================================
   알림
===================================== */

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
    text-align: center;

    opacity: 0;
    pointer-events: none;
    transition: opacity .2s;
}

.toast.show {
    opacity: 1;
}

/* =====================================
   게임 시작 및 종료
===================================== */

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
    padding: 30px 20px;

    border: 6px solid #bc7950;
    border-radius: 25px;
    background: #fff4d9;

    text-align: center;
    box-shadow: 0 10px #7c4d37;
}

.panel-icon {
    font-size: 58px;
}

.start-panel h2 {
    margin: 10px 0;
    color: #954a33;
    font-size: 26px;
}

.start-panel p {
    font-size: 15px;
    font-weight: 900;
    line-height: 1.8;
}

.start-button {
    margin-top: 10px;
    padding: 14px 25px;

    border: none;
    border-radius: 15px;

    background: #e8734c;
    color: white;
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

/* =====================================
   작은 화면 대응
===================================== */

@media (max-width: 800px) {

    .game {
        padding: 6px;
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
        padding: 4px;
        font-size: 12px;
    }

    .stat small {
        font-size: 8px;
    }

    .sign {
        font-size: 14px;
    }

    .customers {
        gap: 5px;
    }

    .customer {
        height: 175px;
        padding: 5px 3px;
    }

    .order-bubble {
        font-size: 10px;
        min-height: 47px;
        padding: 5px 3px;
    }

    .avatar {
        width: 95px;
        height: 90px;
    }

    .avatar-area {
        height: 90px;
    }

    .kitchen {
        grid-template-columns:
            minmax(0, 1.8fr)
            minmax(100px, .7fr);

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

    <!-- 상단 정보 -->

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

    <!-- 손님 3명 -->

    <div
        class="customers"
        id="customers">
    </div>

    <!-- 조리대 -->

    <div class="counter">

        <h3>🍳 타코야끼 조리대</h3>

        <div class="kitchen">

            <div
                class="grills"
                id="grills">
            </div>

            <div class="right">

                <div
                    class="plate-zone"
                    data-drop="plate">

                    <strong>
                        🍽️ 완성 접시
                    </strong>

                    <div
                        class="plate"
                        id="plate">
                        🍽️
                    </div>

                    <small id="plate-help">
                        익은 타코야끼를 올려 주세요
                    </small>

                </div>

                <div
                    class="trash"
                    data-drop="trash">

                    🗑️ 음식 버리기

                </div>

            </div>
        </div>
    </div>

    <!-- 재료 및 토핑 -->

    <div class="supplies">

        <div class="supply">

            <h3>
                🥣 속재료를 조리판으로 드래그
            </h3>

            <div
                class="items"
                id="fillings">
            </div>

        </div>

        <div class="supply">

            <h3>
                ✨ 토핑을 완성 접시로 드래그
            </h3>

            <div
                class="items"
                id="toppings">
            </div>

        </div>

    </div>

    <div class="help">
        재료 → 조리판 → 완성 접시 → 토핑 → 손님 |
        필요 없는 음식은 휴지통에 버리세요!
    </div>

    <div class="toast" id="toast"></div>

    <!-- 시작 및 종료 창 -->

    <div class="overlay" id="overlay">

        <div class="start-panel">

            <div
                class="panel-icon"
                id="panel-icon">
                🐙
            </div>

            <h2 id="panel-title">
                타코야끼 가게
            </h2>

            <p id="panel-description">
                주문에 맞춰 타코야끼를 완성하세요!
                <br>
                ❤️ 목숨 3개 · 총 5레벨
                <br>
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

    <div
        class="countdown"
        id="countdown">

        <span id="count-text">
            3
        </span>

    </div>

</div>


<script>

// ==========================================
// 5. Python에서 전달한 캐릭터 이미지
// ==========================================

const CUSTOMER_IMAGES = __CUSTOMER_IMAGES__;

const BUBBLE_STYLE = "__BUBBLE_STYLE__";

// ==========================================
// 6. 게임 기본 설정
// ==========================================

const LEVEL_TIMES = [
    90, 120, 120, 150, 150
];

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
// 손님 캐릭터 이미지
// ==========================================

function customerImage(number, expression) {

    const key = `${number}_${expression}`;

    return (
        CUSTOMER_IMAGES[key] ||
        CUSTOMER_IMAGES[`${number}_normal`]
    );
}

// ==========================================
// 새 손님 만들기
// ==========================================

function newCustomer() {

    const [min, max] =
        CUSTOMER_WAIT[game.level - 1];

    return {
        character: Math.floor(
            Math.random() * 5
        ) + 1,

        fill: pick(fillings),
        top: pick(toppings),

        born: now(),

        patience: (
            min + Math.random() * (max - min)
        ) * 1000,

        happyUntil: 0
    };
}

// ==========================================
// 카운트다운
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
// 메시지
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

    el('lives').textContent =
        '❤️'.repeat(game.lives);

    el('score').textContent = game.score;
}

// ==========================================
// 손님 출력
// ==========================================

function renderCustomers() {

    if (!game) return;

    el('customers').innerHTML =
        game.customers.map((c, i) => `

        <div
            class="customer"
            id="customer-${i}"
            data-drop="customer"
            data-index="${i}">

            <div
                class="order-bubble ${BUBBLE_STYLE}"
                id="bubble-${i}">

                ${c.fill.emoji} ${c.fill.name}
                +
                ${c.top.emoji} ${c.top.name}

            </div>

            <div class="avatar-area">

                <img
                    class="avatar"
                    id="avatar-${i}"
                    src="${customerImage(
                        c.character,
                        'normal'
                    )}"
                    alt="손님 캐릭터"
                    draggable="false">

            </div>

            <div
                class="customer-label"
                id="customer-label-${i}">

                주문을 기다리는 중

            </div>

            <div class="patience">
                <span id="patience-${i}"></span>
            </div>

        </div>

        `).join('');
}

// ==========================================
// 손님 표정 실시간 변경
// ==========================================

function updateCustomerVisuals(current) {

    if (!game) return;

    game.customers.forEach((c, i) => {

        const avatar = el(`avatar-${i}`);
        const bar = el(`patience-${i}`);
        const label = el(`customer-label-${i}`);
        const card = el(`customer-${i}`);
        const bubble = el(`bubble-${i}`);

        if (!avatar || !bar || !card) return;

        // 서빙 성공 후 만족 표정

        if (c.happyUntil > 0) {

            const image = customerImage(
                c.character,
                'happy'
            );

            if (avatar.src !== image) {
                avatar.src = image;
            }

            card.classList.add('happy');
            card.classList.remove('urgent');

            label.textContent = '맛있어요!';

            bubble.textContent = '감사합니다!';

            bar.style.width = '100%';
            bar.style.background = '#7acb75';

            return;
        }

        const passed = current - c.born;

        const percent = Math.max(
            0,
            100 * (1 - passed / c.patience)
        );

        let expression = 'normal';

        if (percent <= 30) {
            expression = 'angry';
        } else if (percent <= 65) {
            expression = 'waiting';
        }

        const image = customerImage(
            c.character,
            expression
        );

        if (avatar.src !== image) {
            avatar.src = image;
        }

        card.classList.remove('happy');

        card.classList.toggle(
            'urgent',
            percent <= 30
        );

        if (percent <= 30) {

            label.textContent =
                '너무 오래 기다렸어요!';

            bar.style.background = '#dc6753';

        } else if (percent <= 65) {

            label.textContent =
                '조금 초조해요...';

            bar.style.background = '#e8b64a';

        } else {

            label.textContent =
                '주문을 기다리는 중';

            bar.style.background = '#70b963';
        }

        bar.style.width = percent + '%';

    });
}

// ==========================================
// 조리판 표시
// ==========================================

function renderGrills() {

    if (!game) return;

    const messages = {
        empty: '재료를 넣어 주세요',
        cooking: '조리 중...',
        ready: '다 익었어요!',
        burnt: '음식이 탔어요!'
    };

    el('grills').innerHTML =
        game.grills.map((g, i) => {

            let icon = '';

            if (g.state === 'cooking') {
                icon = '🟡';
            }

            if (g.state === 'ready') {
                icon = '🟤';
            }

            if (g.state === 'burnt') {
                icon = '⚫';
            }

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

            <div
                class="grill"
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

                <strong>
                    ${i + 1}번 조리판
                </strong>

                <div class="bar">
                    <span id="cook-${i}"></span>
                </div>

                <small>
                    ${messages[g.state]}
                </small>

            </div>

            `;

        }).join('');
}

// ==========================================
// 완성 접시
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

    plate.setAttribute(
        'data-source',
        'plate'
    );

    plate.setAttribute(
        'data-emoji',
        '🍡'
    );

    plate.setAttribute(
        'data-label',
        '완성 음식'
    );

    el('plate-help').textContent =
        game.plate.top
            ? '손님에게 서빙하세요'
            : '토핑을 올려 주세요';
}

// ==========================================
// 재료 및 토핑
// ==========================================

function renderSupplies() {

    el('fillings').innerHTML =
        fillings.map((f, i) => `

        <div
            class="item"
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

        <div
            class="item"
            data-source="topping"
            data-index="${i}"
            data-emoji="${t.emoji}"
            data-label="${t.name}">

            <span>${t.emoji}</span>
            ${t.name}

        </div>

        `).join('');
}

// ==========================================
// 전체 화면 갱신
// ==========================================

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

    if (!customer || customer.happyUntil > 0) {
        return;
    }

    if (!plate || !plate.top) {

        tell(
            '토핑까지 완성한 음식을 서빙하세요!'
        );

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

        customer.happyUntil = now() + 850;

        tell('주문 성공! 맛있게 드세요!');

        updateHud();

        updateCustomerVisuals(now());

    } else {

        game.missed++;

        loseLife('주문이 틀렸어요!');

        if (!game.ended) {

            game.customers[index] =
                newCustomer();

            renderCustomers();
        }
    }
}

// ==========================================
// 드롭 처리
// ==========================================

function handleDrop(
    kind,
    index,
    target,
    targetIndex
) {

    if (!game || game.ended) return;

    // 속재료를 조리판에 올리기

    if (
        kind === 'filling' &&
        target === 'grill'
    ) {

        const grill = game.grills[targetIndex];

        if (!grill || grill.state !== 'empty') {

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

    // 익은 타코야끼를 접시에 담기

    if (
        kind === 'grill' &&
        target === 'plate'
    ) {

        const grill = game.grills[index];

        if (!grill || grill.state !== 'ready') {

            tell(
                '다 익은 음식만 접시에 담을 수 있어요!'
            );

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

        game.grills[index] = {
            state: 'empty'
        };

        renderGrills();
        renderPlate();

        return;
    }

    // 접시에 토핑 올리기

    if (
        kind === 'topping' &&
        target === 'plate'
    ) {

        if (!game.plate) {

            tell(
                '먼저 타코야끼를 접시에 담아 주세요!'
            );

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

    // 완성된 음식을 손님에게 서빙

    if (
        kind === 'plate' &&
        target === 'customer'
    ) {

        serveCustomer(targetIndex);

        return;
    }

    // 휴지통에 음식 버리기

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

    const source = e.target.closest(
        '[data-source]'
    );

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
        source: source,
        kind: source.dataset.source,
        index: Number(
            source.dataset.index || 0
        ),
        ghost: ghost
    };

    source.classList.add(
        'dragging-original'
    );

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

    if (
        !drag ||
        drag.pointerId !== e.pointerId
    ) {
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

document.addEventListener(
    'pointerup',
    releaseDrag
);

document.addEventListener(
    'pointercancel',
    e => {

        if (
            !drag ||
            drag.pointerId !== e.pointerId
        ) {
            return;
        }

        drag.ghost.remove();

        if (drag.source.isConnected) {
            drag.source.classList.remove(
                'dragging-original'
            );
        }

        if (highlighted) {
            highlighted.classList.remove(
                'drop-over'
            );
        }

        highlighted = null;
        drag = null;
    }
);

// ==========================================
// 레벨 이동
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
        won
            ? '5레벨 클리어!'
            : '영업 종료!';

    el('panel-description').innerHTML = `

        최종 점수: ${game.score}점
        <br>

        성공한 주문: ${game.served}개
        <br>

        ${won
            ? '축하합니다! 모든 레벨을 통과했어요!'
            : '다시 도전해 보세요!'}

    `;

    el('start-button').textContent =
        '🔄 다시 도전하기';

    el('overlay').classList.remove(
        'hidden'
    );
}

// ==========================================
// 게임 타이머
// ==========================================

function tick() {

    if (!game || game.ended) return;

    const current = now();

    const elapsed = (
        current - game.levelStart
    ) / 1000;

    const remaining = Math.max(
        0,
        LEVEL_TIMES[game.level - 1] - elapsed
    );

    el('time').textContent =
        Math.ceil(remaining);

    // 레벨 제한 시간 종료

    if (remaining <= 0) {

        nextLevel();

        return;
    }

    // 손님 대기 시간 확인

    let customersChanged = false;

    for (
        let i = 0;
        i < game.customers.length;
        i++
    ) {

        const c = game.customers[i];

        // 음식을 받은 손님은 잠깐 웃고 퇴장

        if (c.happyUntil > 0) {

            if (current >= c.happyUntil) {

                game.customers[i] =
                    newCustomer();

                customersChanged = true;
            }

            continue;
        }

        const passed = current - c.born;

        if (passed >= c.patience) {

            game.missed++;

            loseLife(
                '손님이 기다리다 떠났어요!'
            );

            if (game.ended) return;

            game.customers[i] =
                newCustomer();

            customersChanged = true;
        }
    }

    if (customersChanged) {

        renderCustomers();
    }

    updateCustomerVisuals(current);

    // 음식 익힘 상태

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

        if (
            grill.state === 'ready' ||
            grill.state === 'burnt'
        ) {

            percent = 100;
        }

        bar.style.width = percent + '%';

        bar.style.background =
            grill.state === 'burnt'
                ? '#9d5950'
                : '#efc456';
    });
}

// ==========================================
// 시작 전 미리보기
// ==========================================

function initializeScreen() {

    renderSupplies();

    el('customers').innerHTML =
        Array.from(
            {length: 3},
            (_, i) => `

            <div class="customer">

                <div
                    class="order-bubble ${BUBBLE_STYLE}">

                    게임 시작 후 주문이 나타나요!

                </div>

                <div class="avatar-area">

                    <img
                        class="avatar"
                        src="${customerImage(
                            i + 1,
                            'normal'
                        )}"
                        alt="손님">

                </div>

                <div class="customer-label">
                    영업 준비 중
                </div>

                <div class="patience">
                    <span></span>
                </div>

            </div>

            `
        ).join('');

    el('grills').innerHTML =
        Array.from(
            {length: 3},
            (_, i) => `

            <div class="grill">

                <div class="holes">

                    ${'<div class="ball"></div>'.repeat(6)}

                </div>

                <strong>
                    ${i + 1}번 조리판
                </strong>

                <div class="bar"></div>

                <small>
                    게임을 시작해 주세요
                </small>

            </div>

            `
        ).join('');
}

initializeScreen();

// 0.1초마다 게임 상태 확인

setInterval(tick, 100);

</script>

</body>
</html>
"""


# ==========================================
# 5. Python 설정을 게임 HTML에 전달
# ==========================================

GAME_HTML = GAME_HTML.replace(
    "__CUSTOMER_IMAGES__",
    json.dumps(customer_images),
)

GAME_HTML = GAME_HTML.replace(
    "__BUBBLE_STYLE__",
    bubble_code,
)


# ==========================================
# 6. 실제 게임 표시
# ==========================================

components.html(
    GAME_HTML,
    height=700,
    scrolling=False,
)
