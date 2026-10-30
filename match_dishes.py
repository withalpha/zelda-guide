"""
将 Item_Cook*.png 与 cooking/1-5.jpg 做图像相似度匹配
策略：
1. 对每张参考图做滑动窗口，提取图标区域（每个格子左上角的图标）
2. 用 perceptual hash 比较相似度
3. 输出匹配结果到 txt 和 excel
"""

import os
import json
import imagehash
import openpyxl
from PIL import Image
import numpy as np

# ── 路径配置 ──────────────────────────────────────────────────────────────────
ITEMS_DIR   = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\Items'
COOKING_DIR = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\images\cooking'
OUT_DIR     = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页'

# ── 参考图网格参数（通过分析得出）────────────────────────────────────────────
# 每张参考图：600px宽，4列，每列150px
# 每行高度约132px，图标在格子左上角，约80x80px
COLS      = 4
CELL_W    = 150
CELL_H    = 132
# 图标在格子内的偏移和尺寸（图标居中在格子上半部分）
ICON_SIZE = 80   # 裁切图标的尺寸
ICON_X_OFF = (CELL_W - ICON_SIZE) // 2   # 35
ICON_Y_OFF = 10  # 距格子顶部10px

# ── 第一步：从参考图裁切所有图标格子 ─────────────────────────────────────────
print("=== 第一步：裁切参考图格子 ===")

ref_cells = []  # list of (img_idx, row, col, icon_image)

for img_idx in range(1, 6):
    path = os.path.join(COOKING_DIR, f'{img_idx}.jpg')
    img  = Image.open(path).convert('RGBA')
    w, h = img.size
    
    # 计算行数
    rows = h // CELL_H
    
    for r in range(rows):
        for c in range(COLS):
            x0 = c * CELL_W + ICON_X_OFF
            y0 = r * CELL_H + ICON_Y_OFF
            x1 = x0 + ICON_SIZE
            y1 = y0 + ICON_SIZE
            
            if y1 > h:
                continue
            
            icon = img.crop((x0, y0, x1, y1)).resize((64, 64), Image.LANCZOS)
            ref_cells.append({
                'img_idx': img_idx,
                'row': r,
                'col': c,
                'icon': icon,
                'hash': imagehash.phash(icon)
            })

print(f"  共裁切 {len(ref_cells)} 个参考格子")

# ── 第二步：加载所有 Item_Cook 图片并计算哈希 ─────────────────────────────────
print("\n=== 第二步：加载 Item_Cook 图片 ===")

item_files = sorted([
    f for f in os.listdir(ITEMS_DIR)
    if f.startswith('Item_Cook') and f.endswith('.png') and f != 'Item_CookSet.png'
])

print(f"  共找到 {len(item_files)} 个 Item_Cook 图片")

items = []
for fname in item_files:
    path = os.path.join(ITEMS_DIR, fname)
    img  = Image.open(path).convert('RGBA')
    
    # Item_Cook 图片通常有透明背景，取图标主体
    # 缩放到64x64
    icon = img.resize((64, 64), Image.LANCZOS)
    h_val = imagehash.phash(icon)
    
    items.append({
        'filename': fname,
        'icon': icon,
        'hash': h_val
    })

# ── 第三步：匹配 ──────────────────────────────────────────────────────────────
print("\n=== 第三步：图像哈希匹配 ===")

# 预计算所有参考格子的哈希列表
ref_hashes = [cell['hash'] for cell in ref_cells]

results = []
for item in items:
    best_dist  = 999
    best_cell  = None
    
    for cell in ref_cells:
        dist = item['hash'] - cell['hash']
        if dist < best_dist:
            best_dist = dist
            best_cell = cell
    
    results.append({
        'filename':  item['filename'],
        'best_dist': best_dist,
        'img_idx':   best_cell['img_idx'],
        'row':       best_cell['row'],
        'col':       best_cell['col'],
    })

# ── 第四步：用模板匹配做二次验证（对哈希距离>10的做精确匹配）────────────────
print("\n=== 第四步：模板匹配精确验证 ===")

# 加载参考图（灰度）
ref_imgs_gray = {}
for i in range(1, 6):
    path = os.path.join(COOKING_DIR, f'{i}.jpg')
    ref_imgs_gray[i] = np.array(Image.open(path).convert('L'), dtype=np.float32)

