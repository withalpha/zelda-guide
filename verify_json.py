#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# 读取并验证 JSON 文件
with open('correct_dishes_mapping.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"总记录数: {len(data)}")
print()
print("前5条记录:")
for item in data[:5]:
    print(f"  No.{item['no']:3d}: {item['name']:20s} -> {item['img']}")

print()
print("最后5条记录:")
for item in data[-5:]:
    print(f"  No.{item['no']:3d}: {item['name']:20s} -> {item['img']}")

print()
print("验证完成！✓")
