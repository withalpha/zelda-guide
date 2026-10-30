#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

# 读取正确的映射
with open('correct_dishes_mapping.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

# 读取cooking.html
with open('cooking.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 生成新的DISHES数组
dishes_array = "const DISHES = [\n"
for item in mapping:
    no = item['no']
    name = item['name']
    # 暂时使用空的食材数组，后续可以补充
    dishes_array += f'  {{no:{no},  cat:"未分类", name:"{name}",       ing:[]}},\n'
dishes_array += "];\n"

# 找到并替换DISHES数组
# 查找从 "const DISHES = [" 到 "];" 的部分
pattern = r'const DISHES = \[[\s\S]*?\];'
new_html = re.sub(pattern, dishes_array.rstrip('\n'), html_content)

# 保存修改后的HTML
with open('cooking.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("✓ 已成功更新cooking.html中的DISHES数组")
print(f"✓ 总共更新了 {len(mapping)} 道料理")
print(f"✓ 前5条记录:")
for i in range(min(5, len(mapping))):
    item = mapping[i]
    print(f"  No.{item['no']:3d}: {item['name']:20s} → {item['img']}")
