---
name: "paper-brief"
description: "Use when the user wants a short read of a paper (arXiv link, PDF or title): an importable English Markdown brief, 5 to 10 minutes long, with core idea, located findings, trust check."
---

# Paper Brief

Turn one research paper into a brief that a reader finishes in 5 to 10 minutes and still holds the paper's idea, its evidence and how far to trust it. The output is a single English Markdown file that imports directly into the blog's post editor ("Import .md") and renders without edits.

The brief is layered. Each section is useful on its own, so a reader who stops after the Summary or after the core idea still leaves with something correct. The reader should never need the original paper to understand the brief, and the brief tells them exactly which parts of the original are worth opening.

The reader to write for is curious and technical but has not read this paper and does not work in its subfield. The writer has just read the whole paper, so every term feels obvious to them; that is the main way a brief fails. A brief that covers less and is understood beats one that covers more and is not. When a rule below and the length budget collide, drop a finding, a name or a number, never the explanation of what is kept.

The brief follows the Curiosities voice of the site (repository skill `curiosities-voice` in `dangvngiang.dev`). If that skill and this one ever disagree on voice or formatting, the repository skill wins. For a full lecture-style post on the same paper, use `graduate-lecture` instead; this skill is the short format and is often the screening step before it.

## When to use

- The user gives a paper (arXiv URL, PDF, DOI or title) and wants to grasp it quickly, screen it, or post a short summary.
- The user asks for a brief, digest, summary or short read of a paper.
- Not for broad topics without a single paper (use `graduate-lecture`), and not for surveys of many papers.

## Length budget

- Target 1,200 to 2,000 words of prose, which is 5 to 9 minutes at about 230 words per minute. Hard limit 2,300 words.
- Count words outside code and Mermaid fences. The self-check below computes it. The site counts slightly more (about 5 percent, since it also counts table cells and link text differently), so stay at or under 2,100 by the self-check count.
- When over budget, cut in this order: the fifth finding, extra context in Key findings, the third trust point, the third related work, then wording. Never cut the Summary, the worked instance, the core idea diagram, a definition, or the location of a finding.

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

- The first sentence names the paper: authors (first author and "colleagues" when there are more than two), year, and the paper's title verbatim, linked to its abstract page, for example `Smith and colleagues (2025), in [Seeing Is Not Saying](https://arxiv.org/abs/2501.01234), ask whether ...`. Use the `arxiv.org/abs/` link, not the HTML or PDF link.
- Then 3 to 5 sentences: the question, why it matters to someone outside the subfield (one sentence), the method, the main result, the main limit.
- Give the single most striking number with its unit, its scale and a reference point (the previous best, a naive baseline or chance), so the reader can tell whether it is large. "From 2.3716 to 2.3713, where 3 is the schoolbook method and 2 is the floor" carries meaning; "to 2.3713" does not.

### The core idea (about 2 minutes)

- One paragraph on what the paper does that earlier work did not, named precisely (the new measurement, the new mechanism, the new setup). Cite the prior work it departs from as (Author, year).
- One worked instance: a single concrete input, what the method does to it step by step, and what comes out. Take it from the paper (a figure, an example, an appendix case) or build it from the paper's definitions; never invent behaviour the paper does not report.
- Exactly one Mermaid diagram of the method or mechanism, followed by one or two sentences that read the diagram. Every label in the diagram uses only words the prose has already explained.
- At most one display equation, and only when the paper's idea is the equation (a loss, a metric, an estimator). Define every symbol in the sentence after it.

### Key findings (about 3 minutes)

- A numbered list of 4 or 5 findings, most important first.
- Each item: a bold one-sentence claim, then one or two sentences of evidence with the paper's own numbers, then the location in parentheses: `(Fig. 1B)`, `(Table 2)`, `(Section 3.4)`, `(Appendix B.6)`. When the paper has an arXiv HTML version, link the location to its anchor, for example `([Table 2](https://arxiv.org/html/2501.01234#S4.T2))`.
- At most 3 numbers per finding. When more numbers are needed, use a small table, and prefer a table anyway when 3 or more findings share the same columns (model, condition, number).
- Every number says what it measures and which direction is better the first time its metric appears.
- A finding without a location in the paper does not go in this list.

### How far to trust it (1 to 2 minutes)

