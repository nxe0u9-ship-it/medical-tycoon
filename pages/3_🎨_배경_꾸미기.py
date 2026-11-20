
import streamlit as st

# ==========================================
# 와글와글 포장마차 - 배경 꾸미기
# ==========================================

# ==========================================
# 1. 꾸미기 선택 항목
# ==========================================

BACKGROUNDS = [
    "🌸 벚꽃 축제",
    "🎆 여름 축제",
    "🍁 가을 야시장",
    "❄️ 겨울 포장마차",
]

CUSTOMER_STYLES = [
    "🎆 축제 손님",
    "🎒 학생",
    "💼 직장인",
    "👕 캐주얼",
]

BUBBLE_STYLES = [
    "💭 둥근 말풍선",
    "✨ 강조 말풍선",
    "▫️ 심플 말풍선",
]

# ==========================================
# 2. 기본 설정
# ==========================================

DEFAULTS = {
    "saved_background": "🌸 벚꽃 축제",
    "saved_customer_style": "🎆 축제 손님",
    "saved_bubble_style": "💭 둥근 말풍선",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 기존 코믹 말풍선 설정을 새 이름으로 변경
if (
    st.session_state.get("saved_bubble_style")
    == "💥 코믹 말풍선"
):
    st.session_state["saved_bubble_style"] = (
        "✨ 강조 말풍선"
    )

# ==========================================
# 3. 화면 디자인
# ==========================================

st.html("""
<style>

[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        180deg,
        #fff4e4 0%,
        #ffe0c5 100%
    );
}

[data-testid="stMain"] .block-container {
    max-width: 850px !important;
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

.decorate-title {
    padding: 24px 20px;
    margin-bottom: 25px;
    border: 4px solid #d7a077;
    border-radius: 22px;

    background: #fff7e8;
    box-shadow: 0 6px #b9825d;

    text-align: center;
}

.decorate-title h1 {
    margin: 0 0 10px;
    color: #965032;
    font-size: 32px;
    font-weight: 900;
}

.decorate-title p {
    margin: 0;
    color: #90634b;
    font-size: 15px;
    font-weight: 700;
}

.section-title {
    margin: 12px 0;
    color: #965438;
    font-size: 21px;
    font-weight: 900;
}

.saved-settings {
    padding: 20px;
    margin-top: 8px;

    border: 3px solid #e8bb8f;
    border-radius: 18px;

    background: #fff8ec;
}

.saved-settings h3 {
    margin: 0 0 14px;
    color: #965438;
    font-size: 20px;
}

.saved-item {
    padding: 10px 0;
    color: #795039;
    font-size: 15px;
    font-weight: 700;
}

.saved-label {
    display: inline-block;
    min-width: 130px;
    color: #ad714e;
}

.stButton button[kind="primary"] {
    background: #c83e50 !important;
    color: white !important;
    border-radius: 11px !important;
    min-height: 45px !important;
    font-weight: 800 !important;
}

</style>
""")

# ==========================================
# 4. 페이지 제목
# ==========================================

st.html("""
<div class="decorate-title">
    <h1>🎨 나만의 포장마차 꾸미기</h1>
    <p>
        포장마차 배경과 손님 스타일,
        주문 말풍선을 원하는 대로 선택해 보세요!
    </p>
</div>
""")

# ==========================================
# 5. 꾸미기 설정
# ==========================================

st.html("""
<div class="section-title">
    🏮 꾸미기 설정
</div>
""")

background = st.selectbox(
    "🌸 포장마차 배경",
    BACKGROUNDS,
    index=BACKGROUNDS.index(
        st.session_state.saved_background
        if st.session_state.saved_background in BACKGROUNDS
        else BACKGROUNDS[0]
    ),
)

customer_style = st.selectbox(
    "👥 손님 스타일",
    CUSTOMER_STYLES,
    index=CUSTOMER_STYLES.index(
        st.session_state.saved_customer_style
        if st.session_state.saved_customer_style in CUSTOMER_STYLES
        else CUSTOMER_STYLES[0]
    ),
)

bubble_style = st.selectbox(
    "💬 주문 말풍선",
    BUBBLE_STYLES,
    index=BUBBLE_STYLES.index(
        st.session_state.saved_bubble_style
        if st.session_state.saved_bubble_style in BUBBLE_STYLES
        else BUBBLE_STYLES[0]
    ),
)

st.write("")

if st.button(
    "💾 꾸미기 설정 저장하기",
    type="primary",
    use_container_width=True,
):
    st.session_state.saved_background = background
    st.session_state.saved_customer_style = customer_style
    st.session_state.saved_bubble_style = bubble_style

    st.success("꾸미기 설정이 저장되었어요!")

# ==========================================
# 6. 현재 저장된 설정
# ==========================================

st.divider()

st.html("""
<div class="section-title">
    📋 현재 저장된 꾸미기 설정
</div>
""")

st.write(
    f"🌸 **포장마차 배경:** "
    f"{st.session_state.saved_background}"
)

st.write(
    f"👥 **손님 스타일:** "
    f"{st.session_state.saved_customer_style}"
)

st.write(
    f"💬 **주문 말풍선:** "
    f"{st.session_state.saved_bubble_style}"
)
