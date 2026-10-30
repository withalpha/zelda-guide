"""
分析 cooking/1-5.jpg 的网格布局，裁切每个料理格子并保存预览
"""
from PIL import Image
import os

base = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\images\cooking'
out_dir = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\grid_cells'
os.makedirs(out_dir, exist_ok=True)

for i in range(1, 6):
    img = Image.open(os.path.join(base, f'{i}.jpg'))
    w, h = img.size
    print(f"\n=== {i}.jpg: {w}x{h} ===")
    
    # 每行4列，估算行高
    cols = 4
    cell_w = w // cols
    # 估算行数
    # 先看看每行大概多高 - 取一个小样本行分析
    # 假设格子是正方形或接近正方形
    cell_h = cell_w  # 先假设正方形
    rows = h // cell_h
    print(f"  cols={cols}, cell_w={cell_w}, cell_h={cell_h}, estimated rows={rows}")
    print(f"  total cells estimate: {rows * cols}")
    
    # 裁切前几个格子看看
    for r in range(min(2, rows)):
        for c in range(cols):
            x0 = c * cell_w
            y0 = r * cell_h
            x1 = x0 + cell_w
            y1 = y0 + cell_h
            cell = img.crop((x0, y0, x1, y1))
            cell.save(os.path.join(out_dir, f'img{i}_r{r}_c{c}.png'))

print("\n前2行格子已保存到 grid_cells/")
