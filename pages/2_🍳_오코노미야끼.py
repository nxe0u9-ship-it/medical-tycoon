
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json

# ==========================================
# 와글와글 포장마차 - 오코노미야끼
# 손님 PNG 및 꾸미기 설정 연동
# ==========================================

CUSTOMER_THEMES = {
    "🎆 축제 손님": "festival",
    "🎒 학생": "student",
    "💼 직장인": "office",
    "👕 캐주얼": "casual",
}

BUBBLE_THEMES = {
    "💭 둥근 말풍선": "round",
    "✨ 강조 말풍선": "comic",
    "💥 코믹 말풍선": "comic",
    "▫️ 심플 말풍선": "simple",
}

customer_style = st.session_state.get(
    "saved_customer_style", "🎆 축제 손님"
)

bubble_style = st.session_state.get(
    "saved_bubble_style", "💭 둥근 말풍선"
)

theme = CUSTOMER_THEMES.get(
    customer_style, "festival"
)

bubble = BUBBLE_THEMES.get(
    bubble_style, "round"
)

ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = ROOT / "assets" / "customers" / theme


# ==========================================
# 손님 이미지 불러오기
# ==========================================

def load_customer_images():
    images = {}
    missing = []

    for number in range(1, 6):
        for expression in (
            "normal", "waiting", "angry", "happy"
        ):
            filename = (
                f"{theme}_{number:02d}_{expression}.png"
            )
            path = IMAGE_DIR / filename

            if path.is_file():
                encoded = base64.b64encode(
                    path.read_bytes()
                ).decode("ascii")

                images[f"{number}_{expression}"] = (
                    "data:image/png;base64," + encoded
                )
            else:
                missing.append(filename)

    return images, missing


customer_images, missing_images = load_customer_images()

if missing_images:
    st.error("손님 캐릭터 이미지가 누락되었어요.")
    st.code("\n".join(missing_images))
    st.stop()


# ==========================================
# Streamlit 화면 스타일
# ==========================================

st.html("""
<style>
[data-testid="stAppViewContainer"] {
    background: #fff0d8;
}

[data-testid="stMain"] .block-container {
    max-width: 100% !important;
    padding: 0.25rem 0.5rem !important;
}

iframe {
    display: block;
    border: none !important;
}
</style>
""")


# ==========================================
# 게임 HTML / CSS / JavaScript
# ==========================================

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width,initial-scale=1">

<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: "Malgun Gothic", sans-serif;
    color: #75452e;
}

.game {
    position: relative;
    width: 100%;
    height: 680px;
    padding: 8px 12px;
    border-radius: 18px;
    overflow: hidden;
    background: linear-gradient(
        180deg,
        #7895b8 0%,
        #d7a5ad 25%,
        #f8c1a9 48%,
        #f8d9aa 75%,
        #c48e65 100%
    );
}

/* 상단 정보 */

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 43px;
    gap: 8px;
}

.logo {
    padding: 7px 12px;
    border: 3px solid #a85d37;
    border-radius: 13px;
    background: #fff0ce;
    color: #964b30;
    font-size: 17px;
    font-weight: 900;
    white-space: nowrap;
}

.stats {
    display: flex;
    gap: 6px;
}

