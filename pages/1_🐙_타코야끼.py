
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json

from game_unlock import listen_for_takoyaki_clear

# ==========================================
# 와글와글 포장마차 - 타코야끼
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


# ==========================================
# 이미지 파일 로딩
# ==========================================

def to_data_url(path):
    if not path.is_file():
        return ""

    data = base64.b64encode(
        path.read_bytes()
    ).decode("ascii")

    return "data:image/png;base64," + data


customer_images = {}
customer_folder = (
    ROOT / "assets" / "customers" / customer_theme
)

for number in range(1, 6):
    for mood in (
        "normal", "waiting", "angry", "happy"
    ):
        filename = (
            f"{customer_theme}_{number:02d}_{mood}.png"
        )
        customer_images[f"{number}_{mood}"] = (
            to_data_url(customer_folder / filename)
        )


ingredient_files = [
    "batter.png",
    "octopus.png",
    "cheese.png",
    "bonito.png",
    "sauce.png",
    "mentai_mayo.png",
]

ingredient_images = {
    name: to_data_url(
        ROOT / "assets" / "ingredients" / name
    )
    for name in ingredient_files
}


food_files = [
    "takoyaki_plain.png",
    "takoyaki_bonito.png",
    "takoyaki_original.png",
    "takoyaki_mentai.png",
]

food_images = {
    name: to_data_url(
        ROOT / "assets" / "foods" / name
    )
    for name in food_files
}

background_url = to_data_url(
    ROOT / background_file
)

missing = [
    name
    for name, url in {
        **ingredient_images,
        **food_images,
    }.items()
    if not url
]

if missing:
    st.warning(
        "이미지 파일을 찾을 수 없습니다: "
        + ", ".join(missing)
    )


st.html("""
<style>
[data-testid="stAppViewContainer"] {
    background: #fff0d8;
}
[data-testid="stMain"] .block-container {
    max-width: 100% !important;
    padding: .25rem .5rem !important;
}
iframe {
    border: 0 !important;
    display: block;
}
</style>
""")


# ==========================================
# 게임 화면
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
    overflow: hidden;
    border-radius: 18px;
    background: linear-gradient(
        #88a0c6, #f2c1aa 52%, #f6d5a0
    );
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

/* 상단 */

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 45px;
    gap: 8px;
}

.logo {
    padding: 8px 12px;
    background: #fff0ce;
    color: #964b30;
    border: 3px solid #a85d37;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 900;
    white-space: nowrap;
}

.stats {
    display: flex;
    gap: 6px;
}

