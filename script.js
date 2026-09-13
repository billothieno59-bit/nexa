// Login screen background — rotates through real photography, with
// a matching location caption. Single element + JS crossfade rather
// than 5 stacked CSS keyframe animations, so photo and caption always
// stay in sync, and it's trivial to disable under prefers-reduced-motion.
const loginBg = document.getElementById('loginBg');
const loginLocation = document.getElementById('loginLocation');
const backgroundScenes = [
  { file: 'diani-beach-resort.jpg', caption: 'Diani Beach, Kenya' },
  { file: 'mount-kenya-sunset.jpg', caption: 'Mount Kenya, Kenya' },
  { file: 'lamu-lagoon-island.jpg', caption: 'Lamu, Kenya' },
  { file: 'maasai-mara-acacia-sunset.jpg', caption: 'Maasai Mara, Kenya' },
  { file: 'street-mural-portrait.jpg', caption: 'Street Art, South Africa' },
];

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let bgIndex = 0;

function applyBackgroundScene(index) {
  const scene = backgroundScenes[index];
  loginBg.style.backgroundImage = `url('/assets/${scene.file}')`;
  loginLocation.textContent = scene.caption;
}

applyBackgroundScene(0);

if (!prefersReducedMotion) {
  setInterval(function () {
    bgIndex = (bgIndex + 1) % backgroundScenes.length;
    loginBg.style.opacity = '0';
    loginLocation.style.opacity = '0';
    setTimeout(function () {
      applyBackgroundScene(bgIndex);
      loginBg.style.opacity = '1';
      loginLocation.style.opacity = '1';
    }, 900);
  }, 8000);
}

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

// Real clock.
function updateTime() {
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  document.getElementById('clock').textContent = `${hours}:${minutes}`;
}

updateTime();
setInterval(updateTime, 30000);

// --- Live backend data via GET /api/dashboard ---

const pipelineStages = document.querySelectorAll('.pipeline-stage');

function applyPipelineStage(currentIndex) {
  pipelineStages.forEach((stage, i) => {
    const active = i === currentIndex;
    stage.classList.toggle('active', active);
    stage.querySelector('.stage-dot').classList.toggle('active', active);
  });
}

function applyProviderStatus(elementIdSuffix) {
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
  applyProviderStatus('Anthropic')(providers.anthropic);
  applyProviderStatus('Openai')(providers.openai);
  applyProviderStatus('Elevenlabs')(providers.elevenlabs);

  const pipeline = data.pipeline || {};
  if (typeof pipeline.current_index === 'number') {
    applyPipelineStage(pipeline.current_index);
  }
}

refreshDashboard();
setInterval(refreshDashboard, 5000);

// --- Rail navigation: switch between Home and Skills views ---

const railItems = document.querySelectorAll('.rail-item');
const viewHome = document.getElementById('viewHome');
const viewSkills = document.getElementById('viewSkills');

function showView(viewName) {
  railItems.forEach(item => item.classList.toggle('active', item.dataset.view === viewName));
  viewHome.classList.toggle('hidden-view', viewName !== 'home');
  viewSkills.classList.toggle('hidden-view', viewName !== 'skills');

  if (viewName === 'skills') {
    loadSkillsList();
  }
}

railItems.forEach(item => {
  item.addEventListener('click', () => showView(item.dataset.view));
});

// --- Skills panel: fetch GET /api/skills, run one via POST /api/skills/<id> ---

const skillsListEl = document.getElementById('skillsList');
const skillRunCard = document.getElementById('skillRunCard');
const skillRunTitle = document.getElementById('skillRunTitle');
const skillRunDescription = document.getElementById('skillRunDescription');
const skillRunParams = document.getElementById('skillRunParams');
const skillRunButton = document.getElementById('skillRunButton');
const skillRunCancel = document.getElementById('skillRunCancel');
const skillRunResult = document.getElementById('skillRunResult');

let selectedSkillId = null;

async function loadSkillsList() {
  skillsListEl.textContent = 'Loading…';
  try {
    const response = await fetch('/api/skills');
    if (!response.ok) throw new Error('Skills request failed: ' + response.status);
    const skills = await response.json();

    skillsListEl.innerHTML = '';
    const skillIds = Object.keys(skills).sort();

    if (skillIds.length === 0) {
      skillsListEl.textContent = 'No skills available.';
      return;
    }

    skillIds.forEach(skillId => {
      const row = document.createElement('div');
      row.className = 'skill-run-item';
      row.innerHTML = `<strong>${skillId}</strong><span class="skill-run-item-desc">${skills[skillId]}</span>`;
      row.addEventListener('click', () => openSkillRunCard(skillId, skills[skillId]));
      skillsListEl.appendChild(row);
    });
  } catch (err) {
    skillsListEl.textContent = 'Could not reach /api/skills.';
  }
}

function openSkillRunCard(skillId, description) {
  selectedSkillId = skillId;
  skillRunTitle.textContent = skillId;
  skillRunDescription.textContent = description;
  skillRunParams.value = '';
  skillRunResult.textContent = '';
  skillRunCard.style.display = 'block';
}

// --- Module cards on Home: jump to Skills view and auto-open a skill ---

const moduleCards = document.querySelectorAll('.module-card');

moduleCards.forEach(card => {
  card.addEventListener('click', async () => {
    showView('skills');
    const targetSkill = card.dataset.skill;

    if (!targetSkill) return;

    if (skillsListEl.textContent === 'Loading…' || skillsListEl.children.length === 0) {
      await loadSkillsList();
    }

    const knownSkillIds = Array.from(skillsListEl.querySelectorAll('.skill-run-item strong'))
      .map(el => el.textContent);

    if (knownSkillIds.includes(targetSkill)) {
      const row = Array.from(skillsListEl.querySelectorAll('.skill-run-item'))
        .find(r => r.querySelector('strong').textContent === targetSkill);
      if (row) row.click();
    }
  });
});

skillRunCancel.addEventListener('click', () => {
  skillRunCard.style.display = 'none';
  selectedSkillId = null;
});

skillRunButton.addEventListener('click', async () => {
  if (!selectedSkillId) return;

  let params = {};
  const raw = skillRunParams.value.trim();
  if (raw) {
    try {
      params = JSON.parse(raw);
    } catch (err) {
      skillRunResult.textContent = 'Invalid JSON in parameters.';
      return;
    }
  }

  skillRunResult.textContent = 'Running…';

  try {
    const response = await fetch('/api/skills/' + encodeURIComponent(selectedSkillId), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    const data = await response.json();
    skillRunResult.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    skillRunResult.textContent = 'Request failed: ' + err.message;
  }
});