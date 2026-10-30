#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 cooking.html 中的料理数据和图片映射
"""

import json
import re

# 读取正确的映射
with open('correct_dishes_mapping.json', 'r', encoding='utf-8') as f:
    correct_dishes = json.load(f)

# 生成分类映射
def get_category(name):
    """根据料理名称推断分类"""
    if '烤' in name and any(x not in name for x in ['蘑菇', '鱼', '肉', '蛋', '螃蟹', '田螺', '树果', '橡子']):
        if '蘑菇' in name or '鱼' in name or '肉' in name or '蛋' in name or '螃蟹' in name or '田螺' in name or '树果' in name or '橡子' in name:
            return '烤食'
        return '烤食'
    elif '蒸' in name:
        return '蒸炒'
    elif '炒' in name and '烤' not in name:
        return '蒸炒'
    elif '煎' in name or '炸' in name:
        return '煎炸'
    elif '汤' in name:
        return '汤品'
    elif '炖' in name and '咖喱' not in name:
        return '汤品'
    elif '咖喱' in name:
        return '咖喱'
    elif '烩饭' in name or '菜饭' in name:
        return '烩饭'
    elif '盖饭' in name or '炒饭' in name:
        return '炒饭'
    elif '饭团' in name or '面包' in name or '披萨' in name or '派' in name or '蛋卷' in name:
        return '饭团面包'
    elif '蛋糕' in name or '可丽饼' in name or '蛋挞' in name or '牛奶' in name or '糖' in name or '香蕉' in name or '布丁' in name or '水果' in name or '苹果' in name:
        return '甜点'
    elif '怪物' in name or '魔人' in name or '奇异' in name or '过硬' in name or '巴伊' in name:
        return '特殊'
    elif '冰冻' in name or '冷冻' in name:
        return '冷冻'
    elif '药' in name:
        return '药水'
    elif '水煮' in name:
        return '特殊'
    else:
        return '烤食'

# 生成 JavaScript 数据
dishes_js = "const DISHES = [\n"
for dish in correct_dishes:
    cat = get_category(dish['name'])
    dishes_js += f'  {{no:{dish["no"]}, cat:"{cat}", name:"{dish["name"]}", img:"{dish["img"]}", ing:[]}},\n'
dishes_js += "];\n"

# 生成图片映射
img_map_js = "const DISH_IMG = {\n"
for i, dish in enumerate(correct_dishes):
    img_map_js += f'  {dish["no"]}:"{dish["img"]}"'
    if i < len(correct_dishes) - 1:
        img_map_js += ','
    if (i + 1) % 8 == 0:
        img_map_js += '\n'
    else:
        img_map_js += ' '
img_map_js += "\n};\n"

# 读取原始 HTML
with open('cooking.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 替换 DISH_IMG 映射
old_img_pattern = r'const DISH_IMG = \{[^}]+\};'
html_content = re.sub(old_img_pattern, img_map_js.rstrip() + ';', html_content, flags=re.DOTALL)

# 替换 DISHES 数据
old_dishes_pattern = r'const DISHES = \[[^\]]+\];'
html_content = re.sub(old_dishes_pattern, dishes_js.rstrip() + ';', html_content, flags=re.DOTALL)

# 写回 HTML
with open('cooking.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✓ cooking.html 已更新")
print(f"✓ 共更新 {len(correct_dishes)} 道料理数据")
print("✓ 图片映射已更正")
print("✓ 分类已自动分配")
