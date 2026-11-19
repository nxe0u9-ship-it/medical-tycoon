import streamlit as st

# =====================================
# 꾸미기 선택 항목
# =====================================

BACKGROUNDS = {
    "🌸 벚꽃 축제": {
        "sky": "#f9c8d5",
        "ground": "#f3b9a7",
        "roof": "#c96d88",
        "decoration": "🌸 🌸 🌸",
        "description": "분홍빛 벚꽃이 가득한 봄 축제",
    },
    "🎆 여름 축제": {
        "sky": "#516c9c",
        "ground": "#a98c9d",
        "roof": "#df7950",
        "decoration": "🎆 🏮 🎆",
        "description": "불꽃놀이가 펼쳐지는 여름밤",
    },
    "🍁 가을 야시장": {
        "sky": "#e6a36d",
        "ground": "#c18455",
        "roof": "#a9563d",
        "decoration": "🍁 🍂 🍁",
        "description": "단풍이 물든 따뜻한 가을 거리",
    },
    "❄️ 겨울 포장마차": {
        "sky": "#a7c4dc",
        "ground": "#e3edf2",
        "roof": "#668ca8",
        "decoration": "❄️ ⛄ ❄️",
        "description": "눈 내리는 포근한 겨울 포장마차",
    },
}

CHARACTERS = {
    "🐱 고양이": "🐱",
    "🐰 토끼": "🐰",
    "🐻 곰": "🐻",
    "🦊 여우": "🦊",
}

HATS = {
    "👨‍🍳 요리사 모자": "👨‍🍳",
    "🎀 리본": "🎀",
    "🧢 모자": "🧢",
    "👑 왕관": "👑",
}

APRONS = {
    "❤️ 빨간색": "#dc6c65",
    "💛 노란색": "#e7b64f",
    "💚 초록색": "#89b697",
    "💙 파란색": "#85a9cb",
}

CUSTOMER_STYLES = {
    "🎆 축제 손님": {
        "hair": "#5b3d32",
        "shirt": "#f4a261",
        "accent": "#e76f51",
        "label": "축제 손님",
        "bubble_text": "🐙 타코야끼 주세요!",
    },
    "🎒 학생": {
        "hair": "#4a3b35",
        "shirt": "#9bb7d4",
        "accent": "#5c6f91",
        "label": "학생",
        "bubble_text": "🍳 오코노미야끼 주세요!",
    },
    "💼 직장인": {
        "hair": "#352d2a",
        "shirt": "#c7ccd8",
        "accent": "#7d8698",
        "label": "직장인",
        "bubble_text": "🐙 문어 + 🍥 가쓰오부시!",
    },
    "👕 캐주얼": {
        "hair": "#6a4e42",
        "shirt": "#9ec5a4",
        "accent": "#6d9f76",
        "label": "캐주얼",
        "bubble_text": "소스도 듬뿍 주세요!",
    },
}

BUBBLE_STYLES = {
    "💭 둥근 말풍선": "round",
    "💥 코믹 말풍선": "comic",
    "▫️ 심플 말풍선": "simple",
}

# =====================================
# 기본 설정 및 저장값
# =====================================

DEFAULTS = {
    "saved_background": "🌸 벚꽃 축제",
    "saved_character": "🐱 고양이",
    "saved_hat": "👨‍🍳 요리사 모자",
    "saved_apron": "❤️ 빨간색",
    "saved_customer_style": "🎆 축제 손님",
    "saved_bubble_style": "💭 둥근 말풍선",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =====================================
# 화면 디자인
# =====================================

st.html("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        180deg,
        #fff4e4 0%,
        #ffe0c5 100%
    );
}

.block-container {
    max-width: 1150px !important;
    padding-top: 1.8rem !important;
    padding-bottom: 2rem !important;
}

.main-title {
    background: #fff7e8;
    border: 4px solid #d7a077;
    border-radius: 22px;
    text-align: center;
    padding: 18px;
    margin-bottom: 18px;
    box-shadow: 0 6px #b9825d;
}

