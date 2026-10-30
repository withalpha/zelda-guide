#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 从build_mapping.py中提取的正确映射和名称
correct_data = {
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

# 输出前20个
print("正确的料理映射（前20个）:")
print("=" * 80)
for no in range(1, 21):
    if no in correct_data:
        img, name = correct_data[no]
        print(f"No.{no:3d}: {name:20s} → {img}")