.stat {
    min-width: 70px;
    padding: 5px 7px;
    border: 2px solid #f6d6a0;
    border-radius: 11px;
    background: #784d3d;
    color: white;
    text-align: center;
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

/* 안내 메시지 */

.notice-area {
    height: 43px;
    margin: 2px 0 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
}

.toast {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 245px;
    max-width: min(520px, 85%);
    min-height: 35px;
    padding: 6px 18px;
    border: 2px solid #fff3d9;
    border-radius: 12px;
    color: white;
    font-size: 14px;
    font-weight: 900;
    text-align: center;
    box-shadow: 0 3px 8px #0003;
    opacity: 0;
    transform: translateY(-5px);
    transition: opacity .18s, transform .18s;
}

.toast.show {
    opacity: 1;
    transform: translateY(0);
}

.toast.info {
    background: #8b5a3c;
}

.toast.success {
    background: #269957;
    border-color: #dbffe5;
}

.toast.error {
    background: #d74646;
    border-color: #ffe0de;
}

.toast.warning {
    background: #e8a02f;
    border-color: #fff1b4;
    color: #493116;
}

/* 가게 이름 */

.sign {
    width: fit-content;
    margin: 0 auto 7px;
    padding: 5px 24px;
    border: 3px solid #f2ca87;
    border-radius: 13px;
    background: #934a35;
    box-shadow: 0 4px #683b29;
    color: #fff6dc;
    font-size: 16px;
    font-weight: 900;
}

/* 손님 3명 */

.customers {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    max-width: 1050px;
    height: 151px;
    margin: 0 auto 7px;
}

.customer {
    position: relative;
    min-width: 0;
    padding: 0 5px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    text-align: center;
}

/* 말풍선 공통 */

.bubble {
    position: relative;
    z-index: 2;
    width: 94%;
    max-width: 260px;
    min-height: 35px;
    margin-bottom: 5px;
    padding: 5px 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #fffdf5;
    font-size: 11px;
    font-weight: 900;
    line-height: 1.3;
}

/* 1. 둥근 말풍선 */

.bubble.round {
    border: 3px solid #d9ab83;
    border-radius: 18px;
    background: #fffdf5;
}

/* 2. 강조 말풍선
   기존 노란색 디자인 유지 */

.bubble.comic {
    border: 3px solid #d28b54;
    border-radius: 12px;
    background: #fff3bd;
    box-shadow: 3px 3px #e7b06e;
}

/* 3. 심플 말풍선 */

.bubble.simple {
    border: 2px solid #d8c1aa;
    border-radius: 9px;
    background: #fffdf5;
}

/* 둥근/심플 말풍선의 꼬리 */

.bubble.round::after,
.bubble.simple::after {
    content: "";
    position: absolute;
    bottom: -8px;
    left: calc(50% - 6px);
    width: 12px;
    height: 12px;
    background: inherit;
    transform: rotate(45deg);
    border-right: 2px solid #d9ab83;
    border-bottom: 2px solid #d9ab83;
}

/* 손님 이미지와 대기 게이지 */

.avatar {
    width: 135px;
    height: 88px;
    object-fit: contain;
    object-position: center bottom;
    pointer-events: none;
    user-select: none;
    filter: drop-shadow(0 3px 2px #0002);
}

.customer-label {
    margin: 1px 0 3px;
    font-size: 10px;
    font-weight: 900;
}

.patience {
    width: 74%;
    height: 8px;
    border: 2px solid #b8835c;
    border-radius: 20px;
    background: #e4ccb0;
    overflow: hidden;
}

.patience span {
    display: block;
    width: 100%;
    height: 100%;
    background: #70b963;
}

.customer.happy .avatar {
    filter: drop-shadow(0 0 8px gold);
}

.customer.urgent .bubble {
    border-color: #d9655b;
}

/* 오코노미야끼 철판 */

.counter {
    max-width: 1200px;
    margin: auto;
    padding: 8px;
    border: 5px solid #8e5334;
    border-radius: 20px;
    background: repeating-linear-gradient(
        0deg,
        #b87648 0 20px,
        #c88958 20px 40px
    );
    box-shadow: 0 5px #643b28;
}

.counter h3 {
    margin: 0 0 6px;
    text-align: center;
    color: #fff5de;
    font-size: 15px;
}

.kitchen {
    display: grid;
    grid-template-columns:
        minmax(0, 2fr) minmax(200px, .85fr);
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
    min-height: 132px;
    padding: 5px 3px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    background: #28282c;
    color: #fff5da;
    border: 2px solid #686268;
    border-radius: 13px;
    text-align: center;
}

.grill strong {
    font-size: 11px;
    pointer-events: none;
}

.grill small {
    min-height: 13px;
    font-size: 10px;
    font-weight: 900;
    pointer-events: none;
}

.pancake {
    width: 70px;
    height: 58px;
    display: grid;
    place-items: center;
    font-size: 34px;
    pointer-events: none;
}

.bar {
    width: 80%;
    height: 9px;
    border: 1px solid #555;
    border-radius: 20px;
    background: #151515;
    overflow: hidden;
    pointer-events: none;
}

.bar span {
    display: block;
    width: 0%;
    height: 100%;
    background: #efc456;
    border-radius: 20px;
}

/* 접시 */

.right {
    display: flex;
    flex-direction: column;
    gap: 7px;
    min-width: 0;
}

.plate-zone {
    flex: 1;
    min-height: 105px;
    padding: 6px;
    border: 3px solid #e5bd8f;
    border-radius: 13px;
    background: #fff1d9;
    text-align: center;
}

.plate-zone strong {
    font-size: 12px;
}

.plate {
    width: 74px;
    height: 70px;
    margin: 4px auto;
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
    pointer-events: none;
}

#plate-help {
    font-size: 10px;
}

.trash {
    min-height: 34px;
    padding: 5px;
    border: 3px solid #e5bd8f;
    border-radius: 12px;
    background: #f9d6c7;
    text-align: center;
    font-size: 12px;
    font-weight: 900;
}

/* 재료와 도구 */

.supplies {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 9px;
    max-width: 1200px;
    margin: 10px auto 7px;
}

.supply {
    min-width: 0;
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
    font-size: 11px;
    font-weight: 900;
}

.item span {
    display: block;
    margin-bottom: 2px;
    font-size: 23px;
}

.help {
    max-width: 1200px;
    margin: auto;
    padding: 6px;
    border: 2px solid #d8ab75;
    border-radius: 10px;
    background: #fff4da;
    text-align: center;
    font-size: 11px;
    font-weight: 800;
}

/* 드래그 앤 드롭 */

[data-source] {
    cursor: grab;
    touch-action: none;
    user-select: none;
}

.dragging-original {
    opacity: .45;
}

.drop-over {
    outline: 4px solid #ffe47c;
    outline-offset: 2px;
}

.ghost {
    position: fixed;
    z-index: 1000;
    pointer-events: none;
    padding: 8px;
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
}

/* 게임 시작 및 종료 */

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

.panel {
    width: min(460px, 95%);
    padding: 30px 20px;
    border: 6px solid #bc7950;
    border-radius: 25px;
    background: #fff4d9;
    box-shadow: 0 10px #7c4d37;
    text-align: center;
}

.panel h2 {
    color: #954a33;
    font-size: 26px;
}

.panel p {
    font-size: 15px;
    font-weight: 900;
    line-height: 1.8;
}

.start {
    margin-top: 10px;
    padding: 14px 25px;
    border: none;
    border-radius: 15px;
    background: #e8734c;
    color: white;
    box-shadow: 0 5px #aa4c30;
    font-size: 20px;
    font-weight: 900;
    cursor: pointer;
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
    font-size: 110px;
    font-weight: 900;
}

.countdown.show {
    display: flex;
}

@media (max-width: 900px) {
    .game {
        padding: 6px;
    }

    .logo {
        font-size: 12px;
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

    .bubble {
        font-size: 10px;
    }

    .avatar {
        width: 112px;
    }

    .kitchen {
        grid-template-columns:
            minmax(0, 1.3fr)
            minmax(190px, 1fr);
    }

    .grills {
        gap: 3px;
        padding: 4px;
    }

    .pancake {
        width: 50px;
        font-size: 27px;
    }

    .plate {
        width: 57px;
        height: 57px;
        font-size: 22px;
    }

    .item {
        font-size: 10px;
    }

    .item span {
        font-size: 19px;
    }

    .toast {
        min-width: 180px;
        font-size: 12px;
        padding: 6px 10px;
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

    <div class="notice-area">
        <div class="toast info"
             id="toast"
             role="status"
             aria-live="polite">
        </div>
    </div>

    <div class="sign">
        🍳 오코노미야끼 가게 🍳
    </div>

    <div class="customers" id="customers"></div>

    <div class="counter">
        <h3>🔥 오코노미야끼 철판 조리대</h3>

        <div class="kitchen">

            <div class="grills" id="grills"></div>

            <div class="right">

                <div class="plate-zone"
                     data-drop="plate">

                    <strong>🍽️ 완성 접시</strong>

                    <div class="plate" id="plate">
                        🍽️
                    </div>

                    <small id="plate-help">
                        완성된 음식을 옮겨 주세요
                    </small>

                </div>

                <div class="trash"
                     data-drop="trash">
                    🗑️ 음식 버리기
                </div>

            </div>
        </div>
    </div>

    <div class="supplies">

        <div class="supply">
            <h3>① 반죽과 재료를 철판으로 드래그</h3>
            <div class="items" id="ingredients"></div>
        </div>

        <div class="supply">
            <h3>② 뒤집개 · ③ 토핑</h3>
            <div class="items" id="tools"></div>
        </div>

    </div>

    <div class="help">
        반죽 → 재료 → 굽기 → 뒤집개 →
        반대쪽 굽기 → 접시 → 토핑 → 손님
    </div>

    <div class="overlay" id="overlay">
        <div class="panel">

            <div id="panel-icon"
                 style="font-size:58px">
                🍳
            </div>

            <h2 id="panel-title">
                오코노미야끼 가게
            </h2>

            <p id="panel-text">
                손님의 주문대로 오코노미야끼를 만들어 주세요!<br>
                반죽 → 재료 → 뒤집기 → 토핑 → 서빙<br>
                ❤️ 목숨 3개 · 총 5레벨
            </p>

            <button class="start"
                    id="start-button"
                    onclick="beginCountdown()">
                🎮 오코노미야끼 만들기
            </button>

        </div>
    </div>

    <div class="countdown" id="countdown">
        <span id="count-text">3</span>
    </div>

</div>

<script>

// ==========================================
// 기본 설정
// ==========================================

const CUSTOMER_IMAGES = __IMAGES__;
const BUBBLE_STYLE = __BUBBLE__;

const LEVEL_TIMES = [90, 120, 120, 150, 150];

const CUSTOMER_WAIT = [
    [40, 45],
    [30, 35],
    [22, 27],
    [15, 20],
    [10, 13]
];

const FIRST_COOK_MS = 2200;
const SECOND_COOK_MS = 2000;
const BURN_WAIT_MS = 4200;

const ingredients = [
    {
        name: "반죽",
        emoji: "🥣",
        type: "batter"
    },
    {
        name: "돼지고기",
        emoji: "🥩",
        type: "filling"
    },
    {
        name: "해산물",
        emoji: "🦐",
        type: "filling"
    },
    {
        name: "치즈",
        emoji: "🧀",
        type: "filling"
    }
];

const tools = [
    {
        name: "뒤집개",
        emoji: "🍴",
        type: "flip"
    },
    {
        name: "소스",
        emoji: "🍯",
        type: "topping"
    },
    {
        name: "마요네즈",
        emoji: "🥛",
        type: "topping"
    }
];

const fillings = ingredients.filter(
    x => x.type === "filling"
);

const toppings = tools.filter(
    x => x.type === "topping"
);

const el = id => document.getElementById(id);
const now = () => performance.now();

const pick = array =>
    array[Math.floor(Math.random() * array.length)];

const sleep = ms =>
    new Promise(resolve => setTimeout(resolve, ms));

let game = null;
let drag = null;
let highlighted = null;
let toastTimer = null;
let counting = false;


// ==========================================
// 알림 메시지
// ==========================================

function tell(message, type = "info") {
    const t = el("toast");

    t.className = "toast " + type;
    t.textContent = message;

    void t.offsetWidth;
    t.classList.add("show");

    clearTimeout(toastTimer);

    toastTimer = setTimeout(() => {
        t.classList.remove("show");
    }, 1800);
}


// ==========================================
// 손님 이미지
// ==========================================

function imageFor(number, expression) {
    return (
        CUSTOMER_IMAGES[`${number}_${expression}`] ||
        CUSTOMER_IMAGES[`${number}_normal`] ||
        ""
    );
}


// ==========================================
// 손님 생성 및 주문
// ==========================================

function newCustomer() {
    const [min, max] =
        CUSTOMER_WAIT[game.level - 1];

    return {
        character: Math.floor(Math.random() * 5) + 1,
        fill: pick(fillings),
        top: pick(toppings),
        born: now(),
        patience: (
            min + Math.random() * (max - min)
        ) * 1000,
        happyUntil: 0
    };
}

function orderText(c) {
    return (
        `${c.fill.emoji} ${c.fill.name} + ` +
        `${c.top.emoji} ${c.top.name}`
    );
}


// ==========================================
// 게임 시작 카운트다운
// ==========================================

async function beginCountdown() {
    if (counting) return;

    counting = true;

    el("overlay").classList.add("hidden");
    el("countdown").classList.add("show");

    for (const number of ["3", "2", "1"]) {
        el("count-text").textContent = number;
        await sleep(1000);
    }

    el("count-text").textContent = "START!";
    await sleep(600);

    el("countdown").classList.remove("show");

    counting = false;
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
        best: 0,
        served: 0,
        missed: 0,

        grills: Array.from(
            {length: 3},
            () => ({state: "empty"})
        ),

        plate: null,
        customers: [],
        ended: false
    };

    game.customers = Array.from(
        {length: 3},
        newCustomer
    );

    renderAll();

    tell(
        "영업 시작! 주문을 확인하세요!",
        "info"
    );
}


// ==========================================
// 상단 정보
// ==========================================

function updateHud() {
    if (!game) return;

    el("level").textContent = game.level;
    el("score").textContent = game.score;
    el("lives").textContent =
        "❤️".repeat(game.lives);
}


// ==========================================
// 사람 손님 3명 표시
// ==========================================

function renderCustomers() {
    if (!game) return;

    el("customers").innerHTML =
        game.customers.map((c, i) => `
            <div class="customer"
                 id="customer-${i}"
                 data-drop="customer"
                 data-index="${i}">

                <div class="bubble ${BUBBLE_STYLE}"
                     id="bubble-${i}">
                    ${orderText(c)}
                </div>

                <img class="avatar"
                     id="avatar-${i}"
                     src="${imageFor(c.character, "normal")}"
                     data-expression="normal"
                     draggable="false">

                <div class="customer-label"
                     id="label-${i}">
                    주문을 기다리는 중
                </div>

                <div class="patience">
                    <span id="patience-${i}"></span>
                </div>

            </div>
        `).join("");
}


// ==========================================
// 손님 표정과 대기 게이지
// ==========================================

function updateCustomers(t) {
    if (!game) return;

    game.customers.forEach((c, i) => {
        const avatar = el(`avatar-${i}`);
        const card = el(`customer-${i}`);
        const bar = el(`patience-${i}`);
        const label = el(`label-${i}`);
        const bubbleElement = el(`bubble-${i}`);

        if (!avatar || !card || !bar) return;

        if (c.happyUntil) {
            if (avatar.dataset.expression !== "happy") {
                avatar.src = imageFor(
                    c.character, "happy"
                );

                avatar.dataset.expression = "happy";
            }

            card.classList.add("happy");
            card.classList.remove("urgent");

            bubbleElement.textContent =
                "맛있어요! 감사합니다!";

            label.textContent = "주문 성공!";
            bar.style.width = "100%";
            bar.style.background = "#70b963";
            return;
        }

        const percent = Math.max(
            0,
            100 * (1 - (t - c.born) / c.patience)
        );

        const expression =
            percent <= 30 ? "angry" :
            percent <= 65 ? "waiting" :
            "normal";

        if (avatar.dataset.expression !== expression) {
            avatar.src = imageFor(
                c.character, expression
            );

            avatar.dataset.expression = expression;
        }

        card.classList.remove("happy");
        card.classList.toggle(
            "urgent",
            percent <= 30
        );

        bubbleElement.textContent = orderText(c);

        label.textContent =
            percent <= 30
                ? "너무 오래 기다렸어요!"
                : percent <= 65
                ? "조금 초조해요..."
                : "주문을 기다리는 중";

        bar.style.width = percent + "%";

        bar.style.background =
            percent <= 30 ? "#dc6753" :
            percent <= 65 ? "#e8b64a" :
            "#70b963";
    });
}


// ==========================================
// 철판
// ==========================================

function renderGrills() {
    if (!game) return;

    const messages = {
        empty: "반죽을 넣어 주세요",
        batter: "재료를 올려 주세요",
        cooking: "첫 번째 면 굽는 중",
        flip: "뒤집개를 사용하세요!",
        second: "두 번째 면 굽는 중",
        ready: "다 익었어요!",
        burnt: "음식이 탔어요!"
    };

    const icons = {
        empty: "⚫",
        batter: "🥣",
        cooking: "🟡",
        flip: "🍳",
        second: "🟤",
        ready: "🥞",
        burnt: "⚫"
    };

    el("grills").innerHTML =
        game.grills.map((g, i) => {

            const source =
                ["ready", "burnt"].includes(g.state)
                ? `
                    data-source="grill"
                    data-index="${i}"
                    data-emoji="🍳"
                    data-label="오코노미야끼"
                `
                : "";

            return `
                <div class="grill"
                     data-drop="grill"
                     data-index="${i}"
                     ${source}>

                    <div class="pancake">
                        ${icons[g.state]}
                    </div>

                    <strong>${i + 1}번 철판</strong>

                    <div class="bar">
                        <span id="cook-${i}"></span>
                    </div>

                    <small>
                        ${messages[g.state]}
                    </small>

                </div>
            `;
        }).join("");
}


// ==========================================
// 완성 접시
// ==========================================

function renderPlate() {
    const plate = el("plate");

    if (!game || !game.plate) {
        plate.innerHTML = "🍽️";
        plate.removeAttribute("data-source");
        plate.removeAttribute("data-emoji");
        plate.removeAttribute("data-label");

        el("plate-help").textContent =
            "익은 음식을 옮겨 주세요";
        return;
    }

    const p = game.plate;

    plate.innerHTML = `
        🍳
        <small>
            ${p.fill.name}
            ${p.top ? " + " + p.top.name : ""}
        </small>
    `;

    plate.dataset.source = "plate";
    plate.dataset.emoji = "🍳";
    plate.dataset.label = "완성된 음식";

    el("plate-help").textContent = p.top
        ? "손님에게 서빙하세요"
        : "토핑을 올려 주세요";
}


// ==========================================
// 재료와 도구
// ==========================================

function renderItems() {
    el("ingredients").innerHTML =
        ingredients.map((item, i) => `
            <div class="item"
                 data-source="ingredient"
                 data-index="${i}"
                 data-emoji="${item.emoji}"
                 data-label="${item.name}">

                <span>${item.emoji}</span>
                ${item.name}
            </div>
        `).join("");

    el("tools").innerHTML =
        tools.map((item, i) => `
            <div class="item"
                 data-source="tool"
                 data-index="${i}"
                 data-emoji="${item.emoji}"
                 data-label="${item.name}">

                <span>${item.emoji}</span>
                ${item.name}
            </div>
        `).join("");
}


function renderAll() {
    updateHud();
    renderCustomers();
    renderGrills();
    renderPlate();
    renderItems();
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
            `${message} 남은 목숨 ${game.lives}개`,
            "error"
        );
    }
}


// ==========================================
// 주문 서빙
// ==========================================

function serve(index) {
    const c = game.customers[index];
    const p = game.plate;

    if (!c || c.happyUntil) return;

    if (!p || !p.top) {
        tell(
            "토핑까지 완성한 음식을 서빙하세요!",
            "warning"
        );
        return;
    }

    const correct =
        p.fill.name === c.fill.name &&
        p.top.name === c.top.name;

    game.plate = null;
    renderPlate();

    if (correct) {
        game.combo++;
        game.best = Math.max(
            game.best,
            game.combo
        );

        game.served++;

        game.score += 100 + Math.min(
            game.combo * 10,
            100
        );

        c.happyUntil = now() + 850;

        updateHud();
        updateCustomers(now());

        tell(
            "✅ 주문 성공! 맛있게 드세요!",
            "success"
        );
    } else {
        game.missed++;

        loseLife("❌ 주문이 틀렸어요!");

        if (!game.ended) {
            game.customers[index] = newCustomer();
            renderCustomers();
        }
    }
}


// ==========================================
// 재료 드롭 및 조리
// ==========================================

function handleDrop(kind, index, target, targetIndex) {
    if (!game || game.ended) return;

    // 1. 반죽과 재료

    if (
        kind === "ingredient" &&
        target === "grill"
    ) {
        const item = ingredients[index];
        const g = game.grills[targetIndex];

        if (!g) return;

        if (
            item.type === "batter" &&
            g.state === "empty"
        ) {
            game.grills[targetIndex] = {
                state: "batter"
            };

            renderGrills();

            tell(
                "반죽 완료! 재료를 올려 주세요.",
                "info"
            );
            return;
        }

        if (
            item.type === "filling" &&
            g.state === "batter"
        ) {
            game.grills[targetIndex] = {
                state: "cooking",
                fill: item,
                since: now()
            };

            renderGrills();

            tell(
                "첫 번째 면을 굽고 있어요!",
                "info"
            );
            return;
        }

        tell(
            "반죽 → 재료 순서로 조리해 주세요!",
            "warning"
        );
        return;
    }

    // 2. 뒤집개

    if (
        kind === "tool" &&
        target === "grill"
    ) {
        const tool = tools[index];
        const g = game.grills[targetIndex];

        if (
            tool.type !== "flip" ||
            !g ||
            g.state !== "flip"
        ) {
            tell(
                "뒤집을 타이밍에 뒤집개를 사용하세요!",
                "warning"
            );
            return;
        }

        g.state = "second";
        g.since = now();

        renderGrills();

        tell(
            "✅ 뒤집기 성공! 반대쪽을 굽습니다.",
            "success"
        );
        return;
    }

    // 3. 철판 → 접시

    if (
        kind === "grill" &&
        target === "plate"
    ) {
        const g = game.grills[index];

        if (!g || g.state !== "ready") {
            tell(
                "다 익은 음식만 접시에 담을 수 있어요!",
                "warning"
            );
            return;
        }

        if (game.plate) {
            tell(
                "접시가 이미 차 있어요!",
                "warning"
            );
            return;
        }

        game.plate = {
            fill: g.fill,
            top: null
        };

        game.grills[index] = {
            state: "empty"
        };

        renderGrills();
        renderPlate();

        tell(
            "✅ 접시에 담았어요! 토핑을 올려 주세요.",
            "success"
        );
        return;
    }

    // 4. 토핑

    if (
        kind === "tool" &&
        target === "plate"
    ) {
        const tool = tools[index];

        if (tool.type !== "topping") {
            tell(
                "접시에는 토핑을 올려 주세요!",
                "warning"
            );
            return;
        }

        if (!game.plate) {
            tell(
                "먼저 음식을 접시에 담아 주세요!",
                "warning"
            );
            return;
        }

        if (game.plate.top) {
            tell(
                "이미 토핑을 올렸어요!",
                "warning"
            );
            return;
        }

        game.plate.top = tool;
        renderPlate();

        tell(
            "토핑 완료! 손님에게 서빙하세요.",
            "success"
        );
        return;
    }

    // 5. 서빙

    if (
        kind === "plate" &&
        target === "customer"
    ) {
        serve(targetIndex);
        return;
    }

    // 6. 휴지통

    if (target === "trash") {
        if (kind === "plate") {
            game.plate = null;
            renderPlate();

            tell(
                "음식을 버렸습니다.",
                "info"
            );
            return;
        }

        if (kind === "grill") {
            game.grills[index] = {
                state: "empty"
            };

            renderGrills();

            tell(
                "철판을 비웠습니다.",
                "info"
            );
            return;
        }
    }

    tell(
        "올바른 위치에 재료를 놓아 주세요!",
        "warning"
    );
}


// ==========================================
// 드래그 앤 드롭
// ==========================================

function moveGhost(e) {
    if (!drag) return;

    drag.ghost.style.left =
        (e.clientX + 12) + "px";

    drag.ghost.style.top =
        (e.clientY + 12) + "px";

    if (highlighted) {
        highlighted.classList.remove("drop-over");
    }

    highlighted = document.elementFromPoint(
        e.clientX,
        e.clientY
    )?.closest("[data-drop]");

    if (highlighted) {
        highlighted.classList.add("drop-over");
    }
}


document.addEventListener("pointerdown", e => {
    if (!game || game.ended || drag) return;

    const source = e.target.closest(
        "[data-source]"
    );

    if (!source) return;

    e.preventDefault();

    const ghost = document.createElement("div");
    ghost.className = "ghost";

    ghost.innerHTML = `
        ${source.dataset.emoji || "🍳"}
        <small>
            ${source.dataset.label || ""}
        </small>
    `;

    document.body.appendChild(ghost);

    drag = {
        pointerId: e.pointerId,
        source,
        kind: source.dataset.source,
        index: Number(
            source.dataset.index || 0
        ),
        ghost
    };

    source.classList.add("dragging-original");
    moveGhost(e);
});


document.addEventListener(
    "pointermove",
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

    const d = drag;

    const target = document.elementFromPoint(
        e.clientX,
        e.clientY
    )?.closest("[data-drop]");

    d.ghost.remove();

    if (d.source.isConnected) {
        d.source.classList.remove(
            "dragging-original"
        );
    }

    if (highlighted) {
        highlighted.classList.remove(
            "drop-over"
        );
    }

    highlighted = null;
    drag = null;

    if (target) {
        handleDrop(
            d.kind,
            d.index,
            target.dataset.drop,
            Number(
                target.dataset.index || 0
            )
        );
    }
}


document.addEventListener(
    "pointerup",
    releaseDrag
);


document.addEventListener(
    "pointercancel",
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
                "dragging-original"
            );
        }

        if (highlighted) {
            highlighted.classList.remove(
                "drop-over"
            );
        }

        drag = null;
        highlighted = null;
    }
);


