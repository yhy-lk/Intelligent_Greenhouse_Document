# 智能温室毕业设计 — 项目指令

本项目是**智能温室系统**的毕业设计，当前核心任务是**撰写毕业论文**。

`repomix-output.xml` 包含项目全部源代码（ESP32 交互层 + STM32 控制层），撰写涉及模块实现的内容时**必须先查阅对应代码**。

详细写作流程由 Skills 承载：`thesis-writer`（论文正文写作）、`abstract-writer`（英文摘要）、`mermaid-renderer`（图表渲染）、`thesis-reviewer`（论文审查）、`diagram-prompt-generator`（画图提示词）、`image-cropper`（AI 图片水印裁剪）。

---

# 环境规则

## 代理

网络代理端口 7890：`http://127.0.0.1:7890`。

## 可用搜索工具

| 工具 | 用途 | 备注 |
|---|---|---|
| `WebFetch` | 访问 Google Scholar、论文详情页、数据手册 | 首选 |
| `mcp__agent-browser__*` | 动态页面、交互操作、截图 | 截图保存到 `Docs/images/screenshots/` |

## 不可用工具

| 工具 | 原因 |
|---|---|
| `mcp__duckduckgo__duckduckgo_web_search` | SSL 握手失败 |
| `ddgs` CLI | SSL 握手失败 |
| Read 读取 PNG/JPG | 无法解析位图，读 .mmd 或 .svg |

---

# 写作规范

## 章节字数

| 章 | 标题 | 字数 |
|---|---|---|
| 1 | 绪论 | 1000-1500 |
| 2 | 需求分析与总体设计 | 1000-1500 |
| 3 | 硬件电路设计 | 1500-2500 |
| 4 | STM32控制层软件设计 | 2000-3500 |
| 5 | ESP32交互层软件设计 | 1500-3000 |
| 6 | 总结与展望 | 500-1000 |

总计 8000-13000 字（不含代码、参考文献、附录）。**逐节撰写，禁止整章生成。**

## 代码引用

- 正文代码片段不超过 10 行，完整源码移至附录
- 变量名、数据结构、控制流必须来自 repomix-output.xml 中的真实代码
- 标注源文件路径，如 `Src/Stm32_Control/crates/bsw/src/pid.rs`
- 将代码逻辑转化为带数学公式的学术语言，不要堆砌代码

## 图表规范

- 图题格式：`**图 {章节号}-{序号} {标题}**`，紧跟图表之后
- 正文中必须先引用图表，再出现图表
- Mermaid 图表使用 `%%{init: {'theme': 'base'}}%%` 黑白主题
- Pandoc 不支持 SVG 嵌入 docx，正文**只引用 PNG**
- 泛型尖括号必须转义：`&lt;` `&gt;`
- 优先 TD 布局，节点不超过 10 个，文本不超过 15 个汉字
- 涉及硬件时预留实物照片占位符

## 引用规范

- 参考文献数据库：`Docs/references.bib`，BibTeX 格式
- 正文引用语法：`[@key]`，**禁止手动编号 `[1]`**
- key 命名：`{作者姓小写}{年份}{关键词}`，如 `zhang2020pid`
- 编号由 Pandoc `--citeproc` 自动生成

## Pandoc 编译

**工作目录必须为 `Docs/chapters/`**（图片使用 `../images/code_generated/` 相对路径）：

```bash
cd Docs/chapters
pandoc Chapter4_STM32控制层软件设计.md \
  --citeproc \
  --bibliography=../references.bib \
  --csl=../csl/china-national-standard-gb-t-7714-2015-numeric.csl \
  -o ../output/Chapter4.docx
```

---

# 错误禁忌（已犯过的错）

## 1. 禁止夸大系统功能

描述功能必须严格基于代码实现。DeepSeek AI 当前**仅支持信息查询与建议生成**，不具备直接控制执行器的能力。代码中没有实现的功能不能在论文中声称具备。

## 2. 禁止引用滥用

公共知识（CAN 帧格式、I2C 协议、PID 原理）不需要引用。引用仅用于：引入研究方向、支持技术选型、对比现有研究不足、引用数据手册参数。

## 3. 禁止 AI 语气词汇

以下词汇在论文中禁止使用（完整列表见 `references/forbidden-patterns.md`）：
- 创新夸大：innovative、pioneering、revolutionary、transformative framework
- 性能夸大：superior、surpass、excel、remarkable、unprecedented、breakthrough
- 贡献空话：comprehensive experiments、extensive analysis、general-purpose、is capable of
- AI 连接词：notably、yielding、at its essence
- AI 高频动词：encompass、differentiate、reveal、underscore、exhibit、pave the way for、highlight the potential of
- AI 高频搭配：profound challenges、stems from、rigid、impede

出现 3 处以上为 MAJOR 级别问题。替代词：propose、design、present、show、demonstrate、report、observe。

## 4. 学术诚信

内容必须基于真实实现，不得伪造数据或实验结果。引用必须来自真实文献，不得编造。AI 率检查要求：避免 AI 语气词（见上），用自己的语言改写，不要直接使用 AI 输出的原文。

## 5. 术语一致性

全文统一使用同一术语，首次出现给出英文：迟滞控制（Hysteresis Control）、主节点、从节点。

## 6. 图表可读性

SVG viewBox 宽度控制在 800px 以内。缩放后字号 = 16 × (500 / viewBox宽度)，结果应 >= 10px。结构化数据优先用 Markdown 表格，不要用流程图展示静态信息。

---

# 行为准则

## 1. 编码前先思考

不要凭假设行事。如有不确定之处请向用户确认。存在多种理解方式时逐一列出。有不明确的地方暂停执行，寻求澄清。

## 2. 简洁优先

用最少的代码解决问题。不添加超出需求的功能，不为一次性代码创建抽象层。

## 3. 精确修改

只改动必须改动的部分。不"顺手改进"相邻代码，遵循现有代码风格。每一行改动都应能追溯到用户请求。

## 4. 目标驱动执行

定义明确的成功标准，反复验证直至达成。多步骤任务列出简要计划。
