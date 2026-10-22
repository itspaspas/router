import pytest

from gateway.language import detect_language


@pytest.mark.parametrize("text,expected", [
    ("یک شعر کوتاه درباره باران بنویس", "fa"),
    ("Write a short poem about rain.", "en"),
    ("لطفاً این function را در Python بازنویسی کن", "mixed"),
    ("می‌خواهم", "fa"),                 # ZWNJ (U+200C) must not count as Latin
    ("۱۲۳ 456 !!!", "unknown"),         # digits/punctuation only
    ("", "unknown"),
])
def test_detect_language(text, expected):
    assert detect_language(text) == expected
