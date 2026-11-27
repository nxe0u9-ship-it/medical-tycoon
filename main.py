
import streamlit as st
from pathlib import Path
import base64

from game_unlock import is_takoyaki_cleared

# ==========================================
# 와글와글 포장마차 - 메인 화면
# ==========================================

st.set_page_config(
    page_title="와글와글 포장마차",
    page_icon="🏮",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# 세션 초기화
# ==========================================

if "game_entered" not in st.session_state:
    st.session_state.game_entered = False

if "okonomi_test_unlock" not in st.session_state:
    st.session_state.okonomi_test_unlock = False


# ==========================================
# 시작 화면 손님 이미지 불러오기
# ==========================================

ROOT = Path(__file__).resolve().parent

FESTIVAL_IMAGE_DIR = (
    ROOT / "assets" / "customers" / "festival"
)


def load_festival_customers():
    """
    축제 손님 1~4번의 웃는 표정 PNG를 불러옵니다.
    파일이 없으면 해당 이미지만 건너뜁니다.
    """
    image_tags = []

    for number in range(1, 5):
        filename = (
            f"festival_{number:02d}_happy.png"
        )

        image_path = FESTIVAL_IMAGE_DIR / filename

        if not image_path.is_file():
            continue

        encoded = base64.b64encode(
            image_path.read_bytes()
        ).decode("ascii")

        image_url = (
            "data:image/png;base64," + encoded
        )

        image_tags.append(
            f"""
            <img
                src="{image_url}"
                alt="웃는 축제 손님 {number}"
                draggable="false"
            >
            """
        )

    return "\n".join(image_tags)


# ==========================================
# 페이지 이동 함수
# ==========================================

def enter_game():
    st.session_state.game_entered = True


def return_home():
    st.session_state.game_entered = False
    st.switch_page(home_page)


# ==========================================
# 공통 화면 스타일
# ==========================================

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

[data-testid="stSidebarUserContent"] {
    padding-top: 1rem;
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


# ==========================================
# 홈 페이지
# ==========================================

def render_home():

    cleared = is_takoyaki_cleared()

    # ======================================
    # 홈 화면 디자인
    # ======================================

    st.html(r"""
    <style>

    .block-container {
        padding-top: clamp(
            3rem,
            10vh,
            6rem
        ) !important;
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

        font-size: clamp(
            28px,
            3.5vw,
            50px
        );

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
       포장마차
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

    /* =====================================
       웃는 축제 손님 PNG 4명
    ===================================== */

    .festival-customers {
        display: flex;
        align-items: flex-end;
        justify-content: center;

        gap: 12px;

        max-width: 550px;
        min-height: 115px;

        margin: 12px auto 0;
    }

    .festival-customers img {
        display: block;

        width: min(22%, 115px);
        height: 110px;

        object-fit: contain;
        object-position: center bottom;

        user-select: none;

        filter: drop-shadow(
            0 3px 3px rgba(0, 0, 0, 0.13)
        );
    }

    /* =====================================
       게임 정보
    ===================================== */

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

        box-shadow:
            0 5px 0 #a05233 !important;
    }

    .st-key-game_start_button button:hover {
        background: #f58c56 !important;
        transform: translateY(-2px);
    }

    /* =====================================
       게임 선택 로비
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

        font-size: clamp(
            25px,
            3vw,
            34px
        );

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
       게임 선택 카드
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

        box-shadow:
            0 5px 0 #d29b70 !important;

        transition:
            transform .15s ease,
            box-shadow .15s ease,
            background .15s ease;
    }

    .st-key-card_taco button p,
    .st-key-card_okonomi button p,
    .st-key-card_decorate button p {
        font-size: 23px !important;
        font-weight: 900 !important;

        color: #995338 !important;

        margin: 0 !important;
        line-height: 1.3 !important;
    }

    /* 게임 카드 이모지 */

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

    /* 게임 카드 설명 */

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
        content:
            "주문을 받고 빠르게 구워\A손님에게 서빙하세요!";
    }

    .st-key-card_okonomi button::after {
        content:
            "반죽을 굽고 뒤집어\A주문을 완성하세요!";
    }

    .st-key-card_decorate button::after {
        content:
            "나만의 포장마차를\A원하는 스타일로 꾸며 보세요!";
    }

    /* 마우스를 올렸을 때 */

    .st-key-card_taco button:hover,
    .st-key-card_okonomi button:not(:disabled):hover,
    .st-key-card_decorate button:hover {
        background: #fff0d7 !important;
        border-color: #d9905a !important;

        transform: translateY(-5px);

        box-shadow:
            0 10px 0 #c68b61 !important;
    }

    /* =====================================
       잠긴 오코노미야끼
    ===================================== */

    .st-key-card_okonomi button:disabled {
        background: #e8e2dc !important;

        border-color: #c8bcb1 !important;

        box-shadow:
            0 5px 0 #b8aaa0 !important;

        opacity: .75 !important;
        cursor: not-allowed !important;
    }

    .st-key-card_okonomi button:disabled p {
        color: #87796d !important;
    }

    .st-key-card_okonomi button:disabled::after {
        content:
            "🔒 타코야끼 5레벨을\A클리어하면 열립니다!";

        color: #87796d;
    }

    /* =====================================
       화면 높이가 낮을 때
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

        .festival-customers {
            min-height: 85px;
            margin-top: 8px;
            gap: 8px;
        }

        .festival-customers img {
            height: 80px;
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
       모바일 화면
    ===================================== */

    @media (max-width: 700px) {

        .block-container {
            padding-left: .6rem !important;
            padding-right: .6rem !important;
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

        .stall-food {
            letter-spacing: 2px;
            font-size: 35px;
        }

        .festival-customers {
            gap: 5px;
            min-height: 75px;
            margin-top: 7px;
        }

        .festival-customers img {
            height: 75px;
        }

        .st-key-card_taco button,
        .st-key-card_okonomi button,
        .st-key-card_decorate button {
            min-height: 195px !important;
        }
    }

    </style>
    """)

    # ======================================
    # 게임 시작 전 첫 화면
    # ======================================

    if not st.session_state.game_entered:

        # 첫 화면에서는 사이드바 숨김
        st.html("""
        <div
            id="splash-screen-marker"
            style="display:none;">
        </div>

        <style>
        body:has(#splash-screen-marker)
        [data-testid="stSidebar"],

        body:has(#splash-screen-marker)
        [data-testid="stSidebarCollapsedControl"],

        body:has(#splash-screen-marker)
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        </style>
        """)

        # 웃는 축제 손님 4명
        customer_markup = load_festival_customers()

        # 시작 화면 전체
        st.html(f"""
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

            <div class="festival-customers">
                {customer_markup}
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

    # ======================================
    # 게임 선택 로비
    # ======================================

    else:

        if st.session_state.okonomi_test_unlock:
            status_text = (
                "🧪 테스트용 잠금 해제 활성화! "
                "오코노미야끼에 바로 입장할 수 있어요."
            )

        elif cleared:
            status_text = (
                "🎉 타코야끼 클리어! "
                "오코노미야끼 가게가 열렸어요!"
            )

        else:
            status_text = (
                "🔒 타코야끼 5레벨을 클리어하면 "
                "오코노미야끼 가게가 열립니다!"
            )

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

        with col1:
            if st.button(
                "타코야끼",
                key="card_taco",
                use_container_width=True,
            ):
                st.switch_page(taco_page)

        with col2:
            if st.button(
                "오코노미야끼",
                key="card_okonomi",
                disabled=not cleared,
                use_container_width=True,
            ):
                st.switch_page(okonomi_page)

        with col3:
            if st.button(
                "배경 꾸미기",
                key="card_decorate",
                use_container_width=True,
            ):
                st.switch_page(decorate_page)

        st.html("""
        <div class="game-info">
            ❤️ 목숨 3개 · ⭐ 5레벨 도전
        </div>
        """)

        st.info(status_text)


# ==========================================
# 페이지 등록
# ==========================================

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


# ==========================================
# 페이지 이동 설정
# ==========================================

pg = st.navigation(
    [
        home_page,
        taco_page,
        okonomi_page,
        decorate_page,
    ],
    position="hidden",
)


# ==========================================
# 공통 사이드바
# ==========================================

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

    # 오코노미야끼 잠금 판정
    okonomi_unlocked = is_takoyaki_cleared()

    st.page_link(
        okonomi_page,
        label=(
            "오코노미야끼"
            if okonomi_unlocked
            else "오코노미야끼 🔒"
        ),
        disabled=not okonomi_unlocked,
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

    st.divider()

    # ======================================
    # 오코노미야끼 테스트용 잠금 해제
    # ======================================

    st.toggle(
        "🧪 오코노미야끼 테스트용 잠금 해제",
        key="okonomi_test_unlock",
        help=(
            "활성화하면 타코야끼 5레벨을 "
            "클리어하지 않아도 오코노미야끼에 "
            "입장할 수 있어요."
        ),
    )

    if st.session_state.okonomi_test_unlock:
        st.caption("🟢 테스트용 잠금 해제 ON")
    else:
        st.caption("🔒 테스트용 잠금 해제 OFF")


# ==========================================
# 선택한 페이지 실행
# ==========================================

# 직접 주소로 오코노미야끼에 접근해도
# 잠금 상태를 확인합니다.

if (
    pg.url_path == okonomi_page.url_path
    and not is_takoyaki_cleared()
):

    st.warning(
        "🔒 오코노미야끼 가게는 아직 잠겨 있어요!"
    )

    st.info(
        "사이드바에서 테스트용 잠금 해제를 "
        "활성화하거나, 타코야끼 5레벨을 "
        "클리어하면 오코노미야끼를 "
        "플레이할 수 있어요."
    )

    # 중복 문어 이모지 제거
    # 페이지 아이콘(icon="🐙")이 자동 표시됨
    st.page_link(
        taco_page,
        label="타코야끼 도전하기",
    )

else:
    pg.run()
