"""
关键改进：
1. 分析参考图图标的实际背景颜色（黄褐色，非白色）
2. 将 Item_Cook 图标合成到相同背景色上
3. 再做像素比对
同时：用模板匹配（在参考图上滑动搜索）找到最佳位置
"""
import os, cv2, json, re
import numpy as np
from PIL import Image
import easyocr

BASE      = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页'
ITEMS_DIR = os.path.join(BASE, 'Items')
COOK_DIR  = os.path.join(BASE, 'images', 'cooking')

ICON_X0, ICON_X1 = 39, 109
NAME_X0, NAME_X1 = 111, 202
ROW_START, ROW_H = 29, 66
ICON_W = ICON_X1 - ICON_X0   # 70
ICON_H = ROW_H - 2            # 64

# ── Step 1: 分析参考图背景色 ─────────────────────────────────────────────────
print("=== 分析参考图背景色 ===")
img1 = Image.open(os.path.join(COOK_DIR, '1.jpg')).convert('RGB')
arr1 = np.array(img1)

# 取多个图标的四角像素（背景区域）
bg_samples = []
for r in range(10):
    y0 = ROW_START + r * ROW_H
    icon = arr1[y0+1:y0+ROW_H-1, ICON_X0:ICON_X1]
    # 取四角3x3区域
    bg_samples.extend(icon[:3, :3].reshape(-1,3).tolist())
    bg_samples.extend(icon[:3, -3:].reshape(-1,3).tolist())
    bg_samples.extend(icon[-3:, :3].reshape(-1,3).tolist())
    bg_samples.extend(icon[-3:, -3:].reshape(-1,3).tolist())

bg_color = np.array(bg_samples).mean(axis=0)
print(f"  参考图图标背景色 (RGB): {bg_color.round(1)}")
BG_COLOR = tuple(bg_color.round().astype(int).tolist())

# ── Step 2: OCR 读取名称 ─────────────────────────────────────────────────────
print("\n=== OCR 读取名称列 ===")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)

ref_cells = []
for img_idx in range(1, 6):
    pil = Image.open(os.path.join(COOK_DIR, f'{img_idx}.jpg')).convert('RGB')
    H   = pil.height
    row = 0; y = ROW_START
    while y + ROW_H <= H:
        icon_pil = pil.crop((ICON_X0, y+1, ICON_X1, y+ROW_H-1))
        name_arr = np.array(pil.crop((NAME_X0, y+1, NAME_X1, y+ROW_H-1)))
        ocr_res  = reader.readtext(name_arr, detail=0, paragraph=True)
        raw      = ' '.join(ocr_res).strip()
        chinese  = re.findall(r'[\u4e00-\u9fff]+', raw)
        ocr_name = ''.join(chinese) if chinese else raw
        ref_cells.append({
            'img_idx': img_idx, 'row': row, 'y0': y,
            'icon':    np.array(icon_pil),
            'name':    ocr_name,
        })
        print(f"  {img_idx}.jpg 行{row:02d}: {ocr_name}")
        row += 1; y += ROW_H

print(f"\n共 {len(ref_cells)} 个参考格子")

# ── Step 3: 加载 Item_Cook，合成到参考图背景色 ───────────────────────────────
print(f"\n=== 加载 Item_Cook（合成到背景色 {BG_COLOR}）===")
item_files = sorted([
    f for f in os.listdir(ITEMS_DIR)
    if f.startswith('Item_Cook') and f.endswith('.png') and f != 'Item_CookSet.png'
])

items = []
for fname in item_files:
    pil  = Image.open(os.path.join(ITEMS_DIR, fname)).convert('RGBA')
    # 合成到参考图背景色
    bg   = Image.new('RGB', pil.size, BG_COLOR)
    bg.paste(pil, mask=pil.split()[3])
    # 缩放到参考图图标尺寸
    icon = np.array(bg.resize((ICON_W, ICON_H), Image.LANCZOS))
    items.append({'filename': fname, 'img_key': fname.replace('.png',''), 'icon': icon})

print(f"共 {len(items)} 个")

