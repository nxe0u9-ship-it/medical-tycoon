
import streamlit as st

# ==========================================
# 와글와글 포장마차 - 게임 잠금 해제 관리
# ==========================================

CLEAR_KEY = "takoyaki_cleared"
TEST_KEY = "okonomi_test_unlock"


# ==========================================
# 오코노미야끼 잠금 해제 여부
# ==========================================

def is_takoyaki_cleared():
    # 실제 타코야끼 5레벨 클리어 기록
    actually_cleared = st.session_state.get(
        CLEAR_KEY,
        False
    )

    # 개발 중 사이드바 테스트 스위치
    test_unlocked = st.session_state.get(
        TEST_KEY,
        False
    )

    # 둘 중 하나라도 True이면 입장 허용
    return actually_cleared or test_unlocked


# ==========================================
# 실제 타코야끼 클리어 기록
# ==========================================

def mark_takoyaki_cleared():
    st.session_state[CLEAR_KEY] = True


# ==========================================
# JavaScript → Streamlit 통신
# ==========================================

BRIDGE_JS = """
export default function(component) {

    const { setTriggerValue } = component;

    const receiveMessage = (event) => {

        const message = event.data;

        if (
            !message ||
            message.type !== "waggle_takoyaki_clear"
        ) {
            return;
        }

        if (message.cleared !== true) {
            return;
        }

        const gameFrames = document.querySelectorAll(
            "iframe"
        );

        const fromGame = Array.from(gameFrames).some(
            frame => frame.contentWindow === event.source
        );

        if (!fromGame) {
            return;
        }

        setTriggerValue(
            "cleared",
            true
        );
    };

    window.addEventListener(
        "message",
        receiveMessage
    );

    return () => {
        window.removeEventListener(
            "message",
            receiveMessage
        );
    };
}
"""


def listen_for_takoyaki_clear():

    bridge = st.components.v2.component(
        "waggle_takoyaki_unlock_bridge",
        js=BRIDGE_JS,
    )

    bridge(
        key="takoyaki_unlock_receiver",
        on_cleared_change=mark_takoyaki_cleared,
    )


# ==========================================
# 기존 게임 HTML에 클리어 신호 추가
# ==========================================

def add_takoyaki_clear_signal(game_html):

    original = "game.ended = true;"

    replacement = """
    game.ended = true;

    if (won) {
        window.parent.postMessage(
            {
                type: "waggle_takoyaki_clear",
                cleared: true
            },
            "*"
        );
    }
    """

    function_start = game_html.find(
        "function endGame(won)"
    )

    if function_start == -1:
        raise ValueError(
            "타코야끼 게임에서 "
            "endGame(won) 함수를 찾지 못했습니다."
        )

    before = game_html[:function_start]
    after = game_html[function_start:]

    if original not in after:
        raise ValueError(
            "게임 종료 상태 변경 코드를 "
            "찾지 못했습니다."
        )

    after = after.replace(
        original,
        replacement,
        1
    )

    return before + after
