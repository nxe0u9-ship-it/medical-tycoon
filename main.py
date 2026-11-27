# ==========================================
# 공통 사이드바
# ==========================================

with st.sidebar:

    owner = st.session_state.owner_name.strip()
    stall = st.session_state.stall_name.strip()
    sidebar_name = (
        f"{owner}의 {stall}"
        if owner and stall
        else "와글와글 포장마차"
    )
    st.title(f"🏮 {sidebar_name}")

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

    st.page_link(
        taco_page,
        label="타코야끼 도전하기",
    )

else:
    pg.run()
