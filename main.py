
import random
import streamlit as st

st.set_page_config(page_title="동물보호소 타이쿤", page_icon="🐾", layout="wide")

# 정식 게임 이름은 추후 결정. 현재는 동물보호소 경영 기능을 우선 구현한다.
ANIMALS = [
    {"name": "콩이", "species": "🐶 강아지", "story": "길가에서 구조되었어. 사람을 좋아하지만 조금 긴장했어."},
    {"name": "나비", "species": "🐱 고양이", "story": "공원에서 발견되었어. 조용한 공간을 좋아해."},
    {"name": "토토", "species": "🐰 토끼", "story": "보호소로 인계되었어. 새로운 환경에 적응하는 중이야."},
    {"name": "초코", "species": "🐶 강아지", "story": "동네 주민이 발견해 신고했어. 활발하고 장난기가 많아."},
    {"name": "보리", "species": "🐱 고양이", "story": "구조 후 안정을 찾고 있어. 천천히 친해질 시간이 필요해."},
]

INITIAL = {
    "coins": 700,
    "reputation": 0,
    "rescued": 0,
    "adopted": 0,
    "capacity": 2,
    "facility_level": 1,
    "animals": [],
    "message": "",
}
for key, value in INITIAL.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, list) else value

st.markdown("""
<style>
.stApp {background:linear-gradient(130deg,#effaf4,#fff9f1)}
.block-container {max-width:1150px;padding-top:1.8rem}
.room {background:#fff;border:2px solid #c9e5d4;border-radius:18px;
       text-align:center;padding:25px 8px;min-height:132px;box-shadow:0 4px 14px #00000008}
.room-icon {font-size:38px}.room-name {font-size:18px;font-weight:700;color:#39534a}
.room-sub {font-size:13px;color:#77857f;margin-top:6px}
</style>
""", unsafe_allow_html=True)


def shelter_level():
    return st.session_state.reputation // 30 + 1


def room(icon, name, detail):
    st.markdown(
        f'<div class="room"><div class="room-icon">{icon}</div>'
        f'<div class="room-name">{name}</div>'
        f'<div class="room-sub">{detail}</div></div>',
        unsafe_allow_html=True,
    )


st.title("🐾 동물보호소 타이쿤")
st.caption("작은 보호소에서 시작해 동물들이 새로운 가족을 만날 수 있도록 도와줘!")

cols = st.columns(5)
cols[0].metric("💰 보유 코인", f"{st.session_state.coins:,} C")
cols[1].metric("🌿 보호소 레벨", f"Lv.{shelter_level()}")
cols[2].metric("🐕 보호 중", f"{len(st.session_state.animals)}/{st.session_state.capacity}")
cols[3].metric("🚑 누적 구조", st.session_state.rescued)
cols[4].metric("🏡 누적 입양", st.session_state.adopted)

if st.session_state.message:
    st.success(st.session_state.message)
    st.session_state.message = ""

st.subheader("🏡 우리 보호소")
a, b, c = st.columns(3)
with a:
    room("🛎️", "접수·구조 센터", "새로운 동물 입소")
with b:
    room("🧺", "생활 공간", f"수용 가능 {st.session_state.capacity}마리")
with c:
    room("🧸", "놀이 공간", "돌봄으로 행복도 올리기")
st.write("")
a, b, c = st.columns(3)
with a:
    room("🥣", "급식실", "식사 제공")
with b:
    room("💌", "입양 상담실", "입양 조건 확인")
with c:
    room("🔨", "시설 확장", f"시설 {st.session_state.facility_level}단계")

st.divider()
st.subheader("🚑 동물 구조·입소")
st.write("구조 요청을 받아 동물을 보호소로 데려와. 보호 공간에 빈자리가 있어야 입소할 수 있어.")
if st.button("새로운 동물 구조하기", use_container_width=True):
    if len(st.session_state.animals) >= st.session_state.capacity:
        st.warning("보호 공간이 가득 찼어. 입양을 진행하거나 시설을 확장해 줘.")
    else:
        picked = random.choice(ANIMALS).copy()
        picked["id"] = st.session_state.rescued + 1
        picked["happiness"] = 30
        picked["health"] = 60
        st.session_state.animals.append(picked)
90
