#!/usr/bin/env python3
"""
Writes the one served list, AREA_SERVED in scripts/audit.py, into the
shared business node of every page under docs/. proposed-changes.md 3.79.

WHY A SCRIPT. The business node repeats in full on every page, and a list
typed into 26 pages is 26 chances for one of them to drift. That is how
Jamison had a page and was missing from the list every page carried (the
3.62 open item). Here the list lives once, this writes it everywhere, and
scripts/audit.py fails any page whose node says otherwise.

WHAT IT TOUCHES. Only the areaServed array of a node whose @type is a
LocalBusiness type. Every other node, including a Service node's own
areaServed (a town page names its town there), is left as it is.

HOW IT WRITES. Each JSON-LD block is parsed, the array replaced, and the
block serialised again with json.dumps(indent=2, ensure_ascii=False) under
the block's own leading indentation. Every block on the site round-trips
byte for byte through exactly that (tested on all 24 when this was
written), so the only bytes that change are the list's.

    python3 scripts/sync-area-served.py           # write every page
    python3 scripts/sync-area-served.py --check   # exit 1 if any page is out of date
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK_RE = re.compile(r'(?s)(<script type="application/ld\+json">)(.*?)(</script>)')


def reserialise(body: str, data) -> str:
    """The block as json.dumps writes it, under the block's own indentation
    and with its own leading and trailing whitespace."""
    first = body.lstrip("\n")
    indent = re.match(r"[ ]*", first).group(0)
    out = "\n".join(indent + line for line in
                    json.dumps(data, indent=2, ensure_ascii=False).splitlines())
    head = body[:len(body) - len(body.lstrip("\n"))]
    tail = body[len(body.rstrip()):]
    return head + out + tail


def synced(html: str) -> str:
    want = audit.area_served_nodes()

    def one(m):
        body = m.group(2)
        data = json.loads(body)
        if reserialise(body, data) != body:
            raise SystemExit("FAILED: a JSON-LD block does not round-trip byte for byte, so "
                             "rewriting it would change more than its areaServed. Nothing written.")
        items = data if isinstance(data, list) else [data]
        nodes = []
        for it in items:
            nodes.extend(it.get("@graph", [it]) if isinstance(it, dict) else [])
        for n in nodes:
            t = n.get("@type")
            types = t if isinstance(t, list) else [t]
            if audit.LOCAL_BUSINESS_TYPES.intersection(x for x in types if isinstance(x, str)):
                n["areaServed"] = want
        return m.group(1) + reserialise(body, data) + m.group(3)

    return BLOCK_RE.sub(one, html)


def main() -> int:
    check = "--check" in sys.argv[1:]
    stale = []
    for path in sorted(glob.glob(os.path.join(ROOT, "docs", "**", "index.html"), recursive=True)):
        with open(path, encoding="utf-8") as f:
            html = f.read()
        new = synced(html)
        if new != html:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
    if check:
        if stale:
            print(f"{len(stale)} page(s) carry a served list that is not AREA_SERVED:")
            for p in stale:
                print(f"  {p}")
            print("Run scripts/sync-area-served.py.")
            return 1
        print(f"Every page's business node carries AREA_SERVED ({len(audit.AREA_SERVED)} places).")
        return 0
    print(f"wrote {len(stale)} page(s)" + ("" if not stale else ":"))
    for p in stale:
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
