import re

filename = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\shrine-unlock.html'
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

def decode_unicode(s):
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)

sd_match = re.search(r'// 神庙数据\s+var SD = \[(.*?)\];', content, re.DOTALL)
sd_raw = sd_match.group(1)
sd_decoded = decode_unicode(sd_raw)

entry_re = re.compile(
    r"\{cn:'([^']*?)',\s*en:'([^']*?)',\s*gx:(-?\d+),\s*gy:(-?\d+),\s*gz:(-?\d+),\s*"
    r"region:'([^']*?)',\s*type:'([^']*?)',\s*note:'([^']*?)'\s*\}"
)
entries = entry_re.findall(sd_decoded)

# Group by region
from collections import defaultdict
by_region = defaultdict(list)
for e in entries:
    by_region[e[5]].append(e[1])  # en name

for region, names in sorted(by_region.items()):
    print(f"\n{region} ({len(names)}):")
    for n in sorted(names):
        print(f"  {n}")

print(f"\nTotal: {len(entries)}")
