# Claude Instructions

When adding, removing, renaming, or moving paper summary Markdown files, keep [INDEX.md](INDEX.md) up to date.

## Paper identity

- Confirm the paper's title, authors, and submission date against its primary source.
- Before adding a summary, search the topic directories and open PRs for its base arXiv ID, with the version suffix removed. Update the existing summary or pending submission when the paper is already covered.
- Declare the primary paper near the title using `**ArXiv ID:** [ID](https://arxiv.org/abs/ID)`. Related-work citations identify other papers and are separate from this declaration.
- Preserve the canonical path when enriching an existing summary. Include only source-supported measurements and working resource links.
- Stage new summaries and index changes, then run `python scripts/validate_papers.py`. Every tracked summary must have one consistent primary identity and exactly one index entry.

## Index maintenance

- Add new paper summaries to the correct topic or subtopic section in `INDEX.md`.
- Update links if files are renamed or moved.
- Remove entries for deleted summary files.
- Preserve the existing organization by top-level topic directory and nested subtopic directory.
- Use relative Markdown links so navigation works on GitHub.
- Keep `README.md` linked to `INDEX.md`.
