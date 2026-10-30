"""
重新分类228种料理为7类：
串炒煎炸 / 汤品炖菜 / 饭食 / 特殊料理 / 烤食 / 冷冻 / 药水
"""
import re

# 编号 → 新分类映射
# 串炒煎炸: 1-44  (烧烤串/蒸/炒/煎/炸)
# 汤品炖菜: 45-79 (汤/炖/甘露炖)
# 饭食:     80-134 (咖喱/烩饭/炒饭/盖饭/饭团/面包/甜点/饮品)
# 特殊料理: 135-146, 198 (怪物/魔人/失败/水煮蛋)
# 烤食:     147-197 (篝火烤)
# 冷冻:     199-214
# 药水:     215-228

NEW_CAT = {}
for n in range(1, 45):    NEW_CAT[n] = "串炒煎炸"
for n in range(45, 80):   NEW_CAT[n] = "汤品炖菜"
for n in range(80, 135):  NEW_CAT[n] = "饭食"
for n in range(135, 147): NEW_CAT[n] = "特殊料理"
for n in range(147, 198): NEW_CAT[n] = "烤食"
NEW_CAT[198] = "特殊料理"   # 水煮蛋（温泉煮）
for n in range(199, 215): NEW_CAT[n] = "冷冻"
for n in range(215, 229): NEW_CAT[n] = "药水"

html_path = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\cooking.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 替换每条 DISHES 记录的 cat 字段
def replace_cat(m):
    no = int(m.group(1))
    new_c = NEW_CAT.get(no, m.group(2))
    return m.group(0).replace(f'cat:"{m.group(2)}"', f'cat:"{new_c}"')

pattern = re.compile(r'\{no:(\d+),\s*cat:"([^"]*)"')
new_html = pattern.sub(replace_cat, html)

# 验证
counts = {}
for m in pattern.finditer(new_html):
    no = int(m.group(1))
    c  = NEW_CAT.get(no, '?')
    counts[c] = counts.get(c, 0) + 1

print("新分类统计:")
for cat, cnt in sorted(counts.items()):
    print(f"  {cat}: {cnt} 种")
print(f"  总计: {sum(counts.values())} 种")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)
print("\ncooking.html 已更新")
