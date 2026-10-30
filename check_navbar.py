import os

BASE = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页'

REQUIRED_LINKS = [
    'index.html',
    'main-quest.html',
    'side-quest.html',
    'shrines.html',
    'shrine-unlock.html',
    'roots.html',
    'weapons.html',
    'cooking.html',
    'clothes.html',
    'boss.html',
    'mauyu-lost.html',
    'sage-will.html',
    'harry-tips.html',
    'about.html',
]

SKIP_FILES = {'404.html', 'privacy.html'}

all_html = sorted([f for f in os.listdir(BASE) if f.endswith('.html') and not f.startswith('.')])

print(f'共扫描 {len(all_html)} 个 HTML 文件\n')
print('='*60)

issues = []

for fname in all_html:
    if fname in SKIP_FILES:
        continue
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'class="navbar-nav"' not in content and '<ul class="navbar-nav"' not in content:
        print(f'⚠ {fname}: 无完整 navbar，跳过')
        continue

    missing = []
    for link in REQUIRED_LINKS:
        if link not in content:
            missing.append(link)

    if missing:
        issues.append((fname, missing))
        print(f'❌ {fname}: 缺少 {missing}')
    else:
        print(f'✅ {fname}: navbar 完整')

print('\n' + '='*60)
if issues:
    print(f'\n共发现 {len(issues)} 个页面有 navbar 问题：')
    for fname, missing in issues:
        print(f'  {fname}: 缺少 {missing}')
else:
    print('\n✅ 所有页面 navbar 均完整一致！')
