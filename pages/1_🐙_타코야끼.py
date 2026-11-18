
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="타코야끼 | 와글와글 포장마차",
    page_icon="🐙",
    layout="wide",
)

st.markdown("""
<style>
.block-container {
    max-width: 100% !important;
    padding: 0.5rem !important;
}
[data-testid="stAppViewContainer"] {
    background: #fff0d8;
}
iframe {
    border: none;
    display: block;
}
</style>
""", unsafe_allow_html=True)

components.html(r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width,initial-scale=1.0">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: 'Malgun Gothic', sans-serif;
    color: #68412b;
}

button {
    font: inherit;
    cursor: pointer;
}

.game {
    position: relative;
    min-height: 850px;
    overflow: hidden;
    background: linear-gradient(
        #536c9b 0%,
        #e9a9a0 40%,
        #f3d7a5 70%,
        #bb8258 100%
    );
    padding: 15px;
    border-radius: 20px;
}

.decor {
    position: absolute;
    top: 65px;
    width: 95%;
    left: 2.5%;
    display: flex;
    justify-content: space-between;
    font-size: 48px;
    pointer-events: none;
}

.header {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
    z-index: 2;
}

.logo {
    background: #fff1ce;
    border: 4px solid #a85d37;
    color: #95472e;
    border-radius: 18px;
    padding: 12px;
    font-size: 22px;
    font-weight: 900;
}

