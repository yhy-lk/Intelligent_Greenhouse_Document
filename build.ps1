# 智能温室毕业论文 Pandoc 编译脚本
# 用法：在项目根目录执行 powershell -ExecutionPolicy Bypass -File build.ps1
# 输出：Docs/output/thesis.docx

# 1. 解决控制台输出显示乱码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
# 2. 解决传递给外部程序 (Pandoc) 参数时的中文乱码 (关键修复)
$OutputEncoding = [System.Text.Encoding]::UTF8 
$ErrorActionPreference = "Stop"

Set-Location "$PSScriptRoot\Docs\chapters"

$outputDir = "..\output"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

$files = @(
    "Abstract_cn.md",
    "Abstract_en.md",
    "Chapter1_绪论.md",
    "Chapter2_需求分析与总体设计.md",
    "Chapter3_硬件电路设计.md",
    "Chapter4_STM32控制层软件设计.md",
    "Chapter5_ESP32交互层软件设计.md",
    "Chapter6_总结与展望.md",
    "Chapter7_参考文献.md",
    "Appendix.md",
    "Acknowledgment.md"
)

pandoc $files `
    --citeproc `
    --bibliography=../references.bib `
    --csl=../csl/china-national-standard-gb-t-7714-2015-numeric.csl `
    --reference-doc="$outputDir\reference_docx.docx" `
    -o "$outputDir\thesis.docx"

Write-Host "编译完成 → $outputDir\thesis.docx" -ForegroundColor Green

cd ..\..