"""
AI 生成图片水印裁剪工具

用法:
    python crop_watermark.py <图片路径> [底部裁剪比例] [右侧裁剪比例]
    python crop_watermark.py --batch [底部裁剪比例] [右侧裁剪比例]
    python crop_watermark.py --sweep <图片路径> [最小比例] [最大比例] [步进]

示例:
    python crop_watermark.py original/photo.png              # 默认裁剪底部 22%、右侧 3%
    python crop_watermark.py original/photo.png 0.25 0.05   # 裁剪底部 25%、右侧 5%
    python crop_watermark.py --batch                         # 批量处理 original/ 下所有图片
    python crop_watermark.py --sweep original/photo.png      # 9%-30%，步进 3%，生成多张
    python crop_watermark.py --sweep original/photo.png 0.09 0.30 0.03
"""

import sys
import os
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).parent
ORIGINAL_DIR = BASE_DIR / "ai_generated" / "original"
CROPPED_DIR = BASE_DIR / "ai_generated" / "cropped"

DEFAULT_BOTTOM_RATIO = 0.22  # 裁掉底部 22%（提示词要求留 20-25%）
DEFAULT_RIGHT_RATIO = 0.00   # 裁掉右侧 0%


def crop_watermark(img_path: Path, bottom_ratio: float, right_ratio: float, save_path: Path = None) -> Path:
    """裁剪单张图片的水印区域，返回保存路径。"""
    if save_path is None:
        save_path = CROPPED_DIR / img_path.name
    if save_path.exists():
        print(f"  SKIP {save_path.name}: 已存在，跳过")
        return save_path

    img = Image.open(img_path)
    w, h = img.size

    crop_bottom = int(h * bottom_ratio)
    crop_right = int(w * right_ratio)

    new_w = w - crop_right
    new_h = h - crop_bottom

    if new_w <= 0 or new_h <= 0:
        print(f"  SKIP {img_path.name}: 裁剪比例过大，剩余区域无效")
        return None

    cropped = img.crop((0, 0, new_w, new_h))
    img.close()

    cropped.save(save_path, quality=95)
    cropped.close()

    print(f"  {save_path.name}: {w}x{h} -> {new_w}x{new_h} (去底部{crop_bottom}px, 去右侧{crop_right}px)")
    return save_path


def sweep_crop(img_path: Path, min_ratio: float = 0.09, max_ratio: float = 0.30, step: float = 0.03):
    """对单张图片按不同裁剪比例生成多张，文件名含百分比标识。"""
    CROPPED_DIR.mkdir(parents=True, exist_ok=True)

    stem = img_path.stem
    suffix = img_path.suffix

    ratio = min_ratio
    while ratio <= max_ratio + 1e-9:
        pct = int(round(ratio * 100))
        save_path = CROPPED_DIR / f"{stem}_{pct:02d}pct{suffix}"
        crop_watermark(img_path, ratio, 0.0, save_path)
        ratio += step

    print(f"完成，裁剪后图片保存在: {CROPPED_DIR}")


def batch_crop(bottom_ratio: float, right_ratio: float):
    """批量处理 original/ 下所有图片。"""
    CROPPED_DIR.mkdir(parents=True, exist_ok=True)

    extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    images = [f for f in ORIGINAL_DIR.iterdir() if f.suffix.lower() in extensions]

    if not images:
        print(f"original/ 中没有找到图片: {ORIGINAL_DIR}")
        return

    print(f"找到 {len(images)} 张图片，裁剪参数: 底部{bottom_ratio:.0%} 右侧{right_ratio:.0%}")
    for img_path in sorted(images):
        crop_watermark(img_path, bottom_ratio, right_ratio)
    print(f"完成，裁剪后图片保存在: {CROPPED_DIR}")


def main():
    args = sys.argv[1:]

    bottom = DEFAULT_BOTTOM_RATIO
    right = DEFAULT_RIGHT_RATIO

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return

    if args[0] == "--batch":
        if len(args) >= 2:
            bottom = float(args[1])
        if len(args) >= 3:
            right = float(args[2])
        batch_crop(bottom, right)
    elif args[0] == "--sweep":
        if len(args) < 2:
            print("用法: python crop_watermark.py --sweep <图片路径> [最小比例] [最大比例] [步进]")
            return
        img_path = Path(args[1])
        if not img_path.is_absolute():
            img_path = BASE_DIR / img_path
        if not img_path.exists():
            print(f"文件不存在: {img_path}")
            return
        min_r = float(args[2]) if len(args) >= 3 else 0.09
        max_r = float(args[3]) if len(args) >= 4 else 0.30
        step = float(args[4]) if len(args) >= 5 else 0.03
        sweep_crop(img_path, min_r, max_r, step)
    else:
        img_path = Path(args[0])
        if not img_path.is_absolute():
            # 如果路径以 original/ 开头，去掉前缀，在 ORIGINAL_DIR 中查找
            if img_path.parts[0] == "original":
                candidate = ORIGINAL_DIR / Path(*img_path.parts[1:])
                if candidate.exists():
                    img_path = candidate
                else:
                    # 尝试原始路径
                    if not img_path.exists():
                        img_path = BASE_DIR / img_path
            # 首先尝试相对于当前目录
            elif img_path.exists():
                pass  # 找到文件
            # 然后尝试相对于 ORIGINAL_DIR
            elif (ORIGINAL_DIR / img_path).exists():
                img_path = ORIGINAL_DIR / img_path
            # 最后尝试相对于 BASE_DIR
            else:
                img_path = BASE_DIR / img_path
        if not img_path.exists():
            print(f"文件不存在: {img_path}")
            return
        if len(args) >= 2:
            bottom = float(args[1])
        if len(args) >= 3:
            right = float(args[2])
        CROPPED_DIR.mkdir(parents=True, exist_ok=True)
        crop_watermark(img_path, bottom, right)


if __name__ == "__main__":
    main()
