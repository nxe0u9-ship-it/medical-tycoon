
import html
import random
import time

import streamlit as st

st.set_page_config(
    page_title="타코야끼 타임어택",
    page_icon="🐙",
    layout="centered"
)

GAME_SECONDS = 75
FILLINGS = ["문어", "치즈", "새우"]
TOPPINGS = ["타코야끼 소스", "마요네즈", "가쓰오부시"]
CUSTOMERS = [
    ("🐱", "고양이"),
    ("🐰", "토끼"),
    ("🐻", "곰"),
    ("🦊", "여우"),
]

st.markdown("""
<style>
.block-container {max-width: 820px; padding-top: 2rem;}
h1 {text-align:center; color:#bc652c;}
.stButton button {
    border-radius:14px;
    min-height:52px;
    font-weight:700;
}
.intro {
    text-align:center;
    color:#8b6a57;
    margin-bottom:20px;
}
.customer {
    display:flex;
    align-items:center;
    gap:18px;
    background:#fff0da;
    border:2px solid #f1c78f;
    border-radius:20px;
    padding:16px 22px;
    margin:15px 0;
}
.customer .face {
    font-size:3.3rem;
    animation:bob 2s ease-in-out infinite;
}
.customer .speech {
    font-size:1.05rem;
    color:#593b29;
    line-height:1.8;
}
.pan {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:14px;
    background:#424548;
    border:8px solid #6e4a39;
    border-radius:28px;
    padding:18px;
    max-width:530px;
    margin:15px auto 8px;
}
.hole {
    aspect-ratio:1;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    background:#222629;
    box-shadow:inset 0 5px 11px #131719;
    padding:7px;
}
.ball {
    height:100%;
    width:100%;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:clamp(1.4rem,4vw,2.4rem);
}
.ball.batter {
    background:radial-gradient(
        circle at 30% 25%,#fff9cf,#eecf79
    );
    animation:puff 1.3s infinite;
}
.ball.raw {
    background:radial-gradient(
        circle at 30% 25%,#ffe998,#eab45f
    );
}
.ball.half {
    background:radial-gradient(
        circle at 30% 25%,#ffd477,#cd8737
    );
}
.ball.done {
    background:radial-gradient(
        circle at 30% 25%,#f5cd72,#a9642b
    );
}
.stages {
    display:flex;
    gap:5px;
    margin:14px 0;
}
.stage {
    flex:1;
    background:#ede6dd;
    color:#685447;
    padding:9px 3px;
    font-size:.82rem;
    font-weight:700;
    text-align:center;
    border-radius:11px;
}
.stage.active {
    background:#ffc76b;
    color:#694016;
}
.stage.finished {
    background:#d4ecd2;
    color:#27623b;
}
@keyframes bob {
    50% {transform:translateY(-5px);}
}
@keyframes puff {
    50% {transform:scale(1.04);}
}
</style>
""", unsafe_allow_html=True)


def new_order():
    return {
        "customer": random.choice(CUSTOMERS),
        "filling": random.choice(FILLINGS),
        "topping": random.choice(TOPPINGS),
    }


def start_game():
    st.session_state.game = {
        "status": "playing",
        "start": time.time(),
        "order": new_order(),
        "stage": "batter",
        "flips": 0,
        "score": 0,
        "completed": 0,
        "combo": 0,
        "best_combo": 0,
        "mistakes": 0,
        "message": "첫 주문이 들어왔어! 반죽부터 부어 줘.",
    }


def remaining_seconds(game):
    return max(
        0,
        GAME_SECONDS - (time.time() - game["start"])
    )


def finish_game():
    st.session_state.game["status"] = "finished"


def wrong_answer(game):
    game["score"] = max(0, game["score"] - 10)
    game["mistakes"] += 1
    game["combo"] = 0
    game["message"] = "❌ 주문과 달라! 10점 감점. 다시 골라 줘."


def choose(action, value=""):
    game = st.session_state.game

    if game["status"] != "playing":
        return

    if remaining_seconds(game) <= 0:
        finish_game()
        return

    stage = game["stage"]

    if stage == "batter" and action == "batter":
        game["stage"] = "filling"
        game["message"] = "반죽 완료! 주문받은 속재료를 골라 줘."

    elif stage == "filling" and action == "filling":
        if value == game["order"]["filling"]:
            game["stage"] = "flip"
            game["message"] = "재료가 맞아! 타코야끼를 두 번 뒤집어 줘."
        else:
            wrong_answer(game)

    elif stage == "flip" and action == "flip":
        game["flips"] += 1

        if game["flips"] >= 2:
            game["stage"] = "topping"
            game["message"] = "노릇하게 익었어! 주문한 토핑을 골라 줘."
        else:
            game["message"] = "첫 번째 뒤집기 성공! 한 번 더 뒤집어 줘."

    elif stage == "topping" and action == "topping":
        if value == game["order"]["topping"]:
            points = 100 + min(game["combo"], 5) * 20

            game["score"] += points
            game["completed"] += 1
            game["combo"] += 1
            game["best_combo"] = max(
                game["best_combo"],
                game["combo"]
            )

            game["order"] = new_order()
            game["stage"] = "batter"
            game["flips"] = 0
            game["message"] = (
                f"🎉 주문 완성! +{points}점! "
                "다음 주문을 준비해 줘."
            )
        else:
            wrong_answer(game)


