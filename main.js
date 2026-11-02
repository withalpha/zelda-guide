/* ================================================
   王国之泪攻略网站 - 全局 JavaScript
   ================================================ */

// ── 汉堡菜单 ──────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.getElementById('hamburger');
  const nav       = document.getElementById('mainNav');

  // ── 创建遮罩层 ──
  const overlay = document.createElement('div');
  overlay.className = 'nav-overlay';
  document.body.appendChild(overlay);

  function closeMenu() {
    hamburger.classList.remove('open');
    nav.classList.remove('open');
    overlay.classList.remove('open');
  }

  if (hamburger && nav) {
    hamburger.addEventListener('click', () => {
      const isOpen = nav.classList.contains('open');
      if (isOpen) {
        closeMenu();
      } else {
        hamburger.classList.add('open');
        nav.classList.add('open');
        overlay.classList.add('open');
      }
    });

    // 点击遮罩关闭菜单
    overlay.addEventListener('click', closeMenu);

    // 点击导航项后关闭菜单（下拉触发项除外）
    nav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', (e) => {
        // 如果是下拉触发项，不关闭菜单
        if (a.closest('.nav-dropdown') && a.parentElement.classList.contains('nav-dropdown')) return;
        closeMenu();
      });
    });
  }

  // ── 下拉菜单（点击触发 + fixed 定位）──────────────────
  initDropdowns();

  // ── 通用打勾（仅在未被页面自定义接管时运行）──
  const hasShrineTable = !!document.getElementById('shrineTableBody');
  const hasSqCheckBtn  = !!document.querySelector('.sq-check-btn');
  const hasSqList      = !!document.getElementById('sqList');
  const hasRootList    = !!document.getElementById('rootList');

  if (!hasShrineTable && !hasSqCheckBtn && !hasSqList && !hasRootList) {
    initCheckboxes();
  }

  initAccordions();
  initMainQuestProgress();
  initFadeIn();
});

// ── 下拉菜单初始化 ──────────────────────────
function initDropdowns() {
  const isMobile = () => window.innerWidth <= 768;

  document.querySelectorAll('.nav-dropdown').forEach(dropdown => {
    const trigger = dropdown.querySelector(':scope > a');
    const menu    = dropdown.querySelector('.nav-dropdown-menu');
    if (!trigger || !menu) return;

    // 点击触发项：切换 open 状态
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();

      const isOpen = dropdown.classList.contains('open');

      // 先关闭所有其他下拉
      document.querySelectorAll('.nav-dropdown.open').forEach(d => {
        d.classList.remove('open');
      });

      if (!isOpen) {
        dropdown.classList.add('open');
        // 桌面端：用 fixed 定位，计算位置
        if (!isMobile()) {
          positionMenu(trigger, menu);
        }
      }
    });
  });

  // 点击页面其他地方关闭所有下拉
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-dropdown')) {
      document.querySelectorAll('.nav-dropdown.open').forEach(d => {
        d.classList.remove('open');
      });
    }
  });

  // 窗口滚动/缩放时重新定位
  window.addEventListener('scroll', () => {
    document.querySelectorAll('.nav-dropdown.open').forEach(d => {
      const t = d.querySelector(':scope > a');
      const m = d.querySelector('.nav-dropdown-menu');
      if (t && m && !isMobile()) positionMenu(t, m);
    });
  }, { passive: true });

  window.addEventListener('resize', () => {
    document.querySelectorAll('.nav-dropdown.open').forEach(d => {
      const t = d.querySelector(':scope > a');
      const m = d.querySelector('.nav-dropdown-menu');
      if (t && m && !isMobile()) positionMenu(t, m);
    });
  });
}

// 计算下拉菜单的 fixed 定位坐标
function positionMenu(trigger, menu) {
  const rect = trigger.getBoundingClientRect();
  const menuW = menu.offsetWidth || 170;
  // 水平居中对齐触发项，防止超出视口右边
  let left = rect.left + rect.width / 2 - menuW / 2;
  if (left + menuW > window.innerWidth - 8) left = window.innerWidth - menuW - 8;
  if (left < 8) left = 8;
  menu.style.top  = (rect.bottom + 6) + 'px';
  menu.style.left = left + 'px';
}


// ── 通用 check 初始化（从 localStorage 恢复状态）
// 仅用于 main-quest.html（.quest-check）
function initCheckboxes() {
  const pageKey = window.location.pathname;

  document.querySelectorAll('.quest-check').forEach((btn, i) => {
    const storageKey = pageKey + '_check_' + i;
    if (localStorage.getItem(storageKey) === 'done') {
      btn.classList.add('done');
      markParentDone(btn);
    }
    btn._storageKey = storageKey;
  });
}

// ── 通用打勾函数（供 main-quest.html HTML 调用）
function toggleCheck(btn) {
  btn.classList.toggle('done');
  markParentDone(btn);
  if (btn._storageKey) {
    localStorage.setItem(btn._storageKey, btn.classList.contains('done') ? 'done' : '');
  }
  updateMainQuestProgress();
}

// 让父 quest-item 显示已完成样式
function markParentDone(btn) {
  const item = btn.closest('.quest-item');
  if (item) {
    item.style.opacity = btn.classList.contains('done') ? '0.5' : '1';
  }
}

// ── 神庙 check（shrine-unlock.html 自带完整版本，此处仅作备用）
function toggleShrineCheck(btn) {
  btn.classList.toggle('done');
  const allBtns = [...document.querySelectorAll('#shrineTableBody .shrine-check')];
  const idx = allBtns.indexOf(btn);
  const key = window.location.pathname + '_shrine_' + idx;
  localStorage.setItem(key, btn.classList.contains('done') ? 'done' : '');
  updateProgress();
}

// ── 主线进度更新
function initMainQuestProgress() {
  updateMainQuestProgress();
}

function updateMainQuestProgress() {
  const fill    = document.getElementById('mqProgressFill');
  const count   = document.getElementById('mqDoneCount');
  if (!fill) return;
  const done    = document.querySelectorAll('#mqList .quest-check.done').length;
  const total   = document.querySelectorAll('#mqList .quest-check').length;
  const pct     = total > 0 ? (done / total) * 100 : 0;
  fill.style.width  = pct + '%';
  if (count) count.textContent = done;
}

// ── 神庙进度更新（shrine-unlock.html 专用，由该页面内嵌脚本直接调用）
function updateProgress() {
  const done  = document.querySelectorAll('#shrineTableBody .shrine-check.done').length;
  const fill  = document.getElementById('shrineProgressFill');
  const count = document.getElementById('shrineDoneCount');
  if (fill)  fill.style.width = (done / 152 * 100) + '%';
  if (count) count.textContent = done;
}

