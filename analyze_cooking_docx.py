import zipfile, os, sys
from lxml import etree

# 直接写入文件，避免 Windows 控制台编码问题
_out = open(r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\cooking_docx_output.txt', 'w', encoding='utf-8')

def print(*args, **kwargs):
    kwargs.setdefault('file', _out)
    import builtins
    builtins.print(*args, **kwargs)

docx_path = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\doc\塞尔达传说王国之泪最值得合成的料理.docx'
img_out_dir = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\images\cooking_tips'
os.makedirs(img_out_dir, exist_ok=True)

# ── 1. 提取图片 ──────────────────────────────────────
with zipfile.ZipFile(docx_path, 'r') as z:
    rels_xml = z.read('word/_rels/document.xml.rels')
    rels_root = etree.fromstring(rels_xml)
    rid_map = {}
    for rel in rels_root:
        rid = rel.get('Id')
        target = rel.get('Target', '')
        if 'media/' in target:
            fname = os.path.basename(target)
            data = z.read('word/' + target.lstrip('../'))
            out_path = os.path.join(img_out_dir, fname)
            with open(out_path, 'wb') as f:
                f.write(data)
            rid_map[rid] = fname
            print(f'图片: {rid} -> {fname} ({len(data)} bytes)')

# ── 2. 解析段落顺序（含图片插入位置）──────────────────
with zipfile.ZipFile(docx_path, 'r') as z:
    doc_xml = z.read('word/document.xml')

doc_root = etree.fromstring(doc_xml)
ns_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ns_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

body = doc_root.find(f'{{{ns_w}}}body')
print('\n── 段落顺序 ──')
for i, elem in enumerate(body):
    tag = elem.tag.split('}')[-1]
    if tag == 'p':
        texts = elem.findall(f'.//{{{ns_w}}}t')
        text = ''.join(t.text or '' for t in texts).strip()
        style_elem = elem.find(f'{{{ns_w}}}pPr/{{{ns_w}}}pStyle')
        style = style_elem.get(f'{{{ns_w}}}val') if style_elem is not None else 'Normal'
        blips = elem.findall(f'.//{{{ns_a}}}blip')
        imgs = [rid_map.get(b.get(f'{{{ns_r}}}embed', ''), '?') for b in blips]
        if text or imgs:
            print(f'[{style}] {text[:100]}' + (f' [图片:{imgs}]' if imgs else ''))
    elif tag == 'tbl':
        rows = elem.findall(f'.//{{{ns_w}}}tr')
        print(f'[TABLE {len(rows)}行]')
        for ri, row in enumerate(rows):
            cells = row.findall(f'{{{ns_w}}}tc')
            row_data = []
            for cell in cells:
                texts = cell.findall(f'.//{{{ns_w}}}t')
                cell_text = ''.join(t.text or '' for t in texts).strip()
                blips = cell.findall(f'.//{{{ns_a}}}blip')
                imgs = [rid_map.get(b.get(f'{{{ns_r}}}embed', ''), '?') for b in blips]
                cell_info = cell_text[:40]
                if imgs:
                    cell_info += f'[图:{imgs}]'
                row_data.append(cell_info)
            print(f'  行{ri}: {" | ".join(row_data)}')

_out.close()
