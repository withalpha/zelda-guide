#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网站健康检查脚本
检查HTML文件的SEO问题、内部链接、图片alt属性等
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import json

def check_html_file(filepath):
    """检查单个HTML文件的问题"""
    issues = []
    warnings = []
    info = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
    
    filename = os.path.basename(filepath)
    
    # 1. 检查title标签
    title = soup.find('title')
    if not title:
        issues.append(f"❌ 缺少 <title> 标签")
    elif len(title.text) < 20:
        warnings.append(f"⚠️  title太短（{len(title.text)}字符）: {title.text}")
    elif len(title.text) > 70:
        warnings.append(f"⚠️  title太长（{len(title.text)}字符）: {title.text}")
    else:
        info.append(f"✓ title长度合适: {title.text}")
    
    # 2. 检查meta description
    meta_desc = soup.find('meta', {'name': 'description'})
    if not meta_desc:
        issues.append(f"❌ 缺少 meta description")
    elif meta_desc.get('content'):
        desc_len = len(meta_desc['content'])
        if desc_len < 50:
            warnings.append(f"⚠️  description太短（{desc_len}字符）")
        elif desc_len > 160:
            warnings.append(f"⚠️  description太长（{desc_len}字符）")
        else:
            info.append(f"✓ description长度合适（{desc_len}字符）")
    
    # 3. 检查H1标签
    h1_tags = soup.find_all('h1')
    if len(h1_tags) == 0:
        issues.append(f"❌ 缺少 H1 标签")
    elif len(h1_tags) > 1:
        warnings.append(f"⚠️  有多个 H1 标签（{len(h1_tags)}个）")
    else:
        info.append(f"✓ H1标签正常")
    
    # 4. 检查图片alt属性
    images = soup.find_all('img')
    images_without_alt = []
    for img in images:
        if not img.get('alt'):
            src = img.get('src', '未知路径')
            images_without_alt.append(src)
    
    if images_without_alt:
        issues.append(f"❌ {len(images_without_alt)}个图片缺少alt属性")
        if len(images_without_alt) <= 5:
            for src in images_without_alt:
                issues.append(f"   - {src}")
    elif images:
        info.append(f"✓ 所有图片都有alt属性")
    
    # 5. 检查内联style标签
    inline_styles = soup.find_all('style')
    if inline_styles:
        total_css_len = sum(len(style.string or '') for style in inline_styles)
        if total_css_len > 100:
            warnings.append(f"⚠️  有内联CSS（{total_css_len}字符），建议移到外部CSS文件")
    
    # 6. 检查内部链接数量
    internal_links = []
    external_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('http'):
            if 'zeldaguide.ccwu.cc' in href:
                internal_links.append(href)
            else:
                external_links.append(href)
        elif href.startswith('/') or href.endswith('.html'):
            internal_links.append(href)
    
    info.append(f"✓ 内部链接: {len(internal_links)}个, 外部链接: {len(external_links)}个")
    
    # 7. 检查canonical标签
    canonical = soup.find('link', {'rel': 'canonical'})
    if not canonical:
        warnings.append(f"⚠️  缺少 canonical 标签")
    else:
        info.append(f"✓ 有canonical标签")
    
    # 8. 检查Open Graph标签
    og_tags = soup.find_all('meta', property=re.compile('^og:'))
    if len(og_tags) < 3:
        warnings.append(f"⚠️  Open Graph标签不完整（{len(og_tags)}个）")
    else:
        info.append(f"✓ Open Graph标签完整（{len(og_tags)}个）")
    
    # 9. 检查结构化数据
    structured_data = soup.find_all('script', type='application/ld+json')
    if not structured_data:
        warnings.append(f"⚠️  缺少结构化数据（Schema.org）")
    else:
        info.append(f"✓ 有结构化数据")
    
    return {
        'file': filename,
        'issues': issues,
        'warnings': warnings,
        'info': info,
        'internal_links_count': len(internal_links),
        'images_count': len(images),
        'images_without_alt': len(images_without_alt)
    }

def main():
    """主函数"""
    base_dir = Path(__file__).parent
    html_files = list(base_dir.glob('*.html'))
    
    print("=" * 70)
    print("🔍 网站健康检查报告")
    print("=" * 70)
    print()
    
    all_results = []
    total_issues = 0
    total_warnings = 0
    
    for html_file in sorted(html_files):
        result = check_html_file(html_file)
        all_results.append(result)
        
        if result['issues'] or result['warnings']:
            print(f"\n📄 {result['file']}")
            print("-" * 70)
            
            for issue in result['issues']:
                print(f"  {issue}")
                total_issues += 1
            
            for warning in result['warnings']:
                print(f"  {warning}")
                total_warnings += 1
            
            # 只显示前2条info信息，避免输出过长
            for info_msg in result['info'][:2]:
                print(f"  {info_msg}")
    
    # 统计汇总
    print("\n" + "=" * 70)
    print("📊 检查汇总")
    print("=" * 70)
    print(f"检查文件数: {len(html_files)}")
    print(f"发现问题: {total_issues}个")
    print(f"发现警告: {total_warnings}个")
    
    # 统计缺少alt的图片总数
    total_images_without_alt = sum(r['images_without_alt'] for r in all_results)
    total_images = sum(r['images_count'] for r in all_results)
    print(f"图片总数: {total_images}, 缺少alt: {total_images_without_alt}")
    
    # 找出内部链接最少的页面
    print("\n📈 内部链接统计（前5名）:")
    sorted_by_links = sorted(all_results, key=lambda x: x['internal_links_count'])
    for r in sorted_by_links[:5]:
        print(f"  {r['file']}: {r['internal_links_count']}个内部链接")
    
    print("\n" + "=" * 70)
    
    # 保存详细报告为JSON
    report_path = base_dir / 'website_health_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 详细报告已保存至: {report_path}")
    
    # 给出优化建议
    print("\n💡 优化建议:")
    if total_images_without_alt > 0:
        print(f"  1. 为 {total_images_without_alt} 个图片添加alt属性")
    
    # 检查index.html的内联CSS
    index_result = next((r for r in all_results if r['file'] == 'index.html'), None)
    if index_result:
        for warning in index_result['warnings']:
            if '内联CSS' in warning:
                print(f"  2. 将index.html的内联CSS移到style.css")
                break
    
    if total_warnings > 5:
        print(f"  3. 解决 {total_warnings} 个警告项，提升SEO质量")
    
    print(f"  4. 增加页面间的内部链接，提高页面权重传递")
    print(f"  5. 考虑压缩图片，提升页面加载速度")

if __name__ == '__main__':
    main()