def template_match(item_img, ref_gray):
    """在参考图上滑动匹配模板，返回最佳位置和相似度"""
    import cv2
    tmpl = np.array(item_img.convert('L').resize((64, 64)), dtype=np.float32)
    
    # 缩放模板到不同尺寸匹配
    best_val = -1
    best_loc = (0, 0)
    best_scale = 1.0
    
    for scale in [0.8, 0.9, 1.0, 1.1, 1.2]:
        sz = int(64 * scale)
        if sz < 20:
            continue
        t = cv2.resize(tmpl, (sz, sz))
        if t.shape[0] > ref_gray.shape[0] or t.shape[1] > ref_gray.shape[1]:
            continue
        res = cv2.matchTemplate(ref_gray, t, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > best_val:
            best_val = max_val
            best_loc = max_loc
            best_scale = scale
    
    return best_val, best_loc, best_scale

# 检查是否有 opencv
try:
    import cv2
    HAS_CV2 = True
    print("  OpenCV 可用，进行模板匹配验证")
except ImportError:
    HAS_CV2 = False
    print("  OpenCV 不可用，仅使用哈希匹配结果")

if HAS_CV2:
    for r in results:
        if r['best_dist'] > 8:  # 哈希距离较大的重新验证
            item_img = Image.open(os.path.join(ITEMS_DIR, r['filename'])).convert('RGBA')
            # 去掉透明背景，转灰度
            bg = Image.new('RGB', item_img.size, (255, 255, 255))
            bg.paste(item_img, mask=item_img.split()[3])
            item_gray = np.array(bg.convert('L'), dtype=np.float32)
            
            best_val_all = -1
            best_img_idx = r['img_idx']
            
            for img_idx in range(1, 6):
                val, loc, scale = template_match(bg, ref_imgs_gray[img_idx])
                if val > best_val_all:
                    best_val_all = val
                    best_img_idx = img_idx
                    best_loc_all = loc
                    best_scale_all = scale
            
            # 根据位置推算行列
            col = best_loc_all[0] // CELL_W
            row = best_loc_all[1] // CELL_H
            
            r['img_idx']   = best_img_idx
            r['row']       = row
            r['col']       = col
            r['cv2_score'] = best_val_all

# ── 第五步：构建料理名称映射 ──────────────────────────────────────────────────
# 参考图中每个格子对应的料理名称
# 根据塞尔达传说：王国之泪的料理图鉴顺序
# 5张图共 22+22+22+22+12=100 行 × 4列 = 400格（但实际料理数量约160种）
# 需要知道每个格子的名称 —— 从 correct_dishes_mapping.json 获取

print("\n=== 第五步：加载料理名称映射 ===")

mapping_path = os.path.join(OUT_DIR, 'correct_dishes_mapping.json')
if os.path.exists(mapping_path):
    with open(mapping_path, 'r', encoding='utf-8') as f:
        dishes_mapping = json.load(f)
    print(f"  加载了 {len(dishes_mapping)} 条料理映射")
else:
    dishes_mapping = {}
    print("  未找到 correct_dishes_mapping.json")

# ── 第六步：输出结果 ──────────────────────────────────────────────────────────
print("\n=== 第六步：输出结果 ===")

# 按哈希距离排序，距离越小越可信
results.sort(key=lambda x: x['best_dist'])

# 写 TXT
txt_path = os.path.join(OUT_DIR, 'item_cook_mapping.txt')
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write("Item_Cook 图片 → 参考图位置 匹配结果\n")
    f.write("=" * 70 + "\n")
    f.write(f"{'文件名':<35} {'参考图':<8} {'行':<5} {'列':<5} {'哈希距离':<10}\n")
    f.write("-" * 70 + "\n")
    for r in sorted(results, key=lambda x: x['filename']):
        dish_name = dishes_mapping.get(r['filename'], '未知')
        f.write(f"{r['filename']:<35} {r['img_idx']}.jpg   {r['row']:<5} {r['col']:<5} {r['best_dist']:<10} {dish_name}\n")

print(f"  TXT 已保存: {txt_path}")

# 写 Excel
xlsx_path = os.path.join(OUT_DIR, 'item_cook_mapping.xlsx')
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "料理匹配结果"

headers = ['Item_Cook文件名', '参考图', '行(0起)', '列(0起)', '哈希距离', '料理名称(如有)']
ws.append(headers)

# 设置列宽
ws.column_dimensions['A'].width = 40
ws.column_dimensions['B'].width = 12
ws.column_dimensions['C'].width = 10
ws.column_dimensions['D'].width = 10
ws.column_dimensions['E'].width = 12
ws.column_dimensions['F'].width = 30

# 表头样式
from openpyxl.styles import Font, PatternFill, Alignment
header_font = Font(bold=True, color='FFFFFF')
header_fill = PatternFill(fill_type='solid', fgColor='2E75B6')
for cell in ws[1]:
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center')

# 数据行
for r in sorted(results, key=lambda x: x['filename']):
    dish_name = dishes_mapping.get(r['filename'], '')
    row_data = [
        r['filename'],
        f"{r['img_idx']}.jpg",
        r['row'],
        r['col'],
        r['best_dist'],
        dish_name
    ]
    ws.append(row_data)
    
    # 根据哈希距离着色
    row_num = ws.max_row
    dist = r['best_dist']
    if dist <= 5:
        fill_color = 'C6EFCE'   # 绿色 - 高置信度
    elif dist <= 10:
        fill_color = 'FFEB9C'   # 黄色 - 中等置信度
    else:
        fill_color = 'FFC7CE'   # 红色 - 低置信度

    fill = PatternFill(fill_type='solid', fgColor=fill_color)
    for col_idx in range(1, 7):
        ws.cell(row=row_num, column=col_idx).fill = fill

# 添加图例
ws2 = wb.create_sheet("图例说明")
ws2.append(['颜色', '含义', '哈希距离范围'])
ws2.append(['绿色', '高置信度匹配', '0-5'])
ws2.append(['黄色', '中等置信度', '6-10'])
ws2.append(['红色', '低置信度，需人工确认', '>10'])

wb.save(xlsx_path)
print(f"  Excel 已保存: {xlsx_path}")

# 打印统计
high   = sum(1 for r in results if r['best_dist'] <= 5)
medium = sum(1 for r in results if 5 < r['best_dist'] <= 10)
low    = sum(1 for r in results if r['best_dist'] > 10)
print(f"\n匹配统计:")
print(f"  高置信度 (距离≤5):  {high} 个")
print(f"  中置信度 (距离6-10): {medium} 个")
print(f"  低置信度 (距离>10): {low} 个")
print(f"  总计: {len(results)} 个")

# 打印前20条结果预览
print("\n前20条匹配结果预览:")
print(f"{'文件名':<35} {'参考图':<8} {'行':<4} {'列':<4} {'距离'}")
print("-" * 60)
for r in sorted(results, key=lambda x: x['filename'])[:20]:
    print(f"{r['filename']:<35} {r['img_idx']}.jpg  {r['row']:<4} {r['col']:<4} {r['best_dist']}")
