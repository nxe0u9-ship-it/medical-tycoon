
import streamlit as st

st.set_page_config(
    page_title="오코노미야끼 | 와글와글 포장마차",
    page_icon="🍳",
    layout="wide",
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        180deg, #fff0d8, #f8d4aa
    );
}

.block-container {
    max-width: 1000px;
    padding-top: 3rem;
}

.title-box {
    background: #fff8e9;
    border: 5px solid #d99b62;
    border-radius: 25px;
    padding: 35px;
    text-align: center;
    box-shadow: 0 8px #ad754c;
}

.food-emoji {
    font-size: 85px;
    margin: 15px 0;
}

.game-title {
    color: #994d2f;
    font-size: 40px;
    font-weight: 900;
}

.description {
    color: #83573d;
    font-size: 18px;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-box">
    <div class="food-emoji">🍳</div>
    <div class="game-title">
        오코노미야끼 만들기
    </div>
    <div class="description">
        손님의 주문에 따라
        오코노미야끼를 빠르게 완성해 보세요!
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

st.subheader("🍳 오코노미야끼 타임어택")

st.info(
    "이 페이지에서는 반죽 만들기, "
    "재료 선택, 굽기, 뒤집기, "
    "토핑 올리기 기능을 구현할 예정이에요."
)

st.markdown("### 🎮 게임 규칙")

st.write(
    "❤️ 목숨 3개로 시작하며, "
    "레벨 5까지 살아남으면 승리합니다."
)

st.write(
    "⏱️ 레벨별 제한 시간: "
    "90초 → 120초 → 120초 → 150초 → 150초"
)
