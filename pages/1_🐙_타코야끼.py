










import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json

# ==========================================
# 와글와글 포장마차 - 오코노미야끼
# ==========================================

ROOT = Path(__file__).resolve().parent.parent

# ==========================================
# 꾸미기 설정
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

BACKGROUND_FILES = {
    "🌸 벚꽃 축제": "bg_spring.png",
    "🎆 여름 축제": "bg_summer.png",
    "🍁 가을 야시장": "bg_autumn.png",
    "❄️ 겨울 포장마차": "bg_winter.png",
}

customer_style = st.session_state.get(
    "saved_customer_style",
    "🎆 축제 손님"
)

bubble_style = st.session_state.get(
    "saved_bubble_style",
    "💭 둥근 말풍선"
)

background_style = st.session_state.get(
    "saved_background",
    "🌸 벚꽃 축제"
)

theme = CUSTOMER_THEMES.get(
    customer_style,
    "festival"
)

bubble = BUBBLE_THEMES.get(
    bubble_style,
    "round"
)

background_filename = BACKGROUND_FILES.get(
    background_style,
    "bg_spring.png"
)

# ==========================================
# 이미지 불러오기
# ==========================================

def image_to_data_url(path):
    encoded = base64.b64encode(
        path.read_bytes()
    ).decode("ascii")

    return "data:image/png;base64," + encoded


def load_customer_images():
    result = {}
    missing = []

    image_dir = ROOT / "assets" / "customers" / theme

    for number in range(1, 6):
        for expression in [
            "normal",
            "waiting",
            "angry",
            "happy",
        ]:
            filename = (
                f"{theme}_{number:02d}_{expression}.png"
            )

            path = image_dir / filename

            if path.is_file():
                result[f"{number}_{expression}"] = (
                    image_to_data_url(path)
                )
            else:
                missing.append(filename)

    return result, missing


customer_images, missing_images = (
    load_customer_images()
)

if missing_images:
    st.error("손님 캐릭터 이미지를 찾지 못했어요.")
    st.code("\n".join(missing_images))
    st.stop()


background_path = ROOT / background_filename

background_url = ""

if background_path.is_file():
    background_url = image_to_data_url(
        background_path
    )
else:
    st.warning(
        f"배경 이미지가 없어 기본 배경으로 표시해요: "
        f"{background_filename}"
    )

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
# 게임 HTML
# ==========================================

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">

<head>
<meta charset="UTF-8">
<meta
    name="viewport"
    content="width=device-width, initial-scale=1"
>

<style>

* {
    box-sizing: border-box;
}

html,
body {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;

    font-family: "Malgun Gothic", sans-serif;
    color: #75452e;
}

/* =====================================
   전체 게임 화면
===================================== */

.game {
    position: relative;

    width: 100%;
    height: 680px;

    padding: 8px 12px;

    overflow: hidden;
    border-radius: 18px;

    background: linear-gradient(
        180deg,
        #7895b8 0%,
        #d7a5ad 25%,
        #f8c1a9 48%,
        #f8d9aa 75%,
        #c48e65 100%
    );

    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
}

/* =====================================
   상단 정보
===================================== */

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
    color: #ffe2bd;
    font-size: 10px;
}

.stat.timer {
    background: #c8584c;
}

/* =====================================
   안내 메시지
===================================== */

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

    background: #8b5a3c;
    color: white;

    font-size: 14px;
    font-weight: 900;
    text-align: center;

    box-shadow: 0 3px 8px #0003;

    opacity: 0;
    transform: translateY(-5px);

    transition:
        opacity 0.18s,
        transform 0.18s;
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
    color: #493116;
    border-color: #fff1b4;
}

.sign {
    width: fit-content;
    margin: 0 auto 7px;

    padding: 5px 24px;

    border: 3px solid #f2ca87;
    border-radius: 13px;

    background: #934a35;
    color: #fff6dc;

    box-shadow: 0 4px #683b29;

    font-size: 16px;
    font-weight: 900;
}

/* =====================================
   손님 3명
===================================== */

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

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;

    min-width: 0;
    padding: 0 5px;

    text-align: center;
}

