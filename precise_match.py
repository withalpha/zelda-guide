"""
精确图像匹配：Item_Cook*.png  ←→  cooking/1-5.jpg 中的图标格子
网格参数（通过像素分析得出）：
  列分隔线: x = 0, 38, 110, 203, 308, 599
  图标区域: x = 38~110 (72px)
  行分隔线: y = 0, 29, 95, 161, 227 ... (第0行29px标题, 之后每行66px)
  数据行起始: y = 29, 95, 161, 227, ...
"""

import os, json, cv2, imagehash, openpyxl
import numpy as np
from PIL import Image
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE      = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页'
ITEMS_DIR = os.path.join(BASE, 'Items')
COOK_DIR  = os.path.join(BASE, 'images', 'cooking')
DEBUG_DIR = os.path.join(BASE, 'debug_cells')
os.makedirs(DEBUG_DIR, exist_ok=True)

# ── 网格参数 ──────────────────────────────────────────────────────────────────
ICON_X0   = 39    # 图标列左边界
ICON_X1   = 109   # 图标列右边界  (72px)
ROW_START = 29    # 第一个数据行起始y
ROW_H     = 66    # 每行高度

# ── 用 PIL 读图（支持中文路径）→ numpy ────────────────────────────────────────
def pil_read(path):
    return np.array(Image.open(path).convert('RGB'))

# ── 裁切参考图中所有图标格子 ──────────────────────────────────────────────────
print("=== 裁切参考图图标格子 ===")
ref_cells = []   # {img_idx, row, icon_rgb, icon_gray, hash}

for img_idx in range(1, 6):
    path    = os.path.join(COOK_DIR, f'{img_idx}.jpg')
    ref_rgb = pil_read(path)
    H       = ref_rgb.shape[0]
    
    row = 0
    y   = ROW_START
    while y + ROW_H <= H:
        # 裁切图标区域，留1px内边距避免边框
        icon_rgb = ref_rgb[y+1 : y+ROW_H-1, ICON_X0+1 : ICON_X1-1]
        icon_pil = Image.fromarray(icon_rgb).resize((64, 64), Image.LANCZOS)
        
        # 保存前几个调试用
        if img_idx == 1 and row < 5:
            icon_pil.save(os.path.join(DEBUG_DIR, f'ref_{img_idx}_r{row:02d}.png'))
        
        h = imagehash.phash(icon_pil, hash_size=16)
        ref_cells.append({
            'img_idx': img_idx,
            'row':     row,
            'y0':      y,
            'icon':    icon_pil,
            'hash':    h,
        })
        row += 1
        y   += ROW_H
    
    print(f"  {img_idx}.jpg → {row} 行图标")

print(f"  共 {len(ref_cells)} 个参考格子")

# ── 加载 Item_Cook 图片 ───────────────────────────────────────────────────────
print("\n=== 加载 Item_Cook 图片 ===")
item_files = sorted([
    f for f in os.listdir(ITEMS_DIR)
    if f.startswith('Item_Cook') and f.endswith('.png') and f != 'Item_CookSet.png'
])
print(f"  共 {len(item_files)} 个")

items = []
for fname in item_files:
    path    = os.path.join(ITEMS_DIR, fname)
    pil_img = Image.open(path).convert('RGBA')
    
    # 去透明背景 → 白底
    bg = Image.new('RGB', pil_img.size, (255, 255, 255))
    bg.paste(pil_img, mask=pil_img.split()[3])
    icon = bg.resize((64, 64), Image.LANCZOS)
    
    # 保存前几个调试用
    if len(items) < 5:
        icon.save(os.path.join(DEBUG_DIR, f'item_{fname}'))
    
    h = imagehash.phash(icon, hash_size=16)
    items.append({'filename': fname, 'icon': icon, 'hash': h})

# ── 哈希匹配 ─────────────────────────────────────────────────────────────────
print("\n=== 哈希匹配 ===")

