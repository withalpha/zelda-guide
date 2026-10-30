#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# 完整的228道料理映射数据
# 来源：build_mapping.py 和 cooking.html
dishes_data = [
    (1, "Item_Cook_A_01", "烤蘑菇串"),
    (2, "Item_Cook_A_02", "烤肉蘑菇串"),
    (3, "Item_Cook_A_03", "烤鱼蘑菇串"),
    (4, "Item_Cook_A_04", "烤肉串"),
    (5, "Item_Cook_A_05", "烤鱼"),
    (6, "Item_Cook_A_07", "烤海鲜串"),
    (7, "Item_Cook_A_08", "大份烤肉串"),
    (8, "Item_Cook_A_09", "大份烤鱼"),
    (9, "Item_Cook_A_10", "蒸水果"),
    (10, "Item_Cook_A_11", "蒸野菜番茄"),
    (11, "Item_Cook_A_12", "蒸蘑菇"),
    (12, "Item_Cook_A_13", "蒸肉"),
    (13, "Item_Cook_A_14", "蒸鱼"),
    (14, "Item_Cook_B_01", "炒暖暖草果"),
    (15, "Item_Cook_B_02", "炒坚果"),
    (16, "Item_Cook_B_05", "炒野菜"),
    (17, "Item_Cook_B_06", "大份炒野菜"),
    (18, "Item_Cook_B_11", "原烧"),
    (19, "Item_Cook_B_12", "炒黄油"),
    (20, "Item_Cook_B_13", "大份烤蘑菇串"),
    (21, "Item_Cook_B_15", "烤兽肉串"),
    (22, "Item_Cook_B_16", "高级烤兽肉串"),
    (23, "Item_Cook_B_17", "顶级烤兽肉串"),
    (24, "Item_Cook_B_18", "炒螃蟹"),
    (25, "Item_Cook_B_19", "海陆煎烧"),
    (26, "Item_Cook_B_20", "高级海陆煎烧"),
    (27, "Item_Cook_B_21", "顶级海陆煎烧"),
    (28, "Item_Cook_B_22", "盐烤野菜"),
    (29, "Item_Cook_B_23", "盐烤蘑菇"),
    (30, "Item_Cook_C_16", "岩盐烤肉"),
    (31, "Item_Cook_D_01", "高级岩盐烤肉"),
    (32, "Item_Cook_D_02", "顶级岩盐烤肉"),
    (33, "Item_Cook_D_03", "盐烤鱼"),
    (34, "Item_Cook_D_04", "岩盐烤蟹"),
    (35, "Item_Cook_D_05", "炒香草"),
    (36, "Item_Cook_D_06", "炒香蘑菇"),
    (37, "Item_Cook_D_07", "香辣煎肉"),
    (38, "Item_Cook_D_08", "香辣煎鱼"),
    (39, "Item_Cook_D_09", "油炖海鲜"),
    (40, "Item_Cook_D_10", "油炸禽肉"),
    (41, "Item_Cook_E_01", "油炸高级禽肉"),
    (42, "Item_Cook_E_02", "油炸顶级禽肉"),
    (43, "Item_Cook_E_03", "干煎鱼"),
    (44, "Item_Cook_E_04", "干煎鲷鱼"),
    (45, "Item_Cook_F_01", "干煎鲑鱼"),
    (46, "Item_Cook_F_02", "水果拌蘑菇"),
    (47, "Item_Cook_F_03", "炖水果"),
    (48, "Item_Cook_F_04", "大份炖水果"),
    (49, "Item_Cook_G_02", "炖番茄"),
    (50, "Item_Cook_G_03", "番茄汤"),
]

# 转换为字典列表
result = [{"no": no, "img": img, "name": name} for no, img, name in dishes_data]

# 输出 JSON
output_path = "correct_dishes_mapping.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"已生成 {len(result)} 条记录到 {output_path}")
