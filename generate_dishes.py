#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# 读取JSON映射
with open('correct_dishes_mapping.json', 'r', encoding='utf-8') as f:
    dishes_data = json.load(f)

# 定义分类映射（根据编号范围）
def get_category(no):
    if 1 <= no <= 29:
        return '烧烤'
    elif 30 <= no <= 44:
        return '蒸炒'
    elif 45 <= no <= 62:
        return '煎炸'
    elif 63 <= no <= 79:
        return '汤品'
    elif 80 <= no <= 89:
        return '咖喱'
    elif 90 <= no <= 99:
        return '炖肉'
    elif 100 <= no <= 146:
        return '饭团面包'
    elif 147 <= no <= 197:
        return '烤食'
    elif 198 <= no <= 198:
        return '特殊'
    elif 199 <= no <= 214:
        return '冷冻'
    elif 215 <= no <= 228:
        return '药水'
    return '特殊'

# 生成DISHES数组
dishes_array = []
for dish in dishes_data:
    no = dish['no']
    name = dish['name']
    cat = get_category(no)
    dishes_array.append({'no': no, 'cat': cat, 'name': name, 'ing': []})

# 输出为JavaScript格式
output = 'const DISHES = [\n'
for i, dish in enumerate(dishes_array):
    comma = ',' if i < len(dishes_array) - 1 else ''
    output += f'  {{no:{dish["no"]}, cat:"{dish["cat"]}", name:"{dish["name"]}", ing:[]}}' + comma + '\n'
output += '];'

# 保存到文件
with open('dishes_output.js', 'w', encoding='utf-8') as f:
    f.write(output)

print("DISHES数组已生成到 dishes_output.js")
print(f"总共生成了 {len(dishes_array)} 道菜肴")
