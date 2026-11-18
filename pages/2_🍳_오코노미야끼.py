
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="오코노미야끼 | 와글와글 포장마차",
    page_icon="🍳",
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
    display: block;
    border: none;
}
</style>
""", unsafe_allow_html=True)

components.html(r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: 'Malgun Gothic', sans-serif;
    color: #65432d;
}

button {
    font: inherit;
    cursor: pointer;
}

.game {
    position: relative;
    min-height: 910px;
    padding: 15px;
    overflow: hidden;
    border-radius: 22px;
    background: linear-gradient(
        #587ba2 0%,
        #eba99b 43%,
        #f2d5a6 68%,
        #b77d53 100%
    );
}

.lanterns {
    position: absolute;
    top: 85px;
    left: 6%;
    right: 6%;
    display: flex;
    justify-content: space-between;
    font-size: 45px;
    pointer-events: none;
}

.header {
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    z-index: 2;
}

.logo {
    background: #fff2d5;
    border: 4px solid #a95d38;
    border-radius: 18px;
    color: #984e32;
    padding: 12px;
    font-weight: 900;
    font-size: 23px;
}

.stats {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.stat {
    background: #744a3b;
    border: 3px solid #f2d8a7;
    border-radius: 14px;
    color: white;
    padding: 9px;
    min-width: 84px;
    font-size: 20px;
    font-weight: 900;
    text-align: center;
}

.stat small {
    display: block;
    font-size: 10px;
    color: #ffe2b8;
}

.timer {
    background: #c85449;
}

.sign {
    width: fit-content;
    max-width: 100%;
    margin: 18px auto 42px;
    padding: 10px 30px;
    position: relative;
    background: #944b36;
    border: 5px solid #f0c887;
    border-radius: 15px;
    color: #fff5d8;
    font-size: 23px;
    font-weight: 900;
    text-align: center;
    box-shadow: 0 7px #663c2c;
}

.customers {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    max-width: 1080px;
    margin: 0 auto 20px;
}

.customer {
    background: #fff3da;
    border: 4px solid #d9a16a;
    border-radius: 19px;
    min-height: 155px;
    padding: 10px;
    box-shadow: 0 7px #9b6a43;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    gap: 4px;
}

.face {
    font-size: 39px;
}

.order {
    font-size: 14px;
    font-weight: 900;
}

.patience {
    width: 90%;
    height: 11px;
    background: #dfc7aa;
    border-radius: 10px;
    overflow: hidden;
}

.patience span {
    display: block;
    height: 100%;
    width: 100%;
    background: #72bc65;
}

.counter {
    max-width: 1230px;
    margin: auto;
    background: repeating-linear-gradient(
        0deg,
        #b8794c 0 25px,
        #c88854 25px 50px
    );
    border: 8px solid #925638;
    border-radius: 25px;
    padding: 15px;
    box-shadow: 0 12px #643a29;
}

.counter h3 {
    margin: 0 0 14px;
    text-align: center;
    color: #fff5d8;
    text-shadow: 0 2px #76432f;
}

.kitchen {
    display: grid;
    grid-template-columns: minmax(0, 2fr) minmax(170px, 1fr);
    gap: 14px;
}

.grills {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    padding: 12px;
    background: #49474b;
    border: 5px solid #302d32;
    border-radius: 20px;
}

.grill {
    background: #27292d;
    border: 3px solid #6c686d;
    border-radius: 18px;
    color: #fff5dc;
    min-height: 198px;
    padding: 10px 4px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    gap: 7px;
    text-align: center;
}

.food {
    width: 105px;
    height: 105px;
    border-radius: 50%;
    background: #16181c;
    border: 5px solid #17191d;
    display: grid;
    place-items: center;
    font-size: 39px;
    pointer-events: none;
}

.food.batter {
    background: #f8dfac;
    border-color: #dcbf84;
}

.food.cooking,
.food.flip {
    background: radial-gradient(
        circle at 30% 25%,
        #f4d88a,
        #b98742
    );
    border-color: #996c33;
    animation: sizzle .8s infinite alternate;
}

.food.ready {
    background: radial-gradient(
        circle at 30% 25%,
        #daba69,
        #985d2f
    );
    border-color: #76431f;
}

.food.burnt {
    background: #493326;
    border-color: #2b211b;
}

@keyframes sizzle {
    to {
        filter: brightness(1.15);
        transform: scale(1.04);
    }
}

.grill strong {
    font-size: 13px;
    pointer-events: none;
}

.grill small {
    font-size: 10px;
    pointer-events: none;
}

.bar {
    width: 85%;
    height: 9px;
    background: #18181b;
    border-radius: 10px;
    overflow: hidden;
    pointer-events: none;
}

.bar span {
    display: block;
    height: 100%;
    width: 0;
    background: #ffcd5e;
}

.right {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.plate-zone,
.trash {
    background: #fff1d8;
    border: 5px solid #e3bd91;
    border-radius: 19px;
    min-height: 80px;
    padding: 12px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 8px;
}

.plate-zone {
    min-height: 185px;
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
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 38px;
}

.plate small {
    font-size: 11px;
    font-weight: 900;
}

.trash {
    background: #f6d0bc;
    font-weight: 900;
}

.supplies {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
    margin: 24px auto 12px;
    max-width: 1230px;
}

.supply {
    background: #fff1dc;
    border: 4px solid #c18554;
    border-radius: 19px;
    padding: 12px;
}

.supply h3 {
    font-size: 15px;
    margin: 0 0 10px;
}

.items {
    display: flex;
    gap: 7px;
}

.item {
    flex: 1;
    min-width: 0;
    padding: 10px 3px;
    background: #fffbf1;
    border: 3px solid #e9ca9f;
    border-radius: 13px;
    text-align: center;
    font-size: 13px;
    font-weight: 900;
}

.item span {
    display: block;
    font-size: 26px;
}

[data-source] {
    cursor: grab;
    touch-action: none;
    user-select: none;
}

[data-source]:active {
    cursor: grabbing;
}

.drop-over {
    outline: 5px solid #ffe276;
    outline-offset: 2px;
    filter: brightness(1.12);
}

.dragging-original {
    opacity: .45;
}

.ghost {
    position: fixed;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 100;
    background: #fff5dc;
    border: 3px solid #dda46c;
    border-radius: 15px;
    padding: 11px;
    text-align: center;
    font-size: 29px;
}

.ghost small {
    display: block;
    font-size: 11px;
}

.help {
    margin: 15px auto;
    padding: 10px;
    max-width: 1230px;
    background: #744b37;
    color: white;
    border-radius: 15px;
    font-size: 13px;
    font-weight: 900;
    text-align: center;
}

.toast {
    position: absolute;
    z-index: 15;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    max-width: 90%;
    background: #463126;
    color: white;
    border-radius: 14px;
    padding: 12px 20px;
    text-align: center;
    font-weight: 900;
    opacity: 0;
    pointer-events: none;
}

.toast.show {
    opacity: 1;
}

.overlay {
    position: absolute;
    z-index: 30;
    inset: 0;
    background: #291d30c2;
    display: grid;
    place-items: center;
    padding: 15px;
}

.overlay.hidden {
    display: none;
}

.panel {
    background: #fff1d3;
    border: 8px solid #e7b476;
    border-radius: 28px;
    padding: 30px;
    text-align: center;
    width: min(500px, 95%);
    box-shadow: 0 15px #6c4330;
}

.panel h1 {
    color: #a34f31;
    font-size: 32px;
}

.panel p {
    font-weight: 900;
    line-height: 1.8;
}

.start {
    background: #e4774d;
    color: white;
    border: none;
    padding: 16px 28px;
    border-radius: 17px;
    font-size: 21px;
    font-weight: 900;
    box-shadow: 0 6px #aa4c30;
}

.countdown {
    position: absolute;
    z-index: 40;
    inset: 0;
    display: none;
    align-items: center;
    justify-content: center;
    background: #2d202aca;
    color: #fff0b8;
    font-size: clamp(75px, 15vw, 150px);
    font-weight: 900;
}

.countdown.show {
    display: flex;
}

@media(max-width:800px) {
    .game {
        padding: 7px;
    }

    .logo {
        font-size: 13px;
        padding: 7px;
    }

    .stat {
        min-width: 48px;
        padding: 5px;
        font-size: 12px;
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
        min-height: 135px;
        padding: 5px 2px;
    }

    .face {
        font-size: 26px;
    }

    .order {
        font-size: 10px;
    }

    .kitchen {
        grid-template-columns:
            minmax(0, 1.7fr)
            minmax(95px, .7fr);
        gap: 5px;
    }

    .counter {
        padding: 7px;
    }

    .grills {
        gap: 3px;
        padding: 4px;
    }

    .grill {
        min-height: 145px;
        padding: 4px 1px;
    }

    .food {
        width: 48px;
        height: 48px;
        font-size: 20px;
    }

    .grill strong,
    .grill small {
        font-size: 9px;
    }

    .plate {
        width: 75px;
        height: 75px;
        font-size: 25px;
    }

    .supply {
        padding: 6px;
    }

    .supply h3 {
        font-size: 11px;
    }

    .item {
        font-size: 10px;
        padding: 6px 2px;
    }

    .item span {
        font-size: 20px;
    }
}
</style>
</head>

<body>

<div class="game">

<div class="lanterns">
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
    🍳 오코노미야끼 가게 🍳
</div>

<div class="customers" id="customers"></div>

<div class="counter">

    <h3>🔥 오코노미야끼 철판 조리대</h3>

    <div class="kitchen">

        <div class="grills" id="grills"></div>

        <div class="right">

            <div class="plate-zone" data-drop="plate">
                <strong>🍽️ 완성 접시</strong>
                <div class="plate" id="plate">
                    🍽️
                </div>
                <small id="plate-help">
                    완성된 음식을 옮겨 주세요
                </small>
            </div>

            <div class="trash" data-drop="trash">
                🗑️ 휴지통
            </div>

        </div>

    </div>

</div>

<div class="supplies">

    <div class="supply">
        <h3>① 반죽과 재료를 철판에 드래그</h3>
        <div class="items" id="ingredients"></div>
    </div>

    <div class="supply">
        <h3>② 뒤집개 · ③ 토핑</h3>
        <div class="items" id="tools"></div>
    </div>

</div>

<div class="help">
    반죽 → 재료 → 굽기 → 뒤집기 → 접시
    → 토핑 → 손님에게 서빙
</div>

<div class="toast" id="toast"></div>

<div class="overlay" id="overlay">

    <div class="panel">

        <div id="panel-icon"
             style="font-size:58px">🍳</div>

        <h1 id="panel-title">
            오코노미야끼 만들기
        </h1>

        <p id="panel-text">
            손님의 주문대로 오코노미야끼를
            만들어 주세요!<br>
            ❤️ 목숨 3개 · 총 5레벨<br>
            5레벨까지 살아남으면 승리합니다!
        </p>

        <button class="start"
                id="start-button"
                onclick="beginCountdown()">
            🎮 오코노미야끼 만들기
        </button>

    </div>

</div>

<div class="countdown" id="countdown">
    <span id="count-text">3</span>
</div>

</div>

<script>

// 레벨별 제한 시간
const LEVEL_TIMES = [90,120,120,150,150];

// 레벨별 손님 대기 시간
const CUSTOMER_WAIT = [
    [40,45],
    [30,35],
    [22,27],
    [15,20],
    [10,13]
];

// 굽기 및 뒤집기 시간
const FIRST_COOK_MS = 2200;
const SECOND_COOK_MS = 2000;
const BURN_WAIT_MS = 4200;

const ingredients = [
    {name:'반죽',emoji:'🥣',type:'batter'},
    {name:'돼지고기',emoji:'🥩',type:'filling'},
    {name:'해산물',emoji:'🦐',type:'filling'},
    {name:'치즈',emoji:'🧀',type:'filling'}
];

const tools = [
    {name:'뒤집개',emoji:'🍴',type:'flip'},
    {name:'소스',emoji:'🍯',type:'topping'},
    {name:'마요네즈',emoji:'🥛',type:'topping'}
];

const fillings = ingredients.filter(
    x => x.type==='filling'
);

const toppings = tools.filter(
    x => x.type==='topping'
);

const faces = ['🐱','🐰','🐻','🦊','🐼','🐸'];

const el = id => document.getElementById(id);
const now = () => performance.now();
const pick = arr =>
    arr[Math.floor(Math.random()*arr.length)];

let game = null;
let drag = null;
let highlighted = null;
let toastTimer = null;
let countdownActive = false;


// =====================================
// 시작 카운트다운
// =====================================

async function beginCountdown() {

    if (countdownActive) return;

    countdownActive = true;

    el('overlay').classList.add('hidden');
    el('countdown').classList.add('show');

    for (const n of ['3','2','1']) {

        el('count-text').textContent = n;

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

    startGame();
}


// =====================================
// 게임 초기화
// =====================================

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
        grills: [
            {state:'empty'},
            {state:'empty'},
            {state:'empty'}
        ],
        plate: null,
        customers: [],
        ended: false
    };

    game.customers = [
        newCustomer(),
        newCustomer(),
        newCustomer()
    ];

    renderAll();

    tell('영업 시작! 주문을 확인하세요!');
}


// =====================================
// 손님 생성
// =====================================

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


// =====================================
// 알림
// =====================================

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


// =====================================
// 화면 표시
// =====================================

function renderAll() {
    renderCustomers();
    renderGrills();
    renderPlate();
    renderItems();
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
                ${c.fill.emoji} +
                ${c.top.emoji}
            </div>

            <div class="order">
                ${c.fill.name} +
                ${c.top.name}
            </div>

            <div class="patience">
                <span id="patience-${i}"></span>
            </div>

        </div>
        `).join('');
}

function renderGrills() {

    const messages = {
        empty:'반죽을 올려 주세요',
        batter:'재료를 넣어 주세요',
        cooking:'첫 번째 면 굽는 중',
        flip:'뒤집개로 뒤집으세요!',
        second:'반대쪽 굽는 중',
        ready:'접시로 옮기세요!',
        burnt:'휴지통으로 버리세요'
    };

    el('grills').innerHTML =
        game.grills.map((g,i)=>{

            const movable =
                g.state==='ready' ||
                g.state==='burnt';

            const icon =
                g.state==='empty'?'🍳':
                g.state==='batter'?'🥣':
                g.state==='burnt'?'💨':
                g.state==='ready'?'🍘':
                g.fill?.emoji || '🍘';

            const source = movable
                ? `data-source="grill"
                   data-index="${i}"
                   data-emoji="${icon}"
                   data-label="오코노미야끼"`
                : '';

            return `

            <div class="grill"
                 data-drop="grill"
                 data-index="${i}"
                 ${source}>

                <div class="food ${g.state}">
                    ${icon}
                </div>

                <strong>${i+1}번 철판</strong>

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
            '완성된 음식을 옮겨 주세요';

    } else {

        plate.innerHTML = `
            🍘
            <small>
                ${game.plate.fill.name}
                ${game.plate.top
                    ?' + '+game.plate.top.name
                    :''}
            </small>
        `;

        plate.setAttribute('data-source','plate');
        plate.setAttribute('data-emoji','🍘');
        plate.setAttribute('data-label','완성 접시');

        el('plate-help').textContent =
            game.plate.top
                ?'손님에게 서빙하세요'
                :'토핑을 올려 주세요';
    }
}

function renderItems() {

    el('ingredients').innerHTML =
        ingredients.map((v,i)=>`

        <div class="item"
             data-source="ingredient"
             data-index="${i}"
             data-emoji="${v.emoji}"
             data-label="${v.name}">

            <span>${v.emoji}</span>
            ${v.name}

        </div>
        `).join('');

    el('tools').innerHTML =
        tools.map((v,i)=>`

        <div class="item"
             data-source="tool"
             data-index="${i}"
             data-emoji="${v.emoji}"
             data-label="${v.name}">

            <span>${v.emoji}</span>
            ${v.name}

        </div>
        `).join('');
}


// =====================================
// 드래그 앤 드롭 조리
// =====================================

function handleDrop(kind,index,target,targetIndex) {

    if (!game || game.ended) return;

    // 반죽 또는 재료를 철판에 넣기
    if (kind==='ingredient' && target==='grill') {

        const ingredient = ingredients[index];
        const g = game.grills[targetIndex];

        if (
            ingredient.type==='batter' &&
            g.state==='empty'
        ) {
            game.grills[targetIndex] = {
                state:'batter'
            };

            renderGrills();
            tell('반죽 완료! 재료를 올려 주세요.');
            return;
        }

        if (
            ingredient.type==='filling' &&
            g.state==='batter'
        ) {
            game.grills[targetIndex] = {
                state:'cooking',
                fill:ingredient,
                since:now()
            };

            renderGrills();
            tell('첫 번째 면을 굽고 있어요!');
            return;
        }

        tell('조리 순서를 확인해 주세요!');
        return;
    }

    // 뒤집개로 뒤집기
    if (kind==='tool' && target==='grill') {

        const tool = tools[index];
        const g = game.grills[targetIndex];

        if (tool.type!=='flip') {
            tell('뒤집개를 사용해 주세요!');
            return;
        }

        if (g.state==='flip') {

            g.state='second';
            g.since=now();

            renderGrills();
            tell('뒤집기 성공! 반대쪽을 굽습니다.');

        } else {
            tell('뒤집을 타이밍이 아니에요!');
        }

        return;
    }

    // 익은 음식을 접시에 옮기기
    if (kind==='grill' && target==='plate') {

        const g = game.grills[index];

        if (g.state!=='ready') {
            tell('익은 음식만 접시에 담을 수 있어요!');
            return;
        }

        if (game.plate) {
            tell('접시가 이미 차 있어요!');
            return;
        }

        game.plate = {
            fill:g.fill,
            top:null
        };

        game.grills[index] = {
            state:'empty'
        };

        renderGrills();
        renderPlate();

        tell('접시에 담았어요! 토핑을 올려 주세요.');
        return;
    }

    // 토핑 추가
    if (kind==='tool' && target==='plate') {

        const tool = tools[index];

        if (tool.type!=='topping') {
            tell('토핑을 선택해 주세요!');
            return;
        }

        if (!game.plate) {
            tell('먼저 음식을 접시에 담아 주세요!');
            return;
        }

        game.plate.top=tool;

        renderPlate();
        tell('토핑 완료! 손님에게 서빙하세요!');
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

            game.score+=points;
            game.combo++;
            game.best=Math.max(game.best,game.combo);
            game.served++;

            game.customers[targetIndex]=newCustomer();

            tell(`주문 성공! +${points}점`);

        } else {
            loseLife('잘못된 음식을 서빙했어요!');
        }

        game.plate=null;

        if (!game.ended) {
            renderPlate();
            renderCustomers();
            updateHud();
        }

        return;
    }

    // 휴지통
    if (target==='trash') {

        if (kind==='plate') {

            game.plate=null;

            renderPlate();
            tell('음식을 버렸어요!');
            return;
        }

        if (kind==='grill') {

            game.grills[index]={
                state:'empty'
            };

            renderGrills();
            tell('음식을 휴지통에 버렸어요!');
            return;
        }
    }

    tell('여기에는 놓을 수 없어요!');
}


// =====================================
// 마우스 및 터치 드래그
// =====================================

function moveGhost(e) {

    if (!drag) return;

    drag.ghost.style.left=e.clientX+'px';
    drag.ghost.style.top=e.clientY+'px';

    const target=document.elementFromPoint(
        e.clientX,e.clientY
    )?.closest('[data-drop]');

    if (highlighted) {
        highlighted.classList.remove('drop-over');
    }

    highlighted=target;

    if (target) {
        target.classList.add('drop-over');
    }
}

document.addEventListener('pointerdown',e=>{

    if (!game || game.ended || drag) return;

    const source=e.target.closest('[data-source]');

    if (!source) return;

    e.preventDefault();

    const ghost=document.createElement('div');

    ghost.className='ghost';

    ghost.innerHTML=`
        ${source.dataset.emoji}
        <small>${source.dataset.label}</small>
    `;

    document.body.appendChild(ghost);

    drag={
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

function releaseDrag(e,cancel=false) {

    if (!drag || drag.pointerId!==e.pointerId) return;

    const current=drag;

    const target=cancel
        ?null
        :document.elementFromPoint(
            e.clientX,e.clientY
        )?.closest('[data-drop]');

    current.ghost.remove();

    if (current.source.isConnected) {
        current.source.classList.remove(
            'dragging-original'
        );
    }

    if (highlighted) {
        highlighted.classList.remove('drop-over');
    }

    highlighted=null;
    drag=null;

    if (target) {
        handleDrop(
            current.kind,
            current.index,
            target.dataset.drop,
            Number(target.dataset.index||0)
        );
    }
}

document.addEventListener(
    'pointerup',
    e=>releaseDrag(e)
);

document.addEventListener(
    'pointercancel',
    e=>releaseDrag(e,true)
);


// =====================================
// 목숨 및 레벨
// =====================================

function loseLife(message) {

    if (game.ended) return;

    game.lives--;
    game.combo=0;

    updateHud();

    if (game.lives<=0) {
        endGame(false);
    } else {
        tell(`${message} 남은 목숨 ${game.lives}개`);
    }
}

function nextLevel() {

    if (game.level===5) {
        endGame(true);
        return;
    }

    game.level++;
    game.levelStart=now();

    game.grills=[
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


// =====================================
// 결과 화면
// =====================================

function endGame(won) {

    if (game.ended) return;

    game.ended=true;

    el('panel-icon').textContent=
        won?'🏆':'💔';

    el('panel-title').textContent=
        won?'최종 승리!':'게임 오버!';

    el('panel-text').innerHTML=`
        도달 레벨: ${game.level}/5<br>
        완성한 주문: ${game.served}개<br>
        최종 점수: ${game.score}점<br>
        최고 콤보: ${game.best}회<br>
        놓친 주문: ${game.missed}개
    `;

    el('start-button').textContent='🔄 다시 도전하기';

    el('overlay').classList.remove('hidden');
}


// =====================================
// 실시간 게임 진행
// =====================================

function tick() {

    if (!game || game.ended) return;

    const t=now();
    const limit=LEVEL_TIMES[game.level-1];

    const remaining=
        limit-(t-game.levelStart)/1000;

    el('time').textContent=
        Math.max(0,Math.ceil(remaining));

    if (remaining<=0) {
        nextLevel();
        return;
    }

    let grillChanged=false;

    game.grills.forEach((g,i)=>{

        if (
            g.state==='empty' ||
            g.state==='batter'
        ) return;

        const passed=t-g.since;

        if (
            g.state==='cooking' &&
            passed>=FIRST_COOK_MS
        ) {
            g.state='flip';
            g.since=t;
            grillChanged=true;
        }

        if (
            g.state==='second' &&
            passed>=SECOND_COOK_MS
        ) {
            g.state='ready';
            g.since=t;
            grillChanged=true;
        }

        if (
            (g.state==='flip' ||
             g.state==='ready') &&
            passed>=BURN_WAIT_MS
        ) {
            g.state='burnt';

            game.score=Math.max(0,game.score-10);
            game.combo=0;

            updateHud();
            grillChanged=true;

            tell('🔥 오코노미야끼가 탔어요! -10점');
        }

        const bar=el('cook-'+i);

        if (bar) {

            if (g.state==='flip' || g.state==='ready') {
                bar.style.width='100%';
                bar.style.background='#70ce65';
            } else {
                const duration=
                    g.state==='cooking'
                        ?FIRST_COOK_MS
                        :SECOND_COOK_MS;

                bar.style.width=
                    Math.min(100,passed/duration*100)+'%';
                bar.style.background='#f7c75d';
            }
        }
    });

    if (grillChanged) {
        renderGrills();
    }

    let customerChanged=false;

    for (let i=0;i<game.customers.length;i++) {

        const c=game.customers[i];

        const r=1-(t-c.born)/c.patience;

        const bar=el('patience-'+i);

        if (bar) {
            bar.style.width=Math.max(0,r)*100+'%';

            bar.style.background=
                r<.3?'#e45c4e':
                r<.55?'#e9ad48':
                '#72bc65';
        }

        if (r<=0) {

            game.missed++;

            game.customers[i]=newCustomer();
            customerChanged=true;

            loseLife('손님이 기다리다 떠났어요!');

            if (game.ended) return;
        }
    }

    if (customerChanged) {
        renderCustomers();
    }
}

// 페이지 진입 시에는 게임이 시작되지 않음
// 만들기 버튼의 카운트다운이 끝난 후 시작
setInterval(tick,80);

</script>
</body>
</html>
""", height=940, scrolling=False)
