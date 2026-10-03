"""Validate the tracked paper collection, index, and declared primary identities."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


ID_PATTERN = re.compile(r"(?<![\w.])(\d{4}\.\d{4,5})(?:v\d+)?(?![\w])", re.I)
PRIMARY_LABEL = re.compile(r"^(?:arxiv(?:\s+id)?|paper\s+id)\s*:\s*(.*)$", re.I)
HEADING = re.compile(r"^(#{2,6})\s+(.+?)\s*#*\s*$")
REFERENCE_HEADING = re.compile(r"\b(?:references?|bibliography|related\s+(?:work|papers?|resources?))\b", re.I)
MARKDOWN_LINK = re.compile(r"\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\s*\)")
TOPICS = frozenset({
    'artificial-intelligence', 'computer-vision', 'llm-agents-dev',
    'machine-learning', 'natural-language-processing', 'robotics', 'systems', 'xai',
})


def primary_identity(text: str) -> tuple[str | None, list[str]]:
    """Read primary declarations outside code blocks and reference sections."""
    identities: set[str] = set()
    errors: list[str] = []
    headings: list[tuple[int, bool]] = []
    fence: str | None = None
    declarations = 0
    for line_number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        fence_match = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_match:
            marker = fence_match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is not None:
            continue
        heading = HEADING.match(stripped)
        if heading:
            level = len(heading.group(1))
            while headings and headings[-1][0] >= level:
                headings.pop()
            headings.append((level, bool(REFERENCE_HEADING.search(heading.group(2)))))
            continue
        if any(blocked for _, blocked in headings):
            continue
        plain = re.sub(r"\*\*|__", '', stripped)
        plain = re.sub(r"^[-+*]\s+", '', plain)
        declaration = PRIMARY_LABEL.match(plain)
        if not declaration:
            continue
        found = set(ID_PATTERN.findall(declaration.group(1)))
        # A generic arXiv repository link is a resource, not an ID declaration.
        if re.match(r'^arxiv\s*:', plain, re.I) and not found:
            continue
        declarations += 1
        if len(found) != 1:
            errors.append(f'line {line_number}: malformed or conflicting primary ID declaration')
        identities.update(found)
    if declarations == 0:
        errors.append('missing primary ArXiv ID or Paper ID declaration')
    elif len(identities) != 1:
        errors.append('conflicting primary identities: ' + ', '.join(sorted(identities)))
    return (next(iter(identities)) if len(identities) == 1 and not errors else None), errors


def validate_collection(root: Path, tracked: list[str]) -> tuple[list[str], int, int]:
    """Return actionable errors plus paper and index counts; never rewrite files."""
    papers = sorted(p for p in tracked if p.endswith('.md') and p.split('/')[0] in TOPICS)
    paper_set = set(papers)
    errors: list[str] = []
    index_path = root / 'INDEX.md'
    if not index_path.is_file():
        return ['INDEX.md: missing index'], len(papers), 0
    links: list[str] = []
    for target in MARKDOWN_LINK.findall(index_path.read_text(encoding='utf-8-sig')):
        target = target.removeprefix('<').removesuffix('>')
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        path = unquote(parsed.path)
        if path.endswith('.md'):
            links.append(path.removeprefix('./'))
    counts = Counter(links)
    for path, count in sorted(counts.items()):
        if count > 1:
            errors.append(f'INDEX.md: repeated index path ({count} entries): {path}')
        if path not in paper_set or not (root / path).is_file():
            errors.append(f'INDEX.md: untracked or missing paper target: {path}')
    for path in sorted(paper_set - counts.keys()):
        errors.append(f'INDEX.md: paper not indexed: {path}')
    identities: dict[str, list[str]] = defaultdict(list)
    for path in papers:
        file = root / path
        if not file.is_file():
            errors.append(f'{path}: tracked paper is missing from the working tree')
            continue
        identity, identity_errors = primary_identity(file.read_text(encoding='utf-8-sig'))
        errors.extend(f'{path}: {error}' for error in identity_errors)
        if identity:
            identities[identity].append(path)
    for identity, paths in sorted(identities.items()):
        if len(paths) > 1:
            errors.append(f'duplicate primary ArXiv ID {identity}: ' + ', '.join(paths))
    return errors, len(papers), len(links)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        tracked = subprocess.check_output(
            ['git', 'ls-files', '-z'], cwd=root).decode('utf-8').rstrip('\0').split('\0')
        errors, papers, links = validate_collection(root, tracked)
    except (OSError, UnicodeError, subprocess.CalledProcessError) as exc:
        print(f'ERROR: cannot validate collection: {exc}', file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print('ERROR: ' + error, file=sys.stderr)
        return 1
    print(f'OK: {links} unique INDEX links = {papers} paper files; every primary identity is present and unique.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