// ==========================================
// 레벨 전환
// ==========================================

function nextLevel() {
    if (!game || game.ended) return;

    if (game.level === 5) {
        endGame(true);
        return;
    }

    game.level++;
    game.levelStart = now();

    game.grills = Array.from(
        {length: 3},
        () => ({state: "empty"})
    );

    game.plate = null;

    game.customers = Array.from(
        {length: 3},
        newCustomer
    );

    renderAll();

    tell(
        `⭐ LEVEL ${game.level} 시작!`,
        "info"
    );
}


// ==========================================
// 게임 종료
// ==========================================

function endGame(won) {
    if (!game || game.ended) return;

    game.ended = true;

    el("panel-icon").textContent =
        won ? "🏆" : "💔";

    el("panel-title").textContent =
        won ? "최종 승리!" : "게임 오버!";

    el("panel-text").innerHTML = `
        도달 레벨: ${game.level}/5<br>
        성공한 주문: ${game.served}개<br>
        최종 점수: ${game.score}점<br>
        최고 콤보: ${game.best}회<br>
        놓친 주문: ${game.missed}개
    `;

    el("start-button").textContent =
        "🔄 다시 도전하기";

    el("overlay").classList.remove("hidden");
}


// ==========================================
// 게임 타이머
// ==========================================

