c.metric("🐾 누적 진료", f"{st.session_state.treated}마리")
d.metric("🏥 진료실 등급", f"{st.session_state.room_level}단계")

st.progress(
    (st.session_state.exp % 30) / 30,
    text=f"다음 레벨까지 경험치 {30 - st.session_state.exp % 30}"
)

st.divider()

# 병원 내부 화면
st.subheader("🏡 우리 동물병원")

def room(icon, name, locked=False):
    extra = " locked" if locked else ""
    return f"""
    <div class="room{extra}">
        <div class="room-icon">{icon}</div>
        <div class="room-name">{name}</div>
    </div>
    """

left, middle, right = st.columns(3)

with left:
    st.markdown(room("🛎️", "접수대"), unsafe_allow_html=True)

with middle:
    st.markdown(room("🐕", "대기실"), unsafe_allow_html=True)

with right:
    st.markdown(
        room("🩺", f"진료실 Lv.{st.session_state.room_level}"),
        unsafe_allow_html=True
    )

st.write("")

left, middle, right = st.columns(3)

with left:
    st.markdown(room("💊", "약품 보관실"), unsafe_allow_html=True)

with middle:
    st.markdown(room("🔬", "검사실 · 준비 중", True), unsafe_allow_html=True)

with right:
    st.markdown(room("🏥", "일반 병원 · 잠김", True), unsafe_allow_html=True)

st.divider()

# 환자 진료 시스템
st.subheader("🐾 환자 진료")

if st.session_state.message:
    st.success(st.session_state.message)
    st.session_state.message = ""

if st.session_state.patient is None:
    st.info("현재 대기 중인 환자가 없어. 새로운 환자를 접수해 봐!")

    if st.button("🐾 새로운 환자 접수", use_container_width=True):
        st.session_state.patient = random.choice(PATIENTS).copy()
        st.rerun()

else:
    patient = st.session_state.patient

    st.markdown(f"### {patient['animal']} · {patient['name']}")
    st.write(f"**방문 사유:** {patient['symptom']}")
    st.write(f"**예상 진료 수익:** {patient['reward']} 코인")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🩺 진료 완료", type="primary", use_container_width=True):
            reward = patient["reward"] + (st.session_state.room_level - 1) * 30

            st.session_state.money += reward
            st.session_state.exp += 10
            st.session_state.treated += 1
            st.session_state.patient = None
            st.session_state.message = (
                f"진료 완료! {reward}코인과 경험치 10을 획득했어."
            )
            st.rerun()

    with col2:
        if st.button("↩️ 접수 취소", use_container_width=True):
            st.session_state.patient = None
            st.rerun()

st.divider()

# 시설 업그레이드 시스템
st.subheader("🔧 병원 업그레이드")

st.write(f"현재 진료실 등급: **{st.session_state.room_level}단계**")
st.write(f"다음 업그레이드 비용: **{upgrade_cost:,} 코인**")
st.caption("진료실을 업그레이드하면 환자 한 명당 얻는 코인이 증가해.")

if st.button("⬆️ 진료실 업그레이드", use_container_width=True):
    if st.session_state.money >= upgrade_cost:
        st.session_state.money -= upgrade_cost
        st.session_state.room_level += 1
        st.session_state.message = "진료실 업그레이드 성공!"
        st.rerun()
    else:
        st.warning("코인이 부족해! 환자를 더 진료해 봐.")

st.divider()

st.caption("메디타운 | 동물병원 경영 시뮬레이션")
