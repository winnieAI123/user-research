---
name: kano-from-interviews
description: 从用户访谈文字稿（.doc/.docx）自动生成 KANO 模型分析与可视化图表的端到端技能。适用场景：用户提供用户研究访谈文字稿文件夹，需要进行需求优先级分析并输出 KANO 四象限图表时自动触发。支持：(1) 提取并合并多份 .doc/.docx 文字稿为纯文本，(2) 基于自定义功能关键词在文本中检索用户原话证据，(3) 统计各功能提及频次，(4) 辅助 KANO 定性分类（必备型/期望型/魅力型/无差异型），(5) 生成手绘学术风格 HTML 可视化图表。Use when users say "做 KANO 分析"、"生成 KANO 图"、"分析访谈文字稿需求优先级" or mention interview transcripts + feature prioritization.
---

# KANO From Interviews

基于用户访谈文字稿，端到端生成 KANO 模型分析与可视化图表。

## 完整流程

### Step 1：收集文字稿文件夹路径

询问用户：
- 访谈文字稿位于哪个文件夹（支持 `.doc` / `.docx`，可有子文件夹区分线上/线下）
- 产品名称与访谈人数（用于图表标注）
- 城市/地域信息（如有）

**线下（offline）** = 产品体验后深访，侧重产品感知；**线上（online）** = 远程深访，侧重生活场景需求。如无线上/线下区分，统一放入单一文件夹即可。

### Step 2：提取并合并文字稿

运行 `scripts/extract_transcripts.py`：

```bash
# 区分线上/线下
python scripts/extract_transcripts.py --offline "路径\线下文件夹" --online "路径\线上文件夹" --out "输出路径"

# 不区分，单一文件夹
python scripts/extract_transcripts.py --all "路径\访谈文件夹" --out "输出路径"
```

- `.docx` 用 `python-docx` 读取；`.doc` 用 `win32com.client`（Windows 专用）
- 输出 `merged_offline.txt` + `merged_online.txt`（或 `merged_all.txt`）

**依赖安装**：`pip install python-docx pywin32`

### Step 3：定义功能与关键词

**优先让用户提供功能列表**。如果用户没有现成列表，帮助梳理。参考格式见 `references/feature_keywords_example.md`。

为每个功能定义：
- **功能名**（2-6 字，便于图表显示）
- **描述**（一句话）
- **关键词列表**（10-20 个，覆盖该功能的口语化表达）

关键词设计原则：覆盖用户口语表达，避免过于宽泛词（如单独的"好"/"有"）；覆盖领域特有词优先。

保存为 `features.json` 供下一步使用。

### Step 4：检索证据 & 统计频次

运行 `scripts/analyze_kano.py`：

```bash
python scripts/analyze_kano.py --features features.json --offline merged_offline.txt --online merged_online.txt --out "输出路径"
```

输出：
- `kano_evidence.json`：结构化证据，每项功能含用户原话列表和线上/线下提及次数
- `summary.txt`：按提及频次排序的汇总表

### Step 5：KANO 定性分类

阅读 `kano_evidence.json` 中的用户原话，从三个维度判断每项功能的 KANO 类型：

| 分类 | 判断标准 |
|------|---------|
| **必备型** | 情感强烈的负面表达，缺失=不购买 |
| **期望型** | 主动要求 + 讨论实现细节，质量敏感 |
| **魅力型** | 未主动提出，告知后有惊喜反应 |
| **无差异型** | 冷淡或主动排除 |

详细判断方法见 `references/kano_classification_guide.md`。

**注意**：提及次数高 ≠ 必备型，分类依据是用户情感强度和表达方式。

### Step 6：生成可视化图表

收集分类结果后，生成 HTML 图表。图表规范见 `references/chart_template_guide.md`。

图表特点（手绘学术风格）：
- 中文宋体 + 英文 Arial，暖米色纸张背景
- SVG 四象限散点图，带引线标注，避免标签重叠
- 象限水印清晰标注类型名称
- 底部功能卡片：分类 + 描述 + 提及次数 + 核心证据 + 用户原话

## 输出物清单

| 文件 | 内容 |
|------|------|
| `merged_offline.txt` / `merged_online.txt` | 合并纯文本 |
| `kano_evidence.json` | 结构化证据（含用户原话） |
| `summary.txt` | 频次排序汇总表 |
| `kano_chart.html` | 最终可视化图表（浏览器直接打开） |
