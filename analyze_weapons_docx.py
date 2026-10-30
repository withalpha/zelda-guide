import zipfile, os
from lxml import etree

docx_path = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\doc\《王国之泪》无可争议的终极武器.docx'

with zipfile.ZipFile(docx_path, 'r') as z:
    doc_xml = z.read('word/document.xml')
    rels_xml = z.read('word/_rels/document.xml.rels')

rels_root = etree.fromstring(rels_xml)
rid_map = {}
for rel in rels_root:
    rid = rel.get('Id')
    target = rel.get('Target', '')
    if 'media/' in target:
        rid_map[rid] = os.path.basename(target)

doc_root = etree.fromstring(doc_xml)
ns_w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ns_r = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
ns_a = 'http://schemas.openxmlformats.org/drawingml/2006/main'

# 查找所有表格
tables = doc_root.findall(f'.//{{{ns_w}}}tbl')
print(f'共找到 {len(tables)} 个表格')
for ti, tbl in enumerate(tables):
    rows = tbl.findall(f'{{{ns_w}}}tr')
    for ri, row in enumerate(rows):
        cells = row.findall(f'{{{ns_w}}}tc')
        for ci, cell in enumerate(cells):
            # 获取单元格文字
            texts = cell.findall(f'.//{{{ns_w}}}t')
            cell_text = ''.join(t.text or '' for t in texts).strip()
            # 获取单元格图片
            blips = cell.findall(f'.//{{{ns_a}}}blip')
            for blip in blips:
                rid = blip.get(f'{{{ns_r}}}embed')
                fname = rid_map.get(rid, '未知')
                print(f'表格{ti} 行{ri} 列{ci}: 图片={fname}, 文字前60字符="{cell_text[:60]}"')

# 也打印所有rid_map
print('\n--- 全部媒体文件 ---')
for rid, fname in sorted(rid_map.items()):
    print(f'{rid}: {fname}')