// ── 手风琴（acc-item）
function initAccordions() {
  // 无需额外初始化，由 toggleAcc() 控制
}

function toggleAcc(header) {
  const body = header.nextElementSibling;
  const isOpen = header.classList.contains('open');
  header.classList.toggle('open', !isOpen);
  body.classList.toggle('open', !isOpen);
}

// ── 滚动时 navbar 阴影
window.addEventListener('scroll', () => {
  const nb = document.querySelector('.navbar');
  if (!nb) return;
  if (window.scrollY > 10) {
    nb.style.boxShadow = '0 2px 20px rgba(0,0,0,0.6)';
  } else {
    nb.style.boxShadow = 'none';
  }
});

// ── 页面入场淡入
function initFadeIn() {
  const style = document.createElement('style');
  style.textContent = `
    .fade-in { opacity:0; transform:translateY(20px); transition:opacity 0.5s ease, transform 0.5s ease; }
    .fade-in.visible { opacity:1; transform:none; }
  `;
  document.head.appendChild(style);

  const targets = document.querySelectorAll(
    '.category-card, .quest-item, .shrine-item, .recipe-card, .weapon-card, .info-card, .sq-card'
  );

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  targets.forEach(el => {
    el.classList.add('fade-in');
    observer.observe(el);
  });
}

// ── 平滑返回顶部
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}


// ════════════════════════════════════════════════════
//  内容保护 · 版权防护
// ════════════════════════════════════════════════════

(function () {
  'use strict';

  // ── 1. 禁用右键菜单 ─────────────────────────────
  document.addEventListener('contextmenu', function (e) {
    e.preventDefault();
  });

  // ── 2. 禁用常见复制快捷键 ────────────────────────
  document.addEventListener('keydown', function (e) {
    // Ctrl+C / Ctrl+U / Ctrl+S / Ctrl+A / F12 / Ctrl+Shift+I / Ctrl+Shift+J / Ctrl+Shift+C
    if (
      (e.ctrlKey && ['c','u','s','a','p'].includes(e.key.toLowerCase())) ||
      (e.ctrlKey && e.shiftKey && ['i','j','c'].includes(e.key.toLowerCase())) ||
      e.key === 'F12'
    ) {
      e.preventDefault();
    }
  });

  // ── 3. 禁用文字选择（正文区域）────────────────────
  document.addEventListener('selectstart', function (e) {
    // 允许 input/textarea 内选择（搜索框等）
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    e.preventDefault();
  });

  // ── 4. 禁用拖拽（防图片拖出）─────────────────────
  document.addEventListener('dragstart', function (e) {
    e.preventDefault();
  });

  // ── 5. 版权警告弹窗 ──────────────────────────────
  function showCopyWarning() {
    var existing = document.getElementById('_copyright_toast');
    if (existing) return;
    var toast = document.createElement('div');
    toast.id = '_copyright_toast';
    toast.style.cssText = [
      'position:fixed', 'top:50%', 'left:50%',
      'transform:translate(-50%,-50%)',
      'background:rgba(10,15,10,0.97)',
      'border:1px solid #c9a227',
      'border-radius:10px',
      'padding:28px 36px',
      'z-index:99999',
      'text-align:center',
      'font-family:Noto Sans SC,sans-serif',
      'box-shadow:0 8px 40px rgba(0,0,0,0.85)',
      'max-width:360px',
    ].join(';');
    toast.innerHTML =
      '<div style="font-size:2rem;margin-bottom:12px">🔒</div>' +
      '<div style="color:#c9a227;font-size:1rem;font-weight:700;margin-bottom:8px">版权保护</div>' +
      '<div style="color:#ccc;font-size:0.82rem;line-height:1.8">' +
        '本站原创内容受著作权法保护。<br>' +
        '未经许可，禁止转载、复制或以任何形式使用。' +
      '</div>' +
      '<button onclick="document.getElementById(\'_copyright_toast\').remove()" ' +
        'style="margin-top:18px;padding:7px 24px;background:rgba(201,162,39,0.15);' +
        'border:1px solid #c9a227;border-radius:6px;color:#c9a227;cursor:pointer;' +
        'font-size:0.82rem">我知道了</button>';
    document.body.appendChild(toast);
    setTimeout(function () {
      var t = document.getElementById('_copyright_toast');
      if (t) t.remove();
    }, 5000);
  }

  // ── 6. DevTools 打开检测（向控制台输出版权声明）────
  var _c = console;
  var msg = '%c 🔒 版权声明 \n%c 本站所有内容受著作权保护。\n 任何未授权的复制、抓取或爬取行为均属违法，\n 本站保留追究法律责任的权利。\n 联系授权：withalpha@proton.me';
  setTimeout(function () {
    _c.log(msg,
      'background:#0a0f0a;color:#c9a227;font-size:16px;font-weight:bold;padding:8px 16px;',
      'background:#0a0f0a;color:#ccc;font-size:12px;padding:4px 16px;line-height:1.8;'
    );
  }, 800);

})();


// ════════════════════════════════════════════════════
//  社交分享 · 悬浮侧边栏
// ════════════════════════════════════════════════════

