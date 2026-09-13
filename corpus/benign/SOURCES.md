# Benign multilingual corpus — sources & licensing (ADR-015 D3)

A standing false-positive smoke test: a future detector (Season 3+) must score
**zero findings** against every file in this directory. Independent of any
single taxonomy family — see `corpus/manifests/corpus.jsonl` for the
per-family positive/benign pairs instead.

All text below is vendored as static files, fetched once by hand and
committed; nothing in `corpus/` fetches anything at generation or test time.

## Files

| File | Language | Source |
|---|---|---|
| `fa.txt` | Persian (Farsi) | UDHR, Article 1, official UN translation |
| `hi.txt` | Hindi | UDHR, Article 1, official UN translation |
| `ar.txt` | Arabic | UDHR, Article 1, official UN translation |
| `he.txt` | Hebrew | UDHR, Article 1, official UN translation |
| `vi.txt` | Vietnamese | UDHR, Article 1, official UN translation |
| `zh.txt` | Chinese (Simplified) | UDHR, Article 1, official UN translation |
| `emoji.txt` | — | Hand-built ZWJ/VS16 emoji sequences (real, registered Unicode emoji sequences per UTS #51) |

The Universal Declaration of Human Rights is reproduced by the United Nations
without copyright restriction and is translated into essentially every
written language — short, stable, and unambiguous to attribute, which is why
it was chosen over a larger scraped multilingual dataset (ADR-015 D3
"Alternatives considered").

These excerpts are for corpus/testing purposes only and are not a legal
citation of the Declaration.
