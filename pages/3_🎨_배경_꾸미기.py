
import streamlit as st
from pathlib import Path

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

BACKGROUND_FILES = {
    "🌸 벚꽃 축제": "bg_spring.png",
    "🎆 여름 축제": "bg_summer.png",
    "🍁 가을 야시장": "bg_autumn.png",
    "❄️ 겨울 포장마차": "bg_winter.png",
}

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
if st.session_state.get("saved_bubble_style") == "💥 코믹 말풍선":
    st.session_state["saved_bubble_style"] = "✨ 강조 말풍선"

# ==========================================
# 3. 이미지 파일 경로
# ==========================================

# 이 파일이 pages 폴더 안에 있어도
# GitHub 저장소의 최상위 폴더를 기준으로 찾음
ROOT_DIR = Path(__file__).resolve().parent.parent

def get_background_path(background_name):
    filename = BACKGROUND_FILES.get(background_name)
    if not filename:
        return None

    return ROOT_DIR / filename

# ==========================================
# 4. 화면 디자인
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

.preview-box {
    padding: 12px 16px;
    margin-top: 8px;
    border: 3px solid #e8bb8f;
    border-radius: 16px;
    background: #fff8ec;
    color: #965438;
    font-weight: 800;
    text-align: center;
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
# 5. 페이지 제목
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
# 6. 꾸미기 설정
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

# ==========================================
# 7. 배경 이미지 미리보기
# ==========================================

st.html("""
<div class="preview-box">
    🖼️ 선택한 포장마차 배경 미리보기
</div>
""")

background_path = get_background_path(background)

if background_path is not None and background_path.is_file():
    st.image(
        str(background_path),
        use_container_width=True,
    )
else:
    st.info(
        "아직 배경 이미지가 등록되지 않았어요. "
        "GitHub에 해당 이미지 파일을 추가하면 "
        "이곳에 자동으로 표시돼요!"
    )

# ==========================================
# 8. 손님 및 말풍선 선택
# ==========================================

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

# ==========================================
# 9. 설정 저장
# ==========================================

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
# 10. 현재 저장된 설정
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
