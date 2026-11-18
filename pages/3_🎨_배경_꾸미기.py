
import streamlit as st

st.set_page_config(
    page_title="배경 꾸미기 | 와글와글 포장마차",
    page_icon="🎨",
    layout="wide",
)

# 배경과 캐릭터 설정
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

# 기본 설정 및 저장된 설정 불러오기
DEFAULTS = {
    "saved_background": "🌸 벚꽃 축제",
    "saved_character": "🐱 고양이",
    "saved_hat": "👨‍🍳 요리사 모자",
    "saved_apron": "❤️ 빨간색",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        180deg, #fff4e4, #ffe0c5
    );
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}

.main-title {
    background: #fff7e8;
    border: 4px solid #d7a077;
    border-radius: 22px;
    text-align: center;
    padding: 22px;
    margin-bottom: 24px;
    box-shadow: 0 6px #b9825d;
}

.main-title h1 {
    color: #965032;
    margin: 0;
    font-size: 36px;
}

.main-title p {
    color: #90634b;
    margin-top: 10px;
    font-weight: 700;
}

.preview-title {
    text-align: center;
    color: #855034;
    font-size: 22px;
    font-weight: 900;
    margin-bottom: 12px;
}

.preview-scene {
    position: relative;
    min-height: 440px;
    border: 7px solid #ad7552;
    border-radius: 25px;
    overflow: hidden;
    text-align: center;
    padding: 20px;
    box-shadow: 0 9px #875737;
}

.scene-decoration {
    font-size: 35px;
    margin: 12px 0 20px;
    letter-spacing: 13px;
}

.scene-stall {
    max-width: 550px;
    margin: 0 auto;
    border: 6px solid #99583a;
    background: #fff0d8;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 10px #85543b;
}

.stall-roof {
    padding: 13px;
    color: #fff9e8;
    font-size: 25px;
    font-weight: 900;
    border-bottom: 6px solid #99583a;
}

.stall-inside {
    padding: 18px 10px 12px;
}

.chef-hat {
    font-size: 38px;
    line-height: 1;
}

.chef-face {
    font-size: 80px;
    line-height: 1.1;
}

.apron {
    width: 70px;
    height: 62px;
    margin: 0 auto 12px;
    border-radius: 12px 12px 22px 22px;
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
    padding: 10px;
    font-size: 35px;
    border-top: 5px solid #8d593a;
}

.scene-caption {
    margin: 15px auto 0;
    background: #fff8e9d9;
    color: #855036;
    border-radius: 13px;
    padding: 9px;
    max-width: 450px;
    font-size: 14px;
    font-weight: 800;
}

.settings-box {
    background: #fff8ec;
    border: 3px solid #e8bb8f;
    border-radius: 20px;
    padding: 17px 20px;
    margin-bottom: 14px;
}

.settings-box h3 {
    margin: 0 0 10px;
    font-size: 19px;
    color: #965438;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
    <h1>🎨 나만의 포장마차 꾸미기</h1>
    <p>
        배경과 요리사 캐릭터를
        원하는 스타일로 꾸며 보세요!
    </p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1.3], gap="large")

# 왼쪽: 설정 화면
with left:
    st.subheader("🏮 꾸미기 설정")

    background = st.selectbox(
        "🌸 포장마차 배경",
        list(BACKGROUNDS.keys()),
        index=list(BACKGROUNDS.keys()).index(
            st.session_state.saved_background
        ),
    )

    character = st.selectbox(
        "🐱 요리사 캐릭터",
        list(CHARACTERS.keys()),
        index=list(CHARACTERS.keys()).index(
            st.session_state.saved_character
        ),
    )

    hat = st.selectbox(
        "🎩 머리 장식",
        list(HATS.keys()),
        index=list(HATS.keys()).index(
            st.session_state.saved_hat
        ),
    )

    apron = st.selectbox(
        "🎽 앞치마 색상",
        list(APRONS.keys()),
        index=list(APRONS.keys()).index(
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
        "다음 단계에서 실제 요리 게임 화면에도 "
        "적용할 예정이에요."
    )

# 오른쪽: 실시간 미리보기
with right:
    st.markdown(
        '<div class="preview-title">'
        '✨ 포장마차 미리보기'
        '</div>',
        unsafe_allow_html=True,
    )

    theme = BACKGROUNDS[background]
    character_emoji = CHARACTERS[character]
    hat_emoji = HATS[hat]
    apron_color = APRONS[apron]

    st.markdown(
        f"""
        <div class="preview-scene"
             style="
                background:
                linear-gradient(
                    180deg,
                    {theme["sky"]} 0%,
                    {theme["ground"]} 100%
                );
             ">

            <div class="scene-decoration">
                {theme["decoration"]}
            </div>

            <div class="scene-stall">

                <div class="stall-roof"
                     style="
                         background:{theme["roof"]};
                     ">
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
                         style="
                             background:{apron_color};
                         ">
                        ★
                    </div>

                </div>

                <div class="food-counter">
                    🐙 🍡 🍳 🥢
                </div>

            </div>

            <div class="scene-caption">
                {theme["description"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown("### 🧸 현재 저장된 꾸미기 설정")

a, b, c, d = st.columns(4)

a.metric("배경", st.session_state.saved_background)
b.metric("캐릭터", st.session_state.saved_character)
c.metric("머리 장식", st.session_state.saved_hat)
d.metric("앞치마", st.session_state.saved_apron)