.stat {
    min-width: 68px;
    padding: 5px 8px;
    border: 2px solid #f6d6a0;
    border-radius: 12px;
    background: #784d3d;
    color: white;
    text-align: center;
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

/* 안내 메시지 */

.notice-area {
    height: 43px;
    margin: 2px 0 4px;
    display: grid;
    place-items: center;
    pointer-events: none;
}

.toast {
    max-width: 90%;
    min-height: 34px;
    padding: 8px 20px;
    background: #8b5a3c;
    color: white;
    border: 2px solid #fff3d9;
    border-radius: 12px;
    text-align: center;
    font-size: 13px;
    font-weight: 900;
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
    border-radius: 12px;
    font-size: 16px;
    font-weight: 900;
    text-align: center;
}

/* 손님 */

.customers {
    display: grid;
    grid-template-columns:
        repeat(3, minmax(0, 1fr));
    width: 100%;
    max-width: 1050px;
    height: 160px;
    margin: 0 auto 7px;
    gap: 8px;
}

.customer {
    min-width: 0;
    padding: 0 3px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    text-align: center;
}

.bubble {
    position: relative;
    z-index: 2;
    width: 96%;
    max-width: 260px;
    min-height: 44px;
    margin-bottom: 5px;
    padding: 5px 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #fffdf5;
    font-size: 11px;
    font-weight: 900;
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
    left: calc(50% - 6px);
    bottom: -8px;
    width: 12px;
    height: 12px;
    background: inherit;
    transform: rotate(45deg);
    border-right: 2px solid #d9ab83;
    border-bottom: 2px solid #d9ab83;
}

/* 주문 이미지 */

.order-content,
.order-part,
.order-images {
    display: flex;
    align-items: center;
    justify-content: center;
}

.order-content {
    width: 100%;
    min-width: 0;
    gap: 5px;
}

.order-part {
    min-width: 0;
    flex: 1;
    gap: 3px;
}

.order-images {
    flex-shrink: 0;
    gap: 1px;
}

.order-images img {
    width: 23px;
    height: 25px;
    object-fit: contain;
    pointer-events: none;
}

.order-images.double img {
    width: 17px;
    height: 23px;
}

.order-name {
    font-size: 10px;
    white-space: nowrap;
}

.order-plus {
    color: #c17b48;
    font-size: 15px;
}

.customers.four .bubble {
    padding: 4px 2px;
}

.customers.four .order-content {
    gap: 2px;
}

.customers.four .order-part {
    gap: 1px;
}

.customers.four .order-images img {
    width: 18px;
    height: 21px;
}

.customers.four .order-images.double img {
    width: 14px;
    height: 19px;
}

.customers.four .order-name {
    font-size: 9px;
}

.avatar {
    width: min(130px, 100%);
    height: 83px;
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
    width: 100%;
    height: 100%;
    background: #70b963;
}

.customer.urgent .bubble {
    border-color: #d9655b;
}

.customer.happy .avatar {
    filter: drop-shadow(0 0 7px #ffe46a);
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
    grid-template-columns:
        repeat(3, minmax(0, 1fr));
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
    min-width: 0;
    min-height: 132px;
    gap: 4px;
    padding: 5px 3px;
    background: #28282c;
    color: #fff5da;
    border: 2px solid #686268;
    border-radius: 13px;
    text-align: center;
}

.grill.ready { border-color: #62b780; }
.grill.burnt { border-color: #87493d; }
.grill.urgent { border-color: #e76b5d; }

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

/* 빈 철판은 기존 구멍 형태 유지 */

.holes {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 3px;
    width: min(95px, 95%);
    pointer-events: none;
}

.ball {
    aspect-ratio: 1;
    border-radius: 50%;
    background: #15161a;
    border: 2px solid #111219;
}

/* 조리 중에는 새 음식 디자인 사용 */

.grill-food {
    width: 95px;
    max-width: 90%;
    height: 57px;
    object-fit: contain;
    pointer-events: none;
    user-select: none;
}

.grill.cooking .grill-food {
    opacity: .82;
    filter: saturate(.75);
}

.grill.ready .grill-food {
    filter: drop-shadow(0 2px 3px #0005);
}

.grill-burnt {
    display: grid;
    place-items: center;
    width: 95px;
    height: 57px;
    font-size: 35px;
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
    width: 0%;
    height: 100%;
    background: #efc456;
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
    padding: 6px;
    background: #fff1d9;
    border: 3px solid #e5bd8f;
    border-radius: 13px;
    text-align: center;
}

.plate-zone strong {
    font-size: 12px;
}

#plate-help {
    font-size: 10px;
}

.plates {
    display: grid;
    grid-template-columns:
        repeat(3, minmax(0, 1fr));
    gap: 5px;
    margin: 5px auto;
}

.plate {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-width: 0;
    min-height: 85px;
    padding: 5px 2px;
    gap: 3px;
    border: 2px solid #c8b5a2;
    border-radius: 12px;
    background: radial-gradient(
        circle,
        white 0 48%,
        #b7d6e2 50% 60%,
        white 62%
    );
    font-size: 21px;
    font-weight: 900;
}

.plate.ready {
    border-color: #79ad6a;
}

.plate small {
    font-size: 9px;
    line-height: 1.2;
    overflow-wrap: anywhere;
    pointer-events: none;
}

.plate-number {
    position: absolute;
    top: 2px;
    left: 4px;
    font-size: 9px;
    pointer-events: none;
}

.plate-food {
    width: 72px;
    max-width: 95%;
    height: 55px;
    display: block;
    object-fit: contain;
    pointer-events: none;
}

.trash {
    display: grid;
    place-items: center;
    min-height: 35px;
    padding: 5px;
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

/* 새 PNG 조리 순서 안내 */

.help {
    max-width: 1200px;
    margin: 7px auto 0;
    padding: 5px 8px;
    background: #fff4da;
    border: 2px solid #d8ab75;
    border-radius: 10px;
}

.help-title {
    font-size: 11px;
    font-weight: 900;
    text-align: center;
}

.guide {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 5px;
}

.guide-step {
    display: flex;
    align-items: center;
    gap: 3px;
    font-size: 10px;
    font-weight: 900;
    white-space: nowrap;
}

.guide-step img {
    width: 25px;
    height: 25px;
    object-fit: contain;
}

.guide-step img.food-icon {
    width: 35px;
}

.guide-arrow {
    color: #b7794c;
    font-size: 15px;
    font-weight: 900;
}

/* 드래그 */

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
    padding: 8px;
    border: 3px solid #d9a16b;
    border-radius: 14px;
    background: #fff8e7;
    box-shadow: 0 5px 12px #0004;
    pointer-events: none;
    text-align: center;
    font-size: 24px;
}

.ghost .ingredient-art img {
    width: 45px;
    height: 45px;
}

.ghost .plate-food {
    width: 95px;
    height: 75px;
}

.ghost small {
    display: block;
    font-size: 11px;
}

/* 시작 및 종료 */

.overlay,
.countdown {
    position: absolute;
    inset: 0;
    padding: 15px;
    align-items: center;
    justify-content: center;
    background: #241b20bc;
}

.overlay {
    z-index: 35;
    display: flex;
}

.overlay.hidden {
    display: none;
}

.panel {
    width: min(460px, 95%);
    padding: 30px 20px;
    background: #fff4d9;
    border: 6px solid #bc7950;
    border-radius: 25px;
    box-shadow: 0 10px #7c4d37;
    text-align: center;
}

.panel h2 {
    color: #954a33;
}

.panel p {
    font-size: 15px;
    font-weight: 900;
    line-height: 1.8;
}

.start {
    padding: 14px 25px;
    background: #e8734c;
    color: white;
    border: none;
    border-radius: 15px;
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

.countdown.show {
    display: flex;
}

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

@media(max-width:900px) {
    .game { padding: 6px; }
    .logo { font-size: 12px; }
    .stat {
        min-width: 48px;
        padding: 4px;
        font-size: 12px;
    }
    .stat small { font-size: 8px; }
    .order-images img {
        width: 19px;
        height: 22px;
    }
    .order-name { font-size: 9px; }
    .avatar { width: min(110px,100%); }
    .kitchen {
        grid-template-columns:
            minmax(0,1.3fr)
            minmax(205px,1fr);
    }
    .grills { gap: 3px; padding: 4px; }
    .grill-food {
        width: 70px;
        height: 50px;
    }
    .item { font-size: 10px; }
    .ingredient-art img { height: 32px; }
    .plate-food { height: 45px; }
    .guide-step { font-size: 9px; }
    .guide-step img {
        width: 21px;
        height: 21px;
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
        🐙 타코야끼 가게 🐙
    </div>

    <div class="customers" id="customers"></div>

    <div class="counter">
        <h3>🍳 타코야끼 조리대</h3>

        <div class="kitchen">
            <div class="grills" id="grills"></div>

            <div class="right">
                <div class="plate-zone">
                    <strong>완성 접시 3개</strong>
                    <div class="plates" id="plates"></div>
                    <small id="plate-help">
                        익은 타코야끼를 접시에 올려 주세요
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
            <h3>반죽 + 문어 / 선택 재료</h3>
            <div class="items" id="fillings"></div>
        </div>

        <div class="supply">
            <h3>가쓰오부시 / 소스</h3>
            <div class="items" id="toppings"></div>
        </div>
    </div>

    <div class="help">
        <div class="help-title">조리 순서</div>
        <div class="guide" id="guide"></div>
    </div>

    <div class="overlay" id="overlay">
        <div class="panel">
            <div id="panel-icon"
                 style="font-size:58px">🐙</div>

            <h2 id="panel-title">타코야끼 가게</h2>

            <p id="panel-text">
                반죽과 문어는 기본 재료예요.<br>
                치즈는 선택할 수 있어요.<br>
                가쓰오부시는 꼭 올려 주세요.<br>
                목숨 3개 · 총 5레벨<br>
                익는 시간 6초 · 익은 후 15초 뒤에 타요.<br>
                레벨마다 목숨이 다시 3개로 회복돼요.
            </p>

            <button class="start"
                    id="start-button"
                    onclick="beginCountdown()">
                🎮 타코야끼 만들기
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
// ==========================================
// 게임 설정
// ==========================================

const CUSTOMER_IMAGES = __CUSTOMERS__;
const INGREDIENT_IMAGES = __INGREDIENTS__;
const FOOD_IMAGES = __FOODS__;
const BUBBLE_STYLE = __BUBBLE__;

const LEVEL_TIMES = [50, 55, 60, 65, 70];
const CUSTOMER_COUNT = [3, 3, 3, 4, 4];

// 변경된 손님 대기 시간
const CUSTOMER_WAIT = [
    [45, 50],
    [40, 45],
    [35, 40],
    [30, 35],
    [25, 30]
];

const COOK_MS = 6000;
const READY_TIME_MS = 15000;
const BURN_MS = COOK_MS + READY_TIME_MS;
const MAX_LIVES = 3;

const fillings = [
    {
        id: "base",
        name: "반죽 + 문어",
        type: "base",
        images: ["batter.png", "octopus.png"]
    },
    {
        id: "cheese",
        name: "치즈 추가",
        type: "cheese",
        images: ["cheese.png"]
    }
];

const toppings = [
    {
        id: "katsu",
        name: "가쓰오부시",
        type: "katsu",
        images: ["bonito.png"]
    },
    {
        id: "original",
        name: "오리지널",
        type: "sauce",
        images: ["sauce.png"]
    },
    {
        id: "mentai",
        name: "명란마요",
        type: "sauce",
        images: ["mentai_mayo.png"]
    }
];

const el = id => document.getElementById(id);
const now = () => performance.now();
const sleep = ms => new Promise(r => setTimeout(r, ms));

let game = null;
let drag = null;
let highlighted = null;
let counting = false;
let toastTimer = null;

// ==========================================
// PNG 표시 함수
// ==========================================

function imageTag(url, className = "", alt = "") {
    if (!url) return "";
    return `<img class="${className}" src="${url}"
                 alt="${alt}" draggable="false">`;
}

function ingredientMarkup(files, fallback = "재료") {
    const images = files
        .filter(name => INGREDIENT_IMAGES[name])
        .map(name => imageTag(INGREDIENT_IMAGES[name]))
        .join("");

    return `
        <span class="ingredient-art">
            ${images || fallback}
        </span>
    `;
}

function foodFilename(plate) {
    if (plate.sauce === "original") {
        return "takoyaki_original.png";
    }
    if (plate.sauce === "mentai") {
        return "takoyaki_mentai.png";
    }
    if (plate.katsu) {
        return "takoyaki_bonito.png";
    }
    return "takoyaki_plain.png";
}

function foodMarkup(filename, className = "plate-food") {
    const url = FOOD_IMAGES[filename];
    return url
        ? imageTag(url, className, "타코야끼")
        : `<span>타코야끼</span>`;
}

function imageFor(number, mood) {
    return (
        CUSTOMER_IMAGES[`${number}_${mood}`] ||
        CUSTOMER_IMAGES[`${number}_normal`] ||
        ""
    );
}

// ==========================================
// 새 조리 순서 안내
// ==========================================

function guideImage(filename, isFood = false) {
    const source = isFood
        ? FOOD_IMAGES[filename]
        : INGREDIENT_IMAGES[filename];

    return source
        ? imageTag(
            source,
            isFood ? "food-icon" : "",
            filename
        )
        : "";
}

function renderGuide() {
    el("guide").innerHTML = `
        <span class="guide-step">
            ${guideImage("batter.png")}
            ${guideImage("octopus.png")}
            반죽+문어
        </span>

        <span class="guide-arrow">→</span>

        <span class="guide-step">
            ${guideImage("cheese.png")}
            치즈 선택
        </span>

        <span class="guide-arrow">→</span>

        <span class="guide-step">
            ${guideImage("takoyaki_plain.png", true)}
            6초 굽기
        </span>

        <span class="guide-arrow">→</span>

        <span class="guide-step">
            ${guideImage("bonito.png")}
            가쓰오부시
        </span>

        <span class="guide-arrow">→</span>

        <span class="guide-step">
            ${guideImage("sauce.png")}
            ${guideImage("mentai_mayo.png")}
            소스 선택
        </span>

        <span class="guide-arrow">→</span>

        <span class="guide-step">손님에게 서빙</span>
    `;
}

// ==========================================
// 손님 주문 이미지
// ==========================================

function orderImage(files) {
    const valid = files.filter(
        name => INGREDIENT_IMAGES[name]
    );

    const images = valid.map(name =>
        imageTag(INGREDIENT_IMAGES[name])
    ).join("");

    return `
        <span class="order-images ${
            valid.length > 1 ? "double" : ""
        }">
            ${images}
        </span>
    `;
}

function orderMarkup(customer) {
    const fillFiles = customer.cheese
        ? ["cheese.png"]
        : ["batter.png", "octopus.png"];

    const fillName = customer.cheese
        ? "치즈"
        : "기본";

    const sauceFile = customer.sauce === "original"
        ? "sauce.png"
        : "mentai_mayo.png";

    const sauceName = customer.sauce === "original"
        ? "오리지널"
        : "명란마요";

    return `
        <div class="order-content">
            <span class="order-part">
                ${orderImage(fillFiles)}
                <span class="order-name">${fillName}</span>
            </span>

            <span class="order-plus">+</span>

            <span class="order-part">
                ${orderImage([sauceFile])}
                <span class="order-name">${sauceName}</span>
            </span>
        </div>
    `;
}

// ==========================================
// 안내 메시지
// ==========================================

function tell(message, type = "info") {
    const box = el("toast");
    box.textContent = message;
    box.className = `toast ${type} show`;

    clearTimeout(toastTimer);
    toastTimer = setTimeout(
        () => box.classList.remove("show"),
        1800
    );
}

// ==========================================
// 손님 생성
// ==========================================

function newCustomer() {
    const [min, max] = CUSTOMER_WAIT[game.level - 1];

    return {
        character: Math.floor(Math.random() * 5) + 1,
        cheese: Math.random() < .5,
        sauce: Math.random() < .5
            ? "original" : "mentai",
        born: now(),
        patience: (
            min + Math.random() * (max - min)
        ) * 1000,
        happyUntil: 0
    };
}

function createNewGame() {
    game = {
        level: 1,
        levelStart: 0,
        lives: MAX_LIVES,
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
        ended: false,
        paused: true
    };
}

// ==========================================
// 시작 및 레벨 이동
// ==========================================

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
        `LEVEL ${game.level}`;
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
    el("time").textContent =
        LEVEL_TIMES[game.level - 1];

    el("countdown").classList.remove("show");
    counting = false;

    tell(`${game.level}레벨 영업 시작!`);
}

function nextLevel() {
    if (!game || game.ended || game.paused) return;

    if (game.level === 5) {
        endGame(true);
        return;
    }

    game.level++;
    game.lives = MAX_LIVES;
    game.combo = 0;
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

// ==========================================
// 게임 정보
// ==========================================

function updateHud() {
    if (!game) return;

    el("level").textContent = game.level;
    el("score").textContent = game.score;
    el("lives").textContent =
        "❤️".repeat(game.lives);
}

// ==========================================
// 손님 표시
// ==========================================

function renderCustomers() {
    if (!game) return;

    const area = el("customers");
    const count = game.customers.length;

    area.style.gridTemplateColumns =
        `repeat(${count}, minmax(0, 1fr))`;
    area.classList.toggle("four", count === 4);

    area.innerHTML = game.customers.map((c, i) => `
        <div class="customer"
             id="customer-${i}"
             data-drop="customer"
             data-index="${i}">

            <div class="bubble ${BUBBLE_STYLE}"
                 id="bubble-${i}">
                ${orderMarkup(c)}
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

function updateCustomers(t) {
    if (!game) return;

    game.customers.forEach((c, i) => {
        const avatar = el(`avatar-${i}`);
        const card = el(`customer-${i}`);
        const label = el(`label-${i}`);
        const bar = el(`patience-${i}`);
        const bubble = el(`bubble-${i}`);

        if (!avatar || !bar || !bubble) return;

        if (c.happyUntil) {
            if (avatar.dataset.expression !== "happy") {
                avatar.src = imageFor(c.character, "happy");
                avatar.dataset.expression = "happy";
            }

            card.classList.add("happy");
            card.classList.remove("urgent");

            if (bubble.dataset.state !== "happy") {
                bubble.textContent = "맛있어요! 감사합니다!";
                bubble.dataset.state = "happy";
            }

            label.textContent = "주문 성공!";
            bar.style.width = "100%";
            bar.style.background = "#70b963";
            return;
        }

        const percent = Math.max(
            0,
            100 * (1 - (t - c.born) / c.patience)
        );

        const mood = percent <= 30
            ? "angry"
            : percent <= 65
            ? "waiting"
            : "normal";

        if (avatar.dataset.expression !== mood) {
            avatar.src = imageFor(c.character, mood);
            avatar.dataset.expression = mood;
        }

        card.classList.remove("happy");
        card.classList.toggle(
            "urgent", percent <= 30
        );

        if (bubble.dataset.state === "happy") {
            bubble.innerHTML = orderMarkup(c);
            bubble.dataset.state = "order";
        }

        label.textContent = percent <= 30
            ? "너무 오래 기다렸어요!"
            : percent <= 65
            ? "기다림이 길어지고 있어요..."
            : "주문을 기다리는 중";

        bar.style.width = percent + "%";
        bar.style.background = percent <= 30
            ? "#dc6753"
            : percent <= 65
            ? "#e8b64a"
            : "#70b963";
    });
}

// ==========================================
// 조리판 - PNG 디자인 적용
// ==========================================

function grillVisual(grill) {
    if (grill.state === "empty") {
        return `
            <div class="holes">
                ${'<span class="ball"></span>'.repeat(6)}
            </div>
        `;
    }

    if (grill.state === "burnt") {
        return `<div class="grill-burnt">🔥</div>`;
    }

    // 조리 중과 완성 상태 모두 새 타코야끼 디자인
    return foodMarkup(
        "takoyaki_plain.png",
        "grill-food"
    );
}

function renderGrills() {
    if (!game) return;

    const messages = {
        empty: "반죽을 넣어 주세요",
        cooking: "익는 중...",
        ready: "다 익었어요!",
        burnt: "음식이 탔어요!"
    };

    el("grills").innerHTML =
        game.grills.map((grill, i) => {

            const draggable = (
                grill.state === "ready" ||
                grill.state === "burnt"
            );

            const source = draggable ? `
                data-source="grill"
                data-index="${i}"
                data-label="타코야끼"
            ` : "";

            const fillingName = grill.cheese
                ? "치즈"
                : "기본";

            return `
                <div class="grill ${grill.state}"
                     id="grill-${i}"
                     data-drop="grill"
                     data-index="${i}"
                     ${source}>

                    ${grillVisual(grill)}

                    <strong>
                        ${i + 1}번 조리판
                        ${grill.state !== "empty"
                            ? " · " + fillingName
                            : ""}
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
// 조리판 시간
// ==========================================

function updateGrillBars(t) {
    if (!game) return;

    game.grills.forEach((grill, i) => {
        const bar = el(`cook-${i}`);
        const status = el(`grill-status-${i}`);
        const card = el(`grill-${i}`);

        if (!bar || !status) return;

        let percent = 0;
        let color = "#efc456";
        let message = "반죽을 넣어 주세요";

        if (grill.state === "cooking") {
            const elapsed = t - grill.born;
            const remain = Math.max(
                0, COOK_MS - elapsed
            );

            percent = Math.min(
                100, elapsed / COOK_MS * 100
            );

            message =
                `익기까지 ${(remain / 1000).toFixed(1)}초`;

        } else if (grill.state === "ready") {
            const remain = Math.max(
                0, BURN_MS - (t - grill.born)
            );

            percent =
                remain / READY_TIME_MS * 100;

            const seconds = Math.ceil(remain / 1000);

            color = seconds <= 3
                ? "#d9534f"
                : seconds <= 6
                ? "#f0a43a"
                : "#4fa568";

            message = seconds <= 3
                ? `곧 타요! ${seconds}초`
                : `타기까지 ${seconds}초`;

        } else if (grill.state === "burnt") {
            color = "#d9534f";
            message = "음식이 탔어요!";
        }

        bar.style.width = percent + "%";
        bar.style.background = color;
        status.textContent = message;

        if (card) {
            card.classList.toggle(
                "urgent",
                grill.state === "ready" &&
                BURN_MS - (t - grill.born) <= 3000
            );
        }
    });
}

// ==========================================
// 접시 - 음식 PNG 4종
// ==========================================

function renderPlates() {
    const area = el("plates");

    if (!game) {
        area.innerHTML = Array.from(
            {length: 3},
            (_, i) => `
                <div class="plate">
                    <span class="plate-number">${i + 1}</span>
                    🍽️
                    <small>빈 접시</small>
                </div>
            `
        ).join("");
        return;
    }

    area.innerHTML = game.plates.map((plate, i) => {
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

        const filename = foodFilename(plate);
        const complete = plate.katsu && plate.sauce;

        let stage = "기본";
        if (plate.katsu) stage = "가쓰오부시";
        if (plate.sauce === "original") {
            stage = "오리지널";
        }
        if (plate.sauce === "mentai") {
            stage = "명란마요";
        }

        return `
            <div class="plate ${complete ? "ready" : ""}"
                 data-drop="plate"
                 data-index="${i}"
                 data-source="plate"
                 data-food="${filename}"
                 data-label="타코야끼">

                <span class="plate-number">
                    ${i + 1}
                </span>

                ${foodMarkup(filename)}

                <small>
                    ${plate.cheese ? "치즈" : "기본"}
                    · ${stage}
                </small>
            </div>
        `;
    }).join("");

    if (game.plates.some(
        p => p && (!p.katsu || !p.sauce)
    )) {
        el("plate-help").textContent =
            "가쓰오부시와 소스를 올려 주세요";
    } else if (game.plates.some(Boolean)) {
        el("plate-help").textContent =
            "완성된 음식을 손님에게 서빙하세요";
    } else {
        el("plate-help").textContent =
            "익은 타코야끼를 접시에 올려 주세요";
    }
}

// ==========================================
// 재료
// ==========================================

function renderSupplies() {
    el("fillings").innerHTML =
        fillings.map((item, i) => `
            <div class="item"
                 data-source="filling"
                 data-index="${i}"
                 data-images="${item.images.join(",")}"
                 data-label="${item.name}">
                ${ingredientMarkup(item.images)}
                ${item.name}
            </div>
        `).join("");

    el("toppings").innerHTML =
        toppings.map((item, i) => `
            <div class="item"
                 data-source="topping"
                 data-index="${i}"
                 data-images="${item.images.join(",")}"
                 data-label="${item.name}">
                ${ingredientMarkup(item.images)}
                ${item.name}
            </div>
        `).join("");
}

function renderAll() {
    updateHud();
    renderCustomers();
    renderGrills();
    renderPlates();
    renderSupplies();
    renderGuide();
}

// ==========================================
// 목숨 및 주문
// ==========================================

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

    if (!plate || !plate.katsu || !plate.sauce) {
        tell(
            "가쓰오부시와 소스를 모두 올려 주세요!",
            "warning"
        );
        return;
    }

    const correct =
        plate.cheese === customer.cheese &&
        plate.sauce === customer.sauce;

    game.plates[plateIndex] = null;
    renderPlates();

    if (correct) {
        game.combo++;
        game.served++;
        game.score +=
            100 + Math.min(game.combo * 10, 100);

        customer.happyUntil = now() + 850;

        updateHud();
        updateCustomers(now());

        tell("주문 성공! 맛있게 드세요!", "success");

    } else {
        game.missed++;
        loseLife("주문이 틀렸어요!");

        if (!game.ended) {
            game.customers[customerIndex] =
                newCustomer();
            renderCustomers();
        }
    }
}

// ==========================================
// 재료 드롭
// ==========================================

function handleDrop(kind, index, target, targetIndex) {
    if (!game || game.ended || game.paused) return;

    if (kind === "filling" && target === "grill") {
        const item = fillings[index];
        const grill = game.grills[targetIndex];

        if (!item || !grill) return;

        if (item.type === "base") {
            if (grill.state !== "empty") {
                tell("이미 사용 중인 조리판입니다!", "warning");
                return;
            }

            game.grills[targetIndex] = {
                state: "cooking",
                cheese: false,
                born: now()
            };

            renderGrills();
            updateGrillBars(now());
            return;
        }

        if (item.type === "cheese") {
            if (grill.state !== "cooking") {
                tell(
                    "조리 중인 타코야끼에 치즈를 넣어 주세요!",
                    "warning"
                );
                return;
            }

            if (grill.cheese) {
                tell("이미 치즈가 들어 있어요!", "warning");
                return;
            }

            grill.cheese = true;
            renderGrills();
            updateGrillBars(now());
            tell("치즈를 추가했어요!", "success");
            return;
        }
    }

    if (kind === "grill" && target === "plate") {
        const grill = game.grills[index];

        if (!grill || grill.state !== "ready") {
            tell(
                "다 익은 타코야끼만 접시에 담을 수 있어요!",
                "warning"
            );
            return;
        }

        if (game.plates[targetIndex]) {
            tell("그 접시는 사용 중이에요!", "warning");
            return;
        }

        game.plates[targetIndex] = {
            cheese: grill.cheese,
            katsu: false,
            sauce: null
        };

        game.grills[index] = {state: "empty"};

        renderGrills();
        renderPlates();
        tell("접시에 담았어요!", "success");
        return;
    }

    if (kind === "topping" && target === "plate") {
        const item = toppings[index];
        const plate = game.plates[targetIndex];

        if (!item || !plate) {
            tell("먼저 접시에 타코야끼를 담아 주세요!", "warning");
            return;
        }

        if (item.type === "katsu") {
            if (plate.katsu) {
                tell("이미 가쓰오부시를 올렸어요!", "warning");
                return;
            }

            plate.katsu = true;
            renderPlates();
            tell("가쓰오부시를 올렸어요!", "success");
            return;
        }

        if (item.type === "sauce") {
            if (!plate.katsu) {
                tell("먼저 가쓰오부시를 올려 주세요!", "warning");
                return;
            }

            if (plate.sauce) {
                tell("이미 소스를 선택했어요!", "warning");
                return;
            }

            plate.sauce = item.id;
            renderPlates();
            tell("타코야끼 완성! 서빙하세요!", "success");
            return;
        }
    }

    if (kind === "plate" && target === "customer") {
        serve(targetIndex, index);
        return;
    }

    if (target === "trash") {
        if (kind === "plate") {
            game.plates[index] = null;
            renderPlates();
            tell("음식을 버렸습니다.");
            return;
        }

        if (kind === "grill") {
            game.grills[index] = {state: "empty"};
            renderGrills();
            tell("조리판을 비웠습니다.");
            return;
        }
    }

    tell("올바른 위치에 재료를 놓아 주세요!", "warning");
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
        highlighted.classList.remove("drop-over");
    }

    highlighted = document.elementFromPoint(
        event.clientX, event.clientY
    )?.closest("[data-drop]");

    if (highlighted) {
        highlighted.classList.add("drop-over");
    }
}

document.addEventListener("pointerdown", event => {
    if (!game || game.ended || game.paused || drag) {
        return;
    }

    const source = event.target.closest("[data-source]");
    if (!source) return;

    event.preventDefault();

    const ghost = document.createElement("div");
    ghost.className = "ghost";

    if (source.dataset.source === "plate") {
        ghost.innerHTML = `
            ${foodMarkup(source.dataset.food)}
            <small>타코야끼</small>
        `;
    } else if (source.dataset.source === "grill") {
        ghost.innerHTML = `
            ${foodMarkup("takoyaki_plain.png")}
            <small>익은 타코야끼</small>
        `;
    } else {
        const files = (
            source.dataset.images || ""
        ).split(",").filter(Boolean);

        ghost.innerHTML = `
            ${ingredientMarkup(files)}
            <small>${source.dataset.label || ""}</small>
        `;
    }

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
    if (!drag || event.pointerId !== drag.pointerId) {
        return;
    }

    event.preventDefault();
    moveGhost(event);
}, {passive: false});

function cancelDrag() {
    if (!drag) return;

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
}

document.addEventListener("pointerup", event => {
    if (!drag || event.pointerId !== drag.pointerId) {
        return;
    }

    const kind = drag.kind;
    const index = drag.index;

    const target = document.elementFromPoint(
        event.clientX, event.clientY
    )?.closest("[data-drop]");

    // 드래그 표시를 먼저 제거
    cancelDrag();

    if (target) {
        handleDrop(
            kind,
            index,
            target.dataset.drop,
            Number(target.dataset.index || 0)
        );
    }
});

document.addEventListener("pointercancel", cancelDrag);

// ==========================================
// 게임 종료
// ==========================================

function endGame(won) {
    if (!game || game.ended) return;

    game.ended = true;
    game.paused = true;

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
            ? "오코노미야끼 가게 잠금 해제!"
            : "다시 도전해 보세요!"}
    `;

    el("start-button").textContent =
        "다시 도전하기";

    el("overlay").classList.remove("hidden");
}

// ==========================================
// 게임 타이머
// ==========================================

function tick() {
    if (!game || game.ended || game.paused) return;

    const t = now();

    const remaining = Math.max(
        0,
        LEVEL_TIMES[game.level - 1] -
        (t - game.levelStart) / 1000
    );

    el("time").textContent =
        Math.ceil(remaining);

    if (remaining <= 0) {
        nextLevel();
        return;
    }

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

        if (t - customer.born >= customer.patience) {
            game.missed++;
            loseLife("손님이 기다리다 떠났어요!");

            if (game.ended) return;

            game.customers[i] = newCustomer();
            customersChanged = true;
        }
    }

    if (customersChanged) {
        renderCustomers();
    }

    updateCustomers(t);

    let grillsChanged = false;

    game.grills.forEach(grill => {
        if (!["cooking", "ready"].includes(grill.state)) {
            return;
        }

        const elapsed = t - grill.born;

        if (
            grill.state === "cooking" &&
            elapsed >= COOK_MS
        ) {
            grill.state = "ready";
            grillsChanged = true;
        }

        if (
            grill.state === "ready" &&
            elapsed >= BURN_MS
        ) {
            grill.state = "burnt";
            grillsChanged = true;
            tell("타코야끼가 탔어요!", "error");
        }
    });

    if (grillsChanged) {
        renderGrills();
    }

    updateGrillBars(t);
}

// ==========================================
// 시작 전 화면
// ==========================================

function initializeScreen() {
    renderSupplies();
    renderGuide();

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
                <div class="holes">
                    ${'<span class="ball"></span>'.repeat(6)}
                </div>
                <strong>${i + 1}번 조리판</strong>
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


# ==========================================
# Python 데이터 연결
# ==========================================

GAME_HTML = GAME_HTML.replace(
    "__CUSTOMERS__",
    json.dumps(customer_images)
)

GAME_HTML = GAME_HTML.replace(
    "__INGREDIENTS__",
    json.dumps(ingredient_images)
)

GAME_HTML = GAME_HTML.replace(
    "__FOODS__",
    json.dumps(food_images)
)

GAME_HTML = GAME_HTML.replace(
    "__BUBBLE__",
    json.dumps(bubble_theme)
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

# 타코야끼 클리어 시 오코노미야끼 잠금 해제
listen_for_takoyaki_clear()

components.html(
    GAME_HTML,
    height=700,
    scrolling=False
)