.bubble {
    position: relative;
    z-index: 2;

    display: flex;
    align-items: center;
    justify-content: center;

    width: 94%;
    max-width: 260px;
    min-height: 35px;

    margin-bottom: 5px;
    padding: 5px 7px;

    background: #fffdf5;

    font-size: 11px;
    font-weight: 900;
    line-height: 1.3;
}

/* 둥근 말풍선 */

.bubble.round {
    border: 3px solid #d9ab83;
    border-radius: 18px;
    background: #fffdf5;
}

/* 강조 말풍선 */

.bubble.comic {
    border: 3px solid #d28b54;
    border-radius: 12px;

    background: #fff3bd;
    box-shadow: 3px 3px #e7b06e;
}

/* 심플 말풍선 */

.bubble.simple {
    border: 2px solid #d8c1aa;
    border-radius: 9px;
    background: #fffdf5;
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

/* =====================================
   철판 조리대
===================================== */

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

    color: #fff5de;

    font-size: 15px;
    text-align: center;
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

    border: 4px solid #302e34;
    border-radius: 15px;

    background: #44434a;
}

.grill {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    gap: 5px;

    min-width: 0;
    min-height: 132px;

    padding: 5px 3px;

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
    min-height: 13px;
    font-size: 10px;
    font-weight: 900;
    pointer-events: none;
}

.pancake {
    display: grid;
    place-items: center;

    width: 70px;
    height: 58px;

    font-size: 34px;
    pointer-events: none;
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

/* 조리 진행 게이지 */

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

    border-radius: 20px;
    background: #efc456;
}

/* =====================================
   완성 접시 3개
===================================== */

.right {
    display: flex;
    flex-direction: column;

    gap: 7px;
    min-width: 0;
}

.plate-zone {
    flex: 1;
    min-width: 0;

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
    margin: 5px auto;

    width: 100%;
}

