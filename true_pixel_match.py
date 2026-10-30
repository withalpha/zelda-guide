"""
真正的像素级比对：
- 参考图图标背景是白/米白色（非暗色UI）
- Item_Cook 是透明背景，合成白底后缩小到参考图尺寸
- 用多种相似度指标逐一比对，取最高分
"""
import os, cv2, json, re
import numpy as np
from PIL import Image
import easyocr

BASE      = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页'
ITEMS_DIR = os.path.join(BASE, 'Items')
COOK_DIR  = os.path.join(BASE, 'images', 'cooking')

# 网格参数
ICON_X0, ICON_X1 = 39, 109   # 第2列图标: 70px宽
NAME_X0, NAME_X1 = 111, 202  # 第3列名称
ROW_START, ROW_H = 29, 66
ICON_W = ICON_X1 - ICON_X0   # 70
ICON_H = ROW_H - 2            # 64

print("=== 裁切参考图第2列图标 + OCR名称 ===")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)

ref_cells = []
for img_idx in range(1, 6):
    pil = Image.open(os.path.join(COOK_DIR, f'{img_idx}.jpg')).convert('RGB')
    H   = pil.height
    row = 0
    y   = ROW_START
    while y + ROW_H <= H:
        # 裁切图标（原始尺寸，不缩放）
        icon_pil = pil.crop((ICON_X0, y+1, ICON_X1, y+ROW_H-1))
        icon_arr = np.array(icon_pil)   # (64, 70, 3)

        # OCR 名称
        name_arr = np.array(pil.crop((NAME_X0, y+1, NAME_X1, y+ROW_H-1)))
        ocr_res  = reader.readtext(name_arr, detail=0, paragraph=True)
        raw      = ' '.join(ocr_res).strip()
        chinese  = re.findall(r'[\u4e00-\u9fff]+', raw)
        ocr_name = ''.join(chinese) if chinese else raw

        ref_cells.append({
            'img_idx': img_idx, 'row': row, 'y0': y,
            'icon':    icon_arr,
            'name':    ocr_name,
        })
        print(f"  {img_idx}.jpg 行{row:02d}: {ocr_name}")
        row += 1; y += ROW_H

print(f"\n共 {len(ref_cells)} 个参考格子")

print("\n=== 加载 Item_Cook 图标（缩放到参考图尺寸）===")
item_files = sorted([
    f for f in os.listdir(ITEMS_DIR)
    if f.startswith('Item_Cook') and f.endswith('.png') and f != 'Item_CookSet.png'
])

items = []
for fname in item_files:
    pil = Image.open(os.path.join(ITEMS_DIR, fname)).convert('RGBA')
    # 白底合成
    bg = Image.new('RGB', pil.size, (255, 255, 255))
    bg.paste(pil, mask=pil.split()[3])
    # 缩放到参考图图标尺寸 (70x64)
    resized = bg.resize((ICON_W, ICON_H), Image.LANCZOS)
    items.append({
        'filename': fname,
        'img_key':  fname.replace('.png', ''),
        'icon':     np.array(resized),   # (64, 70, 3)
    })
print(f"共 {len(items)} 个 Item_Cook 图标")

# ── 相似度函数 ────────────────────────────────────────────────────────────────
def similarity(a, b):
    """a, b: numpy RGB arrays, 同尺寸"""
    af = a.astype(np.float32)
    bf = b.astype(np.float32)

    # 1. 归一化互相关 NCC（对亮度变化鲁棒）
    ag = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY).astype(np.float32)
    bg_ = cv2.cvtColor(b, cv2.COLOR_RGB2GRAY).astype(np.float32)
    ag_n = (ag - ag.mean()) / (ag.std() + 1e-6)
    bg_n = (bg_ - bg_.mean()) / (bg_.std() + 1e-6)
    ncc  = float(np.mean(ag_n * bg_n))

    # 2. HSV 直方图 Bhattacharyya（颜色分布）
    a_hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    b_hsv = cv2.cvtColor(b, cv2.COLOR_RGB2HSV)
    ha = cv2.calcHist([a_hsv],[0,1],None,[32,32],[0,180,0,256])
    hb = cv2.calcHist([b_hsv],[0,1],None,[32,32],[0,180,0,256])
    cv2.normalize(ha,ha); cv2.normalize(hb,hb)
    bhat = cv2.compareHist(ha, hb, cv2.HISTCMP_BHATTACHARYYA)
    hist_sim = 1.0 - bhat

    # 3. MSE（像素级差异）
    mse = float(np.mean((af - bf)**2))
    mse_sim = 1.0 / (1.0 + mse / 500.0)

    # 4. 结构相似性 SSIM（简化）
    mu_a, mu_b = ag.mean(), bg_.mean()
    sa, sb = ag.std(), bg_.std()
    sab = float(np.mean((ag - mu_a)*(bg_ - mu_b)))
    C1, C2 = 6.5025, 58.5225
    ssim = ((2*mu_a*mu_b+C1)*(2*sab+C2)) / ((mu_a**2+mu_b**2+C1)*(sa**2+sb**2+C2))

    # 综合（NCC 和直方图权重最高）
    score = ncc*0.30 + hist_sim*0.40 + mse_sim*0.15 + ssim*0.15
    return float(score), float(ncc), float(hist_sim), float(mse_sim), float(ssim)

