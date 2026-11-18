
import streamlit as st

# =====================================
# 기본 페이지 설정
# =====================================

st.set_page_config(
    page_title="와글와글 포장마차",
    page_icon="🏮",
    layout="wide",
    initial_sidebar_state="collapsed",
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

st.html("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        180deg,
        #fff3dd 0%,
        #fbe1c2 60%,
        #f5ccab 100%
    );
}

[data-testid="stHeader"] {
    background: transparent;
    height: 2.5rem;
}

[data-testid="stSidebar"] {
    background: #fff7eb;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem;
}

[data-testid="stSidebar"] [data-testid="stPageLink"] {
    border-radius: 12px;
}

[data-testid="stSidebar"] [data-testid="stPageLink"]:hover {
    background: #f8dfc9;
}

.block-container {
    max-width: 1200px;
    padding-bottom: 1.5rem;
}

#MainMenu, footer {
    visibility: hidden;
}
</style>
""")


# =====================================
# 홈 화면
# =====================================

def render_home():

    st.html("""
    <style>
    .block-container {
        padding-top: clamp(3rem, 10vh, 6rem) !important;
    }

    .hero {
        position: relative;
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
        margin: 10px auto 13px;
        padding: 12px 28px;
        border: 4px solid #ffe9ae;
        border-radius: 17px;
        background: #a84839;
        color: #fff2ca;
        font-size: clamp(32px, 4vw, 50px);
        font-weight: 900;
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
        margin: 8px auto 7px;
        padding: 5px;
        font-size: 16px;
        font-weight: 900;
        color: #855337;
    }

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

    .lobby {
        background: #fff7e7;
        border: 5px solid #d69b70;
        border-radius: 24px;
        text-align: center;
        padding: 23px 18px;
        box-shadow: 0 7px 0 #aa7854;
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
        line-height: 1.7;
    }

    .menu-card {
        background: #fff8e9;
        border: 4px solid #e4b689;
        border-radius: 22px;
        text-align: center;
        min-height: 180px;
        padding: 19px 10px;
        margin-top: 15px;
    }

    .menu-emoji {
        font-size: 55px;
    }

    .menu-title {
        color: #995338;
        font-size: 21px;
        font-weight: 900;
        margin: 8px auto;
    }

    .menu-description {
        color: #906248;
        font-size: 13px;
        font-weight: 700;
        line-height: 1.6;
    }

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

        .menu-title {
            font-size: 16px;
        }

        .menu-card {
            min-height: 160px;
            padding: 13px 5px;
        }
    }
    </style>
    """)

    # =====================================
    # 게임 시작 전 첫 화면
    # =====================================

    if not st.session_state.game_entered:

        st.html("""
        <style>
        [data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        </style>
        """)

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
                지금부터 나만의 포장마차를
                운영해 보세요.<br><br>
                원하는 게임을 선택해 주세요!
            </div>

        </div>
        """)

        col1, col2, col3 = st.columns(
            3,
            gap="medium"
        )

        # 타코야끼 카드
        with col1:

            st.html("""
            <div class="menu-card">
                <div class="menu-emoji">🐙</div>
                <div class="menu-title">타코야끼</div>
                <div class="menu-description">
                    타코야끼를 빠르게 구워<br>
                    손님에게 서빙하세요!
                </div>
            </div>
            """)

            st.page_link(
                taco_page,
                label="타코야끼 가게 입장하기",
                use_container_width=True,
            )

        # 오코노미야끼 카드
        with col2:

            st.html("""
            <div class="menu-card">
                <div class="menu-emoji">🍳</div>
                <div class="menu-title">오코노미야끼</div>
                <div class="menu-description">
                    주문에 맞춰<br>
                    맛있는 오코노미야끼를 만드세요!
                </div>
            </div>
            """)

            st.page_link(
                okonomi_page,
                label="오코노미야끼 가게 입장하기",
                use_container_width=True,
            )

        # 배경 꾸미기 카드
        with col3:

            st.html("""
            <div class="menu-card">
                <div class="menu-emoji">🎨</div>
                <div class="menu-title">배경 꾸미기</div>
                <div class="menu-description">
                    배경과 캐릭터를 선택해<br>
                    나만의 포장마차를 꾸며 보세요!
                </div>
            </div>
            """)

            st.page_link(
                decorate_page,
                label="배경 꾸미러 가기",
                use_container_width=True,
            )

        st.html("""
        <div class="game-info">
            ❤️ 3개의 목숨으로 시작하고
            5레벨까지 생존하면 승리합니다!
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
# 자동 메뉴 대신 직접 만든 메뉴 사용
# =====================================

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

if st.session_state.game_entered:

    with st.sidebar:

        st.title("🏮 와글와글 포장마차")

        st.caption("원하는 메뉴를 선택해 주세요!")

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

        st.button(
            "🏠 처음 화면으로",
            use_container_width=True,
            on_click=return_home,
        )


# =====================================
# 선택한 페이지 실행
# =====================================

pg.run()
