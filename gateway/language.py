"""Language detection for the last user message of a chat request.

Labels text as "fa" (Persian), "en" (English), "mixed", or "unknown".

Known limitation: Arabic-script text in any language (e.g. Arabic itself) is
labelled "fa", because the script is what is measured, not the language.
Letters outside Arabic script and ASCII a-z/A-Z (e.g. accented Latin, Cyrillic,
CJK) are ignored entirely.
"""
from __future__ import annotations

from typing import Literal

Language = Literal["fa", "en", "mixed", "unknown"]

_ARABIC_SCRIPT_RANGES = (
    (0x0600, 0x06FF),
    (0x0750, 0x077F),
    (0xFB50, 0xFDFF),
    (0xFE70, 0xFEFF),
)
_FA_MIN_RATIO = 0.8
_EN_MAX_RATIO = 0.2


def _is_arabic_script(ch: str) -> bool:
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in _ARABIC_SCRIPT_RANGES)


def _is_ascii_latin(ch: str) -> bool:
    return ("a" <= ch <= "z") or ("A" <= ch <= "Z")


def detect_language(text: str) -> Language:
    """Classify text by the share of Arabic-script letters among Arabic + Latin letters.

    Only letters (``str.isalpha()``) are counted, so ZWNJ, diacritics, digits and
    punctuation do not affect the result. With ``r = arabic / (arabic + latin)``:
    no letters -> "unknown"; ``r >= 0.8`` -> "fa"; ``r <= 0.2`` -> "en"; else "mixed".
    """
    arabic = 0
    latin = 0
    for ch in text:
        if not ch.isalpha():
            continue
        if _is_arabic_script(ch):
            arabic += 1
        elif _is_ascii_latin(ch):
            latin += 1

    total = arabic + latin
    if total == 0:
        return "unknown"
    ratio = arabic / total
    if ratio >= _FA_MIN_RATIO:
        return "fa"
    if ratio <= _EN_MAX_RATIO:
        return "en"
    return "mixed"
