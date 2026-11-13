
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="타코야끼 스피드게임",
    page_icon="🐙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.block-container {
    padding:0 !important;
    max-width:100% !important;
}
[data-testid="stAppViewContainer"] {
    background:#1e2637;
}
iframe {display:block; border:0;}
</style>
""", unsafe_allow_html=True)

components.html(r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1.0" />
<style>
*{box-sizing:border-box}
html,body{
    margin:0;width:100%;height:100%;
    font-family:'Malgun Gothic','Apple SD Gothic Neo',sans-serif;
    color:#493322;overflow:hidden
}
button{
    font:inherit;cursor:pointer;
    -webkit-tap-highlight-color:transparent
}
button:active{transform:translateY(2px) scale(.98)}
.game{
    position:relative;isolation:isolate;width:100%;
    height:900px;overflow:hidden;
    background:linear-gradient(#5578a0 0%,#a0d6dc 46%,#dfb985 100%)
}
.backdrop{
    position:absolute;inset:0;z-index:-2;
    width:100%;height:100%
}
.shade{
    position:absolute;inset:0;z-index:-1;
    background:linear-gradient(
        90deg,#3a54771f,transparent 30%,
        transparent 65%,#30486e33
    )
}
.lantern{
    position:absolute;top:51px;font-size:37px;
    filter:drop-shadow(0 7px 8px #6e391e44);
    animation:swing 3s ease-in-out infinite;
    pointer-events:none
}
.l1{left:6%}
.l2{right:6%;animation-delay:-1s}
.l3{left:17%;font-size:26px;animation-delay:-1.7s}
.l4{right:17%;font-size:26px}
@keyframes swing{
    50%{transform:rotate(7deg) translateY(4px)}
}
.hud{
    max-width:1370px;margin:auto;display:flex;
    justify-content:space-between;align-items:center;
    gap:12px;padding:13px 18px;position:relative;z-index:4
}
.logo{
    padding:8px 15px;background:#fff4d9e8;
    border:3px solid #9d4e2f;border-radius:18px;
    box-shadow:0 5px #69381d70;
    font-weight:900;font-size:20px;color:#963c25;
    white-space:nowrap
}
.hud-right{display:flex;gap:9px;align-items:center}
.hud-box{
    border:3px solid #fff5c8;background:#784d3bec;
    border-radius:16px;min-width:103px;
    padding:8px 12px;color:#fff7dd;text-align:center;
    box-shadow:0 5px 0 #56322377;
    font-weight:900;font-size:19px
}
.hud-box small{
    display:block;font-size:10px;
    letter-spacing:.05em;opacity:.95
}
.timer{
    background:#b84742;font-size:25px;min-width:110px
}
.timer.low{animation:pulse .35s infinite alternate}
@keyframes pulse{
    to{background:#fa322f;transform:scale(1.04)}
}
.sign{
    position:relative;width:max-content;
    margin:-1px auto 2px;padding:5px 40px;
    background:#873d31;color:#fff7db;
    border:4px solid #edbd71;
    border-radius:4px 4px 15px 15px;
    box-shadow:0 7px 0 #5b2f28,0 11px 17px #56342888;
    font-weight:900;font-size:22px;letter-spacing:2px;
    text-shadow:1px 2px #5a271a
}
.customers{
    display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
    gap:13px;max-width:1140px;margin:22px auto 0;
    padding:0 15px;position:relative;z-index:2;
    min-height:185px
}
.customer{
    position:relative;border:4px solid #d79554;
    border-radius:20px;background:linear-gradient(#fff6df,#fff0d1);
    box-shadow:0 9px 0 #845d3e8a,0 13px 22px #3e2c2850;
    min-height:167px;padding:13px 10px 10px;
    display:flex;flex-direction:column;align-items:center;
    gap:5px;transition:transform .12s
}
.customer:hover{
    transform:translateY(-3px);border-color:#edac4d
}
.avatar{
    position:absolute;left:11px;top:-38px;font-size:56px;
    filter:drop-shadow(0 4px 1px #ffffffa8);
    animation:bob 1.8s infinite alternate;
    pointer-events:none
}
@keyframes bob{to{transform:translateY(-5px)}}
.ordername{font-weight:900;font-size:13px;color:#a35b31}
.orderfood{font-size:34px;line-height:1.2;white-space:nowrap}
.ordertext{
    font-size:13px;font-weight:900;text-align:center;
    color:#663e2a;white-space:nowrap
}
.patience{
    height:11px;width:88%;background:#e6d0ac;
    border:2px solid #fff;border-radius:15px;
    overflow:hidden;margin-top:3px
}
.patience>span{
    display:block;height:100%;background:#64ae60;
    width:100%;transition:width .09s linear
}
.servehint{font-size:11px;color:#875e45;font-weight:800}
.counter{
    position:relative;max-width:1280px;margin:13px auto 0;
    border:9px solid #9e5732;
    border-radius:27px 27px 40px 40px;
    background:repeating-linear-gradient(
        0deg,#bf7b44 0 21px,#c8884d 22px 45px
    );
    box-shadow:0 17px 0 #653b25,0 24px 32px #4d2c2059;
    padding:14px 21px 18px;z-index:2
}
.counter:before{
    content:'';position:absolute;inset:9px;
    border:2px solid #f3cb91;border-radius:17px;
    pointer-events:none
}
.counter-caption{
    position:relative;color:#fff7d5;font-size:13px;
    letter-spacing:3px;text-align:center;font-weight:900;
    text-shadow:0 2px #7b3e23;margin-bottom:8px
}
.worktop{
    display:grid;
    grid-template-columns:minmax(0,1.7fr) minmax(245px,.8fr);
    gap:16px
}
.grill-area{
    padding:13px;background:#45434a;
    border:5px solid #292b33;border-radius:23px;
    box-shadow:inset 0 4px #686572,0 5px 0 #372e2c;
    min-width:0
}
.grills{
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:12px
}
.grill{
    position:relative;min-height:180px;
    background:linear-gradient(140deg,#262b32,#38353a);
    border:3px solid #686368;border-radius:20px;
    box-shadow:inset 0 5px 12px #17181b,0 3px 1px #222;
    display:flex;flex-direction:column;
    align-items:center;justify-content:center;
    color:#fff8dc;padding:12px 4px 8px;overflow:hidden
}
.grill:hover{border-color:#ffd47e}
.balls{
    display:grid;grid-template-columns:repeat(2,1fr);
    gap:5px;width:min(110px,90%);margin-bottom:9px
}
.ball{
    aspect-ratio:1;border-radius:50%;background:#13171c;
    border:3px solid #15191e;
    box-shadow:inset 0 3px 4px #040609;
    display:flex;align-items:center;justify-content:center;
    font-size:19px
}
.ball.cooking{
    background:radial-gradient(circle at 35% 27%,#f9dd8e,#d2a55c);
    border-color:#b48047;animation:fry .8s infinite alternate
}
.ball.ready{
    background:radial-gradient(circle at 30% 25%,#f8d37b,#a76127);
    border-color:#6d3919
}
.ball.burnt{
    background:radial-gradient(circle at 30% 25%,#735138,#291a13);
    border-color:#1b1510
}
@keyframes fry{
    to{filter:brightness(1.12);transform:scale(1.05)}
}
.grill-name{font-size:13px;font-weight:900;text-align:center}
.cookbar{
    height:8px;width:83%;margin:6px 0;
    background:#151719;border-radius:8px;overflow:hidden
}
.cookbar span{
    display:block;height:100%;width:0;background:#91dc69
}
.grill .micro{font-size:11px;color:#ffdfa0}
.plating{
    position:relative;
    background:linear-gradient(140deg,#f4d8b7,#f7eacb);
    border:5px solid #eac88e;border-radius:23px;
    text-align:center;min-height:199px;
    box-shadow:inset 0 4px #fff9ee,0 5px #815634;
    display:flex;align-items:center;
    justify-content:space-evenly;flex-direction:column;padding:8px
}
.plating b{font-size:16px;color:#935127}
.plate{
    width:118px;height:118px;
    background:radial-gradient(
        circle,#fff 0 48%,#b7d3df 50% 58%,white 61% 100%
    );
    border-radius:50%;
    box-shadow:0 6px 0 #bba482,0 8px 12px #4f393955;
    display:flex;flex-direction:column;align-items:center;
    justify-content:center;font-size:40px;margin:2px
}
.plate small{
    font-size:11px;font-weight:900;color:#7b432b;
    max-width:115px
}
.plate-note{font-size:12px;color:#8e5d3a;font-weight:800}
.supply{
    max-width:1260px;margin:22px auto 0;padding:0 12px;
    display:grid;grid-template-columns:1fr 1fr;
    gap:18px;position:relative;z-index:2
}
.supply-box{
    background:#ffefd5e8;border:4px solid #bb7a45;
    border-radius:20px;padding:11px 12px 12px;
    box-shadow:0 7px 0 #6b422d80
}
.supply-title{
    font-size:14px;font-weight:900;
    color:#8a492d;margin:0 0 8px 4px
}
.choices{display:flex;gap:8px}
.choice{
    flex:1;background:#fff9ec;border:3px solid #f3c895;
    border-radius:14px;color:#6c4127;
    min-height:64px;font-weight:900;font-size:14px;
    box-shadow:0 4px 0 #af814f;white-space:nowrap
}
.choice.active{
    border-color:#e9673e;background:#ffddb0;
    box-shadow:0 4px 0 #b6593f
}
.choice .emoji{display:block;font-size:25px;margin-bottom:1px}
.tips{
    position:relative;z-index:2;text-align:center;
    font-weight:900;font-size:13px;color:#fff5d7;
    text-shadow:0 2px 4px #4d2e29;margin:17px auto 0;
    padding:5px 16px;background:#6b3e30c9;
    width:max-content;max-width:98%;border-radius:15px
}
.toast{
    position:absolute;left:50%;bottom:118px;
    transform:translateX(-50%);
    background:#392823e8;color:#fff6dd;
    font-weight:900;border:2px solid #f6cb84;
    border-radius:13px;padding:10px 20px;z-index:8;
    text-align:center;white-space:nowrap;max-width:90%;
    font-size:15px;opacity:0;pointer-events:none;
    transition:opacity .15s
}
.toast.show{opacity:1}
.overlay{
    position:absolute;z-index:20;inset:0;
    background:#1d1826c4;display:flex;
    justify-content:center;align-items:center;padding:20px
}
.overlay.hidden{display:none}
.result{
    width:min(450px,95%);border:9px solid #f2c476;
    border-radius:28px;background:#fff3d9;
    box-shadow:0 16px 0 #5c351db8;
    padding:29px;text-align:center
}
.result h2{font-size:33px;margin:5px;color:#ab5228}
.result p{font-size:19px;font-weight:800}
.result .replay{
    border:0;border-radius:16px;background:#d85e42;
    color:white;font-size:21px;font-weight:900;
    padding:15px 35px;box-shadow:0 6px #9e3c2b
}
@media(max-width:780px){
    .logo{font-size:14px;padding:8px}
    .hud-box{min-width:60px;font-size:15px;padding:7px}
    .hud-box small{font-size:9px}
    .timer{font-size:19px;min-width:75px}
    .sign{font-size:17px;padding:7px 21px}
    .customers{gap:6px;margin-top:35px}
    .customer{min-height:157px;padding:15px 3px 7px}
    .avatar{font-size:37px;top:-27px}
    .orderfood{font-size:24px}
    .ordertext{font-size:10px;white-space:normal}
    .ordername,.servehint{font-size:10px}
    .counter{margin:15px 8px 0;padding:9px;border-width:6px}
    .worktop{
        grid-template-columns:minmax(0,1.2fr) minmax(120px,.7fr);
        gap:7px
    }
    .grill-area{padding:6px}
    .grills{gap:3px}
    .grill{min-height:155px;padding:3px}
    .balls{gap:2px}
    .ball{font-size:11px;border-width:1px}
    .grill-name{font-size:10px}
    .grill .micro{font-size:8px}
    .plating{min-height:160px;padding:3px}
    .plating b{font-size:11px}
    .plate{width:77px;height:77px;font-size:24px}
    .plate small,.plate-note{font-size:9px}
    .supply{gap:6px;margin-top:16px;padding:0 5px}
    .supply-box{padding:7px 5px;border-width:3px}
    .supply-title{font-size:11px}
    .choices{gap:3px}
    .choice{font-size:10px;min-height:55px;padding:1px}
    .choice .emoji{font-size:18px}
    .tips{font-size:10px;white-space:normal}
}
</style>
</head>
<body>
<div class="game">
<svg class="backdrop" viewBox="0 0 1200 900"
     preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop stop-color="#496ba1"/>
      <stop offset=".43" stop-color="#d69aa1"/>
      <stop offset="1" stop-color="#f6ce92"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="900" fill="url(#sky)"/>
  <circle cx="1000" cy="120" r="73" fill="#ffe7af" opacity=".8"/>
  <path d="M0 370 Q120 230 255 365 T530 360 T825 357 T1200 355
           L1200 900H0" fill="#647f92" opacity=".45"/>
  <path d="M0 440L0 210L110 210L110 395L175 395L175 145L340 145
           L340 430L445 430L445 240L535 240L535 475L670 475
           L670 190L800 190L800 400L917 400L917 180L1040 180
           L1040 430L1200 430V900H0" fill="#414e70" opacity=".63"/>
  <path d="M0 470L0 280L148 280L148 470
           M1052 470L1052 290H1200V470" fill="#695469" opacity=".9"/>
  <g fill="#f8c77d" opacity=".8">
    <rect x="28" y="320" width="28" height="36"/>
    <rect x="89" y="320" width="28" height="36"/>
    <rect x="225" y="195" width="43" height="38"/>
    <rect x="290" y="195" width="30" height="38"/>
    <rect x="940" y="238" width="39" height="45"/>
    <rect x="1081" y="335" width="36" height="38"/>
    <rect x="1145" y="335" width="36" height="38"/>
  </g>
  <path d="M0 380H1200V475H0Z" fill="#613c49"/>
  <path d="M0 355H1200V421H0Z" fill="#f7e2b5"/>
  <path d="M0 350H1200V388H0Z" fill="#a93e3c"/>
  <path d="M0 388H1200V425H0Z" fill="#f8d6a8"/>
  <g stroke="#8f403b" stroke-width="6">
    <path d="M0 387V424M110 387V424M220 387V424
             M330 387V424M440 387V424M550 387V424
             M660 387V424M770 387V424M880 387V424
             M990 387V424M1100 387V424M1200 387V424"/>
  </g>
  <path d="M0 420H1200V900H0" fill="#cc9873" opacity=".5"/>
  <g fill="#548d79" opacity=".8">
    <ellipse cx="45" cy="570" rx="75" ry="120"/>
    <ellipse cx="1160" cy="590" rx="72" ry="145"/>
    <ellipse cx="113" cy="660" rx="60" ry="80"/>
  </g>
</svg>

<div class="shade"></div>
<div class="lantern l1">🏮</div>
<div class="lantern l2">🏮</div>
<div class="lantern l3">🏮</div>
<div class="lantern l4">🏮</div>

<div class="hud">
  <div class="logo">🐙 타코야끼 대소동!</div>
  <div class="hud-right">
    <div class="hud-box timer" id="timer">
      <small>남은 시간</small>
      <span id="time">75</span>초
    </div>
    <div class="hud-box">
      <small>매출 점수</small>
      <span id="score">0</span> ⭐
    </div>
    <div class="hud-box">
      <small>연속 성공</small>
      <span id="combo">0</span> 🔥
    </div>
  </div>
</div>

<div class="sign">🏮 타코타코 포장마차 🏮</div>
<div class="customers" id="customers"></div>

<div class="counter">
  <div class="counter-caption">
    🍳 지글지글 타코야끼 조리대 🍳
  </div>
  <div class="worktop">
    <div class="grill-area">
      <div class="grills" id="grills"></div>
    </div>
    <div class="plating">
      <b>🍽️ 완성 접시</b>
      <div class="plate" id="plate"></div>
      <div class="plate-note" id="plate-note">
        익은 타코야끼를 클릭!
      </div>
    </div>
  </div>
</div>

<div class="supply">
  <div class="supply-box">
    <div class="supply-title">
      ① 속재료 선택 → 빈 조리판 클릭
    </div>
    <div class="choices" id="fillings"></div>
  </div>
  <div class="supply-box">
    <div class="supply-title">
      ② 다 익으면 집기 → 토핑 선택
    </div>
    <div class="choices" id="toppings"></div>
  </div>
</div>

<div class="tips">
  ③ 주문이 완성되면 손님 카드를 클릭해서 서빙!
  · 늦으면 주문 취소!
</div>

<div class="toast" id="toast"></div>

<div class="overlay hidden" id="overlay">
  <div class="result">
    <div style="font-size:56px">🏆</div>
    <h2>영업 종료!</h2>
    <p id="result-text"></p>
    <button class="replay" onclick="restart()">
      🔄 다시 도전하기
    </button>
  </div>
</div>

</div>

<script>
const DURATION = 75;
const COOK_MS = 2700;
const BURN_MS = 6700;

const fillings = [
    {name:'문어',emoji:'🐙'},
    {name:'치즈',emoji:'🧀'},
    {name:'새우',emoji:'🦐'}
];

const toppings = [
    {name:'소스',emoji:'🍯'},
    {name:'마요네즈',emoji:'🥛'},
    {name:'가쓰오부시',emoji:'🍥'}
];

const faces = ['🐱','🐰','🐻','🦊','🐼','🐸'];

let game;
let toastTimer;

const el = id => document.getElementById(id);
const pick = arr => arr[Math.floor(Math.random()*arr.length)];
const now = () => performance.now();

function newCustomer(){
    return {
        id:Math.random(),
        face:pick(faces),
        fill:pick(fillings),
        top:pick(toppings),
        born:now(),
        patience:15000+Math.random()*3500
    };
}

function tell(message){
    const x=el('toast');
    x.textContent=message;
    x.classList.add('show');

    clearTimeout(toastTimer);
    toastTimer=setTimeout(
        ()=>x.classList.remove('show'),1450
    );
}

function restart(){
    game={
        start:now(),
        score:0,
        combo:0,
        best:0,
        served:0,
        missed:0,
        selected:fillings[0],
        grills:[
            {state:'empty'},
            {state:'empty'},
            {state:'empty'}
        ],
        plate:null,
        customers:[
            newCustomer(),
            newCustomer(),
            newCustomer()
        ],
        ended:false
    };

    el('overlay').classList.add('hidden');
    renderAll();
}

function renderAll(){
    renderCustomers();
    renderGrills();
    renderPlate();
    renderFillings();
    renderToppings();
    updateHud();
}

function renderCustomers(){
    el('customers').innerHTML=game.customers.map((c,i)=>`
        <button class="customer" onclick="serve(${i})">
            <span class="avatar">${c.face}</span>
            <span class="ordername">손님 ${i+1} · 주문표</span>
            <span class="orderfood">
                🐙 ${c.fill.emoji} ${c.top.emoji}
            </span>
            <span class="ordertext">
                ${c.fill.name} + ${c.top.name}
            </span>
            <span class="patience">
                <span id="patience-${i}"></span>
            </span>
            <span class="servehint">👆 클릭하면 서빙!</span>
        </button>
    `).join('');
}

function renderFillings(){
    el('fillings').innerHTML=fillings.map((v,i)=>`
        <button
            class="choice ${game.selected.name===v.name?'active':''}"
            onclick="selectFilling(${i})">
            <span class="emoji">${v.emoji}</span>
            ${v.name}
        </button>
    `).join('');
}

function renderToppings(){
    el('toppings').innerHTML=toppings.map((v,i)=>`
        <button
            class="choice ${game.plate?.top?.name===v.name?'active':''}"
            onclick="addTopping(${i})">
            <span class="emoji">${v.emoji}</span>
            ${v.name}
        </button>
    `).join('');
}

function renderGrills(){
    el('grills').innerHTML=game.grills.map((g,i)=>{
        const icons={
            empty:'',
            cooking:'🥣',
            ready:g.fill?.emoji||'🐙',
            burnt:'💨'
        };

        const captions={
            empty:'빈 판 · 클릭해서 굽기',
            cooking:'굽는 중...',
            ready:'완성! 빨리 클릭',
            burnt:'탔다! 눌러서 버리기'
        };

        return `
        <button class="grill" onclick="tapGrill(${i})">
            <div class="balls">
                ${Array.from({length:6},()=>`
                    <div class="ball ${g.state}">
                        ${icons[g.state]}
                    </div>
                `).join('')}
            </div>
            <div class="grill-name">
                ${i+1}번 판 ${g.fill?.emoji||'🍳'}
            </div>
            <div class="cookbar">
                <span id="cook-${i}"></span>
            </div>
            <div class="micro">${captions[g.state]}</div>
        </button>`;
    }).join('');
}

function renderPlate(){
    if(!game.plate){
        el('plate').innerHTML='🍽️';
        el('plate-note').textContent='익은 타코야끼를 클릭!';
    }else{
        el('plate').innerHTML=`
            🐙<small>
                ${game.plate.fill.name}
                ${game.plate.top?'+ '+game.plate.top.name:''}
            </small>`;

        el('plate-note').textContent=game.plate.top
            ?'주문에 맞는 손님 클릭!'
            :'아래에서 토핑을 골라 줘!';
    }
    renderToppings();
}

function selectFilling(i){
    if(game.ended)return;
    game.selected=fillings[i];
    renderFillings();
    tell(`${game.selected.name} 선택! 빈 판을 눌러!`);
}

function tapGrill(i){
    if(game.ended)return;

    let g=game.grills[i];

    if(g.state==='empty'){
        game.grills[i]={
            state:'cooking',
            fill:game.selected,
            born:now()
        };
        tell(`${game.selected.name} 타코야끼 굽기 시작!`);

    }else if(g.state==='cooking'){
        tell('조금만 더 익혀 줘!');
        return;

    }else if(g.state==='ready'){
        if(game.plate){
            tell('접시가 꽉 찼어! 손님께 먼저 서빙해!');
            return;
        }

        game.plate={fill:g.fill,top:null};
        game.grills[i]={state:'empty'};
        tell('접시에 담았어! 토핑을 올려 줘.');
        renderPlate();

    }else{
        game.grills[i]={state:'empty'};
        tell('탄 타코야끼를 치웠어!');
    }

    renderGrills();
}

function addTopping(i){
    if(game.ended)return;

    if(!game.plate){
        tell('먼저 익은 타코야끼를 접시에 올려!');
        return;
    }

    game.plate.top=toppings[i];
    renderPlate();
    tell('토핑 완료! 맞는 손님을 클릭!');
}

function serve(i){
    if(game.ended)return;

    if(!game.plate||!game.plate.top){
        tell('타코야끼를 완성한 뒤 손님을 눌러!');
        return;
    }

    const c=game.customers[i];

    if(
        c.fill.name===game.plate.fill.name &&
        c.top.name===game.plate.top.name
    ){
        const bonus=Math.min(game.combo,5)*20;

        game.score+=100+bonus;
        game.combo++;
        game.best=Math.max(game.combo,game.best);
        game.served++;

        tell(`🎉 주문 성공! +${100+bonus}점`);
        game.customers[i]=newCustomer();

    }else{
        game.score=Math.max(0,game.score-20);
        game.combo=0;
        tell('❌ 주문과 달라! -20점');
    }

    game.plate=null;
    renderPlate();
    renderCustomers();
    updateHud();
}

function updateHud(){
    el('score').textContent=game.score;
    el('combo').textContent=game.combo;
}

function end(){
    if(game.ended)return;
    game.ended=true;
    el('time').textContent='0';

    el('result-text').innerHTML=`
        총 <b>${game.served}개</b> 완성<br>
        최종 점수 <b>${game.score}점</b><br>
        최고 콤보 <b>${game.best}</b><br>
        놓친 주문 <b>${game.missed}</b>
    `;

    el('overlay').classList.remove('hidden');
}

function tick(){
    if(!game||game.ended)return;

    const t=now();
    const left=Math.max(
        0,DURATION-(t-game.start)/1000
    );

    el('time').textContent=Math.ceil(left);
    el('timer').classList.toggle('low',left<=10);

    if(left<=0){
        end();
        return;
    }

    let grillChanged=false;

    game.grills.forEach((g,i)=>{
        if(g.state==='empty')return;

        const elapsed=t-g.born;

        if(g.state==='cooking'&&elapsed>=COOK_MS){
            g.state='ready';
            grillChanged=true;
        }

        if(g.state==='ready'&&elapsed>=BURN_MS){
            g.state='burnt';
            game.score=Math.max(0,game.score-10);
            game.combo=0;
            grillChanged=true;
            updateHud();
            tell('🔥 타코야끼가 타버렸어! -10점');
        }

        const bar=el(`cook-${i}`);

        if(bar){
            bar.style.width=
                `${Math.min(100,elapsed/BURN_MS*100)}%`;

            bar.style.background=
                g.state==='ready'?'#71d56c':
                g.state==='burnt'?'#ef665d':'#ffcc58';
        }
    });

    if(grillChanged)renderGrills();

    let customerChanged=false;

    game.customers.forEach((c,i)=>{
        const remaining=1-(t-c.born)/c.patience;
        const bar=el(`patience-${i}`);

        if(bar){
            bar.style.width=
                `${Math.max(0,remaining)*100}%`;

            bar.style.background=
                remaining<.28?'#e35248':
                remaining<.55?'#e6a942':'#65b56c';
        }

        if(remaining<=0){
            game.missed++;
            game.score=Math.max(0,game.score-15);
            game.combo=0;
            game.customers[i]=newCustomer();
            customerChanged=true;
        }
    });

    if(customerChanged){
        renderCustomers();
        updateHud();
        tell('⌛ 손님이 떠났어! -15점');
    }
}

restart();
setInterval(tick,80);
</script>
</body>
</html>
""", height=900, scrolling=False)
