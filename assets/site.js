/* The Brue Yard: shared site behaviour. Each feature starts only when its markup is on the page. */
(() => {
  "use strict";
  /* ---------- Helpers ---------- */
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const money = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" });
  const day0 = d => { const x = new Date(d); x.setHours(0,0,0,0); return x; };
  const D = (y, m, d) => new Date(y, m - 1, d);
  const addDays = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };
  const sameDay = (a, b) => a.getTime() === b.getTime();
  const iso = d => `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")}`;
  const fmt = (d, o) => d.toLocaleDateString("en-GB", o);
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  const TODAY = day0(new Date());

  function days(from, to, dows, skip = []) {
    const out = [];
    for (let x = new Date(from); x <= to; x = addDays(x, 1)) {
      if (dows && !dows.includes(x.getDay())) continue;
      if (skip.includes(iso(x))) continue;
      out.push(new Date(x));
    }
    return out;
  }
  const BY = window.BY || {};
  const ROOT = document.documentElement.dataset.root || "";
  const ISO = s => { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d); };
  const EXTRA = BY.extra || {}, PHOTOS = BY.photos || {}, CLOSED = BY.closed || [];
  const END = ISO(BY.seasonEnd || "2027-02-28");

  /* ---------- Data ---------- */
  const ACCESS = {
    stepfree: { label: "Step-free", icon: '<svg viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="2" r="1.5"/><path d="M4 4h3v3h2.5L11 10.5 10 11 8.8 8.5H5.5a1.5 1.5 0 0 1-1.5-1.5z"/></svg>' },
    bsl: { label: "BSL interpreted", icon: '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 11V5l1-3 1 3V1.5l1 .2V5l1-3.5 1 .3L7.5 6 10 4.5l.7.7L7 9.5V11z"/></svg>' },
    relaxed: { label: "Relaxed", icon: '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M6 1a5 5 0 1 0 0 10A5 5 0 0 0 6 1zm-2 3.5a.8.8 0 1 1 0 1.6.8.8 0 0 1 0-1.6zm4 0a.8.8 0 1 1 0 1.6.8.8 0 0 1 0-1.6zM3.6 7.4h4.8A2.6 2.6 0 0 1 6 9a2.6 2.6 0 0 1-2.4-1.6z"/></svg>' },
    audio: { label: "Audio described", icon: '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M1 4.5h2L6 2v8L3 7.5H1zM8 3.5a3.5 3.5 0 0 1 0 5l-.7-.7a2.5 2.5 0 0 0 0-3.6zm1.5-1.5a5.6 5.6 0 0 1 0 8l-.7-.7a4.6 4.6 0 0 0 0-6.6z"/></svg>' }
  };
  const CATS = [
    { id: "all", label: "All" },
    { id: "exhibition", label: "Exhibitions", eyebrow: "Exhibition" },
    { id: "performance", label: "Performances", eyebrow: "Performance · Music" },
    { id: "workshop", label: "Workshops", eyebrow: "Workshop · Family" },
    { id: "walk", label: "Outdoor Walks", eyebrow: "Outdoor · Tour" },
    { id: "talk", label: "Talks", eyebrow: "Talk · Lecture" }
  ];
  const EVENTS = (BY.events || []).map(e => ({ ...e,
    url: ROOT + "events/" + e.slug + ".html",
    dates: e.dates ? e.dates.map(ISO) : days(ISO(e.from), ISO(e.to), e.dows || null, e.skipClosed ? CLOSED : []) }));
  EVENTS.forEach(e => e.upcoming = e.dates.filter(d => d >= TODAY));
  const LIVE = EVENTS.filter(e => e.upcoming.length);

  /* ---------- Photo fallback ---------- */
  const markMissing = im => { const f = im.closest(".ph"); f && f.classList.add("is-missing"); };
  document.addEventListener("error", e => { if (e.target.tagName === "IMG") markMissing(e.target); }, true);
  const sweep = () => $$(".ph img").forEach(im => { if (im.complete && im.naturalWidth === 0) markMissing(im); });
  window.addEventListener("load", sweep);

  /* ---------- Topographic plate ---------- */
  const canvas = $("#topo");
  if (canvas) {
  function drawTopo() {
    const r = canvas.getBoundingClientRect();
    if (!r.width) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(r.width * dpr); canvas.height = Math.round(r.height * dpr);
    const ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const W = r.width, H = r.height;
    const cs = getComputedStyle(document.documentElement);
    const c1 = cs.getPropertyValue("--contour").trim(), c2 = cs.getPropertyValue("--contour-index").trim();
    const river = cs.getPropertyValue("--river").trim(), ink = cs.getPropertyValue("--ink").trim(), surf = cs.getPropertyValue("--surface").trim();
    ctx.clearRect(0, 0, W, H);
    const ry = x => H * (0.58 + 0.09 * Math.sin((x / W) * Math.PI * 2.1 + 0.7) + 0.03 * Math.sin((x / W) * 9));
    const f = (x, y) => {
      const d = Math.abs(y - ry(x)) / H;
      const hill = 34 * Math.exp(-(((x - W * 0.28) / (W * 0.22)) ** 2 + ((y - H * 0.18) / (H * 0.16)) ** 2));
      const hill2 = 22 * Math.exp(-(((x - W * 0.8) / (W * 0.2)) ** 2 + ((y - H * 0.92) / (H * 0.14)) ** 2));
      return 58 + 150 * Math.pow(d, 0.95) + hill + hill2 + 7 * Math.sin(x * 0.019 + y * 0.011) + 5 * Math.cos(x * 0.031 - y * 0.023);
    };
    const step = 5, cols = Math.ceil(W / step) + 1, rows = Math.ceil(H / step) + 1;
    const v = new Float32Array(cols * rows);
    for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) v[j * cols + i] = f(i * step, j * step);
    const labels = [];
    for (let L = 60; L <= 200; L += 10) {
      const major = L % 50 === 0;
      ctx.beginPath(); ctx.strokeStyle = major ? c2 : c1; ctx.lineWidth = major ? 1.1 : 0.7;
      let labelPt = null;
      for (let j = 0; j < rows - 1; j++) for (let i = 0; i < cols - 1; i++) {
        const a = v[j*cols+i], b = v[j*cols+i+1], c = v[(j+1)*cols+i+1], d = v[(j+1)*cols+i];
        const k = (a > L ? 8 : 0) | (b > L ? 4 : 0) | (c > L ? 2 : 0) | (d > L ? 1 : 0);
        if (k === 0 || k === 15) continue;
        const x = i * step, y = j * step;
        const T = [x + step * (L - a) / (b - a), y], R = [x + step, y + step * (L - b) / (c - b)];
        const B = [x + step * (L - d) / (c - d), y + step], Lf = [x, y + step * (L - a) / (d - a)];
        const seg = (p, q) => { ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); if (major && !labelPt && p[0] > W * 0.06 && p[0] < W * 0.2) labelPt = p; };
        switch (k) {
          case 1: case 14: seg(Lf, B); break;
          case 2: case 13: seg(B, R); break;
          case 3: case 12: seg(Lf, R); break;
          case 4: case 11: seg(T, R); break;
          case 5: seg(Lf, T); seg(B, R); break;
          case 6: case 9: seg(T, B); break;
          case 7: case 8: seg(Lf, T); break;
          case 10: seg(T, R); seg(Lf, B); break;
        }
      }
      ctx.stroke();
      if (labelPt) labels.push([labelPt, L]);
    }
    // river
    ctx.beginPath(); ctx.strokeStyle = river; ctx.lineWidth = 2.4; ctx.lineCap = "round";
    for (let x = 0; x <= W; x += 3) { const y = ry(x); x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    ctx.stroke();
    ctx.font = "500 10px 'IBM Plex Mono', monospace"; ctx.textBaseline = "middle";
    labels.forEach(([p, L]) => { const t = `${L}`; const w = ctx.measureText(t).width; ctx.fillStyle = surf; ctx.fillRect(p[0] - 2, p[1] - 6, w + 4, 12); ctx.fillStyle = c2; ctx.fillText(t, p[0], p[1]); });
    // commission sites
    const marks = [];
    [0.18, 0.42, 0.63, 0.86].forEach((t, n) => {
      const x = W * t, y = ry(x) + (n % 2 ? 14 : -14); marks.push([x, y]);
      ctx.fillStyle = ink; ctx.fillRect(x - 4, y - 4, 8, 8);
      ctx.fillStyle = ink; ctx.font = "500 11px 'IBM Plex Mono', monospace";
      ctx.fillText(`N${n + 1}`, x + 8, y);
    });
    ctx.fillStyle = river; ctx.font = "italic 13px Newsreader, Georgia, serif";
    ctx.fillText("River Brue", W * 0.52, ry(W * 0.52) + 22);
    // scale bar
    ctx.fillStyle = ink; ctx.fillRect(16, H - 22, 60, 2); ctx.fillRect(16, H - 26, 1, 8); ctx.fillRect(75, H - 26, 1, 8);
    ctx.font = "500 10px 'IBM Plex Mono', monospace"; ctx.fillText("200 m", 82, H - 21);
    // north
    ctx.fillText("N ↑", W - 36, 18);
    topo = { snap: ctx.getImageData(0, 0, canvas.width, canvas.height), ry, W, H, dpr, surf, marks, ochre: river, ink };
    paintTopo(performance.now());
  }
  let commActive = -1;
  function overlay(ctx, now) {
    if (!topo || commActive < 0) return;
    const [x, y] = topo.marks[commActive];
    const pulse = topoOn ? 3 * Math.sin(now / 260) : 0;
    ctx.save();
    ctx.strokeStyle = topo.ochre; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(x, y, 14 + pulse, 0, Math.PI * 2); ctx.stroke();
    ctx.globalAlpha = .35; ctx.beginPath(); ctx.arc(x, y, 22 + pulse * 1.6, 0, Math.PI * 2); ctx.stroke();
    ctx.globalAlpha = 1; ctx.fillStyle = topo.ochre; ctx.fillRect(x - 5, y - 5, 10, 10);
    ctx.restore();
  }
  function paintTopo(now) {
    if (!topo) return;
    const ctx = canvas.getContext("2d");
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.putImageData(topo.snap, 0, 0);
    ctx.setTransform(topo.dpr, 0, 0, topo.dpr, 0, 0);
    overlay(ctx, now);
  }
  let topo = null, topoOn = false, topoRaf = 0, topoT = 0;
  function flow(now) {
    if (!topo || !topoOn) return;
    const ctx = canvas.getContext("2d");
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.putImageData(topo.snap, 0, 0);
    ctx.setTransform(topo.dpr, 0, 0, topo.dpr, 0, 0);
    ctx.save(); ctx.beginPath();
    for (let x = 0; x <= topo.W; x += 3) { const y = topo.ry(x); x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    ctx.setLineDash([3, 22]); ctx.lineDashOffset = -now / 60; ctx.strokeStyle = topo.surf; ctx.globalAlpha = .9; ctx.lineWidth = 1.4; ctx.lineCap = "round"; ctx.stroke();
    ctx.restore();
    overlay(ctx, now);
    topoRaf = requestAnimationFrame(flow);
  }
  if ("IntersectionObserver" in window) new IntersectionObserver(es => es.forEach(en => {
    topoOn = en.isIntersecting && !reduced.matches; cancelAnimationFrame(topoRaf);
    if (topoOn) topoRaf = requestAnimationFrame(flow);
  })).observe(canvas);
  if ("ResizeObserver" in window) new ResizeObserver(() => drawTopo()).observe(canvas);
  $$("[data-comm]").forEach(b => b.addEventListener("click", () => {
    const i = +b.dataset.comm; commActive = commActive === i ? -1 : i;
    $$("[data-comm]").forEach(o => o.setAttribute("aria-pressed", String(+o.dataset.comm === commActive)));
    $("#comm-live").textContent = commActive < 0 ? "" : `N${commActive + 1} is marked on the map in terracotta.`;
    if (!topoOn) paintTopo(performance.now());
    if (matchMedia("(max-width:860px)").matches && commActive >= 0) canvas.scrollIntoView({ behavior: reduced.matches ? "auto" : "smooth", block: "center" });
  }));
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => drawTopo());
  new MutationObserver(() => drawTopo()).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  document.fonts && document.fonts.ready.then(drawTopo);
  }

  /* ---------- Modal plumbing (inert background + focus trap) ---------- */
  const page = $("#page");
  let lastFocus = null, openModal = null;
  const focusables = el => $$('a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),[tabindex]:not([tabindex="-1"])', el)
    .filter(n => n.getClientRects().length && !n.closest("[hidden]"));
  function showModal(el, onShown, extra) {
    lastFocus = document.activeElement;
    openModal = el;
    el.hidden = false; if (extra) extra.hidden = false;
    page.inert = true; document.body.style.overflow = "hidden";
    requestAnimationFrame(() => requestAnimationFrame(() => { el.classList.add("is-open"); extra && extra.classList.add("is-open"); onShown && onShown(); }));
  }
  function hideModal(el, extra, after) {
    el.classList.remove("is-open"); extra && extra.classList.remove("is-open");
    const done = () => { el.hidden = true; if (extra) extra.hidden = true; page.inert = false; document.body.style.overflow = ""; openModal = null; after && after(); lastFocus && lastFocus.focus && lastFocus.focus(); };
    reduced.matches ? done() : setTimeout(done, 320);
  }
  document.addEventListener("keydown", e => {
    if (!openModal) return;
    if (e.key === "Escape") { e.preventDefault(); openModal === drawer ? closeBooking() : closeMenu(); return; }
    if (e.key !== "Tab") return;
    const f = focusables(openModal); if (!f.length) return;
    const first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  /* ---------- Mobile menu ---------- */
  const menu = $("#mobile-menu"), menuBtn = $("#menu-trigger");
  function openMenu() { menuBtn.setAttribute("aria-expanded", "true"); showModal(menu, () => $("#menu-close").focus()); }
  function closeMenu(after) { menuBtn.setAttribute("aria-expanded", "false"); hideModal(menu, null, after); }
  menuBtn.addEventListener("click", openMenu);
  $("#menu-close").addEventListener("click", () => closeMenu());
  $$(".menu__list a", menu).forEach(a => a.addEventListener("click", e => {
    const id = a.getAttribute("href"); if (!id.startsWith("#") || !$(id)) return;
    e.preventDefault();
    lastFocus = null;
    closeMenu(() => { const t = $(id); t.scrollIntoView({ behavior: reduced.matches ? "auto" : "smooth" }); t.setAttribute("tabindex", "-1"); t.focus({ preventScroll: true }); });
  }));

  /* ---------- What's On filters ---------- */
  const state = { date: "all", cat: "all", access: new Set(), view: "grid" };
  try { const v = localStorage.getItem("brue-view"); if (v === "list" || v === "grid") state.view = v; } catch (e) {}

  function dateRange(key) {
    if (key === "today") return [TODAY, TODAY];
    if (key === "weekend") {
      const dow = TODAY.getDay();
      if (dow === 6) return [TODAY, addDays(TODAY, 1)];
      if (dow === 0) return [TODAY, TODAY];
      const sat = addDays(TODAY, 6 - dow); return [sat, addDays(sat, 1)];
    }
    if (key === "month") return [TODAY, addDays(TODAY, 30)];
    return [TODAY, END];
  }
  const inRange = (e, [a, b]) => e.upcoming.filter(d => d >= a && d <= b);
  function matches(e, ignoreCat) {
    if (!ignoreCat && state.cat !== "all" && e.cat !== state.cat) return false;
    for (const a of state.access) if (!e.access.includes(a)) return false;
    return inRange(e, dateRange(state.date)).length > 0;
  }

  const catWrap = $("#cat-filter");
  const hasProgramme = !!(catWrap && $("#events"));
  try { const q = new URLSearchParams(location.search);
    if (CATS.some(c => c.id === q.get("cat"))) state.cat = q.get("cat");
    if (["all", "today", "weekend", "month"].includes(q.get("date"))) state.date = q.get("date"); } catch (e) {}
  if (hasProgramme) {
  catWrap.innerHTML = CATS.map(c => `<button type="button" role="tab" id="tab-${c.id}" data-cat="${c.id}" aria-selected="${c.id === "all"}" aria-controls="events" tabindex="${c.id === "all" ? 0 : -1}">${c.label}<span class="n"></span></button>`).join("");
  catWrap.addEventListener("click", e => { const b = e.target.closest("[data-cat]"); if (b) { state.cat = b.dataset.cat; render(); } });
  catWrap.addEventListener("keydown", e => {
    const tabs = $$("[role=tab]", catWrap); const i = tabs.indexOf(document.activeElement);
    if (i < 0) return;
    let n = null;
    if (e.key === "ArrowRight") n = (i + 1) % tabs.length;
    if (e.key === "ArrowLeft") n = (i - 1 + tabs.length) % tabs.length;
    if (e.key === "Home") n = 0; if (e.key === "End") n = tabs.length - 1;
    if (n !== null) { e.preventDefault(); tabs[n].focus(); state.cat = tabs[n].dataset.cat; render(); }
  });
  $("#date-filter").addEventListener("click", e => { const b = e.target.closest("[data-date]"); if (b) { state.date = b.dataset.date; render(); } });
  $$("#access-filter input").forEach(i => i.addEventListener("change", () => { i.checked ? state.access.add(i.value) : state.access.delete(i.value); render(); }));
  $$(".view-toggle button").forEach(b => b.addEventListener("click", () => { state.view = b.dataset.view; try { localStorage.setItem("brue-view", state.view); } catch (e) {} render(); }));
  $("#clear-filters").addEventListener("click", () => {
    state.date = "all"; state.cat = "all"; state.access.clear();
    $$("#access-filter input").forEach(i => i.checked = false);
    render(); $("#tab-all").focus();
  });
  }

  const esc = s => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function nextLabel(e) {
    const hits = inRange(e, dateRange(state.date)); const d = hits[0];
    if (!d) return { text: "", today: false };
    const today = sameDay(d, TODAY);
    const base = today ? "Today" : fmt(d, { weekday: "short", day: "numeric", month: "short" }).replace(",", "");
    return { text: (state.date === "all" ? (today ? "Today" : "Next: " + base) : base) + (state.date !== "all" && hits.length > 1 ? ` + ${hits.length - 1} more` : ""), today };
  }
  function phSrc(id, w, r) { return `https://images.unsplash.com/${id}?auto=format&fit=crop&w=${w}&h=${Math.round(w * r)}&q=72`; }
  function photoFrame(e) {
    const p = PHOTOS[e.photo]; if (!p) return "";
    const set = [400, 640, 960, 1280].map(w => `${phSrc(p.id, w, 2 / 3)} ${w}w`).join(", ");
    return `<figure class="ph ph--3x2" data-alt="${esc(e.title)}"><img src="${phSrc(p.id, 960, 2 / 3)}" srcset="${set}" sizes="(max-width: 820px) 100vw, 33vw" width="960" height="640" alt="${esc(p.alt)}" loading="lazy" decoding="async"></figure>`;
  }
  const shortDate = d => fmt(d, { weekday: "short", day: "numeric", month: "short" }).replace(",", "");
  function card(e, i) {
    const cat = CATS.find(c => c.id === e.cat); const n = nextLabel(e); const x = EXTRA[e.id] || {};
    const chips = e.access.map(a => `<li class="chip">${ACCESS[a].icon}${ACCESS[a].label}</li>`).join("");
    const [p1, p2] = e.price.split(" · ");
    const dates = inRange(e, dateRange(state.date)).slice(0, 4).map(d =>
      `<li><button type="button" class="date-pill" data-book="${e.id}" data-date="${iso(d)}" aria-label="Book ${esc(e.title)} on ${fmt(d, { weekday: "long", day: "numeric", month: "long" })}">${sameDay(d, TODAY) ? "Today" : shortDate(d)}</button></li>`).join("");
    const credit = PHOTOS[e.photo] ? `<p class="credit">Photo: <a href="${PHOTOS[e.photo].href}" target="_blank" rel="noopener">${esc(PHOTOS[e.photo].who)}</a> / Unsplash</p>` : "";
    return `<li class="event" data-id="${e.id}" style="--i:${i}">
      <div class="event__flip">
        <article class="face face--front" aria-labelledby="ev-${e.id}">
          ${photoFrame(e)}
          <div class="event__date"><span class="eyebrow eyebrow--accent">${cat.eyebrow}</span><span class="event__next${n.today ? " is-today" : ""}">${n.text}</span></div>
          <div class="event__body">
            <h3 id="ev-${e.id}"><a class="event__link" href="${e.url}">${esc(e.title)}</a></h3>
            <p class="event__desc">${esc(e.desc)}</p>
            <dl class="event__facts"><dt>When</dt><dd>${esc(e.when)}</dd><dt>Where</dt><dd>${esc(e.where)}</dd></dl>
            <ul class="chips" aria-label="Access">${chips}</ul>
            ${credit}
          </div>
          <div class="event__foot"><span class="price"><b>${p1}</b> · ${p2}</span>
            <span class="event__actions">
              <button type="button" class="flip-btn" data-flip aria-expanded="false" aria-controls="evb-${e.id}">More info <svg viewBox="0 0 14 14" aria-hidden="true"><path d="M2.5 6A4.5 4.5 0 0 1 11 4.5M11.5 8A4.5 4.5 0 0 1 3 9.5"/><path d="M11 1.5v3H8M3 12.5v-3h3"/></svg><span class="sr-only"> about ${esc(e.title)}</span></button>
              <button type="button" class="btn btn--sm" data-book="${e.id}" aria-label="Book ${esc(e.title)}">Book</button>
            </span>
          </div>
        </article>
        <article class="face face--back" id="evb-${e.id}" aria-labelledby="evb-t-${e.id}" aria-hidden="true" inert>
          <div class="back__top">
            <div><p class="eyebrow">${cat.eyebrow}</p><h3 id="evb-t-${e.id}" tabindex="-1">${esc(e.title)}</h3></div>
            <button type="button" class="back__close" data-unflip aria-label="Back to summary of ${esc(e.title)}"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13"/></svg></button>
          </div>
          <p class="back__more">${esc(x.more || e.desc)}</p>
          <dl class="back__facts">
            <dt>Length</dt><dd>${esc(x.duration || "")}</dd>
            <dt>Suits</dt><dd>${esc(x.suitable || "")}</dd>
            <dt>Bring</dt><dd>${esc(x.bring || "")}</dd>
            <dt>Access</dt><dd>${esc(x.accessnote || "")}</dd>
          </dl>
          ${dates ? `<div class="back__dates"><p>Choose a date</p><ul>${dates}</ul></div>` : ""}
          <a class="back__page" href="${e.url}">Full event details →</a>
          <div class="event__foot"><span class="price"><b>${p1}</b> · ${p2}</span>
            <button type="button" class="btn btn--sm" data-book="${e.id}" aria-label="Book ${esc(e.title)}">Book</button></div>
        </article>
      </div>
    </li>`;
  }
  function flip(li, on, focus = true) {
    if (!li) return;
    li.classList.toggle("is-flipped", on);
    const front = $(".face--front", li), back = $(".face--back", li), btn = $("[data-flip]", li);
    front.inert = on; back.inert = !on;
    on ? front.setAttribute("aria-hidden", "true") : front.removeAttribute("aria-hidden");
    on ? back.removeAttribute("aria-hidden") : back.setAttribute("aria-hidden", "true");
    btn.setAttribute("aria-expanded", String(on));
    if (focus) setTimeout(() => (on ? $("h3", back) : btn).focus({ preventScroll: true }), reduced.matches ? 0 : 380);
  }
  document.addEventListener("click", e => {
    const f = e.target.closest("[data-flip]"); if (f) { const li = f.closest(".event"); $$(".event.is-flipped").forEach(o => o !== li && flip(o, false, false)); flip(li, true); return; }
    const u = e.target.closest("[data-unflip]"); if (u) flip(u.closest(".event"), false);
  });
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !openModal) { const li = e.target.closest(".event.is-flipped"); if (li) { e.stopPropagation(); flip(li, false); } } });

  /* Upcoming occurrences across the programme, used by the ticker and the filler tile */
  function upcoming(limit, range, perEvent = 1) {
    const [a, b] = range || [TODAY, END];
    const all = [];
    LIVE.forEach(e => e.upcoming.forEach(d => { if (d >= a && d <= b) all.push({ e, d }); }));
    all.sort((p, q) => p.d - q.d || p.e.title.localeCompare(q.e.title));
    const count = {}, out = [];
    for (const o of all) { const n = count[o.e.id] || 0; if (n >= perEvent) continue; count[o.e.id] = n + 1; out.push(o); if (out.length >= limit) break; }
    return out;
  }
  const occButton = (o, cls = "") => `<button type="button" class="${cls}" data-book="${o.e.id}" data-date="${iso(o.d)}"><span class="d">${sameDay(o.d, TODAY) ? "Today" : shortDate(o.d)}</span><span class="t">${esc(o.e.title)}</span><span class="go" aria-hidden="true">Book →</span></button>`;

  let tileDay = null;
  function fillGap(list, shown) {
    const old = $(".filler", list);
    const cols = getComputedStyle(list).gridTemplateColumns.split(" ").filter(Boolean).length;
    const key = `${cols}|${shown.length}|${state.date}|${state.view}`;
    if (old && old.dataset.key === key) return;
    old && old.remove();
    if (state.view !== "grid" || !shown.length) return;
    const rem = shown.length % cols; if (cols < 2 || rem === 0) return;
    const span = cols - rem;
    const nDays = span > 1 ? 14 : 7;
    const days = Array.from({ length: nDays }, (_, i) => addDays(TODAY, i));
    const onDay = d => LIVE.filter(e => e.upcoming.some(x => sameDay(x, d)));
    if (tileDay && !days.some(d => iso(d) === tileDay)) tileDay = null;
    const li = document.createElement("li");
    li.dataset.key = key;
    li.className = "filler"; li.style.gridColumn = `span ${span}`; li.style.setProperty("--fcols", span > 1 ? 2 : 1);
    const draw = () => {
      let items, eyebrow, heading;
      if (tileDay) {
        const d = new Date(tileDay + "T00:00:00");
        items = onDay(d).map(e => ({ e, d }));
        eyebrow = sameDay(d, TODAY) ? "Today" : fmt(d, { weekday: "long" });
        heading = `On ${sameDay(d, TODAY) ? "today" : shortDate(d)}`;
      } else {
        items = upcoming(span > 1 ? 8 : 5, dateRange(state.date));
        eyebrow = state.date === "all" ? "Next at the Yard" : "Also in these dates";
        heading = "Pick a date and go";
      }
      const cells = days.map(d => {
        const n = onDay(d).length, v = iso(d);
        const label = `${fmt(d, { weekday: "long", day: "numeric", month: "long" })}: ${n ? n + (n > 1 ? " events" : " event") : "nothing on"}`;
        return `<button type="button" class="day${sameDay(d, TODAY) ? " is-today" : ""}" data-day="${v}" aria-pressed="${tileDay === v}" aria-label="${label}" ${n ? "" : "disabled"}>
          <span class="w" aria-hidden="true">${fmt(d, { weekday: "short" }).slice(0, 2)}</span><span class="n" aria-hidden="true">${d.getDate()}</span>
          <span class="dots" aria-hidden="true">${"<i></i>".repeat(Math.min(n, 4))}</span></button>`;
      }).join("");
      li.innerHTML = `<p class="eyebrow eyebrow--accent">${eyebrow}</p>
        <h3>${heading}</h3>
        <ol aria-live="polite">${items.length ? items.map(o => `<li>${occButton(o)}</li>`).join("") : `<li class="none">Nothing on that day.</li>`}</ol>
        <div class="strip">
          <div class="strip__head"><span class="eyebrow">Next ${nDays} days</span>${tileDay ? `<button type="button" class="strip__reset" data-day-reset>Show all upcoming</button>` : `<span class="note">Choose a day to see what’s on</span>`}</div>
          <div class="strip__days" role="group" aria-label="Choose a day">${cells}</div>
        </div>`;
    };
    draw();
    li.addEventListener("click", e => {
      const b = e.target.closest("[data-day]"), r = e.target.closest("[data-day-reset]");
      if (!b && !r) return;
      const key = b ? b.dataset.day : null;
      tileDay = r || tileDay === key ? null : key;
      draw();
      const f = tileDay ? $(`[data-day="${tileDay}"]`, li) : $(`[data-day]:not([disabled])`, li);
      f && requestAnimationFrame(() => f.focus({ preventScroll: true }));
      if (!reduced.matches) { const ol = $("ol", li); ol.classList.remove("swap"); void ol.offsetWidth; ol.classList.add("swap"); }
    });
    list.appendChild(li);
  }
  let rendered = false;
  function render() {
    $$("#date-filter button").forEach(b => b.setAttribute("aria-pressed", b.dataset.date === state.date));
    $$("[role=tab]", catWrap).forEach(b => {
      const on = b.dataset.cat === state.cat; b.setAttribute("aria-selected", on); b.tabIndex = on ? 0 : -1;
      const n = LIVE.filter(e => matches(e, true) && (b.dataset.cat === "all" || e.cat === b.dataset.cat)).length;
      $(".n", b).textContent = n;
    });
    $("#events").setAttribute("aria-labelledby", "tab-" + state.cat);
    $$(".view-toggle button").forEach(b => b.setAttribute("aria-pressed", b.dataset.view === state.view));
    const list = $("#events"); list.classList.toggle("is-list", state.view === "list");
    const shown = LIVE.filter(e => matches(e));
    list.innerHTML = shown.length ? shown.map((e, i) => card(e, i)).join("")
      : `<li class="empty"><p>Nothing matches those filters. Try another date range or remove an access filter.</p><button type="button" class="btn btn--ghost btn--sm" id="empty-clear">Clear all filters</button></li>`;
    const ec = $("#empty-clear"); ec && ec.addEventListener("click", () => $("#clear-filters").click());
    const rc = $("#results-count"); const prev = rc.dataset.n;
    rc.innerHTML = `Showing <b>${shown.length}</b> of <b>${LIVE.length}</b> events`;
    if (prev !== undefined && prev !== String(shown.length) && !reduced.matches) { rc.classList.remove("bump"); void rc.offsetWidth; rc.classList.add("bump"); }
    rc.dataset.n = shown.length;
    if (rendered && !reduced.matches) $$(".event", list).forEach(li => li.classList.add("is-entering"));
    rendered = true;
    fillGap(list, shown);
    $("#clear-filters").hidden = !(state.date !== "all" || state.cat !== "all" || state.access.size);
  }
  if (hasProgramme) {
    render();
    let rz; window.addEventListener("resize", () => { clearTimeout(rz); rz = setTimeout(() => fillGap($("#events"), LIVE.filter(e => matches(e))), 150); });
  }
  /* Card lists that aren't the filterable programme: <ul data-cards="id,id,id"> or data-cards="related:id" or "exhibition" */
  $$("[data-cards]").forEach(ul => {
    const spec = ul.dataset.cards; let list;
    if (spec.startsWith("related:")) { const me = EVENTS.find(e => e.id === spec.slice(8)); list = LIVE.filter(e => e.id !== spec.slice(8)).sort((a, b) => (b.cat === (me && me.cat)) - (a.cat === (me && me.cat)) || a.upcoming[0] - b.upcoming[0]).slice(0, 3); }
    else list = spec.split(",").map(id => LIVE.find(e => e.id === id)).filter(Boolean);
    ul.innerHTML = list.map((e, i) => card(e, i)).join("");
  });
  /* Upcoming dates for a single event page */
  $$("[data-event-dates]").forEach(ol => {
    const e = EVENTS.find(x => x.id === ol.dataset.eventDates); if (!e) return;
    const n = +(ol.dataset.limit || 8);
    ol.innerHTML = e.upcoming.length ? e.upcoming.slice(0, n).map(d => `<li><button type="button" class="date-row" data-book="${e.id}" data-date="${iso(d)}"><span class="d">${sameDay(d, TODAY) ? "Today" : fmt(d, { weekday: "long", day: "numeric", month: "long" })}</span><span class="t">${e.slots.join(" · ")}</span><span class="go" aria-hidden="true">Book →</span></button></li>`).join("")
      : `<li class="none">No more dates this season. Sign up to the Journal for the next one.</li>`;
    const more = e.upcoming.length - n; const m = ol.nextElementSibling;
    if (m && m.matches("[data-more-dates]")) m.textContent = more > 0 ? `+ ${more} more dates until ${fmt(e.upcoming[e.upcoming.length - 1], { day: "numeric", month: "long", year: "numeric" })}` : "";
  });
  setTimeout(sweep, 0);

  /* ---------- Ticker ---------- */
  (function ticker() {
    if (!$("#ticker-track")) return;
    const items = upcoming(14, null, 2);
    const listHTML = `<ul>${items.map(o => `<li>${occButton(o)}</li>`).join("")}</ul>`;
    const track = $("#ticker-track"); if (!track) return;
    track.innerHTML = listHTML + listHTML;
    const dup = track.children[1]; dup.setAttribute("aria-hidden", "true"); dup.inert = true;
    const t = $("#ticker"), pb = $("#ticker-pause");
    pb.addEventListener("click", () => {
      const p = !t.classList.contains("is-paused"); t.classList.toggle("is-paused", p);
      pb.setAttribute("aria-pressed", String(p)); pb.setAttribute("aria-label", p ? "Play the coming-up list" : "Pause the coming-up list");
      pb.innerHTML = p ? '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 1.5v11l9-5.5z"/></svg>' : '<svg viewBox="0 0 14 14" aria-hidden="true"><rect x="2" y="1" width="3.5" height="12"/><rect x="8.5" y="1" width="3.5" height="12"/></svg>';
    });
  })();

  /* ---------- Booking drawer ---------- */
  const drawer = $("#booking"), scrim = $("#scrim");
  const TIERS = [
    { id: "adult", name: "Adult General Admission", meta: "Ages 25–64", price: 12.5 },
    { id: "conc", name: "Concession", meta: "Seniors 65+, students with ID", price: 9 },
    { id: "free", name: "Somerset Resident / Under 25", meta: "Free, reservation required", price: 0 }
  ];
  const MAX_EACH = 10, DONATION = 3;
  const bk = { eventId: "echoes", date: null, slot: null, qty: { adult: 0, conc: 0, free: 0 }, donate: false };

  $("#bk-event").innerHTML = LIVE.map(e => `<option value="${e.id}">${esc(e.title)}</option>`).join("");
  $("#bk-tiers").innerHTML = TIERS.map(t => `
    <div class="tier">
      <div><p class="tier__name" id="tier-${t.id}">${t.name}</p><p class="tier__meta">${t.meta} · <span class="tier__price">${t.price ? money.format(t.price) : "Free"}</span></p></div>
      <div class="stepper" role="group" aria-labelledby="tier-${t.id}">
        <button type="button" data-dec="${t.id}" aria-label="Remove one ${t.name} ticket">−</button>
        <output id="qty-${t.id}" aria-label="${t.name} quantity">0</output>
        <button type="button" data-inc="${t.id}" aria-label="Add one ${t.name} ticket">+</button>
      </div>
    </div>`).join("");

  function hash(s) { let h = 2166136261; for (const c of s) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return Math.abs(h); }
  function remaining(eventId, date, slot) {
    const n = hash(`${eventId}|${iso(date)}|${slot}`) % 46;
    return n < 4 ? 0 : n;
  }
  const ev = () => EVENTS.find(e => e.id === bk.eventId);
  const totalQty = () => Object.values(bk.qty).reduce((a, b) => a + b, 0);
  const subtotal = () => TIERS.reduce((s, t) => s + t.price * bk.qty[t.id], 0);
  const total = () => subtotal() + (bk.donate ? DONATION : 0);
  const selDate = () => bk.date ? new Date(bk.date + "T00:00:00") : null;

  function renderDates() {
    const e = ev();
    $("#bk-dates").innerHTML = e.upcoming.slice(0, 12).map(d => {
      const v = iso(d);
      return `<label class="radio-chip"><input type="radio" name="bk-date" id="date-${v}" value="${v}" ${bk.date === v ? "checked" : ""}>
        <span><span class="d1">${sameDay(d, TODAY) ? "Today" : fmt(d, { weekday: "short" })}</span><span class="d2">${d.getDate()}</span><span class="d3">${fmt(d, { month: "short" })}</span></span></label>`;
    }).join("");
  }
  function renderTimes() {
    const e = ev(), d = selDate(), box = $("#bk-times");
    if (!d) { box.innerHTML = `<p class="note">Choose a date to see entry times.</p>`; return; }
    box.innerHTML = e.slots.map(s => {
      const r = remaining(e.id, d, s), id = `time-${s.replace(":", "")}`;
      const status = r === 0 ? "Sold out" : r < 12 ? `${r} left` : "Available";
      return `<label class="radio-chip"><input type="radio" name="bk-time" id="${id}" value="${s}" ${r === 0 ? "disabled" : ""} ${bk.slot === s ? "checked" : ""} aria-label="${s}, ${status}">
        <span><span class="d2">${s}</span><span class="d3">${status}</span></span></label>`;
    }).join("");
  }
  function cap() { return bk.slot && selDate() ? Math.min(remaining(bk.eventId, selDate(), bk.slot), 30) : 30; }

  let shownTotal = 0, raf = 0;
  function tweenTotal(to) {
    const el = $("#tray-total"); cancelAnimationFrame(raf);
    if (reduced.matches || to === shownTotal) { shownTotal = to; el.textContent = money.format(to); return; }
    const from = shownTotal, t0 = performance.now();
    el.classList.remove("bump"); void el.offsetWidth; el.classList.add("bump");
    const stepT = now => { const k = Math.min(1, (now - t0) / 320), v = from + (to - from) * (1 - Math.pow(1 - k, 3));
      el.textContent = money.format(Math.round(v * 100) / 100); if (k < 1) raf = requestAnimationFrame(stepT); else shownTotal = to; };
    raf = requestAnimationFrame(stepT);
  }
  function renderTotals(announce = true) {
    TIERS.forEach(t => {
      $("#qty-" + t.id).textContent = bk.qty[t.id];
      $(`[data-dec="${t.id}"]`).disabled = bk.qty[t.id] === 0;
      $(`[data-inc="${t.id}"]`).disabled = bk.qty[t.id] >= MAX_EACH || totalQty() >= cap();
    });
    const e = ev(), d = selDate(), q = totalQty();
    const when = d ? `${fmt(d, { weekday: "short", day: "numeric", month: "short" })}${bk.slot ? ", " + bk.slot : ""}` : null;
    const rows = [];
    rows.push(`<div><dt>${esc(e.title)}</dt><dd>${when || "Date not chosen"}</dd></div>`);
    TIERS.forEach(t => { if (bk.qty[t.id]) rows.push(`<div><dt>${bk.qty[t.id]} × ${t.name}</dt><dd>${t.price ? money.format(t.price * bk.qty[t.id]) : "Free"}</dd></div>`); });
    if (!q) rows.push(`<div><dt>Tickets</dt><dd>None yet</dd></div>`);
    if (bk.donate) rows.push(`<div><dt>Rural school bus fund</dt><dd>${money.format(DONATION)}</dd></div>`);
    rows.push(`<div><dt>Booking fee</dt><dd>${money.format(0)}</dd></div>`);
    rows.push(`<div class="total"><dt>Total</dt><dd>${money.format(total())}</dd></div>`);
    $("#bk-summary").innerHTML = rows.join("");
    const t = money.format(total());
    tweenTotal(total());
    $("#tray-what").textContent = !d ? "Choose a date to begin" : !bk.slot ? `${when} · choose a time` : q ? `${q} ticket${q > 1 ? "s" : ""} · ${when}` : `${when} · add tickets`;
    const btn = $("#checkout");
    btn.textContent = `Proceed to Secure Checkout — ${t}`;
    btn.setAttribute("aria-disabled", String(!(d && bk.slot && q)));
    if (d && bk.slot && q) $("#tray-error").textContent = "";
    if (announce) $("#tray-live").textContent = `Order total ${t} for ${q} ticket${q === 1 ? "" : "s"}${bk.donate ? ", including £3 donation" : ""}.`;
    // progress
    const done = { 1: !!(d && bk.slot), 2: q > 0, 3: q > 0, 4: !!(d && bk.slot && q) };
    const current = [1, 2, 3, 4].find(n => !done[n]) || 4;
    $$("#steps button").forEach(b => {
      const n = +b.dataset.step; b.classList.toggle("is-done", done[n]);
      n === current ? b.setAttribute("aria-current", "step") : b.removeAttribute("aria-current");
    });
  }

  function trimToCap() {
    let over = totalQty() - cap();
    for (const k of ["free", "conc", "adult"]) { while (over > 0 && bk.qty[k] > 0) { bk.qty[k]--; over--; } }
  }

  $("#bk-event").addEventListener("change", e => {
    bk.eventId = e.target.value; bk.date = null; bk.slot = null;
    renderDates(); renderTimes(); renderTotals();
  });
  $("#bk-dates").addEventListener("change", e => {
    bk.date = e.target.value; const d = selDate();
    if (bk.slot && remaining(bk.eventId, d, bk.slot) === 0) bk.slot = null;
    if (!bk.slot && ev().slots.length === 1 && remaining(bk.eventId, d, ev().slots[0]) > 0) bk.slot = ev().slots[0];
    renderTimes(); trimToCap(); renderTotals();
  });
  $("#bk-times").addEventListener("change", e => { bk.slot = e.target.value; trimToCap(); renderTotals(); });
  $("#bk-tiers").addEventListener("click", e => {
    const inc = e.target.closest("[data-inc]"), dec = e.target.closest("[data-dec]");
    if (inc && !inc.disabled) bk.qty[inc.dataset.inc]++;
    if (dec && !dec.disabled) bk.qty[dec.dataset.dec]--;
    if (inc || dec) {
      renderTotals();
      const b = inc || dec; if (b.disabled) (inc ? $(`[data-dec="${inc.dataset.inc}"]`) : $(`[data-inc="${dec.dataset.dec}"]`)).focus();
    }
  });
  $("#bk-donate").addEventListener("change", e => { bk.donate = e.target.checked; renderTotals(); });
  $("#steps").addEventListener("click", e => {
    const b = e.target.closest("[data-step]"); if (!b) return;
    const s = $("#step-" + b.dataset.step); s.scrollIntoView({ behavior: reduced.matches ? "auto" : "smooth", block: "start" });
    const f = focusables(s)[0]; f && f.focus({ preventScroll: true });
  });
  $("#checkout").addEventListener("click", () => {
    const d = selDate(), q = totalQty();
    if (!d || !bk.slot || !q) {
      const missing = !d ? "Choose a date" : !bk.slot ? "Choose an entry time" : "Add at least one ticket";
      $("#tray-error").textContent = `${missing} before checkout.`;
      const target = !d || !bk.slot ? $("#step-1") : $("#step-2");
      target.scrollIntoView({ behavior: reduced.matches ? "auto" : "smooth", block: "start" });
      return;
    }
    const ref = "BY-" + (hash(iso(d) + bk.slot + q + Date.now()) % 900000 + 100000);
    $("#confirm-text").textContent = `${q} ticket${q > 1 ? "s" : ""} for ${ev().title}, ${fmt(d, { weekday: "long", day: "numeric", month: "long" })} at ${bk.slot}. Total ${money.format(total())}${bk.donate ? ", including your £3 school bus donation" : ""}.`;
    $("#confirm-ref").textContent = ref;
    ["#drawer-body", "#tray", "#steps"].forEach(s => $(s).hidden = true);
    $("#confirm").hidden = false; $("#confirm").focus();
  });
  function resetBooking(eventId, dateIso) {
    bk.eventId = LIVE.some(e => e.id === eventId) ? eventId : (LIVE[0] && LIVE[0].id);
    bk.date = null; bk.slot = null; bk.qty = { adult: 0, conc: 0, free: 0 }; bk.donate = false;
    $("#bk-event").value = bk.eventId; $("#bk-donate").checked = false; $("#tray-error").textContent = "";
    ["#drawer-body", "#tray", "#steps"].forEach(s => $(s).hidden = false); $("#confirm").hidden = true;
    const e = ev();
    const pick = (dateIso && e.upcoming.find(d => iso(d) === dateIso)) || e.upcoming[0];
    if (pick) { bk.date = iso(pick); const free = e.slots.find(s => remaining(e.id, pick, s) > 0); if (free && e.slots.length === 1) bk.slot = free; }
    renderDates(); renderTimes(); renderTotals(false);
    $("#drawer-body").scrollTop = 0;
    const chosen = bk.date && $(`#date-${bk.date}`); chosen && chosen.closest(".radio-chip").scrollIntoView({ block: "nearest" });
  }
  $("#new-booking").addEventListener("click", () => { resetBooking(bk.eventId); $("#bk-event").focus(); });

  function openBooking(eventId, opener, dateIso) {
    resetBooking(eventId, dateIso);
    $$("[data-book]").forEach(b => b.setAttribute("aria-expanded", "false"));
    opener && opener.setAttribute("aria-expanded", "true");
    showModal(drawer, () => $("#booking-close").focus(), scrim);
  }
  function closeBooking() {
    $$("[data-book]").forEach(b => b.setAttribute("aria-expanded", "false"));
    hideModal(drawer, scrim);
  }
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-book]"); if (!b) return;
    e.preventDefault();
    if (openModal === menu) { const id = b.dataset.book; menuBtn.setAttribute("aria-expanded", "false"); menu.classList.remove("is-open"); menu.hidden = true; openModal = null; lastFocus = menuBtn; openBooking(id, null); lastFocus = menuBtn; return; }
    openBooking(b.dataset.book, b, b.dataset.date);
  });
  $$("[data-book]").forEach(b => { b.setAttribute("aria-controls", "booking"); b.setAttribute("aria-haspopup", "dialog"); b.setAttribute("aria-expanded", "false"); });
  const ariaBook = () => $$("[data-book]").forEach(b => { b.setAttribute("aria-controls", "booking"); b.setAttribute("aria-haspopup", "dialog"); if (!b.hasAttribute("aria-expanded")) b.setAttribute("aria-expanded", "false"); });
  $$("#events, [data-cards], [data-event-dates], #ticker-track").forEach(n => new MutationObserver(ariaBook).observe(n, { childList: true }));
  ariaBook();
  $("#booking-close").addEventListener("click", closeBooking);
  scrim.addEventListener("click", closeBooking);

  /* ---------- Journal sign-up ---------- */
  const form = $("#journal-form"), email = $("#email"), err = $("#email-error");
  let touched = false;
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function validate() {
    const v = email.value.trim();
    let msg = "";
    if (!v) msg = "Enter your email address to subscribe.";
    else if (!EMAIL_RE.test(v)) msg = "Enter an email address in the format name@example.co.uk.";
    err.textContent = msg; email.setAttribute("aria-invalid", msg ? "true" : "false");
    return !msg;
  }
  email.addEventListener("blur", () => { if (email.value.trim()) { touched = true; validate(); } });
  email.addEventListener("input", () => { if (touched) validate(); });
  form.addEventListener("submit", e => {
    e.preventDefault(); touched = true;
    if (!validate()) { email.focus(); return; }
    const s = $("#journal-success");
    s.textContent = `Subscribed. The next Journal goes to ${email.value.trim()} on the first Friday of the month.`;
    s.hidden = false; form.hidden = true;
  });
})();

