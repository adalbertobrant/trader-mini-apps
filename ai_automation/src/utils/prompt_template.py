"""
PromptTemplate — input sanitization before any user string reaches an LLM prompt.

Strips control characters and enforces a maximum character length.
This is a Phase 5 pre-condition (BACKLOG: input sanitization on all request fields).
"""
import re

# Sane upper bound: prevents runaway prompts and credit burn.
DEFAULT_MAX_LENGTH = 2000


class PromptTemplate:
    def __init__(self, max_length: int = DEFAULT_MAX_LENGTH):
        self.max_length = max_length

    def sanitize(self, value: str) -> str:
        """Strip control characters and truncate to max_length."""
        cleaned = re.sub(r"[\x00-\x1f\x7f]", " ", value).strip()
        if len(cleaned) > self.max_length:
            raise ValueError(
                f"Input exceeds maximum allowed length of {self.max_length} characters "
                f"(got {len(cleaned)})."
            )
        return cleaned
