/* 站内搜索 · Day 8 (2026-11-18) + 本页范围搜索 (2026-11-26, v2)
 * data-scope: 搜索框所在 .site-search 加 data-scope="/main-quest-" 后, 只在该前缀的索引页里搜; 不设则全站搜。
 * 旧页面不设 data-scope, 行为与 v1 完全一致。
 */
/* 站内搜索 · Day 8 (2026-11-18)
 * 纯前端实现: fetch search-index.json, 本地匹配, 不依赖服务端。
 * 容错: 简繁互通(繁转简归一)、别名(白银人马->白银莱尼尔、乌萨祖姆->乌萨诸马等)、
 * 部分匹配(子串匹配, 如"乌萨"可命中"乌萨诸马")。
 * 统计: 只记查询词与次数, 存 localStorage 键 zelda_search_stats_v1, 不记任何个人信息。
 * 不动 main.js / style.css, 故不涉及全站版号升级; 本文件独立加载 search.js?v=1。
 */
(function () {
  'use strict';

  var INDEX_URL = 'search-index.json';
  var STATS_KEY = 'zelda_search_stats_v1';
  var MAX_RESULTS = 8;
  var MIN_LEN = 1;

  /* 繁体 -> 简体归一(只收与本站检索相关的常用字) */
  var TRAD_MAP = {
    '龍': '龙', '氣': '气', '烏': '乌', '薩': '萨', '諸': '诸', '麼': '么', '嗎': '吗', '點': '点', '盧': '卢', '亞': '亚', '歷': '历', '壓': '压', '澤': '泽', '羅': '罗', '爾': '尔', '蘭': '兰', '絲': '丝', '維': '维', '奧': '奥', '歐': '欧', '漢': '汉', '鬥': '斗', '場': '场', '報': '报', '崑': '昆', '崙': '仑', '劍': '剑', '銀': '银', '廟': '庙', '寶': '宝', '靈': '灵', '術': '术', '鑽': '钻', '礦': '矿', '樹': '树', '葉': '叶', '蘋': '苹', '果': '果', '鐵': '铁', '銅': '铜', '藥': '药', '體': '体', '餘': '余', '還': '还', '過': '过', '邊': '边', '達': '达', '進': '进', '遠': '远', '選': '选', '關': '关', '開': '开', '間': '间', '問': '问', '題': '题', '頭': '头', '臉': '脸', '髮': '发', '鬆': '松', '討': '讨', '戰': '战', '擊': '击', '藍': '蓝', '紅': '红', '白': '白', '黃': '黄', '綠': '绿', '飛': '飞', '馬': '马', '鳥': '鸟', '龜': '龟', '魚': '鱼', '鷹': '鹰', '導': '导', '圖': '图', '錄': '录', '級': '级', '繫': '系', '續': '续', '對': '对', '說': '说', '話': '话', '讀': '读', '學': '学', '覺': '觉', '覽': '览', '觀': '观', '視': '视', '親': '亲', '見': '见', '貝': '贝', '貨': '货', '買': '买', '賣': '卖', '價': '价', '錢': '钱', '鑄': '铸', '鍊': '炼', '鍋': '锅', '爐': '炉', '竈': '灶', '廳': '厅', '灣': '湾', '島': '岛', '峽': '峡', '嶺': '岭', '巖': '岩', '險': '险', '隱': '隐', '隨': '随', '雜': '杂', '雞': '鸡', '鴨': '鸭', '鵝': '鹅', '豬': '猪', '貓': '猫', '狗': '狗', '狼': '狼', '獅': '狮', '虎': '虎', '豹': '豹', '蛇': '蛇', '蟲': '虫', '蟻': '蚁', '蜂': '蜂', '蝶': '蝶', '螢': '萤', '蛙': '蛙', '蝦': '虾', '蟹': '蟹', '參': '参', '蔘': '参', '薑': '姜', '蔥': '葱', '蒜': '蒜', '椒': '椒', '鹽': '盐', '糖': '糖', '麵': '面', '飯': '饭', '餅': '饼', '餃': '饺', '湯': '汤', '羹': '羹', '醬': '酱', '醋': '醋'
  };

  /* 查询词 -> 索引里的规范词(别名展开, 用于标题匹配) */
  var ALIAS_TO_CANON = {
    '白银人马': '白银莱尼尔', '白鬃人马': '白鬃莱尼尔', '蓝鬃人马': '蓝鬃莱尼尔',
    '红鬃人马': '红鬃莱尼尔', '银人马': '白银莱尼尔', '人马': '莱尼尔',
    '乌萨祖姆': '乌萨诸马', '塔列镇': '一始村', '格鲁多': '格鲁德',
    '佐拉': '卓拉', '太阳花': '向阳草', '佐纳乌': '左纳乌',
    '克洛格': '呀哈哈', 'korok': '呀哈哈', '莫尔德拉吉克': '巨霸迦马',
    'molduga': '巨霸迦马', '三头龙': '古栗欧克', 'gleeok': '古栗欧克',
    '吉波多': '吉波得', 'gibdo': '吉波得', 'aerocuda': '卡库达',
    '图林': '丘栗', '尤诺波': '阿沅', 'master sword': '大师之剑',
    '树根': '破魔树根', 'lightroot': '破魔树根', '祠': '神庙',
    'shrine': '神庙', 'blupee': '卢咪', 'blood moon': '血月',
    'paraglider': '滑翔伞'
  };

  var TYPE_ORDER = { '首页': 0, '专栏': 1, '攻略': 2, '收集': 3, 'Boss': 4, '工具': 5, '其他': 6 };

  function normalize(s) {
    s = String(s || '');
    s = s.replace(/[\uFF01-\uFF5E]/g, function (ch) {
      return String.fromCharCode(ch.charCodeAt(0) - 0xFEE0);
    });
    s = s.replace(/　/g, ' ');
    s = s.split('').map(function (ch) { return TRAD_MAP[ch] || ch; }).join('');
    return s.toLowerCase().replace(/\s+/g, ' ').trim();
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* 单个 token 在一页上的最佳匹配档位分 */
  function tokenScore(page, tok, canon) {
    var title = normalize(page.title || '');
    var summary = normalize(page.summary || '');
    var kws = (page.keywords || []).map(normalize);
    var aliases = (page.aliases || []).map(normalize);
    var i, k;
    if (title && title.indexOf(tok) !== -1) return 100;
    if (canon && canon !== tok && title && title.indexOf(canon) !== -1) return 95;
    for (i = 0; i < aliases.length; i++) if (aliases[i] === tok) return 80;
    if (canon && canon !== tok) {
      for (i = 0; i < aliases.length; i++) if (aliases[i] === canon) return 78;
    }
    for (i = 0; i < kws.length; i++) if (kws[i] === tok) return 60;
    for (i = 0; i < kws.length; i++) if (kws[i].indexOf(tok) !== -1) return 55;
    for (i = 0; i < kws.length; i++) if (tok.indexOf(kws[i]) !== -1 && kws[i].length >= 2) return 50;
    if (summary && summary.indexOf(tok) !== -1) return 40;
    if (canon && canon !== tok && summary && summary.indexOf(canon) !== -1) return 38;
    return 0;
  }

  function searchIndex(pages, rawQuery) {
    var q = normalize(rawQuery);
    if (!q) return [];
    var tokens = q.split(' ').filter(function (t) { return t; });
    var results = [];
    var p, i, score, ok, coordBonus;
    for (i = 0; i < pages.length; i++) {
      p = pages[i];
      score = 0; ok = true;
      for (var t = 0; t < tokens.length; t++) {
        var tok = tokens[t];
        var canon = normalize(ALIAS_TO_CANON[tok] || ALIAS_TO_CANON[normalize(tok)] || tok);
        var s = tokenScore(p, tok, canon);
        if (s === 0) { ok = false; break; }
        score += s;
      }
      if (!ok) continue;
      coordBonus = 0;
      if (q.indexOf('坐标') !== -1 && p.coords && p.coords.length) {
        coordBonus = Math.min(p.coords.length, 8);
      }
      results.push({ page: p, score: score + coordBonus, coords: (p.coords || []).length });
    }
    results.sort(function (a, b) {
      if (b.score !== a.score) return b.score - a.score;
      if (b.coords !== a.coords) return b.coords - a.coords;
      var ta = TYPE_ORDER[a.page.type] == null ? 9 : TYPE_ORDER[a.page.type];
      var tb = TYPE_ORDER[b.page.type] == null ? 9 : TYPE_ORDER[b.page.type];
      if (ta !== tb) return ta - tb;
      return String(a.page.title).localeCompare(String(b.page.title), 'zh-CN');
    });
    return results.slice(0, MAX_RESULTS);
  }

  function totalMatches(pages, rawQuery) {
    var q = normalize(rawQuery);
    if (!q) return 0;
    var tokens = q.split(' ').filter(function (t) { return t; });
    var n = 0;
    for (var i = 0; i < pages.length; i++) {
      var ok = true;
      for (var t = 0; t < tokens.length; t++) {
        var tok = tokens[t];
        var canon = normalize(ALIAS_TO_CANON[tok] || tok);
        if (tokenScore(pages[i], tok, canon) === 0) { ok = false; break; }
      }
      if (ok) n++;
    }
    return n;
  }

  /* ---- 本地统计: 只记查询词与次数 ---- */
  function readStats() {
    try {
      var raw = window.localStorage.getItem(STATS_KEY);
      if (!raw) return { v: 1, total: 0, queries: {} };
      var d = JSON.parse(raw);
      if (!d || typeof d !== 'object' || !d.queries) return { v: 1, total: 0, queries: {} };
      return d;
    } catch (e) { return { v: 1, total: 0, queries: {} }; }
  }

  function recordStat(rawQuery) {
    var q = normalize(rawQuery);
    if (!q || q.length < 2) return;
    try {
      var d = readStats();
      d.total = (d.total || 0) + 1;
      d.queries[q] = (d.queries[q] || 0) + 1;
      d.updated = new Date().toISOString().slice(0, 10);
      window.localStorage.setItem(STATS_KEY, JSON.stringify(d));
    } catch (e) { /* 无痕/禁用存储时静默跳过 */ }
  }

  /* ---- 索引加载 ---- */
  var indexPromise = null;
  function loadIndex() {
    if (!indexPromise) {
      indexPromise = window.fetch(INDEX_URL, { credentials: 'same-origin' })
        .then(function (r) {
          if (!r.ok) throw new Error('index http ' + r.status);
          return r.json();
        })
        .then(function (d) { return d.pages || []; })
        .catch(function (e) { indexPromise = null; throw e; });
    }
    return indexPromise;
  }

  function highlight(title, rawQuery) {
    var q = String(rawQuery || '').trim();
    if (!q) return esc(title);
    var idx = title.indexOf(q);
    if (idx === -1) return esc(title);
    return esc(title.slice(0, idx)) + '<mark>' + esc(q) + '</mark>' + esc(title.slice(idx + q.length));
  }

  /* 结果面板用 position:fixed 并挂到 body 下: 首页 hero 与专栏页头都有
   * overflow:hidden, 绝对定位的下拉框会被裁掉, fixed + JS 定位才能完整显示。 */
  function positionPanel(box, panel) {
    var input = box.querySelector('.site-search-input');
    var form = box.querySelector('.site-search-form');
    if (!panel || !input || panel.hidden) return;
    var r = (form || input).getBoundingClientRect();
    var vw = window.innerWidth || (document.documentElement && document.documentElement.clientWidth) || 0;
    var left = Math.max(8, r.left);
    var width = Math.min(r.width, vw - 16);
    if (left + width > vw - 8) left = Math.max(8, vw - 8 - width);
    panel.style.left = left + 'px';
    panel.style.top = (r.bottom + 8) + 'px';
    panel.style.width = width + 'px';
  }

  function render(box, panel, results, total, rawQuery, failed) {
    if (!panel) return;
    if (failed) {
      panel.hidden = false;
      panel.innerHTML = '<div class="site-search-empty">搜索索引加载失败，请刷新页面再试。</div>';
      positionPanel(box, panel);
      return;
    }
    if (!rawQuery || !String(rawQuery).trim()) { panel.hidden = true; panel.innerHTML = ''; return; }
    if (!results.length) {
      panel.hidden = false;
      var hint = '神庙、呀哈哈、料理';
      if (box.getAttribute('data-scope')) {
        var sc = [];
        box.querySelectorAll('.site-search-chip').forEach(function (c) { sc.push(c.getAttribute('data-q') || c.textContent); });
        if (sc.length) hint = sc.join('、');
      }
      panel.innerHTML = '<div class="site-search-empty">没有找到“' + esc(rawQuery) +
        '”相关攻略，换个词试试，如：' + esc(hint) + '。</div>';
      positionPanel(box, panel);
      return;
    }
    var h = '<div class="site-search-count">找到 ' + total + ' 个相关结果</div>';
    for (var i = 0; i < results.length; i++) {
      var p = results[i].page;
      h += '<a class="site-search-item" href="' + esc(p.url) + '">' +
        '<div class="site-search-item-title"><span class="site-search-item-type">' + esc(p.type) +
        '</span>' + highlight(p.title, rawQuery) + '</div>' +
        (p.summary ? '<div class="site-search-item-summary">' + esc(p.summary) + '</div>' : '') +
        '</a>';
    }
    panel.hidden = false;
    panel.innerHTML = h;
    positionPanel(box, panel);
  }

  function initBox(box) {
    var form = box.querySelector('.site-search-form');
    var input = box.querySelector('.site-search-input');
    var panel = box.querySelector('.site-search-results');
    if (!form || !input || !panel) return;
    /* 本页搜索范围: data-scope="/main-quest-" 时只在该前缀的索引页里搜; 不设则全站搜。 */
    var scope = box.getAttribute('data-scope') || '';
    function applyScope(pages) {
      if (!scope) return pages;
      return pages.filter(function (pg) { return String(pg.url || '').indexOf(scope) === 0; });
    }
    if (document.body && panel.parentNode !== document.body) document.body.appendChild(panel);
    var reposition = function () { if (!panel.hidden) positionPanel(box, panel); };
    window.addEventListener('scroll', reposition, true);
    window.addEventListener('resize', reposition);
    window.addEventListener('orientationchange', reposition);
    var timer = null;
    var lastRecorded = '';
    var activeIdx = -1;
    var currentItems = [];

    function run(q, record) {
      if (!q || !String(q).trim()) {
        panel.hidden = true; panel.innerHTML = ''; currentItems = []; activeIdx = -1;
        return;
      }
      loadIndex().then(function (pages) {
        pages = applyScope(pages);
        var res = searchIndex(pages, q);
        var total = totalMatches(pages, q);
        render(box, panel, res, total, q, false);
        currentItems = Array.prototype.slice.call(panel.querySelectorAll('.site-search-item'));
        activeIdx = -1;
        if (record) {
          var nq = normalize(q);
          if (nq !== lastRecorded) { recordStat(q); lastRecorded = nq; }
        }
      }).catch(function () { render(box, panel, [], 0, q, true); });
    }

    function setActive(idx) {
      currentItems.forEach(function (el, i) {
        if (i === idx) el.classList.add('active'); else el.classList.remove('active');
      });
      activeIdx = idx;
    }

    input.addEventListener('input', function () {
      if (timer) clearTimeout(timer);
      timer = setTimeout(function () { run(input.value, true); }, 250);
    });
    input.addEventListener('focus', function () {
      if (input.value.trim()) run(input.value, false);
    });
    input.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') { panel.hidden = true; input.blur(); return; }
      if (ev.key === 'ArrowDown' || ev.key === 'ArrowUp') {
        if (!currentItems.length) return;
        ev.preventDefault();
        var next = ev.key === 'ArrowDown' ? activeIdx + 1 : activeIdx - 1;
        if (next < 0) next = currentItems.length - 1;
        if (next >= currentItems.length) next = 0;
        setActive(next);
        return;
      }
      if (ev.key === 'Enter') {
        ev.preventDefault();
        if (activeIdx >= 0 && currentItems[activeIdx]) {
          recordStat(input.value);
          window.location.href = currentItems[activeIdx].getAttribute('href');
        } else {
          doSubmit();
        }
      }
    });
    function doSubmit() {
      var q = input.value;
      if (!q.trim()) return;
      recordStat(q);
      loadIndex().then(function (pages) {
        pages = applyScope(pages);
        var res = searchIndex(pages, q);
        if (res.length) window.location.href = res[0].page.url;
      }).catch(function () { /* 停留在当前页, 面板已显示失败提示 */ });
    }
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      doSubmit();
    });
    box.querySelectorAll('.site-search-chip').forEach(function (chip) {
      chip.addEventListener('click', function () {
        input.value = chip.getAttribute('data-q') || chip.textContent;
        input.focus();
        run(input.value, true);
      });
    });
    document.addEventListener('click', function (ev) {
      if (!box.contains(ev.target) && !panel.contains(ev.target)) { panel.hidden = true; }
    });
  }

  function init() {
    var boxes = document.querySelectorAll('.site-search');
    if (!boxes.length) return;
    loadIndex().catch(function () { /* 首次加载失败不阻塞页面, 搜索时再试 */ });
    boxes.forEach(initBox);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }

  /* 供 node 自查与 Day 18 复盘复用 */
  window.__zeldaSearch = {
    normalize: normalize,
    searchIndex: searchIndex,
    totalMatches: totalMatches,
    statsKey: STATS_KEY,
    readStats: readStats
  };
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
      normalize: normalize, searchIndex: searchIndex, totalMatches: totalMatches,
      statsKey: STATS_KEY
    };
  }
})();
