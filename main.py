
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="타코야끼 대소동",
    page_icon="🐙",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu,footer,header{visibility:hidden}
.block-container{max-width:100%!important;padding:0!important}
[data-testid="stAppViewContainer"]{background:#25334b}
iframe{display:block;border:0}
</style>
""", unsafe_allow_html=True)

components.html(r"""
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
html,body{margin:0;height:100%;font-family:'Malgun Gothic','Apple SD Gothic Neo',sans-serif;color:#583a28}
button{font:inherit;cursor:pointer}
.game{position:relative;isolation:isolate;min-height:900px;padding:10px 12px 26px;overflow:hidden;background:linear-gradient(#536fa1 0%,#edb69e 47%,#eec995 80%)}
.skyline{position:absolute;inset:0;width:100%;height:100%;z-index:-2}
.game:before{content:"";position:absolute;inset:35% 0 0;z-index:-1;background:linear-gradient(#4b252f0a,#51322655)}
.lanterns{position:absolute;left:0;right:0;top:90px;display:flex;justify-content:space-between;padding:0 7%;font-size:39px;pointer-events:none;z-index:0;filter:drop-shadow(1px 5px 4px #30201877)}
.hud{position:relative;z-index:2;display:flex;justify-content:space-between;align-items:center;gap:10px;max-width:1320px;margin:auto}
.logo{font-size:23px;font-weight:900;background:#fff5d8;border:4px solid #a85935;border-radius:18px;padding:9px 17px;box-shadow:0 5px #61372277;color:#a34524;white-space:nowrap}
.hud-items{display:flex;gap:7px}
.stat{border:3px solid #fff2c6;background:#6e4638ed;color:#fff9e8;border-radius:15px;padding:6px 11px;min-width:85px;text-align:center;font-size:20px;font-weight:900;box-shadow:0 5px #4c332d77}
.stat small{display:block;font-size:10px;font-weight:700;color:#ffebc0}
.stat.timer{background:#b64b43;min-width:95px}
.stat.timer.urgent{animation:alert .45s infinite alternate}
@keyframes alert{to{background:#ed352e;transform:scale(1.04)}}
.hearts{font-size:19px;white-space:nowrap}
.sign{position:relative;z-index:1;width:max-content;margin:8px auto 35px;padding:6px 25px;border-radius:5px 5px 15px 15px;border:4px solid #efbf7f;color:#fff5d4;background:#944633;font-size:22px;font-weight:900;box-shadow:0 7px #653121aa;text-align:center}
.customers{position:relative;z-index:2;max-width:1120px;margin:0 auto;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:15px}
.customer{position:relative;min-height:152px;padding:13px 8px 10px;background:#fff1d5;border:4px solid #dea262;border-radius:20px;box-shadow:0 7px #8151338c;display:flex;flex-direction:column;align-items:center;justify-content:space-around;gap:5px;text-align:center;transition:border .12s,transform .12s}
.customer .face{position:absolute;left:15px;top:-35px;font-size:51px;filter:drop-shadow(0 3px 1px #ffefcd)}
.customer strong{color:#a65534;font-size:12px}
.order{font-size:26px;font-weight:900;white-space:nowrap}
.order-desc{font-size:12px;font-weight:900}
.patience{height:10px;width:90%;border-radius:12px;background:#e6d4b4;overflow:hidden}
.patience span{display:block;height:100%;width:100%;background:#6aae55}
.customer small{color:#916347;font-size:11px;font-weight:900}
.counter{position:relative;max-width:1240px;margin:21px auto 0;padding:14px 18px 18px;border:9px solid #9a5736;border-radius:27px 27px 35px 35px;background:repeating-linear-gradient(0deg,#bb7a48 0 24px,#c98752 24px 49px);box-shadow:0 14px #663b2b,0 25px 30px #39232066}
.counter-title{font-size:15px;letter-spacing:2px;font-weight:900;text-align:center;color:#ffefc7;text-shadow:0 2px #754223;margin-bottom:12px}
.station-row{display:grid;grid-template-columns:minmax(0,1.8fr) minmax(220px,.75fr);gap:14px}
.grills{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;padding:13px;background:#49464b;border:5px solid #2f3137;border-radius:20px;box-shadow:inset 0 3px #747075}
.grill{min-height:180px;display:flex;flex-direction:column;align-items:center;justify-content:space-evenly;background:linear-gradient(140deg,#28292e,#393539);color:#f7e9c6;border:3px solid #686068;border-radius:18px;padding:8px 4px;box-shadow:inset 0 4px 12px #17181c}
.grill label{font-size:12px;font-weight:900;pointer-events:none}
.holes{width:min(113px,95%);display:grid;grid-template-columns:repeat(2,1fr);gap:5px;pointer-events:none}
.ball{aspect-ratio:1;background:#15171b;border:3px solid #17191a;border-radius:50%;display:grid;place-items:center;box-shadow:inset 0 2px 3px #0008;font-size:19px}
.ball.cooking{background:radial-gradient(circle at 27% 20%,#fff0aa,#d9a75a);border-color:#bc844b;animation:bubble .7s infinite alternate}
.ball.ready{background:radial-gradient(circle at 30% 25%,#f2d27b,#b06a2d);border-color:#79451f}
.ball.burnt{background:radial-gradient(circle at 30% 25%,#73543f,#291d18);border-color:#231812}
@keyframes bubble{to{filter:brightness(1.13);transform:scale(1.045)}}
.cookbar{width:86%;height:8px;background:#19181a;border-radius:6px;overflow:hidden;pointer-events:none}
.cookbar span{display:block;width:0;height:100%;background:#f7cc59}
.grill small{font-size:10px;color:#ffdfab;pointer-events:none}
.right-station{display:flex;flex-direction:column;gap:11px}
.plate-zone,.trash-zone{background:#f7e5c6;border:5px solid #eed1a0;border-radius:19px;text-align:center;box-shadow:inset 0 3px #fff7e3,0 4px #855b39;padding:8px;display:flex;flex-direction:column;align-items:center;justify-content:space-around;gap:4px}
.plate-zone{min-height:170px}
.plate-zone strong,.trash-zone strong{font-size:14px;color:#95502f}
.plate{width:105px;height:105px;border-radius:50%;background:radial-gradient(circle,#fff 0 45%,#b6d8e7 47% 59%,#fff 62%);box-shadow:0 5px #a99574;display:flex;align-items:center;justify-content:center;flex-direction:column;font-size:33px}
.plate span{font-size:11px;font-weight:900;color:#72462d}
.plate-zone small{font-size:11px;color:#895c3f}
.trash-zone{min-height:58px;flex-direction:row;background:#f7d1bb;border-color:#d7a083}
.trash-zone .trashicon{font-size:28px}
.supplies{position:relative;z-index:2;max-width:1240px;margin:25px auto 0;display:grid;grid-template-columns:1fr 1fr;gap:15px}
.supply{padding:10px 13px 14px;border:4px solid #c28350;border-radius:19px;background:#fff1d9ed;box-shadow:0 6px #71482e77}
.supply-title{font-size:14px;font-weight:900;margin-bottom:9px;color:#965134}
.items{display:flex;gap:8px}
.item{flex:1;min-width:0;min-height:68px;background:#fffdf5;border:3px solid #f0cf9d;border-radius:13px;box-shadow:0 4px #b59064;font-size:14px;font-weight:900;color:#75452d;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px}
.item .emoji{font-size:27px}
.help{text-align:center;color:#fff9d7;background:#674534d9;border-radius:17px;max-width:max-content;margin:18px auto 0;padding:8px 18px;font-size:13px;font-weight:900;text-shadow:0 1px #372922}
[data-source]{touch-action:none;cursor:grab;user-select:none;-webkit-user-select:none}
[data-source]:active{cursor:grabbing}
.dragging-original{opacity:.48}
.drop-over{outline:5px solid #ffe377!important;outline-offset:1px;transform:scale(1.025);filter:brightness(1.09)}
.drag-ghost{position:fixed;z-index:1000;pointer-events:none;transform:translate(-50%,-50%);background:#fff9e2eb;border:4px solid #eca65e;border-radius:20px;box-shadow:0 8px 22px #352a2255;min-width:72px;min-height:72px;padding:7px 10px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:31px}
.drag-ghost small{font-size:11px;font-weight:900;color:#74402b}
.toast{position:absolute;z-index:15;bottom:95px;left:50%;transform:translateX(-50%);max-width:90%;background:#3f3029ed;color:#fff8dd;border:2px solid #f8c879;border-radius:14px;padding:11px 20px;box-shadow:0 5px 14px #0004;font-size:15px;font-weight:900;text-align:center;opacity:0;pointer-events:none;transition:opacity .15s}
.toast.show{opacity:1}
.overlay{position:absolute;inset:0;z-index:30;display:grid;place-items:center;background:#1c1527cf;padding:20px}
.overlay.hidden{display:none}
.result{background:#fff2d7;border:8px solid #ecc07b;border-radius:27px;width:min(450px,95%);padding:26px;text-align:center;box-shadow:0 14px #5f3b2dc0}
.result h2{color:#a84d2a;font-size:31px;margin:6px}
.result p{font-weight:900;line-height:1.9}
.replay{padding:13px 30px;background:#d96242;color:white;border:0;border-radius:14px;box-shadow:0 5px #a3402a;font-size:19px;font-weight:900}
@media(max-width:800px){
.game{min-height:900px;padding:7px 5px}
.logo{font-size:13px;padding:7px 5px;border-width:2px}
.hud{gap:3px}.hud-items{gap:3px}
.stat{min-width:46px;font-size:12px;padding:5px 3px;border-width:2px}
.stat small{font-size:8px}.stat.timer{min-width:58px;font-size:16px}
.hearts{font-size:12px}.sign{font-size:17px;margin-bottom:33px}
.customers{gap:5px;padding:0 4px}
.customer{padding:11px 2px 5px;min-height:140px;border-width:3px}
.customer .face{font-size:34px;top:-24px;left:5px}
.order{font-size:20px}.order-desc{font-size:10px;white-space:normal}
.customer small,.customer strong{font-size:9px}
.counter{padding:8px 5px;border-width:6px;margin-top:15px}
.counter-title{font-size:11px}.station-row{grid-template-columns:minmax(0,1.6fr) minmax(95px,.65fr);gap:5px}
.grills{gap:3px;padding:5px;border-width:3px}.grill{min-height:135px;padding:3px 1px;border-width:2px}
.holes{gap:2px}.ball{font-size:11px;border-width:1px}
.grill label{font-size:9px}.grill small{font-size:8px}
.plate-zone{min-height:126px}.plate-zone strong,.trash-zone strong{font-size:10px}
.plate{width:70px;height:70px;font-size:20px}.plate span,.plate-zone small{font-size:8px}
.trash-zone{min-height:45px}.trash-zone .trashicon{font-size:21px}
.supplies{gap:5px;margin-top:16px}.supply{padding:7px 4px;border-width:3px}
.supply-title{font-size:10px}.items{gap:3px}.item{min-height:56px;font-size:9px;padding:2px}
.item .emoji{font-size:20px}.help{font-size:10px;margin-top:14px}
}
</style>
</head>
<body>
<div class="game">
<svg class="skyline" viewBox="0 0 1200 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<path fill="#506d9e" d="M0 0h1200v900H0z"/>
<circle cx="1020" cy="125" r="79" fill="#f9dfb4"/>
<path fill="#ac8293" d="M0 350q130-180 270 0t320 0t330 0t280 0v550H0Z"/>
<path fill="#6d617d" d="M0 360V205h100v180h90V140h150v280h95V255h103v185h145V175h120v235h112V205h140v210h145V900H0Z"/>
<g fill="#f7d9a7"><path d="M27 262h34v42H27zM230 190h41v39h-41zM290 190h31v39h-31zM721 222h40v41h-40zM966 250h40v45h-40zM1091 255h36v42h-36z"/></g>
<path fill="#703e4c" d="M0 400h1200v180H0z"/>
<path fill="#a94b42" d="M0 360h1200v45H0z"/>
<path fill="#f3d6a9" d="M0 405h1200v80H0z"/>
<g stroke="#a94b42" stroke-width="7"><path d="M100 404v81M240 404v81M380 404v81M520 404v81M660 404v81M800 404v81M940 404v81M1080 404v81"/></g>
<path fill="#d2a07f" d="M0 485h1200v415H0z"/>
<g fill="#729780"><ellipse cx="35" cy="620" rx="64" ry="135"/><ellipse cx="1175" cy="635" rx="62" ry="135"/></g>
</svg>
<div class="lanterns"><span>🏮</span><span>🏮</span></div>

<header class="hud">
  <div class="logo">🐙 타코야끼 대소동!</div>
  <div class="hud-items">
    <div class="stat"><small>레벨</small>LV.<span id="level">1</span>/5</div>
    <div class="stat timer" id="timer"><small>남은 시간</small><span id="time">90</span>초</div>
    <div class="stat"><small>목숨</small><span class="hearts" id="lives">❤️❤️❤️</span></div>
    <div class="stat"><small>점수</small><span id="score">0</span>⭐</div>
    <div class="stat"><small>콤보</small><span id="combo">0</span>🔥</div>
  </div>
</header>

<div class="sign">🏮 타코타코 포장마차 🏮</div>
<section class="customers" id="customers"></section>

<section class="counter">
  <div class="counter-title">🍳 지글지글 타코야끼 조리대 🍳</div>
  <div class="station-row">
    <div class="grills" id="grills"></div>
    <div class="right-station">
      <div class="plate-zone" data-drop="plate">
        <strong>🍽️ 완성 접시</strong>
        <div class="plate" id="plate"></div>
        <small id="plate-help">익은 타코야끼를 끌어와!</small>
      </div>
      <div class="trash-zone" data-drop="trash">
        <span class="trashicon">🗑️</span><strong>휴지통 · 끌어서 버리기</strong>
      </div>
    </div>
  </div>
</section>

<section class="supplies">
  <div class="supply">
    <div class="supply-title">① 속재료를 조리판으로 드래그</div>
    <div class="items" id="fillings"></div>
  </div>
  <div class="supply">
    <div class="supply-title">③ 토핑을 접시로 드래그</div>
    <div class="items" id="toppings"></div>
  </div>
</section>

<div class="help">
  ② 다 익은 타코야끼 → 접시 &nbsp;
  ④ 완성 접시 → 손님 &nbsp;
  🗑️ 탄 음식/실수한 음식 → 휴지통
</div>

<div class="toast" id="toast"></div>
<div class="overlay hidden" id="overlay">
  <div class="result">
    <div id="result-icon" style="font-size:55px">🏆</div>
    <h2 id="result-title">게임 종료</h2>
    <p id="result-text"></p>
    <button class="replay" onclick="restart()">🔄 다시 도전하기</button>
  </div>
</div>
</div>

<script>
const LEVEL_TIMES=[90,120,120,150,150];
const COOK_MS=2700, BURN_MS=6700;

const fillings=[
  {name:'문어',emoji:'🐙'},
  {name:'치즈',emoji:'🧀'},
  {name:'새우',emoji:'🦐'}
];

const toppings=[
  {name:'소스',emoji:'🍯'},
  {name:'마요네즈',emoji:'🥛'},
  {name:'가쓰오부시',emoji:'🍥'}
];

const faces=['🐱','🐰','🐻','🦊','🐼','🐸'];

const el=id=>document.getElementById(id);
const now=()=>performance.now();
const pick=arr=>arr[Math.floor(Math.random()*arr.length)];

let game, drag=null, highlighted=null, toastTimer;

function newCustomer(){
  return {
    face:pick(faces),
    fill:pick(fillings),
    top:pick(toppings),
    born:now(),
    patience:15000+Math.random()*3500
  };
}

function tell(msg){
  const x=el('toast');
  x.textContent=msg;
  x.classList.add('show');

  clearTimeout(toastTimer);
  toastTimer=setTimeout(
    ()=>x.classList.remove('show'),1400
  );
}

function restart(){
  game={
    level:1,
    levelStart:now(),
    lives:3,
    score:0,
    combo:0,
    best:0,
    served:0,
    missed:0,
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
  tell('재료를 꾹 잡고 끌어서 조리판에 놓아 봐!');
}

function advance(){
  if(game.level===5){
    end(true);
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

  tell(
    `🎉 LEVEL ${game.level}! 제한 시간 ${
      LEVEL_TIMES[game.level-1]
    }초`
  );
}

function loseLife(message){
  if(game.ended)return;

  game.lives--;
  game.combo=0;
  updateHud();

  if(game.lives<=0){
    end(false);
  }else{
    tell(`${message} 남은 목숨 ${game.lives}개`);
  }
}

function renderAll(){
  renderCustomers();
  renderGrills();
  renderPlate();
  renderSupplies();
  updateHud();
}

function updateHud(){
  el('level').textContent=game.level;
  el('score').textContent=game.score;
  el('combo').textContent=game.combo;
  el('lives').textContent=
    '❤️'.repeat(game.lives)+
    '🖤'.repeat(3-game.lives);
}

function renderCustomers(){
  el('customers').innerHTML=
    game.customers.map((c,i)=>`
      <div class="customer"
           data-drop="customer"
           data-index="${i}">
        <span class="face">${c.face}</span>
        <strong>손님 ${i+1} · 주문표</strong>
        <span class="order">
          🐙 ${c.fill.emoji} ${c.top.emoji}
        </span>
        <span class="order-desc">
          ${c.fill.name} + ${c.top.name}
        </span>
        <div class="patience">
          <span id="patience-${i}"></span>
        </div>
        <small>완성 접시를 여기에 놓아 줘!</small>
      </div>
    `).join('');
}

function renderGrills(){
  const captions={
    empty:'재료를 올려 줘',
    cooking:'굽는 중...',
    ready:'접시로 끌어!',
    burnt:'휴지통에 버려!'
  };

  el('grills').innerHTML=
    game.grills.map((g,i)=>{
      const movable=
        g.state==='ready'||g.state==='burnt';

      const em=
        g.state==='cooking'?'🥣':
        g.state==='ready'?(g.fill?.emoji||'🐙'):
        g.state==='burnt'?'💨':'';

      const source=movable?
        `data-source="grill"
         data-index="${i}"
         data-emoji="${em||'🍡'}"
         data-label="${
           g.state==='burnt'?'탄 음식':'익은 타코야끼'
         }"`:'';

      return `
        <div class="grill"
             data-drop="grill"
             data-index="${i}"
             ${source}>
          <div class="holes">
            ${
              Array.from({length:6},()=>`
                <div class="ball ${g.state}">
                  ${em}
                </div>
              `).join('')
            }
          </div>
          <label>${i+1}번 조리판</label>
          <div class="cookbar">
            <span id="cook-${i}"></span>
          </div>
          <small>${captions[g.state]}</small>
        </div>
      `;
    }).join('');
}

function renderPlate(){
  const plate=el('plate');

  if(!game.plate){
    plate.innerHTML='🍽️';
    plate.removeAttribute('data-source');

    el('plate-help').textContent=
      '익은 타코야끼를 끌어와!';
  }else{
    plate.innerHTML=`
      🐙<span>
        ${game.plate.fill.name}
        ${
          game.plate.top?
          ' + '+game.plate.top.name:''
        }
      </span>
    `;

    plate.setAttribute('data-source','plate');
    plate.setAttribute('data-emoji','🍡');
    plate.setAttribute('data-label','완성 접시');

    el('plate-help').textContent=
      game.plate.top?
      '손님에게 끌어다 줘!':
      '토핑을 끌어다 놓아 줘!';
  }
}

function renderSupplies(){
  el('fillings').innerHTML=
    fillings.map((v,i)=>`
      <div class="item"
           data-source="filling"
           data-index="${i}"
           data-emoji="${v.emoji}"
           data-label="${v.name}">
        <span class="emoji">${v.emoji}</span>
        ${v.name}
      </div>
    `).join('');

  el('toppings').innerHTML=
    toppings.map((v,i)=>`
      <div class="item"
           data-source="topping"
           data-index="${i}"
           data-emoji="${v.emoji}"
           data-label="${v.name}">
        <span class="emoji">${v.emoji}</span>
        ${v.name}
      </div>
    `).join('');
}

function handleDrop(kind,index,target,targetIndex){
  if(game.ended)return;

  // 속재료를 빈 조리판에 놓기
  if(target==='grill'&&kind==='filling'){
    const g=game.grills[targetIndex];

    if(g.state!=='empty'){
      tell('이 조리판은 사용 중이야!');
      return;
    }

    game.grills[targetIndex]={
      state:'cooking',
      fill:fillings[index],
      born:now()
    };

    renderGrills();
    tell(`${fillings[index].name} 타코야끼 굽기 시작!`);
    return;
  }

  // 다 익은 타코야끼를 접시로 옮기기
  if(target==='plate'&&kind==='grill'){
    const g=game.grills[index];

    if(g.state!=='ready'){
      tell('익은 타코야끼만 접시에 올릴 수 있어!');
      return;
    }

    if(game.plate){
      tell('접시가 이미 차 있어!');
      return;
    }

    game.plate={
      fill:g.fill,
      top:null
    };

    game.grills[index]={state:'empty'};

    renderGrills();
    renderPlate();
    tell('접시에 담았어! 토핑을 올려 줘.');
    return;
  }

  // 토핑을 접시 위에 올리기
  if(target==='plate'&&kind==='topping'){
    if(!game.plate){
      tell('먼저 타코야끼를 접시로 가져와!');
      return;
    }

    game.plate.top=toppings[index];

    renderPlate();
    tell('토핑 완료! 완성 접시를 손님에게 끌어다 줘!');
    return;
  }

  // 완성 접시를 손님에게 서빙하기
  if(target==='customer'&&kind==='plate'){
    if(!game.plate?.top){
      tell('토핑까지 올리고 서빙해 줘!');
      return;
    }

    const c=game.customers[targetIndex];

    if(
      c.fill.name===game.plate.fill.name &&
      c.top.name===game.plate.top.name
    ){
      const points=
        100+Math.min(game.combo,5)*20;

      game.score+=points;
      game.combo++;
      game.best=Math.max(game.best,game.combo);
      game.served++;

      game.customers[targetIndex]=newCustomer();

      renderCustomers();
      updateHud();
      tell(`🎉 주문 성공! +${points}점`);
    }else{
      loseLife('❌ 잘못 서빙했어!');
    }

    game.plate=null;
    renderPlate();
    return;
  }

  // 휴지통으로 음식 버리기
  if(target==='trash'){
    if(kind==='plate'){
      game.plate=null;
      renderPlate();
      tell('접시의 음식을 버렸어!');
      return;
    }

    if(kind==='grill'){
      if(
        !['ready','burnt'].includes(
          game.grills[index].state
        )
      )return;

      game.grills[index]={state:'empty'};

      renderGrills();
      tell('음식을 휴지통에 버렸어!');
      return;
    }
  }

  tell('여기에는 놓을 수 없어!');
}

// 마우스나 손가락을 따라 움직이는 음식 표시
function updateGhost(e){
  if(!drag)return;

  drag.ghost.style.left=e.clientX+'px';
  drag.ghost.style.top=e.clientY+'px';

  const target=document.elementFromPoint(
    e.clientX,e.clientY
  )?.closest('[data-drop]');

  if(highlighted&&highlighted!==target){
    highlighted.classList.remove('drop-over');
  }

  highlighted=target||null;

  if(highlighted){
    highlighted.classList.add('drop-over');
  }
}

// 드래그 시작
document.addEventListener('pointerdown',e=>{
  if(game?.ended||drag||e.button!==0)return;

  const source=e.target.closest('[data-source]');
  if(!source)return;

  e.preventDefault();

  const ghost=document.createElement('div');
  ghost.className='drag-ghost';

  ghost.innerHTML=`
    ${source.dataset.emoji||'🍡'}
    <small>${source.dataset.label||'음식'}</small>
  `;

  document.body.appendChild(ghost);

  drag={
    pointerId:e.pointerId,
    kind:source.dataset.source,
    index:Number(source.dataset.index||0),
    source,
    ghost
  };

  source.classList.add('dragging-original');
  updateGhost(e);
});

// 드래그 중 이동
document.addEventListener(
  'pointermove',
  e=>{
    if(drag&&e.pointerId===drag.pointerId){
      e.preventDefault();
      updateGhost(e);
    }
  },
  {passive:false}
);

// 드래그 종료
function releaseDrag(e,cancel=false){
  if(!drag||e.pointerId!==drag.pointerId)return;

  const current=drag;

  const destination=cancel?
    null:
    document.elementFromPoint(
      e.clientX,e.clientY
    )?.closest('[data-drop]');

  current.source.classList.remove('dragging-original');
  current.ghost.remove();

  if(highlighted){
    highlighted.classList.remove('drop-over');
  }

  highlighted=null;
  drag=null;

  if(destination){
    handleDrop(
      current.kind,
      current.index,
      destination.dataset.drop,
      Number(destination.dataset.index||0)
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

// 게임 종료
function end(won){
  if(game.ended)return;

  game.ended=true;

  el('result-icon').textContent=won?'🏆':'💔';

  el('result-title').textContent=
    won?'5레벨 생존 성공!':'게임 오버!';

  el('result-text').innerHTML=`
    도달 레벨 <b>${game.level} / 5</b><br>
    총 <b>${game.served}개</b> 완성<br>
    최종 점수 <b>${game.score}점</b><br>
    최고 콤보 <b>${game.best}</b><br>
    놓친 주문 <b>${game.missed}</b>
  `;

  el('overlay').classList.remove('hidden');
}

// 실시간 게임 진행
function tick(){
  if(!game||game.ended)return;

  const t=now();
  const limit=LEVEL_TIMES[game.level-1];

  const left=Math.max(
    0,
    limit-(t-game.levelStart)/1000
  );

  el('time').textContent=Math.ceil(left);

  el('timer').classList.toggle(
    'urgent',left<=10
  );

  if(left<=0){
    advance();
    return;
  }

  let needGrillRender=false;
  let needCustomerRender=false;

  game.grills.forEach((g,i)=>{
    if(g.state==='empty')return;

    const passed=t-g.born;

    if(
      g.state==='cooking' &&
      passed>=COOK_MS
    ){
      g.state='ready';
      needGrillRender=true;
    }

    if(
      g.state==='ready' &&
      passed>=BURN_MS
    ){
      g.state='burnt';

      game.score=Math.max(
        0,game.score-10
      );

      game.combo=0;
      needGrillRender=true;

      updateHud();
      tell('🔥 타코야끼가 탔어! -10점');
    }

    const bar=el('cook-'+i);

    if(bar){
      bar.style.width=
        `${Math.min(100,passed/BURN_MS*100)}%`;

      bar.style.background=
        g.state==='ready'?'#75d66b':
        g.state==='burnt'?'#e35e51':
        '#ffd264';
    }
  });

  if(needGrillRender){
    renderGrills();
  }

  for(let i=0;i<game.customers.length;i++){
    const c=game.customers[i];

    const r=
      1-(t-c.born)/c.patience;

    const bar=el('patience-'+i);

    if(bar){
      bar.style.width=
        `${Math.max(0,r)*100}%`;

      bar.style.background=
        r<.3?'#e4584c':
        r<.55?'#ecad46':
        '#69b65a';
    }

    if(r<=0){
      game.missed++;

      game.customers[i]=newCustomer();
      needCustomerRender=true;

      loseLife('⌛ 손님이 기다리다 떠났어!');

      if(game.ended)return;
    }
  }

  if(needCustomerRender){
    renderCustomers();
  }
}

restart();
setInterval(tick,80);
</script>
</body>
</html>
""",height=900,scrolling=False)
