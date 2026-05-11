import pytest
from src.utils.prompt_template import PromptTemplate


def test_sanitize_strips_control_characters():
    pt = PromptTemplate()
    assert pt.sanitize("hello\x00world\x1f") == "hello world"


def test_sanitize_passes_clean_input():
    pt = PromptTemplate()
    assert pt.sanitize("  AI tools niche  ") == "AI tools niche"


def test_sanitize_raises_on_too_long_input():
    pt = PromptTemplate(max_length=10)
    with pytest.raises(ValueError, match="exceeds maximum"):
        pt.sanitize("a" * 11)


def test_sanitize_accepts_exact_max_length():
    pt = PromptTemplate(max_length=5)
    assert pt.sanitize("hello") == "hello"