- 2 or 3 points. Each point opens with one of two bold labels (any mix; use `Stated by the authors` whenever the paper states a limit worth passing on):
  - `**Stated by the authors.**` for limits the paper itself acknowledges, with location.
  - `**Added in this brief.**` for limits found while writing the brief. Each must be checkable: a calculation that was run (state the result), an inconsistency between two located numbers, or a cited source.
- Each point tests a claim the brief has already stated above. Restate that claim in a few words first ("The 40 percent gain in finding 2 ..."). Never critique a number, table, survey or experiment the reader has not met. New numbers are allowed only when they break down that claim (the per-dataset values behind an average stated above).
- Give the conclusion in plain words first, then the check in one clause: "Three of the twelve wins could be chance (a binomial test on 12 trials gives p = 0.07)". Use no coefficient names, test names or symbols the body has not defined; name the test only as the source of the number.
- Typical checks worth running: sample sizes and what they can resolve, chance baselines, selection over many conditions, missing controls, whether a headline number is a maximum or an average, and whether reported percentages agree with reported counts.
- End with one sentence on which result is most solid and which is weakest.

### Where it fits (about 1 minute)

- 2 or 3 related works, one sentence each on how they relate (precedes, contradicts, extends), cited as (Author, year).
- One sentence on the open question the paper leaves.
- End with one bold line that starts `**Reading the original.**` and gives a verdict: skip it, read only named parts (for example "To go further, read Figure 1 and Section 3.4"), or read it in full, with a reason in one clause. Do not write "for depth": several papers use depth as a technical term.

### Check yourself

- Exactly 3 questions, each followed by its answer, in the format below. Answers are 1 to 3 sentences.
- Questions need reasoning, not recall: one about the core idea, one about interpreting a number, one about a misreading or limit.
- Every number, term and fact in a question or an answer already appears in the body. The quiz tests the brief; it never introduces new material.

```markdown
**Q1. Why does the paper match caption length to the image's token count?**

**Answer.** Prompt length alone could shift behavior. Matching it leaves modality as the only difference between the two conditions.
```

### References

- The paper first, with authors, year, title verbatim, venue or arXiv ID and URL.
- Then only the works cited in the brief. Usually 3 to 9 entries in total.

## Voice rules

1. Neutral person: "the paper", "the authors", "the reader", the imperative. Never "I" or "you". Call the file a "brief" or a "post".
2. Expanding an acronym is not defining it. At first use, say what the thing is or does in plain words, in the same sentence; for a metric, also its scale and which direction is better ("mIoU, the overlap between predicted and true regions, from 0 to 100, higher is better"). The same holds for every named benchmark, dataset, model and prior method: give a gloss of 3 to 10 words, or describe it and drop the name. Name at most 8 such things in the prose, not counting the paper's own system and the model it is built on; names that appear only in a table still need a gloss in the table or the sentence above it. When the paper uses a metric without defining it, take the definition from the work that introduced it and cite that work. No glossary table unless more than 5 terms need defining, and then at most 6 rows directly under the Summary.
3. One meaning per term and one unit per quantity. If a word has a technical sense in the paper ("specialist", "tensor", "depth"), never use it in a second sense. State a change either in percent or in points, not both. The dek agrees with the Summary's definitions, and neither states as fact a claim that "How far to trust it" disputes; attribute it to the authors or leave it out. When the same result is stated two ways, say they are the same result. Arithmetic that does not match the paper's own count (a 5 x 9 x 6 grid that the paper calls 260 runs) is explained or left out.
4. Every number comes from the paper (with location) or from a calculation that was run. A value read off a plot is approximate: say so ("about 250, read from Fig. 2"), and never derive a precise ratio from such readings. Never estimate in your head and never invent a figure, citation or quotation.
5. Separate the paper's claims from the brief's judgments. Paper claims are attributed ("the authors report"); the brief's own judgments live in "How far to trust it" under the "Added in this brief" label.
6. Plain sentences of varied length. Use commas, colons, "to" and "·". Never use em dashes or en dashes.
7. Banned words and phrases: landscape, journey, delve, unlock, seamless, robust, powerful, monumental, revolutionary, game-changer, incredibly, crucial, "deep dive", "Ever wondered", "Picture this", "In this post we will", "Let's dive", "Now go", and exclamation marks outside code. Replace a banned word that carries meaning with the precise claim. Paper titles in References stay verbatim.
8. Cite in text as (Author, year). No bare `[n]` markers and no footnotes.
9. No emojis. Bold only the finding claims, the trust labels, the Reading-the-original line and the Q and A labels.

