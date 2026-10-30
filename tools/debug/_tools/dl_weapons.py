"""
TotK 武器图片批量下载工具
从 zelda.wiki.gallery (MediaWiki CDN) 下载所有武器图标，保存到 images/weapons/
运行前确保已安装 curl_cffi：pip install curl_cffi
若未安装，自动回退到 urllib（部分图片可能因防盗链失败）
"""
import hashlib, os, time

img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "weapons")
os.makedirs(img_dir, exist_ok=True)

def wiki_img_url(filename, size=256):
    """根据 MediaWiki 规则计算 zelda.wiki.gallery 图片 URL"""
    h = hashlib.md5(filename.encode()).hexdigest()
    d1, d2 = h[0], h[:2]
    enc = filename.replace("'", "%27").replace(" ", "_")
    return f"https://zelda.wiki.gallery/images/thumb/{d1}/{d2}/{enc}/{size}px-{enc}"

# (本地文件名, wiki 图片文件名)
WEAPONS = [
    # ── 传说 / 英杰武器 ──────────────────────────────────────
    ("master_sword.png",          "TotK_Master_Sword_Icon.png"),
    ("great_eagle_bow.png",       "TotK_Great_Eagle_Bow_Icon.png"),
    ("lightscale_trident.png",    "TotK_Lightscale_Trident_Icon.png"),
    ("boulder_breaker.png",       "TotK_Boulder_Breaker_Icon.png"),
    ("scimitar_seven.png",        "TotK_Scimitar_of_the_Seven_Icon.png"),
    ("daybreaker.png",            "TotK_Daybreaker_Icon.png"),
    ("hylian_shield.png",         "TotK_Hylian_Shield_Icon.png"),
    ("gloom_sword.png",           "TotK_Gloom_Sword_Icon.png"),
    ("gloom_club.png",            "TotK_Gloom_Club_Icon.png"),
    ("gloom_spear.png",           "TotK_Gloom_Spear_Icon.png"),
    # ── 单手剑 ───────────────────────────────────────────────
    ("travelers_sword.png",       "TotK_Traveler's_Sword_Icon.png"),
    ("soldiers_broadsword.png",   "TotK_Soldier's_Broadsword_Icon.png"),
    ("knights_broadsword.png",    "TotK_Knight's_Broadsword_Icon.png"),
    ("royal_broadsword.png",      "TotK_Royal_Broadsword_Icon.png"),
    ("royal_guard_sword.png",     "TotK_Royal_Guard's_Sword_Icon.png"),
    ("zora_sword.png",            "TotK_Zora_Sword_Icon.png"),
    ("gerudo_scimitar.png",       "TotK_Gerudo_Scimitar_Icon.png"),
    ("flameblade.png",            "TotK_Flameblade_Icon.png"),
    ("frostblade.png",            "TotK_Frostblade_Icon.png"),
    ("thunderblade.png",          "TotK_Thunderblade_Icon.png"),
    ("lizal_boomerang.png",       "TotK_Lizal_Boomerang_Icon.png"),
    ("bokoblin_arm.png",          "TotK_Bokoblin_Arm_Icon.png"),
    ("lizalfos_arm.png",          "TotK_Lizalfos_Arm_Icon.png"),
    ("moblin_arm.png",            "TotK_Moblin_Arm_Icon.png"),
    ("lynel_sword.png",           "TotK_Lynel_Sword_Icon.png"),
    ("blue_lynel_sword.png",      "TotK_Blue-Maned_Lynel_Sword_Icon.png"),
    ("white_lynel_sword.png",     "TotK_White-Maned_Lynel_Sword_Icon.png"),
    ("savage_lynel_sword.png",    "TotK_Savage_Lynel_Sword_Icon.png"),
    ("zonaite_sword.png",         "TotK_Zonaite_Sword_Icon.png"),
    # ── 双手武器 ─────────────────────────────────────────────
    ("travelers_claymore.png",    "TotK_Traveler's_Claymore_Icon.png"),
    ("soldiers_claymore.png",     "TotK_Soldier's_Claymore_Icon.png"),
    ("knights_claymore.png",      "TotK_Knight's_Claymore_Icon.png"),
    ("royal_claymore.png",        "TotK_Royal_Claymore_Icon.png"),
    ("royal_guard_claymore.png",  "TotK_Royal_Guard's_Claymore_Icon.png"),
    ("lynel_crusher.png",         "TotK_Lynel_Crusher_Icon.png"),
    ("blue_lynel_crusher.png",    "TotK_Blue-Maned_Lynel_Crusher_Icon.png"),
    ("white_lynel_crusher.png",   "TotK_White-Maned_Lynel_Crusher_Icon.png"),
    ("savage_lynel_crusher.png",  "TotK_Savage_Lynel_Crusher_Icon.png"),
    ("zonaite_claymore.png",      "TotK_Zonaite_Claymore_Icon.png"),
    # ── 长柄武器 ─────────────────────────────────────────────
    ("travelers_spear.png",       "TotK_Traveler's_Spear_Icon.png"),
    ("soldiers_spear.png",        "TotK_Soldier's_Spear_Icon.png"),
    ("knights_halberd.png",       "TotK_Knight's_Halberd_Icon.png"),
    ("royal_halberd.png",         "TotK_Royal_Halberd_Icon.png"),
    ("royal_guard_spear.png",     "TotK_Royal_Guard's_Spear_Icon.png"),
    ("zora_spear.png",            "TotK_Zora_Spear_Icon.png"),
    ("lynel_spear.png",           "TotK_Lynel_Spear_Icon.png"),
    ("blue_lynel_spear.png",      "TotK_Blue-Maned_Lynel_Spear_Icon.png"),
    ("white_lynel_spear.png",     "TotK_White-Maned_Lynel_Spear_Icon.png"),
    ("savage_lynel_spear.png",    "TotK_Savage_Lynel_Spear_Icon.png"),
    ("zonaite_spear.png",         "TotK_Zonaite_Spear_Icon.png"),
    # ── 弓箭 ─────────────────────────────────────────────────
    ("travelers_bow.png",         "TotK_Traveler's_Bow_Icon.png"),
    ("soldiers_bow.png",          "TotK_Soldier's_Bow_Icon.png"),
    ("knights_bow.png",           "TotK_Knight's_Bow_Icon.png"),
    ("royal_bow.png",             "TotK_Royal_Bow_Icon.png"),
    ("royal_guard_bow.png",       "TotK_Royal_Guard's_Bow_Icon.png"),
    ("rito_bow.png",              "TotK_Rito_Bow_Icon.png"),
    ("zora_bow.png",              "TotK_Zora_Bow_Icon.png"),
    ("lynel_bow.png",             "TotK_Lynel_Bow_Icon.png"),
    ("blue_lynel_bow.png",        "TotK_Blue-Maned_Lynel_Bow_Icon.png"),
    ("white_lynel_bow.png",       "TotK_White-Maned_Lynel_Bow_Icon.png"),
    ("savage_lynel_bow.png",      "TotK_Savage_Lynel_Bow_Icon.png"),
    ("gerudo_bow.png",            "TotK_Gerudo_Bow_Icon.png"),
    ("ancient_bow.png",           "TotK_Ancient_Bow_Icon.png"),
    ("zonaite_bow.png",           "TotK_Zonaite_Bow_Icon.png"),
    # ── 盾牌 ─────────────────────────────────────────────────
    ("travelers_shield.png",      "TotK_Traveler's_Shield_Icon.png"),
    ("soldiers_shield.png",       "TotK_Soldier's_Shield_Icon.png"),
    ("knights_shield.png",        "TotK_Knight's_Shield_Icon.png"),
    ("royal_shield.png",          "TotK_Royal_Shield_Icon.png"),
    ("royal_guard_shield.png",    "TotK_Royal_Guard's_Shield_Icon.png"),
    ("lynel_shield.png",          "TotK_Lynel_Shield_Icon.png"),
    ("blue_lynel_shield.png",     "TotK_Blue-Maned_Lynel_Shield_Icon.png"),
    ("white_lynel_shield.png",    "TotK_White-Maned_Lynel_Shield_Icon.png"),
    ("savage_lynel_shield.png",   "TotK_Savage_Lynel_Shield_Icon.png"),
    ("zora_shield.png",           "TotK_Zora_Shield_Icon.png"),
]

