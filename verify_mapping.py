#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 从build_mapping.py中的正确映射
correct_mapping = {
    1:  ("Item_Cook_A_01", "烤蘑菇串"),
    2:  ("Item_Cook_A_02", "烤肉蘑菇串"),
    3:  ("Item_Cook_A_03", "烤鱼蘑菇串"),
    4:  ("Item_Cook_A_04", "烤肉串"),
    5:  ("Item_Cook_A_05", "烤鱼"),
    6:  ("Item_Cook_A_07", "烤海鲜串"),
    7:  ("Item_Cook_A_08", "大份烤肉串"),
    8:  ("Item_Cook_A_09", "大份烤鱼"),
    9:  ("Item_Cook_A_10", "蒸水果"),
    10: ("Item_Cook_A_11", "蒸野菜番茄"),
    11: ("Item_Cook_A_12", "蒸蘑菇"),
    12: ("Item_Cook_A_13", "蒸肉"),
    13: ("Item_Cook_A_14", "蒸鱼"),
    14: ("Item_Cook_B_01", "炒暖暖草果"),
    15: ("Item_Cook_B_02", "炒坚果"),
    16: ("Item_Cook_B_05", "炒野菜"),
    17: ("Item_Cook_B_06", "大份炒野菜"),
    18: ("Item_Cook_B_11", "原烧"),
    19: ("Item_Cook_B_12", "炒黄油"),
    20: ("Item_Cook_B_13", "大份烤蘑菇串"),
}

# 从cooking.html中读取DISHES数组
import re
with open('cooking.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
# 提取前20个料理
pattern = r'\{no:(\d+),\s*cat:"([^"]+)",\s*name:"([^"]+)"'
matches = re.findall(pattern, content)

print("=" * 80)
print("验证cooking.html中的料理名称与图片映射")
print("=" * 80)

errors = []
for no_str, cat, name in matches[:20]:
    no = int(no_str)
    if no in correct_mapping:
        img, correct_name = correct_mapping[no]
        status = "✓" if name == correct_name else "✗"
        print(f"{status} No.{no:3d}: {name:20s} (应为: {correct_name:20s}) → {img}")
        if name != correct_name:
            errors.append((no, name, correct_name, img))
    else:
        print(f"? No.{no:3d}: {name:20s} (未在映射中找到)")

if errors:
    print("\n" + "=" * 80)
    print(f"发现 {len(errors)} 个错误:")
    for no, actual, correct, img in errors:
        print(f"  No.{no}: '{actual}' 应改为 '{correct}'")
else:
    print("\n✓ 前20个料理名称都正确!")
