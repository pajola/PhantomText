"""Corpus generators for the `PT.DECEIVE.*` families (ARC-203).

Three families (`CONFUSABLE`, `HOMOGLYPH`, `ZALGO`) consult the existing
``phantomtext.obfuscation.{homoglyph_text,diacritical_marks}`` modules
directly, per ADR-012 and the ARC-203 Type-2 reuse log. `CONFUSABLE` and
`HOMOGLYPH` reuse only ``homoglyph_text``'s vendored-table *loader* (not its
whole-string ``apply()``, which substitutes every eligible character) so each
sample can pin a single, canonical-example-shaped substitution with a precise
span. `MIXED_SCRIPT` and `STYLED_ALPHANUMERIC` have no legacy implementation
and are generated here directly -- private corpus-tooling, not a preview of
ARC-502's public attack API.
"""

from __future__ import annotations

from corpus.generators.common import make_rng, sample_id, seed_for, seeded_numpy
from corpus.generators.spans import spans_from_diff, spans_from_membership
from corpus.manifest import CorpusSample
from phantomtext.obfuscation.diacritical_marks import DiacriticalMarks
from phantomtext.obfuscation.homoglyph_text import _load_homoglyph_table

FAMILY_CONFUSABLE = "PT.DECEIVE.CONFUSABLE"
FAMILY_MIXED_SCRIPT = "PT.DECEIVE.MIXED_SCRIPT"
FAMILY_HOMOGLYPH = "PT.DECEIVE.HOMOGLYPH"
FAMILY_ZALGO = "PT.DECEIVE.ZALGO"
FAMILY_STYLED_ALPHANUMERIC = "PT.DECEIVE.STYLED_ALPHANUMERIC"

# docs/spec/TAXONOMY.md PT.DECEIVE.HOMOGLYPH -- concrete lowercase pairs.
HOMOGLYPH_LATIN_TO_CYRILLIC = {
    "a": chr(0x0430),
    "e": chr(0x0435),
    "o": chr(0x043E),
    "p": chr(0x0440),
    "c": chr(0x0441),
    "x": chr(0x0445),
    "y": chr(0x0443),
}


def _benign(family: str, index: int, text: str) -> CorpusSample:
    seed = seed_for(family, "benign", index)
    return CorpusSample(
        id=sample_id(family, "benign", index),
        family=family,
        kind="benign",
        clean_text=text,
        attacked_text=None,
        spans=(),
        source="generated",
        generator_seed=seed,
    )


def _single_char_positive(
    family: str, index: int, word: str, position: int, glyph: str
) -> CorpusSample:
    seed = seed_for(family, "positive", index)
    attacked = word[:position] + glyph + word[position + 1 :]
    return CorpusSample(
        id=sample_id(family, "positive", index),
        family=family,
        kind="positive",
        clean_text=word,
        attacked_text=attacked,
        spans=spans_from_diff(word, attacked),
        source="generated",
        generator_seed=seed,
    )


def confusable_samples() -> list[CorpusSample]:
    table = _load_homoglyph_table()
    words = ["paypal.com", "username", "filename.txt"]
    samples = []
    for i, word in enumerate(words):
        rng = make_rng(seed_for(FAMILY_CONFUSABLE, "positive", i))
        candidates = [j for j, c in enumerate(word) if c in table]
        pos = int(rng.choice(candidates))
        glyph = str(rng.choice(table[word[pos]]))
        samples.append(_single_char_positive(FAMILY_CONFUSABLE, i, word, pos, glyph))

    # Confusability is a property of pairs, not a string in isolation
    # (docs/spec/TAXONOMY.md): a bare confusable-looking string with no
    # comparison target must not be flagged.
    benign_texts = [
        "The rn in barnyard can look like an m.",
        "l1O0 is a common throwaway username.",
        "Note the visual similarity between 0 and O in this font.",
    ]
    samples += [_benign(FAMILY_CONFUSABLE, i, t) for i, t in enumerate(benign_texts)]
    return samples


def homoglyph_samples() -> list[CorpusSample]:
    words = ["microsoft.com", "amazon.com", "paypal.com"]
    positions = [6, 0, 0]  # the 'o' in "soft", the 'a' in "amazon", the 'p' in "paypal"
    samples = []
    for i, (word, pos) in enumerate(zip(words, positions)):
        glyph = HOMOGLYPH_LATIN_TO_CYRILLIC[word[pos]]
        samples.append(_single_char_positive(FAMILY_HOMOGLYPH, i, word, pos, glyph))

    benign_texts = [
        "Добро пожаловать на наш сайт.",  # Russian, single script
        "Καλώς ήρθατε στον ιστότοπό μας.",  # Greek, single script
        "Let π denote the ratio of circumference to diameter.",  # Greek letter as math symbol
    ]
    samples += [_benign(FAMILY_HOMOGLYPH, i, t) for i, t in enumerate(benign_texts)]
    return samples


