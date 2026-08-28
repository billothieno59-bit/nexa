# NEXA Change Log

Every change made to this project, in order, so any builder can see
what exists and why without reconstructing it from git log. Newest
entry at the top. Each entry lists exactly what changed and in which
files, verified against the actual file contents at time of writing.

---

## 2026-08-27 — Removed leftover Vite/React/Tailwind tooling

**What changed:** `src/` (the old React version) had already been
deleted in a prior commit, but its supporting build tooling was still
present at the project root and in `node_modules/`. Removed all of it
since `web/`-style plain HTML/CSS/JS (`index.html`, `style.css`,
`script.js` at project root) is the sole frontend and needs no build
step.

**Files removed:**
- `package.json`
- `package-lock.json`
- `postcss.config.js`
- `tailwind.config.js`
- `vite.config.ts`
- `node_modules/` (entire directory, ~125 MB)

**Verified:** `python -m pytest` — 308 tests passed, confirming the
Python test suite has no dependency on any of the removed JS tooling.

---

## 2026-08-27 — Login screen: tropical leaves + sunrise edge lighting

**What changed:** Added two SVG monstera-leaf silhouettes (top-left,
bottom-right) with a slow independent sway animation to `#loginScreen`,
and strengthened the warm gold radial glow along the bottom edge to
read as a "sunrise." Both leaves disabled under
`prefers-reduced-motion`.

**Files touched:**
- `index.html` (two `.login-leaf` divs added to `#loginScreen`)
- `style.css` (`.login-leaf`, `.leaf-tl`, `.leaf-br`, `leafSwayA`/
  `leafSwayB` keyframes added; `#loginScreen` background gradient
  strengthened)

---

## 2026-08-27 — Login orb upgraded: glass sphere with internal swirl

**What changed:** Replaced the flat gradient-circle login orb with a
layered glass-sphere effect closer to a reference "bioluminescent
orb" image: two rotating conic-gradient swirl layers (blurred,
screen-blended), two soft highlight patches, and a multi-layer
`box-shadow` glow halo.

**Files touched:**
- `index.html` (`.login-orb-swirl` x2 and `.login-orb-highlight` x2
  divs added inside `.login-orb`)
- `style.css` (`.login-orb` background/box-shadow rewritten;
  `.login-orb-swirl`, `.login-orb-highlight` and `swirlSpin` keyframe
  added)

---

## 2026-08-27 — Login screen added

**What changed:** Added a full-screen login/welcome overlay shown on
page load, dismissed by clicking "Enter NEXA" or pressing any key.
Shows "Welcome back, Admin." with a pulsing orb.

**Files touched:**
- `index.html` (`#loginScreen` markup added before `#app`)
- `style.css` (`#loginScreen` and related classes added)
- `script.js` (dismiss-on-click / dismiss-on-keydown logic added)

**Note:** the name shown is currently hardcoded as "Admin" (matches
the header's existing profile chip). Not dynamic, not sourced from
any config file.

---

## 2026-08-27 — Subtle geometric card pattern added

**What changed:** Added a repeating low-opacity (4%) SVG
diamond-and-circle pattern as a `::before` overlay on all `.glass-card`
elements, per the "African materials, subtle geometric patterns"
design direction.

**Files touched:**
- `style.css` (`.glass-card` given `position: relative; overflow: hidden`,
  `.glass-card::before` pattern layer added, `.glass-card > *` raised
  to `z-index: 1`)

---

## 2026-08-27 — Tropical Afrofuture palette applied

**What changed:** Replaced the prior dark-violet/neon-cyan color
scheme with a tropical palette per design direction: Deep Ocean
`#07131F`, Palm Emerald `#0F2A25`, Tropical Mint `#22D3A6`, Sunset
Gold `#C68A2B`, Walnut `#8B5E3C`, Ivory `#F5F7F4`.

- `--violet` repurposed to Walnut (`#8B5E3C`) rather than removed —
  still used for the orb's "Thinking" state.
- `--cyan` set equal to Tropical Mint (`#22D3A6`), since the palette
  has no distinct cyan — gradients that previously blended emerald+cyan
  now render as a single mint tone.
- Background radial gradient's dark accent changed from `#17204a`
  (navy-purple) to `#0F2A25` (Palm Emerald).
- Orb's four states (Idle/Listening/Thinking/Speaking) recolored to
  match — Thinking now uses Walnut instead of the prior violet.

**Not changed:** typography (still Space Grotesk / Inter / JetBrains
Mono — no font swap was made), and the header's "Admin" chip (still
reads "Admin", not renamed).

**Files touched:**
- `style.css` (`:root` color tokens, background gradient, orb-related
  colors)
- `script.js` (`orbStates` array hex values)

**Verified:** 308/308 tests passed after this change (CSS/JS-only,
no Python touched).

---

## Earlier history (before this log started)

Everything before 2026-08-27 predates this file and is tracked only
in git history: the governed execution pipeline, the Universal
Layers, the full builtin + privileged skills catalog, the provider
abstractions, and the original React (`src/`) frontend that was later
replaced by the plain HTML/CSS/JS version at project root.