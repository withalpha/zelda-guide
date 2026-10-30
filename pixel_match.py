"""
像素级精确匹配：
- 从参考图(1-5.jpg)第2列逐行裁切料理图标(70x64px)
- 从参考图第3列逐行裁切料理名称区域，用OCR读取名称
- 将每个 Item_Cook*.png 与所有参考图标做像素相似度比对
- 方法：两张图都缩放到同一尺寸，计算 MSE + SSIM + 颜色直方图相关性
- 取综合得分最高的作为匹配结果
"""

import os, cv2, json
import numpy as np
from PIL import Image

BASE      = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页'
ITEMS_DIR = os.path.join(BASE, 'Items')
COOK_DIR  = os.path.join(BASE, 'images', 'cooking')
DEBUG_DIR = os.path.join(BASE, 'pixel_match_debug')
os.makedirs(DEBUG_DIR, exist_ok=True)

# ── 网格参数（像素分析确认）─────────────────────────────────────────────────
# 列分隔线: x = 0, 38, 110, 203, 308, 599
# 第2列(图标): x = 39~109  (70px)
# 第3列(名称): x = 111~202 (91px)
# 行: 第0数据行 y=29, 之后每行66px
ICON_X0   = 39
ICON_X1   = 109
NAME_X0   = 111
NAME_X1   = 202
ROW_START = 29
ROW_H     = 66
MATCH_SZ  = 64   # 统一缩放到此尺寸做比对

# ── Step 1: 裁切参考图所有图标 ───────────────────────────────────────────────
print("=== Step 1: 裁切参考图第2列图标 ===")
ref_icons = []  # {img_idx, row, icon_rgb_64, name_crop}

for img_idx in range(1, 6):
    path    = os.path.join(COOK_DIR, f'{img_idx}.jpg')
    pil_img = Image.open(path).convert('RGB')
    arr     = np.array(pil_img)
    H       = arr.shape[0]

    row = 0
    y   = ROW_START
    while y + ROW_H <= H:
        # 裁切图标区域（去1px边框避免分隔线干扰）
        icon_pil  = pil_img.crop((ICON_X0, y + 1, ICON_X1, y + ROW_H - 1))
        # 裁切名称区域
        name_pil  = pil_img.crop((NAME_X0, y + 1, NAME_X1, y + ROW_H - 1))

        # 缩放到统一尺寸
        icon_64   = np.array(icon_pil.resize((MATCH_SZ, MATCH_SZ), Image.LANCZOS))

        ref_icons.append({
            'img_idx':  img_idx,
            'row':      row,
            'y0':       y,
            'icon_64':  icon_64,       # numpy RGB (64,64,3)
            'icon_pil': icon_pil,
            'name_pil': name_pil,
        })
        row += 1
        y   += ROW_H

print(f"  共裁切 {len(ref_icons)} 个参考图标")

# ── Step 2: 用 EasyOCR 读取参考图名称列 ─────────────────────────────────────
print("\n=== Step 2: OCR 读取名称列 ===")
import easyocr
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)

for cell in ref_icons:
    name_arr = np.array(cell['name_pil'])
    results  = reader.readtext(name_arr, detail=0, paragraph=True)
    raw_text = ' '.join(results).strip()
    # 提取中文料理名（去掉心吣回复量等干扰）
    # 保留中文字符和常见标点
    import re
    chinese = re.findall(r'[\u4e00-\u9fff]+', raw_text)
    cell['ocr_raw']  = raw_text
    cell['ocr_name'] = ''.join(chinese) if chinese else raw_text
    print(f"  {cell['img_idx']}.jpg 行{cell['row']:02d}: {cell['ocr_name']}")

# ── Step 3: 加载所有 Item_Cook 图片 ─────────────────────────────────────────
print("\n=== Step 3: 加载 Item_Cook 图片 ===")
item_files = sorted([
    f for f in os.listdir(ITEMS_DIR)
    if f.startswith('Item_Cook') and f.endswith('.png') and f != 'Item_CookSet.png'
])
print(f"  共 {len(item_files)} 个")