## Formatting rules for the importer

- Content renders with GFM, KaTeX, Shiki code fences and Mermaid fences. Raw HTML is dropped: never use `<details>`, `<br/>` in prose, or any other tag.
- Links: only `arxiv.org`, `doi.org` and `aclanthology.org` hosts. The site's draft check rejects other hosts, GitHub included.
- Math: inline `$...$`; display math with `$$` alone on the lines above and below. Never use `\eqref`, `\ref`, `\label`, `\newcommand`, `\def`. Escape a literal dollar sign as `\$`. Inside a table cell, write absolute values as `\lvert x \rvert`, never with a bare `|`.
- Mermaid: double quotes around every node and edge label, no double quotes inside labels, no HTML except `<br/>` inside labels, no LaTeX, no underscores, no `classDef`, `style`, `linkStyle`, `:::class` or `%%{init}%%`. Prefer `flowchart TB`. Never use a single capital `I` as a node id.
- Code fences always name a language (`text` for plain output).

## Workflow

1. **Get the full text.** For arXiv, fetch the abstract page for title, authors, date and categories, then the HTML full text (`https://arxiv.org/html/<id>`), continuing with the offset until the whole paper and its appendices are read. Note the HTML anchor of each figure, table and section you may cite. Fall back to the PDF when no HTML exists. Do not write from the abstract alone.
2. **Extract.** List the paper's research questions, method, every headline number with its location, the controls, and the limits the authors state. Note related work the paper positions itself against, and one concrete example the paper works through.
3. **Choose.** Pick the one idea that the Summary and the core idea diagram must carry, the worked instance, and the 4 or 5 findings that support it. Everything else is left out, however interesting. Every term the chosen material needs must be explainable inside the budget; if it is not, choose other material.
4. **Check.** Run every non-trivial calculation the brief will state (chance rates, confidence intervals, consistency of counts and percentages) in Python, and keep the outputs. Search the web for any related-work fact that is not in the paper.
5. **Write** the file with Write to `<topic-slug>-brief.md`, and draft the dek (one or two plain sentences, at most 50 words, not the title verbatim, no hook) in the same pass so it uses the Summary's definitions.
6. **Self-check** with the script below and fix every hit.
7. **Cold-reader review.** The writer cannot see the brief fresh, so get someone who can. When a subagent tool is available, start one subagent with a fresh context and give it only the brief's text and the dek: not the paper, not your notes, not this skill. Ask it: "You have not read the paper this brief summarises. List every term, name, symbol, number or step you cannot interpret from the brief alone, every place where the brief contradicts itself, and every question or answer under Check yourself that uses something the body never said. Quote each item and say why it blocks you. Do not suggest content." Fix each item, then run one more round at most. When no subagent tool is available, re-read the brief top to bottom against the checklist below and report that the review was done without a subagent.
   - Each acronym, metric, benchmark, dataset, model and prior method has a plain gloss at first use.
   - The worked instance follows one concrete input from start to end.
   - Every trust point names a claim made earlier in the brief.
   - Every number in Check yourself appears in the body.
   - No term carries two meanings; no quantity switches between percent and points.
8. **Deliver** the file with the file-delivery tool available (SendUserFile, present_files or an attachment).
9. **Reply** in the language the user wrote in, briefly: word count and reading time, the Reading-the-original verdict, the dek, the number of cold-reader rounds and any item left open, and whether the paper looks worth a full `graduate-lecture` post. Do not repeat the brief in chat.

## Self-check

Lines marked "review" are heuristics: look at each hit and fix the ones that are real, but a hit alone is not a failure.