.main-title h1 {
    color: #965032;
    margin: 0;
    font-size: 32px;
    font-weight: 900;
}

.main-title p {
    color: #90634b;
    margin: 10px 0 0;
    font-size: 15px;
    font-weight: 700;
}

.preview-title {
    text-align: center;
    color: #855034;
    font-size: 22px;
    font-weight: 900;
    margin: 3px auto 14px;
}

.preview-scene {
    position: relative;
    min-height: 510px;
    border: 7px solid #ad7552;
    border-radius: 25px;
    overflow: hidden;
    text-align: center;
    padding: 17px;
    box-shadow: 0 9px #875737;
}

.scene-decoration {
    font-size: 33px;
    margin: 7px 0 16px;
    letter-spacing: 10px;
}

.scene-stall {
    max-width: 550px;
    margin: 0 auto;
    border: 6px solid #99583a;
    background: #fff0d8;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px #85543b;
}

.stall-roof {
    padding: 12px;
    color: #fff9e8;
    font-size: 20px;
    font-weight: 900;
    border-bottom: 6px solid #99583a;
}

.stall-inside {
    padding: 12px 10px 10px;
}

.chef-hat {
    font-size: 34px;
    line-height: 1.1;
}

.chef-face {
    font-size: 66px;
    line-height: 1.1;
}

.apron {
    width: 65px;
    height: 50px;
    margin: 0 auto 9px;
    border-radius: 12px 12px 20px 20px;
    border: 4px solid #fff4dd;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 19px;
    font-weight: 900;
}

.food-counter {
    background: #b9764a;
    padding: 9px;
    font-size: 30px;
    border-top: 5px solid #8d593a;
}

.scene-caption {
    margin: 14px auto 0;
    background: #fff8e9e8;
    color: #855036;
    border-radius: 13px;
    padding: 9px;
    max-width: 450px;
    font-size: 14px;
    font-weight: 800;
}

/* 손님 미리보기 */
.customer-preview-wrap {
    margin: 18px auto 0;
    max-width: 460px;
}

.customer-preview-title {
    color: #855034;
    font-size: 18px;
    font-weight: 900;
    margin-bottom: 10px;
}

.customer-preview {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    gap: 14px;
    background: #fff8e9;
    border: 4px solid #dba980;
    border-radius: 18px;
    padding: 16px 12px 12px;
}

.customer-bubble {
    position: relative;
    min-width: 150px;
    max-width: 210px;
    text-align: center;
    font-size: 13px;
    font-weight: 900;
    color: #6f4b38;
    line-height: 1.5;
}

/* 둥근 말풍선 */
.customer-bubble.round {
    background: white;
    border: 3px solid #e2b48f;
    border-radius: 20px;
    padding: 12px 14px;
}

.customer-bubble.round::after {
    content: "";
    position: absolute;
    left: 25px;
    bottom: -14px;
    width: 22px;
    height: 22px;
    background: white;
    border-left: 3px solid #e2b48f;
    border-bottom: 3px solid #e2b48f;
    transform: rotate(-35deg);
    border-bottom-left-radius: 6px;
}

/* 코믹 말풍선 */
.customer-bubble.comic {
    background: #fff7cc;
    border: 3px solid #d9964d;
    border-radius: 16px;
    padding: 12px 14px;
    box-shadow: 4px 4px 0 #f0b36f;
}

.customer-bubble.comic::after {
    content: "";
    position: absolute;
    left: 28px;
    bottom: -16px;
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 14px solid transparent;
    border-top: 18px solid #d9964d;
}

.customer-bubble.comic::before {
    content: "";
    position: absolute;
    left: 31px;
    bottom: -11px;
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 11px solid transparent;
    border-top: 15px solid #fff7cc;
    z-index: 2;
}

/* 심플 말풍선 */
.customer-bubble.simple {
    background: #ffffffd9;
    border: 2px solid #d7c1b2;
    border-radius: 12px;
    padding: 10px 12px;
}

