# Build Mao Selected Works Skill

This guide shows how to build a Codex skill for studying, searching, quoting, and applying methods from `毛泽东选集`.

The finished skill is named:

```text
mao-selected-works
```

## 1. Design The Skill

Define the skill's purpose before touching files.

This skill should support:

- Reading guidance for each volume and article.
- Concept explanation, such as 实践, 矛盾, 主要矛盾, 群众路线, 统一战线.
- Local corpus search across all four volumes.
- Citation-aware quote checking.
- Close reading of user-provided passages.
- Reading notes, study plans, teaching outlines, and writing support.
- Problem-to-method mapping: the user describes a current problem, and the skill maps it to relevant methods from 毛选.

Do not put the full book text inside `SKILL.md`. Keep `SKILL.md` as the operating manual. Put the extracted books under `corpus/`.

## 2. Recommended File Tree

```text
mao-selected-works/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── corpus/
│   ├── README.md
│   ├── vol-1/
│   ├── vol-2/
│   ├── vol-3/
│   └── vol-4/
├── references/
│   ├── citation-policy.md
│   ├── concepts.md
│   ├── problem-to-method.md
│   └── volume-index.md
└── scripts/
    └── search_corpus.py
```

## 3. Prepare Source PDFs

Put the source PDFs somewhere stable. In this build, the files were:

```text
毛泽东选集1.pdf
毛泽东选集2.pdf
毛泽东选集3.pdf
毛泽东选集4.pdf
```

Check that `pdftotext` is available:

```bash
command -v pdftotext
```

Extract each PDF to temporary text:

```bash
pdftotext -layout 毛泽东选集1.pdf /private/tmp/maoxuan_vol1.txt
pdftotext -layout 毛泽东选集2.pdf /private/tmp/maoxuan_vol2.txt
pdftotext -layout 毛泽东选集3.pdf /private/tmp/maoxuan_vol3.txt
pdftotext -layout 毛泽东选集4.pdf /private/tmp/maoxuan_vol4.txt
```

Inspect each extracted file:

```bash
sed -n '1,240p' /private/tmp/maoxuan_vol1.txt
rg -n "目录|实践论|矛盾论" /private/tmp/maoxuan_vol1.txt
```

Use the table of contents and body headings to identify article start lines.

## 4. Split Corpus Into Markdown

Create the corpus folders:

```bash
mkdir -p mao-selected-works/corpus/vol-1
mkdir -p mao-selected-works/corpus/vol-2
mkdir -p mao-selected-works/corpus/vol-3
mkdir -p mao-selected-works/corpus/vol-4
```

For each article, save one Markdown file:

```text
corpus/vol-1/1937-实践论.md
corpus/vol-1/1937-矛盾论.md
corpus/vol-2/1938-论持久战.md
corpus/vol-3/1945-论联合政府.md
corpus/vol-4/1949-论人民民主专政.md
```

Each file should begin with frontmatter:

```markdown
---
title: 实践论
volume: 1
year: 1937
date_text: 一九三七年七月
source_pdf: 毛泽东选集1.pdf
source_note: Extracted with pdftotext from the user-provided PDF; verify exact quotations against the PDF before citation.
verified: false
---

# 实践论

正文...
```

Use `verified: false` because PDF extraction can introduce artifacts:

- Footnotes may appear in the middle of body text.
- Page headers and page numbers may be mixed into text.
- Line breaks may split words or phrases.
- Some punctuation may differ from the printed edition.

For formal quotation, verify against the source PDF.

## 5. Clean Extraction Artifacts

Remove common noise:

- `www.mzdbl.cn`
- Table of contents pages
- Running page headers
- Page numbers
- Publication/copyright pages

Check for leftovers:

```bash
rg -n "www\\.mzdbl|目\\s*录|人民出版社出版|书号1001|全世界无产者" mao-selected-works/corpus
```

Count files:

```bash
find mao-selected-works/corpus -maxdepth 2 -name '*.md' | wc -l
```

This build produced 160 Markdown article files.

## 6. Write SKILL.md

`SKILL.md` is the required file. Keep it short and procedural.

