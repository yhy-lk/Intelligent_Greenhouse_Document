# AI Generated Images

- `original/` — AI 生成的原始图片（含水印）
- `cropped/` — 裁剪水印后可直接用于论文的图片

## 裁剪方法

```bash
# 批量裁剪（默认底部 22%、右侧 3%）
python crop_watermark.py --batch

# 单张裁剪，自定义比例
python crop_watermark.py original/xxx.png 0.25 0.05
```

裁剪脚本位于上级目录 `images/crop_watermark.py`。
