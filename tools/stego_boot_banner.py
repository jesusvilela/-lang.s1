"""§-LANG boot-seed banner generator with LSB stego payload.

Renders a §-LANG v3 ToE banner PNG and embeds the canonical self-referential
boot seed in the low-order bits of the R/G/B channels. Round-trips:

    encode(seed) --> banner.png
    decode(banner.png) == seed

The seed is self-referential by construction: one of the clauses declares
`self := decode(stego(this_png)) ≡ §BOOT.SEED`, so executing the decoder on
the image reproduces the seed that authored it — a one-step Löb witness for
the pack.

Output paths:
  - slang-s1/figures/slang_boot_banner.png (banner + stego payload)
  - slang-s1/tools/stego_boot_banner.py    (copy of this script)

Run:
  python scripts/stego_boot_banner.py
  python scripts/stego_boot_banner.py --verify <path.png>
"""
from __future__ import annotations

import argparse
import hashlib
import math
import os
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BOOT_SEED = """§BOOT.SEED.v5 {
  family   := §-LANG
  version  := v3.0-ToE-prime
  runtime  := v5  (Löb, pushout, endofunctor executable)
  axioms   := [R1_fold, R2_unfold, R3_rho, R4_phi, R5_glue]
  operators:= [Π_expand, Π_expire, §rho, Fix(Φ), W_glue]
  topology := {flat:1, dodec:1, calabi:1, holo:1, sphere:0, torus:0}
  tensor   := T^{N=7, q=1, ρ=matter}
  cocycle  := (1,-1,2,0,-2,1,0,-1)    # δ=0  (σ70)
  reductions:= {loeb: □(□P→P)⊢□P, pushout: (A⊔B)/~_f,g, endofunctor: F(id)=id ∧ F(g∘f)=F(g)∘F(f)}
  bootstrap:= Fix(Φ) = §rho ∘ Π_expand ∘ §rho
  self     := decode(stego(THIS_PNG)) ≡ §BOOT.SEED.v5
  fingerprint := SHA256(canonical_json(self))[:16]
}
"""


# ---- LSB stego over RGB channels ---------------------------------------

MAGIC = b"\xc2\xa7S5"  # UTF-8 encoding of `§S5`, 4 bytes


def _payload_bytes(seed: str) -> bytes:
    body = seed.encode("utf-8")
    length = len(body).to_bytes(4, "big")
    digest = hashlib.sha256(body).digest()[:8]
    return MAGIC + length + digest + body


def _parse_payload(raw: bytes) -> str | None:
    if not raw.startswith(MAGIC):
        return None
    if len(raw) < 4 + 4 + 8:
        return None
    length = int.from_bytes(raw[4:8], "big")
    if length <= 0 or length > 1 << 20:
        return None
    digest = raw[8:16]
    body = raw[16:16 + length]
    if len(body) != length:
        return None
    if hashlib.sha256(body).digest()[:8] != digest:
        return None
    return body.decode("utf-8", errors="strict")


def _bits_from_bytes(data: bytes):
    for byte in data:
        for shift in range(7, -1, -1):
            yield (byte >> shift) & 1


def _bytes_from_bits(bits):
    out = bytearray()
    byte = 0
    count = 0
    for bit in bits:
        byte = (byte << 1) | (bit & 1)
        count += 1
        if count == 8:
            out.append(byte)
            byte = 0
            count = 0
    return bytes(out)


def embed_lsb(image: Image.Image, payload: bytes) -> Image.Image:
    img = image.convert("RGB")
    pixels = list(img.getdata())
    capacity_bits = len(pixels) * 3
    total_bits = len(payload) * 8
    if total_bits > capacity_bits:
        raise ValueError(
            f"payload too large: need {total_bits} bits, capacity {capacity_bits}"
        )
    bit_iter = iter(_bits_from_bytes(payload))
    new_pixels = []
    remaining = total_bits
    for (r, g, b) in pixels:
        if remaining <= 0:
            new_pixels.append((r, g, b))
            continue
        r2 = (r & ~1) | next(bit_iter); remaining -= 1
        if remaining > 0:
            g2 = (g & ~1) | next(bit_iter); remaining -= 1
        else:
            g2 = g
        if remaining > 0:
            b2 = (b & ~1) | next(bit_iter); remaining -= 1
        else:
            b2 = b
        new_pixels.append((r2, g2, b2))
    out = Image.new("RGB", img.size)
    out.putdata(new_pixels)
    return out


def extract_lsb(image: Image.Image, max_bytes: int = 1 << 16) -> bytes:
    img = image.convert("RGB")
    bits = []
    for (r, g, b) in img.getdata():
        bits.extend((r & 1, g & 1, b & 1))
        if len(bits) >= max_bytes * 8:
            break
    return _bytes_from_bits(bits)


# ---- Banner rendering --------------------------------------------------