Use frontmatter like this:

```markdown
---
name: mao-selected-works
description: Use this skill when Codex needs to help study, search, summarize, quote, annotate, compare, teach, write about, or apply Mao Zedong's Selected Works / 毛泽东选集 / 毛选. Use for chapter-level reading guidance, concept explanations, historical context, citation-aware summaries, local corpus lookup, close reading of user-provided text, study notes, reading plans, and mapping a user's current work, study, project, team, decision, or life problem to relevant methods in 毛选.
---
```

The description is the trigger. Include all major use cases there.

In the body, include:

- Core workflow.
- Local corpus paths.
- Search commands.
- Response rules.
- Common output formats.

Do not include the whole book text in `SKILL.md`.

## 7. Add Reference Files

Create:

```text
references/citation-policy.md
references/concepts.md
references/problem-to-method.md
references/volume-index.md
```

Use them this way:

- `citation-policy.md`: rules for direct quotes, source lookup, and verification.
- `concepts.md`: concept map for 实践, 矛盾, 群众路线, 统一战线, 持久战, 组织起来.
- `problem-to-method.md`: maps real problems to 毛选 methods.
- `volume-index.md`: compact guide to important articles and themes.

Keep detailed knowledge in `references/`, not in `SKILL.md`.

## 8. Add Search Script

Create:

```text
scripts/search_corpus.py
```

The script should:

- Search all `corpus/vol-*/*.md`.
- Read frontmatter for title, volume, and year.
- Print snippets with file paths.
- Support `--volume`, `--limit`, `--context`, and optional whitespace-insensitive search.

Example usage:

```bash
python3 scripts/search_corpus.py "主要矛盾" --volume 1 --limit 3
python3 scripts/search_corpus.py "没有调查" --volume 3 --context 80
python3 scripts/search_corpus.py "群众路线" --limit 10
```

Make it executable:

```bash
chmod +x scripts/search_corpus.py
```

## 9. Add UI Metadata

Create:

```text
agents/openai.yaml
```

Example:

```yaml
display_name: 毛泽东选集研究
short_description: Study, search, cite, and apply methods from 毛泽东选集.
default_prompt: 用毛泽东选集研究 skill 帮我查找相关篇目、解释概念、核对引文，或把我遇到的问题映射成可执行的方法。
```

## 10. Validate The Skill

Run the skill validator:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py mao-selected-works
```

Expected output:

```text
Skill is valid!
```

Test search:

```bash
python3 mao-selected-works/scripts/search_corpus.py "没有调查" --volume 3 --limit 2 --context 60
```

Expected result: matches in `《农村调查》的序言和跋`.

## 11. Install For Codex Auto-Discovery

Copy the skill to the Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R mao-selected-works ~/.codex/skills/mao-selected-works
```

Validate the installed copy:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/mao-selected-works
```

Test the installed search script:

```bash
python3 ~/.codex/skills/mao-selected-works/scripts/search_corpus.py "主要矛盾" --volume 1 --limit 2
```

## 12. Example Prompts

```text
用 mao-selected-works 帮我查一下“没有调查就没有发言权”出自哪里。
```

```text
用 mao-selected-works 给我解释《矛盾论》里的主要矛盾。
```

```text
用 mao-selected-works 帮我制定一个 30 天读毛选计划。
```

```text
用 mao-selected-works 分析我最近的问题：项目想法太多，迟迟无法开始。
```

```text
用 mao-selected-works 把《实践论》和《矛盾论》做一个对照表。
```

## 13. Maintenance

When updating the skill:

1. Edit the workspace copy first.
2. Validate it.
3. Test search.
4. Copy it to `~/.codex/skills/mao-selected-works`.
5. Validate the installed copy.

When adding better source text:

- Keep the same article-level Markdown structure.
- Update `source_pdf`, `source_note`, and `verified`.
- If the new text is carefully proofread, set `verified: true`.
- Regenerate `corpus/README.md` if file names change.

## 14. Important Boundary

This skill can help with study, textual analysis, citation lookup, and method translation. It should not replace professional advice for legal, medical, financial, mental-health, or safety-critical problems.
