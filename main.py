
import streamlit as st
import textwrap

# =====================================
# 기본 페이지 설정
# =====================================

st.set_page_config(
    page_title="와글와글 포장마차",
    page_icon="🏮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 게임 시작 여부 저장
if "game_entered" not in st.session_state:
    st.session_state.game_entered = False


def enter_game():
    st.session_state.game_entered = True


def return_home():
    st.session_state.game_entered = False


# =====================================
# 전체 디자인 설정
# =====================================

st.markdown("""
<style>

/* 전체 배경 */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        180deg,
        #fff3dd 0%,
        #fbe1c2 60%,
        #f5ccab 100%
    );
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* 불필요한 기본 메뉴 숨기기 */
#MainMenu, footer {
    visibility: hidden;
}

/* 메인 화면 */
.hero {
    position: relative;
    overflow: hidden;
    min-height: 470px;
    border: 8px solid #a85f3d;
    border-radius: 30px;
    padding: 30px 20px;
    text-align: center;

    background: linear-gradient(
        180deg,
        #6684b3 0%,
        #f3ada0 55%,
        #ffdc9e 100%
    );

    box-shadow: 0 12px 0 #915637;
}

/* 게임 제목 */
.hero-title {
    display: inline-block;
    margin: 30px auto 15px;
    padding: 15px 30px;
    border: 5px solid #ffe9ae;
    border-radius: 20px;

    background: #a84839;
    color: #fff2ca;

    font-size: clamp(29px, 4.3vw, 56px);
    font-weight: 900;

    text-shadow: 2px 3px #6d332c;
    box-shadow: 0 7px #74372c;
}

/* 부제목 */
.hero-subtitle {
    color: #69402d;
    font-size: 21px;
    font-weight: 900;
    margin: 15px auto 25px;
    line-height: 1.7;
}

/* 포장마차 */
.stall {
    max-width: 660px;
    margin: 0 auto;
    border: 6px solid #965537;
    border-radius: 25px;
    background: #fff0ce;
    overflow: hidden;
    box-shadow: 0 12px 0 #74442e;
}

/* 포장마차 지붕 */
.stall-roof {
    padding: 12px;
    font-size: 32px;

    background: repeating-linear-gradient(
        90deg,
        #c95045 0 85px,
        #ffe8c7 85px 170px
    );

    border-bottom: 5px solid #965537;
}

/* 음식 그림 */
.stall-food {
    padding: 20px 10px;
    font-size: clamp(38px, 5vw, 62px);
    letter-spacing: 10px;
}

/* 포장마차 간판 */
.stall-sign {
    padding: 10px;
    background: #8d4b32;
    color: #fff3d6;
    font-weight: 900;
    font-size: 17px;
}

/* 손님 캐릭터 */
.customers {
    font-size: 39px;
    margin-top: 17px;
    letter-spacing: 14px;
}

/* 게임 안내 */
.game-info {
    text-align: center;
    margin: 22px auto;
    padding: 12px;
    font-size: 17px;
    font-weight: 900;
    color: #855337;
}

/* 게임 시작 버튼 */
.st-key-game_start_button button {
    background: linear-gradient(
        180deg,
        #ffb06e,
        #e5754b
    ) !important;

    color: white !important;
    border: 3px solid #ab542e !important;
    border-radius: 19px !important;
    min-height: 76px !important;
    font-size: 24px !important;
    font-weight: 900 !important;
    box-shadow: 0 7px 0 #a05233 !important;
}

.st-key-game_start_button button:hover {
    background: #f58c56 !important;
    transform: translateY(-2px);
}

/* 게임 선택 화면 */
.lobby {
    background: #fff7e7;
    border: 5px solid #d69b70;
    border-radius: 27px;
    text-align: center;
    padding: 30px 20px;
    box-shadow: 0 8px #aa7854;
}

.lobby-title {
    color: #9a4b31;
    font-size: 36px;
    font-weight: 900;
    margin-bottom: 15px;
}

.lobby-description {
    color: #84543d;
    font-size: 18px;
    font-weight: 700;
    line-height: 1.8;
}

/* 메뉴 카드 */
.menu-card {
    background: #fff8e9;
    border: 4px solid #e4b689;
    border-radius: 23px;
    text-align: center;
    min-height: 195px;
    padding: 22px 10px;
    margin-top: 20px;
}

.menu-emoji {
    font-size: 60px;
}

.menu-title {
    color: #995338;
    font-size: 22px;
    font-weight: 900;
    margin: 10px auto;
}

.menu-description {
    color: #906248;
    font-size: 14px;
    font-weight: 700;
    line-height: 1.7;
}

</style>
""", unsafe_allow_html=True)


# =====================================
# 1. 게임 첫 화면
# =====================================

if not st.session_state.game_entered:

    # 시작 화면에서는 사이드바 숨기기
    st.markdown("""
<style>
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

    # HTML을 들여쓰기 없이 정리해서 출력
    hero_html = """
<div class="hero">
    <div class="hero-title">
        🏮 와글와글 포장마차 🏮
    </div>

    <div class="hero-subtitle">
        손님이 몰려온다!<br>
        5레벨까지 살아남아라!
    </div>

    <div class="stall">
        <div class="stall-roof">
            🏮 🍡 🏮
        </div>

        <div class="stall-food">
            🐙 🍳 🍥 🥢
        </div>

        <div class="stall-sign">
            주문 폭주! 타임어택 요리 대작전
        </div>
    </div>

    <div class="customers">
        🐱 🐰 🐻 🦊
    </div>
</div>
"""

    st.markdown(
        textwrap.dedent(hero_html).strip(),
        unsafe_allow_html=True,
    )

    info_html = """
<div class="game-info">
    ❤️ 목숨 3개
    &nbsp; · &nbsp;
    ⭐ 5레벨 도전
    &nbsp; · &nbsp;
    🍳 2가지 요리
</div>
"""

    st.markdown(
        textwrap.dedent(info_html).strip(),
        unsafe_allow_html=True,
    )

    # 게임 시작 버튼
    left, center, right = st.columns(
        [1, 1.5, 1]
    )

    with center:
        st.button(
            "🎮 게임 시작하기",
            key="game_start_button",
            use_container_width=True,
            on_click=enter_game,
        )


# =====================================
# 2. 게임 시작 후 메뉴 선택
# =====================================

else:

    # 사이드바
    with st.sidebar:

        st.title("🏮 와글와글 포장마차")

        st.write(
            "원하는 메뉴를 선택해 주세요!"
        )

        st.divider()

        st.page_link(
            "pages/1_🐙_타코야끼.py",
            label="🐙 타코야끼",
        )

        st.page_link(
            "pages/2_🍳_오코노미야끼.py",
            label="🍳 오코노미야끼",
        )

        st.page_link(
            "pages/3_🎨_배경_꾸미기.py",
            label="🎨 배경 꾸미기",
        )

        st.divider()

        st.button(
            "🏠 처음 화면으로",
            on_click=return_home,
            use_container_width=True,
        )

    # 게임 선택 안내
    lobby_html = """
<div class="lobby">
    <div class="lobby-title">
        🏮 와글와글 포장마차
    </div>

    <div class="lobby-description">
        어서 오세요!<br>
        지금부터 나만의 포장마차를
        운영해 보세요.<br><br>
        사이드바에서 원하는 게임을
        선택해 주세요!
    </div>
</div>
"""

    st.markdown(
        textwrap.dedent(lobby_html).strip(),
        unsafe_allow_html=True,
    )

    # 세 가지 메뉴
    col1, col2, col3 = st.columns(
        3,
        gap="medium"
    )

    # 타코야끼
    with col1:

        taco_html = """
<div class="menu-card">
    <div class="menu-emoji">🐙</div>
    <div class="menu-title">타코야끼</div>
    <div class="menu-description">
        타코야끼를 빠르게 구워<br>
        손님에게 서빙하세요!
    </div>
</div>
"""

        st.markdown(
            textwrap.dedent(taco_html).strip(),
            unsafe_allow_html=True,
        )

        st.page_link(
            "pages/1_🐙_타코야끼.py",
            label="🐙 타코야끼 가게 입장하기",
            use_container_width=True,
        )

    # 오코노미야끼
    with col2:

        okonomi_html = """
<div class="menu-card">
    <div class="menu-emoji">🍳</div>
    <div class="menu-title">오코노미야끼</div>
    <div class="menu-description">
        주문에 맞춰<br>
        맛있는 오코노미야끼를 만드세요!
    </div>
</div>
"""

        st.markdown(
            textwrap.dedent(okonomi_html).strip(),
            unsafe_allow_html=True,
        )

        st.page_link(
            "pages/2_🍳_오코노미야끼.py",
            label="🍳 오코노미야끼 가게 입장하기",
            use_container_width=True,
        )

    # 배경 꾸미기
    with col3:

        decorate_html = """
<div class="menu-card">
    <div class="menu-emoji">🎨</div>
    <div class="menu-title">배경 꾸미기</div>
    <div class="menu-description">
        배경과 캐릭터를 선택해<br>
        나만의 포장마차를 꾸며 보세요!
    </div>
</div>
"""

        st.markdown(
            textwrap.dedent(decorate_html).strip(),
            unsafe_allow_html=True,
        )

        st.page_link(
            "pages/3_🎨_배경_꾸미기.py",
            label="🎨 배경 꾸미러 가기",
            use_container_width=True,
        )

    # 하단 안내
    bottom_html = """
<div class="game-info">
    ❤️ 3개의 목숨으로 시작하고
    5레벨까지 생존하면 승리합니다!
</div>
"""

    st.markdown(
        textwrap.dedent(bottom_html).strip(),
        unsafe_allow_html=True,
    )