.plate {
    position: relative;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    gap: 2px;

    min-width: 0;
    min-height: 62px;

    padding: 5px 2px;

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

    overflow-wrap: anywhere;
    pointer-events: none;
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

.trash {
    display: grid;
    place-items: center;

    min-height: 34px;
    padding: 5px;

    border: 3px solid #e5bd8f;
    border-radius: 12px;

    background: #f9d6c7;

    font-size: 12px;
    font-weight: 900;
}

/* =====================================
   재료와 도구
===================================== */

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

/* =====================================
   드래그 앤 드롭
===================================== */

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

/* =====================================
   시작 및 종료 화면
===================================== */

.overlay {
    position: absolute;
    z-index: 35;
    inset: 0;

    display: flex;
    align-items: center;
    justify-content: center;

    padding: 15px;

    background: #241b20b8;
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

    font-size: 105px;
    font-weight: 900;
}

.countdown.show {
    display: flex;
}

/* =====================================
   화면 크기 대응
===================================== */

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

    .pancake {
        width: 50px;
        font-size: 27px;
    }

    .plate {
        font-size: 17px;
    }

    .item {
        font-size: 10px;
    }

    .item span {
        font-size: 19px;
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

    <!-- 상단 -->

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

    <!-- 안내 메시지 -->

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
        🍳 오코노미야끼 가게 🍳
    </div>

    <!-- 손님 -->

    <div
        class="customers"
        id="customers">
    </div>

    <!-- 조리대 -->

    <div class="counter">

        <h3>🔥 오코노미야끼 철판 조리대</h3>

        <div class="kitchen">

            <!-- 철판 3개 -->

            <div
                class="grills"
                id="grills">
            </div>

            <!-- 접시 3개 -->

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
                        익은 오코노미야끼를
                        빈 접시에 올려 주세요
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

    <!-- 재료 및 도구 -->

    <div class="supplies">

        <div class="supply">

            <h3>① 반죽과 재료</h3>

            <div
                class="items"
                id="ingredients">
            </div>

        </div>

        <div class="supply">

            <h3>② 뒤집개 · ③ 토핑</h3>

            <div
                class="items"
                id="tools">
            </div>

        </div>

    </div>

    <!-- 조리 안내 -->

    <div class="help">
        반죽 → 재료 → 앞면 굽기 →
        뒤집개 → 뒷면 굽기 →
        접시 → 토핑 → 손님
    </div>

    <!-- 게임 시작 / 종료 화면 -->

    <div
        class="overlay"
        id="overlay">

        <div class="panel">

            <div
                id="panel-icon"
                style="font-size:58px">
                🍳
            </div>

            <h2 id="panel-title">
                오코노미야끼 가게
            </h2>

            <p id="panel-text">
                손님의 주문대로
                오코노미야끼를 만들어 주세요!<br>
                반죽 → 재료 → 앞면 → 뒤집기 →
                뒷면 → 토핑 → 서빙<br>
                ❤️ 목숨 3개 · 총 5레벨
            </p>

            <button
                class="start"
                id="start-button"
                onclick="beginCountdown()">
                🎮 오코노미야끼 만들기
            </button>

        </div>
    </div>

    <!-- 시작 카운트다운 -->

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
// 기본 설정
// ==========================================

const CUSTOMER_IMAGES = __IMAGES__;
const BUBBLE_STYLE = __BUBBLE__;

const LEVEL_TIMES = [
    90,
    120,
    120,
    150,
    150
];

const CUSTOMER_WAIT = [
    [40, 45],
    [30, 35],
    [22, 27],
    [15, 20],
    [10, 13]
];

// 앞면 익는 시간
const FIRST_COOK_MS = 2200;

// 뒷면 익는 시간
const SECOND_COOK_MS = 2000;

// 뒤집기 대기 및 완성 후 타기까지 시간
const BURN_WAIT_MS = 8000;

// ==========================================
// 재료
// ==========================================

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
    item => item.type === "filling"
);

const toppings = tools.filter(
    item => item.type === "topping"
);

// ==========================================
// 공통 도구
// ==========================================

const el = id =>
    document.getElementById(id);

const now = () =>
    performance.now();

const pick = array =>
    array[
        Math.floor(
            Math.random() * array.length
        )
    ];

const sleep = ms =>
    new Promise(resolve =>
        setTimeout(resolve, ms)
    );

let game = null;
let drag = null;
let highlighted = null;
let toastTimer = null;
let counting = false;

// ==========================================
// 안내 메시지
// ==========================================

function tell(message, type = "info") {

    const toast = el("toast");

    toast.className = "toast " + type;
    toast.textContent = message;

    void toast.offsetWidth;

    toast.classList.add("show");

    clearTimeout(toastTimer);

    toastTimer = setTimeout(() => {
        toast.classList.remove("show");
    }, 1800);
}

// ==========================================
// 손님 이미지
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
// 손님 생성
// ==========================================

function newCustomer() {

    const [min, max] =
        CUSTOMER_WAIT[game.level - 1];

    return {
        character:
            Math.floor(Math.random() * 5) + 1,

        fill: pick(fillings),

        top: pick(toppings),

        born: now(),

        patience: (
            min +
            Math.random() * (max - min)
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

// ==========================================
// 게임 시작
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
            () => ({
                state: "empty"
            })
        ),

        // 완성 접시 3개
        plates: [
            null,
            null,
            null
        ],

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
// 손님 출력
// ==========================================

function renderCustomers() {

    if (!game) return;

    el("customers").innerHTML =
        game.customers.map((customer, i) => `
            <div
                class="customer"
                id="customer-${i}"
                data-drop="customer"
                data-index="${i}">

                <div
                    class="bubble ${BUBBLE_STYLE}"
                    id="bubble-${i}">

                    ${orderText(customer)}

                </div>

                <img
                    class="avatar"
                    id="avatar-${i}"

                    src="${
                        imageFor(
                            customer.character,
                            "normal"
                        )
                    }"

                    data-expression="normal"
                    draggable="false">

                <div
                    class="customer-label"
                    id="label-${i}">

                    주문을 기다리는 중

                </div>

                <div class="patience">
                    <span
                        id="patience-${i}">
                    </span>
                </div>

            </div>
        `).join("");
}

// ==========================================
// 손님 표정과 대기 시간
// ==========================================

function updateCustomers(t) {

    if (!game) return;

    game.customers.forEach((customer, i) => {

        const avatar = el(`avatar-${i}`);
        const card = el(`customer-${i}`);
        const bar = el(`patience-${i}`);
        const label = el(`label-${i}`);
        const bubble = el(`bubble-${i}`);

        if (!avatar || !card || !bar) return;

        // 성공한 손님
        if (customer.happyUntil) {

            if (
                avatar.dataset.expression !== "happy"
            ) {
                avatar.src = imageFor(
                    customer.character,
                    "happy"
                );

                avatar.dataset.expression = "happy";
            }

            card.classList.add("happy");
            card.classList.remove("urgent");

            bubble.textContent =
                "맛있어요! 감사합니다!";

            label.textContent =
                "주문 성공!";

            bar.style.width = "100%";
            bar.style.background = "#70b963";

            return;
        }

        // 대기 시간 계산
        const percent = Math.max(
            0,
            100 * (
                1 -
                (t - customer.born) /
                customer.patience
            )
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
                customer.character,
                expression
            );

            avatar.dataset.expression = expression;
        }

        card.classList.remove("happy");

        card.classList.toggle(
            "urgent",
            percent <= 30
        );

        bubble.textContent =
            orderText(customer);

        label.textContent =
            percent <= 30
                ? "너무 오래 기다렸어요!"
                : percent <= 65
                ? "기다림이 길어지고 있어요..."
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
// 철판 출력
// ==========================================

function renderGrills() {

    if (!game) return;

    const icons = {
        empty: "⚫",
        batter: "🥣",
        cooking: "🟡",
        flip: "🍳",
        second: "🟤",

        // 조리 완료: 팬케이크 대신 후라이팬
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

    el("grills").innerHTML =
        game.grills.map((grill, i) => {

            const canDrag = [
                "ready",
                "burnt"
            ].includes(grill.state);

            const source = canDrag
                ? `
                    data-source="grill"
                    data-index="${i}"
                    data-emoji="🍳"
                    data-label="오코노미야끼"
                `
                : "";

            return `
                <div
                    class="grill ${grill.state}"
                    id="grill-${i}"

                    data-drop="grill"
                    data-index="${i}"

                    ${source}>

                    <div class="pancake">
                        ${icons[grill.state]}
                    </div>

                    <strong>
                        ${i + 1}번 철판
                    </strong>

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

// ==========================================
// 익기까지 / 타기까지 시간 표시
// ==========================================

function updateGrillBars(t) {

    if (!game) return;

    game.grills.forEach((grill, i) => {

        const bar = el(`cook-${i}`);

        const status = el(
            `grill-status-${i}`
        );

        const grillElement = el(
            `grill-${i}`
        );

        if (!bar || !status) return;

        let percent = 0;
        let color = "#efc456";

        let message = "반죽을 넣어 주세요";

        const passed = grill.since
            ? t - grill.since
            : 0;

        // 반죽
        if (grill.state === "batter") {
            message = "재료를 올려 주세요";
        }

        // 앞면 굽는 중
        else if (grill.state === "cooking") {

            const remaining = Math.max(
                0,
                FIRST_COOK_MS - passed
            );

            percent = Math.min(
                100,
                passed / FIRST_COOK_MS * 100
            );

            message =
                `앞면 익기까지 ` +
                `${(remaining / 1000).toFixed(1)}초`;

            color = "#efc456";
        }

        // 앞면이 익고 뒤집기 대기 중
        else if (grill.state === "flip") {

            const remaining = Math.max(
                0,
                BURN_WAIT_MS - passed
            );

            percent = Math.max(
                0,
                remaining / BURN_WAIT_MS * 100
            );

            message =
                `뒤집기! 타기까지 ` +
                `${(remaining / 1000).toFixed(1)}초`;

            color =
                remaining <= 1500
                    ? "#d9534f"
                    : "#f0a43a";
        }

        // 뒷면 굽는 중
        else if (grill.state === "second") {

            const remaining = Math.max(
                0,
                SECOND_COOK_MS - passed
            );

            percent = Math.min(
                100,
                passed / SECOND_COOK_MS * 100
            );

            message =
                `뒷면 익기까지 ` +
                `${(remaining / 1000).toFixed(1)}초`;

            color = "#efc456";
        }

        // 다 익은 음식
        else if (grill.state === "ready") {

            const remaining = Math.max(
                0,
                BURN_WAIT_MS - passed
            );

            percent = Math.max(
                0,
                remaining / BURN_WAIT_MS * 100
            );

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

        // 탄 음식
        else if (grill.state === "burnt") {
            percent = 0;
            color = "#d9534f";
            message = "🔥 음식이 탔어요!";
        }

        bar.style.width = percent + "%";
        bar.style.background = color;

        status.textContent = message;

        if (grillElement) {

            grillElement.classList.toggle(
                "urgent",

                (
                    grill.state === "flip" ||
                    grill.state === "ready"
                ) &&
                BURN_WAIT_MS - passed <= 1500
            );
        }
    });
}

// ==========================================
// 완성 접시 3개
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
        game.plates.map((plate, i) => {

            // 빈 접시
            if (!plate) {
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

            // 음식이 담긴 접시
            const complete = Boolean(
                plate.top
            );

            const description =
                plate.fill.name +
                (
                    plate.top
                        ? " + " + plate.top.name
                        : ""
                );

            return `
                <div
                    class="plate ${
                        complete ? "ready" : ""
                    }"

                    data-drop="plate"
                    data-index="${i}"

                    data-source="plate"
                    data-emoji="🍳"
                    data-label="오코노미야끼">

                    <span class="plate-number">
                        ${i + 1}
                    </span>

                    🍳

                    <small>
                        ${description}
                    </small>

                </div>
            `;
        }).join("");

    // 안내 메시지
    const occupied = game.plates.filter(
        plate => plate !== null
    ).length;

    if (occupied === 0) {
        el("plate-help").textContent =
            "익은 오코노미야끼를 빈 접시에 올려 주세요";
    } else if (
        game.plates.some(
            plate => plate && !plate.top
        )
    ) {
        el("plate-help").textContent =
            "접시에 토핑을 올려 주세요";
    } else {
        el("plate-help").textContent =
            "완성된 음식을 손님에게 서빙하세요";
    }
}

// ==========================================
// 재료 및 도구 출력
// ==========================================

function renderItems() {

    el("ingredients").innerHTML =
        ingredients.map((item, i) => `
            <div
                class="item"

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
            <div
                class="item"

                data-source="tool"
                data-index="${i}"

                data-emoji="${item.emoji}"
                data-label="${item.name}">

                <span>${item.emoji}</span>
                ${item.name}

            </div>
        `).join("");
}

// ==========================================
// 전체 화면 갱신
// ==========================================

function renderAll() {
    updateHud();
    renderCustomers();
    renderGrills();
    renderPlates();
    renderItems();
    updateGrillBars(now());
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
// 접시별 손님 서빙
// ==========================================

function serve(customerIndex, plateIndex) {

    const customer =
        game.customers[customerIndex];

    const plate =
        game.plates[plateIndex];

    if (!customer || customer.happyUntil) {
        return;
    }

    if (!plate || !plate.top) {

        tell(
            "토핑까지 완성한 음식을 서빙하세요!",
            "warning"
        );

        return;
    }

    const correct =
        plate.fill.name === customer.fill.name &&
        plate.top.name === customer.top.name;

    // 사용한 접시만 비우기
    game.plates[plateIndex] = null;

    renderPlates();

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

        customer.happyUntil = now() + 850;

        updateHud();
        updateCustomers(now());

        tell(
            "✅ 주문 성공! 맛있게 드세요!",
            "success"
        );

    } else {

        game.missed++;

        loseLife(
            "❌ 주문이 틀렸어요!"
        );

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

function handleDrop(
    kind,
    index,
    target,
    targetIndex
) {

    if (!game || game.ended) return;

    // ======================================
    // 1. 반죽 / 재료 → 철판
    // ======================================

    if (
        kind === "ingredient" &&
        target === "grill"
    ) {

        const item = ingredients[index];
        const grill = game.grills[targetIndex];

        if (!item || !grill) return;

        // 반죽 넣기
        if (
            item.type === "batter" &&
            grill.state === "empty"
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

        // 재료 올리기 → 앞면 조리 시작
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

    // ======================================
    // 2. 뒤집개 → 철판
    // ======================================

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

    // ======================================
    // 3. 완성된 철판 → 빈 접시
    // ======================================

    if (
        kind === "grill" &&
        target === "plate"
    ) {

        const grill = game.grills[index];
        const plate = game.plates[targetIndex];

        if (
            !grill ||
            grill.state !== "ready"
        ) {

            tell(
                "다 익은 오코노미야끼만 접시에 담을 수 있어요!",
                "warning"
            );

            return;
        }

        if (plate !== null) {

            tell(
                "그 접시는 이미 사용 중이에요!",
                "warning"
            );

            return;
        }

        // 선택한 빈 접시에 음식 보관
        game.plates[targetIndex] = {
            fill: grill.fill,
            top: null
        };

        // 사용한 철판 비우기
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

    // ======================================
    // 4. 토핑 → 선택한 접시
    // ======================================

    if (
        kind === "tool" &&
        target === "plate"
    ) {

        const tool = tools[index];

        const plate = game.plates[targetIndex];

        if (!tool) return;

        if (tool.type !== "topping") {

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

        // 접시마다 독립적으로 토핑 선택
        plate.top = tool;

        renderPlates();

        tell(
            "✅ 토핑 완료! 손님에게 서빙하세요.",
            "success"
        );

        return;
    }

    // ======================================
    // 5. 접시 → 손님
    // ======================================

    if (
        kind === "plate" &&
        target === "customer"
    ) {

        serve(
            targetIndex,
            index
        );

        return;
    }

    // ======================================
    // 6. 접시 또는 철판 → 휴지통
    // ======================================

    if (target === "trash") {

        if (kind === "plate") {

            // 선택한 접시만 비우기
            game.plates[index] = null;

            renderPlates();

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

function moveGhost(event) {

    if (!drag) return;

    drag.ghost.style.left =
        (event.clientX + 12) + "px";

    drag.ghost.style.top =
        (event.clientY + 12) + "px";

    if (highlighted) {
        highlighted.classList.remove(
            "drop-over"
        );
    }

    highlighted = document.elementFromPoint(
        event.clientX,
        event.clientY
    )?.closest("[data-drop]");

    if (highlighted) {
        highlighted.classList.add(
            "drop-over"
        );
    }
}

document.addEventListener(
    "pointerdown",
    event => {

        if (
            !game ||
            game.ended ||
            drag ||
            counting
        ) {
            return;
        }

        const source = event.target.closest(
            "[data-source]"
        );

        if (!source) return;

        event.preventDefault();

        const ghost =
            document.createElement("div");

        ghost.className = "ghost";

        ghost.innerHTML = `
            ${source.dataset.emoji || "🍳"}

            <small>
                ${source.dataset.label || ""}
            </small>
        `;

        document.body.appendChild(ghost);

        drag = {
            pointerId: event.pointerId,

            source,

            kind: source.dataset.source,

            index: Number(
                source.dataset.index || 0
            ),

            ghost
        };

        source.classList.add(
            "dragging-original"
        );

        moveGhost(event);
    }
);

document.addEventListener(
    "pointermove",
    event => {

        if (
            drag &&
            drag.pointerId === event.pointerId
        ) {
            event.preventDefault();
            moveGhost(event);
        }
    },
    {
        passive: false
    }
);

// 드롭 완료

function releaseDrag(event) {

    if (
        !drag ||
        drag.pointerId !== event.pointerId
    ) {
        return;
    }

    const previousDrag = drag;

    const target = document.elementFromPoint(
        event.clientX,
        event.clientY
    )?.closest("[data-drop]");

    previousDrag.ghost.remove();

    if (previousDrag.source.isConnected) {
        previousDrag.source.classList.remove(
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
            previousDrag.kind,
            previousDrag.index,
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

// 드래그 취소

document.addEventListener(
    "pointercancel",
    event => {

        if (
            !drag ||
            drag.pointerId !== event.pointerId
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
// 다음 레벨
// ==========================================

function nextLevel() {

    if (!game || game.ended) return;

    if (game.level === 5) {
        endGame(true);
        return;
    }

    game.level++;

    game.levelStart = now();

    // 철판 초기화
    game.grills = Array.from(
        {length: 3},
        () => ({
            state: "empty"
        })
    );

    // 접시 3개 초기화
    game.plates = [
        null,
        null,
        null
    ];

    // 손님 초기화
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
        won
            ? "최종 승리!"
            : "게임 오버!";

    el("panel-text").innerHTML = `
        도달 레벨: ${game.level}/5<br>
        성공한 주문: ${game.served}개<br>
        최종 점수: ${game.score}점<br>
        최고 콤보: ${game.best}회<br>
        놓친 주문: ${game.missed}개
    `;

    el("start-button").textContent =
        "🔄 다시 도전하기";

    el("overlay").classList.remove(
        "hidden"
    );
}

// ==========================================
// 조리 및 게임 타이머
// ==========================================

function tick() {

    if (!game || game.ended || counting) {
        return;
    }

    const t = now();

    // 레벨 남은 시간
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

    // ======================================
    // 철판 상태 변경
    // ======================================

    let grillsChanged = false;

    game.grills.forEach(grill => {

        if (
            ![
                "cooking",
                "flip",
                "second",
                "ready"
            ].includes(grill.state)
        ) {
            return;
        }

        const passed = t - grill.since;

        // 앞면 익음
        if (
            grill.state === "cooking" &&
            passed >= FIRST_COOK_MS
        ) {
            grill.state = "flip";
            grill.since = t;

            grillsChanged = true;
            return;
        }

        // 뒷면 익음
        if (
            grill.state === "second" &&
            passed >= SECOND_COOK_MS
        ) {
            grill.state = "ready";
            grill.since = t;

            grillsChanged = true;
            return;
        }

        // 뒤집기 전이나 완성 후
        // 대기 시간이 지나면 탐
        if (
            (
                grill.state === "flip" ||
                grill.state === "ready"
            ) &&
            passed >= BURN_WAIT_MS
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

    if (grillsChanged) {
        renderGrills();
    }

    updateGrillBars(t);

    // ======================================
    // 손님 대기 시간
    // ======================================

    let customersChanged = false;

    for (
        let i = 0;
        i < game.customers.length;
        i++
    ) {

        const customer = game.customers[i];

        // 주문 성공 후 새 손님 등장
        if (customer.happyUntil) {

            if (t >= customer.happyUntil) {

                game.customers[i] =
                    newCustomer();

                customersChanged = true;
            }

            continue;
        }

        // 손님이 기다리다 떠남
        if (
            t - customer.born >=
            customer.patience
        ) {

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
}

// ==========================================
// 게임 시작 전 화면
// ==========================================

function initializeScreen() {

    renderItems();

    // 시작 전 손님
    el("customers").innerHTML =
        Array.from(
            {length: 3},
            (_, i) => `
                <div class="customer">

                    <div
                        class="bubble ${BUBBLE_STYLE}">

                        게임 시작 후 주문이 나타나요!

                    </div>

                    <img
                        class="avatar"

                        src="${
                            imageFor(
                                i + 1,
                                "normal"
                            )
                        }"

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

    // 시작 전 철판
    el("grills").innerHTML =
        Array.from(
            {length: 3},
            (_, i) => `
                <div class="grill">

                    <div class="pancake">
                        ⚫
                    </div>

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

    // 시작 전 접시 3개
    renderPlates();
}

// ==========================================
// 실행
// ==========================================

initializeScreen();

setInterval(
    tick,
    100
);

</script>

</body>
</html>
"""

# ==========================================
# Python 설정을 HTML에 전달
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
# 배경 꾸미기 이미지 연결
# ==========================================

if background_url:

    background_css = """
    <style>
    .game {
        background-image:
            url("__BACKGROUND_URL__") !important;

        background-position:
            center center !important;

        background-size:
            cover !important;

        background-repeat:
            no-repeat !important;
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

# ==========================================
# 게임 출력
# ==========================================

components.html(
    GAME_HTML,
    height=700,
    scrolling=False,
)