print(f"\n=== 像素级逐一比对 ({len(items)}×{len(ref_cells)}={len(items)*len(ref_cells)} 对) ===")

results = []
for item in items:
    best = {'score': -999}
    for cell in ref_cells:
        s, ncc, hs, ms, ss = similarity(item['icon'], cell['icon'])
        if s > best['score']:
            best = {
                'score': s, 'ncc': ncc, 'hist': hs, 'mse': ms, 'ssim': ss,
                'img_idx': cell['img_idx'], 'row': cell['row'], 'name': cell['name']
            }
    results.append({
        'filename': item['filename'],
        'img_key':  item['img_key'],
        **best
    })
    conf = '✓' if best['score'] >= 0.5 else '△' if best['score'] >= 0.3 else '✗'
    print(f"  {conf} {item['filename']:<42} → [{best['name']}]  "
          f"score={best['score']:.4f} ncc={best['ncc']:.3f} hist={best['hist']:.3f}  "
          f"({best['img_idx']}.jpg 行{best['row']})")

# ── 统计 ──────────────────────────────────────────────────────────────────────
hi = sum(1 for r in results if r['score'] >= 0.5)
md = sum(1 for r in results if 0.3 <= r['score'] < 0.5)
lo = sum(1 for r in results if r['score'] < 0.3)
print(f"\n统计: 高(≥0.5)={hi}  中(0.3-0.5)={md}  低(<0.3)={lo}")

# ── 保存对比图 ────────────────────────────────────────────────────────────────
DEBUG = os.path.join(BASE, 'true_match_debug')
os.makedirs(DEBUG, exist_ok=True)

# 找到每个 Item_Cook 对应的参考图标，并排保存
ref_lookup = {(c['img_idx'], c['row']): c['icon'] for c in ref_cells}
for r in results:
    ref_icon = ref_lookup.get((r['img_idx'], r['row']))
    if ref_icon is None: continue
    item_icon = next(i['icon'] for i in items if i['filename'] == r['filename'])
    # 并排：item(70x64) | 2px分隔 | ref(70x64)，放大4倍
    combined = Image.new('RGB', (70*2+4, 64), (80,80,80))
    combined.paste(Image.fromarray(item_icon), (0,0))
    combined.paste(Image.fromarray(ref_icon),  (74,0))
    big = combined.resize((combined.width*4, combined.height*4), Image.NEAREST)
    safe = r['filename'].replace('.png','')
    big.save(os.path.join(DEBUG, f'{safe}__vs__{r["name"]}__{r["score"]:.3f}.png'))

# ── 输出 JSON ─────────────────────────────────────────────────────────────────
out = [{'img_key': r['img_key'], 'name': r['name'],
        'ref_img': int(r['img_idx']), 'ref_row': int(r['row']),
        'score': round(float(r['score']),4)}
       for r in results]
with open(os.path.join(BASE,'true_match_result.json'),'w',encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# ── 输出 TXT ──────────────────────────────────────────────────────────────────
with open(os.path.join(BASE,'true_match_result.txt'),'w',encoding='utf-8') as f:
    f.write("Item_Cook 像素级匹配结果（参考图第2列图标 vs Item_Cook 白底缩放）\n")
    f.write("="*78+"\n")
    f.write(f"{'文件名':<42} {'料理名称':<22} {'参考图':<10} {'得分'}\n")
    f.write("-"*78+"\n")
    for r in results:
        f.write(f"{r['filename']:<42} {r['name']:<22} "
                f"{r['img_idx']}.jpg行{r['row']:<4} {r['score']:.4f}\n")
    f.write("-"*78+"\n")
    f.write(f"高(≥0.5):{hi}  中(0.3-0.5):{md}  低(<0.3):{lo}\n")

print(f"\n结果已保存: true_match_result.json / .txt")
print(f"对比图已保存: {DEBUG}")
print("完成！")
