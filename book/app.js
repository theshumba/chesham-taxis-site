/* ============================================================
   Chesham Taxis — onboarding flow controller
   Mirrors Uber's web onboarding: landing → auth → OTP →
   add-mobile → name → terms → logged-in home.
   Vanilla JS, no build step. Keyless Leaflet/OSM maps.
   ============================================================ */
(() => {
  'use strict';

  const CHESHAM = [51.7055, -0.6118];       // Chesham Broadway, Bucks
  const AMERSHAM = [51.6742, -0.6079];      // dropoff demo
  const DEMO_CODE = '1234';

  const state = { contact: '', isEmail: false, first: '', last: '' };
  const history = [];
  const maps = {};                          // lazy leaflet instances

  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const screens = new Map($$('.screen').map(el => [el.dataset.screen, el]));

  /* ---------------- routing ---------------- */
  function show(name, { push = true } = {}) {
    const el = screens.get(name);
    if (!el) return;
    const current = $('.screen.is-active');
    if (current && current.dataset.screen === name) return;
    if (push && current) history.push(current.dataset.screen);
    if (current) current.classList.remove('is-active');
    el.classList.add('is-active');
    el.querySelector('.scroll')?.scrollTo(0, 0);
    if (location.hash.slice(1) !== name) {
      history.length ? history : 0;
      try { window.history.replaceState({}, '', '#' + name); } catch (e) {}
    }
    onEnter(name);
  }
  function back() {
    const prev = history.pop();
    show(prev || 'landing', { push: false });
  }

  /* ---------------- per-screen hooks ---------------- */
  function onEnter(name) {
    if (name === 'landing')  ensureMap('map-landing', CHESHAM, 14, true);
    if (name === 'ride')     ensureMap('map-ride', CHESHAM, 14, true);
    if (name === 'account')  ensureMap('map-activity', midpoint(CHESHAM, AMERSHAM), 13, false, true);
    if (name === 'otp') {
      $('#otp-target').textContent = state.contact || 'your email';
      resetOtp();
      setTimeout(() => $('.otp__box')?.focus(), 350);
    }
    if (name === 'auth') setTimeout(() => $('#auth-input')?.focus(), 350);
    if (name === 'account') {
      const full = [state.first, state.last].filter(Boolean).join(' ') || 'there';
      $('#welcome-name').textContent = full;
      const initials = ((state.first[0] || 'A') + (state.last[0] || 'S')).toUpperCase();
      $('#account-avatar').textContent = initials;
    }
  }

  /* ---------------- maps ---------------- */
  function midpoint(a, b) { return [(a[0]+b[0])/2, (a[1]+b[1])/2]; }
  function pinIcon(color) {
    return L.divIcon({
      className: '', iconSize: [26, 34], iconAnchor: [13, 32],
      html: `<svg class="pin" viewBox="0 0 26 34" width="26" height="34"><path d="M13 0C6 0 .5 5.4.5 12.2.5 21 13 34 13 34s12.5-13 12.5-21.8C25.5 5.4 20 0 13 0z" fill="${color}"/><circle cx="13" cy="12" r="4.6" fill="#fff"/></svg>`
    });
  }
  function ensureMap(id, center, zoom, pin, route) {
    if (maps[id]) { setTimeout(() => maps[id].invalidateSize(), 60); return; }
    const node = document.getElementById(id);
    if (!node || typeof L === 'undefined') return;
    const map = L.map(node, { zoomControl: pin, attributionControl: true, dragging: true, scrollWheelZoom: false }).setView(center, zoom);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '© OpenStreetMap · © CARTO', maxZoom: 19, subdomains: 'abcd'
    }).addTo(map);
    if (pin) L.marker(center, { icon: pinIcon('#df4510') }).addTo(map);
    if (route) {
      L.marker(CHESHAM, { icon: pinIcon('#14181b') }).addTo(map);
      L.marker(AMERSHAM, { icon: pinIcon('#df4510') }).addTo(map);
      L.polyline([CHESHAM, AMERSHAM], { color: '#14181b', weight: 3, opacity: .85 }).addTo(map);
      map.fitBounds([CHESHAM, AMERSHAM], { padding: [34, 34] });
    }
    maps[id] = map;
    setTimeout(() => map.invalidateSize(), 120);
  }

  /* ---------------- generic nav wiring ---------------- */
  $$('[data-goto]').forEach(b => b.addEventListener('click', () => {
    if (b.dataset.mode) state.mode = b.dataset.mode;
    show(b.dataset.goto);
  }));
  $$('[data-back]').forEach(b => b.addEventListener('click', back));

  /* landing: service tabs */
  $$('.tab').forEach(t => t.addEventListener('click', () => {
    $$('.tab').forEach(x => { x.classList.remove('is-selected'); x.setAttribute('aria-selected', 'false'); });
    t.classList.add('is-selected'); t.setAttribute('aria-selected', 'true');
  }));

  /* ---------------- AUTH screen ---------------- */
  const authInput = $('#auth-input');
  const authField = $('#auth-field');
  const authError = $('#auth-error');
  function clearAuthError() { authError.hidden = true; authField.classList.remove('is-error'); }
  function setAuthError(msg) { authError.textContent = msg; authError.hidden = false; authField.classList.add('is-error'); }
  authInput.addEventListener('input', clearAuthError);
  $('#auth-continue').addEventListener('click', () => {
    const v = authInput.value.trim();
    if (!v) { setAuthError('Please enter a mobile number or email'); return; }
    // demo "blocked" branch, mirroring Uber's blocked-number state
    if (/^0*$/.test(v.replace(/\D/g, '')) && /\d/.test(v)) {
      setAuthError('The number you entered is blocked. Choose another option to continue.'); return;
    }
    state.isEmail = v.includes('@');
    state.contact = v;
    clearAuthError();
    show('otp');
  });

  /* ---------------- OTP screen ---------------- */
  const otpWrap = $('#otp-inputs');
  const otpBoxes = $$('.otp__box', otpWrap);
  const otpNext = $('#otp-next');
  const otpError = $('#otp-error');
  function otpValue() { return otpBoxes.map(b => b.value).join(''); }
  function resetOtp() {
    otpBoxes.forEach(b => b.value = '');
    otpWrap.classList.remove('is-error'); otpError.hidden = true; otpNext.disabled = true;
  }
  otpBoxes.forEach((box, i) => {
    box.addEventListener('input', () => {
      box.value = box.value.replace(/\D/g, '').slice(0, 1);
      otpWrap.classList.remove('is-error'); otpError.hidden = true;
      if (box.value && i < otpBoxes.length - 1) otpBoxes[i + 1].focus();
      otpNext.disabled = otpValue().length !== 4;
    });
    box.addEventListener('keydown', e => {
      if (e.key === 'Backspace' && !box.value && i > 0) otpBoxes[i - 1].focus();
    });
  });
  otpNext.addEventListener('click', () => {
    if (otpValue() !== DEMO_CODE) {
      otpWrap.classList.add('is-error'); otpError.hidden = false; return;
    }
    show('mobile');
  });
  $('#otp-resend').addEventListener('click', function () {
    const t = this.textContent; this.textContent = 'Sent ✓';
    setTimeout(() => (this.textContent = t), 1600);
  });

  /* ---------------- NAME screen ---------------- */
  const first = $('#name-first'), last = $('#name-last'), nameNext = $('#name-next');
  function checkName() { nameNext.disabled = !(first.value.trim() && last.value.trim()); }
  first.addEventListener('input', checkName);
  last.addEventListener('input', checkName);
  nameNext.addEventListener('click', () => {
    state.first = first.value.trim(); state.last = last.value.trim();
    show('terms');
  });

  /* ---------------- TERMS screen ---------------- */
  const termsCheck = $('#terms-check'), termsNext = $('#terms-next');
  termsCheck.addEventListener('change', () => termsNext.disabled = !termsCheck.checked);
  termsNext.addEventListener('click', () => show('account'));

  /* ---------------- misc ---------------- */
  $('#ride-search').addEventListener('click', function () {
    const t = this.textContent; this.textContent = 'Finding your driver…';
    this.disabled = true;
    setTimeout(() => { this.textContent = t; this.disabled = false; }, 1800);
  });
  $$('[data-locate]').forEach(b => b.addEventListener('click', e => {
    e.preventDefault();
    const inp = b.closest('.field')?.querySelector('input');
    if (inp) inp.value = 'Current location';
  }));
  $('#proto-reset').addEventListener('click', () => {
    Object.assign(state, { contact: '', isEmail: false, first: '', last: '' });
    authInput.value = ''; clearAuthError();
    first.value = ''; last.value = ''; checkName();
    termsCheck.checked = false; termsNext.disabled = true;
    history.length = 0;
    show('landing', { push: false });
  });

  /* ---------------- boot ---------------- */
  const start = location.hash.slice(1);
  show(screens.has(start) && start ? start : 'landing', { push: false });
})();
