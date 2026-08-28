// Login screen — click Enter or press any key to dismiss.
const loginScreen = document.getElementById('loginScreen');
const loginEnter = document.getElementById('loginEnter');

function dismissLogin() {
  loginScreen.classList.add('hidden');
  document.removeEventListener('keydown', dismissLogin);
}

loginEnter.addEventListener('click', dismissLogin);
document.addEventListener('keydown', dismissLogin);

// Jarvis Orb — four real states from the design brief.
const orb = document.getElementById('jarvisOrb');
const orbCore = orb.querySelector('.orb-core');
const orbRing = orb.querySelector('.ring-1') || orb.querySelectorAll('.orb-ring')[0];
const stateLabel = document.getElementById('orbStateLabel');
const orbHint = document.getElementById('orbHint');

const orbStates = [
  { name: 'Idle', a: '#22D3A6', b: '#0F2A25', ring: 'rgba(34,211,166,0.4)',
    hint: 'Mint pulse — Jarvis is present, listening for nothing in particular.' },
  { name: 'Listening', a: '#22D3A6', b: '#07131F', ring: 'rgba(34,211,166,0.5)',
    hint: 'Bioluminescent wave — Jarvis has heard something and is paying attention.' },
  { name: 'Thinking', a: '#8B5E3C', b: '#0F2A25', ring: 'rgba(139,94,60,0.55)',
    hint: 'Walnut rings — moving through the governed execution pipeline.' },
  { name: 'Speaking', a: '#C68A2B', b: '#22D3A6', ring: 'rgba(198,138,43,0.5)',
    hint: 'Gold ripple — delivering a response back to you.' }
];

let orbIndex = 0;

function applyOrbState(index) {
  const s = orbStates[index];
  orbCore.style.setProperty('--orb-a', s.a);
  orbCore.style.setProperty('--orb-b', s.b);
  document.querySelectorAll('.orb-ring').forEach(r => r.style.setProperty('--orb-ring', s.ring));
  stateLabel.textContent = s.name;
  stateLabel.style.color = s.a;
  orbHint.textContent = s.hint;
}

applyOrbState(0);

orb.addEventListener('click', function () {
  orbIndex = (orbIndex + 1) % orbStates.length;
  applyOrbState(orbIndex);
});

// Execution pipeline — visual illumination only, not wired to real jobs yet.
const pipelineStages = document.querySelectorAll('.pipeline-stage');
let activeStage = 0;

function animatePipeline() {
  pipelineStages.forEach(stage => {
    stage.classList.remove('active');
    stage.querySelector('.stage-dot').classList.remove('active');
  });

  const current = pipelineStages[activeStage];
  if (current) {
    current.classList.add('active');
    current.querySelector('.stage-dot').classList.add('active');
  }

  activeStage = (activeStage + 1) % pipelineStages.length;
}

animatePipeline();
setInterval(animatePipeline, 1200);

// Real clock, no fabricated data anywhere else on this page.
function updateTime() {
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  document.getElementById('clock').textContent = `${hours}:${minutes}`;
}

updateTime();
setInterval(updateTime, 30000);