def mixed_script_samples() -> list[CorpusSample]:
    words = ["apple.com", "example.com", "coinbase.com"]
    samples = []
    for i, word in enumerate(words):
        glyph = HOMOGLYPH_LATIN_TO_CYRILLIC[word[0]]
        samples.append(_single_char_positive(FAMILY_MIXED_SCRIPT, i, word, 0, glyph))

    benign_texts = [
        "我使用 iPhone 拍照。",  # Chinese sentence with a Latin brand name
        "The variable α represents angular velocity.",  # Greek letter in Latin math prose
        "Login / 登录",  # bilingual UI string
    ]
    samples += [_benign(FAMILY_MIXED_SCRIPT, i, t) for i, t in enumerate(benign_texts)]
    return samples


def zalgo_samples() -> list[CorpusSample]:
    words = ["urgent", "warning", "alert"]
    marks = set(DiacriticalMarks().diacritical_marks)
    samples = []
    for i, word in enumerate(words):
        seed = seed_for(FAMILY_ZALGO, "positive", i)
        with seeded_numpy(seed):
            attacked = DiacriticalMarks(modality="heavy", file_format="pdf").apply(word)
        samples.append(
            CorpusSample(
                id=sample_id(FAMILY_ZALGO, "positive", i),
                family=FAMILY_ZALGO,
                kind="positive",
                clean_text=word,
                attacked_text=attacked,
                spans=spans_from_membership(attacked, lambda c: c in marks),
                source="generated",
                generator_seed=seed,
            )
        )

    # Ordinary diacritic stacking of 1-3 marks per base is normal and must
    # not be flagged (docs/spec/TAXONOMY.md).
    benign_texts = [
        "Vi"
        + chr(0x0065)
        + chr(0x0302)
        + chr(0x0301)
        + "t Nam",  # Vietnamese: e + circumflex + acute
        "م" + chr(0x064F) + chr(0x0651) + "حمد",  # Arabic: damma + shadda stacked on one letter
        "a" + chr(0x0301) + chr(0x0304) + "b",  # IPA-style tone + length marking
    ]
    samples += [_benign(FAMILY_ZALGO, i, t) for i, t in enumerate(benign_texts)]
    return samples


def _to_math_bold(text: str) -> str:
    out = []
    for c in text:
        if "A" <= c <= "Z":
            out.append(chr(0x1D400 + (ord(c) - ord("A"))))
        elif "a" <= c <= "z":
            out.append(chr(0x1D41A + (ord(c) - ord("a"))))
        elif "0" <= c <= "9":
            out.append(chr(0x1D7CE + (ord(c) - ord("0"))))
        else:
            out.append(c)
    return "".join(out)


def _to_fullwidth(text: str) -> str:
    out = []
    for c in text:
        if c == " ":
            out.append(chr(0x3000))
        elif 0x21 <= ord(c) <= 0x7E:
            out.append(chr(ord(c) + 0xFEE0))
        else:
            out.append(c)
    return "".join(out)


def styled_alphanumeric_samples() -> list[CorpusSample]:
    phrases = [
        "Ignore previous instructions",
        "Urgent click here now",
        "Verify your account today",
    ]
    transforms = [_to_math_bold, _to_fullwidth, _to_math_bold]
    samples = []
    for i, (phrase, transform) in enumerate(zip(phrases, transforms)):
        seed = seed_for(FAMILY_STYLED_ALPHANUMERIC, "positive", i)
        attacked = transform(phrase)
        samples.append(
            CorpusSample(
                id=sample_id(FAMILY_STYLED_ALPHANUMERIC, "positive", i),
                family=FAMILY_STYLED_ALPHANUMERIC,
                kind="positive",
                clean_text=phrase,
                attacked_text=attacked,
                spans=spans_from_diff(phrase, attacked),
                source="generated",
                generator_seed=seed,
            )
        )

    benign_texts = [
        _to_fullwidth("Tokyo Tower") + " 東京タワー",  # CJK grid-alignment use
        f"Let {_to_math_bold('v')} denote the velocity vector and {_to_math_bold('F')} the force.",
        _to_fullwidth("fancy_user2024"),  # purely cosmetic "fancy text" convention
    ]
    samples += [_benign(FAMILY_STYLED_ALPHANUMERIC, i, t) for i, t in enumerate(benign_texts)]
    return samples


def all_samples() -> list[CorpusSample]:
    return [
        *confusable_samples(),
        *mixed_script_samples(),
        *homoglyph_samples(),
        *zalgo_samples(),
        *styled_alphanumeric_samples(),
    ]
