import zipfile, os
from lxml import etree

docx_path = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\doc\神庙挑战-乌萨诸马神庙.docx'
img_out_dir = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\images\shrine_tips'
os.makedirs(img_out_dir, exist_ok=True)

# 提取图片
with zipfile.ZipFile(docx_path, 'r') as z:
    rels_xml = z.read('word/_rels/document.xml.rels')
    rels_root = etree.fromstring(rels_xml)
    rid_map = {}
    for rel in rels_root:
        rid = rel.get('Id')
        target = rel.get('Target', '')
        if 'media/' in target:
            fname = os.path.basename(target)
            try:
                data = z.read('word/' + target.lstrip('../'))
            except:
                data = z.read(target)
            out_path = os.path.join(img_out_dir, fname)
            with open(out_path, 'wb') as f:
                f.write(data)
            rid_map[rid] = fname
            print(f'图片: {rid} -> {fname} ({len(data)} bytes)')

# 解析段落结构（含图片位置）
with zipfile.ZipFile(docx_path, 'r') as z:
    doc_xml = z.read('word/document.xml')
doc_root = etree.fromstring(doc_xml)
ns_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ns_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'
body = doc_root.find(f'{{{ns_w}}}body')

print('\n── 完整段落顺序 ──')
for i, elem in enumerate(body):
    tag = elem.tag.split('}')[-1]
    if tag == 'p':
        texts = elem.findall(f'.//{{{ns_w}}}t')
        text = ''.join(t.text or '' for t in texts).strip()
        style_elem = elem.find(f'{{{ns_w}}}pPr/{{{ns_w}}}pStyle')
        style = style_elem.get(f'{{{ns_w}}}val') if style_elem is not None else 'Normal'
        blips = elem.findall(f'.//{{{ns_a}}}blip')
        imgs = [rid_map.get(b.get(f'{{{ns_r}}}embed',''), '?') for b in blips]
        if text or imgs:
            img_str = f' [图片:{imgs}]' if imgs else ''
            print(f'[{style}] {text}{img_str}')
    elif tag == 'tbl':
        rows = elem.findall(f'.//{{{ns_w}}}tr')
        print(f'[TABLE {len(rows)}行]')
        for ri, row in enumerate(rows):
            cells = row.findall(f'{{{ns_w}}}tc')
            row_data = []
            for cell in cells:
                ctexts = cell.findall(f'.//{{{ns_w}}}t')
                ct = ''.join(t.text or '' for t in ctexts).strip()
                cblips = cell.findall(f'.//{{{ns_a}}}blip')
                cimgs = [rid_map.get(b.get(f'{{{ns_r}}}embed',''), '?') for b in cblips]
                info = ct[:50]
                if cimgs:
                    info += f'[图:{cimgs}]'
                row_data.append(info)
            print(f'  行{ri}: {" | ".join(row_data)}')
