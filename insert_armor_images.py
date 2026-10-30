# -*- coding: utf-8 -*-
"""
在 harry-armor.html 的每个 armor-card 中插入对应套装图片
"""

import re

FILE_PATH = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\harry-armor.html'

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

original_content = content

# ── 替换1：蛮族/鬼神套装 ──────────────────────────────────────────────
OLD1 = '      <div class="armor-bonus">⭐⭐ 二星奖励：蓄力攻击精力持久</div>\n      <div class="armor-review">'
NEW1 = '''      <div class="armor-bonus">⭐⭐ 二星奖励：蓄力攻击精力持久</div>
      <div style="display:flex;gap:20px;justify-content:center;align-items:flex-end;margin:16px 0;">
        <div style="text-align:center;">
          <img src="images/clothes/蛮族套装.png" alt="蛮族套装"
               style="max-width:100%;width:220px;height:auto;object-fit:contain;border-radius:10px;
                      border:1px solid rgba(167,139,250,0.25);
                      box-shadow:0 4px 16px rgba(0,0,0,0.6);
                      background:rgba(10,10,20,0.4);padding:8px;" loading="lazy">
          <div style="margin-top:6px;font-size:0.75rem;color:rgba(201,162,39,0.65);">蛮族套装</div>
        </div>
        <div style="text-align:center;">
          <img src="images/clothes/鬼神套装.png" alt="鬼神套装"
               style="max-width:100%;width:220px;height:auto;object-fit:contain;border-radius:10px;
                      border:1px solid rgba(167,139,250,0.25);
                      box-shadow:0 4px 16px rgba(0,0,0,0.6);
                      background:rgba(10,10,20,0.4);padding:8px;" loading="lazy">
          <div style="margin-top:6px;font-size:0.75rem;color:rgba(201,162,39,0.65);">鬼神套装</div>
        </div>
      </div>
      <div class="armor-review">'''

# ── 替换2：左纳乌套装 ─────────────────────────────────────────────────
OLD2 = '      <div class="armor-bonus">⭐⭐ 二星奖励：能源回复加快</div>\n      <div class="armor-review">'
NEW2 = '''      <div class="armor-bonus">⭐⭐ 二星奖励：能源回复加快</div>
      <div style="text-align:center;margin:16px 0;">
        <img src="images/clothes/左纳尼乌姆之套装.png" alt="左纳乌套装"
             style="max-width:100%;width:220px;height:auto;object-fit:contain;border-radius:10px;
                    border:1px solid rgba(167,139,250,0.25);
                    box-shadow:0 4px 16px rgba(0,0,0,0.6);
                    background:rgba(10,10,20,0.4);padding:8px;" loading="lazy">
        <div style="margin-top:6px;font-size:0.75rem;color:rgba(201,162,39,0.65);">左纳乌套装</div>
      </div>
      <div class="armor-review">'''

# ── 替换3：异次元恶灵套装 ─────────────────────────────────────────────
OLD3 = '      <div class="armor-bonus">💀 套装奖励：骨武器伤害提升 + 骸骨伪装（无法在大妖精处升级）</div>\n      <div class="armor-review">'
NEW3 = '''      <div class="armor-bonus">💀 套装奖励：骨武器伤害提升 + 骸骨伪装（无法在大妖精处升级）</div>
      <div style="text-align:center;margin:16px 0;">
        <img src="images/clothes/异次元恶灵套装.png" alt="异次元恶灵套装"
             style="max-width:100%;width:220px;height:auto;object-fit:contain;border-radius:10px;
                    border:1px solid rgba(167,139,250,0.25);
                    box-shadow:0 4px 16px rgba(0,0,0,0.6);
                    background:rgba(10,10,20,0.4);padding:8px;" loading="lazy">
        <div style="margin-top:6px;font-size:0.75rem;color:rgba(201,162,39,0.65);">异次元恶灵套装</div>
      </div>
      <div class="armor-review">'''

# ── 替换4：滑翔套装 + 天空之勇者套装 ────────────────────────────────
OLD4 = '      <div class="armor-bonus">⭐⭐ 二星奖励：完全免疫坠落伤害（跌落无伤害）</div>\n      <div class="armor-review">'
NEW4 = '''      <div class="armor-bonus">⭐⭐ 二星奖励：完全免疫坠落伤害（跌落无伤害）</div>
      <div style="display:flex;gap:20px;justify-content:center;align-items:flex-end;margin:16px 0;">
        <div style="text-align:center;">
          <img src="images/clothes/滑翔套装.png" alt="滑翔套装"
               style="max-width:100%;width:220px;height:auto;object-fit:contain;border-radius:10px;
                      border:1px solid rgba(167,139,250,0.25);
                      box-shadow:0 4px 16px rgba(0,0,0,0.6);
                      background:rgba(10,10,20,0.4);padding:8px;" loading="lazy">
          <div style="margin-top:6px;font-size:0.75rem;color:rgba(201,162,39,0.65);">滑翔套装</div>
        </div>
        <div style="text-align:center;">
          <img src="images/clothes/天空之勇者套装.png" alt="天空之勇者套装"
               style="max-width:100%;width:220px;height:auto;object-fit:contain;border-radius:10px;
                      border:1px solid rgba(167,139,250,0.25);
                      box-shadow:0 4px 16px rgba(0,0,0,0.6);
                      background:rgba(10,10,20,0.4);padding:8px;" loading="lazy">
          <div style="margin-top:6px;font-size:0.75rem;color:rgba(201,162,39,0.65);">天空之勇者套装</div>
        </div>
      </div>
      <div class="armor-review">'''

