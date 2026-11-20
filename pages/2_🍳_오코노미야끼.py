
import streamlit as st
import streamlit.components.v1 as components

# ========================================
# 와글와글 포장마차 - 오코노미야끼
# ========================================

st.html("""
<style>
[data-testid="stMain"] .block-container {
    max-width: 100% !important;
    padding: .3rem .5rem !important;
}
[data-testid="stAppViewContainer"] {
    background: #fff0d8;
}
iframe {
    display: block;
    border: none !important;
}
</style>
""")

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
html,body{
 margin:0;padding:0;width:100%;height:100%;
 font-family:"Malgun Gothic",sans-serif;
 color:#70422b;overflow:hidden
}
.game{
 position:relative;width:100%;height:680px;
 padding:9px 12px;border-radius:18px;overflow:hidden;
 background:linear-gradient(
 180deg,#6784aa 0%,#e7aaa3 34%,
 #f8d9a6 73%,#bf8961 100%)
}
.header{
 display:flex;align-items:center;
 justify-content:space-between;gap:8px
}
.logo{
 padding:8px 12px;border:3px solid #a85d37;
 border-radius:13px;background:#fff0ce;
 color:#974b31;font-size:17px;font-weight:900
}
.stats{display:flex;gap:6px}
.stat{
 min-width:72px;padding:5px 7px;text-align:center;
 border:2px solid #f6d6a0;border-radius:11px;
 background:#784d3d;color:white;
 font-size:15px;font-weight:900
}
.stat small{display:block;font-size:10px;color:#ffe2bd}
.timer{background:#c8584c}
.sign{
 width:fit-content;margin:5px auto 12px;
 padding:6px 24px;background:#934a35;
 border:3px solid #f2ca87;border-radius:13px;
 box-shadow:0 4px #683b29;color:#fff6dc;
 font-size:17px;font-weight:900
}
.customers{
 display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
 gap:9px;max-width:1050px;margin:0 auto 12px
}
.customer{
 min-height:128px;padding:6px;
 border:3px solid #d7a06c;border-radius:17px;
 background:#fff3df;text-align:center;
 box-shadow:0 4px #a16a43;
 display:flex;flex-direction:column;
 align-items:center;justify-content:center;gap:4px
}
.face{font-size:29px}
.order{font-size:12px;font-weight:900}
.patience{
 width:90%;height:9px;background:#e4ccb0;
 border-radius:20px;overflow:hidden
}
.patience span{
 display:block;height:100%;width:100%;
 background:#70b963
}
.counter{
 max-width:1200px;margin:0 auto;
 padding:8px;border:5px solid #8e5334;
 border-radius:20px;box-shadow:0 5px #643b28;
 background:repeating-linear-gradient(
 0deg,#b87648 0 20px,#c88958 20px 40px)
}
.counter h3{
 margin:0 0 6px;text-align:center;
 color:#fff5de;font-size:15px
}
.kitchen{
 display:grid;grid-template-columns:minmax(0,2fr) minmax(200px,.85fr);
 gap:9px
}
.grills{
 display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
 gap:7px;padding:7px;background:#44434a;
 border:4px solid #302e34;border-radius:15px
}
.grill{
 min-height:157px;padding:6px 3px;
 border:2px solid #686268;border-radius:13px;
 background:#28282c;color:#fff5da;
 display:flex;flex-direction:column;
 align-items:center;justify-content:center;
 gap:5px;text-align:center
}
.grill strong{font-size:11px;pointer-events:none}
.grill small{font-size:10px;pointer-events:none}
.pancake{
 width:75px;height:65px;display:grid;place-items:center;
 font-size:37px;pointer-events:none
}
.bar{
 width:80%;height:7px;background:#151515;
 border-radius:20px;overflow:hidden;pointer-events:none
}
.bar span{display:block;height:100%;width:0;background:#efc456}
.right{display:flex;flex-direction:column;gap:7px}
.plate-zone{
 flex:1;min-height:110px;padding:7px;
 background:#fff1d9;border:3px solid #e5bd8f;
 border-radius:13px;text-align:center
}
.plate-zone strong{font-size:12px}
.plate{
 width:78px;height:78px;margin:5px auto;
 border-radius:50%;display:flex;flex-direction:column;
 align-items:center;justify-content:center;
 background:radial-gradient(circle,white 0 48%,#b7d6e2 50% 60%,white 62%);
 font-size:28px;font-weight:900
}
.plate small{font-size:9px;pointer-events:none}
#plate-help{font-size:10px}
.trash{
 min-height:35px;padding:5px;background:#f9d6c7;
 border:3px solid #e5bd8f;border-radius:12px;
 text-align:center;font-size:12px;font-weight:900
}
.supplies{
 display:grid;grid-template-columns:1fr 1fr;
 gap:9px;max-width:1200px;margin:12px auto 7px
}
.supply{
 padding:7px;border:3px solid #be8454;
 border-radius:15px;background:#fff1da
}
.supply h3{margin:0 0 6px;font-size:12px}
.items{display:flex;gap:6px}
.item{
 flex:1;min-width:0;padding:6px 3px;
 background:#fffaf1;border:2px solid #e5c49a;
 border-radius:11px;text-align:center;
 font-size:12px;font-weight:900
}
.item span{display:block;font-size:24px}
.help{
 max-width:1200px;margin:auto;padding:6px;
 background:#fff4da;border:2px solid #d8ab75;
 border-radius:10px;text-align:center;
 font-size:11px;font-weight:800
}
[data-source]{cursor:grab;touch-action:none;user-select:none}
.dragging-original{opacity:.45}
.drop-over{outline:4px solid #ffe47c;outline-offset:2px}
.ghost{
 position:fixed;z-index:1000;pointer-events:none;
 padding:9px;border:3px solid #d9a16b;
 border-radius:14px;background:#fff8e7;
 box-shadow:0 5px 12px #0004;
 font-size:28px;text-align:center
}
.ghost small{display:block;font-size:11px}
.toast{
 position:absolute;z-index:30;left:50%;bottom:12px;
 transform:translateX(-50%);
 padding:9px 20px;background:#71432f;
 border-radius:14px;color:white;
 font-size:13px;font-weight:900;
 opacity:0;pointer-events:none;text-align:center
}
.toast.show{opacity:1}
.overlay{
 position:absolute;z-index:35;inset:0;
 display:flex;align-items:center;justify-content:center;
 background:#241b20b8;padding:15px
}
.overlay.hidden{display:none}
.panel{
 width:min(460px,95%);padding:30px 20px;
 background:#fff4d9;border:6px solid #bc7950;
 border-radius:25px;box-shadow:0 10px #7c4d37;
 text-align:center
}
.panel h1{color:#954a33;font-size:26px}
.panel p{font-size:15px;font-weight:900;line-height:1.8}
.start{
 margin-top:10px;padding:14px 25px;
 border:none;border-radius:15px;
 background:#e8734c;color:white;
 box-shadow:0 5px #aa4c30;
 font-size:20px;font-weight:900;cursor:pointer
}
.countdown{
 position:absolute;z-index:40;inset:0;
 display:none;align-items:center;justify-content:center;
 background:#2d1e29ba;color:#fff2bc;
 font-size:110px;font-weight:900
}
.countdown.show{display:flex}
@media(max-width:800px){
 .game{padding:6px}
 .logo{font-size:12px}
 .stat{min-width:48px;padding:4px;font-size:12px}
 .stat small{font-size:8px}
 .sign{font-size:14px}
 .customers{gap:4px}
 .customer{padding:4px}
 .face{font-size:24px}
 .order{font-size:10px}
 .kitchen{grid-template-columns:minmax(0,1.5fr) minmax(145px,.8fr)}
 .grills{gap:3px;padding:4px}
 .grill{padding:3px 1px}
 .pancake{width:50px;font-size:26px}
 .plate{width:57px;height:57px;font-size:22px}
 .item{font-size:10px}
 .item span{font-size:19px}
}
</style>
</head>
<body>
<div class="game">
 <div class="header">
  <div class="logo">🏮 와글와글 포장마차</div>
  <div class="stats">
   <div class="stat"><small>레벨</small><span id="level">1</span>/5</div>
   <div class="stat timer"><small>남은 시간</small><span id="time">90</span>초</div>
   <div class="stat"><small>목숨</small><span id="lives">❤️❤️❤️</span></div>
   <div class="stat"><small>점수</small><span id="score">0</span></div>
  </div>
 </div>
 <div class="sign">🍳 오코노미야끼 가게 🍳</div>
 <div class="customers" id="customers"></div>

 <div class="counter">
  <h3>🔥 오코노미야끼 철판 조리대</h3>
  <div class="kitchen">
   <div class="grills" id="grills"></div>
   <div class="right">
    <div class="plate-zone" data-drop="plate">
     <strong>🍽️ 완성 접시</strong>
     <div class="plate" id="plate">🍽️</div>
     <small id="plate-help">완성된 음식을 옮겨 주세요</small>
    </div>
    <div class="trash" data-drop="trash">🗑️ 휴지통</div>
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
  반죽 → 재료 → 굽기 → 뒤집기 → 접시 → 토핑 → 손님에게 서빙
 </div>
 <div class="toast" id="toast"></div>

 <div class="overlay" id="overlay">
  <div class="panel">
   <div id="panel-icon" style="font-size:58px">🍳</div>
   <h1 id="panel-title">오코노미야끼 가게</h1>
   <p id="panel-text">
    손님의 주문대로 오코노미야끼를 만들어 주세요!<br>
    ❤️ 목숨 3개 · 총 5레벨<br>
    5레벨까지 살아남으면 승리합니다!
   </p>
   <button class="start" id="start-button"
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
const LEVEL_TIMES=[90,120,120,150,150];
const CUSTOMER_WAIT=[
 [40,45],[30,35],[22,27],[15,20],[10,13]
];
const FIRST_COOK_MS=2200;
const SECOND_COOK_MS=2000;
const BURN_WAIT_MS=4200;

const ingredients=[
 {name:"반죽",emoji:"🥣",type:"batter"},
 {name:"돼지고기",emoji:"🥩",type:"filling"},
 {name:"해산물",emoji:"🦐",type:"filling"},
 {name:"치즈",emoji:"🧀",type:"filling"}
];
const tools=[
 {name:"뒤집개",emoji:"🍴",type:"flip"},
 {name:"소스",emoji:"🍯",type:"topping"},
 {name:"마요네즈",emoji:"🥛",type:"topping"}
];
const fillings=ingredients.filter(x=>x.type==="filling");
const toppings=tools.filter(x=>x.type==="topping");
const faces=["🐱","🐰","🐻","🦊","🐼","🐸"];

const el=id=>document.getElementById(id);
const now=()=>performance.now();
const pick=a=>a[Math.floor(Math.random()*a.length)];

let game=null;
let drag=null;
let highlighted=null;
let toastTimer=null;
let counting=false;

async function beginCountdown(){
 if(counting)return;
 counting=true;
 el("overlay").classList.add("hidden");
 el("countdown").classList.add("show");

 for(const n of ["3","2","1"]){
  el("count-text").textContent=n;
  await new Promise(r=>setTimeout(r,1000));
 }
 el("count-text").textContent="START!";
 await new Promise(r=>setTimeout(r,600));
 el("countdown").classList.remove("show");
 counting=false;
 startGame();
}

function newCustomer(){
 const [min,max]=CUSTOMER_WAIT[game.level-1];
 return {
  face:pick(faces),
  fill:pick(fillings),
  top:pick(toppings),
  born:now(),
  patience:(min+Math.random()*(max-min))*1000
 };
}

function startGame(){
 game={
  level:1,levelStart:now(),
  lives:3,score:0,combo:0,best:0,served:0,missed:0,
  grills:Array.from({length:3},()=>({state:"empty"})),
  plate:null,customers:[],ended:false
 };
 game.customers=Array.from({length:3},newCustomer);
 renderAll();
 tell("영업 시작! 주문을 확인하세요!");
}

function tell(message){
 const t=el("toast");
 t.textContent=message;
 t.classList.add("show");
 clearTimeout(toastTimer);
 toastTimer=setTimeout(()=>t.classList.remove("show"),1500);
}

function updateHud(){
 if(!game)return;
 el("level").textContent=game.level;
 el("lives").textContent="❤️".repeat(game.lives);
 el("score").textContent=game.score;
}

function renderCustomers(){
 if(!game)return;
 el("customers").innerHTML=game.customers.map((c,i)=>`
  <div class="customer" data-drop="customer" data-index="${i}">
   <div class="face">${c.face}</div>
   <div class="order">
    ${c.fill.emoji} ${c.fill.name} +
    ${c.top.emoji} ${c.top.name}
   </div>
   <div class="patience">
    <span id="patience-${i}"></span>
   </div>
  </div>`).join("");
}

function renderGrills(){
 if(!game)return;
 const messages={
  empty:"반죽을 넣어 주세요",
  batter:"재료를 올려 주세요",
  cooking:"첫 번째 면 굽는 중",
  flip:"뒤집개로 뒤집어 주세요!",
  second:"두 번째 면 굽는 중",
  ready:"다 익었어요!",
  burnt:"음식이 탔어요!"
 };
 const icons={
  empty:"⚫",batter:"🥣",cooking:"🟡",
  flip:"🍳",second:"🟤",ready:"🥞",burnt:"⚫"
 };

 el("grills").innerHTML=game.grills.map((g,i)=>{
  const source=["ready","burnt"].includes(g.state)
   ?`data-source="grill" data-index="${i}"
     data-emoji="🍳" data-label="오코노미야끼"`:"";

  return `
   <div class="grill" data-drop="grill" data-index="${i}" ${source}>
    <div class="pancake">${icons[g.state]}</div>
    <strong>${i+1}번 철판</strong>
    <div class="bar"><span id="cook-${i}"></span></div>
    <small>${messages[g.state]}</small>
   </div>`;
 }).join("");
}

function renderPlate(){
 const p=el("plate");
 if(!game||!game.plate){
  p.innerHTML="🍽️";
  p.removeAttribute("data-source");
  el("plate-help").textContent="익은 음식을 옮겨 주세요";
  return;
 }
 p.innerHTML=`
  🍳<small>
   ${game.plate.fill.name}
   ${game.plate.top?" + "+game.plate.top.name:""}
  </small>`;
 p.dataset.source="plate";
 p.dataset.emoji="🍳";
 p.dataset.label="완성된 음식";
 el("plate-help").textContent=game.plate.top
  ?"손님에게 서빙하세요":"토핑을 올려 주세요";
}

function renderItems(){
 el("ingredients").innerHTML=ingredients.map((x,i)=>`
  <div class="item" data-source="ingredient" data-index="${i}"
       data-emoji="${x.emoji}" data-label="${x.name}">
   <span>${x.emoji}</span>${x.name}
  </div>`).join("");

 el("tools").innerHTML=tools.map((x,i)=>`
  <div class="item" data-source="tool" data-index="${i}"
       data-emoji="${x.emoji}" data-label="${x.name}">
   <span>${x.emoji}</span>${x.name}
  </div>`).join("");
}

function renderAll(){
 renderCustomers();
 renderGrills();
 renderPlate();
 renderItems();
 updateHud();
}

function loseLife(message){
 game.lives--;
 game.combo=0;
 updateHud();
 if(game.lives<=0)endGame(false);
 else tell(`${message} 남은 목숨 ${game.lives}개`);
}

function serve(index){
 const c=game.customers[index];
 const p=game.plate;
 if(!p||!p.top){
  tell("토핑까지 완성한 음식을 서빙하세요!");
  return;
 }

 const correct=p.fill.name===c.fill.name &&
               p.top.name===c.top.name;

 game.plate=null;
 renderPlate();

 if(correct){
  game.combo++;
  game.best=Math.max(game.best,game.combo);
  game.served++;
  game.score+=100+Math.min(game.combo*10,100);
  tell("주문 성공! 맛있게 드세요!");
 }else{
  game.missed++;
  loseLife("주문이 틀렸어요!");
 }
 if(!game.ended){
  game.customers[index]=newCustomer();
  renderCustomers();
  updateHud();
 }
}

function handleDrop(kind,index,target,targetIndex){
 if(!game||game.ended)return;

 if(kind==="ingredient"&&target==="grill"){
  const item=ingredients[index];
  const g=game.grills[targetIndex];
  if(!g)return;

  if(item.type==="batter"&&g.state==="empty"){
   game.grills[targetIndex]={state:"batter"};
   renderGrills();
   tell("반죽 완료! 재료를 올려 주세요.");
   return;
  }

  if(item.type==="filling"&&g.state==="batter"){
   game.grills[targetIndex]={
    state:"cooking",
    fill:item,
    since:now()
   };
   renderGrills();
   tell("첫 번째 면을 굽고 있어요!");
   return;
  }

  tell("반죽 → 재료 순서로 조리해 주세요!");
  return;
 }

 if(kind==="tool"&&target==="grill"){
  const tool=tools[index];
  const g=game.grills[targetIndex];

  if(tool.type!=="flip"||!g||g.state!=="flip"){
   tell("뒤집을 타이밍에 뒤집개를 사용하세요!");
   return;
  }

  g.state="second";
  g.since=now();
  renderGrills();
  tell("뒤집기 성공! 반대쪽을 굽습니다.");
  return;
 }

 if(kind==="grill"&&target==="plate"){
  const g=game.grills[index];

  if(!g||g.state!=="ready"){
   tell("다 익은 음식만 접시에 담을 수 있어요!");
   return;
  }
  if(game.plate){
   tell("접시가 이미 차 있어요!");
   return;
  }

  game.plate={fill:g.fill,top:null};
  game.grills[index]={state:"empty"};
  renderGrills();
  renderPlate();
  tell("접시에 담았어요! 토핑을 올려 주세요.");
  return;
 }

 if(kind==="tool"&&target==="plate"){
  const tool=tools[index];

  if(tool.type!=="topping"){
   tell("접시에는 토핑을 올려 주세요!");
   return;
  }
  if(!game.plate){
   tell("먼저 음식을 접시에 담아 주세요!");
   return;
  }
  if(game.plate.top){
   tell("이미 토핑을 올렸어요!");
   return;
  }

  game.plate.top=tool;
  renderPlate();
  return;
 }

 if(kind==="plate"&&target==="customer"){
  serve(targetIndex);
  return;
 }

 if(target==="trash"){
  if(kind==="plate"){
   game.plate=null;
   renderPlate();
   tell("음식을 버렸습니다.");
   return;
  }
  if(kind==="grill"){
   game.grills[index]={state:"empty"};
   renderGrills();
   tell("철판을 비웠습니다.");
   return;
  }
 }
 tell("올바른 위치로 드래그해 주세요!");
}

/* 드래그 앤 드롭 */
function moveGhost(e){
 if(!drag)return;

 drag.ghost.style.left=(e.clientX+12)+"px";
 drag.ghost.style.top=(e.clientY+12)+"px";

 if(highlighted)highlighted.classList.remove("drop-over");

 highlighted=document.elementFromPoint(
  e.clientX,e.clientY
 )?.closest("[data-drop]");

 if(highlighted)highlighted.classList.add("drop-over");
}

document.addEventListener("pointerdown",e=>{
 if(!game||game.ended||drag)return;
 const source=e.target.closest("[data-source]");
 if(!source)return;
 e.preventDefault();

 const ghost=document.createElement("div");
 ghost.className="ghost";
 ghost.innerHTML=`
  ${source.dataset.emoji||"🍳"}
  <small>${source.dataset.label||""}</small>`;
 document.body.appendChild(ghost);

 drag={
  pointerId:e.pointerId,
  source,
  kind:source.dataset.source,
  index:Number(source.dataset.index||0),
  ghost
 };

 source.classList.add("dragging-original");
 moveGhost(e);
});

document.addEventListener("pointermove",e=>{
 if(drag&&drag.pointerId===e.pointerId){
  e.preventDefault();
  moveGhost(e);
 }
},{passive:false});

function releaseDrag(e){
 if(!drag||drag.pointerId!==e.pointerId)return;

 const d=drag;
 const target=document.elementFromPoint(
  e.clientX,e.clientY
 )?.closest("[data-drop]");

 d.ghost.remove();

 if(d.source.isConnected){
  d.source.classList.remove("dragging-original");
 }
 if(highlighted){
  highlighted.classList.remove("drop-over");
 }

 drag=null;
 highlighted=null;

 if(target){
  handleDrop(
   d.kind,d.index,
   target.dataset.drop,
   Number(target.dataset.index||0)
  );
 }
}

document.addEventListener("pointerup",releaseDrag);

document.addEventListener("pointercancel",e=>{
 if(!drag||drag.pointerId!==e.pointerId)return;
 drag.ghost.remove();
 if(drag.source.isConnected){
  drag.source.classList.remove("dragging-original");
 }
 if(highlighted)highlighted.classList.remove("drop-over");
 drag=null;
 highlighted=null;
});

/* 레벨과 승패 */
function nextLevel(){
 if(game.level===5){
  endGame(true);
  return;
 }

 game.level++;
 game.levelStart=now();
 game.grills=Array.from({length:3},()=>({state:"empty"}));
 game.plate=null;
 game.customers=Array.from({length:3},newCustomer);
 renderAll();
 tell(`LEVEL ${game.level} 시작!`);
}

function endGame(won){
 if(!game||game.ended)return;
 game.ended=true;

 el("panel-icon").textContent=won?"🏆":"💔";
 el("panel-title").textContent=won?"최종 승리!":"게임 오버!";
 el("panel-text").innerHTML=`
  도달 레벨: ${game.level}/5<br>
  완성한 주문: ${game.served}개<br>
  최종 점수: ${game.score}점<br>
  최고 콤보: ${game.best}회<br>
  놓친 주문: ${game.missed}개`;
 el("start-button").textContent="🔄 다시 도전하기";
 el("overlay").classList.remove("hidden");
}

function tick(){
 if(!game||game.ended)return;

 const t=now();
 const remaining=LEVEL_TIMES[game.level-1]-
  (t-game.levelStart)/1000;

 el("time").textContent=Math.max(0,Math.ceil(remaining));

 if(remaining<=0){
  nextLevel();
  return;
 }

 let changed=false;

 game.grills.forEach(g=>{
  if(!["cooking","flip","second","ready"].includes(g.state)){
   return;
  }

  const passed=t-g.since;

  if(g.state==="cooking"&&passed>=FIRST_COOK_MS){
   g.state="flip";
   g.since=t;
   changed=true;
  }

  if(g.state==="second"&&passed>=SECOND_COOK_MS){
   g.state="ready";
   g.since=t;
   changed=true;
  }

  if(["flip","ready"].includes(g.state)&&
     passed>=BURN_WAIT_MS){
   g.state="burnt";
   game.score=Math.max(0,game.score-10);
   game.combo=0;
   updateHud();
   changed=true;
   tell("🔥 오코노미야끼가 탔어요! -10점");
  }
 });

 if(changed)renderGrills();

 game.grills.forEach((g,i)=>{
  const bar=el(`cook-${i}`);
  if(!bar)return;
  const passed=g.since?t-g.since:0;

  const percent=g.state==="cooking"
   ?Math.min(100,passed/FIRST_COOK_MS*100)
   :g.state==="second"
    ?Math.min(100,passed/SECOND_COOK_MS*100)
    :["flip","ready","burnt"].includes(g.state)
     ?100:0;

  bar.style.width=percent+"%";
  bar.style.background=g.state==="burnt"
   ?"#9d5950":"#efc456";
 });

 let customersChanged=false;
 for(let i=0;i<game.customers.length;i++){
  const c=game.customers[i];

  if(t-c.born>=c.patience){
   game.missed++;
   loseLife("손님이 기다리다 떠났어요!");
   if(game.ended)return;

   game.customers[i]=newCustomer();
   customersChanged=true;
  }
 }

 if(customersChanged)renderCustomers();

 game.customers.forEach((c,i)=>{
  const bar=el(`patience-${i}`);
  if(!bar)return;

  const p=Math.max(0,100*(1-(t-c.born)/c.patience));
  bar.style.width=p+"%";
  bar.style.background=p<=30?"#dc6753":
                       p<=65?"#e8b64a":"#70b963";
 });
}

function initializeScreen(){
 renderItems();

 el("customers").innerHTML=
  Array.from({length:3},(_,i)=>`
   <div class="customer">
    <div class="face">${faces[i]}</div>
    <div class="order">게임 시작 후 주문 표시</div>
    <div class="patience"><span></span></div>
   </div>`).join("");

 el("grills").innerHTML=
  Array.from({length:3},(_,i)=>`
   <div class="grill">
    <div class="pancake">⚫</div>
    <strong>${i+1}번 철판</strong>
    <div class="bar"></div>
    <small>게임을 시작해 주세요</small>
   </div>`).join("");

 el("ingredients").innerHTML="";
 renderPlate();
}

initializeScreen();
setInterval(tick,100);
</script>
</body>
</html>
"""

components.html(
    GAME_HTML,
    height=700,
    scrolling=False,
)
