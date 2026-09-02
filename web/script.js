const STATES=[
{
name:"Idle",
color:"#00E5A8",
hint:"Jarvis is calmly waiting."
},
{
name:"Listening",
color:"#00C2FF",
hint:"Receiving your voice."
},
{
name:"Thinking",
color:"#8B5CF6",
hint:"Reasoning through the cognition pipeline."
},
{
name:"Speaking",
color:"#FFB703",
hint:"Delivering a response."
}
];

const orb=document.getElementById("orb");
const state=document.getElementById("state");
const hint=document.getElementById("hint");
const core=document.querySelector(".core");

let index=0;

function render(){

const s=STATES[index];

state.textContent=s.name;
hint.textContent=s.hint;

core.style.background=
`radial-gradient(circle, ${s.color}, #071321)`;

core.style.boxShadow=
`0 0 60px ${s.color}`;

}

render();

orb.addEventListener("click",()=>{

index=(index+1)%STATES.length;

render();

});

const stages=document.querySelectorAll(".pipeline div");

let step=0;

setInterval(()=>{

stages.forEach(x=>x.classList.remove("active"));

stages[step].classList.add("active");

step=(step+1)%stages.length;

},900);

function updateClock(){

const now=new Date();

const h=String(now.getHours()).padStart(2,"0");
const m=String(now.getMinutes()).padStart(2,"0");

document.getElementById("clock").textContent=`${h}:${m}`;

}

updateClock();

setInterval(updateClock,1000);