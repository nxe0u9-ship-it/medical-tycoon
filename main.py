
import streamlit as st

st.set_page_config(
    page_title="와글와글 포장마차",
    page_icon="🏮",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "entered_lobby" not in st.session_state:
    st.session_state.entered_lobby = False


def open_lobby():
    st.session_state.entered_lobby = True


def go_home():
    st.session_state.entered_lobby = False


st.markdown("""
<style>
/* 전체 화면을 포장마차 게임처럼 꾸미기 */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        180deg, #fcebd5 0%, #ffe2bf 70%, #f6d0b1 100%
    );
}

.block-container {
    max-width: 1150px;
    padding-top: 2.3rem;
    padding-bottom: 2rem;
}

#MainMenu, footer {
    visibility: hidden;
}

h1, h2, h3 {
    color: #754027;
}

/* 시작 버튼 */
.st-key-start_waggle button {
    background: linear-gradient(
        180deg, #ffad69, #e66b43
    ) !important;
    color: white !important;
    border: 3px solid #a94a2c !important;
    border-radius: 22px !important;
    min-height: 75px !important;
    font-size: 24px !important;
    font-weight: 900 !important;
    box-shadow: 0 7px 0 #9b4a2f !important;
}

.st-key-start_waggle button:hover {
    background: linear-gradient(
        180deg, #ffbe79, #f17a4b
    ) !important;
    transform: translateY(-2px);
}

/* 첫 화면 */
.hero {
    position: relative;
    overflow: hidden;
    min-height: 460px;
    border: 8px solid #a65337;
    border-radius: 30px;
    background: linear-gradient(
        180deg,
        #5d7db4 0%,
        #f8b5a0 54%,
        #ffe1a6 100%
    );
    box-shadow:
        0 13px 0 #a75e3d,
        0 20px 28px #8a593755;
    text-align: center;
    padding: 25px 20px 30px;
}

.stars {
    position: absolute;
    top: 16px;
    left: 5%;
    right: 5%;
    font-size: 23px;
    letter-spacing: 10px;
    opacity: .9;
}

.hero-title {
    position: relative;
    z-index: 2;
    display: inline-block;
    margin: 33px auto 8px;
    padding: 12px 30px;
    border: 5px solid #fff0b6;
    border-radius: 18px;
    background: #aa493a;
    box-shadow: 0 7px 0 #72372d;
    color: #fff3c9;
    font-size: clamp(30px, 4.4vw, 60px);
    font-weight: 900;
    letter-spacing: 2px;
    text-shadow: 2px 3px #70302b;
}

.hero-sub {
    position: relative;
    z-index: 2;
    color: #693724;
    font-size: 20px;
    font-weight: 900;
    margin: 12px 0 17px;
}

/* 포장마차 그림 */
.stall {
    position: relative;
    z-index: 1;
    max-width: 710px;
    margin: 0 auto;
    background: #f7d7a7;
    border: 6px solid #974c31;
    border-radius: 26px 26px 15px 15px;
    box-shadow: 0 12px 0 #71412c;
}

.stall-roof {
    padding: 10px 15px;
    font-size: 33px;
    background: repeating-linear-gradient(
        90deg,
        #c74f42 0 80px,
        #fff0d4 80px 160px
    );
    border-bottom: 5px solid #a45e3d;
    border-radius: 20px 20px 0 0;
}

.stall-food {
    padding: 12px 8px;
    font-size: clamp(35px, 5vw, 61px);
    letter-spacing: 10px;
}

.stall-label {
    background: #864930;
    color: #fff2d3;
    padding: 8px;
    font-size: 17px;
    font-weight: 900;
}

.hero-crowd {
    margin-top: 12px;
    font-size: 34px;
    letter-spacing: 15px;
}

.small-note {
    text-align: center;
    color: #855c43;
    font-size: 14px;
    font-weight: 700;
    margin: 20px 0 10px;
}

/* 게임 선택 화면 */
.lobby-head {
    text-align: center;
    padding: 30px 15px;
    background: #fff4dd;
    border: 5px solid #ce9266;
    border-radius: 25px;
    margin-bottom: 22px;
}

.lobby-head h1 {
    margin: 0 0 8px;
    font-size: clamp(27px, 4vw, 42px);
}

.lobby-head p {
    margin: 0;
    color: #90603f;
    font-weight: 700;
}

.preview {
    background: #fff8eb;
    border: 4px solid #e0ad7e;
    border-radius: 23px;
    padding: 25px;
    text-align: center;
}

.preview .emoji {
    font-size: 85px;
}

.preview h2 {
    margin: 8px 0;
}

.preview p {
    color: #89563b;
    font-weight: 700;
}

.info-row {
    background: #fff1d9;
    border: 2px solid #e4bf94;
    border-radius: 14px;
    padding: 13px 18px;
    margin-top: 20px;
    font-weight: 700;
    color: #85543d;
}
</style>
""", unsafe_allow_html=True)


# 1. 게임 첫 화면
if not st.session_state.entered_lobby:

    # 게임 시작 전에는 사이드바 숨기기
    st.markdown("""
    <style>
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <div class="stars">
            ✦ ✧ ✦ ✧ ✦ ✧ ✦
        </div>

        <div class="hero-title">
            🏮 와글와글 포장마차 🏮
        </div>

        <div class="hero-sub">
            손님이 몰려온다!
            5레벨까지 살아남아라!
        </div>

        <div class="stall">
            <div class="stall-roof">
                🏮 🍡 🏮
            </div>

            <div class="stall-food">
                🐙 🍳 🥞 🍥
            </div>

            <div class="stall-label">
                주문 폭주! 타임어택 요리 대작전
            </div>
        </div>

        <div class="hero-crowd">
            🐱 🐰 🐻 🦊
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="small-note">
            ❤️ 목숨 3개 · ⭐ 5레벨 도전 · 🍳 2가지 요리
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, middle, right = st.columns([1, 1.6, 1])

    with middle:
        st.button(
            "🎮 게임 시작하기",
            key="start_waggle",
            use_container_width=True,
            on_click=open_lobby,
        )


# 2. 게임 시작 버튼을 누른 뒤
else:

    # 사이드바 메뉴
    with st.sidebar:
        st.title("🏮 와글와글 포장마차")
        st.markdown("**메뉴를 선택해 주세요!**")

        choice = st.radio(
            "페이지 선택",
            [
                "🐙 타코야끼",
                "🥞 오코노미야끼",
                "🎨 배경 꾸미기",
            ],
            label_visibility="collapsed",
        )

        st.divider()

        st.button(
            "🏠 처음 화면으로",
            on_click=go_home,
            use_container_width=True,
        )

    st.markdown("""
    <div class="lobby-head">
        <h1>🏮 와글와글 포장마차</h1>
        <p>
            사이드바에서 원하는 메뉴를 선택해 주세요!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 선택한 메뉴에 따라 안내 화면 변경
    details = {
        "🐙 타코야끼": (
            "🐙",
            "타코야끼",
            "속재료를 조리판으로 옮기고, "
            "익혀서 손님에게 서빙하는 스피드게임",
        ),

        "🥞 오코노미야끼": (
            "🥞",
            "오코노미야끼",
            "반죽을 굽고 뒤집어 손님 주문에 "
            "맞춰 완성하는 스피드게임",
        ),

        "🎨 배경 꾸미기": (
            "🎨",
            "배경 꾸미기",
            "포장마차의 배경과 캐릭터를 "
            "취향대로 꾸미는 공간",
        ),
    }

    emoji, title, description = details[choice]

    st.markdown(
        f"""
        <div class="preview">
            <div class="emoji">{emoji}</div>
            <h2>{title}</h2>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="info-row">
        🚧 현재는 첫 화면과 메뉴 선택까지
        구현한 단계예요.<br>
        다음 단계에서 실제 세 페이지를 연결하고,
        요리 시작 버튼과 3·2·1 카운트다운을
        추가할 예정이에요.
    </div>
    """, unsafe_allow_html=True)