function tick() {
    if (!game || game.ended) return;

    const t = now();

    const remaining =
        LEVEL_TIMES[game.level - 1] -
        (t - game.levelStart) / 1000;

    el("time").textContent = Math.max(
        0,
        Math.ceil(remaining)
    );

    if (remaining <= 0) {
        nextLevel();
        return;
    }

    // 조리 상태 변경

    let grillChanged = false;

    game.grills.forEach(g => {
        if (![
            "cooking", "flip",
            "second", "ready"
        ].includes(g.state)) {
            return;
        }

        const passed = t - g.since;

        if (
            g.state === "cooking" &&
            passed >= FIRST_COOK_MS
        ) {
            g.state = "flip";
            g.since = t;
            grillChanged = true;
        }

        if (
            g.state === "second" &&
            passed >= SECOND_COOK_MS
        ) {
            g.state = "ready";
            g.since = t;
            grillChanged = true;
        }

        if (
            ["flip", "ready"].includes(g.state) &&
            passed >= BURN_WAIT_MS
        ) {
            g.state = "burnt";

            game.score = Math.max(
                0,
                game.score - 10
            );

            game.combo = 0;

            updateHud();
            grillChanged = true;

            tell(
                "🔥 오코노미야끼가 탔어요! -10점",
                "error"
            );
        }
    });

    if (grillChanged) {
        renderGrills();
    }

    // 조리 진행 게이지

    game.grills.forEach((g, i) => {
        const bar = el(`cook-${i}`);
        if (!bar) return;

        const passed = g.since
            ? t - g.since
            : 0;

        const percent =
            g.state === "cooking"
                ? Math.min(
                    100,
                    passed / FIRST_COOK_MS * 100
                )
            : g.state === "second"
                ? Math.min(
                    100,
                    passed / SECOND_COOK_MS * 100
                )
            : ["flip", "ready", "burnt"].includes(
                g.state
            )
                ? 100
                : 0;

        bar.style.width = percent + "%";

        bar.style.background =
            g.state === "burnt"
                ? "#9d5950"
                : "#efc456";
    });

    // 손님 대기 시간

    let customersChanged = false;

    for (
        let i = 0;
        i < game.customers.length;
        i++
    ) {
        const c = game.customers[i];

        if (c.happyUntil) {
            if (t >= c.happyUntil) {
                game.customers[i] = newCustomer();
                customersChanged = true;
            }

            continue;
        }

        if (t - c.born >= c.patience) {
            game.missed++;

            loseLife(
                "❌ 손님이 기다리다 떠났어요!"
            );

            if (game.ended) return;

            game.customers[i] = newCustomer();
            customersChanged = true;
        }
    }

    if (customersChanged) {
        renderCustomers();
    }

    updateCustomers(t);
}