```bash
f=<file>-brief.md
head -1 "$f"                                   # "# <Title>", plain text
grep -c '^# ' "$f"                             # 1
for s in 'Summary' 'The core idea' 'Key findings' 'How far to trust it' 'Where it fits' 'Check yourself' 'References'; do
  printf '%-22s %s\n' "$s" "$(grep -c "^## $s\$" "$f")"   # each 1
done
# Summary's first paragraph links the paper's abstract page
awk '/^## Summary/{s=1;next} s && NF{print; exit}' "$f" | grep -c 'https://arxiv\.org/abs/'   # 1 (0 only for a non-arXiv paper with a doi.org link)
# Reading the original sits under Where it fits
awk '/^## /{sec=$0} /^\*\*Reading the original\.\*\*/{print sec}' "$f"   # "## Where it fits", once
grep -niE '(for|in) depth[,. ]+(read|see|look)' "$f"   # none ("To go further, read")
# prose word count and reading time, fences excluded: target 1200 to 2000, limit 2300
w=$(awk '/^```/{c=!c;next} !c' "$f" | wc -w); echo "words=$w minutes=$((w/230))"   # at most 2100
grep -c '```mermaid' "$f"                      # 1
grep -c '^\$\$' "$f"                           # 0 or 2 (one display equation)
# every finding carries a location in the paper
awk '/^## Key findings/{k=1;next} /^## /{k=0} k && /^[0-9]+\. /{n++; if ($0 !~ /(Fig\.|Figure|Table|Section|Appendix|Sec\.|Eq\.)/) print "no location: " NR} END{print "findings=" n}' "$f"   # 4 or 5, no misses
grep -c '^\*\*Stated by the authors\.\*\*\|\*\*Added in this brief\.\*\*' "$f"   # 2 or 3
grep -c '^\*\*Q[0-9]\.' "$f"; grep -c '^\*\*Answer\.\*\*' "$f"   # 3 and 3
grep -nE '—|–' "$f"                            # no em or en dashes
awk '/^```/{c=!c;next} !c && /!/ {print NR": "$0}' "$f"   # exclamation marks (\! in math excepted)
grep -niE 'landscape|journey|delve|unlock|seamless|robust|powerful|monumental|revolutionary|game.changer|incredibly|crucial|deep dive|ever wondered|picture this|in this post we will|let.s dive|now go' "$f"   # titles in References excepted
grep -nE '\[[0-9]+\]' "$f"                     # no bare numeric citations
grep -nwiE 'you|your' "$f"; grep -nwE 'I' "$f" # neutral person; quoted prompts must be paraphrased
grep -nF -e '\eqref' -e '\label' -e '\newcommand' -e '\def' -e '<sub>' -e '<sup>' -e '<details>' "$f"
awk '/```mermaid/{m=1;next} /```/{m=0} m && /_|classDef|style |%%\{/' "$f"
grep -noE 'https?://[^/)]+' "$f" | grep -vE '//(www\.)?(arxiv\.org|doi\.org|aclanthology\.org)$'   # no other link hosts
# review: numbers in Check yourself that never appear before it
awk '/^## Check yourself/{q=1} /^## References/{q=0} {gsub(/[^0-9.,]+/," "); n=split($0,a," "); for(i=1;i<=n;i++){x=a[i]; sub(/[.,]+$/,"",x); if(x ~ /[0-9]/){ if(q && !(x in seen)) print "quiz-only number: " x; if(!q) seen[x]=1 }}}' "$f"
# review: findings carrying more than 3 numbers
awk '/^## Key findings/{k=1;next} /^## /{k=0} k && /^[0-9]+\. /{t=$0; gsub(/\]\([^)]*\)/,"]",t); gsub(/\([^()]*\)/,"",t); gsub(/\$[^$]*\$/,"#",t); c=gsub(/[0-9]+([.,][0-9]+)?/,"",t); if(c>4) print "numbers=" c-1 ": " substr($0,1,60)}' "$f"   # math counts as one
# review: acronyms; each needs a plain gloss at its first use
sed -E 's/\]\([^)]*\)/]/g; s#https?://[^ )]+##g' "$f" | grep -oE '\b[A-Z][A-Za-z]*[A-Z][A-Za-z0-9-]*\b' | sort | uniq -c | sort -rn | head -30
```

## Revisions

- "Too long": cut in the order given under Length budget, then rerun the self-check.
- "Too shallow" or "I still do not get it": rewrite the core idea paragraph, the worked instance and the diagram first; do not add sections. If the user wants depth beyond the budget, offer `graduate-lecture`.
- A broken diagram or formula: fix it with plain text and Unicode under the formatting rules, not with another markup trick.
- Edit the existing file in place, rerun the self-check and resend it.
