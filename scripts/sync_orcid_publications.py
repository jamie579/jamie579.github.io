#!/usr/bin/env python3
"""
Sync the Publications page from ORCID.

This script updates only the section between:
  <!-- ORCID_WORKS_START -->
  <!-- ORCID_WORKS_END -->

in `content/publications/_index.md`.

Why this exists:
- ORCID is usually the most accurate canonical list of works.
- Keeping your website in sync improves consistency across the web and helps with
  entity disambiguation (useful for Knowledge Panel/Graph signals).

Usage:
  python3 scripts/sync_orcid_publications.py
  python3 scripts/sync_orcid_publications.py --orcid 0000-0000-0000-0000
  python3 scripts/sync_orcid_publications.py --file content/publications/_index.md

Notes:
- Requires an internet connection.
- Uses the ORCID Public API (no auth) via `https://pub.orcid.org/v3.0/`.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Iterable, Optional


DEFAULT_ORCID = "0000-0003-0097-6102"
DEFAULT_FILE = "content/publications/_index.md"
START_MARKER = "<!-- ORCID_WORKS_START -->"
END_MARKER = "<!-- ORCID_WORKS_END -->"


@dataclass(frozen=True)
class OrcidWork:
    title: str
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
    journal: Optional[str]
    work_type: Optional[str]
    url: Optional[str]
    doi: Optional[str]
    doi_url: Optional[str]


def _deep_get(obj: Any, keys: Iterable[str]) -> Any:
    cur = obj
    for k in keys:
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            return None
    return cur


def _as_str(v: Any) -> Optional[str]:
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def _as_int(v: Any) -> Optional[int]:
    s = _as_str(v)
    if not s:
        return None
    try:
        return int(s)
    except ValueError:
        return None


def _extract_value_field(obj: Any) -> Optional[str]:
    # ORCID often uses {"value": "..."} wrappers.
    if isinstance(obj, dict) and "value" in obj:
        return _as_str(obj.get("value"))
    return _as_str(obj)


def _extract_title(work_summary: dict[str, Any]) -> Optional[str]:
    title_obj = work_summary.get("title")
    # Common ORCID JSON shape: title: { title: { value: "..." }, subtitle: ..., translated-title: ...}
    for path in (
        ("title", "title", "value"),
        ("title", "title"),
        ("title", "value"),
    ):
        v = _deep_get(work_summary, path)
        s = _extract_value_field(v)
        if s:
            return s
    # Fallback: some records may embed "citation" only; skip if we can't find a title.
    return None


def _extract_pub_date(work_summary: dict[str, Any]) -> tuple[Optional[int], Optional[int], Optional[int]]:
    pd = work_summary.get("publication-date") or {}
    y = _extract_value_field(_deep_get(pd, ("year", "value"))) or _extract_value_field(pd.get("year"))
    m = _extract_value_field(_deep_get(pd, ("month", "value"))) or _extract_value_field(pd.get("month"))
    d = _extract_value_field(_deep_get(pd, ("day", "value"))) or _extract_value_field(pd.get("day"))
    return (_as_int(y), _as_int(m), _as_int(d))


def _extract_external_ids(work_summary: dict[str, Any]) -> list[dict[str, Any]]:
    ext = work_summary.get("external-ids") or {}
    ids = ext.get("external-id")
    if isinstance(ids, list):
        return [x for x in ids if isinstance(x, dict)]
    if isinstance(ids, dict):
        return [ids]
    return []


def _extract_doi(work_summary: dict[str, Any]) -> tuple[Optional[str], Optional[str]]:
    for eid in _extract_external_ids(work_summary):
        t = _as_str(eid.get("external-id-type"))
        if not t or t.lower() != "doi":
            continue
        doi = _as_str(eid.get("external-id-value"))
        url = _extract_value_field(_deep_get(eid, ("external-id-url", "value"))) or _extract_value_field(
            eid.get("external-id-url")
        )
        if doi and not url:
            url = f"https://doi.org/{doi}"
        return (doi, url)
    return (None, None)


def _pick_best_summary(summaries: list[dict[str, Any]]) -> Optional[dict[str, Any]]:
    if not summaries:
        return None
    if len(summaries) == 1:
        return summaries[0]

    def key(s: dict[str, Any]) -> tuple[int, str]:
        # ORCID may provide "display-index" (lower is better).
        idx = s.get("display-index") or s.get("display-index", 999)
        try:
            idx_i = int(idx)
        except Exception:
            idx_i = 999
        t = _extract_title(s) or ""
        return (idx_i, t.lower())

    return sorted(summaries, key=key)[0]


def fetch_orcid_works(orcid: str) -> list[OrcidWork]:
    url = f"https://pub.orcid.org/v3.0/{orcid}/works"
    req = urllib.request.Request(
        url,
        headers={
            # ORCID prefers their vendor media type.
            "Accept": "application/vnd.orcid+json",
            "User-Agent": "jamiebriansmith.com publications sync (mailto:jamie@hornesmith.co.uk)",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"ORCID HTTP error {e.code} for {url}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(
            "Failed to fetch ORCID works. Check your internet connection and DNS, then try again."
        ) from e

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError("ORCID response was not valid JSON. Try again later.") from e

    groups = data.get("group")
    if not isinstance(groups, list):
        raise RuntimeError("Unexpected ORCID /works JSON structure (missing 'group').")

    works: list[OrcidWork] = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        summaries_raw = group.get("work-summary")
        summaries: list[dict[str, Any]] = []
        if isinstance(summaries_raw, list):
            summaries = [s for s in summaries_raw if isinstance(s, dict)]
        elif isinstance(summaries_raw, dict):
            summaries = [summaries_raw]

        summary = _pick_best_summary(summaries)
        if not summary:
            continue

        title = _extract_title(summary)
        if not title:
            continue

        year, month, day = _extract_pub_date(summary)
        journal = _extract_value_field(_deep_get(summary, ("journal-title", "value"))) or _extract_value_field(
            summary.get("journal-title")
        )
        work_type = _as_str(summary.get("type"))
        work_url = _extract_value_field(_deep_get(summary, ("url", "value"))) or _extract_value_field(summary.get("url"))
        doi, doi_url = _extract_doi(summary)

        works.append(
            OrcidWork(
                title=title,
                year=year,
                month=month,
                day=day,
                journal=journal,
                work_type=work_type,
                url=work_url,
                doi=doi,
                doi_url=doi_url,
            )
        )

    return works


def _section_for(work: OrcidWork) -> str:
    t = (work.work_type or "").lower()
    if t in {"journal-article", "review", "magazine-article", "newspaper-article"}:
        return "Journal articles"
    if t in {"book", "book-chapter", "edited-book"}:
        return "Books & chapters"
    return "Other outputs"


def _sort_key(work: OrcidWork) -> tuple[int, int, int, str]:
    # Sort newest-first. Missing dates go last.
    y = work.year or -1
    m = work.month or 0
    d = work.day or 0
    return (-y, -m, -d, work.title.lower())


def render_markdown(orcid: str, works: list[OrcidWork]) -> str:
    today = _dt.date.today().isoformat()
    lines: list[str] = []
    lines.append("## Academic publications (from ORCID)")
    lines.append("")
    lines.append(f"_Synced from ORCID on {today}. For the canonical record, see https://orcid.org/{orcid}._")
    lines.append("")

    sections: dict[str, list[OrcidWork]] = {}
    for w in works:
        sections.setdefault(_section_for(w), []).append(w)

    section_order = ["Journal articles", "Books & chapters", "Other outputs"]
    any_written = False

    for section in section_order:
        items = sorted(sections.get(section, []), key=_sort_key)
        if not items:
            continue
        any_written = True
        lines.append(f"### {section}")
        lines.append("")
        for i, w in enumerate(items, start=1):
            parts: list[str] = []
            if w.year:
                parts.append(f"({w.year}).")
            parts.append(w.title.rstrip(".") + ".")
            if w.journal:
                parts.append(f"*{w.journal.rstrip('.')}*.")
            link = w.doi_url or w.url
            if link:
                parts.append(link)
            lines.append(f"{i}. {' '.join(parts)}")
        lines.append("")

    if not any_written:
        lines.append("_No works returned by ORCID. If your record is private, make your works public in ORCID._")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def update_file(path: str, markdown: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Keep sitemap + structured data "dateModified" meaningful even if this sync runs
    # in CI without committing back to git.
    new_lastmod = _dt.date.today().isoformat()

    lines = content.splitlines(keepends=True)
    start_idx = None
    end_idx = None
    indent = ""

    for i, line in enumerate(lines):
        if START_MARKER in line:
            start_idx = i
            indent = line.split(START_MARKER, 1)[0]
            break

    if start_idx is None:
        raise RuntimeError(f"Start marker not found in {path}: {START_MARKER}")

    for i in range(start_idx + 1, len(lines)):
        if END_MARKER in lines[i]:
            end_idx = i
            break

    if end_idx is None:
        raise RuntimeError(f"End marker not found in {path}: {END_MARKER}")

    new_block_lines = [(indent + l + "\n") for l in markdown.splitlines()]
    new_lines = lines[: start_idx + 1] + new_block_lines + lines[end_idx:]

    with open(path, "w", encoding="utf-8") as f:
        updated = "".join(new_lines)
        updated = _update_front_matter_lastmod(updated, new_lastmod)
        f.write(updated)


def _update_front_matter_lastmod(content: str, lastmod: str) -> str:
    """Upsert `lastmod:` in YAML front matter for Hugo."""
    # Use a conservative front matter matcher (don't consume extra blank lines after the closing fence).
    m = re.match(r"(?s)\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n", content)
    if not m:
        return content

    front = m.group(1)
    rest = content[m.end() :]
    lines = front.splitlines()

    out: list[str] = []
    replaced = False
    insert_after_idx = -1

    for i, line in enumerate(lines):
        key = line.split(":", 1)[0].strip().lower()
        if key == "date":
            insert_after_idx = i
        if key == "lastmod":
            out.append(f"lastmod: {lastmod}")
            replaced = True
        else:
            out.append(line)

    if not replaced:
        insert_at = insert_after_idx + 1 if insert_after_idx >= 0 else 0
        out.insert(insert_at, f"lastmod: {lastmod}")

    new_front = "\n".join(out).rstrip() + "\n"
    return f"---\n{new_front}---\n{rest}"


def main() -> int:
    p = argparse.ArgumentParser(description="Sync publications section from ORCID.")
    p.add_argument("--orcid", default=DEFAULT_ORCID, help="ORCID iD (default: %(default)s)")
    p.add_argument("--file", default=DEFAULT_FILE, help="Publications page file to update")
    p.add_argument("--dry-run", action="store_true", help="Print generated markdown to stdout, don't edit files")
    args = p.parse_args()

    orcid = args.orcid.strip()
    # ORCID iD format: 0000-0000-0000-0000 (last digit may be X)
    if not re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", orcid):
        print(f"Invalid ORCID iD format: {orcid}", file=sys.stderr)
        return 2

    works = fetch_orcid_works(orcid)
    md = render_markdown(orcid, works)

    if args.dry_run:
        sys.stdout.write(md)
        return 0

    update_file(args.file, md)
    print(f"Updated {args.file} from ORCID ({len(works)} works).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
