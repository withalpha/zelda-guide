from docx import Document
import os

files = [
    r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\doc\《王国之泪》无可争议的终极武器.docx',
    r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\doc\塞尔达传说王国之泪最值得合成的料理.docx',
    r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\doc\塞尔达传说王国之泪究极套装推荐.docx',
]

for f in files:
    print(f'\n\n========== {os.path.basename(f)} ==========')
    doc = Document(f)
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if text:
            style = para.style.name if para.style else ''
            print(f'[{style}] {text}')
