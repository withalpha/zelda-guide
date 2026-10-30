from __future__ import annotations

import math
import io
import os
import struct
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "video"
CANVAS_W, CANVAS_H = 1280, 720
WIDTH, HEIGHT = 640, 360
FPS = 8
VOICE_WAV = OUT / "usazum_voice.wav"
BGM_MP3 = OUT / "Carefree.mp3"
BGM_WAV = OUT / "carefree_bg.wav"
MUSIC_WAV = OUT / "usazum_music.wav"
MIX_WAV = OUT / "usazum_mix.wav"
VIDEO_ONLY = OUT / "usazum_video_only.avi"
FINAL_AVI = OUT / "乌萨诸马神庙攻略_中文解说.avi"
SCRIPT_TXT = OUT / "乌萨诸马神庙攻略_中文解说稿.txt"


NARRATION = [
    ("开场", 0, 9, "这一期我们不照搬别人路线，直接用原创短攻略，带你在两分钟内搞定王国之泪的乌萨诸马神庙。"),
    ("定位", 9, 21, "先到萨托利山麓找神庙底座。这里不会直接给你完整神庙，而是先给你一个提示任务，核心目标就是把绿水晶找回来。"),
    ("追光", 21, 33, "和底座互动后，绿光会像导航线一样射向远处。顺着这道光走，你会抵达萨托利山麓洞窟，真正的攻略从这里开始。"),
    ("洞窟", 33, 47, "进洞先别冲太快，因为里面睡着一只西诺克斯。它脖子上挂着的发光水晶，就是我们要送回神庙的关键道具。"),
    ("打法", 47, 64, "喜欢正面解决问题的朋友，可以走速攻流。先用弓箭瞄它的独眼，带追踪素材会更稳。它倒地以后立刻贴身输出，通常很快就能把水晶打下来。"),
    ("潜行", 64, 82, "想省资源就走潜行流。穿潜行套，慢慢靠近它的手心，等它抬手或者翻身把你送上肚皮，拿到水晶后别恋战，立刻撤离洞窟。"),
    ("搬运", 82, 98, "拿到水晶以后，最稳的办法是用究极手一路拖回去。要是周围没有干扰，也可以直接抱着跑，绿光方向就是最省事的回程路线。"),
    ("完成", 98, 114, "等水晶回到底座，乌萨诸马神庙就会正式出现。里面是劳鲁的祝福，没有额外机关，顺手开宝箱，再领取祝福之光，这一趟就圆满收工。"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "simhei.ttf" if bold else "Deng.ttf"
    return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)


F_TITLE = font(40, True)
F_BIG = font(30, True)
F_MED = font(22, True)
F_BODY = font(18)
F_SMALL = font(15)


def run_powershell(script: str) -> None:
    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        check=True,
    )


def make_voice() -> None:
    text = " ".join(line[3] for line in NARRATION)
    escaped = text.replace("'", "''")
    wav = str(VOICE_WAV).replace("'", "''")
    ps = f"""
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice('Microsoft Huihui Desktop')
$s.Rate = 2
$s.Volume = 100
$s.SetOutputToWaveFile('{wav}')
$s.Speak('{escaped}')
$s.Dispose()
"""
    run_powershell(ps)


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


