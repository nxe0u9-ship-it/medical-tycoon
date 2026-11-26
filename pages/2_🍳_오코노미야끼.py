
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json

# ==========================================
# 오코노미야끼 게임
# ==========================================

ROOT = Path(__file__).resolve().parent.parent

CUSTOMER_STYLES = {
    "🎆 축제 손님": "festival",
    "🎒 학생": "student",
    "💼 직장인": "office",
    "👕 캐주얼": "casual",
}

BUBBLE_STYLES = {
    "💭 둥근 말풍선": "round",
    "✨ 강조 말풍선": "comic",
    "💥 코믹 말풍선": "comic",
    "▫️ 심플 말풍선": "simple",
}

BACKGROUNDS = {
    "🌸 벚꽃 축제": "bg_spring.png",
    "🎆 여름 축제": "bg_summer.png",
    "🍁 가을 야시장": "bg_autumn.png",
    "❄️ 겨울 포장마차": "bg_winter.png",
}

customer_theme = CUSTOMER_STYLES.get(
    st.session_state.get(
        "saved_customer_style", "🎆 축제 손님"
    ),
    "festival"
)

bubble_theme = BUBBLE_STYLES.get(
    st.session_state.get(
        "saved_bubble_style", "💭 둥근 말풍선"
    ),
    "round"
)

background_file = BACKGROUNDS.get(
    st.session_state.get(
        "saved_background", "🌸 벚꽃 축제"
    ),
    "bg_spring.png"
)


def to_data_url(path):
    if not path.is_file():
        return ""

    encoded = base64.b64encode(
        path.read_bytes()
    ).decode("ascii")

    return "data:image/png;base64," + encoded


# 손님 PNG 이미지
customer_images = {}
customer_folder = (
    ROOT / "assets" / "customers" / customer_theme
)

for number in range(1, 6):
    for mood in ("normal", "waiting", "angry", "happy"):
        filename = (
            f"{customer_theme}_{number:02d}_{mood}.png"
        )
        customer_images[f"{number}_{mood}"] = to_data_url(
            customer_folder / filename
        )

# 재료·도구 PNG 이미지
ingredient_files = [
    "batter.png",
    "pork.png",
    "seafood.png",
    "cheese.png",
    "spatula.png",
    "sauce.png",
    "mayonnaise.png",
]

ingredient_images = {
    filename: to_data_url(
        ROOT / "assets" / "ingredients" / filename
    )
    for filename in ingredient_files
}