.customer-bubble.simple::after {
    content: "";
    position: absolute;
    left: 25px;
    bottom: -10px;
    width: 16px;
    height: 16px;
    background: #ffffffd9;
    border-left: 2px solid #d7c1b2;
    border-bottom: 2px solid #d7c1b2;
    transform: rotate(-45deg);
}

.customer-card {
    width: 150px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.customer-face {
    width: 82px;
    height: 82px;
    border-radius: 50%;
    border: 4px solid #86604d;
    position: relative;
    margin-bottom: 8px;
}

.customer-face::before,
.customer-face::after {
    content: "";
    position: absolute;
    top: 32px;
    width: 7px;
    height: 11px;
    border-radius: 999px;
    background: #3f2d26;
}

.customer-face::before {
    left: 22px;
}

.customer-face::after {
    right: 22px;
}

.customer-hair {
    position: absolute;
    top: -2px;
    left: -2px;
    width: 82px;
    height: 42px;
    border-radius: 42px 42px 18px 18px;
}

.customer-bangs {
    position: absolute;
    top: 18px;
    left: 16px;
    width: 46px;
    height: 16px;
    border-radius: 0 0 14px 14px;
}

.customer-mouth {
    position: absolute;
    left: 50%;
    bottom: 18px;
    transform: translateX(-50%);
    width: 16px;
    height: 8px;
    border-bottom: 3px solid #8a4d45;
    border-radius: 0 0 16px 16px;
}

.customer-body {
    width: 92px;
    height: 62px;
    border: 4px solid #86604d;
    border-radius: 22px 22px 14px 14px;
    margin-top: -4px;
}

.customer-style-label {
    margin-top: 7px;
    font-size: 13px;
    font-weight: 900;
    color: #8d5639;
}

/* 저장 버튼 */
.stButton button[kind="primary"] {
    background: #c93650 !important;
    border-color: #c93650 !important;
    border-radius: 10px !important;
    font-weight: 900 !important;
}

.stButton button[kind="primary"]:hover {
    background: #ab2940 !important;
    border-color: #ab2940 !important;
}

@media (max-width: 700px) {
    .block-container {
        padding-top: 1rem !important;
    }

    .main-title h1 {
        font-size: 24px;
    }

    .preview-title {
        font-size: 19px;
    }

    .preview-scene {
        min-height: 560px;
        padding: 10px;
    }

    .scene-decoration {
        font-size: 26px;
        letter-spacing: 5px;
    }

    .stall-roof {
        font-size: 16px;
        padding: 9px;
    }

    .chef-face {
        font-size: 55px;
    }

    .food-counter {
        font-size: 24px;
    }

    .customer-preview {
        flex-direction: column;
        align-items: center;
    }
}
</style>
""")

# =====================================
# 페이지 제목
# =====================================

st.html("""
<div class="main-title">
    <h1>🎨 나만의 포장마차 꾸미기</h1>
    <p>
        배경, 요리사, 손님 느낌까지
        원하는 스타일로 꾸며 보세요!
    </p>
</div>
""")

left, right = st.columns([1, 1.3], gap="large")

# =====================================
# 왼쪽: 설정
# =====================================

with left:
    st.subheader("🏮 꾸미기 설정")

    background_options = list(BACKGROUNDS.keys())
    character_options = list(CHARACTERS.keys())
    hat_options = list(HATS.keys())
    apron_options = list(APRONS.keys())
    customer_style_options = list(CUSTOMER_STYLES.keys())
    bubble_style_options = list(BUBBLE_STYLES.keys())

    background = st.selectbox(
        "🌸 포장마차 배경",
        background_options,
        index=background_options.index(st.session_state.saved_background),
    )

    character = st.selectbox(
        "🐱 요리사 캐릭터",
        character_options,
        index=character_options.index(st.session_state.saved_character),
    )

    hat = st.selectbox(
        "🎩 머리 장식",
        hat_options,
        index=hat_options.index(st.session_state.saved_hat),
    )

    apron = st.selectbox(
        "🎽 앞치마 색상",
        apron_options,
        index=apron_options.index(st.session_state.saved_apron),
    )

    customer_style = st.selectbox(
        "🧍 손님 스타일",
        customer_style_options,
        index=customer_style_options.index(st.session_state.saved_customer_style),
    )

    bubble_style = st.selectbox(
        "💬 말풍선 스타일",
        bubble_style_options,
        index=bubble_style_options.index(st.session_state.saved_bubble_style),
    )

    st.write("")

    if st.button(
        "💾 꾸미기 설정 저장하기",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.saved_background = background
        st.session_state.saved_character = character
        st.session_state.saved_hat = hat
        st.session_state.saved_apron = apron
        st.session_state.saved_customer_style = customer_style
        st.session_state.saved_bubble_style = bubble_style

        st.success("꾸미기 설정이 저장되었어요!")

    st.info(
        "현재는 미리보기와 세션 저장까지만 연결되어 있어요. "
        "다음 단계에서 실제 게임 화면의 손님 스타일과 말풍선에 적용할 수 있어요."
    )

# =====================================
# 오른쪽: 미리보기
# =====================================

with right:
    st.html("""
    <div class="preview-title">
        ✨ 포장마차 미리보기
    </div>
    """)

    theme = BACKGROUNDS[background]
    character_emoji = CHARACTERS[character]
    hat_emoji = HATS[hat]
    apron_color = APRONS[apron]

    customer_theme = CUSTOMER_STYLES[customer_style]
    bubble_class = BUBBLE_STYLES[bubble_style]

    preview_html = f"""
    <div class="preview-scene"
         style="
             background: linear-gradient(
                 180deg,
                 {theme['sky']} 0%,
                 {theme['ground']} 100%
             );
         ">

        <div class="scene-decoration">
            {theme['decoration']}
        </div>

        <div class="scene-stall">
            <div class="stall-roof"
                 style="background: {theme['roof']};">
                🏮 와글와글 포장마차 🏮
            </div>

            <div class="stall-inside">
                <div class="chef-hat">
                    {hat_emoji}
                </div>

                <div class="chef-face">
                    {character_emoji}
                </div>

                <div class="apron"
                     style="background: {apron_color};">
                    ★
                </div>
            </div>

            <div class="food-counter">
                🐙 🍡 🍳 🥢
            </div>
        </div>

        <div class="scene-caption">
            {theme['description']}
        </div>

        <div class="customer-preview-wrap">
            <div class="customer-preview-title">
                💬 손님 미리보기
            </div>

            <div class="customer-preview">
                <div class="customer-bubble {bubble_class}">
                    {customer_theme['bubble_text']}
                </div>

                <div class="customer-card">
                    <div class="customer-face"
                         style="background: #ffd7bf;">
                        <div class="customer-hair"
                             style="background: {customer_theme['hair']};">
                        </div>

                        <div class="customer-bangs"
                             style="background: {customer_theme['hair']};">
                        </div>

                        <div class="customer-mouth"></div>
                    </div>

                    <div class="customer-body"
                         style="background: {customer_theme['shirt']};">
                    </div>

                    <div class="customer-style-label">
                        {customer_theme['label']}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

    st.html(preview_html)

# =====================================
# 현재 저장값 확인
# =====================================

st.divider()

st.subheader("🧸 현재 저장된 꾸미기 설정")

a, b, c = st.columns(3)
d, e, f = st.columns(3)

a.metric("배경", st.session_state.saved_background)
b.metric("캐릭터", st.session_state.saved_character)
c.metric("머리 장식", st.session_state.saved_hat)
d.metric("앞치마", st.session_state.saved_apron)
e.metric("손님 스타일", st.session_state.saved_customer_style)
f.metric("말풍선", st.session_state.saved_bubble_style)