# ── 打印所有 URL（方便调试）──────────────────────────────────
print("=" * 70)
print("URL 映射表（可用于 HTML 中的在线图片备用链接）")
print("=" * 70)
for local, wiki in WEAPONS:
    url = wiki_img_url(wiki)
    print(f'  "{local}": "{url}",')
print()

# ── 初始化 HTTP 客户端 ────────────────────────────────────────
try:
    from curl_cffi import requests as cf_requests
    _session = cf_requests.Session(impersonate="chrome120")
    def _get(url):
        return _session.get(url, headers={
            "Referer":  "https://zeldawiki.wiki/",
            "Accept":   "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        }, timeout=25)
    print("后端: curl_cffi（浏览器伪装模式）")
except ImportError:
    import urllib.request, urllib.error
    class _R:
        def __init__(self, data, code): self.content = data; self.status_code = code
    def _get(url):
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer":    "https://zeldawiki.wiki/",
            "Accept":     "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        })
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return _R(r.read(), r.status)
        except urllib.error.HTTPError as e:
            return _R(b"", e.code)
    print("后端: urllib（未安装 curl_cffi，部分图片可能失败）")
    print("建议安装: pip install curl_cffi\n")

print(f"保存目录: {img_dir}\n")
print("-" * 50)

ok = fail = skip = 0
for local, wiki in WEAPONS:
    out = os.path.join(img_dir, local)
    if os.path.exists(out) and os.path.getsize(out) > 500:
        print(f"  ⊘ 跳过  {local}")
        skip += 1
        ok += 1
        continue
    url = wiki_img_url(wiki)
    print(f"  ↓ {wiki}")
    try:
        r = _get(url)
        if r.status_code == 200 and len(r.content) > 500:
            with open(out, "wb") as f:
                f.write(r.content)
            print(f"    ✓ {local}  ({len(r.content):,} 字节)")
            ok += 1
        else:
            print(f"    ✗ HTTP {r.status_code}  {len(r.content)} 字节  → {local}")
            fail += 1
    except Exception as e:
        print(f"    ✗ 错误: {e}  → {local}")
        fail += 1
    time.sleep(0.45)

print(f"\n{'═' * 50}")
print(f"✓ 成功: {ok}（含 {skip} 跳过）   ✗ 失败: {fail}   合计: {ok+fail}")
print(f"图片目录: {img_dir}")