items = []
for fname in item_files:
    path    = os.path.join(ITEMS_DIR, fname)
    pil_img = Image.open(path).convert('RGBA')

    # 去透明背景 → 白底 RGB
    bg = Image.new('RGB', pil_img.size, (255, 255, 255))
    bg.paste(pil_img, mask=pil_img.split()[3])

    # 缩放到 MATCH_SZ
    icon_64 = np.array(bg.resize((MATCH_SZ, MATCH_SZ), Image.LANCZOS))

    items.append({
        'filename': fname,
        'img_key':  fname.replace('.png', ''),
        'icon_64':  icon_64,
        'icon_pil': bg,
    })

# ── Step 4: 像素级比对函数 ───────────────────────────────────────────────────
def compute_similarity(img_a, img_b):
    """
    综合相似度：
    1. MSE（均方误差，越小越相似）→ 转为相似度
    2. 颜色直方图相关性（Bhattacharyya距离，越小越相似）
    3. 结构相似性（SSIM）
    4. 归一化互相关（NCC）
    """
    a = img_a.astype(np.float32)
    b = img_b.astype(np.float32)

    # 1. MSE → 相似度
    mse  = np.mean((a - b) ** 2)
    mse_sim = 1.0 / (1.0 + mse / 1000.0)

    # 2. HSV 颜色直方图 Bhattacharyya 距离
    a_hsv = cv2.cvtColor(img_a, cv2.COLOR_RGB2HSV)
    b_hsv = cv2.cvtColor(img_b, cv2.COLOR_RGB2HSV)
    hist_a = cv2.calcHist([a_hsv], [0,1,2], None, [16,8,8], [0,180,0,256,0,256])
    hist_b = cv2.calcHist([b_hsv], [0,1,2], None, [16,8,8], [0,180,0,256,0,256])
    cv2.normalize(hist_a, hist_a)
    cv2.normalize(hist_b, hist_b)
    bhat = cv2.compareHist(hist_a, hist_b, cv2.HISTCMP_BHATTACHARYYA)
    hist_sim = 1.0 - bhat  # 越大越相似

    # 3. 归一化互相关（NCC）
    a_gray = cv2.cvtColor(img_a, cv2.COLOR_RGB2GRAY).astype(np.float32)
    b_gray = cv2.cvtColor(img_b, cv2.COLOR_RGB2GRAY).astype(np.float32)
    a_norm = (a_gray - a_gray.mean()) / (a_gray.std() + 1e-6)
    b_norm = (b_gray - b_gray.mean()) / (b_gray.std() + 1e-6)
    ncc    = float(np.mean(a_norm * b_norm))
    ncc_sim = (ncc + 1.0) / 2.0  # 归一化到 [0,1]

    # 4. SSIM（简化版）
    mu_a, mu_b = a_gray.mean(), b_gray.mean()
    sig_a = a_gray.std(); sig_b = b_gray.std()
    sig_ab = np.mean((a_gray - mu_a) * (b_gray - mu_b))
    C1, C2 = 6.5025, 58.5225
    ssim = ((2*mu_a*mu_b + C1) * (2*sig_ab + C2)) / \
           ((mu_a**2 + mu_b**2 + C1) * (sig_a**2 + sig_b**2 + C2))
    ssim_sim = (ssim + 1.0) / 2.0

    # 综合得分（加权）
    score = mse_sim * 0.15 + hist_sim * 0.45 + ncc_sim * 0.25 + ssim_sim * 0.15
    return score, mse_sim, hist_sim, ncc_sim, ssim_sim


# ── Step 5: 逐一比对每个 Item_Cook 与所有参考图标 ────────────────────────────
print("\n=== Step 5: 像素级逐一比对 ===")
print(f"  共需比对: {len(items)} × {len(ref_icons)} = {len(items)*len(ref_icons)} 对")

