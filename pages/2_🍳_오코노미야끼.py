
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json

# ==================================================
# 와글와글 포장마차 - 오코노미야끼 게임
# ==================================================

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
    "▫️ 심플 말풍선": "simple",
    "💥 코믹 말풍선": "comic",
}

BACKGROUNDS = {
    "🌸 벚꽃 축제": "bg_spring.png",
    "🎆 여름 축제": "bg_summer.png",
    "🍁 가을 야시장": "bg_autumn.png",
    "❄️ 겨울 포장마차": "bg_winter.png",
}

customer_theme = CUSTOMER_STYLES.get(
    st.session_state.get(
        "saved_customer_style",
        "🎆 축제 손님"
    ),
    "festival",
)

bubble_theme = BUBBLE_STYLES.get(
    st.session_state.get(
        "saved_bubble_style",
        "💭 둥근 말풍선"
    ),
    "round",
)

background_file = BACKGROUNDS.get(
    st.session_state.get(
        "saved_background",
        "🌸 벚꽃 축제"
    ),
    "bg_spring.png",
)


# ==================================================
# 이미지 파일 읽기
# ==================================================

def to_data_url(path):
    if not path.is_file():
        return ""

    encoded = base64.b64encode(
        path.read_bytes()
    ).decode("ascii")

    return "data:image/png;base64," + encoded


customer_images = {}

customer_folder = (
    ROOT / "assets" / "customers" / customer_theme
)

for number in range(1, 6):
    for mood in (
        "normal",
        "waiting",
        "angry",
        "happy",
    ):
        filename = (
            f"{customer_theme}_{number:02d}_{mood}.png"
        )

        customer_images[f"{number}_{mood}"] = (
            to_data_url(customer_folder / filename)
        )


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


food_files = [
    "okonomiyaki_plain.png",
    "okonomiyaki_sauce.png",
    "okonomiyaki_mayo.png",
    "okonomiyaki_both.png",
]

food_images = {
    filename: to_data_url(
        ROOT / "assets" / "foods" / filename
    )
    for filename in food_files
}

background_url = to_data_url(
    ROOT / background_file
)

missing_files = [
    filename
    for filename, url in {
        **ingredient_images,
        **food_images,
    }.items()
    if not url
]

if missing_files:
    st.warning(
        "다음 이미지 파일을 찾을 수 없습니다: "
        + ", ".join(missing_files)
    )


# ==================================================
# Streamlit 스타일
# ==================================================

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


# ==================================================
# 게임 HTML
# ==================================================

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

/* ==================================================
   전체 화면
================================================== */

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

.game {
    position: relative;

    width: 100%;
    height: 680px;

    padding: 8px 12px;
    overflow: hidden;

    border-radius: 18px;

    background: linear-gradient(
        180deg,
        #88a0c6,
        #f2c1aa 52%,
        #f6d5a0
    );

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}


/* ==================================================
   상단 정보
================================================== */

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    gap: 8px;
    height: 45px;
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

    background: #784d3d;
    color: white;

    border: 2px solid #f6d6a0;
    border-radius: 12px;

    text-align: center;
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


/* ==================================================
   안내 알림
================================================== */

.notice-area {
    display: grid;
    place-items: center;

    height: 43px;
    margin: 2px 0 4px;

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

    font-size: 13px;
    font-weight: 900;
    text-align: center;

    opacity: 0;
    transition: opacity 0.2s;
}

.toast.show {
    opacity: 1;
}

.toast.success {
    background: #269957;
}

.toast.error {
    background: #d74646;
}

.toast.warning {
    background: #e8a02f;
    color: #493116;
}


/* ==================================================
   가게 이름
================================================== */

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


/* ==================================================
   손님
================================================== */

.customers {
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 8px;

    width: 100%;
    max-width: 1050px;
    height: 160px;

    margin: 0 auto 7px;
}

.customer {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;

    min-width: 0;
    padding: 0 3px;

    text-align: center;
}


/* ==================================================
   말풍선
================================================== */

.bubble {
    position: relative;
    z-index: 2;

    display: flex;
    align-items: center;
    justify-content: center;

    width: 96%;
    max-width: 260px;
    min-height: 44px;

    margin-bottom: 5px;
    padding: 5px 6px;

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
    bottom: -8px;
    left: calc(50% - 6px);

    width: 12px;
    height: 12px;

    background: inherit;
    transform: rotate(45deg);

    border-right: 2px solid #d9ab83;
    border-bottom: 2px solid #d9ab83;
}


/* ==================================================
   손님 주문 PNG
================================================== */

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
    gap: 4px;
}

.order-part {
    flex: 1;
    min-width: 0;
    gap: 3px;
}

.order-images {
    flex-shrink: 0;
    gap: 1px;
}

.order-images img {
    display: block;

    width: 23px;
    height: 25px;

    object-fit: contain;
    pointer-events: none;
}

.order-images.double img {
    width: 18px;
    height: 23px;
}

.order-name {
    font-size: 10px;
    font-weight: 900;
    white-space: nowrap;
}