/* ---------- Page-specific forms: membership, donations, enquiries ---------- */
(() => {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Membership: prototype hand-off message
  $$("[data-join]").forEach(a => a.addEventListener("click", ev => {
    ev.preventDefault();
    const n = $("#join-note"); if (!n) return;
    n.textContent = `${a.dataset.join} membership selected. In the live site this continues to secure checkout, where you can pay by card or Direct Debit.`;
  }));

  // Donation picker: show what each amount pays for
  $$("[data-donate]").forEach(form => {
    const IMPACT = { 10: "£10 pays for four pupils’ seats on the coach.", 25: "£25 pays for ten pupils to travel to the Yard and back.",
                     50: "£50 pays for a workshop’s clay, tools and firing.", 120: "£120 pays for a whole class’s coach from a village school." };
    const out = $("[data-impact]", form), btn = $("[data-donate-btn]", form), note = $("[data-donate-note]", form), ga = $("#giftaid", form);
    const update = () => {
      const v = +($("input[name=amount]:checked", form) || {}).value || 0;
      const extra = ga && ga.checked ? ` With Gift Aid it’s worth £${(v * 1.25).toFixed(2).replace(".00", "")} to us.` : "";
      out.textContent = (IMPACT[v] || "") + extra;
      btn.textContent = `Donate £${v}`;
    };
    form.addEventListener("change", update);
    form.addEventListener("submit", ev => { ev.preventDefault(); note.textContent = "Thank you. In the live site this continues to secure payment."; });
    update();
  });

  // Enquiry forms: inline validation
  $$("[data-enquiry]").forEach(form => {
    const RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    const check = el => {
      const f = el.closest(".field"), err = f && $(".error", f); let msg = "";
      if (el.required && !el.value.trim()) msg = `Enter ${el.labels[0].textContent.toLowerCase()}.`;
      else if (el.type === "email" && el.value && !RE.test(el.value.trim())) msg = "Enter an email address like name@example.co.uk.";
      el.setAttribute("aria-invalid", msg ? "true" : "false"); if (err) err.textContent = msg;
      return !msg;
    };
    $$("[required]", form).forEach(el => { el.addEventListener("blur", () => el.value && check(el)); el.addEventListener("input", () => el.getAttribute("aria-invalid") === "true" && check(el)); });
    form.addEventListener("submit", ev => {
      ev.preventDefault();
      const bad = $$("[required]", form).filter(el => !check(el));
      if (bad.length) { bad[0].focus(); return; }
      const s = $(".success", form); s.hidden = false;
      s.textContent = `Thanks, ${$("#q-name").value.trim().split(" ")[0]}. Our events team will reply within two working days.`;
      $$("input, textarea, select, button[type=submit]", form).forEach(el => el.disabled = true);
    });
  });
})();
