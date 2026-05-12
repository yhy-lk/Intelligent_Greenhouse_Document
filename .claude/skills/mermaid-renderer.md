---
name: mermaid-renderer
description: >-
  为论文渲染 Mermaid 图表，应用所有已知的 bug 修复约束。
  处理主题、转义、布局、SVG/PNG 生成。当用户要求
  "画流程图"、"创建图表"、"制作 Mermaid 图"、"渲染架构图"、
  "draw a flowchart"、"create a diagram"、"make a Mermaid chart"、
  "render architecture diagram"，或任何为论文生成可视化图表的请求时使用。
---

# Mermaid 渲染器

## 概述

本技能为毕业论文渲染 Mermaid 图表，应用调试过程中发现的所有约束：主题设置、通用字符转义、A4 布局适配以及 SVG 转 PNG 生成流程。

## 何时使用本技能

- 为论文创建任何 Mermaid 图表时。
- 用户要求"画流程图"、"创建图表"、"制作 Mermaid 图"、"渲染架构图"时。
- 修复渲染失败的 Mermaid 图表时。

## 何时不使用本技能

- 撰写论文正文。请改用 `thesis-writer`。
- 设计非 Mermaid 类型的图表（如 Matplotlib 图表、PowerPoint 图表）。请使用常规辅助功能。

## 强制约束

### 1. 主题声明（必需）

每个 `.mmd` 文件必须以以下内容开头：

```mermaid
%%{init: {'theme': 'base'}}%%
```

不得使用 `default`、`dark`、`forest` 或任何彩色主题。
黑白打印要求使用 `base` 主题。

### 2. 通用字符转义（必需）

Mermaid 会将 `< >` 解析为 HTML 标签。在节点描述中，必须转义所有尖括号：

| 字符 | 转义形式 |
|---|---|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"`（在非引号文本中） | `&quot;` |

**错误示例**：`A[处理 Option<f32> 数据]`
**正确示例**：`A[处理 Option&lt;f32&gt; 数据]`

### 3. 布局规则

- **默认**：流程图使用 `TD`（自上而下）。
- **仅宽架构图**：当图表具有自然的从左到右流向且 TD 布局会过高时，使用 `LR`（从左到右）。
- **每个图表最大节点数**：8-10 个。超出时拆分为子图。
- **节点文本长度**：不超过 15 个汉字（总计约 30 个字符）。

### 4. A4 宽度约束

A4 纸在 72 DPI 下的有效宽度约为 500px。SVG viewBox 宽度应保持在 800px 以下，以确保缩放后文字可读：

```
scaled_font = 16 * (500 / viewBox_width) >= 10px
```

如果 viewBox 宽度超过 800px，则图表过宽，需要拆分。

### 5. SVG 转 PNG 流程（必需）

Pandoc 无法在 docx 中嵌入 SVG。生成流程如下：

```bash
# 步骤 1：保存 .mmd 源文件
# 步骤 2：生成 SVG（保留矢量源文件）
mmdc -i diagram.mmd -o diagram.svg
# 步骤 3：生成 PNG 供论文引用
mmdc -i diagram.mmd -o diagram.png -s 4
```

在论文 Markdown 中，只引用 PNG：
```markdown
![图 X-Y 标题](../images/code_generated/diagram.png)
```

论文 Markdown 中不得引用 SVG。

### 6. 图表类型选择

| 内容类型 | Mermaid 类型 | 示例 |
|---|---|---|
| 系统架构 | `graph LR` 或 `graph TD` | 模块关系 |
| 数据流 | `flowchart LR` 或 `flowchart TD` | 传感器数据管道 |
| 时序/时序图 | `sequenceDiagram` | I2C 读写协议 |
| 状态机 | `stateDiagram-v2` | 调度器状态 |
| 算法步骤 | `flowchart TD` | PID 计算 |

### 7. 文件组织

```
Docs/images/code_generated/
├── architecture.mmd        # 源文件
├── architecture.svg        # 矢量备份
├── architecture.png        # 论文中引用的文件
├── pid_control.mmd
├── pid_control.svg
├── pid_control.png
└── ...
```

## 操作步骤

### 步骤 1：设计图表

根据用户需求，确定：
- 需要传达什么信息
- 使用哪种图表类型
- 如何拆分过于复杂的图表

### 步骤 2：编写 .mmd 文件

应用以上所有约束。保存到 `Docs/images/code_generated/` 目录。

### 步骤 3：渲染

```bash
mmdc -i Docs/images/code_generated/diagram.mmd -o Docs/images/code_generated/diagram.svg
mmdc -i Docs/images/code_generated/diagram.mmd -o Docs/images/code_generated/diagram.png -s 4
```

### 步骤 4：插入论文

为用户提供 Markdown 引用语法，以便粘贴到论文章节中。

## 完整性检查

完成前检查：

1. **[检查]** `.mmd` 文件以 `%%{init: {'theme': 'base'}}%%` 开头。
2. **[检查]** 节点文本中的所有 `<` 和 `>` 均已转义。
3. **[检查]** 节点数量不超过 10 个。
4. **[检查]** viewBox 宽度将低于 800px（检查节点数量和文本长度）。
5. **[检查]** Markdown 中只引用 PNG，不引用 SVG。
6. **[检查]** 图题格式为 `**图 {章节号}-{序号} {标题}**`。