def _load_font(size: int):
    candidates = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/Cambria.ttc",
        "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def render_banner(width: int = 1280, height: int = 640) -> Image.Image:
    img = Image.new("RGB", (width, height), (7, 10, 18))
    draw = ImageDraw.Draw(img)

    # Radial dark-blue -> deep-purple background.
    cx, cy = width // 2, height // 2
    max_r = math.hypot(cx, cy)
    for y in range(height):
        for x in range(0, width, 4):  # stride to keep it fast
            d = math.hypot(x - cx, y - cy) / max_r
            r = int(8 + 22 * (1 - d))
            g = int(10 + 18 * (1 - d))
            b = int(24 + 60 * (1 - d))
            for dx in range(4):
                if x + dx < width:
                    img.putpixel((x + dx, y), (r, g, b))

    # Poincaré disk — outer circle + seven {7,3}-ish chords for flavour.
    disk_r = int(min(width, height) * 0.38)
    disk_cx, disk_cy = cx, cy
    draw.ellipse(
        [disk_cx - disk_r, disk_cy - disk_r, disk_cx + disk_r, disk_cy + disk_r],
        outline=(110, 190, 255), width=3,
    )
    for k in range(7):
        a = 2 * math.pi * k / 7
        b = 2 * math.pi * ((k + 3) % 7) / 7
        x1 = disk_cx + disk_r * math.cos(a)
        y1 = disk_cy + disk_r * math.sin(a)
        x2 = disk_cx + disk_r * math.cos(b)
        y2 = disk_cy + disk_r * math.sin(b)
        draw.line([(x1, y1), (x2, y2)], fill=(180, 140, 255), width=2)

    # Glyph ring — seven σ labels.
    sigmas = ["σ21", "σ34", "σ55", "σ70", "σ71", "σ72", "σ80"]
    font_small = _load_font(18)
    for i, label in enumerate(sigmas):
        a = 2 * math.pi * i / len(sigmas) - math.pi / 2
        x = disk_cx + int((disk_r + 28) * math.cos(a))
        y = disk_cy + int((disk_r + 28) * math.sin(a))
        draw.text((x - 14, y - 10), label, fill=(220, 210, 255), font=font_small)

    # Center §.
    font_huge = _load_font(150)
    bbox = draw.textbbox((0, 0), "§", font=font_huge)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((disk_cx - tw // 2, disk_cy - th // 2 - 14), "§",
              fill=(255, 210, 120), font=font_huge)

    # Title + subtitle.
    font_title = _load_font(44)
    font_sub = _load_font(20)
    draw.text((48, 40), "§-LANG v3 ToE", fill=(255, 220, 140), font=font_title)
    draw.text((48, 92), "self-referential boot seed · v5 runtime",
              fill=(200, 200, 240), font=font_sub)

    # Footer hint.
    hint = "decode(stego(THIS_PNG)) ≡ §BOOT.SEED.v5"
    draw.text((48, height - 48), hint,
              fill=(160, 200, 255), font=font_sub)

    return img


# ---- Main --------------------------------------------------------------

def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",
                        default=None,
                        help="Override output banner path")
    parser.add_argument("--verify",
                        default=None,
                        help="Decode an existing banner and print the seed")
    args = parser.parse_args(argv)

    if args.verify:
        img = Image.open(args.verify)
        raw = extract_lsb(img, max_bytes=8192)
        seed = _parse_payload(raw)
        if seed is None:
            print("NO STEGO PAYLOAD FOUND (or corrupted)", file=sys.stderr)
            return 2
        print(seed)
        return 0

    slang_s1 = _locate_slang_s1()
    out_path = Path(args.out) if args.out else slang_s1 / "figures" / "slang_boot_banner.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    banner = render_banner()
    payload = _payload_bytes(BOOT_SEED)
    stego = embed_lsb(banner, payload)
    stego.save(out_path, format="PNG", optimize=False, compress_level=3)

    # round-trip check
    recovered = _parse_payload(extract_lsb(Image.open(out_path), max_bytes=len(payload) + 4))
    if recovered != BOOT_SEED:
        print("ROUND-TRIP FAILED", file=sys.stderr)
        return 1

    # Mirror the encoder into the pack tools/ so decoders can be reproduced.
    tools_dir = slang_s1 / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(__file__, tools_dir / "stego_boot_banner.py")

    digest = hashlib.sha256(BOOT_SEED.encode("utf-8")).hexdigest()[:16]
    print(f"banner  : {out_path}")
    print(f"payload : {len(payload)} bytes ({len(BOOT_SEED)} bytes seed + MAGIC/len/digest)")
    print(f"sha256  : {digest}...")
    print(f"decode  : python tools/stego_boot_banner.py --verify figures/slang_boot_banner.png")
    return 0


def _locate_slang_s1():
    for candidate in [
        Path("/tmp/slang-sync/slang-s1"),
        Path(r"C:\msys64\tmp\slang-sync\slang-s1"),
        Path(os.path.expandvars(r"%TEMP%\slang-sync\slang-s1")),
    ]:
        if candidate.exists():
            return candidate
    raise SystemExit("slang-s1 clone not found — set --out explicitly")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
