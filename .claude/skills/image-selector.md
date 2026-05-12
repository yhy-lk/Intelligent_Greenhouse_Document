---
name: image-selector
description: >-
  生成多比例裁剪版本供用户挑选，删除未选中图片并重命名选中图片。
  当用户要求"挑选裁剪比例"、"选图片"、"select image"、"对比裁剪效果"时使用。
---

# 图片裁剪挑选器

## 概述

本技能对单张 AI 生成图片按多个裁剪比例生成候选版本，由用户挑选最合适的比例，然后删除其余图片并将选中图片重命名为与原图相同的文件名。

## 何时使用本技能

- 用户说"挑选裁剪比例"、"选图片"、"对比裁剪效果"时。
- 用户要求"帮我选一张合适的裁剪版本"时。
- 用户说"select image"、"pick crop ratio"时。

## 何时不使用本技能

- 直接裁剪图片（不需要挑选）。请改用 `image-cropper`。
- 生成 Mermaid 图表。请改用 `mermaid-renderer`。
- 生成画图提示词。请改用 `diagram-prompt-generator`。

## 操作步骤

### 步骤 1：确认原图

检查 `Docs/images/ai_generated/original/` 中是否有待处理的图片。如用户指定了图片路径，使用指定路径；否则列出 `original/` 下所有图片让用户选择。

### 步骤 2：生成候选版本

运行裁剪脚本的 `--sweep` 模式，生成 9%-30%（步进 3%）的裁剪版本：

```bash
cd Docs/images
python crop_watermark.py --sweep <图片路径>
```

默认参数：最小 9%，最大 30%，步进 3%。用户可自定义：

```bash
python crop_watermark.py --sweep <图片路径> 0.10 0.35 0.05   # 10%-35%，步进 5%
```

### 步骤 3：展示候选版本

将生成的裁剪版本列表展示给用户，格式：

| 文件名 | 裁剪比例 | 尺寸 |
|---|---|---|
| `xxx_09pct.png` | 9% | WxH |
| `xxx_12pct.png` | 12% | WxH |
| ... | ... | ... |

提示用户选择一个或多个满意的版本。

### 步骤 4：清理并重命名

用户选定后，执行以下操作：

1. **删除** `cropped/` 目录下该图片的所有其他裁剪版本（包括 `_XXpct` 后缀的和无后缀的旧版本）
2. **重命名** 选中的图片，去掉 `_XXpct` 后缀，使其与原图文件名一致

示例（用户选中 15%）：

```bash
cd Docs/images/ai_generated/cropped
# 删除未选中的版本
rm -f stm32_layered_architecture_09pct.png stm32_layered_architecture_12pct.png ...
# 重命名选中版本
mv stm32_layered_architecture_15pct.png stm32_layered_architecture.png
```

### 步骤 5：确认结果

向用户报告最终保留的文件路径和尺寸，确认操作完成。

## 文件结构

```
Docs/images/
├── crop_watermark.py          ← 裁剪脚本（含 --sweep 模式）
├── ai_generated/
│   ├── original/              ← 待处理的原图
│   └── cropped/               ← 最终选中的裁剪版本
```
