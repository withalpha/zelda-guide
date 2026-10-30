import sys
import os
import subprocess

# Check and install python-docx if needed
try:
    from docx import Document
except ImportError:
    print("Installing python-docx...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document

files = [
    r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\doc\《王国之泪》无可争议的终极武器.docx',
    r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\doc\塞尔达传说王国之泪最值得合成的料理.docx',
    r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\doc\塞尔达传说王国之泪究极套装推荐.docx',
]

for filepath in files:
    print("\n" + "="*80)
    print(f"文件名: {os.path.basename(filepath)}")
    print("="*80)
    
    if not os.path.exists(filepath):
        print(f"[错误] 文件不存在: {filepath}")
        continue
    
    try:
        doc = Document(filepath)
        for i, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if text:
                print(f"---PARAGRAPH---")
                print(text)
        print("\n[文件读取完毕]")
    except Exception as e:
        print(f"[错误] 读取失败: {e}")
