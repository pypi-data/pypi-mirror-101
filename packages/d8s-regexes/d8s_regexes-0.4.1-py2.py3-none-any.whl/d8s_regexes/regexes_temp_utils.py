"""Utility functions temporarily provided until the rest of the democritus functions get uploaded."""

from typing import Any, Iterable, List


def sort_by_length(list_arg: Iterable[Any], **kwargs) -> List[Any]:
    """."""
    sorted_list = sorted(list_arg, key=lambda x: len(x), **kwargs)
    return sorted_list


def longest(iterable: Iterable) -> Any:
    """."""
    longest_item = sort_by_length(iterable, reverse=True)[0]
    return longest_item


def deduplicate(iterable: Iterable) -> list:
    """Deduplicate the iterable."""
    # TODO: will this work for every type except for dicts???
    deduplicated_list = list(set(iterable))
    return deduplicated_list
