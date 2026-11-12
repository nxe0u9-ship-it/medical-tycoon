
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

# Supabase 인증: 로그인한 계정만 게임 화면에 접근할 수 있다.
from supabase import create_client

if "supabase_client" not in st.session_state:
    try:
        st.session_state.supabase_client = create_client(
            st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"]
        )
    except (KeyError, FileNotFoundError):
        st.error("Streamlit Secrets에 SUPABASE_URL과 SUPABASE_KEY를 등록해 줘.")
        st.stop()

supabase = st.session_state.supabase_client

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if st.session_state.logged_in_user is None:
    st.title("🐾 동물보호소 타이쿤")
    st.caption("내 보호소를 운영하려면 로그인하거나 새 계정을 만들어 줘.")
    tab_login, tab_signup = st.tabs(["로그인", "회원가입"])

    with tab_login:
        with st.form("login_form"):
            login_email = st.text_input("이메일", key="login_email")
            login_password = st.text_input("비밀번호", type="password", key="login_password")
            login_submit = st.form_submit_button("로그인", use_container_width=True)
        if login_submit:
            try:
                result = supabase.auth.sign_in_with_password({
                    "email": login_email.strip(), "password": login_password
                })
                if result.user and result.session:
                    st.session_state.logged_in_user = result.user.id
                    st.rerun()
                else:
                    st.error("로그인할 수 없어. 이메일 인증 상태를 확인해 줘.")
            except Exception:
                st.error("로그인에 실패했어. 이메일, 비밀번호, 이메일 인증 여부를 확인해 줘.")

    with tab_signup:
        with st.form("signup_form"):
            signup_email = st.text_input("이메일", key="signup_email")
            signup_password = st.text_input("비밀번호 (6자 이상)", type="password", key="signup_password")
            signup_submit = st.form_submit_button("회원가입", use_container_width=True)
        if signup_submit:
            if len(signup_password) < 6:
                st.warning("비밀번호는 6자 이상으로 설정해 줘.")
            else:
                try:
                    result = supabase.auth.sign_up({
                        "email": signup_email.strip(), "password": signup_password
                    })
                    st.success("회원가입 요청이 완료됐어. 이메일 인증이 활성화돼 있다면 메일함에서 인증한 뒤 로그인해 줘.")
                except Exception:
                    st.error("회원가입에 실패했어. 입력값과 Supabase 인증 설정을 확인해 줘.")
    st.stop()

with st.sidebar:
    st.caption("로그인한 계정으로 플레이 중")
    if st.button("로그아웃", use_container_width=True):
        try:
            supabase.auth.sign_out()
        finally:
            # 이전 사용자의 진행 상황이 다음 계정에 남지 않도록 초기화한다.
            st.session_state.clear()
            st.rerun()

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

90
