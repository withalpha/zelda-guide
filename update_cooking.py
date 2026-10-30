#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

# 读取新的DISHES数组
with open('dishes_output.js', 'r', encoding='utf-8') as f:
    new_dishes = f.read()

# 读取cooking.html
with open('cooking.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 使用正则表达式找到并替换DISHES数组
# 从 "const DISHES = [" 到 "];" 的部分
pattern = r'const DISHES = \[.*?\];'
replacement = new_dishes

# 使用DOTALL标志使.匹配换行符
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# 保存更新后的cooking.html
with open('cooking.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("cooking.html已成功更新！")
print("DISHES数组已替换为正确的映射。")
