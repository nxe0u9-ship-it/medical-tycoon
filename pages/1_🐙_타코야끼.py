
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json

from game_unlock import listen_for_takoyaki_clear

# ==========================================
# 와글와글 포장마차 - 타코야끼
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

theme = CUSTOMER_THEMES.get(
    st.session_state.get(
        "saved_customer_style",
        "🎆 축제 손님",
    ),
    "festival",
)

bubble = BUBBLE_THEMES.get(
    st.session_state.get(
        "saved_bubble_style",
        "💭 둥근 말풍선",
    ),
    "round",
)

# ==========================================
# 손님 이미지 불러오기
# ==========================================

ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = ROOT / "assets" / "customers" / theme


def load_customer_images():
    images = {}
    missing = []

    expressions = [
        "normal",
        "waiting",
        "angry",
        "happy",
    ]

    for number in range(1, 6):
        for expression in expressions:
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
# Streamlit 화면 설정
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
    border: none !important;
    display: block;
}
</style>
""")


# ==========================================
# 게임 HTML
# ==========================================

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">

<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1">

<style>

/* 기본 화면 */

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

/* 안내문 전용 공간 */

.notice-area {
    width: 100%;
    height: 43px;
    margin: 2px 0 4px;

    display: flex;
    align-items: center;
    justify-content: center;

    pointer-events: none;
}

.toast {
    position: relative;
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
    line-height: 1.3;

    box-shadow: 0 3px 8px #0003;

    opacity: 0;
    transform: translateY(-5px);

    transition:
        opacity 0.18s ease,
        transform 0.18s ease;
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

/* 가게 제목 */

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

/* 손님 영역 */

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

/* 조리대 */

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
        minmax(0, 1.6fr)
        minmax(260px, 1fr);
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
    gap: 5px;

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

.holes {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 3px;
    width: min(100px, 95%);
    pointer-events: none;
}

.ball {
    aspect-ratio: 1;
    display: grid;
    place-items: center;

    border: 2px solid #111219;
    border-radius: 50%;
    background: #15161a;
    font-size: 14px;
}

.ball.cooking {
    background: #d9ab65;
}

.ball.ready {
    background: #dca34d;
}

.ball.burnt {
    background: #493024;
}

/* 조리 및 타기까지 남은 시간 게이지 */

.bar {
    width: 80%;
    height: 9px;

    background: #151515;
    border: 1px solid #555;
    border-radius: 20px;

    overflow: hidden;
    pointer-events: none;
}

.bar span {
    display: block;
    width: 0%;
    height: 100%;
    background: #efc456;
    border-radius: 20px;
    transition:
        background-color 0.15s ease;
}

.grill.ready {
    border-color: #62b780;
}

.grill.urgent {
    border-color: #e76b5d;
}

.grill.burnt {
    border-color: #87493d;
}

/* 완성 접시 3개 */

.right {
    display: flex;
    flex-direction: column;
    gap: 7px;
    min-width: 0;
}

.plate-zone {
    flex: 1;
    padding: 6px;

    border: 3px solid #e5bd8f;
    border-radius: 13px;
    background: #fff1d9;

    text-align: center;
}

.plate-zone strong {
    font-size: 12px;
}

.plates {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 5px;

    width: 100%;
    margin: 5px auto;
}

.plate {
    position: relative;
    min-width: 0;
    min-height: 62px;
    padding: 5px 2px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;

    border: 2px solid #c8b5a2;
    border-radius: 12px;

    background: radial-gradient(
        circle,
        white 0 48%,
        #b7d6e2 50% 60%,
        white 62%
    );

    font-size: 22px;
    font-weight: 900;
}

.plate small {
    font-size: 9px;
    line-height: 1.2;
    pointer-events: none;
    overflow-wrap: anywhere;
}

.plate.ready {
    border-color: #79ad6a;
}

.plate-number {
    position: absolute;
    top: 2px;
    left: 4px;
    font-size: 9px;
    pointer-events: none;
}

#plate-help {
    font-size: 10px;
}

/* 휴지통 */

.trash {
    min-height: 34px;
    padding: 5px;

    display: grid;
    place-items: center;

    background: #f9d6c7;
    border: 3px solid #e5bd8f;
    border-radius: 12px;

    font-size: 12px;
    font-weight: 900;
}

/* 재료 */

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

    background: #fff1da;
    border: 3px solid #be8454;
    border-radius: 15px;
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
    font-size: 12px;
    font-weight: 900;
}

.item span {
    display: block;
    margin-bottom: 2px;
    font-size: 24px;
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

/* 드래그 앤 드롭 */

[data-source] {
    cursor: grab;
    touch-action: none;
    user-select: none;
}

.dragging-original {
    opacity: 0.45;
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

/* 시작 / 종료 화면 */

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

/* 작은 화면 */

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
            minmax(205px, 1fr);
    }

    .grills {
        gap: 3px;
        padding: 4px;
    }

    .ball {
        font-size: 11px;
        border-width: 1px;
    }

    .plate {
        font-size: 17px;
    }

    .item {
        font-size: 10px;
    }

    .item span {
        font-size: 20px;
    }

    .toast {
        min-width: 180px;
        max-width: 90%;
        padding: 6px 10px;
        font-size: 12px;
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

    <!-- 안내문 전용 공간 -->

    <div class="notice-area">

        <div
            class="toast info"
            id="toast"
            role="status"
            aria-live="polite">
        </div>

    </div>

    <!-- 가게 제목 -->

    <div class="sign">
        🐙 타코야끼 가게 🐙
    </div>

    <!-- 손님 -->

    <div
        class="customers"
        id="customers">
    </div>

    <!-- 조리대 -->

    <div class="counter">

        <h3>
            🍳 타코야끼 조리대
        </h3>

        <div class="kitchen">

            <div
                class="grills"
                id="grills">
            </div>

            <div class="right">

                <div class="plate-zone">

                    <strong>
                        🍽️ 완성 접시 3개
                    </strong>

                    <div
                        class="plates"
                        id="plates">
                    </div>

                    <small id="plate-help">
                        익은 타코야끼를 빈 접시에 올려 주세요
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

    <!-- 재료와 토핑 -->

    <div class="supplies">

        <div class="supply">

            <h3>
                🥣 기본 반죽 + 선택 재료
            </h3>

            <div
                class="items"
                id="fillings">
            </div>

        </div>

        <div class="supply">

            <h3>
                🍥 가쓰오부시 + 소스 선택
            </h3>

            <div
                class="items"
                id="toppings">
            </div>

        </div>
    </div>

    <!-- 조작 방법 -->

    <div class="help">
        반죽+문어 → 치즈 선택 → 굽기 → 접시 →
        가쓰오부시 → 소스 → 손님
    </div>

    <!-- 시작 화면 -->

    <div
        class="overlay"
        id="overlay">

        <div class="panel">

            <div
                id="panel-icon"
                style="font-size:58px">
                🐙
            </div>

            <h2 id="panel-title">
                타코야끼 가게
            </h2>

            <p id="panel-text">
                반죽과 문어는 기본!<br>
                치즈는 선택하고 가쓰오부시는 필수예요.<br>
                ❤️ 목숨 3개 · 총 5레벨<br>
                익은 타코야끼는 10초 이상 보관할 수 있어요!
            </p>

            <button
                class="start"
                id="start-button"
                onclick="beginCountdown()">

                🎮 타코야끼 만들기

            </button>

        </div>
    </div>

    <div
        class="countdown"
        id="countdown">

        <span id="count-text">3</span>

    </div>

</div>


<script>

// ==========================================
// 게임 기본 설정
// ==========================================

const CUSTOMER_IMAGES = __IMAGES__;
const BUBBLE_STYLE = __BUBBLE__;

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

// ==========================================
// 조리 시간
// ==========================================

// 익는 시간: 2.7초
const COOK_MS = 2700;

// 조리 시작 후 13초가 지나면 탐
const BURN_MS = 13000;

// 다 익은 후 타기까지 10.3초
const READY_TIME_MS = BURN_MS - COOK_MS;


// ==========================================
// 재료
// ==========================================

const fillings = [

    {
        id: "base",
        name: "반죽 + 문어",
        emoji: "🥣",
        type: "base"
    },

    {
        id: "cheese",
        name: "치즈 추가",
        emoji: "🧀",
        type: "cheese"
    }

];

const toppings = [

    {
        id: "katsu",
        name: "가쓰오부시",
        emoji: "🍥",
        type: "katsu"
    },

    {
        id: "original",
        name: "오리지널",
        emoji: "🍯",
        type: "sauce"
    },

    {
        id: "mentai",
        name: "명란마요",
        emoji: "🥫",
        type: "sauce"
    }

];

const el = id => document.getElementById(id);

const now = () => performance.now();

let game = null;
let drag = null;
let highlighted = null;
let toastTimer = null;
let counting = false;


// ==========================================
// 안내 메시지
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
// 손님 캐릭터 이미지
// ==========================================

function imageFor(number, expression) {

    return (
        CUSTOMER_IMAGES[
            `${number}_${expression}`
        ] ||
        CUSTOMER_IMAGES[
            `${number}_normal`
        ] ||
        ""
    );
}


// ==========================================
// 새로운 손님
// ==========================================

function newCustomer() {

    const [min, max] =
        CUSTOMER_WAIT[game.level - 1];

    return {

        character: Math.floor(Math.random() * 5) + 1,

        cheese: Math.random() < 0.5,

        sauce: Math.random() < 0.5
            ? "original"
            : "mentai",

        born: now(),

        patience: (
            min + Math.random() * (max - min)
        ) * 1000,

        happyUntil: 0
    };
}


// ==========================================
// 주문 내용
// ==========================================

function orderText(c) {

    const cheese = c.cheese
        ? "🧀 치즈"
        : "🥣 기본";

    const sauce = c.sauce === "original"
        ? "🍯 오리지널"
        : "🥫 명란마요";

    return `${cheese} + ${sauce}`;
}


// ==========================================
// 카운트다운
// ==========================================

async function beginCountdown() {

    if (counting) return;

    counting = true;

    el("overlay").classList.add("hidden");
    el("countdown").classList.add("show");

    for (const number of ["3", "2", "1"]) {

        el("count-text").textContent = number;

        await new Promise(resolve =>
            setTimeout(resolve, 1000)
        );
    }

    el("count-text").textContent = "START!";

    await new Promise(resolve =>
        setTimeout(resolve, 600)
    );

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
        served: 0,
        missed: 0,

        grills: Array.from(
            {length: 3},
            () => ({state: "empty"})
        ),

        plates: [null, null, null],

        customers: [],

        ended: false
    };

    game.customers = Array.from(
        {length: 3},
        newCustomer
    );

    renderAll();

    tell(
        "영업 시작! 주문을 만들어 주세요!",
        "info"
    );
}


// ==========================================
// 상단 상태 갱신
// ==========================================

function updateHud() {

    if (!game) return;

    el("level").textContent = game.level;
    el("score").textContent = game.score;
    el("lives").textContent = "❤️".repeat(game.lives);
}


// ==========================================
// 손님 표시
// ==========================================

function renderCustomers() {

    if (!game) return;

    el("customers").innerHTML =
        game.customers.map((c, i) => `

        <div
            class="customer"
            id="customer-${i}"
            data-drop="customer"
            data-index="${i}">

            <div
                class="bubble ${BUBBLE_STYLE}"
                id="bubble-${i}">

                ${orderText(c)}

            </div>

            <img
                class="avatar"
                id="avatar-${i}"
                src="${imageFor(c.character, "normal")}"
                data-expression="normal"
                draggable="false">

            <div
                class="customer-label"
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
// 손님 표정 변화
// ==========================================

function updateCustomers(t) {

    game.customers.forEach((c, i) => {

        const avatar = el(`avatar-${i}`);
        const card = el(`customer-${i}`);
        const bar = el(`patience-${i}`);
        const label = el(`label-${i}`);
        const bubble = el(`bubble-${i}`);

        if (!avatar || !bar) return;

        if (c.happyUntil) {

            if (
                avatar.dataset.expression !== "happy"
            ) {

                avatar.src = imageFor(
                    c.character,
                    "happy"
                );

                avatar.dataset.expression = "happy";
            }

            card.classList.add("happy");
            card.classList.remove("urgent");

            label.textContent = "맛있어요!";
            bubble.textContent = "감사합니다!";

            bar.style.width = "100%";
            bar.style.background = "#70b963";

            return;
        }

        const percent = Math.max(
            0,
            100 * (1 - (t - c.born) / c.patience)
        );

        const expression =
            percent <= 30
                ? "angry"
                : percent <= 65
                ? "waiting"
                : "normal";

        if (
            avatar.dataset.expression !== expression
        ) {

            avatar.src = imageFor(
                c.character,
                expression
            );

            avatar.dataset.expression = expression;
        }

        card.classList.remove("happy");

        card.classList.toggle(
            "urgent",
            percent <= 30
        );

        label.textContent =
            percent <= 30
                ? "너무 오래 기다렸어요!"
                : percent <= 65
                ? "조금 초조해요..."
                : "주문을 기다리는 중";

        bar.style.width = percent + "%";

        bar.style.background =
            percent <= 30
                ? "#dc6753"
                : percent <= 65
                ? "#e8b64a"
                : "#70b963";
    });
}


// ==========================================
// 조리판 표시
// ==========================================

function renderGrills() {

    if (!game) return;

    const messages = {
        empty: "반죽을 넣어 주세요",
        cooking: "조리 중...",
        ready: "다 익었어요!",
        burnt: "음식이 탔어요!"
    };

    el("grills").innerHTML =
        game.grills.map((g, i) => {

            const icon =
                g.state === "cooking"
                    ? "🟡"
                    : g.state === "ready"
                    ? "🟤"
                    : g.state === "burnt"
                    ? "⚫"
                    : "";

            const source =
                ["ready", "burnt"].includes(g.state)

                ? `data-source="grill"
                   data-index="${i}"
                   data-emoji="🍡"
                   data-label="타코야끼"`

                : "";

            const cheeseLabel =
                g.cheese
                    ? "🧀 치즈"
                    : "🥣 기본";

            return `

            <div
                class="grill ${g.state}"
                id="grill-${i}"
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
                    ).join("")}

                </div>

                <strong>
                    ${i + 1}번 조리판
                    ${g.state !== "empty"
                        ? " · " + cheeseLabel
                        : ""}
                </strong>

                <div class="bar">
                    <span id="cook-${i}"></span>
                </div>

                <small id="grill-status-${i}">
                    ${messages[g.state]}
                </small>

            </div>

            `;
        }).join("");
}


// ==========================================
// 완성 접시
// ==========================================

function renderPlates() {

    const root = el("plates");

    if (!game) {

        root.innerHTML = Array.from(
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

    root.innerHTML =
        game.plates.map((p, i) => {

            if (!p) {

                return `

                <div
                    class="plate"
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

            const complete =
                p.katsu && p.sauce !== null;

            let description = p.cheese
                ? "치즈"
                : "기본";

            if (p.katsu) {
                description += " + 가쓰오";
            }

            if (p.sauce) {

                description +=
                    p.sauce === "original"
                        ? " + 오리지널"
                        : " + 명란마요";
            }

            return `

            <div
                class="plate ${complete ? "ready" : ""}"
                data-drop="plate"
                data-index="${i}"
                data-source="plate"
                data-emoji="🍡"
                data-label="타코야끼">

                <span class="plate-number">
                    ${i + 1}
                </span>

                🍡

                <small>
                    ${description}
                </small>

            </div>

            `;
        }).join("");

    el("plate-help").textContent =
        game.plates.some(Boolean)
            ? "가쓰오부시와 소스를 올려 주세요"
            : "익은 타코야끼를 빈 접시에 올려 주세요";
}


// ==========================================
// 재료
// ==========================================

function renderSupplies() {

    el("fillings").innerHTML =
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

        `).join("");

    el("toppings").innerHTML =
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

        `).join("");
}


function renderAll() {

    updateHud();
    renderCustomers();
    renderGrills();
    renderPlates();
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
            `${message} 남은 목숨 ${game.lives}개`,
            "error"
        );
    }
}


// ==========================================
// 손님에게 서빙
// ==========================================

function serve(customerIndex, plateIndex) {

    const c = game.customers[customerIndex];
    const p = game.plates[plateIndex];

    if (!c || c.happyUntil) return;

    if (!p) {

        tell(
            "먼저 타코야끼를 완성해 주세요!",
            "warning"
        );

        return;
    }

    if (!p.katsu || !p.sauce) {

        tell(
            "가쓰오부시와 소스를 모두 올려 주세요!",
            "warning"
        );

        return;
    }

    const correct =
        p.cheese === c.cheese &&
        p.sauce === c.sauce;

    game.plates[plateIndex] = null;

    renderPlates();

    if (correct) {

        game.combo++;
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

            game.customers[customerIndex] =
                newCustomer();

            renderCustomers();
        }
    }
}


// ==========================================
// 드롭 처리
// ==========================================

function handleDrop(kind, index, target, targetIndex) {

    if (!game || game.ended) return;

    // 기본 반죽 + 문어

    if (
        kind === "filling" &&
        target === "grill"
    ) {

        const item = fillings[index];
        const g = game.grills[targetIndex];

        if (!g) return;

        if (item.type === "base") {

            if (g.state !== "empty") {

                tell(
                    "이미 사용 중인 조리판입니다!",
                    "warning"
                );

                return;
            }

            game.grills[targetIndex] = {
                state: "cooking",
                cheese: false,
                born: now()
            };

            renderGrills();

            return;
        }

        // 치즈 추가

        if (item.type === "cheese") {

            if (g.state !== "cooking") {

                tell(
                    "조리 중인 타코야끼에 치즈를 추가해 주세요!",
                    "warning"
                );

                return;
            }

            if (g.cheese) {

                tell(
                    "이미 치즈가 들어 있어요!",
                    "warning"
                );

                return;
            }

            g.cheese = true;

            renderGrills();

            tell(
                "🧀 치즈를 추가했어요!",
                "success"
            );

            return;
        }
    }

    // 익은 음식을 접시로 이동

    if (
        kind === "grill" &&
        target === "plate"
    ) {

        const g = game.grills[index];

        if (!g || g.state !== "ready") {

            tell(
                "다 익은 타코야끼만 접시에 담을 수 있어요!",
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
            cheese: g.cheese,
            katsu: false,
            sauce: null
        };

        game.grills[index] = {
            state: "empty"
        };

        renderGrills();
        renderPlates();

        return;
    }

    // 가쓰오부시와 소스

    if (
        kind === "topping" &&
        target === "plate"
    ) {

        const item = toppings[index];
        const p = game.plates[targetIndex];

        if (!p) {

            tell(
                "먼저 타코야끼를 접시에 담아 주세요!",
                "warning"
            );

            return;
        }

        if (item.type === "katsu") {

            if (p.katsu) {

                tell(
                    "이미 가쓰오부시를 올렸어요!",
                    "warning"
                );

                return;
            }

            p.katsu = true;

            renderPlates();
            return;
        }

        if (item.type === "sauce") {

            if (!p.katsu) {

                tell(
                    "먼저 가쓰오부시를 올려 주세요!",
                    "warning"
                );

                return;
            }

            if (p.sauce) {

                tell(
                    "이미 소스를 선택했어요!",
                    "warning"
                );

                return;
            }

            p.sauce = item.id;

            renderPlates();

            tell(
                "✅ 타코야끼 완성! 손님에게 서빙하세요!",
                "success"
            );

            return;
        }
    }

    // 손님에게 서빙

    if (
        kind === "plate" &&
        target === "customer"
    ) {

        serve(targetIndex, index);
        return;
    }

    // 휴지통

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

            tell("조리판을 비웠습니다.", "info");
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
        e.clientX, e.clientY
    )?.closest("[data-drop]");

    if (highlighted) {
        highlighted.classList.add("drop-over");
    }
}


document.addEventListener(
    "pointerdown",
    e => {

        if (!game || game.ended || drag) return;

        const source = e.target.closest(
            "[data-source]"
        );

        if (!source) return;

        e.preventDefault();

        const ghost = document.createElement("div");

        ghost.className = "ghost";

        ghost.innerHTML = `
            ${source.dataset.emoji || "🍡"}
            <small>
                ${source.dataset.label || ""}
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

        source.classList.add("dragging-original");

        moveGhost(e);
    }
);


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
        e.clientX, e.clientY
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
            Number(target.dataset.index || 0)
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
// 레벨 이동
// ==========================================

function nextLevel() {

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

    game.plates = [null, null, null];

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

    if (won) {

        window.parent.postMessage(
            {
                type: "waggle_takoyaki_clear",
                cleared: true
            },
            "*"
        );
    }

    el("panel-icon").textContent =
        won ? "🏆" : "💔";

    el("panel-title").textContent =
        won ? "5레벨 클리어!" : "영업 종료!";

    el("panel-text").innerHTML = `
        최종 점수: ${game.score}점<br>
        성공한 주문: ${game.served}개<br>
        ${won
            ? "🔓 오코노미야끼 가게 잠금 해제!"
            : "다시 도전해 보세요!"}
    `;

    el("start-button").textContent =
        "🔄 다시 도전하기";

    el("overlay").classList.remove("hidden");
}


// ==========================================
// 조리판 게이지 및 남은 시간
// ==========================================

function updateGrillBars(t) {

    if (!game) return;

    game.grills.forEach((g, i) => {

        const bar = el(`cook-${i}`);
        const statusText = el(`grill-status-${i}`);
        const grillElement = el(`grill-${i}`);

        if (!bar || !statusText) return;

        let percent = 0;
        let color = "#efc456";
        let message = "반죽을 넣어 주세요";

        // 조리 중: 노란색 게이지가 차오름

        if (g.state === "cooking") {

            const elapsed = t - g.born;

            percent = Math.min(
                100,
                (elapsed / COOK_MS) * 100
            );

            color = "#efc456";

            const remaining = Math.max(
                0,
                COOK_MS - elapsed
            );

            message =
                `익기까지 ${(remaining / 1000).toFixed(1)}초`;

        }

        // 다 익음: 타기까지 남은 시간 감소

        else if (g.state === "ready") {

            const elapsed = t - g.born;

            const remaining = Math.max(
                0,
                BURN_MS - elapsed
            );

            percent = Math.max(
                0,
                Math.min(
                    100,
                    (remaining / READY_TIME_MS) * 100
                )
            );

            const seconds = Math.ceil(
                remaining / 1000
            );

            if (seconds <= 3) {

                color = "#d9534f";

                message =
                    `🔥 곧 타요! ${seconds}초`;

            } else if (seconds <= 6) {

                color = "#f0a43a";

                message =
                    `⚠️ 타기까지 ${seconds}초`;

            } else {

                color = "#4fa568";

                message =
                    `타기까지 ${seconds}초`;
            }
        }

        // 음식이 탄 상태

        else if (g.state === "burnt") {

            percent = 0;
            color = "#d9534f";
            message = "🔥 음식이 탔어요!";
        }

        bar.style.width = percent + "%";
        bar.style.background = color;

        statusText.textContent = message;

        if (grillElement) {

            grillElement.classList.toggle(
                "urgent",
                g.state === "ready" &&
                BURN_MS - (t - g.born) <= 3000
            );
        }
    });
}


// ==========================================
// 타이머 및 상태 갱신
// ==========================================

function tick() {

    if (!game || game.ended) return;

    const t = now();

    const remaining = Math.max(
        0,
        LEVEL_TIMES[game.level - 1] -
        (t - game.levelStart) / 1000
    );

    el("time").textContent =
        Math.ceil(remaining);

    // 레벨 제한 시간

    if (remaining <= 0) {

        nextLevel();
        return;
    }

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

                game.customers[i] =
                    newCustomer();

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

            game.customers[i] =
                newCustomer();

            customersChanged = true;
        }
    }

    if (customersChanged) {
        renderCustomers();
    }

    updateCustomers(t);

    // 조리 상태 변화

    let grillsChanged = false;

    game.grills.forEach(g => {

        if (
            g.state !== "cooking" &&
            g.state !== "ready"
        ) {
            return;
        }

        const elapsed = t - g.born;

        if (
            g.state === "cooking" &&
            elapsed >= COOK_MS
        ) {

            g.state = "ready";
            grillsChanged = true;
        }

        if (
            g.state === "ready" &&
            elapsed >= BURN_MS
        ) {

            g.state = "burnt";
            grillsChanged = true;

            tell(
                "🔥 타코야끼가 탔어요!",
                "error"
            );
        }
    });

    if (grillsChanged) {
        renderGrills();
    }

    // 조리판별 시간 게이지 갱신
    updateGrillBars(t);
}


// ==========================================
// 시작 전 미리보기
// ==========================================

function initializeScreen() {

    renderSupplies();

    el("customers").innerHTML =
        Array.from(
            {length: 3},
            (_, i) => `

            <div class="customer">

                <div class="bubble ${BUBBLE_STYLE}">
                    게임 시작 후 주문이 나타나요!
                </div>

                <img
                    class="avatar"
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
        ).join("");

    renderPlates();
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
# Python 데이터를 HTML에 전달
# ==========================================

GAME_HTML = GAME_HTML.replace(
    "__IMAGES__",
    json.dumps(customer_images),
)

GAME_HTML = GAME_HTML.replace(
    "__BUBBLE__",
    json.dumps(bubble),
)


# ==========================================
# 5레벨 클리어 신호 수신
# ==========================================

listen_for_takoyaki_clear()


# ==========================================
# 게임 표시
# ==========================================

components.html(
    GAME_HTML,
    height=700,
    scrolling=False,
)
