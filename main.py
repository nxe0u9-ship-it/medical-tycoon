import math
import random
import time

import streamlit as st


GAME_SECONDS = 75
FILLINGS = ["문어", "치즈", "새우"]
TOPPINGS = ["타코야끼 소스", "마요네즈", "가쓰오부시"]

st.set_page_config(
    page_title="타코야끼 타임어택",
    page_icon="🐙",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 850px; padding-top: 1.5rem;}
    .stButton > button {min-height: 3.2rem; font-weight: 700;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🐙 타코야끼 타임어택")
st.caption("제한 시간 75초! 주문을 확인하고 재료를 골라 타코야끼를 완성해 보세요.")


def create_order():
    return {
        "filling": random.choice(FILLINGS),
        "topping": random.choice(TOPPINGS),
    }


def start_game():
    st.session_state.tako_game = {
        "status": "playing",
        "started_at": time.time(),
        "order": create_order(),
        "stage": "batter",
        "flips": 0,
        "score": 0,
        "completed": 0,
        "combo": 0,
        "best_combo": 0,
        "mistakes": 0,
        "notice": "첫 주문이 들어왔어!",
    }


def time_left(game):
    return max(0, GAME_SECONDS - (time.time() - game["started_at"]))


def wrong_choice(game):
    game["score"] = max(0, game["score"] - 10)
    game["mistakes"] += 1
    game["combo"] = 0
    game["notice"] = "❌ 주문과 달라! 10점 감점. 다시 선택해 봐."


def completed_order(game):
    earned = 100 + min(game["combo"], 5) * 20
    game["score"] += earned
    game["completed"] += 1
    game["combo"] += 1
    game["best_combo"] = max(game["best_combo"], game["combo"])
    game["order"] = create_order()
    game["stage"] = "batter"
    game["flips"] = 0
    game["notice"] = f"✅ 완성! +{earned}점! 다음 주문이 들어왔어."


@st.fragment(run_every="1s")
def show_game():
    game = st.session_state.get("tako_game")

    if not game or game["status"] == "ready":
        st.subheader("🍽️ 게임 방법")
        st.write("① 반죽 붓기 → ② 주문한 속재료 선택 → ③ 두 번 뒤집기 → ④ 주문한 토핑 선택")
        st.write("정확히 만들면 100점! 연속 성공하면 콤보 보너스가 쌓여.")
        st.write("잘못 선택하면 10점이 깎이고 콤보가 초기화돼.")
        if st.button("🚀 게임 시작", type="primary", use_container_width=True):
            start_game()
            st.rerun(scope="fragment")
        return

    if game["status"] == "playing" and time_left(game) <= 0:
        game["status"] = "finished"

    seconds = math.ceil(time_left(game))
    col1, col2, col3, col4 = st.columns(4)