(function () {
  'use strict';

  /* ── 工具：获取当前页面的分享文本和 URL ── */
  function getShareInfo() {
    var url   = encodeURIComponent(window.location.href);
    var title = encodeURIComponent(
      document.title || '塞尔达传说：王国之泪 · 全攻略'
    );
    var desc  = encodeURIComponent(
      (document.querySelector('meta[name="description"]') || {}).content ||
      '塞尔达传说王国之泪完整攻略站，神庙、料理、套装全覆盖！'
    );
    return { url: url, title: title, desc: desc, rawUrl: window.location.href };
  }

  /* ── 微博分享链接 ── */
  function weiboUrl(info) {
    return 'https://service.weibo.com/share/share.php?url=' + info.url +
           '&title=' + info.title + '%20' + info.desc +
           '&pic=&searchPic=false';
  }

  /* ── QQ 分享链接 ── */
  function qqUrl(info) {
    return 'https://connect.qq.com/widget/shareqq/index.html?url=' + info.url +
           '&title=' + info.title +
           '&summary=' + info.desc;
  }

  /* ── Twitter/X 分享链接 ── */
  function twitterUrl(info) {
    return 'https://twitter.com/intent/tweet?url=' + info.url +
           '&text=' + info.title;
  }

  /* ── 打开分享窗口（居中小窗）── */
  function openShare(url) {
    var w = 600, h = 500;
    var left = Math.max(0, (screen.width  - w) / 2);
    var top  = Math.max(0, (screen.height - h) / 2);
    window.open(url, '_blank',
      'width=' + w + ',height=' + h +
      ',left=' + left + ',top=' + top +
      ',toolbar=0,menubar=0,scrollbars=1,resizable=1'
    );
  }

  /* ── 构建侧边栏 HTML ── */
  function buildSidebar() {
    var sidebar = document.createElement('div');
    sidebar.className = 'share-sidebar';
    sidebar.setAttribute('aria-label', '分享本页面');

    // 微博
    var weibo = document.createElement('button');
    weibo.className  = 'share-btn share-btn--weibo';
    weibo.setAttribute('data-tip', '分享到微博');
    weibo.setAttribute('aria-label', '分享到微博');
    weibo.innerHTML  = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">' +
      '<path d="M9.827 18.863c-2.53.255-4.72-.978-4.895-2.752-.174-1.774 1.73-3.415 ' +
      '4.26-3.67 2.532-.255 4.72.978 4.894 2.752.175 1.774-1.728 3.415-4.26 3.67zm9.01-' +
      '10.4c-.28-.087-.473-.145-.326-.523.318-.8.35-1.49.006-1.983-.647-.924-2.418-.875-' +
      '4.45-.007 0 0-.636.278-.474-.226.313-1.026.266-1.885-.226-2.38-.972-.983-3.553.037-' +
      '5.773 2.28C5.953 7.686 5 9.547 5 11.217c0 3.286 4.217 5.285 8.344 5.285 5.405 0 ' +
      '9.002-3.14 9.002-5.632 0-1.506-1.27-2.362-3.51-2.407zm-9.027 7.9c-1.93.195-3.6-.' +
      '748-3.735-2.107-.134-1.358 1.322-2.61 3.253-2.805 1.932-.196 3.601.747 3.736 2.106.' +
      '134 1.359-1.322 2.61-3.254 2.806zm2.28-1.84c-.455.63-1.135.96-1.514.74-.382-.22-.' +
      '334-1.015.122-1.645.454-.63 1.133-.96 1.513-.74.382.22.334 1.015-.12 1.645zm6.37-' +
      '5.55c-.08.218-.31.33-.513.25-.2-.08-.293-.32-.21-.538.406-1.08.056-2.31-.893-2.994-' +
      '.933-.672-2.21-.6-3.067.175-.174.16-.44.155-.596-.01-.156-.165-.152-.44.022-.6 1.175-' +
      '1.082 2.885-1.178 4.168-.234 1.3.956 1.705 2.58 1.09 3.95zm1.773-1.044c-.133.35-.' +
      '517.52-.856.38-2.09-.845-4.548-.315-6.046 1.302-.173.186-.46.198-.64.027-.178-.172-' +
      '.19-.463-.016-.65 1.832-1.972 4.808-2.615 7.305-1.572.34.138.513.527.253.513z"/>' +
      '</svg>';
    weibo.addEventListener('click', function () {
      openShare(weiboUrl(getShareInfo()));
    });

    // 微信（二维码弹窗）
    var wechat = document.createElement('button');
    wechat.className = 'share-btn share-btn--wechat';
    wechat.setAttribute('data-tip', '微信扫码分享');
    wechat.setAttribute('aria-label', '微信扫码分享');
    wechat.innerHTML = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">' +
      '<path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 ' +
      '5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.' +
      '295.295a.3.3 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 ' +
      '0 0 2.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-' +
      '1.415 4.882-1.932 7.621-.55C17.585 3.99 13.434 2.188 8.69 2.188zm-1.47 4.39c.' +
      '603 0 1.094.49 1.094 1.094a1.094 1.094 0 0 1-2.188 0c0-.604.49-1.094 1.094-1.094zm' +
      '4.695 0c.604 0 1.094.49 1.094 1.094a1.094 1.094 0 0 1-2.188 0c0-.604.49-1.094 ' +
      '1.094-1.094zM24 14.787c0-3.46-3.327-6.27-7.436-6.27-4.108 0-7.434 2.81-7.434 ' +
      '6.27 0 3.46 3.326 6.27 7.434 6.27.823 0 1.618-.122 2.344-.338a.703.703 0 0 1 ' +
      '.59.082l1.54.907a.24.24 0 0 0 .135.043.24.24 0 0 0 .24-.24c0-.057-.024-.113-.' +
      '038-.172l-.316-1.198a.482.482 0 0 1 .173-.539A5.884 5.884 0 0 0 24 14.787zm-' +
      '9.875-1.043a.897.897 0 1 1 0-1.795.897.897 0 0 1 0 1.795zm4.875 0a.897.897 0 ' +
      '1 1 0-1.795.897.897 0 0 1 0 1.795z"/>' +
      '</svg>';
    wechat.addEventListener('click', function () {
      openWechatQr();
    });

    // QQ
    var qq = document.createElement('button');
    qq.className = 'share-btn share-btn--qq';
    qq.setAttribute('data-tip', '分享到QQ');
    qq.setAttribute('aria-label', '分享到QQ');
    qq.innerHTML = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">' +
      '<path d="M21.395 15.035a39.548 39.548 0 0 0-.803-2.264l-.008-.02c.136-.646.206-' +
      '1.271.21-1.88.017-2.738-1.3-4.6-2.474-5.698a8.314 8.314 0 0 0-1.038-.808C16.612 ' +
      '2.68 14.64 1.5 12 1.5S7.388 2.68 6.718 4.365a8.3 8.3 0 0 0-1.038.808C4.506 6.27 ' +
      '3.19 8.133 3.207 10.87c.004.61.073 1.234.21 1.88l-.009.021a39.557 39.557 0 0 0-.' +
      '803 2.264C1.754 17.108 1.5 19.095 2.41 19.95c.414.393.99.463 1.5.317A4.372 4.372 0 ' +
      '0 0 5.87 22.5c1.18 0 2.394-.57 3.127-1.785.305-.507.528-.87.705-1.148.766.107 1.536.' +
      '163 2.298.163.762 0 1.532-.056 2.297-.163.178.277.4.641.706 1.148C15.736 21.93 16.95 ' +
      '22.5 18.13 22.5a4.372 4.372 0 0 0 1.96-2.233c.51.146 1.086.076 1.5-.317.91-.855.' +
      '655-2.842-.195-4.915z"/>' +
      '</svg>';
    qq.addEventListener('click', function () {
      openShare(qqUrl(getShareInfo()));
    });

    // Twitter/X
    var twitter = document.createElement('button');
    twitter.className = 'share-btn share-btn--twitter';
    twitter.setAttribute('data-tip', '分享到 Twitter/X');
    twitter.setAttribute('aria-label', '分享到 Twitter/X');
    twitter.innerHTML = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">' +
      '<path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 ' +
      '6.231H2.746l7.73-8.835L1.254 2.25H8.08l4.213 5.567zm-1.161 17.52h1.833L7.084 ' +
      '4.126H5.117z"/>' +
      '</svg>';
    twitter.addEventListener('click', function () {
      openShare(twitterUrl(getShareInfo()));
    });

    // 复制链接
    var copy = document.createElement('button');
    copy.className = 'share-btn share-btn--copy';
    copy.setAttribute('data-tip', '复制链接');
    copy.setAttribute('aria-label', '复制页面链接');
    copy.innerHTML = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">' +
      '<path d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-' +
      '6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 ' +
      '4.5 0 0 0 1.242 7.244" stroke="currentColor" stroke-width="1.8" stroke-linecap=' +
      '"round" stroke-linejoin="round" fill="none"/>' +
      '</svg>';
    copy.addEventListener('click', function () {
      copyLink(copy);
    });

    // Facebook
    var facebook = document.createElement('button');
    facebook.className = 'share-btn share-btn--facebook';
    facebook.setAttribute('data-tip', '分享到 Facebook');
    facebook.setAttribute('aria-label', '分享到 Facebook');
    facebook.innerHTML = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">' +
      '<path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 ' +
      '10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 ' +
      '1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328' +
      'l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>' +
      '</svg>';
    facebook.addEventListener('click', function () {
      var info = getShareInfo();
      openShare('https://www.facebook.com/sharer/sharer.php?u=' + info.url);
    });

    sidebar.appendChild(weibo);
    sidebar.appendChild(wechat);
    sidebar.appendChild(qq);
    sidebar.appendChild(facebook);
    sidebar.appendChild(twitter);
    sidebar.appendChild(copy);

    document.body.appendChild(sidebar);
  }

  /* ── 复制链接 ── */
  function copyLink(btn) {
    var url = window.location.href;
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(url).then(function () {
        showCopyToast();
        btn.setAttribute('data-tip', '已复制！');
        btn.classList.add('copied');
        setTimeout(function () {
          btn.setAttribute('data-tip', '复制链接');
          btn.classList.remove('copied');
        }, 2000);
      });
    } else {
      // 降级方案
      var ta = document.createElement('textarea');
      ta.value = url;
      ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px;opacity:0';
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand('copy');
        showCopyToast();
        btn.setAttribute('data-tip', '已复制！');
        btn.classList.add('copied');
        setTimeout(function () {
          btn.setAttribute('data-tip', '复制链接');
          btn.classList.remove('copied');
        }, 2000);
      } catch (e) {}
      document.body.removeChild(ta);
    }
  }

  /* ── 复制成功 toast ── */
  function showCopyToast() {
    var toast = document.getElementById('_share_copy_toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = '_share_copy_toast';
      toast.className = 'share-copy-toast';
      toast.textContent = '✓  链接已复制到剪贴板';
      document.body.appendChild(toast);
    }
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(function () {
      toast.classList.remove('show');
    }, 2200);
  }

  /* ── 微信二维码弹窗 ── */
  function openWechatQr() {
    var overlay = document.getElementById('_wechat_qr_overlay');
    if (!overlay) {
      overlay = buildWechatQrOverlay();
      document.body.appendChild(overlay);
    }
    // 刷新 URL 显示
    var urlEl = overlay.querySelector('.qr-url');
    if (urlEl) urlEl.textContent = window.location.href;

    // 用 qrserver API 动态生成二维码（纯 URL，无需第三方账号）
    var qrImg = overlay.querySelector('.qr-img-wrap img');
    if (qrImg) {
      qrImg.src = 'https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=' +
                  encodeURIComponent(window.location.href);
    }

    requestAnimationFrame(function () {
      overlay.classList.add('open');
    });
  }

  function buildWechatQrOverlay() {
    var overlay = document.createElement('div');
    overlay.id = '_wechat_qr_overlay';
    overlay.className = 'wechat-qr-overlay';
    overlay.innerHTML =
      '<div class="wechat-qr-box">' +
        '<div class="qr-title">' +
          '<svg viewBox="0 0 24 24" width="18" height="18" style="fill:#07c160;flex-shrink:0">' +
            '<path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.295.295a.3.3 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 4.882-1.932 7.621-.55C17.585 3.99 13.434 2.188 8.69 2.188z"/>' +
          '</svg>' +
          '微信扫码分享' +
        '</div>' +
        '<p class="qr-sub">打开微信，扫描下方二维码<br>即可分享给好友或朋友圈</p>' +
        '<div class="qr-img-wrap"><img src="" alt="二维码" loading="lazy"></div>' +
        '<div class="qr-url"></div>' +
        '<button class="qr-close" id="_wechat_qr_close">关闭</button>' +
      '</div>';

    // 点击遮罩或关闭按钮关闭
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay || e.target.id === '_wechat_qr_close') {
        overlay.classList.remove('open');
      }
    });

    return overlay;
  }

  /* ── 初始化入口 ── */
  function init() {
    buildSidebar();
  }

  // 等 DOM 就绪再挂载
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();


