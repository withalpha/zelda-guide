import zipfile, os

docx_path = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\doc\《王国之泪》无可争议的终极武器.docx'
out_dir = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\images\items'
os.makedirs(out_dir, exist_ok=True)

with zipfile.ZipFile(docx_path, 'r') as z:
    all_files = z.namelist()
    print('zip 内所有条目（前30个）：')
    for entry in all_files[:30]:
        print(f'  {entry}')
    
    media_files = [f for f in all_files if 'media/' in f and not f.endswith('/')]
    print(f'\n找到 {len(media_files)} 个媒体文件：')
    for mf in media_files:
        fname = os.path.basename(mf)
        if not fname:
            print(f'  跳过空文件名：{mf}')
            continue
        data = z.read(mf)
        out_path = os.path.join(out_dir, fname)
        with open(out_path, 'wb') as f:
            f.write(data)
        print(f'  {fname}  ({len(data)} bytes) -> 已保存')

print('\nimages/items/ 目录内容：')
for f in sorted(os.listdir(out_dir)):
    size = os.path.getsize(os.path.join(out_dir, f))
    print(f'  {f}  ({size} bytes)')
