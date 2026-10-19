#!/usr/bin/env python3
"""Build a BFA one pager from a content fragment.

The house style, the BFA logo and the page furniture all come from
reference/template.html. This script only drops the content in, so the styling
cannot drift and the logo cannot go missing.

Usage:
    python3 scripts/build_sheet.py \
        --title "Connected skills" \
        --subtitle "AI Brown Bag #4 · August 17, 2026 · What the reader gets" \
        --footer "BFA Global · AI Brown Bag series · session 4 of 6" \
        --content content.html \
        --out sheet.html

The content file holds the cards, in order, with a marker before each page:

    <!-- PAGE -->
    <div class="card">...</div>
    <div class="card">...</div>
    <!-- PAGE -->
    <div class="card">...</div>
    <div class="panel">...</div>

Pages use the tight spacing by default, because in practice almost every real
sheet needs it and a page that overflows puts its last line under the footer.
Use `<!-- PAGE roomy -->` for a deliberately sparse page. `<!-- PAGE tight -->`
still works and means the same as the default.

Headers, footers and "Page x of y" are generated. Do not write them yourself.

Pass --check to measure the built sheet in headless Chrome and report how much
room each page has left. Anything negative prints under the footer.
"""

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "reference" / "template.html"


def slice_template(html):
    """Return (head_through_body_open, one_page_header, tail_after_body)."""
    m = re.search(r"^(.*?<body>\n)(.*)(</body>.*)$", html, re.S | re.M)
    if not m:
        sys.exit("template.html does not have the expected <body> structure")
    head, body, tail = m.groups()

    hm = re.search(r"(  <header>.*?  </header>\n)", body, re.S)
    if not hm:
        sys.exit("template.html has no <header> block to copy the logo from")
    return head, hm.group(1), tail


def build_header(header_block, title, subtitle):
    """Reuse the template's header, swapping only the two text slots.

    The <img> carrying the embedded logo is left exactly as it is.
    """
    out = re.sub(
        r"<h1>.*?</h1>",
        "<h1>%s</h1>" % title,
        header_block,
        flags=re.S,
    )
    out = re.sub(
        r'<div class="sub">.*?</div>',
        '<div class="sub">%s</div>' % subtitle,
        out,
        flags=re.S,
    )
    return out


def check_no_furniture(content):
    """The script owns the header, footers and page divs. Reject duplicates.

    Without this a stray <footer> in the content prints twice, which is easy
    to miss on screen and obvious only once it is on paper.
    """
    banned = [
        ("<header", "the header is generated from --title and --subtitle"),
        ("<footer", "footers are generated from --footer, with page numbers"),
        ('class="page', "page divs are generated from the <!-- PAGE --> markers"),
    ]
    found = [
        "  found %s: %s" % (tag, why) for tag, why in banned if tag in content
    ]
    if found:
        sys.exit(
            "the content file must hold cards and panels only.\n"
            + "\n".join(found)
        )


def split_pages(content):
    """Split the content fragment on <!-- PAGE --> markers."""
    check_no_furniture(content)
    parts = re.split(r"<!--\s*PAGE(\s+\w+)?\s*-->", content)
    if parts[0].strip():
        sys.exit(
            "content before the first <!-- PAGE --> marker:\n  %s"
            % parts[0].strip()[:120]
        )
    pages = []
    for i in range(1, len(parts), 2):
        word = (parts[i] or "").strip().lower()
        if word not in ("", "tight", "roomy"):
            sys.exit(
                'unknown page marker "<!-- PAGE %s -->". Use <!-- PAGE --> or '
                "<!-- PAGE roomy -->." % word
            )
        pages.append((word != "roomy", parts[i + 1].strip()))
    if not pages:
        sys.exit("no <!-- PAGE --> markers found in the content file")
    return pages


CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "chromium",
    "chromium-browser",
]

PROBE = """<script>window.addEventListener('load',function(){
var mm=96/25.4,out=[];
document.querySelectorAll('.page').forEach(function(p,i){
  var r=p.getBoundingClientRect(),last=null;
  p.querySelectorAll(':scope > *').forEach(function(c){if(c.tagName!=='FOOTER')last=c;});
  if(!last){out.push('p'+(i+1)+':empty');return;}
  var used=(last.getBoundingClientRect().bottom-r.top)/mm;
  var ft=(p.querySelector('footer').getBoundingClientRect().top-r.top)/mm;
  out.push('p'+(i+1)+':'+(ft-used).toFixed(1));
});
document.title='CLEARANCE::'+out.join(',');});</script>"""