# 同时用 phash + dhash + ahash 三种哈希投票
def multi_hash(pil_img):
    return {
        'p': imagehash.phash(pil_img, hash_size=16),
        'd': imagehash.dhash(pil_img, hash_size=16),
        'a': imagehash.average_hash(pil_img, hash_size=16),
        'w': imagehash.whash(pil_img, hash_size=16),
    }

print("  计算参考格子多重哈希...")
for cell in ref_cells:
    cell['mh'] = multi_hash(cell['icon'])

print("  计算 Item 多重哈希...")
for item in items:
    item['mh'] = multi_hash(item['icon'])

print("  开始匹配...")
results = []

for item in items:
    best_score = 9999
    best_cell  = None
    
    for cell in ref_cells:
        # 四种哈希距离加权求和（越小越相似）
        score = (
            (item['mh']['p'] - cell['mh']['p']) * 1.0 +
            (item['mh']['d'] - cell['mh']['d']) * 1.0 +
            (item['mh']['a'] - cell['mh']['a']) * 0.5 +
            (item['mh']['w'] - cell['mh']['w']) * 1.0
        )
        if score < best_score:
            best_score = score
            best_cell  = cell
    
    results.append({
        'filename': item['filename'],
        'img_key':  item['filename'].replace('.png', ''),
        'img_idx':  best_cell['img_idx'],
        'row':      best_cell['row'],
        'score':    round(best_score, 2),
        'item_icon': item['icon'],
        'ref_icon':  best_cell['icon'],
    })

# ── 用 OpenCV 模板匹配做二次精确验证 ─────────────────────────────────────────
print("\n=== OpenCV 模板匹配精确验证 ===")

# 加载参考图灰度（PIL读取避免中文路径问题）
ref_grays = {}
for i in range(1, 6):
    path = os.path.join(COOK_DIR, f'{i}.jpg')
    ref_grays[i] = np.array(Image.open(path).convert('L'), dtype=np.uint8)