def draw_pan(game):
    stage = game["stage"]
    style = ""
    icon = ""

    if stage == "filling":
        style, icon = "batter", "🥣"

    elif stage == "flip":
        style = "half" if game["flips"] else "raw"
        icon = {
            "문어": "🐙",
            "치즈": "🧀",
            "새우": "🦐"
        }[game["order"]["filling"]]

    elif stage == "topping":
        style, icon = "done", "✨"

    balls = "".join(
        f'<div class="hole">'
        f'<div class="ball {style}">{icon}</div>'
        f'</div>'
        for _ in range(6)
    )

    st.markdown(
        f'<div class="pan">{balls}</div>',
        unsafe_allow_html=True
    )
    st.caption("🔥 따끈따끈한 타코야끼 6구 조리판")


def draw_stages(game):
    labels = [
        ("batter", "① 반죽"),
        ("filling", "② 재료"),
        ("flip", "③ 뒤집기"),
        ("topping", "④ 토핑"),
    ]

    stages = [item[0] for item in labels]
    current = stages.index(game["stage"])

    cards = "".join(
        f'<div class="stage '
        f'{"finished" if i < current else "active" if i == current else ""}'
        f'">{label}</div>'
        for i, (_, label) in enumerate(labels)
    )

    st.markdown(
        f'<div class="stages">{cards}</div>',
        unsafe_allow_html=True
    )


@st.fragment(run_every="1s")
def show_timer():
    game = st.session_state.game
    seconds = remaining_seconds(game)

    if seconds <= 0:
        game["status"] = "finished"
        st.rerun()

    st.progress(
        seconds / GAME_SECONDS,
        text=f"⏱️ 남은 시간: {seconds:.0f}초"
    )


st.title("🐙 타코야끼 타임어택")
st.markdown(
    '<div class="intro">'
    '75초 안에 주문을 빠르고 정확하게 완성해 봐!'
    '</div>',
    unsafe_allow_html=True
)

if "game" not in st.session_state:
    st.session_state.game = {"status": "ready"}

game = st.session_state.game


if game["status"] == "ready":
    st.info(
        "반죽 → 속재료 → 2번 뒤집기 → 토핑 순서로 요리해!"
    )
    st.write(
        "정확하게 완성하면 100점, 연속 성공하면 콤보 보너스! "
        "틀리면 10점 감점이야."
    )
    st.button(
        "🍳 게임 시작하기",
        use_container_width=True,
        type="primary",
        on_click=start_game
    )

elif game["status"] == "playing":
    show_timer()

    c1, c2, c3 = st.columns(3)
    c1.metric("⭐ 점수", game["score"])
    c2.metric("🐙 완성", f'{game["completed"]}개')
    c3.metric("🔥 콤보", game["combo"])

    order = game["order"]
    face, name = order["customer"]

    st.markdown(
        f'<div class="customer">'
        f'<div class="face">{face}</div>'
        f'<div class="speech">'
        f'<strong>{html.escape(name)} 손님</strong><br>'
        f'{html.escape(order["filling"])} 들어간 타코야끼에 '
        f'{html.escape(order["topping"])} 올려 주세요!'
        f'</div></div>',
        unsafe_allow_html=True
    )

    draw_stages(game)
    draw_pan(game)
    st.info(game["message"])

    if game["stage"] == "batter":
        st.button(
            "🥣 반죽 붓기",
            use_container_width=True,
            type="primary",
            on_click=choose,
            args=("batter",)
        )

    elif game["stage"] == "filling":
        st.write("**속재료 선택**")
        cols = st.columns(3)

        for col, filling in zip(cols, FILLINGS):
            with col:
                st.button(
                    filling,
                    use_container_width=True,
                    on_click=choose,
                    args=("filling", filling)
                )

    elif game["stage"] == "flip":
        st.button(
            f'🍳 뒤집기 ({game["flips"]}/2)',
            use_container_width=True,
            type="primary",
            on_click=choose,
            args=("flip",)
        )

    elif game["stage"] == "topping":
        st.write("**토핑 선택**")
        cols = st.columns(3)

        for col, topping in zip(cols, TOPPINGS):
            with col:
                st.button(
                    topping,
                    use_container_width=True,
                    on_click=choose,
                    args=("topping", topping)
                )

    st.divider()
    st.button(
        "게임 끝내고 결과 보기",
        on_click=finish_game
    )

else:
    st.success("⏰ 게임 종료! 수고했어!")

    c1, c2, c3 = st.columns(3)
    c1.metric("최종 점수", f'{game["score"]}점')
    c2.metric("완성한 주문", f'{game["completed"]}개')
    c3.metric("최고 콤보", f'{game["best_combo"]}번')

    st.write(f'틀린 선택: {game["mistakes"]}회')

    if game["score"] >= 1000:
        st.subheader("🏆 전설의 타코야끼 장인")
    elif game["score"] >= 500:
        st.subheader("🌟 실력 있는 포장마차 요리사")
    else:
        st.subheader("🐣 성장 중인 타코야끼 요리사")

    st.button(
        "🔁 다시 도전하기",
        use_container_width=True,
        type="primary",
        on_click=start_game
    )
