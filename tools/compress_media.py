#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nén ảnh lookbook (trang cổng) và video (trang shop) trước khi đưa web lên Vercel.

Chạy từ thư mục gốc dự án (cần: pip install pillow numpy imageio-ffmpeg):
    python tools/compress_media.py

Cách làm (ưu tiên giữ chất lượng):
  - File gốc được chuyển vào assets/_source/ (đã .gitignore, chỉ giữ trên máy).
  - Ảnh: PNG/JPG -> WebP chất lượng 94, giữ nguyên độ phân giải 1440px (đủ nét cho màn hình retina).
  - Video: mã hoá lại H.264 với CRF 20 (càng nhỏ càng đẹp; 18-23 là mức "gần như không thấy khác"),
    giữ nguyên 1080px và 30 fps, bỏ track âm thanh (video luôn tắt tiếng), +faststart để phát ngay khi đang tải.
  - In ra độ giống bản gốc: PSNR cho ảnh (trên 40 dB là khó thấy khác), SSIM cho video (trên 0.99 là khó thấy khác).
Chạy lại nhiều lần vẫn an toàn: luôn nén từ file gốc trong _source, không nén chồng lên bản đã nén.
"""
import shutil
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "assets" / "_source"

IMAGE_QUALITY = 94
VIDEO_CRF = 20
LOOKBOOK = ["home-01.jpg", "home-02.png", "home-03.png", "home-04.png", "home-05.png",
            "home-07.png", "home-08.png", "home-09.png", "home-10.png", "home-11.png"]
VIDEOS = ["hero.mp4", "break-1.mp4", "break-2.mp4", "break-3.mp4"]

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def keep_original(folder, name):
    """Chuyển file gốc vào assets/_source/<folder>/ (nếu chưa chuyển). Trả về đường dẫn file gốc."""
    original = SOURCE / folder / name
    current = ROOT / "assets" / folder / name
    if not original.exists():
        if not current.exists():
            return None
        original.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(current), str(original))
    return original


def psnr(a, b):
    """Độ giống nhau giữa 2 ảnh, đơn vị dB (càng cao càng giống)."""
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    mse = ((a - b) ** 2).mean()
    return 99.0 if mse == 0 else 10 * np.log10(255 ** 2 / mse)


def compress_image(name):
    src = keep_original("images", name)
    if src is None:
        print("Thiếu ảnh:", name)
        return 0, 0
    dst = ROOT / "assets" / "images" / (Path(name).stem + ".webp")
    with Image.open(src) as im:
        im = im.convert("RGB")
        im.save(dst, "WEBP", quality=IMAGE_QUALITY, method=6)
        with Image.open(dst) as out:
            score = psnr(im, out.convert("RGB"))
    before, after = src.stat().st_size, dst.stat().st_size
    print("  %-12s %6d KB -> %5d KB   PSNR %.1f dB" % (name, before // 1024, after // 1024, score))
    return before, after


def compress_video(name):
    src = keep_original("videos", name)
    if src is None:
        print("Thiếu video:", name)
        return 0, 0
    dst = ROOT / "assets" / "videos" / name
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
                    "-c:v", "libx264", "-preset", "slow", "-crf", str(VIDEO_CRF), "-pix_fmt", "yuv420p",
                    "-an", "-movflags", "+faststart", str(dst)], check=True, stdin=subprocess.DEVNULL)
    # So từng khung hình với bản gốc bằng bộ lọc ssim của ffmpeg
    log = subprocess.run([FFMPEG, "-hide_banner", "-i", str(dst), "-i", str(src), "-lavfi", "ssim", "-f", "null", "-"],
                         capture_output=True, text=True, stdin=subprocess.DEVNULL).stderr
    ssim = log.rsplit("All:", 1)[-1].split()[0] if "All:" in log else "?"
    before, after = src.stat().st_size, dst.stat().st_size
    print("  %-12s %6.1f MB -> %5.1f MB   SSIM %s" % (name, before / 1e6, after / 1e6, ssim))
    return before, after


def main():
    total_before = total_after = 0
    print("Ảnh lookbook (WebP q%d):" % IMAGE_QUALITY)
    for name in LOOKBOOK:
        b, a = compress_image(name)
        total_before += b
        total_after += a
    print("Video (H.264 CRF %d):" % VIDEO_CRF)
    for name in VIDEOS:
        b, a = compress_video(name)
        total_before += b
        total_after += a
    print("Tổng: %.1f MB -> %.1f MB" % (total_before / 1e6, total_after / 1e6))


if __name__ == "__main__":
    main()
