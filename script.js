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

// Real clock, no fabricated data anywhere else on this page.
function updateTime() {
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  document.getElementById('clock').textContent = `${hours}:${minutes}`;
}

updateTime();
setInterval(updateTime, 30000);

// --- Live backend data via GET /api/dashboard ---
// Same route this static page can now reach when served by
// core/applications/api/http_server.py (same-origin). Replaces the
// previously hardcoded provider "Connected" labels, the fake test-count
// claim, and the animated (not real) pipeline stage cycling.

const pipelineStages = document.querySelectorAll('.pipeline-stage');

function applyPipelineStage(currentIndex) {
  pipelineStages.forEach((stage, i) => {
    const active = i === currentIndex;
    stage.classList.toggle('active', active);
    stage.querySelector('.stage-dot').classList.toggle('active', active);
  });
}

function applyProviderStatus(providerKey, elementIdSuffix) {
  return function (status) {
    const dot = document.getElementById('dot' + elementIdSuffix);
    const label = document.getElementById('status' + elementIdSuffix);
    if (!dot || !label) return;

    const connected = status === 'connected';
    dot.classList.toggle('live', connected);
    dot.classList.toggle('reserved', !connected);
    label.textContent = connected ? 'Connected' : 'Not Configured';
    label.classList.toggle('connected', connected);
    label.classList.toggle('reserved', !connected);
  };
}

async function refreshDashboard() {
  let data;
  try {
    const response = await fetch('/api/dashboard');
    if (!response.ok) throw new Error('Dashboard request failed: ' + response.status);
    data = await response.json();
  } catch (err) {
    document.getElementById('statusPass').textContent = 'Offline';
    document.getElementById('statusFooter').textContent =
      'Could not reach /api/dashboard — is core/applications/api/http_server.py running?';
    return;
  }

  const skills = data.skills || {};
  document.getElementById('statusPass').textContent =
    `${skills.total ?? '—'} SKILLS REGISTERED`;
  document.getElementById('statusFooter').textContent =
    `${skills.builtin ?? '—'} Builtin \u00b7 ${skills.privileged ?? '—'} Privileged`;

  const providers = data.providers || {};
  applyProviderStatus('anthropic', 'Anthropic')(providers.anthropic);
  applyProviderStatus('openai', 'Openai')(providers.openai);
  applyProviderStatus('elevenlabs', 'Elevenlabs')(providers.elevenlabs);

  const pipeline = data.pipeline || {};
  if (typeof pipeline.current_index === 'number') {
    applyPipelineStage(pipeline.current_index);
  }
}

refreshDashboard();
setInterval(refreshDashboard, 5000);