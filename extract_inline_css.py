#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取所有HTML文件的内联CSS并整合到外部文件
"""

import os
import re
from pathlib import Path

def extract_inline_css(html_file):
    """提取HTML文件中的内联CSS"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找<style>标签中的CSS
    pattern = r'<style>(.*?)</style>'
    matches = re.findall(pattern, content, re.DOTALL)
    
    if not matches:
        return None, content
    
    # 合并所有内联CSS
    inline_css = '\n\n'.join(matches)
    
    # 从HTML中移除style标签
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    return inline_css, new_content

def process_files():
    """处理所有HTML文件"""
    base_dir = Path(__file__).parent
    html_files = list(base_dir.glob('*.html'))
    
    # 排除已处理的index.html
    html_files = [f for f in html_files if f.name != 'index.html']
    
    all_css = {}
    
    for html_file in html_files:
        print(f"处理: {html_file.name}...")
        css, new_content = extract_inline_css(html_file)
        
        if css:
            all_css[html_file.name] = css
            print(f"  ✓ 提取了 {len(css)} 字符的CSS")
            
            # 在head中添加对style.css的引用（如果还没有）
            if 'href="style.css"' not in new_content and 'href="./style.css"' not in new_content:
                # 在</head>前添加
                new_content = new_content.replace('</head>', '  <link rel="stylesheet" href="style.css">\n</head>')
                print(f"  ✓ 添加了style.css引用")
            
            # 保存修改后的HTML
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✓ 已更新HTML文件")
        else:
            print(f"  - 没有找到内联CSS")
    
    if all_css:
        # 将所有CSS写入单独的文件
        css_output_file = base_dir / 'extracted_inline_css.css'
        with open(css_output_file, 'w', encoding='utf-8') as f:
            f.write('/* ═══════════════════════════════════════════════\n')
            f.write('   从各页面提取的内联CSS\n')
            f.write('   自动生成 - 请手动整理并合并到style.css\n')
            f.write('═══════════════════════════════════════════════ */\n\n')
            
            for filename, css in all_css.items():
                f.write(f'\n/* ═════════ {filename} ═════════ */\n')
                f.write(css)
                f.write('\n')
        
        print(f"\n✅ 完成！共处理 {len(all_css)} 个文件")
        print(f"📄 提取的CSS已保存至: {css_output_file}")
        print(f"\n下一步：")
        print(f"  1. 查看 extracted_inline_css.css")
        print(f"  2. 手动审查并合并到 style.css")
        print(f"  3. 删除 extracted_inline_css.css")
    else:
        print("\n没有找到任何内联CSS")

if __name__ == '__main__':
    process_files()
