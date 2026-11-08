---
name: "paper-brief"
description: "Use when the user wants a short read of a paper (arXiv link, PDF or title): an importable English Markdown brief, 5 to 10 minutes long, with core idea, located findings, trust check."
---

# Paper Brief

Turn one research paper into a brief that a reader finishes in 5 to 10 minutes and still holds the paper's idea, its evidence and how far to trust it. The output is a single English Markdown file that imports directly into the blog's post editor ("Import .md") and renders without edits.

The brief is layered. Each section is useful on its own, so a reader who stops after the Summary or after the core idea still leaves with something correct. The reader should never need the original paper to understand the brief, and the brief tells them exactly which parts of the original are worth opening.

The brief follows the Curiosities voice of the site (repository skill `curiosities-voice` in `dangvngiang.dev`). If that skill and this one ever disagree on voice or formatting, the repository skill wins. For a full lecture-style post on the same paper, use `graduate-lecture` instead; this skill is the short format and is often the screening step before it.

## When to use

- The user gives a paper (arXiv URL, PDF, DOI or title) and wants to grasp it quickly, screen it, or post a short summary.
- The user asks for a brief, digest, summary or short read of a paper.
- Not for broad topics without a single paper (use `graduate-lecture`), and not for surveys of many papers.

## Length budget

- Target 1,200 to 2,000 words of prose, which is 5 to 9 minutes at about 230 words per minute. Hard limit 2,300 words.
- Count words outside code and Mermaid fences. The self-check below computes it.
- When over budget, cut in this order: extra context in Key findings, the fourth and later trust points, Further reading, then wording. Never cut the Summary, the core idea diagram, or the location of a finding.

## File structure

Line 1 is `# <Title>`: plain text only, no math, no Markdown, no dashes. Lead with the object studied, for example `# Visual Steering in Vision-Language Models`. The importer turns it into the post title and slug and removes it from the content. It is the only `#` heading. Every other heading is `##` or `###`, in sentence case, with plain words only (no math, no HTML), because `##` headings form the table of contents.

Use exactly these sections, in this order:

```text
# <Title>

## Summary
## The core idea
## Key findings
## How far to trust it
## Where it fits
## Check yourself
## References
```

### Summary (about 30 seconds)

- 3 to 5 sentences: the question, the method, the main result, the main limit. Give the single most striking number.
- End with one bold line that starts `**Reading the original.**` and gives a verdict: skip it, read only named parts (for example "Figure 1 and Section 3.4"), or read it in full, with a reason in one clause.

### The core idea (about 2 minutes)

- One paragraph on what the paper does that earlier work did not, named precisely (the new measurement, the new mechanism, the new setup). Cite the prior work it departs from as (Author, year).
- Exactly one Mermaid diagram of the method or mechanism, followed by one or two sentences that read the diagram.
- At most one display equation, and only when the paper's idea is the equation (a loss, a metric, an estimator). Define every symbol in the sentence after it.

### Key findings (about 3 minutes)

- A numbered list of 4 to 6 findings, most important first.
- Each item: a bold one-sentence claim, then one or two sentences of evidence with the paper's own numbers, then the location in parentheses: `(Fig. 1B)`, `(Table 2)`, `(Section 3.4)`, `(Appendix B.6)`.
- A finding without a location in the paper does not go in this list.
- Prefer a small comparison table over prose when 3 or more findings share the same columns (model, condition, number).

### How far to trust it (1 to 2 minutes)

- 2 to 4 points. Each point opens with one of two bold labels:
  - `**Stated by the authors.**` for limits the paper itself acknowledges, with location.
  - `**Added in this brief.**` for limits found while writing the brief. Each must be checkable: a calculation that was run (state the result), an inconsistency between two located numbers, or a cited source.
- Typical checks worth running: sample sizes and what they can resolve, chance baselines, selection over many conditions, missing controls, whether a headline number is a maximum or an average, and whether reported percentages agree with reported counts.
- End with one sentence on which result is most solid and which is weakest.

### Where it fits (about 1 minute)

- 2 or 3 related works, one sentence each on how they relate (precedes, contradicts, extends), cited as (Author, year).
- One sentence on the open question the paper leaves.
- One sentence pointing to the parts of the original worth reading for depth, by section or figure.

### Check yourself

- Exactly 3 questions, each followed by its answer, in the format below. Answers are 1 to 3 sentences.
- Questions need reasoning, not recall: one about the core idea, one about interpreting a number, one about a misreading or limit.

```markdown
**Q1. Why does the paper match caption length to the image's token count?**

**Answer.** Prompt length alone could shift behavior. Matching it leaves modality as the only difference between the two conditions.
```

### References

- The paper first, with authors, year, title verbatim, venue or arXiv ID and URL.
- Then only the works cited in the brief. Usually 3 to 7 entries in total.

## Voice rules

1. Neutral person: "the paper", "the authors", "the reader", the imperative. Never "I" or "you". Call the file a "brief" or a "post".
2. Define every acronym and term at first use, in the same sentence. No glossary table unless more than 5 terms need defining, and then at most 6 rows directly under the Summary.
3. Every number comes from the paper (with location) or from a calculation that was run. Never estimate in your head and never invent a figure, citation or quotation.
4. Separate the paper's claims from the brief's judgments. Paper claims are attributed ("the authors report"); the brief's own judgments live in "How far to trust it" under the "Added in this brief" label.
5. Plain sentences of varied length. Use commas, colons, "to" and "·". Never use em dashes or en dashes.
6. Banned words and phrases: landscape, journey, delve, unlock, seamless, robust, powerful, monumental, revolutionary, game-changer, incredibly, crucial, "deep dive", "Ever wondered", "Picture this", "In this post we will", "Let's dive", "Now go", and exclamation marks outside code. Replace a banned word that carries meaning with the precise claim. Paper titles in References stay verbatim.
7. Cite in text as (Author, year). No bare `[n]` markers and no footnotes.
8. No emojis. Bold only the finding claims, the trust labels, the Reading-the-original line and the Q and A labels.

