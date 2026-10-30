import os

BASE = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页'

TARGET_FILES = [
    'about.html',
    'boss.html',
    'boss-ganondorf.html',
    'boss-lynel.html',
    'boss-lynel-blue.html',
    'boss-lynel-silver.html',
    'boss-lynel-white.html',
    'boss-phantom-ganon.html',
    'clothes.html',
    'cooking.html',
    'main-quest.html',
    'mauyu-lost.html',
    'shrine-unlock.html',
    'shrines.html',
    'side-quest.html',
    'weapons.html',
    '404.html',
    'privacy.html',
]

INSERT_BEFORE = '<li><a href="about.html">关于我们</a></li>'
INSERT_ITEM   = '      <li><a href="harry-tips.html">哈里的终极秘籍</a></li>\n'

results = []

for fname in TARGET_FILES:
    fpath = os.path.join(BASE, fname)
    if not os.path.exists(fpath):
        results.append(f'⚠ 跳过（文件不存在）: {fname}')
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 已有 harry-tips.html 则跳过
    if 'harry-tips.html' in content:
        results.append(f'✅ 已有，跳过: {fname}')
        continue
    
    # 查找 about.html 导航项并在前面插入
    if INSERT_BEFORE in content:
        new_content = content.replace(INSERT_BEFORE, INSERT_ITEM + INSERT_BEFORE, 1)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        results.append(f'✅ 已修复: {fname}')
    else:
        results.append(f'❌ 未找到插入点: {fname}（需手动检查）')

print('\n'.join(results))
print(f'\n处理完成，共 {len(TARGET_FILES)} 个文件。')

# 验证：统计现在有多少页面包含 harry-tips.html
count = 0
all_html = [f for f in os.listdir(BASE) if f.endswith('.html') and not f.startswith('.')]
missing = []
for f in sorted(all_html):
    fpath = os.path.join(BASE, f)
    with open(fpath, 'r', encoding='utf-8') as fp:
        c = fp.read()
    if 'class="navbar"' in c:
        if 'harry-tips.html' in c:
            count += 1
        else:
            missing.append(f)

print(f'\n有 navbar 且包含 harry-tips.html 的页面数：{count}')
if missing:
    print(f'仍缺少的页面：{missing}')
else:
    print('✅ 所有有 navbar 的页面均已包含 harry-tips.html')
