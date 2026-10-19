---
name: bfa-one-pager
description: >-
  Turns notes, slides, a document or a meeting transcript into a printable one or two page A4
  document in the BFA Global house style, with the brand colours, fonts and logo already correct.
  Use it whenever someone asks for a one pager, a cheat sheet, a take-home sheet, a leave-behind, a
  handout, an agenda, a glossary, a briefing note, a printable summary or a PDF that looks like the
  AI Brown Bag sheets, or asks to turn a session, a deck or a set of notes into something they can
  print and hand out.
metadata:
  version: 1.0.0
---

# BFA one pager

## What this produces

A single self-contained HTML file the user prints to PDF. One or two A4 pages, portrait, designed to be skimmed quickly and kept on a desk.

The genre varies: a session cheat sheet, a leave-behind after a client meeting, a one page agenda, a glossary, a briefing note. The house style and the building blocks are the same for all of them.

The sheet is built from a fixed set of blocks: a dark header band carrying the BFA logo, numbered cards, tight bullet or numbered lists, a table for definitions and comparisons, a teal box for anything the reader should copy or say out loud, an orange box for the one thing that goes wrong, a dark closing panel naming the single next action, and a footer.

That is the whole set. If the content does not fit one of those blocks, the content usually needs rethinking rather than a new block.

## Before you write

- Read `reference/example.html`. It is a real sheet that was delivered, and it shows the density to aim for.
- Work only from material the user gives you or asks you to fetch. Never invent facts, numbers, quotes or attendees to fill a card.
- Decide one page or two before you start writing. Two pages is the normal size for a session recap; one page suits a single procedure or a glossary.
- Ask the user only what you genuinely cannot infer: usually the title, the source and date line for the subtitle, and the footer series name.

## How to write it

- **One idea per card**, numbered in the order the reader needs them. Give each card a short title and, on the right, a hint of a few words saying the point of the card.
- **Bold the phrase that carries the point** so the sheet can be skimmed without being read.
- **Four bullets per card at most.** Past that, split the card.
- **One warning per sheet at most**, in the orange note box. More than one and it stops being a warning.
- **The dark panel goes last, once**, and names an action rather than a topic. "Take last week's skill and add one connector line" beats "Next steps".
- Short sentences. No filler, no throat clearing, no restating the title back to the reader.
- **Never use em dashes or en dashes.** Use a comma, a colon or a full stop.

## How to present it

**Preferred, when you can run code.** Write the cards to a content file and let the script assemble the sheet. It supplies the house style, the logo, the header and the page numbering, so none of those can come out wrong.

Write `content.html` holding only cards and panels, with a marker before each page:

```html
<!-- PAGE -->
<div class="card">
  <div class="card-head"><span class="num">1</span><h2>Card title</h2><span class="hint">the point, in a few words</span></div>
  <div class="card-body">
    <ul class="tight"><li><strong>The phrase that carries it.</strong> Then the rest</li></ul>
  </div>
</div>
<!-- PAGE -->
<div class="card">...</div>
<div class="panel"><h2>This week</h2><p>The one action.</p></div>
```

Then build it:

```bash
python3 scripts/build_sheet.py \
  --title 'Connected skills<span>:</span> the take-home sheet' \
  --subtitle 'AI Brown Bag #4 &middot; August 17, 2026 &middot; What the reader gets' \
  --footer 'BFA Global &middot; AI Brown Bag series &middot; session 4 of 6' \
  --content content.html --out sheet.html --check
```

**Always pass `--check`.** It renders the sheet and reports how much room each page has left. A negative number means the last block prints on top of the footer, which you cannot see in the markup and the user will not notice until it is on paper. If it reports an overflow, cut content or move a card to the next page, then build again.

Wrap one word or mark of the title in `<span>` to pick it up in teal. Do not write headers, footers or page divs into the content file; the script generates them and will stop if it finds them.

Pages use the tight spacing by default, because nearly every real sheet needs it. Use `<!-- PAGE roomy -->` only for a deliberately sparse page, and check it afterwards.

**Fallback, when you cannot run code.** Copy `reference/template.html` in full and replace only what is inside `<body>`. Keep the `<style>` block byte for byte, and keep the `<img class="logo">` line exactly as it is: the logo is embedded in it as a data URI, which is what makes the sheet a single file that survives being emailed around.

**Either way, finish by giving the user the print settings**, because the sheet prints wrong without them:

> Open the file in Chrome, then Print. Destination **Save as PDF**, Paper **A4**, Margins **None**, Scale **Default**, and **tick Background graphics**.

Background graphics is the one people miss. Without it the sheet prints as plain white with no dark header and no teal.

## Rules that do not bend

- **Do not change the `:root` colour block, the font sizes or the page dimensions.** They are set to work together and are checked against the BFA brand guidelines.
- **Three colours deliberately depart from the brand palette, for legibility in print.** Borders use `#d8d8d8` because BFA's `#ececec` disappears as a printed hairline. Hints and footers use `#7d7d7d` because BFA's `#aaaaaa` fails legibility at 7.8pt. The warning label is set in ink because brand orange on its own tint measures about 3.4:1. Do not "correct" these back to brand values.
- **Page height is 296mm, not 297mm.** The millimetre of slack stops a rounding error emitting a blank final page. Leave it alone.
- **The logo is used as supplied.** If you resize it, set the width and leave the height on `auto`. Never below 15mm wide, never rotated, recoloured, rearranged or stretched.
- **Poppins is deliberate.** It is BFA's own named substitute where Century Gothic is unavailable. It needs an internet connection when printing.

## Finish by

Tell the user how many pages the sheet came out at, and give them the print settings above.

**Never hand over a sheet you have not checked for overflow.** With the script, that is `--check`. Without it, open the file and confirm the last block on each page clears the footer, because a full page silently prints its final line underneath the footer text.

If it ran long, **cut content, never shrink the type.** Poppins sets wider than Century Gothic, so a sheet built on a Mac has less room than the same sheet on Windows, not more.

## Reference

- `reference/template.html`: the house style with placeholder content. The `<style>` block is the authority on every colour and size. Read it before your first sheet.
- `reference/example.html`: a real two page sheet as delivered. Read it for density and tone.
- `scripts/build_sheet.py`: assembles a sheet from a content file and, with `--check`, measures whether it fits. Run it with `--help` for the arguments.
