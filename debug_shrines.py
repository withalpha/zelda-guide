import re

filename = r'c:\Users\黄志成\Desktop\VIBE CODING\我的游戏网页\shrine-unlock.html'
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

sd_match = re.search(r'// 神庙数据\s+var SD = \[(.*?)\];', content, re.DOTALL)
sd_raw = sd_match.group(1)

def decode_unicode(s):
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)

sd_decoded = decode_unicode(sd_raw)

# Count all opening braces that start entries
all_entries = re.findall(r'\{cn:', sd_decoded)
print(f"Total {{cn: occurrences: {len(all_entries)}")

# The strict regex
strict_re = re.compile(
    r"\{cn:'([^']*?)',\s*en:'([^']*?)',\s*gx:(-?\d+),\s*gy:(-?\d+),\s*gz:(-?\d+),\s*"
    r"region:'([^']*?)',\s*type:'([^']*?)',\s*note:'([^']*?)'\s*\}"
)
matched = strict_re.findall(sd_decoded)
print(f"Matched by strict regex: {len(matched)}")

# Find entries that don't match - compare positions
all_entry_positions = [m.start() for m in re.finditer(r'\{cn:', sd_decoded)]
matched_positions = set(m.start() for m in strict_re.finditer(sd_decoded))
print(f"All positions: {len(all_entry_positions)}, Matched: {len(matched_positions)}")

# Find unmatched
unmatched_pos = [p for p in all_entry_positions if p not in matched_positions]
print(f"Unmatched count: {len(unmatched_pos)}")
for pos in unmatched_pos:
    snippet = sd_decoded[pos:pos+300]
    print(f"\n  POS {pos}:")
    print(f"  {repr(snippet)}")