.order-plus {
    color: #c17b48;
    font-size: 15px;
    font-weight: 900;
    flex-shrink: 0;
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


/* ==================================================
   손님 이미지 / 대기 게이지
================================================== */

.avatar {
    width: min(130px, 100%);
    height: 83px;

    object-fit: contain;
    object-position: center bottom;

    pointer-events: none;
    user-select: none;
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
    filter: drop-shadow(
        0 0 7px #ffe46a
    );
}


/* ==================================================
   조리대
================================================== */

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


/* ==================================================
   철판 3개
================================================== */

.grills {
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 7px;
    padding: 7px;

    background: #44434a;

    border: 4px solid #302e34;
    border-radius: 15px;
}

.grill {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    min-width: 0;
    min-height: 132px;

    padding: 5px 3px;
    gap: 5px;

    background: #28282c;
    color: #fff5da;

    border: 2px solid #686268;
    border-radius: 13px;

    text-align: center;
}

.grill.ready {
    border-color: #62b780;
}

.grill.burnt {
    border-color: #87493d;
}

.grill.urgent {
    border-color: #e76b5d;
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


/* ==================================================
   철판 이미지
================================================== */

.grill-visual {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 100%;
    height: 58px;

    pointer-events: none;
}

.empty-pan {
    width: 75px;
    height: 58px;

    border-radius: 50%;

    background: radial-gradient(
        ellipse,
        #252529 50%,
        #666168 54%,
        #17171b 66%
    );
}

.grill-batter {
    width: 75px;
    height: 58px;

    object-fit: contain;
}

.grill-food {
    width: 95px;
    max-width: 95%;
    height: 58px;

    object-fit: contain;

    pointer-events: none;
}

.grill.cooking .grill-food {
    opacity: 0.82;
    filter: saturate(0.75);
}

.grill.second .grill-food {
    opacity: 0.9;
}

.grill.ready .grill-food {
    filter: drop-shadow(
        0 2px 4px rgba(0, 0, 0, 0.35)
    );
}

.grill.burnt .grill-food {
    filter: brightness(0.35) saturate(0.4);
}


/* ==================================================
   조리 게이지
================================================== */

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


/* ==================================================
   접시 3개
================================================== */

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


/* ==================================================
   수정: 타코야끼와 동일한 빈 접시 디자인
================================================== */

.empty-plate {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    gap: 3px;
    width: 100%;
}

.empty-plate-icon {
    font-size: 23px;
    line-height: 1;
}

.empty-plate-text {
    font-size: 10px;
    line-height: 1.2;

    font-weight: 900;
    color: #75452e;
}

/* 완성 음식은 기존 PNG 사용 */

.plate-food {
    display: block;

    width: 72px;
    max-width: 95%;
    height: 55px;

    object-fit: contain;

    pointer-events: none;
    user-select: none;
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


/* ==================================================
   재료와 도구
================================================== */

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


/* ==================================================
   조리 순서 안내
================================================== */

.help {
    max-width: 1200px;

    margin: 7px auto 0;
    padding: 5px 8px;

    background: #fff4da;

    border: 2px solid #d8ab75;
    border-radius: 10px;
}

.help-title {
    margin-bottom: 4px;

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

.guide-step img.food-guide {
    width: 35px;
}

.guide-arrow {
    color: #b7794c;

    font-size: 15px;
    font-weight: 900;
}


/* ==================================================
   드래그 앤 드롭
================================================== */

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


/* ==================================================
   시작 / 종료 / 카운트다운
================================================== */

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

    border: 6px solid #bc7950;
    border-radius: 25px;

    background: #fff4d9;

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

.countdown.show {
    display: flex;
}

.count-level {
    font-size: 42px;
    font-weight: 900;
}

.count-lives {
    padding: 8px 20px;

    border: 3px solid #e3a36d;
    border-radius: 15px;

    background: #fff3d9;
    color: #b44d47;

    font-size: 21px;
    font-weight: 900;
}

.count-number {
    font-size: 105px;
    font-weight: 900;
}


/* ==================================================
   반응형
================================================== */

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

    .order-images img {
        width: 18px;
        height: 21px;
    }

    .order-name {
        font-size: 9px;
    }

    .avatar {
        width: min(110px, 100%);
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

    .grill-food,
    .grill-batter {
        width: 70px;
        height: 50px;
    }

    .item {
        font-size: 10px;
    }

    .ingredient-art img {
        height: 32px;
    }

    .plate-food {
        height: 45px;
    }

    .guide-step {
        font-size: 9px;
    }

    .guide-step img {
        width: 21px;
        height: 21px;
    }

    .empty-plate-icon {
        font-size: 21px;
    }

    .empty-plate-text {
        font-size: 9px;
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


    <!-- 안내 메시지 -->

    <div class="notice-area">
        <div class="toast" id="toast"></div>
    </div>


    <!-- 가게 이름 -->

    <div class="sign">
        오코노미야끼 가게
    </div>


    <!-- 손님 -->

    <div
        class="customers"
        id="customers">
    </div>


    <!-- 조리대 -->

    <div class="counter">

        <h3>오코노미야끼 철판 조리대</h3>

        <div class="kitchen">

            <div
                class="grills"
                id="grills">
            </div>

            <div class="right">

                <div class="plate-zone">

                    <strong>
                        완성 접시 3개
                    </strong>

                    <div
                        class="plates"
                        id="plates">
                    </div>

                    <small id="plate-help">
                        익은 오코노미야끼를
                        접시에 올려 주세요
                    </small>

                </div>

                <div
                    class="trash"
                    data-drop="trash">
                    음식 버리기
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
            <h3>② 뒤집개와 토핑</h3>

            <div
                class="items"
                id="tools">
            </div>
        </div>

    </div>


    <!-- 조리 안내 -->

    <div class="help">

        <div class="help-title">
            조리 순서
        </div>

        <div
            class="guide"
            id="guide">
        </div>

    </div>


    <!-- 시작 / 종료 -->

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
                반죽 → 재료 → 앞면 → 뒤집기 → 뒷면<br>
                접시 → 토핑 → 서빙<br>
                소스와 마요네즈를 모두 주문할 수도 있어요!<br>
                목숨 3개 · 총 5레벨<br>
                뒤집기 전과 완성 후에는
                각각 8초 안에 옮겨 주세요.<br>
                레벨마다 목숨이 회복돼요.
            </p>

            <button
                class="start"
                id="start-button"
                onclick="beginCountdown()">
                오코노미야끼 만들기
            </button>

        </div>
    </div>


    <!-- 카운트다운 -->

    <div
        class="countdown"
        id="countdown">

        <div
            class="count-level"
            id="count-level">
            LEVEL 1
        </div>

        <div
            class="count-lives"
            id="count-lives">
            목숨 3개
        </div>

        <div
            class="count-number"
            id="count-text">
            3
        </div>

    </div>

</div>


<script>

// ==================================================
// 게임 설정
// ==================================================

const CUSTOMER_IMAGES = __CUSTOMERS__;
const INGREDIENT_IMAGES = __INGREDIENTS__;
const FOOD_IMAGES = __FOODS__;
const BUBBLE_STYLE = __BUBBLE__;

const LEVEL_TIMES = [
    60, 70, 80, 90, 100
];

const CUSTOMER_COUNT = [
    3, 3, 3, 4, 4
];

const CUSTOMER_WAIT = [
    [40, 45],
    [35, 40],
    [30, 35],
    [27, 32],
    [25, 30]
];

const FIRST_COOK_MS = 2200;
const SECOND_COOK_MS = 2000;
const BURN_WAIT_MS = 8000;

const MAX_LIVES = 3;


// ==================================================
// 재료 및 조리 도구
// ==================================================

const ingredients = [
    {
        id: "batter",
        name: "반죽",
        type: "batter",
        images: ["batter.png"]
    },
    {
        id: "pork",
        name: "돼지고기",
        type: "filling",
        images: ["pork.png"]
    },
    {
        id: "seafood",
        name: "해산물",
        type: "filling",
        images: ["seafood.png"]
    },
    {
        id: "cheese",
        name: "치즈",
        type: "filling",
        images: ["cheese.png"]
    }
];

const tools = [
    {
        id: "flip",
        name: "뒤집개",
        type: "flip",
        images: ["spatula.png"]
    },
    {
        id: "sauce",
        name: "소스",
        type: "topping",
        images: ["sauce.png"]
    },
    {
        id: "mayonnaise",
        name: "마요네즈",
        type: "topping",
        images: ["mayonnaise.png"]
    }
];

const fillings = ingredients.filter(
    item => item.type === "filling"
);

const TOPPING_ORDERS = [
    "sauce",
    "mayo",
    "both"
];


// ==================================================
// 공통 함수
// ==================================================

const el = id =>
    document.getElementById(id);

const now = () =>
    performance.now();

const sleep = ms =>
    new Promise(resolve => setTimeout(resolve, ms));

const pick = array =>
    array[
        Math.floor(Math.random() * array.length)
    ];

let game = null;
let drag = null;
let highlighted = null;
let counting = false;
let toastTimer = null;


// ==================================================
// 이미지 표시 함수
// ==================================================

function imageTag(
    url,
    className = "",
    alt = ""
) {

    if (!url) return "";

    return `
        <img
            class="${className}"
            src="${url}"
            alt="${alt}"
            draggable="false">
    `;
}


function ingredientMarkup(files) {

    const images = files
        .filter(name => INGREDIENT_IMAGES[name])
        .map(name =>
            imageTag(INGREDIENT_IMAGES[name])
        )
        .join("");

    return `
        <span class="ingredient-art">
            ${images || "재료"}
        </span>
    `;
}


// ==================================================
// 음식 PNG 4종
// ==================================================

function foodFilename(plate) {

    if (plate.sauce && plate.mayo) {
        return "okonomiyaki_both.png";
    }

    if (plate.sauce) {
        return "okonomiyaki_sauce.png";
    }

    if (plate.mayo) {
        return "okonomiyaki_mayo.png";
    }

    return "okonomiyaki_plain.png";
}


function foodMarkup(
    filename,
    className = "plate-food"
) {

    const url = FOOD_IMAGES[filename];

    return url
        ? imageTag(
            url,
            className,
            "오코노미야끼"
        )
        : "<span>오코노미야끼</span>";
}


// ==================================================
// 손님 이미지
// ==================================================

function imageFor(number, mood) {

    return (
        CUSTOMER_IMAGES[`${number}_${mood}`] ||
        CUSTOMER_IMAGES[`${number}_normal`] ||
        ""
    );
}


// ==================================================
// 조리 순서 안내
// ==================================================

function guideImage(
    filename,
    isFood = false
) {

    const url = isFood
        ? FOOD_IMAGES[filename]
        : INGREDIENT_IMAGES[filename];

    if (!url) return "";

    return imageTag(
        url,
        isFood ? "food-guide" : "",
        filename
    );
}


function renderGuide() {

    el("guide").innerHTML = `

        <span class="guide-step">
            ${guideImage("batter.png")}
            반죽
        </span>

        <span class="guide-arrow">→</span>

        <span class="guide-step">
            ${guideImage("pork.png")}
            ${guideImage("seafood.png")}
            ${guideImage("cheese.png")}
            재료 선택
        </span>

        <span class="guide-arrow">→</span>

        <span class="guide-step">
            ${guideImage(
                "okonomiyaki_plain.png",
                true
            )}
            앞면 굽기
        </span>

        <span class="guide-arrow">→</span>

        <span class="guide-step">
            ${guideImage("spatula.png")}
            뒤집기
        </span>

        <span class="guide-arrow">→</span>

        <span class="guide-step">
            ${guideImage(
                "okonomiyaki_plain.png",
                true
            )}
            뒷면 굽기
        </span>

        <span class="guide-arrow">→</span>

        <span class="guide-step">
            ${guideImage("sauce.png")}
            ${guideImage("mayonnaise.png")}
            토핑 선택
        </span>

        <span class="guide-arrow">→</span>

        <span class="guide-step">
            서빙
        </span>
    `;
}


// ==================================================
// 주문 이미지
// ==================================================

function orderImages(files) {

    const valid = files.filter(
        name => INGREDIENT_IMAGES[name]
    );

    return `
        <span class="order-images ${
            valid.length > 1 ? "double" : ""
        }">

            ${valid.map(name =>
                imageTag(INGREDIENT_IMAGES[name])
            ).join("")}

        </span>
    `;
}


function toppingName(order) {

    if (order === "sauce") {
        return "소스";
    }

    if (order === "mayo") {
        return "마요네즈";
    }

    return "소스+마요";
}


function toppingFiles(order) {

    if (order === "sauce") {
        return ["sauce.png"];
    }

    if (order === "mayo") {
        return ["mayonnaise.png"];
    }

    return [
        "sauce.png",
        "mayonnaise.png"
    ];
}


function orderMarkup(customer) {

    return `
        <div class="order-content">

            <span class="order-part">

                ${orderImages(
                    customer.fill.images
                )}

                <span class="order-name">
                    ${customer.fill.name}
                </span>

            </span>

            <span class="order-plus">+</span>

            <span class="order-part">

                ${orderImages(
                    toppingFiles(
                        customer.toppingOrder
                    )
                )}

                <span class="order-name">
                    ${toppingName(
                        customer.toppingOrder
                    )}
                </span>

            </span>

        </div>
    `;
}


// ==================================================
// 알림
// ==================================================

function tell(message, type = "info") {

    const box = el("toast");

    const cleanMessage = message
        .replace(/[✅❌🔥⚠️🍳🥣]/gu, "")
        .trim();

    box.textContent = cleanMessage;
    box.className = `toast ${type} show`;

    clearTimeout(toastTimer);

    toastTimer = setTimeout(() => {
        box.classList.remove("show");
    }, 1800);
}


// ==================================================
// 손님 생성
// ==================================================

function newCustomer() {

    const [min, max] =
        CUSTOMER_WAIT[game.level - 1];

    return {
        character:
            Math.floor(Math.random() * 5) + 1,

        fill:
            pick(fillings),

        toppingOrder:
            pick(TOPPING_ORDERS),

        born:
            now(),

        patience:
            (
                min +
                Math.random() * (max - min)
            ) * 1000,

        happyUntil: 0
    };
}


// ==================================================
// 게임 초기화
// ==================================================

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

        plates: [
            null,
            null,
            null
        ],

        customers: [],

        ended: false,
        paused: true
    };
}


// ==================================================
// 시작 카운트다운
// ==================================================

async function beginCountdown() {

    if (counting) return;

    createNewGame();
    await runLevelCountdown(false);
}


async function runLevelCountdown(showIntro) {

    if (
        counting ||
        !game ||
        game.ended
    ) {
        return;
    }

    counting = true;
    game.paused = true;

    el("overlay").classList.add("hidden");
    el("countdown").classList.add("show");

    el("count-level").textContent =
        `LEVEL ${game.level}`;

    el("count-lives").textContent =
        `목숨 ${game.lives}개`;

    if (showIntro) {

        el("count-text").textContent =
            "다음 레벨!";

        await sleep(1200);
    }

    for (const number of ["3", "2", "1"]) {

        el("count-text").textContent =
            number;

        await sleep(1000);
    }

    el("count-text").textContent =
        "START!";

    await sleep(600);

    game.levelStart = now();

    game.customers = Array.from(
        {
            length:
                CUSTOMER_COUNT[game.level - 1]
        },
        newCustomer
    );

    game.paused = false;

    renderAll();

    el("time").textContent =
        LEVEL_TIMES[game.level - 1];

    el("countdown").classList.remove(
        "show"
    );

    counting = false;

    tell(
        `${game.level}레벨 영업 시작!`,
        "info"
    );
}


// ==================================================
// 다음 레벨
// ==================================================

function nextLevel() {

    if (
        !game ||
        game.ended ||
        game.paused
    ) {
        return;
    }

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

    game.plates = [
        null,
        null,
        null
    ];

    game.customers = [];
    game.paused = true;

    updateHud();

    el("time").textContent =
        LEVEL_TIMES[game.level - 1];

    runLevelCountdown(true);
}


// ==================================================
# 상단 정보
// ==================================================

function updateHud() {

    if (!game) return;

    el("level").textContent =
        game.level;

    el("score").textContent =
        game.score;

    el("lives").textContent =
        "❤️".repeat(game.lives);
}


// ==================================================
// 손님 표시
// ==================================================

function renderCustomers() {

    if (!game) return;

    const area = el("customers");
    const count = game.customers.length;

    area.style.gridTemplateColumns =
        `repeat(${count}, minmax(0, 1fr))`;

    area.classList.toggle(
        "four",
        count === 4
    );

    area.innerHTML =
        game.customers.map((customer, i) => `

            <div
                class="customer"
                id="customer-${i}"

                data-drop="customer"
                data-index="${i}">

                <div
                    class="bubble ${BUBBLE_STYLE}"
                    id="bubble-${i}">

                    ${orderMarkup(customer)}

                </div>

                <img
                    class="avatar"
                    id="avatar-${i}"

                    src="${imageFor(
                        customer.character,
                        "normal"
                    )}"

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


// ==================================================
// 손님 대기 상태
// ==================================================

function updateCustomers(t) {

    if (!game) return;

    game.customers.forEach(
        (customer, i) => {

            const avatar =
                el(`avatar-${i}`);

            const card =
                el(`customer-${i}`);

            const bar =
                el(`patience-${i}`);

            const bubble =
                el(`bubble-${i}`);

            const label =
                el(`label-${i}`);

            if (
                !avatar ||
                !card ||
                !bar ||
                !bubble ||
                !label
            ) {
                return;
            }

            if (customer.happyUntil) {

                if (
                    avatar.dataset.expression !==
                    "happy"
                ) {

                    avatar.src = imageFor(
                        customer.character,
                        "happy"
                    );

                    avatar.dataset.expression =
                        "happy";
                }

                card.classList.add("happy");
                card.classList.remove("urgent");

                if (
                    bubble.dataset.state !==
                    "happy"
                ) {

                    bubble.textContent =
                        "맛있어요! 감사합니다!";

                    bubble.dataset.state =
                        "happy";
                }

                label.textContent =
                    "주문 성공!";

                bar.style.width =
                    "100%";

                bar.style.background =
                    "#70b963";

                return;
            }

            const percent = Math.max(
                0,
                100 * (
                    1 -
                    (t - customer.born) /
                    customer.patience
                )
            );

            const mood =
                percent <= 30
                    ? "angry"
                    : percent <= 65
                    ? "waiting"
                    : "normal";

            if (
                avatar.dataset.expression !== mood
            ) {

                avatar.src = imageFor(
                    customer.character,
                    mood
                );

                avatar.dataset.expression =
                    mood;
            }

            card.classList.remove("happy");

            card.classList.toggle(
                "urgent",
                percent <= 30
            );

            if (
                bubble.dataset.state === "happy"
            ) {

                bubble.innerHTML =
                    orderMarkup(customer);

                bubble.dataset.state =
                    "order";
            }

            label.textContent =
                percent <= 30
                    ? "너무 오래 기다렸어요!"
                    : percent <= 65
                    ? "기다림이 길어지고 있어요..."
                    : "주문을 기다리는 중";

            bar.style.width =
                percent + "%";

            bar.style.background =
                percent <= 30
                    ? "#dc6753"
                    : percent <= 65
                    ? "#e8b64a"
                    : "#70b963";
        }
    );
}


// ==================================================
// 철판 이미지
// ==================================================

function grillVisual(grill) {

    const state = grill.state;

    if (state === "empty") {

        return `
            <div class="grill-visual">
                <div class="empty-pan"></div>
            </div>
        `;
    }

    if (state === "batter") {

        const batterImage =
            INGREDIENT_IMAGES["batter.png"];

        return `
            <div class="grill-visual">

                ${batterImage
                    ? imageTag(
                        batterImage,
                        "grill-batter",
                        "반죽"
                    )
                    : "반죽"}

            </div>
        `;
    }

    return `
        <div class="grill-visual">

            ${foodMarkup(
                "okonomiyaki_plain.png",
                "grill-food"
            )}

        </div>
    `;
}


// ==================================================
// 철판 표시
// ==================================================

function renderGrills() {

    if (!game) return;

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

            const source = canDrag ? `
                data-source="grill"
                data-index="${i}"
                data-label="오코노미야끼"
            ` : "";

            return `
                <div
                    class="grill ${grill.state}"
                    id="grill-${i}"

                    data-drop="grill"
                    data-index="${i}"

                    ${source}>

                    ${grillVisual(grill)}

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


// ==================================================
// 조리 시간
// ==================================================

function updateGrillBars(t) {

    if (!game) return;

    game.grills.forEach((grill, i) => {

        const bar =
            el(`cook-${i}`);

        const status =
            el(`grill-status-${i}`);

        const card =
            el(`grill-${i}`);

        if (!bar || !status) return;

        const elapsed = grill.since
            ? t - grill.since
            : 0;

        let percent = 0;
        let color = "#efc456";
        let message = "반죽을 넣어 주세요";

        if (grill.state === "batter") {

            message = "재료를 올려 주세요";

        } else if (grill.state === "cooking") {

            const remain = Math.max(
                0,
                FIRST_COOK_MS - elapsed
            );

            percent = Math.min(
                100,
                elapsed / FIRST_COOK_MS * 100
            );

            message =
                `앞면 익기까지 ` +
                `${(remain / 1000).toFixed(1)}초`;

        } else if (grill.state === "flip") {

            const remain = Math.max(
                0,
                BURN_WAIT_MS - elapsed
            );

            percent =
                remain / BURN_WAIT_MS * 100;

            message =
                `뒤집기! 타기까지 ` +
                `${(remain / 1000).toFixed(1)}초`;

            color =
                remain <= 1500
                    ? "#d9534f"
                    : "#f0a43a";

        } else if (grill.state === "second") {

            const remain = Math.max(
                0,
                SECOND_COOK_MS - elapsed
            );

            percent = Math.min(
                100,
                elapsed / SECOND_COOK_MS * 100
            );

            message =
                `뒷면 익기까지 ` +
                `${(remain / 1000).toFixed(1)}초`;

        } else if (grill.state === "ready") {

            const remain = Math.max(
                0,
                BURN_WAIT_MS - elapsed
            );

            percent =
                remain / BURN_WAIT_MS * 100;

            message =
                `타기까지 ` +
                `${(remain / 1000).toFixed(1)}초`;

            color =
                remain <= 1500
                    ? "#d9534f"
                    : remain <= 2500
                    ? "#f0a43a"
                    : "#4fa568";

        } else if (grill.state === "burnt") {

            color = "#d9534f";
            message = "음식이 탔어요!";
        }

        bar.style.width =
            percent + "%";

        bar.style.background =
            color;

        status.textContent =
            message;

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


// ==================================================
// 수정: 빈 접시 디자인
// ==================================================

function emptyPlateMarkup(index, active = true) {

    const dropAttributes = active
        ? `data-drop="plate" data-index="${index}"`
        : "";

    return `
        <div
            class="plate"
            ${dropAttributes}>

            <span class="plate-number">
                ${index + 1}
            </span>

            <div class="empty-plate">
                <span class="empty-plate-icon">
                    🍽️
                </span>

                <span class="empty-plate-text">
                    빈 접시
                </span>
            </div>

        </div>
    `;
}


// ==================================================
// 접시 표시
// ==================================================

function renderPlates() {

    const area = el("plates");

    if (!game) {

        area.innerHTML = Array.from(
            {length: 3},
            (_, i) => emptyPlateMarkup(i, false)
        ).join("");

        return;
    }

    area.innerHTML =
        game.plates.map((plate, i) => {

            // 빈 접시
            if (!plate) {

                return emptyPlateMarkup(i);
            }

            // 완성 음식
            const filename =
                foodFilename(plate);

            const topping =
                plate.sauce && plate.mayo
                    ? "소스+마요"
                    : plate.sauce
                    ? "소스"
                    : plate.mayo
                    ? "마요네즈"
                    : "토핑 전";

            const complete =
                plate.sauce || plate.mayo;

            return `
                <div
                    class="plate ${
                        complete ? "ready" : ""
                    }"

                    data-drop="plate"
                    data-index="${i}"

                    data-source="plate"
                    data-food="${filename}"
                    data-label="오코노미야끼">

                    <span class="plate-number">
                        ${i + 1}
                    </span>

                    ${foodMarkup(filename)}

                    <small>
                        ${plate.fill.name}
                        · ${topping}
                    </small>

                </div>
            `;
        }).join("");

    if (
        game.plates.some(
            p => p && !p.sauce && !p.mayo
        )
    ) {

        el("plate-help").textContent =
            "접시에 토핑을 올려 주세요";

    } else if (game.plates.some(Boolean)) {

        el("plate-help").textContent =
            "주문에 맞게 토핑한 뒤 서빙하세요";

    } else {

        el("plate-help").textContent =
            "익은 오코노미야끼를 접시에 올려 주세요";
    }
}


// ==================================================
// 재료와 도구 표시
// ==================================================

function renderItems() {

    el("ingredients").innerHTML =
        ingredients.map((item, i) => `
            <div
                class="item"

                data-source="ingredient"
                data-index="${i}"

                data-images="${item.images.join(",")}"
                data-label="${item.name}">

                ${ingredientMarkup(item.images)}

                ${item.name}

            </div>
        `).join("");

    el("tools").innerHTML =
        tools.map((item, i) => `
            <div
                class="item"

                data-source="tool"
                data-index="${i}"

                data-images="${item.images.join(",")}"
                data-label="${item.name}">

                ${ingredientMarkup(item.images)}

                ${item.name}

            </div>
        `).join("");
}


// ==================================================
// 전체 화면 갱신
// ==================================================

function renderAll() {

    updateHud();
    renderCustomers();
    renderGrills();
    renderPlates();
    renderItems();
    renderGuide();
    updateGrillBars(now());
}


// ==================================================
// 목숨 감소
// ==================================================

function loseLife(message) {

    if (
        !game ||
        game.ended ||
        game.paused
    ) {
        return;
    }

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


// ==================================================
// 토핑 조합 판정
// ==================================================

function plateToppingOrder(plate) {

    if (plate.sauce && plate.mayo) {
        return "both";
    }

    if (plate.sauce) {
        return "sauce";
    }

    if (plate.mayo) {
        return "mayo";
    }

    return "none";
}


// ==================================================
// 손님에게 서빙
// ==================================================

function serve(customerIndex, plateIndex) {

    const customer =
        game.customers[customerIndex];

    const plate =
        game.plates[plateIndex];

    if (
        !customer ||
        customer.happyUntil
    ) {
        return;
    }

    if (
        !plate ||
        (!plate.sauce && !plate.mayo)
    ) {

        tell(
            "주문에 맞는 토핑을 올려 주세요!",
            "warning"
        );

        return;
    }

    const correct =
        plate.fill.id === customer.fill.id &&
        plateToppingOrder(plate) ===
        customer.toppingOrder;

    game.plates[plateIndex] = null;

    renderPlates();

    if (correct) {

        game.combo++;

        game.best = Math.max(
            game.best,
            game.combo
        );

        game.served++;

        game.score +=
            100 + Math.min(
                game.combo * 10,
                100
            );

        customer.happyUntil =
            now() + 850;

        updateHud();
        updateCustomers(now());

        tell(
            "주문 성공! 맛있게 드세요!",
            "success"
        );

    } else {

        game.missed++;

        loseLife(
            "주문과 재료 또는 토핑이 달라요!"
        );

        if (!game.ended) {

            game.customers[customerIndex] =
                newCustomer();

            renderCustomers();
        }
    }
}


// ==================================================
// 드롭 처리
// ==================================================

function handleDrop(
    kind,
    index,
    target,
    targetIndex
) {

    if (
        !game ||
        game.ended ||
        game.paused
    ) {
        return;
    }


    // 반죽 / 재료 → 철판
    if (
        kind === "ingredient" &&
        target === "grill"
    ) {

        const item =
            ingredients[index];

        const grill =
            game.grills[targetIndex];

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

        const tool =
            tools[index];

        const grill =
            game.grills[targetIndex];

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
            "뒤집기 성공! 뒷면을 굽습니다.",
            "success"
        );

        return;
    }


    // 철판 → 빈 접시
    if (
        kind === "grill" &&
        target === "plate"
    ) {

        const grill =
            game.grills[index];

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

        if (
            game.plates[targetIndex]
        ) {

            tell(
                "그 접시는 이미 사용 중이에요!",
                "warning"
            );

            return;
        }

        game.plates[targetIndex] = {
            fill: grill.fill,
            sauce: false,
            mayo: false
        };

        game.grills[index] = {
            state: "empty"
        };

        renderGrills();
        renderPlates();

        tell(
            "접시에 담았어요! 토핑을 올려 주세요.",
            "success"
        );

        return;
    }


    // 소스 / 마요네즈 → 접시
    if (
        kind === "tool" &&
        target === "plate"
    ) {

        const tool =
            tools[index];

        const plate =
            game.plates[targetIndex];

        if (
            !tool ||
            tool.type !== "topping"
        ) {

            tell(
                "소스나 마요네즈를 올려 주세요!",
                "warning"
            );

            return;
        }

        if (!plate) {

            tell(
                "먼저 음식을 접시에 담아 주세요!",
                "warning"
            );

            return;
        }

        if (tool.id === "sauce") {

            if (plate.sauce) {

                tell(
                    "이미 소스를 올렸어요!",
                    "warning"
                );

                return;
            }

            plate.sauce = true;

            renderPlates();

            tell(
                plate.mayo
                    ? "소스와 마요네즈가 모두 올라갔어요!"
                    : "소스를 올렸어요!",
                "success"
            );

            return;
        }

        if (tool.id === "mayonnaise") {

            if (plate.mayo) {

                tell(
                    "이미 마요네즈를 올렸어요!",
                    "warning"
                );

                return;
            }

            plate.mayo = true;

            renderPlates();

            tell(
                plate.sauce
                    ? "소스와 마요네즈가 모두 올라갔어요!"
                    : "마요네즈를 올렸어요!",
                "success"
            );

            return;
        }
    }


    // 접시 → 손님
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


// ==================================================
// 드래그 위치
// ==================================================

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

    highlighted =
        document.elementFromPoint(
            event.clientX,
            event.clientY
        )?.closest("[data-drop]");

    if (highlighted) {

        highlighted.classList.add(
            "drop-over"
        );
    }
}


// ==================================================
// 드래그 시작
// ==================================================

document.addEventListener(
    "pointerdown",
    event => {

        if (
            !game ||
            game.ended ||
            game.paused ||
            drag
        ) {
            return;
        }

        const source =
            event.target.closest(
                "[data-source]"
            );

        if (!source) return;

        event.preventDefault();

        const ghost =
            document.createElement("div");

        ghost.className = "ghost";

        if (
            source.dataset.source === "plate"
        ) {

            ghost.innerHTML = `
                ${foodMarkup(
                    source.dataset.food
                )}

                <small>
                    오코노미야끼
                </small>
            `;

        } else if (
            source.dataset.source === "grill"
        ) {

            ghost.innerHTML = `
                ${foodMarkup(
                    "okonomiyaki_plain.png"
                )}

                <small>
                    익은 오코노미야끼
                </small>
            `;

        } else {

            const files = (
                source.dataset.images || ""
            ).split(",").filter(Boolean);

            ghost.innerHTML = `
                ${ingredientMarkup(files)}

                <small>
                    ${source.dataset.label || ""}
                </small>
            `;
        }

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


// ==================================================
// 드래그 이동
// ==================================================

document.addEventListener(
    "pointermove",
    event => {

        if (
            !drag ||
            drag.pointerId !== event.pointerId
        ) {
            return;
        }

        event.preventDefault();
        moveGhost(event);
    },
    {
        passive: false
    }
);


// ==================================================
// 드래그 취소
// ==================================================

function cancelDrag() {

    if (!drag) return;

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


// ==================================================
// 드롭 완료
// ==================================================

document.addEventListener(
    "pointerup",
    event => {

        if (
            !drag ||
            drag.pointerId !== event.pointerId
        ) {
            return;
        }

        const kind = drag.kind;
        const index = drag.index;

        const target =
            document.elementFromPoint(
                event.clientX,
                event.clientY
            )?.closest("[data-drop]");

        cancelDrag();

        if (target) {

            handleDrop(
                kind,
                index,
                target.dataset.drop,

                Number(
                    target.dataset.index || 0
                )
            );
        }
    }
);

document.addEventListener(
    "pointercancel",
    cancelDrag
);


// ==================================================
// 게임 종료
// ==================================================

function endGame(won) {

    if (!game || game.ended) return;

    game.ended = true;
    game.paused = true;

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
        "다시 도전하기";

    el("overlay").classList.remove(
        "hidden"
    );
}


// ==================================================
// 게임 타이머
// ==================================================

function tick() {

    if (
        !game ||
        game.ended ||
        game.paused
    ) {
        return;
    }

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


    // 조리 진행
    let grillsChanged = false;

    game.grills.forEach(grill => {

        if (![
            "cooking",
            "flip",
            "second",
            "ready"
        ].includes(grill.state)) {

            return;
        }

        const elapsed =
            t - grill.since;

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
            ["flip", "ready"].includes(
                grill.state
            ) &&
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
                "오코노미야끼가 탔어요! -10점",
                "error"
            );
        }
    });

    if (grillsChanged) {
        renderGrills();
    }

    updateGrillBars(t);


    // 손님 대기 시간
    let customersChanged = false;

    for (
        let i = 0;
        i < game.customers.length;
        i++
    ) {

        const customer =
            game.customers[i];

        if (customer.happyUntil) {

            if (
                t >= customer.happyUntil
            ) {

                game.customers[i] =
                    newCustomer();

                customersChanged = true;
            }

            continue;
        }

        if (
            t - customer.born >=
            customer.patience
        ) {

            game.missed++;

            loseLife(
                "손님이 기다리다 떠났어요!"
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


// ==================================================
// 게임 시작 전 화면
// ==================================================

function initializeScreen() {

    renderItems();
    renderGuide();

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

                        src="${imageFor(
                            i + 1,
                            "normal"
                        )}"

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

                    <div class="grill-visual">
                        <div class="empty-pan"></div>
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

    renderPlates();
}


// ==================================================
// 실행
// ==================================================

initializeScreen();

setInterval(tick, 100);

</script>

</body>
</html>
"""


# ==================================================
# 이미지 데이터 연결
# ==================================================

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


# ==================================================
# 배경 이미지 적용
# ==================================================

if background_url:

    background_css = """
    <style>
    .game {
        background-image:
            url("__IMAGE__") !important;

        background-size:
            cover !important;

        background-position:
            center !important;

        background-repeat:
            no-repeat !important;
    }
    </style>
    """

    background_css = background_css.replace(
        "__IMAGE__",
        background_url
    )

    GAME_HTML = GAME_HTML.replace(
        "</head>",
        background_css + "</head>",
        1
    )


# ==================================================
# 게임 출력
# ==================================================

components.html(
    GAME_HTML,
    height=700,
    scrolling=False
)
