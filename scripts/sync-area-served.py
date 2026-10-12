#!/usr/bin/env python3
"""
Writes the one served list, AREA_SERVED in scripts/audit.py, into the
shared business node of every page under docs/. proposed-changes.md 3.79.
And the shop's profiles, SAME_AS, since 3.97.

WHY A SCRIPT. The business node repeats in full on every page, and a list
typed into 26 pages is 26 chances for one of them to drift. That is how
Jamison had a page and was missing from the list every page carried (the
3.62 open item). Here the list lives once, this writes it everywhere, and
scripts/audit.py fails any page whose node says otherwise.

SINCE 3.97 IT ALSO WRITES sameAs, from SAME_AS in scripts/audit.py, the
shop's profiles, placed directly after the node's hasMap because the list
opens on that same Maps URL. One script, because both are the business
node's one-list fields and a second script would be a second thing to
forget to run.

WHAT IT TOUCHES. Only the areaServed and sameAs of a node whose @type is a
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
    profiles = list(audit.SAME_AS)

    def with_same_as(n: dict) -> dict:
        """The node with sameAs directly after hasMap (at the end if the
        node has none), every other key in its own order."""
        out = {}
        for k, v in n.items():
            if k == "sameAs":
                continue
            out[k] = v
            if k == "hasMap":
                out["sameAs"] = profiles
        out.setdefault("sameAs", profiles)
        return out

    def one(m):
        body = m.group(2)
        data = json.loads(body)
        if reserialise(body, data) != body:
            raise SystemExit("FAILED: a JSON-LD block does not round-trip byte for byte, so "
                             "rewriting it would change more than its areaServed and sameAs. "
                             "Nothing written.")
        items = data if isinstance(data, list) else [data]
        def is_business(n) -> bool:
            t = n.get("@type") if isinstance(n, dict) else None
            types = t if isinstance(t, list) else [t]
            return bool(audit.LOCAL_BUSINESS_TYPES.intersection(x for x in types if isinstance(x, str)))

        for it in items:
            if not isinstance(it, dict):
                continue
            graph = it.get("@graph")
            nodes = graph if isinstance(graph, list) else [it]
            for i, n in enumerate(nodes):
                if is_business(n):
                    n["areaServed"] = want
                    fixed = with_same_as(n)
                    n.clear()
                    n.update(fixed)
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
            print(f"{len(stale)} page(s) carry a served list or profiles that are not "
                  f"AREA_SERVED and SAME_AS:")
            for p in stale:
                print(f"  {p}")
            print("Run scripts/sync-area-served.py.")
            return 1
        print(f"Every page's business node carries AREA_SERVED ({len(audit.AREA_SERVED)} places) "
              f"and SAME_AS ({len(audit.SAME_AS)} profiles).")
        return 0
    print(f"wrote {len(stale)} page(s)" + ("" if not stale else ":"))
    for p in stale:
        print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