# ── Step 4: 相似度函数 ───────────────────────────────────────────────────────
def sim(a, b):
    af, bf = a.astype(np.float32), b.astype(np.float32)
    # NCC
    ag = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY).astype(np.float32)
    bg_ = cv2.cvtColor(b, cv2.COLOR_RGB2GRAY).astype(np.float32)
    an = (ag - ag.mean()) / (ag.std() + 1e-6)
    bn = (bg_ - bg_.mean()) / (bg_.std() + 1e-6)
    ncc = float(np.mean(an * bn))
    # HSV 直方图
    ah = cv2.calcHist([cv2.cvtColor(a,cv2.COLOR_RGB2HSV)],[0,1],None,[32,32],[0,180,0,256])
    bh = cv2.calcHist([cv2.cvtColor(b,cv2.COLOR_RGB2HSV)],[0,1],None,[32,32],[0,180,0,256])
    cv2.normalize(ah,ah); cv2.normalize(bh,bh)
    hist = 1.0 - cv2.compareHist(ah, bh, cv2.HISTCMP_BHATTACHARYYA)
    # MSE
    mse = 1.0 / (1.0 + float(np.mean((af-bf)**2)) / 300.0)
    # SSIM
    mu_a,mu_b = ag.mean(),bg_.mean()
    sa,sb = ag.std(),bg_.std()
    sab = float(np.mean((ag-mu_a)*(bg_-mu_b)))
    C1,C2 = 6.5025,58.5225
    ssim = ((2*mu_a*mu_b+C1)*(2*sab+C2))/((mu_a**2+mu_b**2+C1)*(sa**2+sb**2+C2))
    return ncc*0.30 + hist*0.40 + mse*0.15 + ssim*0.15, ncc, hist, mse, ssim

# ── Step 5: 逐一比对 ─────────────────────────────────────────────────────────
print(f"\n=== 像素级比对 ({len(items)}×{len(ref_cells)}={len(items)*len(ref_cells)} 对) ===")
results = []
for item in items:
    best = {'score': -999}
    for cell in ref_cells:
        s, ncc, hs, ms, ss = sim(item['icon'], cell['icon'])
        if s > best['score']:
            best = {'score':s,'ncc':ncc,'hist':hs,'mse':ms,'ssim':ss,
                    'img_idx':cell['img_idx'],'row':cell['row'],'name':cell['name']}
    results.append({'filename':item['filename'],'img_key':item['img_key'],**best})
    c = '✓' if best['score']>=0.55 else '△' if best['score']>=0.40 else '✗'
    print(f"  {c} {item['filename']:<42} → [{best['name']}]  "
          f"score={best['score']:.4f} ncc={best['ncc']:.3f} hist={best['hist']:.3f}  "
          f"({best['img_idx']}.jpg 行{best['row']})")

hi = sum(1 for r in results if r['score']>=0.55)
md = sum(1 for r in results if 0.40<=r['score']<0.55)
lo = sum(1 for r in results if r['score']<0.40)
print(f"\n统计: 高(≥0.55)={hi}  中(0.40-0.55)={md}  低(<0.40)={lo}")

# ── Step 6: 保存结果 ─────────────────────────────────────────────────────────
out = [{'img_key':r['img_key'],'name':r['name'],
        'ref_img':int(r['img_idx']),'ref_row':int(r['row']),
        'score':round(float(r['score']),4)} for r in results]
with open(os.path.join(BASE,'bg_match_result.json'),'w',encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

with open(os.path.join(BASE,'bg_match_result.txt'),'w',encoding='utf-8') as f:
    f.write("Item_Cook 像素级匹配（合成参考图背景色后比对）\n")
    f.write("="*78+"\n")
    f.write(f"{'文件名':<42} {'料理名称':<22} {'参考图':<10} {'得分'}\n")
    f.write("-"*78+"\n")
    for r in results:
        f.write(f"{r['filename']:<42} {r['name']:<22} "
                f"{r['img_idx']}.jpg行{r['row']:<4} {r['score']:.4f}\n")
    f.write(f"\n高(≥0.55):{hi}  中(0.40-0.55):{md}  低(<0.40):{lo}\n")

print(f"\n结果已保存: bg_match_result.json / .txt")
print("完成！")