.stats {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.stat {
    background: #794b3b;
    color: white;
    border: 3px solid #f1d49b;
    border-radius: 14px;
    padding: 9px;
    text-align: center;
    min-width: 90px;
    font-weight: 900;
    font-size: 20px;
}

.stat small {
    display: block;
    font-size: 11px;
    color: #ffe1b7;
}

.timer {
    background: #c55548;
}

.sign {
    position: relative;
    width: fit-content;
    max-width: 100%;
    margin: 18px auto 45px;
    padding: 12px 30px;
    background: #934a35;
    border: 5px solid #f2ca87;
    border-radius: 16px;
    color: #fff6da;
    font-size: 23px;
    font-weight: 900;
    text-align: center;
    box-shadow: 0 7px #683b29;
}

.customers {
    display: grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap: 12px;
    max-width: 1050px;
    margin: 0 auto 20px;
}

.customer {
    min-height: 160px;
    padding: 13px;
    border: 4px solid #d49d65;
    border-radius: 20px;
    background: #fff4dd;
    text-align: center;
    box-shadow: 0 7px #9d693f;
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-direction: column;
    gap: 5px;
}

.face {
    font-size: 38px;
}

.customer strong {
    font-size: 14px;
}

.order {
    font-size: 15px;
    font-weight: 900;
}

.patience {
    width: 90%;
    height: 12px;
    background: #dfc29d;
    border-radius: 10px;
    overflow: hidden;
}

.patience span {
    display: block;
    height: 100%;
    width: 100%;
    background: #70b963;
}

.counter {
    max-width: 1200px;
    margin: auto;
    padding: 16px;
    background: repeating-linear-gradient(
        0deg,
        #b87648 0 24px,
        #c88958 24px 48px
    );
    border: 8px solid #8e5334;
    border-radius: 25px;
    box-shadow: 0 12px #643b28;
}

.counter h3 {
    text-align: center;
    color: #fff3d4;
    text-shadow: 0 2px #73472e;
    margin: 0 0 15px;
}

.kitchen {
    display: grid;
    grid-template-columns: minmax(0,2fr) minmax(170px,1fr);
    gap: 14px;
}

.grills {
    display: grid;
    grid-template-columns: repeat(3,minmax(0,1fr));
    gap: 10px;
    background: #44434a;
    padding: 12px;
    border: 5px solid #302e34;
    border-radius: 20px;
}

.grill {
    min-height: 180px;
    border: 3px solid #686268;
    border-radius: 18px;
    background: #28282c;
    color: #fff5da;
    padding: 10px 4px;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 8px;
}

.holes {
    display: grid;
    grid-template-columns: repeat(2,1fr);
    gap: 5px;
    width: min(110px,90%);
    pointer-events: none;
}

.ball {
    aspect-ratio: 1;
    border-radius: 50%;
    background: #15161a;
    border: 3px solid #121319;
    display: grid;
    place-items: center;
    font-size: 20px;
}

.ball.cooking {
    background: radial-gradient(
        circle at 25% 25%,
        #fff1b0,
        #d9ab65
    );
    animation: fry .8s infinite alternate;
}

.ball.ready {
    background: radial-gradient(
        circle at 25% 25%,
        #f8d27a,
        #ad692b
    );
}

.ball.burnt {
    background: #493024;
}

@keyframes fry {
    to {
        transform: scale(1.07);
    }
}

.grill small {
    font-size: 11px;
    pointer-events: none;
}

.grill strong {
    pointer-events: none;
}

.bar {
    background: #151515;
    width: 80%;
    height: 9px;
    border-radius: 10px;
    overflow: hidden;
    pointer-events: none;
}

.bar span {
    display: block;
    width: 0;
    height: 100%;
    background: #efc456;
}

.right {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.plate-zone, .trash {
    border: 5px solid #e5bd8f;
    border-radius: 20px;
    background: #fff1d9;
    text-align: center;
    padding: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 8px;
}

.plate-zone {
    min-height: 175px;
}

.plate {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        white 0 48%,
        #b7d6e2 50% 60%,
        white 62%
    );
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    font-size: 38px;
}

.plate small {
    font-size: 11px;
    font-weight: 900;
}

.trash {
    min-height: 70px;
    background: #f9d6c7;
    font-weight: 900;
}

.supplies {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    max-width: 1200px;
    margin: 25px auto;
}

.supply {
    background: #fff1da;
    border: 4px solid #be8454;
    border-radius: 20px;
    padding: 13px;
}

.supply h3 {
    margin: 0 0 12px;
    font-size: 16px;
}

.items {
    display: flex;
    gap: 8px;
}

.item {
    flex: 1;
    min-width: 0;
    padding: 12px 5px;
    background: #fffaf1;
    border: 3px solid #e5c49a;
    border-radius: 14px;
    text-align: center;
    font-weight: 900;
    font-size: 14px;
}

.item span {
    display: block;
    font-size: 29px;
}

[data-source] {
    cursor: grab;
    touch-action: none;
    user-select: none;
}

[data-source]:active {
    cursor: grabbing;
}

.dragging-original {
    opacity: .45;
}

.drop-over {
    outline: 5px solid #ffe47c;
    outline-offset: 2px;
    filter: brightness(1.1);
}

.ghost {
    position: fixed;
    z-index: 100;
    pointer-events: none;
    transform: translate(-50%,-50%);
    padding: 12px;
    background: #fff4d9;
    border: 3px solid #d99a60;
    border-radius: 15px;
    text-align: center;
    font-size: 32px;
}

.ghost small {
    display: block;
    font-size: 11px;
}

.help {
    background: #744c36;
    color: white;
    text-align: center;
    font-size: 14px;
    font-weight: 900;
    padding: 12px;
    border-radius: 16px;
}

.toast {
    position: absolute;
    z-index: 15;
    bottom: 45px;
    left: 50%;
    transform: translateX(-50%);
    max-width: 90%;
    padding: 13px 20px;
    background: #493427;
    color: white;
    border-radius: 15px;
    opacity: 0;
    pointer-events: none;
    text-align: center;
    font-weight: 900;
}

.toast.show {
    opacity: 1;
}

.overlay {
    position: absolute;
    z-index: 30;
    inset: 0;
    background: #251b29bc;
    display: grid;
    place-items: center;
    padding: 20px;
}

.overlay.hidden {
    display: none;
}

.start-panel {
    width: min(500px,95%);
    padding: 30px;
    background: #fff0d0;
    border: 8px solid #e5af6c;
    border-radius: 30px;
    text-align: center;
    box-shadow: 0 15px #68412d;
}

.start-panel h1 {
    color: #a44c30;
    font-size: 36px;
}

.start-panel p {
    font-weight: 900;
    line-height: 1.8;
}

.start-button {
    padding: 17px 30px;
    background: #e8734c;
    color: white;
    border: 0;
    border-radius: 16px;
    box-shadow: 0 6px #aa4c30;
    font-size: 23px;
    font-weight: 900;
}

.countdown {
    position: absolute;
    z-index: 40;
    inset: 0;
    display: none;
    align-items: center;
    justify-content: center;
    background: #2d1e29ba;
    color: #fff2bc;
    font-size: clamp(80px,15vw,160px);
    font-weight: 900;
    text-shadow: 0 9px #82432e;
}

.countdown.show {
    display: flex;
}

@media(max-width:800px) {
    .game {
        padding: 8px;
        min-height: 830px;
    }

    .logo {
        font-size: 13px;
        padding: 7px;
    }

    .stat {
        font-size: 13px;
        min-width: 53px;
        padding: 5px;
    }

    .stat small {
        font-size: 9px;
    }

    .sign {
        font-size: 17px;
    }

    .customers {
        gap: 5px;
    }

    .customer {
        padding: 6px 2px;
        min-height: 135px;
    }

    .face {
        font-size: 25px;
    }

    .order {
        font-size: 11px;
    }

    .customer strong {
        font-size: 10px;
    }

    .kitchen {
        grid-template-columns: minmax(0,1.7fr) minmax(95px,.7fr);
        gap: 5px;
    }

    .counter {
        padding: 8px;
    }

    .grills {
        gap: 3px;
        padding: 5px;
    }

    .grill {
        min-height: 140px;
        padding: 5px 1px;
    }

    .ball {
        font-size: 12px;
        border-width: 1px;
    }

    .holes {
        gap: 2px;
    }

    .grill small {
        font-size: 8px;
    }

    .plate {
        width: 75px;
        height: 75px;
        font-size: 24px;
    }

    .supply {
        padding: 7px;
    }

    .supply h3 {
        font-size: 11px;
    }

    .item {
        font-size: 10px;
        padding: 7px 2px;
    }

    .item span {
        font-size: 19px;
    }
}
</style>
</head>

<body>

<div class="game">

<div class="decor">
    <span>🏮</span>
    <span>🏮</span>
</div>

<div class="header">

    <div class="logo">
        🏮 와글와글 포장마차
    </div>

    <div class="stats">

        <div class="stat">
            <small>레벨</small>
            <span id="level">1</span>/5
        </div>

        <div class="stat timer">
            <small>남은 시간</small>
            <span id="time">90</span>초
        </div>

        <div class="stat">
            <small>목숨</small>
            <span id="lives">❤️❤️❤️</span>
        </div>

        <div class="stat">
            <small>점수</small>
            <span id="score">0</span>
        </div>

    </div>

</div>

<div class="sign">
    🐙 타코야끼 가게 🐙
</div>

<div class="customers" id="customers"></div>

<div class="counter">

    <h3>🍳 타코야끼 조리대</h3>

    <div class="kitchen">

        <div class="grills" id="grills"></div>

        <div class="right">

            <div class="plate-zone"
                 data-drop="plate">

                <strong>🍽️ 완성 접시</strong>

                <div class="plate" id="plate">
                    🍽️
                </div>

                <small id="plate-help">
                    익은 타코야끼를 올려 주세요
                </small>

            </div>

            <div class="trash"
                 data-drop="trash">

                🗑️ 휴지통

            </div>

        </div>

    </div>

</div>

<div class="supplies">

    <div class="supply">
        <h3>① 속재료를 조리판으로 옮기세요</h3>
        <div class="items" id="fillings"></div>
    </div>

    <div class="supply">
        <h3>③ 토핑을 접시에 올리세요</h3>
        <div class="items" id="toppings"></div>
    </div>

</div>

<div class="help">
    ② 익은 음식 → 접시　
    ④ 완성 접시 → 손님　
    🗑️ 잘못 만든 음식 → 휴지통
</div>

<div class="toast" id="toast"></div>

<!-- 게임 시작 및 결과 화면 -->
<div class="overlay" id="overlay">

    <div class="start-panel">

        <div style="font-size:58px"
             id="panel-icon">
            🐙
        </div>

        <h1 id="panel-title">
            타코야끼 만들기
        </h1>

        <p id="panel-description">
            손님의 주문에 맞춰 타코야끼를 완성하세요!
            <br>
            ❤️ 목숨 3개 · 총 5레벨
            <br>
            5레벨까지 살아남으면 승리합니다!
        </p>

        <button class="start-button"
                id="start-button"
                onclick="beginCountdown()">

            🎮 타코야끼 만들기

        </button>

    </div>

</div>

<!-- 카운트다운 -->
<div class="countdown" id="countdown">
    <span id="count-text">3</span>
</div>

</div>

<script>

// 레벨별 제한 시간 (초)
const LEVEL_TIMES = [
    90, 120, 120, 150, 150
];

// 레벨별 손님 대기 시간 (초)
const CUSTOMER_WAIT = [
    [40,45],
    [30,35],
    [22,27],
    [15,20],
    [10,13]
];

const COOK_MS = 2700;
const BURN_MS = 6700;

const fillings = [
    {name:'문어', emoji:'🐙'},
    {name:'치즈', emoji:'🧀'},
    {name:'새우', emoji:'🦐'}
];

const toppings = [
    {name:'소스', emoji:'🍯'},
    {name:'마요네즈', emoji:'🥛'},
    {name:'가쓰오부시', emoji:'🍥'}
];

const faces = [
    '🐱','🐰','🐻','🦊','🐼','🐸'
];

const el = id => document.getElementById(id);
const now = () => performance.now();
const pick = arr =>
    arr[Math.floor(Math.random()*arr.length)];

let game = null;
let drag = null;
let highlighted = null;
let toastTimer = null;
let countdownActive = false;


// ====================================
// 카운트다운 시작
// ====================================

async function beginCountdown() {

    if (countdownActive) return;

    countdownActive = true;

    el('overlay').classList.add('hidden');

    el('countdown').classList.add('show');

    for (const number of ['3','2','1']) {

        el('count-text').textContent = number;

        await new Promise(
            resolve => setTimeout(resolve,1000)
        );
    }

    el('count-text').textContent = 'START!';

    await new Promise(
        resolve => setTimeout(resolve,700)
    );

    el('countdown').classList.remove('show');

    countdownActive = false;

    // 카운트다운이 끝난 다음 게임 시작
    startGame();
}


// ====================================
// 게임 시작
// ====================================

function startGame() {

    game = {
        level: 1,
        levelStart: now(),
        lives: 3,
        score: 0,
        combo: 0,
        best: 0,
        served: 0,
        missed: 0,
        plate: null,
        grills: [
            {state:'empty'},
            {state:'empty'},
            {state:'empty'}
        ],
        customers: [],
        ended: false
    };

    game.customers = [
        newCustomer(),
        newCustomer(),
        newCustomer()
    ];

    renderAll();

    tell('영업 시작! 주문을 만들어 주세요!');
}


// ====================================
// 손님 생성
// ====================================

function newCustomer() {

    const [min,max] =
        CUSTOMER_WAIT[game.level-1];

    return {
        face: pick(faces),
        fill: pick(fillings),
        top: pick(toppings),
        born: now(),
        patience: (
            min + Math.random()*(max-min)
        )*1000
    };
}


// ====================================
// 알림
// ====================================

function tell(message) {

    const box = el('toast');

    box.textContent = message;

    box.classList.add('show');

    clearTimeout(toastTimer);

    toastTimer = setTimeout(
        ()=>box.classList.remove('show'),
        1400
    );
}


// ====================================
// 화면 갱신
// ====================================

function renderAll() {
    renderCustomers();
    renderGrills();
    renderPlate();
    renderSupplies();
    updateHud();
}

function updateHud() {

    el('level').textContent = game.level;

    el('score').textContent = game.score;

    el('lives').textContent =
        '❤️'.repeat(game.lives) +
        '🖤'.repeat(3-game.lives);
}

function renderCustomers() {

    el('customers').innerHTML =
        game.customers.map((c,i)=>`

        <div class="customer"
             data-drop="customer"
             data-index="${i}">

            <span class="face">${c.face}</span>

            <strong>손님 ${i+1}</strong>

            <div class="order">
                ${c.fill.emoji} + ${c.top.emoji}
            </div>

            <div class="order">
                ${c.fill.name} + ${c.top.name}
            </div>

            <div class="patience">
                <span id="patience-${i}"></span>
            </div>

        </div>

        `).join('');
}

function renderGrills() {

    const messages = {
        empty: '재료를 올려 주세요',
        cooking: '굽는 중',
        ready: '접시로 옮기세요',
        burnt: '휴지통에 버리세요'
    };

    el('grills').innerHTML =
        game.grills.map((g,i)=>{

            const movable =
                g.state==='ready' ||
                g.state==='burnt';

            const icon =
                g.state==='cooking'?'🥣':
                g.state==='ready'
                    ?g.fill.emoji:
                g.state==='burnt'?'💨':'';

            const source = movable
                ? `data-source="grill"
                   data-index="${i}"
                   data-emoji="${icon}"
                   data-label="타코야끼"`
                : '';

            return `

            <div class="grill"
                 data-drop="grill"
                 data-index="${i}"
                 ${source}>

                <div class="holes">

                    ${Array.from(
                        {length:6},
                        ()=>`
                        <div class="ball ${g.state}">
                            ${icon}
                        </div>
                        `
                    ).join('')}

                </div>

                <strong>${i+1}번 조리판</strong>

                <div class="bar">
                    <span id="cook-${i}"></span>
                </div>

                <small>${messages[g.state]}</small>

            </div>
            `;
        }).join('');
}

function renderPlate() {

    const plate = el('plate');

    if (!game.plate) {

        plate.innerHTML = '🍽️';

        plate.removeAttribute('data-source');

        el('plate-help').textContent =
            '익은 타코야끼를 올려 주세요';

    } else {

        plate.innerHTML = `
            🐙
            <small>
                ${game.plate.fill.name}
                ${game.plate.top
                    ?' + '+game.plate.top.name
                    :''}
            </small>
        `;

        plate.setAttribute('data-source','plate');
        plate.setAttribute('data-emoji','🍡');
        plate.setAttribute('data-label','접시');

        el('plate-help').textContent =
            game.plate.top
                ?'손님에게 서빙하세요'
                :'토핑을 올려 주세요';
    }
}

function renderSupplies() {

    el('fillings').innerHTML =
        fillings.map((f,i)=>`

        <div class="item"
             data-source="filling"
             data-index="${i}"
             data-emoji="${f.emoji}"
             data-label="${f.name}">

            <span>${f.emoji}</span>
            ${f.name}

        </div>

        `).join('');

    el('toppings').innerHTML =
        toppings.map((t,i)=>`

        <div class="item"
             data-source="topping"
             data-index="${i}"
             data-emoji="${t.emoji}"
             data-label="${t.name}">

            <span>${t.emoji}</span>
            ${t.name}

        </div>

        `).join('');
}


// ====================================
// 드래그 앤 드롭 처리
// ====================================

function handleDrop(kind,index,target,targetIndex) {

    if (!game || game.ended) return;

    // 재료를 조리판에 올리기
    if (kind==='filling' && target==='grill') {

        if (game.grills[targetIndex].state!=='empty') {
            tell('이미 사용 중인 조리판입니다!');
            return;
        }

        game.grills[targetIndex] = {
            state:'cooking',
            fill:fillings[index],
            born:now()
        };

        renderGrills();
        return;
    }

    // 익은 타코야끼를 접시로
    if (kind==='grill' && target==='plate') {

        const g = game.grills[index];

        if (g.state!=='ready') {
            tell('익은 음식만 담을 수 있습니다!');
            return;
        }

        if (game.plate) {
            tell('접시가 이미 차 있습니다!');
            return;
        }

        game.plate = {
            fill:g.fill,
            top:null
        };

        game.grills[index] = {state:'empty'};

        renderGrills();
        renderPlate();
        return;
    }

    // 토핑을 접시에 올리기
    if (kind==='topping' && target==='plate') {

        if (!game.plate) {
            tell('타코야끼를 먼저 담아 주세요!');
            return;
        }

        game.plate.top = toppings[index];
        renderPlate();
        return;
    }

    // 손님에게 서빙
    if (kind==='plate' && target==='customer') {

        if (!game.plate?.top) {
            tell('토핑을 먼저 올려 주세요!');
            return;
        }

        const c = game.customers[targetIndex];

        if (
            c.fill.name===game.plate.fill.name &&
            c.top.name===game.plate.top.name
        ) {

            const points =
                100+Math.min(game.combo,5)*20;

            game.score += points;
            game.combo++;
            game.best = Math.max(
                game.best,game.combo
            );
            game.served++;

            game.customers[targetIndex] =
                newCustomer();

            tell(`주문 성공! +${points}점`);

        } else {
            loseLife('잘못된 주문입니다!');
        }

        game.plate = null;

        renderPlate();
        renderCustomers();
        updateHud();
        return;
    }

    // 휴지통
    if (target==='trash') {

        if (kind==='plate') {

            game.plate = null;
            renderPlate();
            tell('음식을 버렸습니다!');
            return;
        }

        if (kind==='grill') {

            game.grills[index] = {
                state:'empty'
            };

            renderGrills();
            tell('음식을 버렸습니다!');
            return;
        }
    }

    tell('이곳에는 놓을 수 없습니다!');
}


// ====================================
// 마우스 드래그 처리
// ====================================

function moveGhost(e) {

    if (!drag) return;

    drag.ghost.style.left =
        e.clientX+'px';

    drag.ghost.style.top =
        e.clientY+'px';

    const target =
        document.elementFromPoint(
            e.clientX,e.clientY
        )?.closest('[data-drop]');

    if (highlighted) {
        highlighted.classList.remove('drop-over');
    }

    highlighted = target;

    if (target) {
        target.classList.add('drop-over');
    }
}

document.addEventListener('pointerdown',e=>{

    if (!game || game.ended || drag) return;

    const source =
        e.target.closest('[data-source]');

    if (!source) return;

    e.preventDefault();

    const ghost = document.createElement('div');

    ghost.className = 'ghost';

    ghost.innerHTML = `
        ${source.dataset.emoji}
        <small>${source.dataset.label}</small>
    `;

    document.body.appendChild(ghost);

    drag = {
        pointerId:e.pointerId,
        source:source,
        kind:source.dataset.source,
        index:Number(source.dataset.index||0),
        ghost:ghost
    };

    source.classList.add('dragging-original');

    moveGhost(e);
});

document.addEventListener(
    'pointermove',
    e=>{
        if (drag && drag.pointerId===e.pointerId) {
            e.preventDefault();
            moveGhost(e);
        }
    },
    {passive:false}
);

function releaseDrag(e) {

    if (!drag || drag.pointerId!==e.pointerId) {
        return;
    }

    const current = drag;

    const target =
        document.elementFromPoint(
            e.clientX,e.clientY
        )?.closest('[data-drop]');

    current.ghost.remove();

    current.source.classList.remove(
        'dragging-original'
    );

    if (highlighted) {
        highlighted.classList.remove('drop-over');
    }

    highlighted = null;
    drag = null;

    if (target) {
        handleDrop(
            current.kind,
            current.index,
            target.dataset.drop,
            Number(target.dataset.index||0)
        );
    }
}

document.addEventListener('pointerup',releaseDrag);

document.addEventListener('pointercancel',e=>{
    if (!drag || drag.pointerId!==e.pointerId) {
        return;
    }
    drag.ghost.remove();
    if (drag.source.isConnected) {
        drag.source.classList.remove('dragging-original');
    }
    if (highlighted) {
        highlighted.classList.remove('drop-over');
    }
    highlighted = null;
    drag = null;
});


// ====================================
// 목숨 감소
// ====================================

function loseLife(message) {

    if (game.ended) return;

    game.lives--;
    game.combo=0;

    updateHud();

    if (game.lives<=0) {
        endGame(false);
    } else {
        tell(
            `${message} 남은 목숨 ${game.lives}개`
        );
    }
}


// ====================================
// 레벨 전환
// ====================================

function nextLevel() {

    if (game.level===5) {
        endGame(true);
        return;
    }

    game.level++;
    game.levelStart=now();

    game.grills = [
        {state:'empty'},
        {state:'empty'},
        {state:'empty'}
    ];

    game.plate=null;

    game.customers=[
        newCustomer(),
        newCustomer(),
        newCustomer()
    ];

    renderAll();

    tell(`LEVEL ${game.level} 시작!`);
}


// ====================================
// 게임 결과
// ====================================

function endGame(won) {

    game.ended=true;

    el('panel-icon').textContent =
        won?'🏆':'💔';

    el('panel-title').textContent =
        won?'최종 승리!':'게임 오버!';

    el('panel-description').innerHTML = `
        도달 레벨: ${game.level}/5<br>
        완성한 주문: ${game.served}개<br>
        최종 점수: ${game.score}점<br>
        최고 콤보: ${game.best}회<br>
        놓친 주문: ${game.missed}개
    `;

    el('start-button').textContent =
        '🔄 다시 도전하기';

    el('overlay').classList.remove('hidden');
}


// ====================================
// 실시간 타이머
// ====================================

function tick() {

    // 게임 시작 전에는 타이머가 흐르지 않음
    if (!game || game.ended) return;

    const t = now();

    const limit =
        LEVEL_TIMES[game.level-1];

    const remaining =
        limit-(t-game.levelStart)/1000;

    el('time').textContent =
        Math.max(0,Math.ceil(remaining));

    if (remaining<=0) {
        nextLevel();
        return;
    }

    let grillChanged=false;

    game.grills.forEach((g,i)=>{

        if (g.state==='empty') return;

        const elapsed=t-g.born;

        if (
            g.state==='cooking' &&
            elapsed>=COOK_MS
        ) {
            g.state='ready';
            grillChanged=true;
        }

        if (
            g.state==='ready' &&
            elapsed>=BURN_MS
        ) {
            g.state='burnt';
            game.score=Math.max(0,game.score-10);
            game.combo=0;
            updateHud();
            grillChanged=true;
        }

        const bar=el('cook-'+i);

        if (bar) {
            bar.style.width=
                Math.min(
                    100,elapsed/BURN_MS*100
                )+'%';
        }
    });

    if (grillChanged) {
        renderGrills();
    }

    let customersChanged=false;

    for (let i=0;i<game.customers.length;i++) {

        const c=game.customers[i];

        const r=
            1-(t-c.born)/c.patience;

        const bar=el('patience-'+i);

        if (bar) {
            bar.style.width=
                Math.max(0,r)*100+'%';

            bar.style.background=
                r<.3?'#e35a4d':
                r<.55?'#e9ac49':
                '#70b963';
        }

        if (r<=0) {

            game.missed++;

            game.customers[i]=newCustomer();

            customersChanged=true;

            loseLife('손님이 떠났습니다!');

            if (game.ended) return;
        }
    }

    if (customersChanged) {
        renderCustomers();
    }
}

// 처음에는 게임을 시작하지 않음
// 카운트다운 완료 후 startGame() 실행
setInterval(tick,80);

</script>
</body>
</html>
""", height=900, scrolling=False)