# ── 替换5：蛙之套装 ──────────────────────────────────────────────────
OLD5 = '      <div class="armor-bonus">⭐⭐ 二星奖励：彻底不滑落</div>\n      <div class="armor-review">'
NEW5 = '''      <div class="armor-bonus">⭐⭐ 二星奖励：彻底不滑落</div>
      <div style="text-align:center;margin:16px 0;">
        <img src="images/clothes/蛙之套装.png" alt="蛙之套装"
             style="max-width:100%;width:220px;height:auto;object-fit:contain;border-radius:10px;
                    border:1px solid rgba(167,139,250,0.25);
                    box-shadow:0 4px 16px rgba(0,0,0,0.6);
                    background:rgba(10,10,20,0.4);padding:8px;" loading="lazy">
        <div style="margin-top:6px;font-size:0.75rem;color:rgba(201,162,39,0.65);">蛙之套装</div>
      </div>
      <div class="armor-review">'''

# ── 替换6：采矿套装 ──────────────────────────────────────────────────
OLD6 = '      <div class="armor-bonus">⭐⭐ 二星奖励：步履留光</div>\n      <div class="armor-review">'
NEW6 = '''      <div class="armor-bonus">⭐⭐ 二星奖励：步履留光</div>
      <div style="text-align:center;margin:16px 0;">
        <img src="images/clothes/采矿套装.png" alt="采矿套装"
             style="max-width:100%;width:220px;height:auto;object-fit:contain;border-radius:10px;
                    border:1px solid rgba(167,139,250,0.25);
                    box-shadow:0 4px 16px rgba(0,0,0,0.6);
                    background:rgba(10,10,20,0.4);padding:8px;" loading="lazy">
        <div style="margin-top:6px;font-size:0.75rem;color:rgba(201,162,39,0.65);">采矿套装</div>
      </div>
      <div class="armor-review">'''

# ── 替换7：黑暗/暗黑套装 ──────────────────────────────────────────────
OLD7 = '      <div class="armor-bonus">⭐⭐ 二星奖励：瘴气伤害减少</div>\n      <div class="armor-review">'
NEW7 = '''      <div class="armor-bonus">⭐⭐ 二星奖励：瘴气伤害减少</div>
      <div style="display:flex;gap:20px;justify-content:center;align-items:flex-end;margin:16px 0;">
        <div style="text-align:center;">
          <img src="images/clothes/黑暗套装.png" alt="黑暗套装"
               style="max-width:100%;width:220px;height:auto;object-fit:contain;border-radius:10px;
                      border:1px solid rgba(167,139,250,0.25);
                      box-shadow:0 4px 16px rgba(0,0,0,0.6);
                      background:rgba(10,10,20,0.4);padding:8px;" loading="lazy">
          <div style="margin-top:6px;font-size:0.75rem;color:rgba(201,162,39,0.65);">黑暗套装</div>
        </div>
        <div style="text-align:center;">
          <img src="images/clothes/暗黑套装.png" alt="暗黑套装"
               style="max-width:100%;width:220px;height:auto;object-fit:contain;border-radius:10px;
                      border:1px solid rgba(167,139,250,0.25);
                      box-shadow:0 4px 16px rgba(0,0,0,0.6);
                      background:rgba(10,10,20,0.4);padding:8px;" loading="lazy">
          <div style="margin-top:6px;font-size:0.75rem;color:rgba(201,162,39,0.65);">暗黑套装</div>
        </div>
      </div>
      <div class="armor-review">'''

replacements = [
    (OLD1, NEW1, '替换1：蛮族/鬼神套装'),
    (OLD2, NEW2, '替换2：左纳乌套装'),
    (OLD3, NEW3, '替换3：异次元恶灵套装'),
    (OLD4, NEW4, '替换4：滑翔/天空之勇者套装'),
    (OLD5, NEW5, '替换5：蛙之套装'),
    (OLD6, NEW6, '替换6：采矿套装'),
    (OLD7, NEW7, '替换7：黑暗/暗黑套装'),
]

for old, new, label in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        print(f'✅ {label} — 成功')
    else:
        print(f'❌ {label} — 未找到目标片段，请检查 HTML 内容')

if content != original_content:
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print('\n📄 文件已保存')
else:
    print('\n⚠️  内容无变化，文件未保存')

# ── 验证 ──────────────────────────────────────────────────────────────
print('\n── 验证插入结果 ──')
checks = [
    '蛮族套装.png',
    '鬼神套装.png',
    '左纳尼乌姆之套装.png',
    '滑翔套装.png',
    '天空之勇者套装.png',
    '蛙之套装.png',
    '采矿套装.png',
    '黑暗套装.png',
    '暗黑套装.png',
]

all_ok = True
for img in checks:
    if img in content:
        print(f'✅ {img} 存在')
    else:
        print(f'❌ {img} 不存在')
        all_ok = False

print()
if all_ok:
    print('SUCCESS: 全部9张套装图片已插入')
else:
    print('WARNING: 部分图片未插入，请检查上方日志')
