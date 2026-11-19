
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


# =====================================
# 기본 설정 및 저장값
# =====================================

DEFAULTS = {
    "saved_background": "🌸 벚꽃 축제",
    "saved_character": "🐱 고양이",
    "saved_hat": "👨‍🍳 요리사 모자",
    "saved_apron": "❤️ 빨간색",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================
# 화면 디자인
# =====================================

st.html("""
<style>

/* 배경 */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        180deg,
        #fff4e4 0%,
        #ffe0c5 100%
    );
}

/* 본문 크기와 여백 */
.block-container {
    max-width: 1150px !important;
    padding-top: 1.8rem !important;
    padding-bottom: 2rem !important;
}

/* 페이지 제목 */
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

/* 미리보기 제목 */
.preview-title {
    text-align: center;
    color: #855034;
    font-size: 22px;
    font-weight: 900;
    margin: 3px auto 14px;
}

/* 미리보기 전체 영역 */
.preview-scene {
    position: relative;
    min-height: 390px;
    border: 7px solid #ad7552;
    border-radius: 25px;
    overflow: hidden;
    text-align: center;
    padding: 17px;
    box-shadow: 0 9px #875737;
}

/* 계절 장식 */
.scene-decoration {
    font-size: 33px;
    margin: 7px 0 16px;
    letter-spacing: 10px;
}

/* 포장마차 */
.scene-stall {
    max-width: 550px;
    margin: 0 auto;
    border: 6px solid #99583a;
    background: #fff0d8;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px #85543b;
}

/* 포장마차 지붕 */
.stall-roof {
    padding: 12px;
    color: #fff9e8;
    font-size: 20px;
    font-weight: 900;
    border-bottom: 6px solid #99583a;
}

/* 요리사 캐릭터 영역 */
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

/* 앞치마 */
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

/* 음식 진열대 */
.food-counter {
    background: #b9764a;
    padding: 9px;
    font-size: 30px;
    border-top: 5px solid #8d593a;
}

/* 계절 설명 */
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

/* 설정 영역의 버튼 */
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

/* 화면이 좁은 경우 */
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
        min-height: 340px;
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
        배경과 요리사 캐릭터를
        원하는 스타일로 꾸며 보세요!
    </p>
</div>
""")


# =====================================
# 화면 좌우 구분
# =====================================

left, right = st.columns(
    [1, 1.3],
    gap="large",
)


# =====================================
# 왼쪽: 꾸미기 설정
# =====================================

with left:

    st.subheader("🏮 꾸미기 설정")

    background_options = list(BACKGROUNDS.keys())
    character_options = list(CHARACTERS.keys())
    hat_options = list(HATS.keys())
    apron_options = list(APRONS.keys())

    background = st.selectbox(
        "🌸 포장마차 배경",
        background_options,
        index=background_options.index(
            st.session_state.saved_background
        ),
    )

    character = st.selectbox(
        "🐱 요리사 캐릭터",
        character_options,
        index=character_options.index(
            st.session_state.saved_character
        ),
    )

    hat = st.selectbox(
        "🎩 머리 장식",
        hat_options,
        index=hat_options.index(
            st.session_state.saved_hat
        ),
    )

    apron = st.selectbox(
        "🎽 앞치마 색상",
        apron_options,
        index=apron_options.index(
            st.session_state.saved_apron
        ),
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

        st.success("꾸미기 설정이 저장되었어요!")

    st.info(
        "설정은 현재 접속 중인 세션에 저장됩니다. "
        "실제 요리 게임 화면에 적용하는 기능은 "
        "아직 연결되지 않았어요."
    )


# =====================================
# 오른쪽: 실시간 미리보기
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

    # HTML 전용 렌더링 사용
    # 들여쓰기가 있어도 코드 블록으로 출력되지 않음

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

    </div>
    """

    st.html(preview_html)


# =====================================
# 저장된 설정 확인
# =====================================

st.divider()

st.subheader("🧸 현재 저장된 꾸미기 설정")

a, b, c, d = st.columns(4)

a.metric(
    "배경",
    st.session_state.saved_background,
)

b.metric(
    "캐릭터",
    st.session_state.saved_character,
)

c.metric(
    "머리 장식",
    st.session_state.saved_hat,
)

d.metric(
    "앞치마",
    st.session_state.saved_apron,
)
