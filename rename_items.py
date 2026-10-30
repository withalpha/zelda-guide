import os, shutil

items_dir = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\images\items'

rename_map = {
    'image2.png': 'gerudo-sword.png',
    'image3.png': 'gerudo-shield.png',
    'image4.png': 'diamond.png',
    'image5.png': 'flint.png',
    'image6.png': 'silver-lynel-horn.png',
}

for old_name, new_name in rename_map.items():
    old_path = os.path.join(items_dir, old_name)
    new_path = os.path.join(items_dir, new_name)
    if os.path.exists(old_path):
        shutil.copy2(old_path, new_path)
        print(f'已复制: {old_name} -> {new_name}')
    else:
        print(f'文件不存在: {old_path}')

print('\n当前 images/items 目录内容:')
for f in sorted(os.listdir(items_dir)):
    print(f'  {f}')
