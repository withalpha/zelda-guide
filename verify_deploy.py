import re
with open(r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\cooking.html', encoding='utf-8') as f:
    html = f.read()

checks = [1, 30, 64, 100, 135, 146, 215, 228]
for no in checks:
    pat = r'no:' + str(no) + r',\s*cat:"([^"]*)",\s*name:"([^"]*)"'
    m = re.search(pat, html)
    if m:
        print(f'  no:{no:3d}  cat={m.group(1):<12}  name={m.group(2)}')

print()
print('dish-name-label 样式存在:', 'dish-name-label' in html)
print('card.title 属性存在:', 'card.title = d.name' in html)
print('弹窗显示名称:', 'No.${d.no} · ${d.name}' in html)
