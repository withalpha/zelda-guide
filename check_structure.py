import zipfile
from lxml import etree

docx_path = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\doc\塞尔达传说王国之泪最值得合成的料理.docx'
out_path = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\cooking_docx_full.txt'

with zipfile.ZipFile(docx_path, 'r') as z:
    rels_xml = z.read('word/_rels/document.xml.rels')
    rels_root = etree.fromstring(rels_xml)
    rid_map = {}
    for rel in rels_root:
        rid = rel.get('Id')
        target = rel.get('Target', '')
        if 'media/' in target:
            fname = target.split('/')[-1]
            rid_map[rid] = fname

with zipfile.ZipFile(docx_path, 'r') as z:
    doc_xml = z.read('word/document.xml')

doc_root = etree.fromstring(doc_xml)
ns_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ns_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

body = doc_root.find(f'{{{ns_w}}}body')

lines = []

# 顶层结构统计
top_tags = [elem.tag.split('}')[-1] for elem in body]
lines.append(f'顶层元素: {top_tags}')
lines.append('')

lines.append('── 完整段落顺序（无截断）──')
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
            lines.append(f'[{style}] {text}' + (f' [图片:{imgs}]' if imgs else ''))
    elif tag == 'tbl':
        rows = elem.findall(f'.//{{{ns_w}}}tr')
        lines.append(f'[TABLE {len(rows)}行]')
        for ri, row in enumerate(rows):
            cells = row.findall(f'{{{ns_w}}}tc')
            row_data = []
            for cell in cells:
                texts = cell.findall(f'.//{{{ns_w}}}t')
                cell_text = ''.join(t.text or '' for t in texts).strip()
                blips = cell.findall(f'.//{{{ns_a}}}blip')
                imgs = [rid_map.get(b.get(f'{{{ns_r}}}embed', ''), '?') for b in blips]
                cell_info = cell_text
                if imgs:
                    cell_info += f'[图:{imgs}]'
                row_data.append(cell_info)
            lines.append(f'  行{ri}: {" | ".join(row_data)}')
    else:
        lines.append(f'[{tag}] (跳过)')

with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('done')
