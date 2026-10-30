import os, re
from bs4 import BeautifulSoup

BASE = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页'

files = [
    'roots.html',
    'sage-will.html',
    'harry-tips.html',
    'harry-weapons.html',
    'harry-cooking.html',
    'harry-armor.html',
    'harry-shrine-usazum.html',
]

for fname in files:
    fpath = os.path.join(BASE, fname)
    print(f'\n' + '='*60)
    print(f'文件：{fname}')
    print('='*60)

    if not os.path.exists(fpath):
        print(f'  ❌ 文件不存在！')
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # 检查1：img src
    print('\n[IMG SRC 检查]')
    imgs = soup.find_all('img', src=True)
    broken = []
    ok = []
    for img in imgs:
        src = img.get('src', '')
        if src.startswith('http'):
            continue
        full_path = os.path.join(BASE, src.replace('/', os.sep))
        if os.path.exists(full_path):
            ok.append(src)
        else:
            broken.append(src)

    if broken:
        for b in broken:
            print(f'  ❌ 缺失图片: {b}')
    else:
        print(f'  ✅ 所有 {len(ok)} 张图片路径正确')

    # 检查2：内部 href 链接
    print('\n[内部链接 href 检查]')
    links = soup.find_all('a', href=True)
    bad_links = []
    for a in links:
        href = a.get('href', '')
        if href.startswith('http') or href.startswith('#') or href.startswith('javascript'):
            continue
        if href.endswith('.html'):
            lpath = os.path.join(BASE, href)
            if not os.path.exists(lpath):
                bad_links.append(href)
    if bad_links:
        for l in bad_links:
            print(f'  ❌ 缺失页面: {l}')
    else:
        print(f'  ✅ 所有内部 .html 链接有效')

    # 检查3：JS 关键词检查
    print('\n[JavaScript 关键检查]')

    if 'function g2ll' in content:
        if 'return [gy, gx]' in content:
            print('  ✅ g2ll: Y轴已修复 [gy, gx]')
        elif 'return [-gy, gx]' in content:
            print('  ❌ g2ll: Y轴仍然错误！使用了 [-gy, gx]')
        else:
            print('  ⚠ g2ll: 存在但形式不认识')

    if fname == 'roots.html':
        lr_count = len(re.findall(r'\[[-\d]+,[-\d]+,"(?:central|lanayru|eldin|gerudo|hebra|forest|akkala|necluda|faron)"', content))
        print(f'  {"✅" if lr_count == 120 else "❌"} LIGHTROOTS 条目数: {lr_count} (期望120)')

        si_count = len(re.findall(r'class="shrine-item"', content))
        print(f'  {"✅" if si_count == 120 else "❌"} shrine-item 数: {si_count} (期望120)')

        bad_labels = ['东聂尔鲁达', '西聂尔鲁达', '海布拉山脉', '奥尔汀峡谷', '格鲁德沙漠地底', '阿卡莱高地地底']
        for bl in bad_labels:
            if bl in content:
                print(f'  ❌ 旧地名仍存在: {bl}')

        good_labels = ['中央大废矿', '赫布拉废矿', '奥尔汀废矿', '格鲁德废矿']
        for gl in good_labels:
            if gl not in content:
                print(f'  ❌ 废矿标注缺失: {gl}')
            else:
                print(f'  ✅ 废矿标注存在: {gl}')

        if "onclick=\"switchLayer('surface')\"" in content or 'onclick="switchLayer(\'surface\')"' in content:
            print('  ❌ 地表按钮 onclick 仍然存在！')
        else:
            print('  ✅ 地表按钮已移除')

    if fname == 'sage-will.html':
        colspan7 = content.count('colspan="7"')
        colspan5 = content.count('colspan="5"')
        print(f'  {"✅" if colspan7 == 0 else "❌"} colspan="7": {colspan7} 处 (期望0)')
        print(f'  {"✅" if colspan5 >= 4 else "❌"} colspan="5": {colspan5} 处 (期望≥4)')

        boss_td = len(re.findall(r'<td><span class="boss-badge', content))
        print(f'  {"✅" if boss_td == 0 else "❌"} boss-badge td: {boss_td} 处 (期望0)')

    if fname.startswith('harry-') and fname != 'harry-tips.html':
        if 'harry-tips.html' in content:
            print('  ✅ 返回专栏链接存在')
        else:
            print('  ❌ 缺少返回专栏链接')

    # 检查4：HTML基本结构
    print('\n[HTML 结构检查]')
    has_head = '<head>' in content
    has_body = '<body>' in content
    has_nav = 'class="navbar"' in content
    has_footer = 'class="footer"' in content
    has_title = '<title>' in content
    print(f'  {"✅" if has_head else "❌"} <head>')
    print(f'  {"✅" if has_body else "❌"} <body>')
    print(f'  {"✅" if has_nav else "❌"} navbar')
    print(f'  {"✅" if has_footer else "❌"} footer')
    print(f'  {"✅" if has_title else "❌"} <title>')

    if 'harry-tips.html' not in content:
        print('  ❌ navbar 缺少哈里的终极秘籍入口')
    else:
        print('  ✅ navbar 包含哈里的终极秘籍')

print('\n\n检查完成。')