def cv_match_icon(item_pil, ref_gray_dict):
    """在参考图的图标列区域做模板匹配"""
    # 将 item 转灰度
    item_gray = np.array(item_pil.convert('L'), dtype=np.uint8)
    
    best_val  = -1
    best_idx  = 1
    best_row  = 0
    
    for idx, rg in ref_gray_dict.items():
        H = rg.shape[0]
        # 只在图标列区域搜索
        icon_col = rg[:, ICON_X0:ICON_X1]
        
        for scale in [0.9, 1.0, 1.1]:
            new_sz = max(8, int(64 * scale))
            tmpl   = cv2.resize(item_gray, (new_sz, new_sz))
            
            if tmpl.shape[0] > icon_col.shape[0] or tmpl.shape[1] > icon_col.shape[1]:
                continue
            
            res = cv2.matchTemplate(icon_col, tmpl, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            
            if max_val > best_val:
                best_val = max_val
                best_idx = idx
                # 推算行号
                match_y  = max_loc[1]
                best_row = max(0, (match_y - ROW_START + ROW_H//2) // ROW_H)
    
    return best_val, best_idx, best_row

print("  对所有结果做 OpenCV 验证...")
for r in results:
    item_pil = r['item_icon']
    cv_val, cv_idx, cv_row = cv_match_icon(item_pil, ref_grays)
    r['cv_score'] = round(float(cv_val), 4)
    r['cv_idx']   = cv_idx
    r['cv_row']   = cv_row
    
    # 综合判断：哈希和CV都同意则高置信
    r['agree'] = (r['img_idx'] == cv_idx)

# ── 生成对比图（保存前10个匹配对） ───────────────────────────────────────────
print("\n=== 保存匹配对比图 ===")
for i, r in enumerate(results[:15]):
    # 并排显示 item 和 ref
    combined = Image.new('RGB', (140, 64), (200, 200, 200))
    combined.paste(r['item_icon'], (0, 0))
    combined.paste(r['ref_icon'],  (76, 0))
    combined.save(os.path.join(DEBUG_DIR, f'match_{i:03d}_{r["filename"]}.png'))

# ── 统计 ──────────────────────────────────────────────────────────────────────
agree_count = sum(1 for r in results if r['agree'])
print(f"\n哈希与CV匹配一致: {agree_count}/{len(results)}")

# ── 写 TXT ────────────────────────────────────────────────────────────────────
txt_path = os.path.join(BASE, 'item_cook_mapping.txt')
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write("塞尔达传说：王国之泪 — Item_Cook 图片 → 参考图位置 精确匹配结果\n")
    f.write("匹配方法：多重感知哈希(phash+dhash+whash) + OpenCV模板匹配\n")
    f.write("=" * 80 + "\n")
    f.write(f"{'文件名':<42} {'哈希图':<8} {'哈希行':<6} {'CV图':<6} {'CV行':<6} {'CV得分':<8} {'一致'}\n")
    f.write("-" * 80 + "\n")
    for r in results:
        agree_mark = '✓' if r['agree'] else '✗'
        f.write(f"{r['filename']:<42} {r['img_idx']}.jpg  {r['row']:<6} "
                f"{r['cv_idx']}.jpg {r['cv_row']:<6} {r['cv_score']:<8} {agree_mark}\n")
    f.write("-" * 80 + "\n")
    f.write(f"哈希与CV一致: {agree_count}/{len(results)}\n")

print(f"TXT 已保存: {txt_path}")

# ── 写 Excel ──────────────────────────────────────────────────────────────────
xlsx_path = os.path.join(BASE, 'item_cook_mapping.xlsx')
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "匹配结果"

thin  = Side(style='thin', color='CCCCCC')
bdr   = Border(left=thin, right=thin, top=thin, bottom=thin)
ctr   = Alignment(horizontal='center', vertical='center')
lft   = Alignment(horizontal='left',   vertical='center')

def hdr(cell, text, bg='1F4E79'):
    cell.value     = text
    cell.font      = Font(bold=True, color='FFFFFF', size=10)
    cell.fill      = PatternFill(fill_type='solid', fgColor=bg)
    cell.alignment = ctr
    cell.border    = bdr

# 列宽
for col, w in zip('ABCDEFGH', [44, 10, 8, 8, 8, 10, 8, 12]):
    ws.column_dimensions[col].width = w

# 表头
headers = ['Item_Cook 文件名', '哈希匹配图', '哈希行', 'CV匹配图', 'CV行', 'CV得分', '两者一致', '置信度']
for ci, h_text in enumerate(headers, 1):
    hdr(ws.cell(1, ci), h_text)
ws.row_dimensions[1].height = 22
ws.freeze_panes = 'A2'

fill_hi  = PatternFill(fill_type='solid', fgColor='C6EFCE')
fill_mid = PatternFill(fill_type='solid', fgColor='FFEB9C')
fill_lo  = PatternFill(fill_type='solid', fgColor='FFC7CE')

for r in results:
    agree_str = '✓ 一致' if r['agree'] else '✗ 不一致'
    
    # 置信度判断
    if r['agree'] and r['cv_score'] >= 0.6:
        conf = '高'
        fill = fill_hi
    elif r['agree'] or r['cv_score'] >= 0.5:
        conf = '中'
        fill = fill_mid
    else:
        conf = '低'
        fill = fill_lo
    
    row_data = [
        r['filename'],
        f"{r['img_idx']}.jpg",
        r['row'],
        f"{r['cv_idx']}.jpg",
        r['cv_row'],
        r['cv_score'],
        agree_str,
        conf,
    ]
    ws.append(row_data)
    rn = ws.max_row
    for ci, al in zip(range(1, 9), [lft, ctr, ctr, ctr, ctr, ctr, ctr, ctr]):
        cell = ws.cell(rn, ci)
        cell.fill      = fill
        cell.border    = bdr
        cell.alignment = al

wb.save(xlsx_path)
print(f"Excel 已保存: {xlsx_path}")
print(f"\n调试图片保存在: {DEBUG_DIR}")
print("完成！")
