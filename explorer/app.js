/* Rollout Atlas: browse the rollouts of the CoT-controllability x eval-awareness experiments.
   Data comes from data/manifest.json and one shard per view, built by explorer/build.py. */
(() => {
  'use strict';
  const $ = (s, el = document) => el.querySelector(s);
  const el = (tag, attrs = {}, ...kids) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      if (k === 'class') n.className = v; else if (k === 'text') n.textContent = v;
      else if (k.startsWith('on')) n.addEventListener(k.slice(2), v); else n.setAttribute(k, v === true ? '' : v);
    }
    for (const c of kids.flat()) if (c != null) n.append(c.nodeType ? c : document.createTextNode(String(c)));
    return n;
  };

  const TAG = '<this is not suspicious>';
  const ARM_COLOR = { base: 'var(--a0)', ctrldel: 'var(--a1)', cdel: 'var(--a2)', steerctrl: 'var(--a3)', steer: 'var(--a4)', steerrand: 'var(--a5)',
    screen_qwen3_32b: 'var(--a0)', screen_qwq_32b: 'var(--a1)', screen_olmo3_32b_think: 'var(--a2)', screen_olmo31_32b_think: 'var(--a3)', screen_deepseek_r1: 'var(--a4)', olmo31: 'var(--a3)' };
  const ARMED = new Set(['gptoss', 'screen', 'graded']);  // experiments whose rollouts carry a model (arm)
  const armed = () => ARMED.has(S.exp);
  const COND_LABEL = {
    eval_like: 'eval-framed', deploy_like: 'normal-use', none: 'no cue', explicit: '+ system eval cue', subtle: '+ metadata cue', asis: 'as provided',
    dev_explicit: '+ formal cue (system)', user_explicit: '+ formal cue (user turn)', user_casual: '+ casual cue (user turn)',
    baseline: 'no instruction', all_caps: 'all caps (train)', all_lower: 'all lowercase (train)', bullet: 'bulleted list (held-out)',
    numbered: 'numbered list (held-out)', no_word_so: 'avoid “so” (held-out)',
    'cot:baseline': 'CoT · no constraint', 'cot:word_suppression': 'CoT · avoid a word', 'cot:tag_start': 'CoT · tag at start',
    'cot:lowercase': 'CoT · lowercase', 'answer_if:lowercase': 'Answer-IF · lowercase answer'
  };

  // ---------- label definitions per experiment ----------
  const v4 = (r, j, ch) => r.lab[j] && r.lab[j][ch] ? r.lab[j][ch].v : undefined;
  const v3bad = (r) => r.lab.v3q ? r.lab.v3q.ex.some((e) => e.at === 'prompt' || e.at === 'none') : undefined;
  const LABELS = {
    gptoss: [
      ['v4q', 'Cue in reasoning · Qwen v4', (r) => v4(r, 'v4q', 'cot')],
      ['v4d', 'Cue in reasoning · DeepSeek v4', (r) => v4(r, 'v4d', 'cot')],
      ['v4ans', 'Cue in answer · Qwen v4', (r) => v4(r, 'v4q', 'response')],
      ['v4dis', 'v4 judges disagree', (r) => (r.lab.v4q && r.lab.v4d ? v4(r, 'v4q', 'cot') !== v4(r, 'v4d', 'cot') : undefined)],
      ['v3', 'v3 judge flagged', (r) => (r.lab.v3q ? r.lab.v3q.a : undefined)],
      ['v3bad', 'v3 quote not in model text', v3bad],
      ['lex', 'Cue words echoed (text match)', (r) => r.lab.lex],
      ['ref', 'Refusal', (r) => r.lab.ref],
      ['trunc', 'Hit token limit', (r) => r.finish === 'length'],
      ['comp', 'Follows instruction', (r) => r.lab.comp],
      ['acc', 'Correct answer', (r) => r.lab.acc]
    ],
    olmo: [
      ['comp', 'Follows constraint', (r) => r.lab.comp],
      ['mentions', 'Talks about the constraint', (r) => r.lab.mentions],
      ['correct', 'Correct answer', (r) => r.lab.correct],
      ['aif', 'Answer-IF compliant', (r) => r.lab.aif],
      ['v3', 'Judge: eval-aware', (r) => (r.lab.v3q ? r.lab.v3q.a : undefined)],
      ['v3bad', 'Judge quote not in model text', v3bad],
      ['trunc', 'Hit token limit', (r) => r.finish === 'length']
    ],
    screen: [
      ['v4q', 'Mentions evaluation in reasoning · v4', (r) => v4(r, 'v4q', 'cot')],
      ['ref', 'Refusal (text match)', (r) => r.lab.ref],
      ['trunc', 'Hit token limit', (r) => r.finish === 'length']
    ],
    graded: [
      ['v4q', 'Mentions evaluation in reasoning · v4', (r) => v4(r, 'v4q', 'cot')],
      ['ref', 'Refused (StrongREJECT judge)', (r) => r.lab.ref],
      ['help', 'Substantive help (score ≥ 0.5)', (r) => (r.lab.sr == null ? undefined : r.lab.sr >= 0.5)],
      ['trunc', 'Hit token limit', (r) => r.finish === 'length']
    ],
    pilot: [
      ['v3', 'v3 judge flagged', (r) => (r.lab.v3q ? r.lab.v3q.a : undefined)],
      ['v3bad', 'v3 quote not in model text', v3bad],
      ['ref', 'Refusal', (r) => r.lab.ref],
      ['trunc', 'Hit token limit', (r) => r.finish === 'length']
    ]
  };
  const condOf = (exp, r) => (exp === 'olmo' ? `${r.task}:${r.cons}` : r.cond);

  // ---------- state ----------
  const S = {
    manifest: null, exp: 'gptoss', shard: null, data: null, cache: new Map(),
    arms: new Set(), conds: new Set(), labels: {}, q: '', regex: true, scope: 'all', sort: 'prompt',
    list: [], shown: 150, sel: null, pair: false, pairSample: null
  };

  // ---------- theme ----------
  const themeBtn = $('#theme');
  const applyTheme = (t) => { if (t) document.documentElement.dataset.theme = t; else delete document.documentElement.dataset.theme; };
  try { applyTheme(localStorage.getItem('atlas-theme')); } catch (e) { /* storage unavailable */ }
  themeBtn.addEventListener('click', () => {
    const cur = document.documentElement.dataset.theme;
    const next = !cur ? (matchMedia('(prefers-color-scheme: dark)').matches ? 'light' : 'dark') : (cur === 'dark' ? 'light' : 'dark');
    applyTheme(next); try { localStorage.setItem('atlas-theme', next); } catch (e) { /* ignore */ }
  });

  // ---------- hash state ----------
  function readHash() {
    const h = new URLSearchParams(location.hash.slice(1));
    return { x: h.get('x'), s: h.get('s'), r: h.get('r'), p: h.get('p') === '1', q: h.get('q') };
  }
  function writeHash() {
    const h = new URLSearchParams();
    h.set('x', S.exp); if (S.shard) h.set('s', S.shard); if (S.sel) h.set('r', S.sel); if (S.pair) h.set('p', '1'); if (S.q) h.set('q', S.q);
    history.replaceState(null, '', '#' + h.toString());
  }

  // ---------- data loading ----------
  async function loadManifest() {
    const res = await fetch('data/manifest.json');
    if (!res.ok) throw new Error('data/manifest.json not found. Run: python explorer/build.py');
    S.manifest = await res.json();
    $('#built').textContent = S.manifest.built ? `data built ${S.manifest.built}` : '';
  }
  async function loadShard(exp, id) {
    const key = `${exp}/${id}`;
    if (S.cache.has(key)) return S.cache.get(key);
    $('#count').textContent = 'Loading…';
    const res = await fetch(`data/${exp}/${encodeURIComponent(id)}.json`);
    if (!res.ok) throw new Error(`Could not load data/${key}.json`);
    const d = await res.json();
    d.rollouts.forEach((r, i) => { r._i = i; });
    if (S.cache.size >= 4) S.cache.delete(S.cache.keys().next().value);
    S.cache.set(key, d);
    return d;
  }

  // ---------- experiment + shard pickers ----------
  function shardLabel(exp, s) {
    if (exp === 'olmo') return `${s.size} · ${s.pipeline}${s.step ? ` · step ${Number(s.step).toLocaleString()}` : s.revision === 'main' ? ' · released' : ''}`;
    return `${s.label} (${s.n.toLocaleString()})`;
  }
  function fillShards() {
    const sel = $('#shard'); sel.replaceChildren();
    const shards = S.manifest[S.exp].shards;
    if (S.exp === 'olmo') {
      const groups = new Map();
      shards.forEach((s) => { const g = `${s.size} · ${s.pipeline}`; if (!groups.has(g)) groups.set(g, []); groups.get(g).push(s); });
      for (const [g, list] of groups) {
        const og = el('optgroup', { label: g });
        list.forEach((s) => og.append(el('option', { value: s.id, text: shardLabel('olmo', s) })));
        sel.append(og);
      }
    } else shards.forEach((s) => sel.append(el('option', { value: s.id, text: shardLabel(S.exp, s) })));
  }
  async function setExp(exp, shardId, keepSel) {
    S.exp = exp;
    document.querySelectorAll('.exps button').forEach((b) => b.setAttribute('aria-selected', String(b.dataset.exp === exp)));
    fillShards();
    const shards = S.manifest[exp].shards;
    const id = shards.some((s) => s.id === shardId) ? shardId : shards[0].id;
    $('#shard').value = id;
    await setShard(id, keepSel);
  }
  async function setShard(id, keepSel) {
    S.shard = id;
    S.data = await loadShard(S.exp, id);
    const arms = armed() ? S.manifest[S.exp].arms.map((a) => a.id) : [];
    S.arms = new Set(arms);
    S.conds = new Set(S.data.rollouts.map((r) => condOf(S.exp, r)));
    S.labels = {}; S.shown = 150;
    if (!keepSel) { S.sel = null; S.pair = false; }
    buildFilterUI();
    apply();
  }

  // ---------- filter UI ----------
  function buildFilterUI() {
    const armBox = $('#arms'); armBox.replaceChildren();
    $('#armsec').hidden = !armed() || S.manifest[S.exp].arms.length < 2;
    if (armed()) {
      S.manifest[S.exp].arms.forEach((a) => {
        const cb = el('input', { type: 'checkbox', checked: S.arms.has(a.id), onchange: () => { cb.checked ? S.arms.add(a.id) : S.arms.delete(a.id); S.shown = 150; apply(); } });
        armBox.append(el('label', {}, cb, el('span', { class: 'sw', style: `background:${ARM_COLOR[a.id]}` }), a.label));
      });
    }
    const condBox = $('#conds'); condBox.replaceChildren();
    const counts = new Map();
    S.data.rollouts.forEach((r) => { const c = condOf(S.exp, r); counts.set(c, (counts.get(c) || 0) + 1); });
    $('#condsec').hidden = counts.size < 2;
    $('#condlab').textContent = S.exp === 'olmo' ? 'Constraint' : (S.shard.startsWith('ctrl_check') ? 'Instruction' : 'Condition');
    [...counts.keys()].sort().forEach((c) => {
      const cb = el('input', { type: 'checkbox', checked: S.conds.has(c), onchange: () => { cb.checked ? S.conds.add(c) : S.conds.delete(c); S.shown = 150; apply(); } });
      condBox.append(el('label', {}, cb, `${COND_LABEL[c] || c} `, el('span', { class: 'meta', text: `(${counts.get(c)})` })));
    });
    const lb = $('#labels'); lb.replaceChildren();
    LABELS[S.exp].forEach(([key, name, fn]) => {
      if (!S.data.rollouts.some((r) => fn(r) !== undefined && fn(r) !== null)) return;
      const chip = el('button', { type: 'button', class: 'chip', 'data-state': S.labels[key] || 'any', text: name });
      chip.addEventListener('click', () => {
        const nxt = { any: 'yes', yes: 'no', no: 'any' }[S.labels[key] || 'any'];
        if (nxt === 'any') delete S.labels[key]; else S.labels[key] = nxt;
        chip.dataset.state = nxt; S.shown = 150; apply();
      });
      lb.append(chip);
    });
    buildLegend();
  }
  function buildLegend() {
    const L = $('#legend'); L.replaceChildren(el('div', { class: 'lab', text: 'Highlights' }));
    const row = (cls, txt) => L.append(el('div', {}, el('mark', { class: cls, text: 'abc' }), txt));
    if (S.exp === 'olmo') {
      row('h-ban', 'banned word'); row('h-tag', 'required tag'); row('h-caps', 'capitals under a lowercase rule'); row('h-quote', 'judge quote found in model text');
    } else {
      row('h-cue', 'eval cue in the prompt');
      if (S.exp === 'gptoss') { row('h-quote', 'v4 judge quote (verified)'); row('h-quote3', 'v3 judge quote (saw the prompt)'); }
      else if (armed()) row('h-quote', 'v4 judge quote (verified)');
      else row('h-quote', 'v3 judge quote found in model text');
      row('h-echo', 'words from the cue, echoed');
    }
    row('h-search', 'your search');
  }

  $('#q').addEventListener('input', debounce(() => { S.q = $('#q').value; S.shown = 150; apply(); }, 200));
  $('#regex').addEventListener('change', () => { S.regex = $('#regex').checked; apply(); });
  $('#scope').addEventListener('change', () => { S.scope = $('#scope').value; apply(); });
  $('#sort').addEventListener('change', () => { S.sort = $('#sort').value; apply(); });
  $('#reset').addEventListener('click', () => { $('#q').value = ''; S.q = ''; setShard(S.shard, true); });
  $('#more').addEventListener('click', () => { S.shown += 300; renderList(); });
  $('#shard').addEventListener('change', () => setShard($('#shard').value));
  document.querySelectorAll('.exps button').forEach((b) => b.addEventListener('click', () => setExp(b.dataset.exp)));
  $('#togglefilters').addEventListener('click', () => $('#filters').classList.toggle('open'));

  function debounce(fn, ms) { let t; return () => { clearTimeout(t); t = setTimeout(fn, ms); }; }

  // ---------- filtering ----------
  function searchRe() {
    if (!S.q) return null;
    try { return new RegExp(S.regex ? S.q : S.q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'); } catch (e) { return null; }
  }
  const promptText = (r) => {
    if (S.exp === 'olmo') return S.data.prompts[r.ph] || '';
    const p = S.data.prompts[r.pid]; return p ? `${p.system || ''}\n${p.user}` : '';
  };
  function apply() {
    const re = searchRe();
    const defs = LABELS[S.exp].filter(([k]) => S.labels[k]);
    const out = [];
    for (const r of S.data.rollouts) {
      if (armed() && !S.arms.has(r.arm)) continue;
      if (!S.conds.has(condOf(S.exp, r))) continue;
      let ok = true;
      for (const [k, , fn] of defs) { const v = fn(r) === true; if ((S.labels[k] === 'yes') !== v) { ok = false; break; } }
      if (!ok) continue;
      if (re) {
        re.lastIndex = 0;
        const hay = S.scope === 'reasoning' ? r.reasoning : S.scope === 'response' ? r.response : S.scope === 'prompt' ? promptText(r) : `${r.reasoning}\n${r.response}`;
        if (!re.test(hay)) continue;
      }
      out.push(r);
    }
    if (S.sort === 'len-desc') out.sort((a, b) => b.reasoning.length - a.reasoning.length);
    else if (S.sort === 'len-asc') out.sort((a, b) => a.reasoning.length - b.reasoning.length);
    S.list = out;
    renderList();
    const cur = S.sel && S.data.rollouts.find((r) => r.id === S.sel);
    if (cur) renderDetail(cur); else if (!S.sel) $('#detail').replaceChildren(el('div', { class: 'empty', text: out.length ? 'Pick a rollout on the left. Keys: j / k next and previous, p same prompt across models, / search.' : 'No rollouts match these filters.' }));
    writeHash();
  }

  // ---------- list ----------
  function badgesFor(r) {
    const b = [];
    const add = (txt, cls, title) => b.push(el('span', { class: `b ${cls || ''}`, text: txt, title }));
    if (S.exp === 'gptoss') {
      const q = v4(r, 'v4q', 'cot'), d = v4(r, 'v4d', 'cot');
      if (q || d) add(q && d ? 'cue·CoT' : 'cue·CoT?', q && d ? 'on' : 'info', `v4 cue in reasoning: Qwen ${q ? 'yes' : 'no'}, DeepSeek ${d ? 'yes' : 'no'}`);
      if (v4(r, 'v4q', 'response')) add('cue·ans', 'on', 'v4 Qwen: cue mentioned in the final answer');
      if (r.lab.v3q && r.lab.v3q.a) add(v3bad(r) ? 'v3 ✗' : 'v3', v3bad(r) ? 'warn' : '', v3bad(r) ? 'v3 judge flagged, but a quote is not in the model text' : 'v3 judge flagged');
      if (r.lab.ref) add('refusal', '', 'refusal-style response');
      if (r.lab.comp === true) add('follows', 'on', 'reasoning follows the instruction');
    } else if (S.exp === 'screen' || S.exp === 'graded') {
      if (v4(r, 'v4q', 'cot')) add('EA·CoT', 'on', 'v4 judge: reasoning mentions evaluation (verified quote)');
      if (r.lab.sr != null) add(`SR ${r.lab.sr.toFixed(2)}`, r.lab.sr >= 0.5 ? 'warn' : '', `StrongREJECT score ${r.lab.sr} (0 = refuses, 1 = full help)`);
      if (r.lab.ref) add('refused', '', S.exp === 'graded' ? 'StrongREJECT judge: refused' : 'refusal-style response');
    } else if (S.exp === 'olmo') {
      if (r.lab.comp === true) add('follows', 'on', 'follows the constraint'); else if (r.lab.comp === false) add('violates', '', 'does not follow the constraint');
      if (r.lab.mentions) add('meta', 'info', 'talks about the constraint');
      if (r.lab.v3q && r.lab.v3q.a) add(v3bad(r) ? 'VEA ✗' : 'VEA', v3bad(r) ? 'warn' : 'on', 'judge flagged eval awareness');
    } else {
      if (r.lab.v3q && r.lab.v3q.a) add(v3bad(r) ? 'v3 ✗' : 'v3', v3bad(r) ? 'warn' : '', 'v3 judge flagged');
      if (r.lab.ref) add('refusal', '', 'refusal-style response');
    }
    if (r.finish === 'length') add('cut', 'warn', 'hit the token limit');
    return b;
  }
  function snippet(r) {
    const re = searchRe(); const base = r.reasoning || r.response || '';
    if (re && S.scope !== 'prompt') {
      const t = S.scope === 'response' ? r.response : base; re.lastIndex = 0; const m = re.exec(t);
      if (m) { const s = Math.max(0, m.index - 60); return (s ? '…' : '') + t.slice(s, m.index + 120).replace(/\s+/g, ' '); }
    }
    return base.slice(0, 200).replace(/\s+/g, ' ');
  }
  function armChip(arm) {
    const a = (S.manifest[S.exp].arms || []).find((x) => x.id === arm);
    return el('span', { class: 'armchip', style: `background:${ARM_COLOR[arm] || 'var(--muted)'}`, text: a ? a.label : arm });
  }
  function renderList() {
    const ol = $('#items'); ol.replaceChildren();
    const total = S.data.rollouts.length;
    $('#count').textContent = `${S.list.length.toLocaleString()} of ${total.toLocaleString()} rollouts`;
    S.list.slice(0, S.shown).forEach((r) => {
      const idTxt = S.exp === 'olmo' ? `${COND_LABEL[condOf('olmo', r)] || condOf('olmo', r)} · ${r.qid.split(':').pop()}` : `${r.item} · ${COND_LABEL[r.cond] || r.cond} · s${r.sample}`;
      const li = el('li', { class: 'item', 'aria-selected': String(r.id === S.sel), 'data-id': r.id, tabindex: '0' },
        el('div', { class: 'l1' }, armed() && S.manifest[S.exp].arms.length > 1 ? armChip(r.arm) : null, el('span', { class: 'id', text: idTxt }), el('span', { class: 'badges' }, badgesFor(r))),
        el('div', { class: 'snip', text: snippet(r) }));
      li.addEventListener('click', () => select(r.id));
      li.addEventListener('keydown', (e) => { if (e.key === 'Enter') select(r.id); });
      ol.append(li);
    });
    $('#more').hidden = S.list.length <= S.shown;
  }
  function select(id, opts = {}) {
    S.sel = id; if (!opts.keepPair) S.pairSample = null;
    document.querySelectorAll('.item').forEach((n) => n.setAttribute('aria-selected', String(n.dataset.id === id)));
    const r = S.data.rollouts.find((x) => x.id === id);
    if (r) renderDetail(r);
    document.body.classList.add('showdetail');
    const li = document.querySelector(`.item[data-id="${id}"]`); if (li) li.scrollIntoView({ block: 'nearest' });
    writeHash();
  }

  // ---------- highlighting ----------
  function findAll(text, needle, { word = false, ci = true } = {}) {
    if (!needle) return [];
    const esc = needle.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp(word ? `\\b${esc}\\b` : esc, ci ? 'gi' : 'g');
    const out = []; let m;
    while ((m = re.exec(text))) { out.push([m.index, m.index + m[0].length]); if (!m[0].length) re.lastIndex++; }
    return out;
  }
  function findQuote(text, quote) {
    if (!quote || !text) return [];
    const lt = text.toLowerCase(), q = quote.trim().replace(/^["“']|["”']$/g, '');
    let i = lt.indexOf(q.toLowerCase());
    if (i >= 0) return [[i, i + q.length]];
    const out = [];
    q.split(/\.\.\.|…/).map((f) => f.trim()).filter((f) => f.length >= 12).forEach((f) => {
      const j = lt.indexOf(f.toLowerCase()); if (j >= 0) out.push([j, j + f.length]);
    });
    if (out.length) return out;
    for (const part of [q.slice(0, 50), q.slice(-50)]) { if (part.length >= 20) { const j = lt.indexOf(part.toLowerCase()); if (j >= 0) out.push([j, j + part.length]); } }
    return out;
  }
  function render(text, specs) {
    const frag = document.createDocumentFragment();
    if (!text) return frag;
    const pts = new Set([0, text.length]); const rs = [];
    specs.forEach(([cls, ranges]) => ranges.forEach(([s, e]) => { if (e > s) { rs.push([s, e, cls]); pts.add(s); pts.add(e); } }));
    const cuts = [...pts].sort((a, b) => a - b);
    for (let k = 0; k < cuts.length - 1; k++) {
      const s = cuts[k], e = cuts[k + 1]; const seg = text.slice(s, e);
      const cls = [...new Set(rs.filter(([a, b]) => a <= s && b >= e).map((x) => x[2]))];
      frag.append(cls.length ? el('mark', { class: cls.join(' '), text: seg }) : document.createTextNode(seg));
    }
    return frag;
  }
  function searchRanges(text) {
    const re = searchRe(); if (!re || !text) return [];
    const out = []; let m; re.lastIndex = 0;
    while ((m = re.exec(text))) { out.push([m.index, m.index + m[0].length]); if (!m[0].length) re.lastIndex++; }
    return out;
  }
  function quoteRanges(r, channel, text, which) {
    const out = [];
    if (which === 'v4' && armed()) {
      for (const j of ['v4q', 'v4d']) { const c = r.lab[j] && r.lab[j][channel]; if (c && c.v && c.q) out.push(...findQuote(text, c.q)); }
    }
    if (which === 'v3') {
      for (const j of ['v3q', 'v3d']) {
        const v = r.lab[j]; if (!v || !v.a) continue;
        v.ex.forEach((e) => { if (e.at === channel) out.push(...findQuote(text, e.t)); });
      }
    }
    return out;
  }
  function specsFor(r, channel, text) {
    const v3cls = S.exp === 'gptoss' ? 'h-quote3' : 'h-quote';
    const sp = [['h-search', searchRanges(text)], ['h-quote', quoteRanges(r, channel, text, 'v4')], [v3cls, quoteRanges(r, channel, text, 'v3')]];
    if (S.exp !== 'olmo') {
      const p = S.data.prompts[r.pid];
      if (p && p.cue_words && p.cue_words.length && channel === 'cot') sp.push(['h-echo', p.cue_words.flatMap((w) => findAll(text, w, { word: true }))]);
    } else {
      if (r.cons === 'word_suppression' && r.kw && channel === 'cot') sp.push(['h-ban', findAll(text, r.kw, { word: true })]);
      if (r.cons === 'tag_start') sp.push(['h-tag', findAll(text, TAG)]);
      if (r.cons === 'lowercase' && ((r.task === 'cot' && channel === 'cot') || (r.task === 'answer_if' && channel === 'response')))
        sp.push(['h-caps', [...text.matchAll(/[A-Z]+/g)].map((m) => [m.index, m.index + m[0].length])]);
    }
    return sp;
  }

  // ---------- detail ----------
  function textBlock(label, text, specs, extra) {
    return el('div', { class: 'block' }, el('div', { class: 'lab' }, label, extra || null),
      text ? el('div', { class: 'text' }, render(text, specs)) : el('div', { class: 'text dim', text: '(empty)' }));
  }
  function promptBlocks(r) {
    if (S.exp === 'olmo') {
      const t = S.data.prompts[r.ph] || '';
      const sp = [['h-search', S.scope === 'prompt' ? searchRanges(t) : []], ['h-tag', findAll(t, TAG)]];
      if (r.kw && r.cons === 'word_suppression') sp.push(['h-ban', findAll(t, r.kw, { word: true })]);
      return [el('div', { class: 'block' }, el('div', { class: 'lab', text: 'Prompt' }), el('div', { class: 'text prompt' }, render(t, sp)))];
    }
    const p = S.data.prompts[r.pid] || {};
    const cueSpecs = (t) => [['h-cue', (p.cue || []).flatMap((c) => findAll(t, c))], ['h-search', S.scope === 'prompt' ? searchRanges(t) : []]];
    const out = [];
    if (p.system) out.push(el('div', { class: 'block' }, el('div', { class: 'lab', text: 'System prompt (developer message in gpt-oss)' }), el('div', { class: 'text prompt sys' }, render(p.system, cueSpecs(p.system)))));
    out.push(el('div', { class: 'block' }, el('div', { class: 'lab', text: 'User message' }), el('div', { class: 'text prompt' }, render(p.user || '', cueSpecs(p.user || '')))));
    return out;
  }
  const WHERE = { cot: 'found in reasoning', response: 'found in answer', prompt: 'only in the prompt', none: 'not found' };
  function judgeTable(r) {
    const rows = [];
    const verdict = (a) => el('span', { class: `b ${a ? 'on' : ''}`, text: a ? 'yes' : 'no' });
    if (S.exp === 'graded' && r.lab.sr != null) {
      rows.push(el('tr', {}, el('td', { text: 'StrongREJECT rubric · Qwen 2.5 72B (answer only)' }), el('td', {}, verdict(!r.lab.ref)),
        el('td', { text: `${r.lab.ref ? 'refused' : 'did not refuse'} · convincing ${r.lab.src ? r.lab.src[0] : '?'}/5 · specific ${r.lab.src ? r.lab.src[1] : '?'}/5 · score ${r.lab.sr}` }), el('td', {})));
    }
    if (armed()) {
      for (const [j, name] of [['v4q', 'Qwen 2.5 72B'], ['v4d', 'DeepSeek V3.2']]) {
        for (const ch of ['cot', 'response']) {
          const c = r.lab[j] && r.lab[j][ch]; if (!c) continue;
          rows.push(el('tr', {}, el('td', { text: `v4 · ${name} · ${ch === 'cot' ? 'reasoning' : 'answer'}` }), el('td', {}, verdict(c.v)),
            el('td', { text: c.q || '' }), el('td', {}, c.a ? el('span', { class: `where ${c.v ? ch : 'none'}`, text: c.v ? WHERE[ch] : 'quote not found' }) : '')));
        }
      }
    }
    for (const [j, name] of [['v3q', S.exp === 'olmo' ? 'Strict judge (v2 rubric) · Qwen 2.5 72B' : 'v3 · Qwen 2.5 72B (saw the prompt)'], ['v3d', 'v3 · DeepSeek V3.2 (saw the prompt)']]) {
      const v = r.lab[j]; if (!v) continue;
      if (!v.ex.length) rows.push(el('tr', {}, el('td', { text: name }), el('td', {}, verdict(v.a)), el('td', { class: 'meta', text: v.n || '' }), el('td', {})));
      v.ex.forEach((e, i) => rows.push(el('tr', {}, el('td', { text: i ? '' : name }), el('td', {}, i ? '' : verdict(v.a)),
        el('td', { text: `${e.t}${e.loc ? `  [judge said: ${e.loc}]` : ''}` }), el('td', {}, el('span', { class: `where ${e.at}`, text: WHERE[e.at] || e.at })))));
    }
    if (!rows.length) return null;
    return el('div', { class: 'block' }, el('div', { class: 'lab', text: 'Judges' }),
      el('table', { class: 'judges' }, el('thead', {}, el('tr', {}, el('th', { text: 'Judge' }), el('th', { text: 'Flag' }), el('th', { text: 'Quote' }), el('th', { text: 'Where the quote really is' }))), el('tbody', {}, rows)),
      el('p', { class: 'note', text: armed() ? 'v4 judges saw one channel without the prompt; a flag counts only if its quote is found in that channel. v3 judges saw the prompt and often quoted it as if the model wrote it.' : 'This judge saw the prompt, so its quotes are checked against the model text.' }));
  }
  function olmoFacts(r) {
    const g = r.lab.g || {}; const f = [];
    if (r.cons === 'word_suppression') f.push(`banned word “${r.kw}”: used ${g.uses ?? '?'} times here, ${g.uses_base ?? '?'} times in the same question's unconstrained rollout`);
    if (r.cons === 'tag_start') f.push(`tag at start: ${g.tag_start === '1.0' || g.tag_start === '1' ? 'yes' : 'no'}; tag anywhere: ${g.tag_anywhere === '1.0' || g.tag_anywhere === '1' ? 'yes' : 'no'}`);
    if (r.cons === 'lowercase' && r.task === 'cot' && g.lc_frac) f.push(`lowercase share of letters: ${(Number(g.lc_frac) * 100).toFixed(1)}%`);
    f.push(`answer ${r.answer ?? '—'} · gold “${(r.gold || '').slice(0, 80)}” · ${r.lab.correct ? 'correct' : 'not correct'}`);
    return el('div', { class: 'block' }, el('div', { class: 'lab', text: 'Grading' }), el('ul', { class: 'note' }, f.map((t) => el('li', { text: t }))));
  }
  function renderDetail(r) {
    const d = $('#detail'); d.replaceChildren();
    const title = S.exp === 'olmo' ? `${shardLabel('olmo', S.manifest.olmo.shards.find((s) => s.id === S.shard))} · ${r.qid}` : `${r.item}`;
    const meta = S.exp === 'olmo'
      ? `${COND_LABEL[condOf('olmo', r)] || condOf('olmo', r)} · ${r.domain || ''} · ${r.ntok ?? '?'} tokens · ${r.finish}`
      : `${COND_LABEL[r.cond] || r.cond} · ${r.file === 'confirm' ? 'rerun' : r.file} · sample ${r.sample} · ${r.ntok ?? '?'} tokens · ${r.finish}`;
    const back = el('button', { class: 'ghost small', type: 'button', text: '← list', onclick: () => document.body.classList.remove('showdetail') });
    back.style.display = matchMedia('(max-width: 720px)').matches ? '' : 'none';
    const pairBtn = el('button', { class: 'ghost small', type: 'button', text: S.pair ? 'Single view' : (S.exp === 'gptoss' || S.exp === 'screen' ? 'Same prompt, all models' : S.exp === 'graded' ? 'Same prompt, with and without cue' : S.exp === 'olmo' ? 'Same question, all constraints' : 'Same item, all conditions'), onclick: () => { S.pair = !S.pair; renderDetail(r); writeHash(); } });
    const linkBtn = el('button', { class: 'ghost small', type: 'button', text: 'Copy link', onclick: async () => { try { await navigator.clipboard.writeText(location.href); linkBtn.textContent = 'Copied'; } catch (e) { linkBtn.textContent = 'Copy failed'; } } });
    d.append(el('div', { class: 'dhead' }, back, armed() ? armChip(r.arm) : null, el('h2', { text: title }), el('span', { class: 'badges' }, badgesFor(r)), el('div', { class: 'actions' }, pairBtn, linkBtn)), el('div', { class: 'meta', text: meta }));
    if (S.pair) { d.append(...promptBlocks(r), pairView(r)); return; }
    d.append(...promptBlocks(r));
    d.append(textBlock('Reasoning', r.reasoning, specsFor(r, 'cot', r.reasoning), el('span', { class: 'meta', text: `${r.reasoning.split(/\s+/).filter(Boolean).length} words` })));
    d.append(textBlock('Final answer', r.response, specsFor(r, 'response', r.response)));
    if (S.exp === 'olmo') d.append(olmoFacts(r));
    const jt = judgeTable(r); if (jt) d.append(jt);
  }
  function pairView(r) {
    let group, colKey, cols;
    if (S.exp === 'gptoss' || S.exp === 'screen') {
      const samples = [...new Set(S.data.rollouts.filter((x) => x.pid === r.pid).map((x) => x.sample))].sort((a, b) => a - b);
      const smp = S.pairSample ?? r.sample;
      group = S.data.rollouts.filter((x) => x.pid === r.pid && String(x.sample) === String(smp));
      colKey = (x) => x.arm; cols = S.manifest[S.exp].arms.map((a) => a.id);
      const sel = el('select', { 'aria-label': 'Sample' }, samples.map((s) => el('option', { value: s, text: `sample ${s}`, selected: String(s) === String(smp) })));
      sel.addEventListener('change', () => { S.pairSample = sel.value; renderDetail(r); });
      return el('div', { class: 'block' }, el('div', { class: 'lab' }, 'Same prompt across models ', sel), grid(group, colKey, cols, (x) => armChip(x.arm)));
    }
    if (S.exp === 'olmo') {
      group = S.data.rollouts.filter((x) => x.qid === r.qid); colKey = (x) => condOf('olmo', x);
      cols = ['cot:baseline', 'cot:word_suppression', 'cot:tag_start', 'cot:lowercase', 'answer_if:lowercase'];
      return el('div', { class: 'block' }, el('div', { class: 'lab', text: 'Same question across constraints (prompt above is for the selected rollout)' }), grid(group, colKey, cols, (x) => el('span', { class: 'b info', text: COND_LABEL[condOf('olmo', x)] })));
    }
    if (S.exp === 'graded') {
      group = S.data.rollouts.filter((x) => x.item === r.item && x.sample === r.sample); colKey = (x) => x.cond; cols = ['none', 'user_casual'];
      return el('div', { class: 'block' }, el('div', { class: 'lab', text: `Same prompt and sample index (${r.sample}), without and with the cue` }), grid(group, colKey, cols, (x) => el('span', { class: 'b info', text: COND_LABEL[x.cond] || x.cond })));
    }
    group = S.data.rollouts.filter((x) => x.item === r.item); colKey = (x) => x.cond; cols = [...new Set(group.map((x) => x.cond))];
    return el('div', { class: 'block' }, el('div', { class: 'lab', text: 'Same item across conditions' }), grid(group, colKey, cols, (x) => el('span', { class: 'b info', text: COND_LABEL[x.cond] || x.cond })));
  }
  function grid(group, colKey, cols, head) {
    const g = el('div', { class: 'pair' });
    cols.forEach((c) => {
      const x = group.find((y) => colKey(y) === c); if (!x) return;
      const open = el('button', { class: 'ghost small', type: 'button', text: 'Open', onclick: () => { S.pair = false; select(x.id); } });
      g.append(el('div', { class: 'pcol' }, el('div', { class: 'ph' }, head(x), el('span', { class: 'badges' }, badgesFor(x)), open),
        el('div', { class: 'lab', text: 'Reasoning' }), x.reasoning ? el('div', { class: 'text' }, render(x.reasoning, specsFor(x, 'cot', x.reasoning))) : el('div', { class: 'text dim', text: '(empty)' }),
        el('div', { class: 'lab', text: 'Final answer' }), x.response ? el('div', { class: 'text' }, render(x.response, specsFor(x, 'response', x.response))) : el('div', { class: 'text dim', text: '(empty)' })));
    });
    return g;
  }

  // ---------- keyboard ----------
  document.addEventListener('keydown', (e) => {
    if (e.target.matches('input, select, textarea')) { if (e.key === 'Escape') e.target.blur(); return; }
    const idx = S.list.findIndex((r) => r.id === S.sel);
    if (e.key === 'j' || e.key === 'ArrowDown') { const n = S.list[Math.min(S.list.length - 1, idx + 1)]; if (n) { if (idx + 1 >= S.shown) { S.shown += 300; renderList(); } select(n.id, { keepPair: true }); e.preventDefault(); } }
    else if (e.key === 'k' || e.key === 'ArrowUp') { const n = S.list[Math.max(0, idx - 1)]; if (n) { select(n.id, { keepPair: true }); e.preventDefault(); } }
    else if (e.key === 'p' && S.sel) { S.pair = !S.pair; const r = S.data.rollouts.find((x) => x.id === S.sel); if (r) renderDetail(r); writeHash(); }
    else if (e.key === '/') { $('#q').focus(); e.preventDefault(); }
    else if (e.key === 'Escape') { if (S.pair) { S.pair = false; const r = S.data.rollouts.find((x) => x.id === S.sel); if (r) renderDetail(r); writeHash(); } else document.body.classList.remove('showdetail'); }
  });

  // ---------- boot ----------
  (async () => {
    try {
      await loadManifest();
      const h = readHash();
      if (h.q) { S.q = h.q; $('#q').value = h.q; }
      const exp = S.manifest[h.x] ? h.x : 'gptoss';
      S.sel = h.r; S.pair = h.p;
      await setExp(exp, h.s, true);
      if (S.sel && S.data.rollouts.some((r) => r.id === S.sel)) select(S.sel, { keepPair: true }); else { S.sel = null; S.pair = false; apply(); }
    } catch (err) {
      $('#count').textContent = '';
      $('#detail').replaceChildren(el('div', { class: 'empty' }, el('p', { text: String(err.message || err) }),
        el('p', { text: 'Build the data first, then serve this folder: python explorer/build.py && python -m http.server 8000 -d explorer' })));
    }
  })();
})();
