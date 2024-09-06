from pathlib import Path

import pytest
from web_watchr.compare.fs_comparer import FSComparer, Status


@pytest.mark.parametrize(
    "exists",
    [True, False],
)
def test_cache_path(
    exists: bool,
    fs_comparer: FSComparer,
    cache_dir: Path,
):
    assert not cache_dir.exists()
    if exists:
        cache_dir.mkdir(parents=True)

    cache_path = fs_comparer.cache_path

    assert cache_dir.exists()
    assert cache_path.parent == cache_dir
    assert not cache_path.exists()


@pytest.mark.parametrize(
    "send_on_missing, status",
    [
        (True, Status.CHANGED),
        (False, Status.NO_CHANGES),
    ],
)
def test_first_call(
    send_on_missing: bool,
    status: Status,
    fs_comparer: FSComparer,
):
    text = "anything"
    fs_comparer.send_on_missing = send_on_missing

    received_status = fs_comparer(text=text)

    assert received_status == status


@pytest.mark.parametrize(
    "texts, status",
    [
        (["a", "b", "c"], Status.CHANGED),
        (["a", "a", "b"], Status.CHANGED),
        (["a", "a", "a"], Status.NO_CHANGES),
    ],
)
def test_second_call(
    texts: list[str],
    status: Status,
    fs_comparer: FSComparer,
):
    for text in texts:
        received_status = fs_comparer(text=text)

    assert received_status == status