background_url = to_data_url(
    ROOT / background_file
)

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
    border: none !important;
}
</style>
""")

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width,initial-scale=1">

<style>
* { box-sizing: border-box; }

html, body {
    margin: 0;
    height: 100%;
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
        #88a0c6, #f2c1aa, #f6d5a0
    );
    background-size: cover;
    background-position: center;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    height: 45px;
}

.logo, .stat, .sign {
    border-radius: 12px;
    font-weight: 900;
    text-align: center;
}

.logo {
    padding: 8px 12px;
    background: #fff0ce;
    border: 3px solid #a85d37;
    color: #964b30;
    white-space: nowrap;
}

.stats {
    display: flex;
    gap: 6px;
}

.stat {
    min-width: 68px;
    padding: 5px 8px;
    background: #784d3d;
    color: white;
    border: 2px solid #f6d6a0;
}

.stat small {
    display: block;
    font-size: 10px;
    color: #ffe2bd;
}

.stat.timer { background: #c8584c; }

.notice-area {
    height: 43px;
    margin: 2px 0 4px;
    display: grid;
    place-items: center;
    pointer-events: none;
}

.toast {
    max-width: 90%;
    padding: 8px 20px;
    border: 2px solid #fff3d9;
    border-radius: 12px;
    background: #8b5a3c;
    color: white;
    font-size: 13px;
    font-weight: 900;
    text-align: center;
    opacity: 0;
    transition: opacity .2s;
}

.toast.show { opacity: 1; }
.toast.success { background: #269957; }
.toast.error { background: #d74646; }
.toast.warning {
    background: #e8a02f;
    color: #493116;
}

.sign {
    width: fit-content;
    margin: 0 auto 7px;
    padding: 5px 24px;
    background: #934a35;
    color: #fff6dc;
    border: 3px solid #f2ca87;
    font-size: 16px;
}

.customers {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    width: 100%;
    max-width: 1050px;
    height: 150px;
    margin: 0 auto 8px;
    gap: 8px;
}

.customer {
    min-width: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    padding: 0 3px;
    text-align: center;
}

.bubble {
    position: relative;
    z-index: 2;
    width: 96%;
    min-height: 35px;
    margin-bottom: 5px;
    padding: 5px;
    display: grid;
    place-items: center;
    font-size: 11px;
    font-weight: 900;
    background: #fffdf5;
}

.bubble.round {
    border: 3px solid #d9ab83;
    border-radius: 18px;
}

.bubble.comic {
    border: 3px solid #d28b54;
    border-radius: 12px;
    background: #fff3bd;
    box-shadow: 3px 3px #e7b06e;
}

.bubble.simple {
    border: 2px solid #d8c1aa;
    border-radius: 9px;
}

.avatar {
    width: min(130px, 100%);
    height: 87px;
    object-fit: contain;
    object-position: center bottom;
    pointer-events: none;
}

.customer-label {
    margin: 1px 0 3px;
    font-size: 10px;
    font-weight: 900;
}

.patience {
    width: 74%;
    height: 8px;
    background: #e4ccb0;
    border: 2px solid #b8835c;
    border-radius: 20px;
    overflow: hidden;
}

.patience span {
    display: block;
    height: 100%;
    width: 100%;
    background: #70b963;
}

.customer.urgent .bubble {
    border-color: #d9655b;
}

.counter {
    max-width: 1200px;
    margin: auto;
    padding: 8px;
    border: 5px solid #8e5334;
    border-radius: 20px;
    background: repeating-linear-gradient(
        0deg, #b87648 0 20px, #c88958 20px 40px
    );
    box-shadow: 0 5px #643b28;
}

.counter h3 {
    margin: 0 0 6px;
    color: #fff5de;
    font-size: 15px;
    text-align: center;
}

.kitchen {
    display: grid;
    grid-template-columns:
        minmax(0, 1.6fr) minmax(260px, 1fr);
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
    min-width: 0;
    min-height: 133px;
    padding: 5px 3px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 5px;
    background: #28282c;
    color: #fff5da;
    border: 2px solid #686268;
    border-radius: 13px;
    text-align: center;
}

.grill.ready { border-color: #62b780; }
.grill.burnt { border-color: #87493d; }
.grill.urgent { border-color: #e76b5d; }

.grill strong { font-size: 11px; }
.grill small {
    font-size: 10px;
    font-weight: 900;
}

.pancake {
    display: grid;
    place-items: center;
    width: 70px;
    height: 58px;
    font-size: 34px;
    pointer-events: none;
}

.bar {
    width: 80%;
    height: 9px;
    background: #151515;
    border: 1px solid #555;
    border-radius: 20px;
    overflow: hidden;
}

.bar span {
    display: block;
    height: 100%;
    width: 0%;
    background: #efc456;
}

.right {
    display: flex;
    flex-direction: column;
    gap: 7px;
    min-width: 0;
}

.plate-zone {
    flex: 1;
    padding: 6px;
    background: #fff1d9;
    border: 3px solid #e5bd8f;
    border-radius: 13px;
    text-align: center;
}

.plate-zone strong { font-size: 12px; }
#plate-help { font-size: 10px; }

.plates {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 5px;
    margin: 5px auto;
}

.plate {
    position: relative;
    min-height: 64px;
    min-width: 0;
    padding: 5px 2px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3px;
    background: radial-gradient(
        circle, white 0 48%,
        #b7d6e2 50% 60%, white 62%
    );
    border: 2px solid #c8b5a2;
    border-radius: 12px;
    font-size: 21px;
    font-weight: 900;
}

.plate.ready { border-color: #79ad6a; }

.plate small {
    font-size: 9px;
    overflow-wrap: anywhere;
}

.plate-number {
    position: absolute;
    top: 2px;
    left: 4px;
    font-size: 9px;
}

.trash {
    min-height: 35px;
    padding: 5px;
    display: grid;
    place-items: center;
    background: #f9d6c7;
    border: 3px solid #e5bd8f;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 900;
}

.supplies {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 9px;
    max-width: 1200px;
    margin: 10px auto 7px;
}

.supply {
    padding: 7px;
    background: #fff1da;
    border: 3px solid #be8454;
    border-radius: 15px;
    min-width: 0;
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
    background: #fffaf1;
    border: 2px solid #e5c49a;
    border-radius: 11px;
    text-align: center;
    font-size: 11px;
    font-weight: 900;
}

.ingredient-art {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2px;
    min-height: 39px;
}

.ingredient-art img {
    width: min(45%, 40px);
    height: 38px;
    object-fit: contain;
    pointer-events: none;
}

.ingredient-art img:only-child {
    width: 45px;
}

.fallback {
    font-size: 26px;
}

.help {
    max-width: 1200px;
    margin: auto;
    padding: 6px;
    background: #fff4da;
    border: 2px solid #d8ab75;
    border-radius: 10px;
    text-align: center;
    font-size: 11px;
    font-weight: 800;
}

[data-source] {
    cursor: grab;
    touch-action: none;
    user-select: none;
}

.dragging-original { opacity: .45; }

.drop-over {
    outline: 4px solid #ffe47c;
    outline-offset: 2px;
}

.ghost {
    position: fixed;
    z-index: 1000;
    pointer-events: none;
    padding: 8px;
    background: #fff8e7;
    border: 3px solid #d9a16b;
    border-radius: 14px;
    box-shadow: 0 5px 12px #0004;
    text-align: center;
    font-size: 24px;
}

.ghost .ingredient-art img {
    width: 45px;
    height: 45px;
}

.ghost small {
    display: block;
    font-size: 11px;
}

.overlay, .countdown {
    position: absolute;
    inset: 0;
    align-items: center;
    justify-content: center;
    padding: 15px;
    background: #241b20bc;
}

.overlay {
    z-index: 35;
    display: flex;
}

.overlay.hidden { display: none; }

.panel {
    width: min(460px, 95%);
    padding: 30px 20px;
    border: 6px solid #bc7950;
    border-radius: 25px;
    background: #fff4d9;
    text-align: center;
    box-shadow: 0 10px #7c4d37;
}

.panel h2 { color: #954a33; }

.panel p {
    font-size: 15px;
    font-weight: 900;
    line-height: 1.8;
}

.start {
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
    z-index: 40;
    display: none;
    flex-direction: column;
    gap: 12px;
    color: #fff2bc;
    text-align: center;
}

.countdown.show { display: flex; }

.count-level {
    font-size: 42px;
    font-weight: 900;
}

.count-lives {
    padding: 8px 20px;
    background: #fff3d9;
    color: #b44d47;
    border: 3px solid #e3a36d;
    border-radius: 15px;
    font-size: 21px;
    font-weight: 900;
}

.count-number {
    font-size: 105px;
    font-weight: 900;
}

@media (max-width: 900px) {
    .game { padding: 6px; }
    .logo { font-size: 12px; }
    .stat {
        min-width: 48px;
        padding: 4px;
        font-size: 12px;
    }
    .stat small { font-size: 8px; }
    .bubble { font-size: 10px; }
    .avatar { width: min(110px, 100%); }
    .kitchen {
        grid-template-columns:
            minmax(0, 1.3fr) minmax(205px, 1fr);
    }
    .grills { gap: 3px; padding: 4px; }
    .item { font-size: 10px; }
    .ingredient-art img { height: 32px; }
    .plate { font-size: 17px; }
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
                <span id="time">60</span>초
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
        <div class="toast" id="toast"></div>
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
                <div class="plate-zone">
                    <strong>🍽️ 완성 접시 3개</strong>
                    <div class="plates" id="plates"></div>
                    <small id="plate-help">
                        익은 오코노미야끼를
                        접시에 올려 주세요
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
            <h3>① 반죽과 재료</h3>
            <div class="items" id="ingredients"></div>
        </div>
        <div class="supply">
            <h3>② 뒤집개 · ③ 토핑</h3>
            <div class="items" id="tools"></div>
        </div>
    </div>

    <div class="help">
        반죽 → 재료 → 앞면 굽기 →
        뒤집개 → 뒷면 굽기 →
        접시 → 토핑 → 손님
    </div>

    <div class="overlay" id="overlay">
        <div class="panel">
            <div id="panel-icon"
                 style="font-size:58px">🍳</div>
            <h2 id="panel-title">
                오코노미야끼 가게
            </h2>
            <p id="panel-text">
                손님의 주문대로 만들어 주세요!<br>
                반죽 → 재료 → 앞면 → 뒤집기 → 뒷면<br>
                접시 → 토핑 → 서빙<br>
                ❤️ 목숨 3개 · 5레벨 도전<br>
                뒤집기 전과 완성 후에는
                각각 8초 안에 옮겨 주세요.<br>
                레벨이 바뀌면 목숨이 회복돼요.
            </p>
            <button class="start"
                    id="start-button"
                    onclick="beginCountdown()">
                🎮 오코노미야끼 만들기
            </button>
        </div>
    </div>

    <div class="countdown" id="countdown">
        <div class="count-level" id="count-level">
            LEVEL 1
        </div>
        <div class="count-lives" id="count-lives">
            ❤️ 목숨 3개
        </div>
        <div class="count-number" id="count-text">
            3
        </div>
    </div>
</div>

<script>
const CUSTOMER_IMAGES = __CUSTOMERS__;
const INGREDIENT_IMAGES = __INGREDIENTS__;
const BUBBLE_STYLE = __BUBBLE__;

const LEVEL_TIMES = [60, 70, 80, 90, 100];
const CUSTOMER_COUNT = [3, 3, 3, 4, 4];

const CUSTOMER_WAIT = [
    [40, 45],
    [30, 35],
    [22, 27],
    [15, 20],
    [10, 13]
];

const FIRST_COOK_MS = 2200;
const SECOND_COOK_MS = 2000;
const BURN_WAIT_MS = 8000;
const MAX_LIVES = 3;

const ingredients = [
    {
        id: "batter",
        name: "반죽",
        emoji: "🥣",
        type: "batter",
        images: ["batter.png"]
    },
    {
        id: "pork",
        name: "돼지고기",
        emoji: "🥩",
        type: "filling",
        images: ["pork.png"]
    },
    {
        id: "seafood",
        name: "해산물",
        emoji: "🦐",
        type: "filling",
        images: ["seafood.png"]
    },
    {
        id: "cheese",
        name: "치즈",
        emoji: "🧀",
        type: "filling",
        images: ["cheese.png"]
    }
];

const tools = [
    {
        id: "flip",
        name: "뒤집개",
        emoji: "🍴",
        type: "flip",
        images: ["spatula.png"]
    },
    {
        id: "sauce",
        name: "소스",
        emoji: "🍯",
        type: "topping",
        images: ["sauce.png"]
    },
    {
        id: "mayonnaise",
        name: "마요네즈",
        emoji: "🥛",
        type: "topping",
        images: ["mayonnaise.png"]
    }
];

const fillings = ingredients.filter(
    item => item.type === "filling"
);

const toppingOptions = tools.filter(
    item => item.type === "topping"
);

const el = id => document.getElementById(id);
const now = () => performance.now();
const sleep = ms =>
    new Promise(resolve => setTimeout(resolve, ms));

const pick = array =>
    array[Math.floor(Math.random() * array.length)];

let game = null;
let drag = null;
let highlighted = null;
let counting = false;
let toastTimer = null;

function art(filenames, fallback = "🍳") {
    const images = filenames
        .filter(name => INGREDIENT_IMAGES[name])
        .map(name =>
            `<img src="${INGREDIENT_IMAGES[name]}"
                  alt="" draggable="false">`
        );

    if (images.length === 0) {
        return `<span class="fallback">${fallback}</span>`;
    }

    return images.join("");
}

function artMarkup(filenames, fallback) {
    return `
        <span class="ingredient-art">
            ${art(filenames, fallback)}
        </span>
    `;
}

function imageFor(number, mood) {
    return (
        CUSTOMER_IMAGES[`${number}_${mood}`] ||
        CUSTOMER_IMAGES[`${number}_normal`] ||
        ""
    );
}

function tell(message, type = "info") {
    const box = el("toast");
    box.className = `toast ${type} show`;
    box.textContent = message;

    clearTimeout(toastTimer);
    toastTimer = setTimeout(
        () => box.classList.remove("show"),
        1800
    );
}

function newCustomer() {
    const [min, max] =
        CUSTOMER_WAIT[game.level - 1];

    return {
        character:
            Math.floor(Math.random() * 5) + 1,
        fill: pick(fillings),
        top: pick(toppingOptions),
        born: now(),
        patience: (
            min + Math.random() * (max - min)
        ) * 1000,
        happyUntil: 0
    };
}

function orderText(customer) {
    return (
        `${customer.fill.emoji} ` +
        `${customer.fill.name} + ` +
        `${customer.top.emoji} ` +
        `${customer.top.name}`
    );
}

function createNewGame() {
    game = {
        level: 1,
        levelStart: 0,
        lives: MAX_LIVES,
        score: 0,
        combo: 0,
        best: 0,
        served: 0,
        missed: 0,
        grills: Array.from(
            {length: 3},
            () => ({state: "empty"})
        ),
        plates: [null, null, null],
        customers: [],
        ended: false,
        paused: true
    };
}

async function beginCountdown() {
    if (counting) return;

    createNewGame();
    await runLevelCountdown(false);
}

async function runLevelCountdown(showIntro) {
    if (counting || !game || game.ended) return;

    counting = true;
    game.paused = true;

    el("overlay").classList.add("hidden");
    el("countdown").classList.add("show");

    el("count-level").textContent =
        `⭐ LEVEL ${game.level}`;

    el("count-lives").textContent =
        `❤️ 목숨 ${game.lives}개`;

    if (showIntro) {
        el("count-text").textContent = "다음 레벨!";
        await sleep(1200);
    }

    for (const number of ["3", "2", "1"]) {
        el("count-text").textContent = number;
        await sleep(1000);
    }

    el("count-text").textContent = "START!";
    await sleep(600);

    game.levelStart = now();
    game.customers = Array.from(
        {length: CUSTOMER_COUNT[game.level - 1]},
        newCustomer
    );

    game.paused = false;
    renderAll();
    updateGrillBars(now());

    el("time").textContent =
        LEVEL_TIMES[game.level - 1];

    el("countdown").classList.remove("show");
    counting = false;

    tell(
        `⭐ ${game.level}레벨 영업 시작!`,
        "info"
    );
}

function updateHud() {
    if (!game) return;

    el("level").textContent = game.level;
    el("score").textContent = game.score;
    el("lives").textContent =
        "❤️".repeat(game.lives);
}

function renderCustomers() {
    if (!game) return;

    const area = el("customers");

    area.style.gridTemplateColumns =
        `repeat(${game.customers.length}, minmax(0, 1fr))`;

    area.innerHTML = game.customers
        .map((customer, i) => `
            <div class="customer"
                 id="customer-${i}"
                 data-drop="customer"
                 data-index="${i}">
                <div class="bubble ${BUBBLE_STYLE}"
                     id="bubble-${i}">
                    ${orderText(customer)}
                </div>
                <img class="avatar"
                     id="avatar-${i}"
                     src="${imageFor(
                         customer.character, "normal"
                     )}"
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

function updateCustomers(t) {
    if (!game) return;

    game.customers.forEach((customer, i) => {
        const avatar = el(`avatar-${i}`);
        const card = el(`customer-${i}`);
        const bar = el(`patience-${i}`);
        const label = el(`label-${i}`);
        const bubble = el(`bubble-${i}`);

        if (!avatar || !card || !bar) return;

        if (customer.happyUntil) {
            if (avatar.dataset.expression !== "happy") {
                avatar.src = imageFor(
                    customer.character, "happy"
                );
                avatar.dataset.expression = "happy";
            }

            card.classList.remove("urgent");
            bubble.textContent = "맛있어요! 감사합니다!";
            label.textContent = "주문 성공!";
            bar.style.width = "100%";
            bar.style.background = "#70b963";
            return;
        }

        const percent = Math.max(
            0,
            100 * (
                1 -
                (t - customer.born) / customer.patience
            )
        );

        const mood =
            percent <= 30 ? "angry" :
            percent <= 65 ? "waiting" : "normal";

        if (avatar.dataset.expression !== mood) {
            avatar.src = imageFor(
                customer.character, mood
            );
            avatar.dataset.expression = mood;
        }

        card.classList.toggle(
            "urgent", percent <= 30
        );

        bubble.textContent = orderText(customer);

        label.textContent =
            percent <= 30
                ? "너무 오래 기다렸어요!"
                : percent <= 65
                ? "기다림이 길어지고 있어요..."
                : "주문을 기다리는 중";

        bar.style.width = percent + "%";
        bar.style.background =
            percent <= 30 ? "#dc6753" :
            percent <= 65 ? "#e8b64a" :
            "#70b963";
    });
}

function renderGrills() {
    if (!game) return;

    const icons = {
        empty: "⚫",
        batter: "🥣",
        cooking: "🟡",
        flip: "🍳",
        second: "🟤",
        ready: "🍳",
        burnt: "⚫"
    };

    const messages = {
        empty: "반죽을 넣어 주세요",
        batter: "재료를 올려 주세요",
        cooking: "앞면 굽는 중",
        flip: "뒤집개를 사용하세요!",
        second: "뒷면 굽는 중",
        ready: "다 익었어요!",
        burnt: "음식이 탔어요!"
    };

    el("grills").innerHTML = game.grills
        .map((grill, i) => {
            const source = (
                grill.state === "ready" ||
                grill.state === "burnt"
            ) ? `
                data-source="grill"
                data-index="${i}"
                data-label="오코노미야끼"
                data-emoji="🍳"
            ` : "";

            return `
                <div class="grill ${grill.state}"
                     id="grill-${i}"
                     data-drop="grill"
                     data-index="${i}"
                     ${source}>
                    <div class="pancake">
                        ${icons[grill.state]}
                    </div>
                    <strong>${i + 1}번 철판</strong>
                    <div class="bar">
                        <span id="cook-${i}"></span>
                    </div>
                    <small id="grill-status-${i}">
                        ${messages[grill.state]}
                    </small>
                </div>
            `;
        }).join("");
}

function updateGrillBars(t) {
    if (!game) return;

    game.grills.forEach((grill, i) => {
        const bar = el(`cook-${i}`);
        const status = el(`grill-status-${i}`);
        const card = el(`grill-${i}`);

        if (!bar || !status) return;

        const elapsed = grill.since
            ? t - grill.since
            : 0;

        let percent = 0;
        let color = "#efc456";
        let message = "반죽을 넣어 주세요";

        if (grill.state === "batter") {
            message = "재료를 올려 주세요";
        }

        else if (grill.state === "cooking") {
            const remaining = Math.max(
                0, FIRST_COOK_MS - elapsed
            );

            percent = Math.min(
                100,
                elapsed / FIRST_COOK_MS * 100
            );

            message =
                `앞면 익기까지 ` +
                `${(remaining / 1000).toFixed(1)}초`;
        }

        else if (grill.state === "flip") {
            const remaining = Math.max(
                0, BURN_WAIT_MS - elapsed
            );

            percent =
                remaining / BURN_WAIT_MS * 100;

            message =
                `뒤집기! 타기까지 ` +
                `${(remaining / 1000).toFixed(1)}초`;

            color = remaining <= 1500
                ? "#d9534f"
                : "#f0a43a";
        }

        else if (grill.state === "second") {
            const remaining = Math.max(
                0, SECOND_COOK_MS - elapsed
            );

            percent = Math.min(
                100,
                elapsed / SECOND_COOK_MS * 100
            );

            message =
                `뒷면 익기까지 ` +
                `${(remaining / 1000).toFixed(1)}초`;
        }

        else if (grill.state === "ready") {
            const remaining = Math.max(
                0, BURN_WAIT_MS - elapsed
            );

            percent =
                remaining / BURN_WAIT_MS * 100;

            message =
                `타기까지 ` +
                `${(remaining / 1000).toFixed(1)}초`;

            color =
                remaining <= 1500
                    ? "#d9534f"
                    : remaining <= 2500
                    ? "#f0a43a"
                    : "#4fa568";
        }

        else if (grill.state === "burnt") {
            color = "#d9534f";
            message = "🔥 음식이 탔어요!";
        }

        bar.style.width = percent + "%";
        bar.style.background = color;
        status.textContent = message;

        if (card) {
            card.classList.toggle(
                "urgent",
                ["flip", "ready"].includes(
                    grill.state
                ) &&
                BURN_WAIT_MS - elapsed <= 1500
            );
        }
    });
}

function renderPlates() {
    const area = el("plates");

    if (!game) {
        area.innerHTML = Array.from(
            {length: 3},
            (_, i) => `
                <div class="plate">
                    <span class="plate-number">
                        ${i + 1}
                    </span>
                    🍽️
                    <small>빈 접시</small>
                </div>
            `
        ).join("");
        return;
    }

    area.innerHTML = game.plates
        .map((plate, i) => {
            if (!plate) {
                return `
                    <div class="plate"
                         data-drop="plate"
                         data-index="${i}">
                        <span class="plate-number">
                            ${i + 1}
                        </span>
                        🍽️
                        <small>빈 접시</small>
                    </div>
                `;
            }

            const description =
                plate.fill.name +
                (plate.top
                    ? " + " + plate.top.name
                    : "");

            return `
                <div class="plate ${plate.top ? "ready" : ""}"
                     data-drop="plate"
                     data-index="${i}"
                     data-source="plate"
                     data-label="오코노미야끼"
                     data-emoji="🍳">
                    <span class="plate-number">
                        ${i + 1}
                    </span>
                    🍳
                    <small>${description}</small>
                </div>
            `;
        }).join("");

    if (
        game.plates.some(
            plate => plate && !plate.top
        )
    ) {
        el("plate-help").textContent =
            "접시에 토핑을 올려 주세요";
    } else if (game.plates.some(Boolean)) {
        el("plate-help").textContent =
            "완성된 음식을 서빙하세요";
    } else {
        el("plate-help").textContent =
            "익은 오코노미야끼를 접시에 올려 주세요";
    }
}

function renderItems() {
    el("ingredients").innerHTML = ingredients
        .map((item, i) => `
            <div class="item"
                 data-source="ingredient"
                 data-index="${i}"
                 data-images="${item.images.join(",")}"
                 data-emoji="${item.emoji}"
                 data-label="${item.name}">
                ${artMarkup(item.images, item.emoji)}
                ${item.name}
            </div>
        `).join("");

    el("tools").innerHTML = tools
        .map((item, i) => `
            <div class="item"
                 data-source="tool"
                 data-index="${i}"
                 data-images="${item.images.join(",")}"
                 data-emoji="${item.emoji}"
                 data-label="${item.name}">
                ${artMarkup(item.images, item.emoji)}
                ${item.name}
            </div>
        `).join("");
}

function renderAll() {
    updateHud();
    renderCustomers();
    renderGrills();
    renderPlates();
    renderItems();
    updateGrillBars(now());
}

function loseLife(message) {
    if (!game || game.ended || game.paused) return;

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

function serve(customerIndex, plateIndex) {
    const customer = game.customers[customerIndex];
    const plate = game.plates[plateIndex];

    if (!customer || customer.happyUntil) return;

    if (!plate || !plate.top) {
        tell(
            "토핑까지 완성한 음식을 서빙하세요!",
            "warning"
        );
        return;
    }

    const correct =
        plate.fill.id === customer.fill.id &&
        plate.top.id === customer.top.id;

    game.plates[plateIndex] = null;
    renderPlates();

    if (correct) {
        game.combo++;

        game.best = Math.max(
            game.best, game.combo
        );

        game.served++;
        game.score += 100 + Math.min(
            game.combo * 10,
            100
        );

        customer.happyUntil = now() + 850;
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
            game.customers[customerIndex] =
                newCustomer();
            renderCustomers();
        }
    }
}

function handleDrop(kind, index, target, targetIndex) {
    if (!game || game.ended || game.paused) return;

    // 반죽 / 재료 → 철판
    if (
        kind === "ingredient" &&
        target === "grill"
    ) {
        const item = ingredients[index];
        const grill = game.grills[targetIndex];

        if (!item || !grill) return;

        if (
            item.type === "batter" &&
            grill.state === "empty"
        ) {
            game.grills[targetIndex] = {
                state: "batter"
            };

            renderGrills();
            tell(
                "반죽 완료! 재료를 올려 주세요!",
                "info"
            );
            return;
        }

        if (
            item.type === "filling" &&
            grill.state === "batter"
        ) {
            game.grills[targetIndex] = {
                state: "cooking",
                fill: item,
                since: now()
            };

            renderGrills();
            updateGrillBars(now());

            tell(
                "앞면을 굽고 있어요!",
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

    // 뒤집개 → 철판
    if (
        kind === "tool" &&
        target === "grill"
    ) {
        const tool = tools[index];
        const grill = game.grills[targetIndex];

        if (!tool || !grill) return;

        if (
            tool.type !== "flip" ||
            grill.state !== "flip"
        ) {
            tell(
                "앞면이 다 익으면 뒤집개를 사용하세요!",
                "warning"
            );
            return;
        }

        grill.state = "second";
        grill.since = now();

        renderGrills();
        updateGrillBars(now());

        tell(
            "✅ 뒤집기 성공! 뒷면을 굽습니다.",
            "success"
        );
        return;
    }

    // 철판 → 빈 접시
    if (
        kind === "grill" &&
        target === "plate"
    ) {
        const grill = game.grills[index];

        if (!grill || grill.state !== "ready") {
            tell(
                "다 익은 오코노미야끼만 접시에 담을 수 있어요!",
                "warning"
            );
            return;
        }

        if (game.plates[targetIndex]) {
            tell(
                "그 접시는 이미 사용 중이에요!",
                "warning"
            );
            return;
        }

        game.plates[targetIndex] = {
            fill: grill.fill,
            top: null
        };

        game.grills[index] = {
            state: "empty"
        };

        renderGrills();
        renderPlates();

        tell(
            "✅ 접시에 담았어요! 토핑을 올려 주세요.",
            "success"
        );
        return;
    }

    // 토핑 → 접시
    if (
        kind === "tool" &&
        target === "plate"
    ) {
        const tool = tools[index];
        const plate = game.plates[targetIndex];

        if (!tool || tool.type !== "topping") {
            tell(
                "접시에는 소스나 마요네즈를 올려 주세요!",
                "warning"
            );
            return;
        }

        if (!plate) {
            tell(
                "먼저 오코노미야끼를 접시에 담아 주세요!",
                "warning"
            );
            return;
        }

        if (plate.top) {
            tell(
                "이미 토핑을 올렸어요!",
                "warning"
            );
            return;
        }

        plate.top = tool;
        renderPlates();

        tell(
            "✅ 토핑 완료! 손님에게 서빙하세요.",
            "success"
        );
        return;
    }

    // 접시 → 손님
    if (
        kind === "plate" &&
        target === "customer"
    ) {
        serve(targetIndex, index);
        return;
    }

    // 철판 또는 접시 → 휴지통
    if (target === "trash") {
        if (kind === "plate") {
            game.plates[index] = null;
            renderPlates();
            tell("음식을 버렸습니다.", "info");
            return;
        }

        if (kind === "grill") {
            game.grills[index] = {
                state: "empty"
            };

            renderGrills();
            tell("철판을 비웠습니다.", "info");
            return;
        }
    }

    tell(
        "올바른 위치에 재료를 놓아 주세요!",
        "warning"
    );
}

function moveGhost(event) {
    if (!drag) return;

    drag.ghost.style.left =
        (event.clientX + 12) + "px";

    drag.ghost.style.top =
        (event.clientY + 12) + "px";

    if (highlighted) {
        highlighted.classList.remove("drop-over");
    }

    highlighted = document.elementFromPoint(
        event.clientX,
        event.clientY
    )?.closest("[data-drop]");

    if (highlighted) {
        highlighted.classList.add("drop-over");
    }
}

document.addEventListener("pointerdown", event => {
    if (
        !game ||
        game.ended ||
        game.paused ||
        drag
    ) return;

    const source = event.target.closest(
        "[data-source]"
    );

    if (!source) return;

    event.preventDefault();

    const ghost = document.createElement("div");
    ghost.className = "ghost";

    const filenames = (
        source.dataset.images || ""
    ).split(",").filter(Boolean);

    ghost.innerHTML = `
        ${artMarkup(
            filenames,
            source.dataset.emoji || "🍳"
        )}
        <small>${source.dataset.label || ""}</small>
    `;

    document.body.appendChild(ghost);

    drag = {
        pointerId: event.pointerId,
        source,
        kind: source.dataset.source,
        index: Number(source.dataset.index || 0),
        ghost
    };

    source.classList.add("dragging-original");
    moveGhost(event);
});

document.addEventListener("pointermove", event => {
    if (
        !drag ||
        drag.pointerId !== event.pointerId
    ) return;

    event.preventDefault();
    moveGhost(event);
}, {passive: false});

function releaseDrag(event) {
    if (
        !drag ||
        drag.pointerId !== event.pointerId
    ) return;

    const oldDrag = drag;

    const target = document.elementFromPoint(
        event.clientX,
        event.clientY
    )?.closest("[data-drop]");

    oldDrag.ghost.remove();

    if (oldDrag.source.isConnected) {
        oldDrag.source.classList.remove(
            "dragging-original"
        );
    }

    if (highlighted) {
        highlighted.classList.remove("drop-over");
    }

    drag = null;
    highlighted = null;

    if (target) {
        handleDrop(
            oldDrag.kind,
            oldDrag.index,
            target.dataset.drop,
            Number(target.dataset.index || 0)
        );
    }
}

document.addEventListener("pointerup", releaseDrag);

document.addEventListener("pointercancel", event => {
    if (
        !drag ||
        drag.pointerId !== event.pointerId
    ) return;

    drag.ghost.remove();

    if (drag.source.isConnected) {
        drag.source.classList.remove(
            "dragging-original"
        );
    }

    if (highlighted) {
        highlighted.classList.remove("drop-over");
    }

    drag = null;
    highlighted = null;
});

function nextLevel() {
    if (!game || game.ended || game.paused) return;

    if (game.level === 5) {
        endGame(true);
        return;
    }

    game.level++;
    game.lives = MAX_LIVES;

    game.grills = Array.from(
        {length: 3},
        () => ({state: "empty"})
    );

    game.plates = [null, null, null];
    game.customers = [];
    game.paused = true;

    updateHud();

    el("time").textContent =
        LEVEL_TIMES[game.level - 1];

    runLevelCountdown(true);
}

function endGame(won) {
    if (!game || game.ended) return;

    game.ended = true;
    game.paused = true;

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

function updateGrillBarsAndTime(t) {
    if (!game) return;
    updateGrillBars(t);
}

function tick() {
    if (!game || game.ended || game.paused) return;

    const t = now();

    const remaining = Math.max(
        0,
        LEVEL_TIMES[game.level - 1] -
        (t - game.levelStart) / 1000
    );

    el("time").textContent = Math.ceil(remaining);

    if (remaining <= 0) {
        nextLevel();
        return;
    }

    let grillsChanged = false;

    game.grills.forEach(grill => {
        if (![
            "cooking", "flip", "second", "ready"
        ].includes(grill.state)) {
            return;
        }

        const elapsed = t - grill.since;

        if (
            grill.state === "cooking" &&
            elapsed >= FIRST_COOK_MS
        ) {
            grill.state = "flip";
            grill.since = t;
            grillsChanged = true;
            return;
        }

        if (
            grill.state === "second" &&
            elapsed >= SECOND_COOK_MS
        ) {
            grill.state = "ready";
            grill.since = t;
            grillsChanged = true;
            return;
        }

        if (
            ["flip", "ready"].includes(grill.state) &&
            elapsed >= BURN_WAIT_MS
        ) {
            grill.state = "burnt";
            game.score = Math.max(
                0,
                game.score - 10
            );
            game.combo = 0;

            updateHud();
            grillsChanged = true;

            tell(
                "🔥 오코노미야끼가 탔어요! -10점",
                "error"
            );
        }
    });

    if (grillsChanged) renderGrills();

    updateGrillBarsAndTime(t);

    let customersChanged = false;

    for (let i = 0; i < game.customers.length; i++) {
        const customer = game.customers[i];

        if (customer.happyUntil) {
            if (t >= customer.happyUntil) {
                game.customers[i] = newCustomer();
                customersChanged = true;
            }
            continue;
        }

        if (
            t - customer.born >= customer.patience
        ) {
            game.missed++;

            loseLife(
                "❌ 손님이 기다리다 떠났어요!"
            );

            if (game.ended) return;

            game.customers[i] = newCustomer();
            customersChanged = true;
        }
    }

    if (customersChanged) renderCustomers();

    updateCustomers(t);
}

function initializeScreen() {
    renderItems();

    el("customers").innerHTML = Array.from(
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

    el("grills").innerHTML = Array.from(
        {length: 3},
        (_, i) => `
            <div class="grill">
                <div class="pancake">⚫</div>
                <strong>${i + 1}번 철판</strong>
                <div class="bar"></div>
                <small>게임을 시작해 주세요</small>
            </div>
        `
    ).join("");

    renderPlates();
}

initializeScreen();
setInterval(tick, 100);
</script>
</body>
</html>
"""

GAME_HTML = GAME_HTML.replace(
    "__CUSTOMERS__", json.dumps(customer_images)
)
GAME_HTML = GAME_HTML.replace(
    "__INGREDIENTS__", json.dumps(ingredient_images)
)
GAME_HTML = GAME_HTML.replace(
    "__BUBBLE__", json.dumps(bubble_theme)
)

if background_url:
    background_css = """
    <style>
    .game {
        background-image: url("__IMAGE__") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
    }
    </style>
    """.replace("__IMAGE__", background_url)

    GAME_HTML = GAME_HTML.replace(
        "</head>",
        background_css + "</head>",
        1
    )

components.html(
    GAME_HTML,
    height=700,
    scrolling=False
)
