# 智能温室系统 - 毕业设计论文仓库

本仓库是**智能温室系统**毕业设计的论文与文档工程。采用 **Markdown + Pandoc + Mermaid** 的工作流撰写学术论文，支持从 Markdown 源文件自动生成带参考文献的 Word 文档。

## 项目概述

系统包含两个子系统：

| 子系统 | 技术栈 | 职责 |
|---|---|---|
| **ESP32 交互层** | C/C++, PlatformIO, LVGL | GUI 显示、语音助手、WiFi 联网、DeepSeek API 调用、CAN 通信 |
| **STM32 控制层** | Rust, Cargo | 传感器驱动（SHT30, BH1750）、电机控制（PID）、LED 控制、CAN 协议 |

> 源代码通过 [Repomix](https://github.com/yamadashy/repomix) 打包为 `repomix-output.xml` 供 AI 阅读，该文件已通过 `.gitignore` 排除（含 API 密钥等敏感信息）。

## 目录结构

```
Document/
├── Docs/
│   ├── chapters/                  # 论文章节 Markdown 源文件
│   │   ├── Chapter1_绪论.md
│   │   └── ...
│   ├── images/                    # 图表资源（SVG/PNG/Mermaid 源文件）
│   │   ├── architecture.svg
│   │   ├── pid_control_strategy.svg
│   │   └── screenshots/           # 截图资源
│   ├── csl/                       # 引用样式文件（GB/T 7714-2015）
│   ├── references.bib             # 参考文献数据库（BibTeX 格式）
│   └── output/                    # Pandoc 编译产物（docx 等，已 gitignore）
├── INSTRUCTIONS.md                # AI 辅助写作行为准则
├── CLAUDE.md                      # Claude Code 项目指令
├── .mcp.json                      # MCP 工具配置
└── repomix-output.xml             # 源代码打包文件（已 gitignore）
```

## 环境部署

### 前置依赖

| 工具 | 用途 | 安装方式 |
|---|---|---|
| **Pandoc** | Markdown → Word 转换 | [官网下载](https://pandoc.org/installing.html) 或 `scoop install pandoc` |
| **Mermaid CLI** | `.mmd` → `.svg`/`.png` 渲染 | `npm install -g @mermaid-js/mermaid-cli` |
| **Node.js** | Mermaid CLI 运行环境 | [官网下载](https://nodejs.org/) |

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/yhy-lk/Intelligent_Greenhouse_Document.git
cd Intelligent_Greenhouse_Document

# 2. 安装 Mermaid CLI（需先安装 Node.js）
npm install -g @mermaid-js/mermaid-cli

# 3. 验证 Pandoc 安装
pandoc --version
```

## 使用方法

### 编译单章论文为 Word

```bash
pandoc Docs/chapters/Chapter1_绪论.md \
  --citeproc \
  --bibliography=Docs/references.bib \
  --csl=Docs/csl/china-national-standard-gb-t-7714-2015-numeric.csl \
  -o Docs/output/Chapter1_绪论.docx
```

### 合并多章编译为完整论文

```bash
pandoc Docs/chapters/Chapter1_绪论.md \
       Docs/chapters/Chapter2_需求分析与总体设计.md \
  --citeproc \
  --bibliography=Docs/references.bib \
  --csl=Docs/csl/china-national-standard-gb-t-7714-2015-numeric.csl \
  -o Docs/output/Thesis_Draft.docx
```

### 渲染 Mermaid 图表

```bash
# 生成 SVG 矢量图（推荐，学术排版首选）
mmdc -i Docs/images/architecture.mmd -o Docs/images/architecture.svg

# 生成高分辨率 PNG（备选）
mmdc -i Docs/images/architecture.mmd -o Docs/images/architecture.png -s 4
```

### SVG 转 PNG（Pandoc 兼容性处理）

Pandoc 默认不支持在 docx 中嵌入 SVG，需先转换：

```bash
# 使用 rsvg-convert（推荐）
rsvg-convert -w 2000 Docs/images/architecture.svg > Docs/images/architecture.png

# 或使用 mmdc 直接从源文件生成 PNG
mmdc -i Docs/images/architecture.mmd -o Docs/images/architecture.png -s 4
```

## 参考文献管理

所有文献信息集中在 `Docs/references.bib` 中，使用 BibTeX 格式管理。论文正文中通过 `[@key]` 语法引用，Pandoc `--citeproc` 会自动生成编号和参考文献列表。

```markdown
# 单篇引用
温室温度控制常采用 PID 算法实现闭环调节[@wei2022intelligent]。

# 多篇引用
多项研究[@hooshmand2025smart; @huang2024vegetable]表明……
```

引用样式遵循 **GB/T 7714-2015 顺序编码制**，CSL 文件来自 [zepinglee/chinese-std-gb-t-7714-2015-csl](https://github.com/zepinglee/chinese-std-gb-t-7714-2015-csl)。

## AI 辅助写作

本项目使用 [Claude Code](https://claude.ai/code) 进行 AI 辅助论文写作，行为准则定义在 `INSTRUCTIONS.md` 中。核心规范：

1. **联网搜索**：通过 WebFetch 访问 Google Scholar 获取真实文献
2. **基于真实代码**：论文内容必须基于 `repomix-output.xml` 中的实际代码
3. **切香肠写法**：逐节撰写，每节不少于 500 字
4. **图文穿插**：图表紧跟引用处，预留实物图占位符

## 许可证

学术用途，仅供学习参考。
