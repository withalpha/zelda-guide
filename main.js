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
