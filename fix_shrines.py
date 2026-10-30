import re

filename = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\shrine-unlock.html'

with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

def decode_unicode(s):
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)

S2T = {
    '庙':'廟','乌':'烏','萨':'薩','纳':'納','亚':'亞','玛':'瑪',
    '鲁':'魯','苏':'蘇','诺':'諾','马':'馬','维':'維','约':'約',
    '图':'圖','尔':'爾','库':'庫','欧':'歐','奥':'奧','贝':'貝',
    '达':'達','兹':'茲','齐':'齊','华':'華','汉':'漢',
    '东':'東','风':'風','龙':'龍','学':'學','来':'來',
}

def s2t(text):
    return ''.join(S2T.get(c, c) for c in text)

REGION = {
    '初始空岛': ('sky-island', 'rbadge-sky',     '初始之島'),
    '天空群岛': ('sky',        'rbadge-sky',     '天空群島'),
    '中央平原': ('central',    'rbadge-central', '中央海拉魯'),
    '山脊':     ('ridge',      'rbadge-central', '海拉魯山脊'),
    '奈克鲁达': ('necluda',    'rbadge-necluda', '奈克魯達'),
    '法罗尼':   ('faron',      'rbadge-faron',   '法隆草原'),
    '拉纳尤':   ('lanayru',    'rbadge-zora',    '拉聶爾'),
    '艾尔丁':   ('eldin',      'rbadge-goron',   '艾爾丁'),
    '阿卡拉':   ('akkala',     'rbadge-akkala',  '阿卡萊'),
    '赫布拉':   ('hebra',      'rbadge-rito',    '赫布拉'),
    '格鲁德':   ('gerudo',     'rbadge-gerudo',  '格魯德'),
    '大森林':   ('forest',     'rbadge-central', '海拉魯大森林'),
}

TYPE = {
    '谜题': ('tag-gold',   '謎題'),
    '祝福': ('tag-green',  '祝福'),
    '战斗': ('tag-red',    '戰鬥'),
    '教学': ('tag-blue',   '教學'),
    '试炼': ('tag-purple', '試煉'),
}

# Find SD array
sd_match = re.search(r'// 神庙数据\s+var SD = \[(.*?)\];', content, re.DOTALL)
if not sd_match:
    raise ValueError("SD array not found!")

sd_raw = sd_match.group(1)
sd_decoded = decode_unicode(sd_raw)

entry_re = re.compile(
    r"\{cn:'([^']*?)',\s*en:'([^']*?)',\s*gx:(-?\d+),\s*gy:(-?\d+),\s*gz:(-?\d+),\s*"
    r"region:'([^']*?)',\s*type:'([^']*?)',\s*note:'([^']*?)'\s*\}"
)
entries = entry_re.findall(sd_decoded)
print(f"Parsed {len(entries)} entries")

for i, e in enumerate(entries[:3]):
    print(f"  [{i}] {e[0]} / {e[1]} / region:{e[5]}")
for i, e in enumerate(entries[-3:]):
    print(f"  [{len(entries)-3+i}] {e[0]} / {e[1]} / region:{e[5]}")

# Build table HTML
table_lines = []
table_lines.append('  <div class="table-wrap">')
table_lines.append('    <table class="data-tbl">')
table_lines.append('      <thead><tr><th>#</th><th>神廟名稱</th><th>座標 (X, Y, Z)</th><th>地區</th><th>類型</th><th>✓</th></tr></thead>')
table_lines.append('      <tbody id="shrineTableBody">')

for idx, (cn, en, gx, gy, gz, region, stype, note) in enumerate(entries):
    cn_tw = s2t(cn)
    num = str(idx + 1).zfill(3)
    coord = f'({gx}, {gy}, {gz})'
    dr, rbadge_cls, region_tw = REGION.get(region, ('other', 'rbadge-central', s2t(region)))
    tag_cls, type_tw = TYPE.get(stype, ('tag-gold', stype))

    row = (
        f'<tr id="shrine-row-{idx}" data-region="{dr}" data-type="{stype}">'
        f'<td class="num-cell">{num}</td>'
        f'<td><span class="sname-cn">{cn_tw}</span>'
        f'<span class="sname-en">{en}</span></td>'
        f'<td><span class="coord">{coord}</span></td>'
        f'<td><span class="rbadge {rbadge_cls}">{region_tw}</span></td>'
        f'<td><span class="tag {tag_cls}">{type_tw}</span></td>'
        f'<td><button class="shrine-check" onclick="toggleShrineCheck(this)">✓</button></td>'
        f'</tr>'
    )
    table_lines.append(row)

table_lines.append('      </tbody>')
table_lines.append('    </table>')
table_lines.append('  </div>')

new_table = '\n'.join(table_lines)

# Replace old table
old_match = re.search(r'  <div class="table-wrap">.*?  </div>', content, re.DOTALL)
if old_match:
    content = content[:old_match.start()] + new_table + content[old_match.end():]
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"SUCCESS: Wrote {len(entries)} rows.")
else:
    print("ERROR: table-wrap div not found!")
