"""Tokenizer-independent token-ID length matching for the approved neutral pad."""

from __future__ import annotations


class NeutralPadUnrepresentable(ValueError):
    """Raised when the full marker cannot fit in the removed memory's token length."""


def length_matched_marker_token_ids(
    marker_token_ids: tuple[int, ...] | list[int], target_length: int
) -> tuple[int, ...]:
    marker = tuple(marker_token_ids)
    if not marker or any(not isinstance(token_id, int) or token_id < 0 for token_id in marker):
        raise ValueError("marker token IDs must be non-empty non-negative integers")
    if target_length < len(marker):
        raise NeutralPadUnrepresentable(
            "target is shorter than the complete neutral-pad marker"
        )
    return tuple(marker[index % len(marker)] for index in range(target_length))
