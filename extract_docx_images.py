import zipfile, os
from lxml import etree

docx_path = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\doc\《王国之泪》无可争议的终极武器.docx'

# 读取 word/document.xml 和 word/_rels/document.xml.rels
with zipfile.ZipFile(docx_path, 'r') as z:
    doc_xml = z.read('word/document.xml')
    rels_xml = z.read('word/_rels/document.xml.rels')

# 解析关系文件，建立 rId -> 文件名 映射
rels_root = etree.fromstring(rels_xml)
rid_map = {}
for rel in rels_root:
    rid = rel.get('Id')
    target = rel.get('Target', '')
    if 'media/' in target:
        rid_map[rid] = os.path.basename(target)
print('rId -> 图片文件名映射：')
for k, v in rid_map.items():
    print(f'  {k}: {v}')

# 解析 document.xml，找每个段落里的图片 rId 和段落文本
ns = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'a14': 'http://schemas.microsoft.com/office/drawing/2010/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
}

doc_root = etree.fromstring(doc_xml)
body = doc_root.find('.//w:body', ns)

print('\n段落扫描（含图片的段落）：')
for i, para in enumerate(body):
    # 获取段落文本
    texts = para.findall('.//w:t', ns)
    para_text = ''.join(t.text or '' for t in texts).strip()
    
    # 查找图片引用
    blips = para.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip')
    for blip in blips:
        rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        fname = rid_map.get(rid, '未知')
        print(f'  段落{i}: 图片={fname}, rId={rid}, 段落文字="{para_text[:80]}"')
    
    # 也查找 v:imagedata
    imgdata = para.findall('.//{urn:schemas-microsoft-com:vml}imagedata')
    for img in imgdata:
        rid = img.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        fname = rid_map.get(rid, '未知')
        print(f'  段落{i}[vml]: 图片={fname}, rId={rid}, 段落文字="{para_text[:80]}"')
