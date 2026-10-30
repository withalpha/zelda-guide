import re

filename = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\shrine-unlock.html'

with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

def decode_unicode(s):
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)

# Find SD array
sd_match = re.search(r'// 神庙数据\s+var SD = \[(.*?)\n  \];', content, re.DOTALL)
sd_decoded = decode_unicode(sd_match.group(1))

# Count total {cn: entries
all_cn = re.findall(r"\{cn:'", sd_decoded)
print(f"Total {{cn: entries found: {len(all_cn)}")

# Try strict regex
strict_re = re.compile(
    r"\{cn:'([^']*)',en:'([^']*)',gx:(-?\d+),gy:(-?\d+),gz:(-?\d+),"
    r"region:'([^']*)',type:'([^']*)',note:'([^']*)'\}"
)
strict_matches = strict_re.findall(sd_decoded)
print(f"Strict regex matched: {len(strict_matches)}")

# Try flexible regex (note field can contain anything up to '}')
flex_re = re.compile(
    r"\{cn:'([^']*)',en:'([^']*)',gx:(-?\d+),gy:(-?\d+),gz:(-?\d+),"
    r"region:'([^']*)',type:'([^']*)',note:'(.*?)'\}"
)
flex_matches = flex_re.findall(sd_decoded)
print(f"Flexible regex matched: {len(flex_matches)}")

# Find which en names are missing by comparing
strict_en = {m[1] for m in strict_matches}
flex_en = {m[1] for m in flex_matches}
missing = flex_en - strict_en
print(f"\nMissing shrines:")
for m in flex_matches:
    if m[1] not in strict_en:
        print(f"  cn={m[0]}, en={m[1]}, note={repr(m[6])}")

# Also show raw text around the missing entries
for en in missing:
    idx = sd_decoded.find(f"en:'{en}'")
    if idx > 0:
        snippet = sd_decoded[idx-20:idx+150]
        print(f"\nRaw snippet for {en}:")
        print(repr(snippet))