results = []
for item in items:
    best_score = -1
    best_cell  = None
    best_detail = None

    for cell in ref_icons:
        score, mse_s, hist_s, ncc_s, ssim_s = compute_similarity(
            item['icon_64'], cell['icon_64']
        )
        if score > best_score:
            best_score  = score
            best_cell   = cell
            best_detail = (mse_s, hist_s, ncc_s, ssim_s)

    results.append({
        'filename':  item['filename'],
        'img_key':   item['img_key'],
        'img_idx':   best_cell['img_idx'],
        'row':       best_cell['row'],
        'ocr_name':  best_cell['ocr_name'],
        'ocr_raw':   best_cell['ocr_raw'],
        'score':     round(best_score, 4),
        'mse_s':     round(best_detail[0], 4),
        'hist_s':    round(best_detail[1], 4),
        'ncc_s':     round(best_detail[2], 4),
        'ssim_s':    round(best_detail[3], 4),
        'item_icon': item['icon_64'],
        'ref_icon':  best_cell['icon_64'],
    })

    conf = '✓高' if best_score >= 0.65 else ('△中' if best_score >= 0.50 else '✗低')
    print(f"  {conf} {item['filename']:<42} → [{best_cell['ocr_name']}]  "
          f"得分={best_score:.4f}  ({best_cell['img_idx']}.jpg 行{best_cell['row']})")

# ── Step 6: 保存对比图（每个匹配对并排显示）────────────────────────────────
print("\n=== Step 6: 保存对比图 ===")
for r in results:
    combined = Image.new('RGB', (MATCH_SZ*2 + 4, MATCH_SZ), (40, 40, 40))
    combined.paste(Image.fromarray(r['item_icon']), (0, 0))
    combined.paste(Image.fromarray(r['ref_icon']),  (MATCH_SZ + 4, 0))
    safe_name = r['filename'].replace('.png', '')
    combined.save(os.path.join(DEBUG_DIR, f'{safe_name}_vs_{r["ocr_name"]}.png'))

# ── Step 7: 统计 ─────────────────────────────────────────────────────────────
high   = sum(1 for r in results if r['score'] >= 0.65)
medium = sum(1 for r in results if 0.50 <= r['score'] < 0.65)
low    = sum(1 for r in results if r['score'] < 0.50)
print(f"\n匹配统计: 高置信={high}  中置信={medium}  低置信={low}  总={len(results)}")

# ── Step 8: 输出 JSON（供后续使用）─────────────────────────────────────────
out_json = []
for r in results:
    out_json.append({
        'img_key':  r['img_key'],
        'name':     r['ocr_name'],
        'ref_img':  r['img_idx'],
        'ref_row':  r['row'],
        'score':    r['score'],
    })

json_path = os.path.join(BASE, 'pixel_match_result.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(out_json, f, ensure_ascii=False, indent=2)
print(f"JSON 已保存: {json_path}")

# ── Step 9: 输出 TXT ─────────────────────────────────────────────────────────
txt_path = os.path.join(BASE, 'pixel_match_result.txt')
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write("像素级精确匹配结果 — Item_Cook 图片 vs 参考图第2列图标\n")
    f.write("=" * 80 + "\n")
    f.write(f"{'文件名':<42} {'料理名称':<20} {'参考图':<10} {'综合得分':<10} {'直方图':<8} {'NCC'}\n")
    f.write("-" * 80 + "\n")
    for r in results:
        f.write(f"{r['filename']:<42} {r['ocr_name']:<20} "
                f"{r['img_idx']}.jpg行{r['row']:<4} {r['score']:<10.4f} "
                f"{r['hist_s']:<8.4f} {r['ncc_s']:.4f}\n")
    f.write("-" * 80 + "\n")
    f.write(f"高置信(≥0.65):{high}  中置信(0.50-0.64):{medium}  低置信(<0.50):{low}\n")

print(f"TXT 已保存: {txt_path}")
print("\n完成！")
