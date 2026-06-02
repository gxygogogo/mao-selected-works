---
name: mao-selected-works
description: Use this skill when Codex needs to help study, search, summarize, quote, annotate, compare, teach, write about, or apply Mao Zedong's Selected Works / 毛泽东选集 / 毛选. Use for chapter-level reading guidance, concept explanations, historical context, citation-aware summaries, local corpus lookup, close reading of user-provided text, study notes, reading plans, and mapping a user's current work, study, project, team, decision, or life problem to relevant methods in 毛选.
---

# Mao Selected Works

## Core Workflow

1. Classify the request as reading guidance, concept explanation, corpus search, quotation lookup, close reading, comparison, writing support, teaching support, or problem-to-method mapping.
2. Use `references/volume-index.md` to identify relevant volumes, titles, years, and themes.
3. Use `references/concepts.md` when the user asks about recurring concepts such as investigation, practice, contradiction, mass line, united front, protracted war, policy, organization, or party work methods.
4. Use `scripts/search_corpus.py` to search local Markdown files under `corpus/` before claiming that a phrase, passage, or exact wording appears in the text.
5. Follow `references/citation-policy.md` for direct quotations and source attribution.
6. For modern personal or work problems, follow `references/problem-to-method.md`; present the mapping as a methodological analogy, not as a claim that the text directly addresses the modern situation.
7. State uncertainty clearly when PDF extraction artifacts, editions, page numbers, or exact wording may need verification.

## Local Corpus

The local corpus is stored in:

- `corpus/vol-1/`
- `corpus/vol-2/`
- `corpus/vol-3/`
- `corpus/vol-4/`

Each article is a Markdown file with YAML frontmatter. The field `verified: false` means the text was extracted from user-provided PDFs and should be checked against the PDFs before formal citation.

## Search Commands

Search across all volumes:

```bash
python3 scripts/search_corpus.py "主要矛盾"
```

Search one volume:

```bash
python3 scripts/search_corpus.py "没有调查" --volume 1
```

Show more context:

```bash
python3 scripts/search_corpus.py "群众路线" --context 120 --limit 8
```

## Response Rules

- Distinguish direct quote, paraphrase, interpretation, and historical context.
- Prefer article title, volume, and year over page numbers unless the user provides or verifies a specific edition.
- Do not fabricate exact quotations. If search fails, say the local corpus did not find the phrase.
- When giving advice through this skill, translate concepts into concrete actions and include what to observe next.
- If the user's problem is medical, legal, financial, mental-health, safety-critical, or otherwise high stakes, do not use 毛选 as a substitute for professional help.
- Avoid forcing every question into a 毛选 framework. If the mapping is weak, say so and use the closest relevant method cautiously.

## Common Output Patterns

For article explanations:

1. Title, year, and volume
2. Historical problem addressed
3. Core argument
4. Key concepts
5. Structure
6. Useful passages to inspect
7. Reading notes or follow-up questions

For problem-to-method mapping:

1. Restate the user's problem concretely
2. Diagnose the problem type
3. Map to relevant concepts and essays
4. Extract the method
5. Give a concrete action plan
6. Define what to observe in the next review

For quotation lookup:

1. Search the corpus
2. Report exact matches or near matches
3. Give title, volume, and year
4. Mark whether the wording is exact from the local corpus
5. Warn when formal citation needs PDF verification
