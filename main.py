
import streamlit as st

# =====================================
# 기본 페이지 설정
# =====================================

st.set_page_config(
    page_title="와글와글 포장마차",
    page_icon="🏮",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "game_entered" not in st.session_state:
    st.session_state.game_entered = False


def enter_game():
    st.session_state.game_entered = True


def return_home():
    st.session_state.game_entered = False
    st.switch_page(home_page)


# =====================================
# 공통 디자인
# =====================================

st.html(r"""
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

/* 상단 영역 */
[data-testid="stHeader"] {
    background: transparent;
    height: 2.5rem;
}

/* 사이드바 */
[data-testid="stSidebar"] {
    background: #fff7eb;
}

[data-testid="stSidebarUserContent"] {
    padding-top: 1rem;
}

/* 사이드바 페이지 링크 */
[data-testid="stSidebar"] [data-testid="stPageLink"] {
    border-radius: 12px;
}

[data-testid="stSidebar"] [data-testid="stPageLink"]:hover {
    background: #f8dfc9;
}

/* 본문 */
.block-container {
    max-width: 1200px;
    padding-bottom: 1.5rem;
}

/* 기본 하단 메뉴 숨기기 */
#MainMenu, footer {
    visibility: hidden;
}

</style>
""")


# =====================================
# 홈 페이지 함수
# =====================================

def render_home():

    # =====================================
    # 홈 페이지 디자인
    # =====================================

    st.html(r"""
    <style>

    .block-container {
        padding-top: clamp(3rem, 10vh, 6rem) !important;
    }

    /* =====================================
       게임 시작 화면
    ===================================== */

    .hero {
        overflow: hidden;
        border: 7px solid #a85f3d;
        border-radius: 30px;
        padding: 22px 25px 28px;
        text-align: center;

        background: linear-gradient(
            180deg,
            #6684b3 0%,
            #f3ada0 55%,
            #ffdc9e 100%
        );

        box-shadow: 0 8px 0 #915637;
    }

    .hero-title {
        display: inline-block;
        max-width: 100%;

        margin: 10px auto 13px;
        padding: 12px 28px;

        border: 4px solid #ffe9ae;
        border-radius: 17px;

        background: #a84839;
        color: #fff2ca;

        font-size: clamp(28px, 3.5vw, 50px);
        font-weight: 900;
        line-height: 1.3;

        text-shadow: 2px 3px #6d332c;
        box-shadow: 0 5px #74372c;
    }

    .hero-subtitle {
        color: #69402d;
        font-size: 19px;
        font-weight: 900;

        margin: 12px auto 18px;
        line-height: 1.5;
    }

    /* =====================================
       포장마차 그림
    ===================================== */

    .stall {
        max-width: 650px;
        margin: 0 auto;

        border: 5px solid #965537;
        border-radius: 21px;

        background: #fff0ce;
        overflow: hidden;

        box-shadow: 0 7px 0 #74442e;
    }

    .stall-roof {
        padding: 10px;
        font-size: 29px;

        background: repeating-linear-gradient(
            90deg,
            #c95045 0 73px,
            #ffe8c7 73px 146px
        );

        border-bottom: 4px solid #965537;
    }

    .stall-food {
        padding: 17px 10px;
        font-size: 53px;
        letter-spacing: 8px;
    }

    .stall-sign {
        padding: 8px;

        background: #8d4b32;
        color: #fff3d6;

        font-weight: 900;
        font-size: 14px;
    }

    .customers {
        font-size: 35px;
        margin-top: 17px;
        letter-spacing: 10px;
    }

    .game-info {
        text-align: center;
        margin: 13px auto 10px;
        padding: 5px;

        font-size: 16px;
        font-weight: 900;
        color: #855337;
    }

    /* =====================================
       게임 시작 버튼
    ===================================== */

    .st-key-game_start_button button {
        background: linear-gradient(
            180deg,
            #ffb06e,
            #e5754b
        ) !important;

        color: white !important;

        border: 3px solid #ab542e !important;
        border-radius: 17px !important;

        min-height: 68px !important;
        font-size: 23px !important;
        font-weight: 900 !important;

        box-shadow: 0 5px 0 #a05233 !important;
    }

    .st-key-game_start_button button:hover {
        background: #f58c56 !important;
        transform: translateY(-2px);
    }

    /* =====================================
       홈 안내 영역
    ===================================== */

    .lobby {
        background: #fff7e7;

        border: 5px solid #d69b70;
        border-radius: 24px;

        text-align: center;
        padding: 23px 18px;

        box-shadow: 0 7px #aa7854;
        margin-bottom: 16px;
    }

    .lobby-title {
        color: #9a4b31;

        font-size: clamp(25px, 3vw, 34px);
        font-weight: 900;

        margin-bottom: 10px;
    }

    .lobby-description {
        color: #84543d;

        font-size: 16px;
        font-weight: 700;
        line-height: 1.8;
    }

    /* =====================================
       클릭 가능한 메뉴 카드
    ===================================== */

    .st-key-card_taco button,
    .st-key-card_okonomi button,
    .st-key-card_decorate button {

        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;

        gap: 14px !important;

        width: 100% !important;
        min-height: 235px !important;
        padding: 20px 12px !important;

        border: 4px solid #e4b689 !important;
        border-radius: 24px !important;

        background: #fff8e9 !important;
        color: #995338 !important;

        box-shadow: 0 5px 0 #d29b70 !important;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease,
            background 0.15s ease;
    }

    /* 카드 제목 */

    .st-key-card_taco button p,
    .st-key-card_okonomi button p,
    .st-key-card_decorate button p {

        font-size: 23px !important;
        font-weight: 900 !important;

        color: #995338 !important;

        margin: 0 !important;
        line-height: 1.3 !important;
    }

    /* 카드 그림 */

    .st-key-card_taco button::before,
    .st-key-card_okonomi button::before,
    .st-key-card_decorate button::before {

        display: block;
        font-size: 57px;
        line-height: 1.2;
    }

    .st-key-card_taco button::before {
        content: "🐙";
    }

    .st-key-card_okonomi button::before {
        content: "🍳";
    }

    .st-key-card_decorate button::before {
        content: "🎨";
    }

    /* 카드 설명 */

    .st-key-card_taco button::after,
    .st-key-card_okonomi button::after,
    .st-key-card_decorate button::after {

        display: block;

        font-size: 13px;
        line-height: 1.7;
        font-weight: 800;

        color: #976443;

        white-space: pre-line;
        text-align: center;
    }

    .st-key-card_taco button::after {
        content: "주문을 받고 빠르게 구워\A손님에게 서빙하세요!";
    }

    .st-key-card_okonomi button::after {
        content: "반죽을 굽고 뒤집어\A주문을 완성하세요!";
    }

    .st-key-card_decorate button::after {
        content: "나만의 포장마차를\A원하는 스타일로 꾸며 보세요!";
    }

    /* 마우스를 올렸을 때 */

    .st-key-card_taco button:hover,
    .st-key-card_okonomi button:hover,
    .st-key-card_decorate button:hover {

        background: #fff0d7 !important;
        border-color: #d9905a !important;

        transform: translateY(-5px);

        box-shadow: 0 10px 0 #c68b61 !important;
    }

    /* 클릭 효과 */

    .st-key-card_taco button:active,
    .st-key-card_okonomi button:active,
    .st-key-card_decorate button:active {

        transform: translateY(2px);
        box-shadow: 0 2px 0 #c68b61 !important;
    }

    /* =====================================
       화면 높이가 작은 경우
    ===================================== */

    @media (max-height: 750px) {

        .block-container {
            padding-top: 2rem !important;
        }

        .hero {
            padding: 12px 15px 16px;
        }

        .hero-title {
            font-size: 32px;
            padding: 7px 16px;
            margin: 5px auto 9px;
        }

        .hero-subtitle {
            font-size: 15px;
            margin: 6px auto 10px;
        }

        .stall {
            max-width: 550px;
        }

        .stall-roof {
            font-size: 22px;
            padding: 4px;
        }

        .stall-food {
            padding: 9px;
            font-size: 40px;
        }

        .customers {
            font-size: 29px;
            margin-top: 9px;
        }

        .game-info {
            font-size: 13px;
        }

        .st-key-game_start_button button {
            min-height: 52px !important;
            font-size: 18px !important;
        }
    }

    /* =====================================
       모바일
    ===================================== */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
            padding-top: 1.5rem !important;
        }

        .hero {
            padding: 15px 8px;
            border-width: 5px;
        }

        .hero-title {
            font-size: 25px;
            padding: 9px;
        }

        .hero-subtitle {
            font-size: 15px;
        }

        .stall-food {
            letter-spacing: 2px;
            font-size: 35px;
        }

        .customers {
            letter-spacing: 3px;
            font-size: 27px;
        }

        .st-key-card_taco button,
        .st-key-card_okonomi button,
        .st-key-card_decorate button {
            min-height: 195px !important;
        }
    }

    </style>
    """)

    # =====================================
    # 게임 시작 전 첫 화면
    # =====================================

    if not st.session_state.game_entered:

        # 첫 화면에만 표시되는 구분 요소
        # 이 요소가 존재할 때만 사이드바를 숨김

        st.html("""
        <div
            id="splash-screen-marker"
            style="display:none;">
        </div>

        <style>

        body:has(#splash-screen-marker)
        [data-testid="stSidebar"] {
            display: none !important;
        }

        body:has(#splash-screen-marker)
        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }

        body:has(#splash-screen-marker)
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        /* 첫 화면에서는 본문을 전체 너비로 표시 */

        body:has(#splash-screen-marker)
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            width: 100% !important;
        }

        </style>
        """)

        # 첫 화면 포장마차 그림

        st.html("""
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
        """)

        st.html("""
        <div class="game-info">
            ❤️ 목숨 3개
            &nbsp; · &nbsp;
            ⭐ 5레벨 도전
            &nbsp; · &nbsp;
            🍳 2가지 요리
        </div>
        """)

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
    # 게임 시작 후 홈 화면
    # =====================================

    else:

        st.html("""
        <div class="lobby">

            <div class="lobby-title">
                🏮 와글와글 포장마차
            </div>

            <div class="lobby-description">
                어서 오세요!<br>
                오늘은 어떤 가게를 운영해 볼까요?<br><br>
                플레이할 메뉴를 선택해 주세요!
            </div>

        </div>
        """)

        col1, col2, col3 = st.columns(
            3,
            gap="medium"
        )

        # 타코야끼 카드

        with col1:

            if st.button(
                "타코야끼",
                key="card_taco",
                use_container_width=True,
            ):
                st.switch_page(taco_page)

        # 오코노미야끼 카드

        with col2:

            if st.button(
                "오코노미야끼",
                key="card_okonomi",
                use_container_width=True,
            ):
                st.switch_page(okonomi_page)

        # 배경 꾸미기 카드

        with col3:

            if st.button(
                "배경 꾸미기",
                key="card_decorate",
                use_container_width=True,
            ):
                st.switch_page(decorate_page)

        st.html("""
        <div class="game-info">
            ❤️ 목숨 3개 · ⭐ 5레벨 도전<br>
            카드를 눌러 원하는 가게에 입장하세요!
        </div>
        """)


# =====================================
# 페이지 등록
# =====================================

home_page = st.Page(
    render_home,
    title="홈",
    icon="🏠",
    default=True,
)

taco_page = st.Page(
    "pages/1_🐙_타코야끼.py",
    title="타코야끼",
    icon="🐙",
)

okonomi_page = st.Page(
    "pages/2_🍳_오코노미야끼.py",
    title="오코노미야끼",
    icon="🍳",
)

decorate_page = st.Page(
    "pages/3_🎨_배경_꾸미기.py",
    title="배경 꾸미기",
    icon="🎨",
)


# =====================================
# 페이지 이동 설정
# =====================================

# Streamlit의 기본 자동 메뉴는 숨기고
# 아래에서 사이드바를 직접 구성함

pg = st.navigation(
    [
        home_page,
        taco_page,
        okonomi_page,
        decorate_page,
    ],
    position="hidden",
)


# =====================================
# 공통 사이드바
# =====================================

# 사이드바는 모든 페이지에 생성하지만
# 첫 화면에서는 CSS로만 숨김

with st.sidebar:

    st.title("🏮 와글와글 포장마차")

    st.caption(
        "원하는 메뉴를 선택해 주세요!"
    )

    st.divider()

    st.page_link(
        home_page,
        label="홈",
        use_container_width=True,
    )

    st.page_link(
        taco_page,
        label="타코야끼",
        use_container_width=True,
    )

    st.page_link(
        okonomi_page,
        label="오코노미야끼",
        use_container_width=True,
    )

    st.page_link(
        decorate_page,
        label="배경 꾸미기",
        use_container_width=True,
    )

    st.divider()

    if st.button(
        "🏠 처음 화면으로",
        use_container_width=True,
    ):

        return_home()


# =====================================
# 선택한 페이지 실행
# =====================================

pg.run()