def read_wav_mono(path: Path, target_rate: int = 44100) -> list[int]:
    with wave.open(str(path), "rb") as w:
        channels = w.getnchannels()
        rate = w.getframerate()
        width = w.getsampwidth()
        frames = w.readframes(w.getnframes())
    if width != 2:
        raise ValueError("Only 16-bit WAV is supported")
    values = struct.unpack("<" + "h" * (len(frames) // 2), frames)
    if channels == 2:
        values = tuple((values[i] + values[i + 1]) // 2 for i in range(0, len(values), 2))
    if rate == target_rate:
        return list(values)
    out_len = int(len(values) * target_rate / rate)
    return [values[min(len(values) - 1, int(i * rate / target_rate))] for i in range(out_len)]


def ensure_bgm_wav() -> None:
    if not BGM_MP3.exists():
        return
    ffmpeg = None
    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg = None
    if not ffmpeg:
        return
    if BGM_WAV.exists() and BGM_WAV.stat().st_mtime >= BGM_MP3.stat().st_mtime:
        return
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-i",
            str(BGM_MP3),
            "-ac",
            "1",
            "-ar",
            "44100",
            str(BGM_WAV),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def write_mix(duration: float) -> None:
    rate = 44100
    voice = read_wav_mono(VOICE_WAV, rate)
    ensure_bgm_wav()
    bgm = read_wav_mono(BGM_WAV, rate) if BGM_WAV.exists() else []
    total = max(len(voice), int(duration * rate))
    mixed = []
    for i in range(total):
        t = i / rate
        v = voice[i] if i < len(voice) else 0
        b = 0
        if bgm:
            b = bgm[i % len(bgm)]
            fade = min(1.0, i / (rate * 1.2), (total - i) / (rate * 1.8))
            b = int(b * 0.18 * max(0.0, fade))
        sample = int(v * 0.95 + b)
        mixed.append(max(-32768, min(32767, sample)))
    tmp_mix = MIX_WAV.with_suffix(".tmp.wav")
    with wave.open(str(tmp_mix), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(struct.pack("<" + "h" * len(mixed), *mixed))
    os.replace(tmp_mix, MIX_WAV)


def fit_image(path: Path, box: tuple[int, int], radius: int = 24) -> Image.Image:
    img = Image.open(path).convert("RGBA")
    img.thumbnail(box, Image.LANCZOS)
    bg = Image.new("RGBA", box, (0, 0, 0, 0))
    bg.alpha_composite(img, ((box[0] - img.width) // 2, (box[1] - img.height) // 2))
    mask = Image.new("L", box, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, box[0], box[1]), radius=radius, fill=255)
    bg.putalpha(mask)
    return bg


SHRINE = fit_image(ROOT / "images/shrines/乌萨诸马神庙.png", (285, 205), 18)
HINOX = fit_image(ROOT / "images/bosses/西诺克斯.png", (292, 220), 18)
CRYSTAL = Image.open(ROOT / "Items/LightBall_Large.png").convert("RGBA")
ULTRAHAND = Image.open(ROOT / "Items/Obj_UltraHand.png").convert("RGBA")


def draw_text_box(draw: ImageDraw.ImageDraw, xy, text, title=None, width=560) -> None:
    x, y = xy
    lines = wrap(draw, text, F_BODY, width - 36)
    h = 28 + len(lines) * 34 + (44 if title else 0)
    draw.rounded_rectangle((x, y, x + width, y + h), radius=18, fill=(11, 18, 24, 218), outline=(0, 215, 170, 150), width=2)
    cy = y + 18
    if title:
        draw.text((x + 18, cy), title, font=F_MED, fill=(255, 218, 93))
        cy += 44
    for line in lines:
        draw.text((x + 18, cy), line, font=F_BODY, fill=(240, 248, 240))
        cy += 34


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    lines, cur = [], ""
    for ch in text:
        test = cur + ch
        if draw.textlength(test, font=fnt) <= max_width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def arrow(draw, start, end, color=(0, 255, 175), width=8) -> None:
    draw.line((start, end), fill=color, width=width)
    ang = math.atan2(end[1] - start[1], end[0] - start[0])
    pts = [
        end,
        (end[0] - 28 * math.cos(ang - 0.45), end[1] - 28 * math.sin(ang - 0.45)),
        (end[0] - 28 * math.cos(ang + 0.45), end[1] - 28 * math.sin(ang + 0.45)),
    ]
    draw.polygon(pts, fill=color)


def make_base_background() -> Image.Image:
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), (8, 18, 20))
    pix = img.load()
    for y in range(CANVAS_H):
        for x in range(CANVAS_W):
            v = int(18 + 16 * math.sin(x / 95) + 10 * math.cos(y / 80))
            pix[x, y] = (7, max(16, v + 12), max(20, v + 18))
    return img.convert("RGBA")


BASE_BG = make_base_background()


def background(t: float) -> Image.Image:
    img = BASE_BG.copy()
    overlay = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for i in range(18):
        x = (i * 173 + int(t * 22)) % (CANVAS_W + 100) - 50
        d.ellipse((x, 70 + (i * 37) % 520, x + 4, 74 + (i * 37) % 520), fill=(0, 230, 180, 90))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def scene_at(t: float):
    for item in NARRATION:
        if item[1] <= t < item[2]:
            return item
    return NARRATION[-1]


def draw_frame(t: float, duration: float) -> Image.Image:
    key, start, end, line = scene_at(t)
    local = max(0, min(1, (t - start) / max(0.1, end - start)))
    img = background(t)
    d = ImageDraw.Draw(img, "RGBA")

    d.rectangle((0, 0, WIDTH, 76), fill=(5, 10, 13, 210))
    d.text((42, 18), "乌萨诸马神庙攻略", font=F_BIG, fill=(255, 222, 104))
    d.text((430, 29), "王国之泪 · 原创短攻略", font=F_SMALL, fill=(170, 240, 220))
    d.rounded_rectangle((1030, 22, 1238, 54), radius=14, fill=(0, 188, 140, 60), outline=(0, 230, 180, 180))
    d.text((1052, 27), f"{int(t):02d}s / {int(duration):02d}s", font=F_SMALL, fill=(230, 255, 245))

    if key in {"开场", "定位", "追光"}:
        d.rounded_rectangle((70, 122, 690, 612), radius=24, fill=(18, 34, 29, 190), outline=(0, 220, 160, 120), width=2)
        d.text((100, 150), "路线总览", font=F_MED, fill=(255, 225, 90))
        points = [(200, 470), (340, 395), (510, 325), (610, 240)]
        d.line(points, fill=(78, 105, 82), width=34, joint="curve")
        d.line(points, fill=(143, 180, 115), width=18, joint="curve")
        d.ellipse((165, 435, 235, 505), fill=(0, 210, 160), outline=(255, 255, 255), width=3)
        d.text((150, 515), "神庙底座", font=F_SMALL, fill=(240, 250, 238))
        d.ellipse((575, 205, 645, 275), fill=(70, 42, 28), outline=(255, 230, 130), width=3)
        d.text((548, 285), "萨托利山麓洞窟", font=F_SMALL, fill=(240, 250, 238))
        arrow(d, (220, 450), (590, 252), width=7)
        pulse = int(18 + 9 * math.sin(t * 5))
        d.ellipse((200 - pulse, 470 - pulse, 200 + pulse, 470 + pulse), outline=(0, 255, 190, 180), width=4)
        img.alpha_composite(SHRINE, (780, 170))
        draw_text_box(d, (760, 500), line, title="路线重点：底座 -> 绿光 -> 洞窟", width=455)

    elif key in {"洞窟", "打法", "潜行"}:
        img.alpha_composite(HINOX, (75, 190))
        c = CRYSTAL.resize((110, 110))
        bob = int(math.sin(t * 5) * 9)
        img.alpha_composite(c, (370, 250 + bob))
        d.text((95, 145), "水晶挂在西诺克斯脖子上", font=F_MED, fill=(255, 230, 96))
        if key == "打法":
            d.rounded_rectangle((690, 145, 1190, 330), radius=18, fill=(35, 20, 15, 220), outline=(255, 120, 70, 160), width=2)
            d.text((720, 170), "方案 A：剑圣流", font=F_MED, fill=(255, 176, 95))
            d.text((720, 220), "1. 弓箭射独眼", font=F_BODY, fill=(255, 245, 230))
            d.text((720, 258), "2. 倒地后贴脸输出", font=F_BODY, fill=(255, 245, 230))
            d.text((720, 296), "3. 水晶和材料一起拿", font=F_BODY, fill=(255, 245, 230))
            arrow(d, (690, 430), (455, 290), color=(255, 90, 60), width=9)
        elif key == "潜行":
            d.rounded_rectangle((690, 145, 1190, 330), radius=18, fill=(20, 23, 45, 220), outline=(170, 145, 255, 170), width=2)
            d.text((720, 170), "方案 B：潜行流", font=F_MED, fill=(205, 190, 255))
            d.text((720, 220), "1. 穿潜行套靠近手心", font=F_BODY, fill=(245, 242, 255))
            d.text((720, 258), "2. 等它抬手上肚皮", font=F_BODY, fill=(245, 242, 255))
            d.text((720, 296), "3. 抱起水晶马上跑", font=F_BODY, fill=(245, 242, 255))
            for i in range(6):
                x = 650 + i * 58 + int(math.sin(t * 4 + i) * 6)
                d.ellipse((x, 455, x + 18, 473), fill=(170, 145, 255, 150))
        draw_text_box(d, (650, 455), line, title="原创思路：能打就速推，想稳就潜行", width=555)

    else:
        d.rounded_rectangle((72, 130, 610, 575), radius=24, fill=(18, 34, 29, 190), outline=(0, 220, 160, 120), width=2)
        d.text((105, 160), "搬水晶回底座", font=F_MED, fill=(255, 225, 90))
        sx, sy = 180, 455
        ex, ey = 520, 220
        cx = sx + (ex - sx) * local
        cy = sy + (ey - sy) * local
        arrow(d, (sx, sy), (ex, ey), width=8)
        cc = CRYSTAL.resize((92, 92))
        img.alpha_composite(cc, (int(cx - 46), int(cy - 46)))
        uh = ULTRAHAND.resize((66, 66))
        img.alpha_composite(uh, (int(cx + 30), int(cy + 20)))
        d.ellipse((490, 190, 550, 250), fill=(0, 210, 160), outline=(255, 255, 255), width=3)
        img.alpha_composite(SHRINE, (725, 135))
        d.rounded_rectangle((785, 468, 1160, 560), radius=20, fill=(201, 162, 39, 70), outline=(255, 225, 90, 160), width=2)
        d.text((820, 490), "奖励：宝箱 + 祝福之光", font=F_MED, fill=(255, 232, 132))
        draw_text_box(d, (95, 590), line, title="最后一步：拖回底座，进门领奖", width=1090)

    sub_lines = wrap(d, line, F_BODY, 1080)
    sub_h = 28 + len(sub_lines) * 32
    d.rounded_rectangle((82, 606 - sub_h, 1198, 662), radius=14, fill=(0, 0, 0, 178))
    yy = 620 - sub_h
    for s in sub_lines:
        d.text((110, yy), s, font=F_BODY, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        yy += 32

    progress = int((t / duration) * (CANVAS_W - 84))
    d.rounded_rectangle((42, 694, CANVAS_W - 42, 704), radius=5, fill=(255, 255, 255, 55))
    d.rounded_rectangle((42, 694, 42 + progress, 704), radius=5, fill=(0, 245, 180, 230))
    return img.convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def avi_list(kind: bytes, payload: bytes) -> bytes:
    return b"LIST" + struct.pack("<I", len(payload) + 4) + kind + payload


def avi_chunk(kind: bytes, payload: bytes) -> bytes:
    pad = b"\0" if len(payload) % 2 else b""
    return kind + struct.pack("<I", len(payload)) + payload + pad


def write_avi(frames: int, duration: float) -> None:
    with wave.open(str(MIX_WAV), "rb") as aw:
        audio_rate = aw.getframerate()
        audio_channels = aw.getnchannels()
        audio_width = aw.getsampwidth()
        audio_bytes = aw.readframes(aw.getnframes())
    if audio_channels != 1 or audio_width != 2:
        raise ValueError("Expected mono 16-bit PCM audio")

    frame_size = WIDTH * HEIGHT * 3
    samples_per_frame = audio_rate / FPS
    audio_chunks = []
    for n in range(frames):
        a0 = int(round(n * samples_per_frame)) * audio_width
        a1 = int(round((n + 1) * samples_per_frame)) * audio_width
        audio_chunks.append(audio_bytes[a0:a1])

    avih = avi_chunk(
        b"avih",
        struct.pack(
            "<IIIIIIIIIIIIII",
            int(1_000_000 / FPS),
            frame_size * FPS + audio_rate * audio_width,
            0,
            0x10,
            frames,
            0,
            2,
            frame_size,
            WIDTH,
            HEIGHT,
            0,
            0,
            0,
            0,
        ),
    )
    v_strh = avi_chunk(
        b"strh",
        b"vids"
        + b"MJPG"
        + struct.pack("<IIIIIIIIIIII", 0, 0, 0, 0, 1, FPS, 0, frames, frame_size, 0xFFFFFFFF, 0, 0)
        + struct.pack("<hhhh", 0, 0, WIDTH, HEIGHT),
    )
    v_strf = avi_chunk(b"strf", struct.pack("<IiiHHIIIIII", 40, WIDTH, HEIGHT, 1, 24, 1196444237, frame_size, 0, 0, 0, 0))
    a_strh = avi_chunk(
        b"strh",
        b"auds"
        + b"\0\0\0\0"
        + struct.pack("<IIIIIIIIIIII", 0, 0, 0, 0, audio_width, audio_rate * audio_width, 0, len(audio_bytes) // audio_width, audio_rate * audio_width, 0xFFFFFFFF, audio_width, 0)
        + struct.pack("<hhhh", 0, 0, 0, 0),
    )
    a_strf = avi_chunk(
        b"strf",
        struct.pack("<HHIIHHH", 1, audio_channels, audio_rate, audio_rate * audio_channels * audio_width, audio_channels * audio_width, audio_width * 8, 0),
    )
    hdrl = avi_list(b"hdrl", avih + avi_list(b"strl", v_strh + v_strf) + avi_list(b"strl", a_strh + a_strf))

    with open(VIDEO_ONLY, "wb") as f:
        def w(data: bytes):
            f.write(data)

        w(b"RIFF\0\0\0\0AVI ")
        w(hdrl)
        movi_start = f.tell()
        w(b"LIST\0\0\0\0movi")
        idx = []
        offset = 4
        for n in range(frames):
            t = n / FPS
            frame = draw_frame(t, duration).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            buf = io.BytesIO()
            frame.save(buf, format="JPEG", quality=84)
            data = buf.getvalue()
            pad = b"\0" if len(data) % 2 else b""
            w(b"00dc" + struct.pack("<I", len(data)) + data + pad)
            idx.append((b"00dc", 0x10, offset, len(data)))
            offset += 8 + len(data) + len(pad)
            audio = audio_chunks[n]
            if audio:
                pad = b"\0" if len(audio) % 2 else b""
                w(b"01wb" + struct.pack("<I", len(audio)) + audio + pad)
                idx.append((b"01wb", 0x10, offset, len(audio)))
                offset += 8 + len(audio) + len(pad)
        end_movi = f.tell()
        f.seek(movi_start + 4)
        f.write(struct.pack("<I", end_movi - movi_start - 8))
        f.seek(end_movi)
        w(b"idx1" + struct.pack("<I", len(idx) * 16))
        for item in idx:
            w(item[0] + struct.pack("<III", item[1], item[2], item[3]))
        end_file = f.tell()
        f.seek(4)
        f.write(struct.pack("<I", end_file - 8))
    if FINAL_AVI.exists():
        FINAL_AVI.unlink()
    VIDEO_ONLY.replace(FINAL_AVI)


def mux_with_powershell() -> None:
    # Windows Media Foundation is not guaranteed on every host. Keep the raw
    # AVI and WAV if muxing is unavailable; most players can open both files.
    pass


def main() -> None:
    OUT.mkdir(exist_ok=True)
    SCRIPT_TXT.write_text("\n".join(f"{a} [{b}-{c}s]\n{d}\n" for a, b, c, d in NARRATION), encoding="utf-8")
    make_voice()
    duration = max(wav_duration(VOICE_WAV) + 1.0, NARRATION[-1][2])
    write_mix(duration)
    frames = int(math.ceil(duration * FPS))
    write_avi(frames, duration)
    print(f"video={VIDEO_ONLY}")
    print(f"audio={MIX_WAV}")
    print(f"script={SCRIPT_TXT}")
    print(f"duration={duration:.2f}s frames={frames}")


if __name__ == "__main__":
    main()