## Formatting rules for the importer

- Content renders with GFM, KaTeX, Shiki code fences and Mermaid fences. Raw HTML is dropped: never use `<details>`, `<br/>` in prose, or any other tag.
- Math: inline `$...$`; display math with `$$` alone on the lines above and below. Never use `\eqref`, `\ref`, `\label`, `\newcommand`, `\def`. Escape a literal dollar sign as `\$`. Inside a table cell, write absolute values as `\lvert x \rvert`, never with a bare `|`.
- Mermaid: double quotes around every node and edge label, no double quotes inside labels, no HTML except `<br/>` inside labels, no LaTeX, no underscores, no `classDef`, `style`, `linkStyle`, `:::class` or `%%{init}%%`. Prefer `flowchart TB`. Never use a single capital `I` as a node id.
- Code fences always name a language (`text` for plain output).

## Workflow

1. **Get the full text.** For arXiv, fetch the abstract page for title, authors, date and categories, then the HTML full text (`https://arxiv.org/html/<id>`), continuing with the offset until the whole paper and its appendices are read. Fall back to the PDF when no HTML exists. Do not write from the abstract alone.
2. **Extract.** List the paper's research questions, method, every headline number with its location, the controls, and the limits the authors state. Note related work the paper positions itself against.
3. **Choose.** Pick the one idea that the Summary and the core idea diagram must carry, and the 4 to 6 findings that support it. Everything else is left out, however interesting.
4. **Check.** Run every non-trivial calculation the brief will state (chance rates, confidence intervals, consistency of counts and percentages) in Python, and keep the outputs. Search the web for any related-work fact that is not in the paper.
5. **Write** the file with Write to `<topic-slug>-brief.md`.
6. **Self-check** with the script below and fix every hit. Then read the file once as a reader would: each finding has a location, each "Added in this brief" point is checkable, the Summary alone states the idea correctly.
7. **Deliver** the file with the file-delivery tool available (SendUserFile, present_files or an attachment).
8. **Reply** in the language the user wrote in, briefly: word count and reading time, the Reading-the-original verdict, a proposed dek (one or two plain sentences, at most 50 words, not the title verbatim, no hook), and whether the paper looks worth a full `graduate-lecture` post. Do not repeat the brief in chat.

## Self-check

```bash
f=<file>-brief.md
head -1 "$f"                                   # "# <Title>", plain text
grep -c '^# ' "$f"                             # 1
for s in 'Summary' 'The core idea' 'Key findings' 'How far to trust it' 'Where it fits' 'Check yourself' 'References'; do
  printf '%-22s %s\n' "$s" "$(grep -c "^## $s\$" "$f")"   # each 1
done
grep -c '^\*\*Reading the original\.\*\*' "$f"   # 1
# prose word count and reading time, fences excluded: target 1200 to 2000, limit 2300
w=$(awk '/^```/{c=!c;next} !c' "$f" | wc -w); echo "words=$w minutes=$((w/230))"
grep -c '```mermaid' "$f"                      # 1, at most 2
grep -c '^\$\$' "$f"                           # 0 or 2 (one display equation)
# every finding carries a location in the paper
awk '/^## Key findings/{k=1;next} /^## /{k=0} k && /^[0-9]+\. /{n++; if ($0 !~ /(Fig\.|Figure|Table|Section|Appendix|Sec\.|Eq\.)/) print "no location: " NR} END{print "findings=" n}' "$f"   # 4 to 6, no misses
grep -c '^\*\*Stated by the authors\.\*\*\|\*\*Added in this brief\.\*\*' "$f"   # 2 to 4
grep -c '^\*\*Q[0-9]\.' "$f"; grep -c '^\*\*Answer\.\*\*' "$f"   # 3 and 3
grep -nE '—|–' "$f"                            # no em or en dashes
awk '/^```/{c=!c;next} !c && /!/ {print NR": "$0}' "$f"   # exclamation marks (\! in math excepted)
grep -niE 'landscape|journey|delve|unlock|seamless|robust|powerful|monumental|revolutionary|game.changer|incredibly|crucial|deep dive|ever wondered|picture this|in this post we will|let.s dive|now go' "$f"   # titles in References excepted
grep -nE '\[[0-9]+\]' "$f"                     # no bare numeric citations
grep -nwiE 'you|your' "$f"; grep -nwE 'I' "$f" # neutral person; quoted prompts must be paraphrased
grep -nE '\\eqref|\\label|\\newcommand|\\def|<sub>|<sup>|<details>' "$f"
awk '/```mermaid/{m=1;next} /```/{m=0} m && /_|classDef|style |%%\{/' "$f"
```

## Revisions

- "Too long": cut in the order given under Length budget, then rerun the self-check.
- "Too shallow" or "I still do not get it": rewrite the core idea paragraph and diagram first; do not add sections. If the user wants depth beyond the budget, offer `graduate-lecture`.
- A broken diagram or formula: fix it with plain text and Unicode under the formatting rules, not with another markup trick.
- Edit the existing file in place, rerun the self-check and resend it.