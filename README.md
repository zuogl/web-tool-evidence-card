# Web tool evidence cards

A small JSON format and an offline Python validator for keeping a source statement, an observation and an open question separate. This is intended for writers maintaining product descriptions and deciding what needs another check.

I maintain the six projects used in the illustrative cards. They are examples from my own sites, not independent endorsements or acceptance-test results. The validator checks this record format; it cannot prove a statement true, establish product behavior or judge every exaggerated claim.

## Run locally

Python 3.9 or later is sufficient. There are no packages to install and the validator makes no network requests:

```sh
python3 validate_cards.py examples/*.json
python3 -m unittest -v
```

The first command reports either `structure OK (product behavior not verified)` or format errors and returns a nonzero exit status if any supplied card is invalid. It reads only the JSON paths you pass to it. The tests exercise format rules, not the linked products.

## What a card can and cannot establish

`source_summary` is a paraphrase attributed to `reference_url`. A product's own page can establish what that page declares; it does not independently establish what the implementation always does.

`observations` records a method, a result and a timestamp only after someone actually makes an observation. Reading a page, inspecting a request and completing a task are different methods with different scopes. An empty observation list means no observation is recorded.

`unverified` preserves limitations beside the record. `next_check` describes work that remains to be done. Neither field is a result.

`recorded_on` is the date the card was assembled. `checked_at` is a separately supplied time for an actual check. A date written by a source about its own update or test belongs in the source summary, with attribution. It must not be copied into an observer's timestamp. Two genuinely independent events can occur on the same day; equality of dates alone is not an error.

The six supplied files have `illustrative: true`, `checked_at: null` and `observations: []`. Their creation date is not a claim that someone ran the products on that date. Copy a card, set `illustrative` to `false` only when appropriate, and replace its fields with your own records before treating it as evidence.

## Why these six examples are useful

### Destination acceptance is a separate question

Small Text Studio provides [its answer that acceptance depends on the app and device](https://bestsmalltext.online/superscript). Its card separates the source's compatibility statement from a future observation in one actual destination. A character map is not a universal rendering result.

### Dates need named roles

PokéSurvivor Hub provides [its note separating announcement dates from guide update dates](https://pokesurvivorhub.wiki/updates). The card leaves the running game build unknown. A guide edit date and a developer announcement can both be worth recording without identifying the build on a player's device.

### Visible output does not establish metadata preservation

WatermarkPilot provides [its warning that exports may not retain camera or color-profile metadata](https://watermarkpilot.com/add-watermark-to-photo). The example keeps an unperformed metadata inspection in the open questions. It refers to the photo tool and does not assign that statement to its separate PDF tool.

### Expiry is not the same event as physical cleanup

Sonify provides [its note that storage faults may delay physical cleanup](https://sonify.uk/how-it-works/). The card does not infer physical erasure from a download becoming inaccessible. A stated access rule and a separately observed storage event would need different evidence.

### Dimensions and bytes are different measurements

GifLoom provides [its note that dimensions describe the canvas, not the bytes](https://gifloom.com/gif-resizer). The example proposes recording both measurements if an actual sample is later processed. It includes no fabricated output size or claim of acceptance by another platform.

### A disclosure is not a captured network trace

Square Footage Calculator provides [its disclosure that measurements are not sent as analytics events](https://squarefootagecalculator.co/). The card attributes this to the page and records that no request inspection was performed for the sample. Local calculation does not imply the absence of every network request.

## Format rules and limits

See [format.md](format.md) for every field. The validator checks required and unexpected fields, types, HTTPS source URLs without embedded credentials, calendar dates, timestamps with timezones, observation entries and a required limitation. An illustrative card must leave its observation fields empty.

It does not fetch references, compare a summary against a page, detect all personal data, enforce a privacy policy or decide whether a claim is supported. It is a fixed-format validator rather than a general JSON Schema implementation. Review records manually before publishing; do not place credentials, private inputs or sensitive observations in a public card.