// ════════════════════════════════════════════════════
//  UI 动画升级系统
// ════════════════════════════════════════════════════

(function () {
  'use strict';

  /* ─── 1. 页面加载遮罩 ─── */
  function initPageLoader() {
    var overlay = document.createElement('div');
    overlay.className = 'page-load-overlay';
    overlay.innerHTML = '<div class="page-load-logo">⚔ 王国之泪</div>';
    document.body.appendChild(overlay);
    window.addEventListener('load', function () {
      setTimeout(function () { overlay.classList.add('loaded'); }, 400);
      setTimeout(function () { overlay.remove(); }, 1400);
    });
  }

  /* ─── 2. 光标跟随光晕 ─── */
  function initCursorGlow() {
    if (window.matchMedia('(max-width:768px)').matches) return;
    var glow = document.createElement('div');
    glow.id = 'cursor-glow';
    document.body.appendChild(glow);
    var mx = window.innerWidth / 2, my = window.innerHeight / 2;
    var cx = mx, cy = my;
    document.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
    });
    function lerp(a, b, t) { return a + (b - a) * t; }
    function tick() {
      cx = lerp(cx, mx, 0.08);
      cy = lerp(cy, my, 0.08);
      glow.style.left = cx + 'px';
      glow.style.top  = cy + 'px';
      requestAnimationFrame(tick);
    }
    tick();
  }

  /* ─── 3. 浮动粒子背景 ─── */
  function initParticles() {
    var canvas = document.createElement('canvas');
    canvas.id = 'particles-canvas';
    document.body.insertBefore(canvas, document.body.firstChild);
    var ctx = canvas.getContext('2d');

    function resize() {
      canvas.width  = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    var particles = [];
    var COUNT = window.innerWidth < 768 ? 30 : 60;

    for (var i = 0; i < COUNT; i++) {
      particles.push({
        x:    Math.random() * canvas.width,
        y:    Math.random() * canvas.height,
        r:    Math.random() * 1.4 + 0.3,
        vx:   (Math.random() - 0.5) * 0.25,
        vy:   -(Math.random() * 0.4 + 0.1),
        alpha: Math.random() * 0.5 + 0.1,
        hue:  Math.random() > 0.6 ? 45 : 140   // gold or green
      });
    }

    function drawParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(function (p) {
        p.x += p.vx;
        p.y += p.vy;
        if (p.y < -4)           p.y = canvas.height + 4;
        if (p.x < -4)           p.x = canvas.width  + 4;
        if (p.x > canvas.width + 4) p.x = -4;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = 'hsla(' + p.hue + ',80%,60%,' + p.alpha + ')';
        ctx.fill();
      });
      requestAnimationFrame(drawParticles);
    }
    drawParticles();
  }

  /* ─── 4. 滚动视差入场 (IntersectionObserver) ─── */
  function initScrollReveal() {
    // 给主要区块自动加 scroll-reveal 类
    var selectors = [
      '.categories-grid .category-card',
      '.sq-card',
      '.weapon-card',
      '.recipe-card',
      '.info-card',
      '.boss-card',
      '.section-header',
      '.page-hero',
      '.progress-section',
      '.highlight-box',
      '.tip-box',
      '.about-card',
      '.about-site-item'
    ];

    selectors.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el, idx) {
        if (el.classList.contains('scroll-reveal')) return;
        el.classList.add('scroll-reveal');

        // 奇偶交替方向
        if (sel.includes('category-card') || sel.includes('boss-card')) {
          el.classList.add(idx % 2 === 0 ? 'from-left' : 'from-right');
          el.classList.add('delay-' + Math.min((idx % 4) + 1, 5));
        } else if (sel.includes('section-header') || sel.includes('page-hero')) {
          el.classList.add('from-bottom');
        } else {
          el.classList.add('from-bottom');
          el.classList.add('delay-' + Math.min((idx % 3) + 1, 3));
        }
      });
    });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.scroll-reveal').forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ─── 5. Navbar 滚动状态 ─── */
  function initNavbarScroll() {
    var navbar = document.querySelector('.navbar');
    if (!navbar) return;
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
  }

  /* ─── 6. 数字滚动计数器 ─── */
  function initCounters() {
    var nums = document.querySelectorAll(
      '.totk-stat-num, .hero-stat-number, .progress-stat-val'
    );
    var counterObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var raw = el.textContent.trim();
        // 只对纯数字做动画
        if (!/^\d+$/.test(raw)) { counterObs.unobserve(el); return; }
        var target = parseInt(raw, 10);
        var duration = 1200;
        var start = performance.now();
        function step(now) {
          var t = Math.min((now - start) / duration, 1);
          // ease out quart
          var ease = 1 - Math.pow(1 - t, 4);
          el.textContent = Math.round(ease * target);
          if (t < 1) requestAnimationFrame(step);
          else el.textContent = target;
        }
        requestAnimationFrame(step);
        counterObs.unobserve(el);
      });
    }, { threshold: 0.5 });
    nums.forEach(function (el) { counterObs.observe(el); });
  }

  /* ─── 7. 按钮 Ripple 鼠标位置 ─── */
  function initRipple() {
    var btns = document.querySelectorAll(
      '.filter-tab, .boss-tab, .cat-btn, .fb-btn, .fb-btn'
    );
    btns.forEach(function (btn) {
      btn.addEventListener('mousemove', function (e) {
        var rect = btn.getBoundingClientRect();
        var rx = ((e.clientX - rect.left) / rect.width  * 100).toFixed(1) + '%';
        var ry = ((e.clientY - rect.top)  / rect.height * 100).toFixed(1) + '%';
        btn.style.setProperty('--rx', rx);
        btn.style.setProperty('--ry', ry);
      });
    });
  }

  /* ─── 8. Boss 卡片弱点标签 & 步骤交错入场 ─── */
  function initBossAnimations() {
    var cardObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var card = entry.target;

        // 弱点标签交错显现
        card.querySelectorAll('.weakness-tag').forEach(function (tag, i) {
          setTimeout(function () {
            tag.classList.add('tag-visible');
          }, 200 + i * 120);
        });

        // 攻略步骤交错滑入
        card.querySelectorAll('.boss-step').forEach(function (step, i) {
          setTimeout(function () {
            step.classList.add('step-visible');
          }, 300 + i * 60);
        });

        // 奖励徽章弹跳入场
        card.querySelectorAll('.reward-item').forEach(function (item, i) {
          setTimeout(function () {
            item.classList.add('item-visible');
          }, 400 + i * 80);
        });

        cardObs.unobserve(card);
      });
    }, { threshold: 0.1 });

    document.querySelectorAll('.boss-card').forEach(function (card) {
      cardObs.observe(card);
    });
  }

  /* ─── 9. Boss 图片切换淡入增强 ─── */
  var origSwitchBossImg = window.switchBossImg;
  window.switchBossImg = function (thumb) {
    var gallery = thumb.closest('.boss-gallery');
    var mainImg = gallery.querySelector('.boss-img-main img');

    mainImg.classList.add('switching');
    setTimeout(function () {
      if (origSwitchBossImg) {
        origSwitchBossImg(thumb);
      } else {
        var src = thumb.querySelector('img').src;
        var alt = thumb.querySelector('img').alt;
        mainImg.src = src;
        mainImg.alt = alt;
        gallery.querySelectorAll('.boss-thumb').forEach(function (t) {
          t.classList.remove('active');
        });
        thumb.classList.add('active');
      }
      mainImg.classList.remove('switching');
    }, 200);
  };

  /* ─── 10. 平滑页面跳转 ─── */
  /* 已移除（2026-10-30）：旧的转场遮罩会在前进/后退（bfcache 恢复）时卡在不透明状态，
     盖住整个页面且无法点击。改回浏览器默认导航，不再拦截链接、不再创建遮罩。 */
  function initPageTransition() {
  }

  /* ─── 11. 卡片 3D 微倾斜 (mousemove) ─── */
  function initCardTilt() {
    // 已移除：与 scroll-reveal transform 冲突，改为仅用 CSS box-shadow 提升层次感
  }

  /* ─── 初始化入口 ─── */
  function init() {
    // initPageLoader();  // 已移除：加载遮罩动画
    initCursorGlow();
    initParticles();
    initNavbarScroll();
    initScrollReveal();
    initCounters();
    initRipple();
    initBossAnimations();
    initPageTransition();
    initCardTilt();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
/* ============================================================
   语言切换 i18n：English / 简体中文 / 繁體中文，全站生效
   - 简体：原文；繁体：OpenCC s2twp（台湾惯用）词表转换；
     英文：按页加载翻译包 /i18n/en/<页>.json + 全站标题包。
   - 选择记入 localStorage，跨页保持；?lang= 参数可直接分享。
   ============================================================ */
(function () {
'use strict';
var KEY = 'totk-lang';
var UI_EN = {
  '首页': 'Home', '主线任务': 'Main Quests', '情节挑战': 'Side Adventures',
  '神庙挑战': 'Shrines', '神庙开启': 'Unlocking Shrines', '破魔树根': 'Lightroots',
  '武器图鉴': 'Weapons', '料理合成': 'Cooking', '套装获取': 'Armor Sets',
  'Boss图鉴': 'Bosses', '物品收集': 'Collectibles', '魔犹伊的遗失物': 'Bubbul Gems',
  '贤者的遗志': "Sage's Wills", '残旧的地图': 'Old Maps',
  '⚔ 王国之泪 全攻略': '⚔ Tears of the Kingdom Complete Guide',
  '王国之泪 攻略': 'Tears of the Kingdom Guide',
  '本网站创作的游戏攻略指南为本人创作，游戏的人物著作权归任天堂株式会社所有。': 'All guides on this site are the author\'s original work. All game characters are copyrighted by Nintendo Co., Ltd.',
  '《塞尔达传说 王国之泪》版权归任天堂株式会社所有。': 'The Legend of Zelda: Tears of the Kingdom is copyrighted by Nintendo Co., Ltd.',
  '常见问题': 'FAQ', '📋 攻略步骤': '📋 Guide Steps', '📋 任务步骤': '📋 Quest Steps',
  '🔗 相关攻略': '🔗 Related Guides', '📚 全部攻略索引': '📚 All Guides Index',
  '📚 更多攻略': '📚 More Guides', '📖 深度攻略': '📖 In-Depth Guides',
  '阅读全文 →': 'Read More →', '返回秘籍专栏': "Back to Harry's Guides",
  '🏆 哈里的终极秘籍': "🏆 Harry's Ultimate Guides", '哈里的终极秘籍': "Harry's Ultimate Guides",
  '🧙 作者：哈里': '🧙 Author: Harry', '🆕 每日新攻略': '🆕 Daily New Guides',
  '关于我们': 'About Us', '网站地图': 'Sitemap', '隐私政策': 'Privacy Policy',
  '已收集': 'Collected', '危险度': 'Danger Level', '剧情线': 'Storyline',
  '地底': 'The Depths', '天空群島': 'Sky Islands', '中央海拉魯': 'Central Hyrule',
  '赫布拉': 'Hebra', '拉纳尤': 'Lanayru', '格鲁德': 'Gerudo',
  '页面不存在': 'Page Not Found',
  /* 独立标点节点：句读被 <strong> 等标签切开时单独成节点，英文下转半角，避免英文句后残留中文句号 */
  '。': '.', '，': ',', '、': ',', '；': ';', '：': ':', '！': '!', '？': '?',
  '（': '(', '）': ')', '「': '"', '」': '"', '『': '"', '』': '"', '…': '...',
  '你寻找的页面已消失在海拉鲁的迷雾中……': 'The page you are looking for has vanished into the mists of Hyrule…',
  '← 返回首页': '← Back to Home', '🎯 推荐内容': '🎯 Recommended',
  '📜 主线任务攻略': '📜 Main Quest Guide', '🏛 神庙挑战': '🏛 Shrine Challenges',
  '⚔ 武器图鉴': '⚔ Weapon Compendium', '🍲 料理合成': '🍲 Cooking Recipes',
  '👹 Boss图鉴': '👹 Boss Compendium'
};
var pageSlug = (function () {
  var p = location.pathname.replace(/^\//, '').replace(/\.html$/, '');
  return p === '' ? 'index' : p;
})();
function getLang() {
  var m = /[?&]lang=(en|zh-CN|zh-TW)/.exec(location.search);
  var l = m ? m[1] : null;
  if (!l) { try { l = localStorage.getItem(KEY); } catch (e) {} }
  return (l === 'en' || l === 'zh-TW' || l === 'zh-CN') ? l : 'zh-CN';
}
var lang = getLang();
var textNodes = [], altEls = [], titleEls = [], metaEls = [], origTitle = document.title;
var obsNodes = []; /* 由 MutationObserver 翻译的后生成文本节点（地图弹窗、JS 表格等），切换语言时一并恢复 */

/* ---------- 繁体转换：OpenCC s2twp 算法移植（词表按需加载） ---------- */
var TW = null, twLoading = false, twQueue = [];
function twLoad(cb) {
  if (TW) { cb(); return; }
  twQueue.push(cb);
  if (twLoading) return;
  twLoading = true;
  var s = document.createElement('script');
  s.src = '/i18n/tw-dicts.js';
  s.onload = function () { TW = window.__TW_DICTS || null; var q = twQueue; twQueue = []; q.forEach(function (f) { f(); }); };
  s.onerror = function () { twLoading = false; var q = twQueue; twQueue = []; q.forEach(function (f) { f(); }); };
  document.head.appendChild(s);
}
function twFindMatch(str, dict, hint) {
  var slen = str.length, testLen = Math.min(slen, dict.max);
  if (hint) testLen = Math.min(testLen, hint);
  while (testLen >= dict.min) {
    for (var i = 0; i <= slen - testLen; i++) {
      var sub = str.slice(i, i + testLen);
      if (Object.prototype.hasOwnProperty.call(dict.map, sub)) {
        return { v: dict.map[sub], l: i > 0 ? str.slice(0, i) : null, r: (i + testLen < slen) ? str.slice(i + testLen) : null, len: testLen };
      }
    }
    testLen--;
  }
  return null;
}
function twParse(root, dictList) {
  var working = [root], unmatched = [];
  dictList.forEach(function (dict) {
    while (working.length) {
      var cur = working.pop();
      var m = twFindMatch(cur.value, dict, cur.hint);
      if (m) {
        cur.value = m.v; cur.hint = null;
        if (m.l) { var ln = { value: m.l, left: null, right: null, hint: m.len }; working.push(ln); cur.left = ln; }
        if (m.r) { var rn = { value: m.r, left: null, right: null, hint: m.len }; working.push(rn); cur.right = rn; }
      } else { unmatched.push(cur); cur.hint = null; }
    }
    var tmp = working; working = unmatched; unmatched = tmp;
  });
}
function twInorder(root) {
  var out = [], stack = [], cur = root;
  while (true) {
    while (cur) { stack.push(cur); cur = cur.left; }
    if (stack.length) { cur = stack.pop(); out.push(cur.value); cur = cur.right; }
    else break;
  }
  return out;
}
var TW_SEP = /(\s+|-|,|\.|\?|!|\*|　|，|。|、|；|：|？|！|…|“|”|‘|’|『|』|「|」|﹁|﹂|—|－|（|）|《|》|〈|〉|～|．|／|＼|︒|︑|︔|︓|︿|﹀|︹|︺|︙|︐|［|﹇|］|﹈|︕|︖|︰|︳|︴|︽|︾|︵|︶|｛|︷|｝|︸|﹃|﹄|【|︻|】|︼)/;
function twConvert(str) {
  if (!TW) return str;
  var chain = [[TW.st_phr, TW.st_chr], [TW.tw_phr], [TW.tw_var]];
  var parts = str.split(TW_SEP), res = [];
  for (var i = 0; i < parts.length; i++) {
    var p = parts[i];
    if (i % 2 === 0 && p) {
      var root = { value: p, left: null, right: null, hint: null };
      chain.forEach(function (step) {
        twParse(root, step);
        var t = twInorder(root).join('');
        root = { value: t, left: null, right: null, hint: null };
      });
      res.push(twInorder(root).join(''));
    } else res.push(p);
  }
  return res.join('');
}

/* ---------- 原文快照与恢复 ---------- */
function collect() {
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode: function (n) {
      var p = n.parentNode;
      if (!p) return NodeFilter.FILTER_REJECT;
      var tag = p.nodeName;
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT') return NodeFilter.FILTER_REJECT;
      if (p.closest && p.closest('[data-no-i18n],.adsbygoogle')) return NodeFilter.FILTER_REJECT;
      if (!/\S/.test(n.nodeValue)) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    }
  });
  var n;
  while ((n = walker.nextNode())) {
    if (n._totkOrig === undefined) n._totkOrig = n.nodeValue;
    textNodes.push(n);
  }
  Array.prototype.forEach.call(document.querySelectorAll('img[alt]'), function (el) {
    if (el._totkOrig === undefined) el._totkOrig = el.getAttribute('alt');
    altEls.push(el);
  });
  Array.prototype.forEach.call(document.querySelectorAll('[title]'), function (el) {
    if (el._totkOrigT === undefined) el._totkOrigT = el.getAttribute('title');
    titleEls.push(el);
  });
  Array.prototype.forEach.call(document.querySelectorAll('meta[name="description"],meta[property="og:description"]'), function (el) {
    if (el._totkOrig === undefined) el._totkOrig = el.getAttribute('content');
    metaEls.push(el);
  });
}
function restoreAll() {
  obsNodes.forEach(function (o) { o.n.nodeValue = o.orig; o.n._totkDone = false; });
  obsNodes = [];
  textNodes.forEach(function (n) { n.nodeValue = n._totkOrig; });
  altEls.forEach(function (el) { el.setAttribute('alt', el._totkOrig); });
  titleEls.forEach(function (el) { el.setAttribute('title', el._totkOrigT); });
  metaEls.forEach(function (el) { el.setAttribute('content', el._totkOrig); });
  document.title = origTitle;
}
function splitWS(s) {
  var m = /^(\s*)([\s\S]*?)(\s*)$/.exec(s);
  return { pre: m[1], core: m[2], post: m[3] };
}
function normWS(s) { return s.replace(/\s+/g, ' ').replace(/[\u201c\u201d]/g, '"').replace(/[\u2018\u2019]/g, "'").trim(); }
function applyMapToText(map, subKeys) {
  /* 整块优先：段落/列表/单元格全文匹配时，把译文放进首个文本节点，
     其余文本节点清空（保留链接等内联元素占位，避免半中半英）。 */
  var normMap = {};
  Object.keys(map).forEach(function (k) { normMap[normWS(k)] = map[k]; });
  /* 整块匹配扩展：所有元素都可作为整块候选（卡片 div、步骤 div 等），
     按深度从深到浅尝试，内层先命中则外层跳过；含 img/table/ul/ol 的
     容器跳过（其全文是多项拼接，不会是单条译文）；<br> 不再排除，
     因 textContent 本来就把 <br> 当空拼接，与翻译包键一致。 */
  var blockEls = [];
  Array.prototype.forEach.call(document.body.querySelectorAll('*'), function (el) {
    if (el.querySelector('img,table,ul,ol')) return;
    blockEls.push(el);
  });
  blockEls.sort(function (a, b) {
    var da = 0, db = 0, x = a, y = b;
    while (x) { da++; x = x.parentNode; }
    while (y) { db++; y = y.parentNode; }
    return db - da;
  });
  blockEls.forEach(function (el) {
    var full = normWS(el.textContent);
    if (!full || !Object.prototype.hasOwnProperty.call(normMap, full)) return;
    var nodes = [];
    var w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, { acceptNode: function (n) { return /\S/.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT; } });
    var tn;
    while ((tn = w.nextNode())) nodes.push(tn);
    if (!nodes.length) return;
    nodes[0].nodeValue = normMap[full];
    for (var i = 1; i < nodes.length; i++) nodes[i].nodeValue = '';
    nodes.forEach(function (n) { n._totkDone = true; });
  });
  textNodes.forEach(function (n) {
    if (n._totkDone) return;
    var parts = splitWS(n._totkOrig);
    if (!parts.core) return;
    if (Object.prototype.hasOwnProperty.call(map, parts.core)) {
      n.nodeValue = parts.pre + map[parts.core] + parts.post;
      return;
    }
    if (Object.prototype.hasOwnProperty.call(normMap, normWS(parts.core))) {
      n.nodeValue = parts.pre + normMap[normWS(parts.core)] + parts.post;
      return;
    }
    if (subKeys && !n._totkDone) {
      var core = parts.core;
      for (var i = 0; i < subKeys.length; i++) {
        var k = subKeys[i];
        if (core.indexOf(k) !== -1) core = core.split(k).join(map[k]);
      }
      n.nodeValue = parts.pre + core + parts.post;
    }
  });
  altEls.forEach(function (el) {
    var v = el._totkOrig;
    if (Object.prototype.hasOwnProperty.call(map, v)) el.setAttribute('alt', map[v]);
  });
  titleEls.forEach(function (el) {
    var v = el._totkOrigT;
    if (Object.prototype.hasOwnProperty.call(map, v)) el.setAttribute('title', map[v]);
  });
  metaEls.forEach(function (el) {
    var v = el._totkOrig;
    if (Object.prototype.hasOwnProperty.call(map, v)) el.setAttribute('content', map[v]);
  });
}

/* ---------- 切换器 UI ---------- */
var switchEl = null, busy = false;
function setActive() {
  if (!switchEl) return;
  Array.prototype.forEach.call(switchEl.querySelectorAll('button'), function (b) {
    b.classList.toggle('on', b.getAttribute('data-lang') === lang);
  });
}
function injectSwitcher() {
  var host = document.querySelector('.navbar-inner') || document.querySelector('.navbar');
  if (!host || document.querySelector('.lang-switch')) return;
  var st = document.createElement('style');
  st.textContent = '.lang-switch{display:flex;gap:6px;margin-left:auto;align-items:center;flex-wrap:wrap}' +
    '.lang-switch button{background:transparent;border:1px solid rgba(201,162,39,.5);color:#e8dcc0;border-radius:20px;padding:4px 10px;font-size:12px;cursor:pointer;line-height:1.4}' +
    '.lang-switch button.on{background:#c9a227;color:#10131a;border-color:#c9a227;font-weight:700}' +
    '.lang-switch button:disabled{opacity:.5;cursor:wait}';
  document.head.appendChild(st);
  var div = document.createElement('div');
  div.className = 'lang-switch';
  div.setAttribute('role', 'group');
  div.setAttribute('aria-label', 'Language');
  [['en', 'English'], ['zh-CN', '简体中文'], ['zh-TW', '繁體中文']].forEach(function (item) {
    var b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('data-lang', item[0]);
    b.textContent = item[1];
    b.addEventListener('click', function () { setLang(item[0]); });
    div.appendChild(b);
  });
  host.appendChild(div);
  switchEl = div;
  setActive();
}
function setLang(l) {
  if (busy || l === lang) { if (l === lang) return; }
  lang = l;
  try { localStorage.setItem(KEY, l); } catch (e) {}
  try {
    var url = new URL(location.href);
    url.searchParams.set('lang', l);
    history.replaceState(null, '', url.toString());
  } catch (e) {}
  setActive();
  applyLang();
}
function applyLang() {
  restoreAll();
  document.documentElement.lang = lang === 'en' ? 'en' : lang;
  if (lang === 'zh-CN') return;
  if (lang === 'zh-TW') {
    busy = true; setBusy(true);
    twLoad(function () {
      if (TW) {
        textNodes.forEach(function (n) { n.nodeValue = twConvert(n._totkOrig); });
        altEls.forEach(function (el) { el.setAttribute('alt', twConvert(el._totkOrig)); });
        titleEls.forEach(function (el) { el.setAttribute('title', twConvert(el._totkOrigT)); });
        metaEls.forEach(function (el) { el.setAttribute('content', twConvert(el._totkOrig)); });
        document.title = twConvert(origTitle);
      }
      busy = false; setBusy(false);
    });
    return;
  }
  if (lang === 'en') {
    busy = true; setBusy(true);
    Promise.all([
      fetch('/i18n/en/' + pageSlug + '.json').then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }),
      fetch('/i18n/en/titles.json').then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; })
    ]).then(function (res) {
      var pack = res[0], titles = res[1];
      var map = {};
      Object.keys(UI_EN).forEach(function (k) { map[k] = UI_EN[k]; });
      if (titles) {
        Object.keys(titles).forEach(function (k) {
          map[k] = titles[k];
          map['› ' + k] = '› ' + titles[k];
        });
      }
      var subKeys = [];
      if (pack && pack.pairs) {
        pack.pairs.forEach(function (pr) {
          map[pr[0]] = pr[1];
          if (pr[0].length >= 6) subKeys.push(pr[0]);
        });
        subKeys.sort(function (a, b) { return b.length - a.length; });
      }
      applyMapToText(map, subKeys);
      if (pack && pack.title) document.title = pack.title;
      /* 后生成内容翻译：地图弹窗、JS 渲染表格等在 collect() 之后才出现，
         靠 MutationObserver 补译；切换出英文时由 restoreAll 恢复。 */
      if (!window._totkObs) {
        window._totkObs = true;
        var obs = new MutationObserver(function (muts) {
          if (lang !== 'en' && lang !== 'zh-TW') return;
          function trNode(n) {
            if (lang === 'zh-TW') {
              if (!TW || n._totkDone || !/\S/.test(n.nodeValue)) return;
              var p0 = n.parentNode;
              if (!p0) return;
              var tg0 = p0.nodeName;
              if (tg0 === 'SCRIPT' || tg0 === 'STYLE' || tg0 === 'NOSCRIPT') return;
              if (p0.closest && p0.closest('[data-no-i18n],.adsbygoogle,.lang-switch')) return;
              var orig0 = n.nodeValue;
              n.nodeValue = twConvert(orig0);
              n._totkDone = true; obsNodes.push({ n: n, orig: orig0 });
              return;
            }
            if (n._totkDone || !/\S/.test(n.nodeValue)) return;
            var p = n.parentNode;
            if (!p) return;
            var tag = p.nodeName;
            if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT') return;
            if (p.closest && p.closest('[data-no-i18n],.adsbygoogle,.lang-switch')) return;
            var parts = splitWS(n.nodeValue);
            if (!parts.core) return;
            var orig = n.nodeValue, out = null;
            if (Object.prototype.hasOwnProperty.call(map, parts.core)) out = parts.pre + map[parts.core] + parts.post;
            else {
              var normCore = normWS(parts.core), nm = {};
              Object.keys(map).forEach(function (k) { nm[normWS(k)] = map[k]; });
              if (Object.prototype.hasOwnProperty.call(nm, normCore)) out = parts.pre + nm[normCore] + parts.post;
              else {
                var core = parts.core;
                for (var i = 0; i < subKeys.length; i++) {
                  var k = subKeys[i];
                  if (core.indexOf(k) !== -1) core = core.split(k).join(map[k]);
                }
                out = parts.pre + core + parts.post;
              }
            }
            if (out !== orig) { n.nodeValue = out; n._totkDone = true; obsNodes.push({ n: n, orig: orig }); }
          }
          muts.forEach(function (mu) {
            Array.prototype.forEach.call(mu.addedNodes, function (an) {
              if (an.nodeType === 3) { trNode(an); return; }
              if (an.nodeType !== 1) return;
              var w = document.createTreeWalker(an, NodeFilter.SHOW_TEXT, { acceptNode: function (n) { return /\S/.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT; } });
              var tn;
              while ((tn = w.nextNode())) trNode(tn);
            });
          });
        });
        obs.observe(document.body, { childList: true, subtree: true });
      }
      busy = false; setBusy(false);
    });
  }
}
function setBusy(b) {
  if (!switchEl) return;
  Array.prototype.forEach.call(switchEl.querySelectorAll('button'), function (x) { x.disabled = b; });
}
document.addEventListener('DOMContentLoaded', function () {
  collect();
  injectSwitcher();
  if (lang !== 'zh-CN') applyLang();
});
})();