def find_chrome():
    for path in CHROME_PATHS:
        found = path if os.path.exists(path) else shutil.which(path)
        if found:
            return found
    return None


def check_clearance(html_path):
    """Render the sheet and report spare room per page, in mm.

    A negative number means that page's last block prints on top of the footer,
    which is invisible on screen and obvious only once it is on paper.
    """
    chrome = find_chrome()
    if not chrome:
        print("--check skipped: no Chrome or Chromium found. Check it by eye:")
        print("  open the file and confirm the last block clears the footer.")
        return 0

    html = html_path.read_text(encoding="utf-8")
    probe = html_path.with_name(html_path.stem + ".probe.html")
    probe.write_text(html.replace("</body>", PROBE + "</body>"), encoding="utf-8")
    try:
        out = subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--virtual-time-budget=4000",
             "--dump-dom", probe.resolve().as_uri()],
            capture_output=True, text=True, timeout=90,
        ).stdout
    except (subprocess.SubprocessError, OSError) as exc:
        print("--check could not run Chrome: %s" % exc)
        return 0
    finally:
        probe.unlink(missing_ok=True)

    m = re.search(r"CLEARANCE::([^<'\"]*)", out)
    if not m:
        print("--check could not read a measurement back from Chrome.")
        return 0

    worst = 0.0
    for item in m.group(1).split(","):
        name, _, value = item.partition(":")
        if value == "empty":
            print("  %s has no content" % name)
            continue
        mmleft = float(value)
        worst = min(worst, mmleft)
        state = "OVERFLOWS" if mmleft < 0 else "ok"
        print("  %s: %6.1fmm spare  %s" % (name, mmleft, state))

    if worst < 0:
        print(
            "\nThis sheet prints its last block over the footer by %.1fmm.\n"
            "Cut content, or move a card to the next page. Do not shrink the type."
            % -worst
        )
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True, help="header title; wrap one word in <span> for teal")
    ap.add_argument("--subtitle", required=True, help="one line: source, date, what the reader gets")
    ap.add_argument("--footer", required=True, help="footer left side, repeated on every page")
    ap.add_argument("--content", required=True, type=pathlib.Path)
    ap.add_argument("--out", required=True, type=pathlib.Path)
    ap.add_argument("--check", action="store_true",
                    help="render in headless Chrome and report spare room per page")
    args = ap.parse_args()

    if not TEMPLATE.exists():
        sys.exit("cannot find %s" % TEMPLATE)
    head, header_block, tail = slice_template(TEMPLATE.read_text(encoding="utf-8"))
    pages = split_pages(args.content.read_text(encoding="utf-8"))

    total = len(pages)
    chunks = []
    for n, (tight, body) in enumerate(pages, start=1):
        cls = "page tightpage" if tight else "page"
        chunks.append('<div class="%s">\n' % cls)
        if n == 1:
            chunks.append(build_header(header_block, args.title, args.subtitle))
        chunks.append("\n" + body + "\n\n")
        chunks.append(
            "  <footer>\n"
            "    <span>%s</span>\n"
            "    <span>Page %d of %d</span>\n"
            "  </footer>\n" % (args.footer, n, total)
        )
        chunks.append("</div>\n\n")

    # Retitle the browser tab to match the sheet.
    plain = re.sub(r"<[^>]+>", "", args.title)
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % plain, head, flags=re.S)

    # Drop notes addressed to whoever edits the template; they are not for the
    # reader of the finished sheet.
    head = re.sub(r"<!-- TEMPLATE-NOTE.*?-->\n", "", head, flags=re.S)

    args.out.write_text(head + "".join(chunks) + tail, encoding="utf-8")
    print("wrote %s: %d page(s)" % (args.out, total))

    if args.check:
        if check_clearance(args.out):
            sys.exit(1)

    print("Now print it: Chrome, A4, Margins None, Background graphics ON.")


if __name__ == "__main__":
    main()
