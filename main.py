"""타코야끼 스피드 타임어택 — Streamlit 단일 파일 게임."""

import html
import math
import random
import time

import streamlit as st


GAME_SECONDS = 75
FILLINGS = ["문어", "치즈", "새우"]
TOPPINGS = ["타코야끼 소스", "마요네즈", "가쓰오부시"]
CUSTOMERS = [
    ("🐱", "고양이 손님"),
    ("🐻", "곰 손님"),
    ("🐰", "토끼 손님"),
    ("🦊", "여우 손님"),
    ("🐼", "판다 손님"),
]
FILLING_ICONS = {"문어": "🐙", "치즈": "🧀", "새우": "🦐"}

st.set_page_config(
    page_title="타코야끼 타임어택",
    page_icon="🐙",
    layout="centered",
)

st.markdown(
    """
<style>
.block-container {max-width: 850px; padding-top: 1.3rem; padding-bottom: 3rem;}
.stButton > button {min-height: 3.2rem; font-weight: 800; border-radius: 14px;}
.game-title {text-align:center; font-size:2.1rem; font-weight:900; letter-spacing:-1px; margin:0;}
.game-subtitle {text-align:center; color:#946f56; font-size:0.98rem; margin:0.4rem 0 1.1rem;}
.customer-card {
    display:flex; align-items:center; gap:18px; border-radius:20px;
    padding:18px 20px; background:#fff0d9; border:2px solid #f6cb8e;
    box-shadow:0 5px 0 #f2d8b7; margin:16px 0 20px;
}
.customer-face {font-size:3.4rem; line-height:1; animation:gentle-bob 2.3s ease-in-out infinite;}
.customer-name {font-size:0.85rem; font-weight:800; color:#936436;}
.customer-speech {color:#422b1d; font-size:1.06rem; font-weight:800; line-height:1.55;}
.kitchen {
    border:8px solid #70493b; border-radius:32px; padding:24px 12px;
    background:repeating-linear-gradient(130deg, #53403a, #53403a 11px, #604a41 12px, #604a41 20px);
    box-shadow:inset 0 7px 13px rgba(0,0,0,.3), 0 8px 0 #402d28;
    margin:14px auto 20px;
}
.pan {max-width:570px; margin:auto; border:9px solid #34373b; border-radius:30px; padding:19px;
    background:linear-gradient(130deg,#565b5f,#252a2d); box-shadow:inset 0 4px 10px rgba(0,0,0,.5);
    display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:16px;
}
.pan-hole {aspect-ratio:1; border-radius:50%; padding:6px;
    display:flex; align-items:center; justify-content:center;
    background:radial-gradient(circle at 45% 35%,#15191a,#323638 75%);
    box-shadow:inset 0 6px 11px #0d0e10,0 2px 2px #7e8589;
}
.ball {width:100%; height:100%; border-radius:50%; display:flex; align-items:center; justify-content:center;
    position:relative; font-size:clamp(1.25rem,4vw,2.3rem);
    box-shadow:inset -10px -10px 15px rgba(130,60,10,.17),inset 8px 8px 13px rgba(255,255,255,.28);
}
.ball.empty {background:transparent; box-shadow:none;}
.ball.batter {background:radial-gradient(circle at 35% 30%,#fff9ce,#f7dd86 72%,#dfb65c); animation:bubble 1.6s ease-in-out infinite;}
.ball.raw {background:radial-gradient(circle at 35% 25%,#ffeb94,#f9c968 65%,#d79a3e);}
.ball.half {background:radial-gradient(circle at 35% 25%,#ffd678,#e9a749 60%,#bd7029); animation:flip 0.7s ease-in-out;}
.ball.golden {background:radial-gradient(circle at 35% 25%,#ffe08a,#d9953f 55%,#9a5323);}
.ball.golden::before {content:""; position:absolute; inset:9%; border-radius:50%; border:2px dotted rgba(132,61,19,.4);}
.ball-icon {z-index:1; font-size:0.88em; filter:drop-shadow(0 2px 2px rgba(0,0,0,.12));}
.heat {text-align:center; color:#ffe9c4; font-weight:900; font-size:1rem; letter-spacing:1px; margin:18px auto 0;}
.stage-bar {display:flex; gap:6px; margin:14px 0; flex-wrap:wrap;}
.stage-chip {flex:1; min-width:100px; text-align:center; padding:9px 4px; border-radius:12px;
    font-weight:800; font-size:.85rem; background:#ece5de; color:#856e5b;}
.stage-chip.done {background:#dcf5d9; color:#296934;}
.stage-chip.now {background:#ffcf73; color:#5f330d; box-shadow:0 3px 0 #e9ad43;}
.served {color:#70451d; font-size:.87rem; font-weight:800; background:#fff3d9;
    border-radius:12px; padding:10px 15px; margin:10px 0;}
@keyframes gentle-bob {0%,100% {transform:translateY(0);} 50% {transform:translateY(-5px);}}
@keyframes bubble {0%,100% {transform:scale(.96);} 50% {transform:scale(1.02);}}
@keyframes flip {0% {transform:rotateX(0deg) translateY(0);} 55% {transform:rotateX(165deg) translateY(-15px);} 100% {transform:rotateX(360deg) translateY(0);}}
@media (max-width:560px) {
  .game-title {font-size:1.6rem;}
  .customer-face {font-size:2.6rem;}
  .customer-card {padding:14px 12px; gap:12px;}
  .pan {gap:7px; padding:10px; border-width:6px;}
  .kitchen {padding:10px 6px; border-width:5px;}
  .pan-hole {padding:3px;}
  .stage-chip {min-width:68px; font-size:.75rem;}
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="game-title">🐙 타코야끼 타임어택</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="game-subtitle">손님의 주문대로 만들고, 75초 안에 최고 점수에 도전해 봐!</div>',
    unsafe_allow_html=True,
)


def create_order():
    emoji, name = random.choice(CUSTOMERS)
    return {
        "filling": random.choice(FILLINGS),
        "topping": random.choice(TOPPINGS),
        "customer_emoji": emoji,
        "customer_name": name,
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
        "last_served": None,
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
    game["last_served"] = {
        "filling": game["order"]["filling"],
        "topping": game["order"]["topping"],
        "points": earned,
    }
    game["order"] = create_order()
    game["stage"] = "batter"
    game["flips"] = 0
    game["notice"] = f"✅ 완성! +{earned}점! 다음 주문이 들어왔어."


def draw_customer(order):
    emoji = html.escape(order["customer_emoji"])
    name = html.escape(order["customer_name"])
    filling = html.escape(order["filling"])
0