// ==========================================
// 시작 전 화면
// ==========================================

function initializeScreen() {
    renderItems();

    el("customers").innerHTML =
        Array.from(
            {length: 3},
            (_, i) => `
                <div class="customer">
                    <div class="bubble ${BUBBLE_STYLE}">
                        게임 시작 후 주문이 나타나요!
                    </div>

                    <img class="avatar"
                         src="${imageFor(i + 1, "normal")}"
                         draggable="false">

                    <div class="customer-label">
                        영업 준비 중
                    </div>

                    <div class="patience">
                        <span></span>
                    </div>
                </div>
            `
        ).join("");

    el("grills").innerHTML =
        Array.from(
            {length: 3},
            (_, i) => `
                <div class="grill">
                    <div class="pancake">⚫</div>

                    <strong>
                        ${i + 1}번 철판
                    </strong>

                    <div class="bar"></div>

                    <small>
                        게임을 시작해 주세요
                    </small>
                </div>
            `
        ).join("");

    renderPlate();
}


// ==========================================
// 실행
// ==========================================

initializeScreen();

setInterval(tick, 100);

</script>
</body>
</html>
"""

# ==========================================
# Python → 게임 설정 전달
# ==========================================

GAME_HTML = GAME_HTML.replace(
    "__IMAGES__",
    json.dumps(customer_images)
)

GAME_HTML = GAME_HTML.replace(
    "__BUBBLE__",
    json.dumps(bubble)
)

# ==========================================
# 게임 출력
# ==========================================


# ==========================================
# 배경 꾸미기에서 선택한 이미지 적용
# ==========================================

BACKGROUND_FILES = {
    "🌸 벚꽃 축제": "bg_spring.png",
    "🎆 여름 축제": "bg_summer.png",
    "🍁 가을 야시장": "bg_autumn.png",
    "❄️ 겨울 포장마차": "bg_winter.png",
}

selected_background = st.session_state.get(
    "saved_background",
    "🌸 벚꽃 축제"
)

background_filename = BACKGROUND_FILES.get(
    selected_background,
    "bg_spring.png"
)

background_path = (
    Path(__file__).resolve().parent.parent
    / background_filename
)

if background_path.is_file():
    encoded = base64.b64encode(
        background_path.read_bytes()
    ).decode("ascii")

    background_url = "data:image/png;base64," + encoded

    background_css = """
    <style>
    .game {
        background-image: url("__BACKGROUND_URL__") !important;
        background-position: center center !important;
        background-size: cover !important;
        background-repeat: no-repeat !important;
    }
    </style>
    """

    background_css = background_css.replace(
        "__BACKGROUND_URL__",
        background_url
    )

    GAME_HTML = GAME_HTML.replace(
        "</head>",
        background_css + "\n</head>",
        1
    )
else:
    st.warning(
        f"배경 이미지 파일을 찾을 수 없어요: "
        f"{background_filename}"
    )

components.html(
    GAME_HTML,
    height=700,
    scrolling=False,
)
