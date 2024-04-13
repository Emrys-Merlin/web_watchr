from website_monitoring_bot.compare.fs_comparer import FSComparer, FSComparerConfig
from unittest.mock import MagicMock
from typing import Callable


def test_no_previous_state_with_send_on_missing(
    test_fs_comparer: FSComparer,
    mock_poller: Callable[[], str],
):
    """New state is saved if send on missing"""
    test_fs_comparer.config.send_on_missing = True
    mocked_save = MagicMock()
    test_fs_comparer.save = mocked_save  # type: ignore
    new_state = mock_poller()

    test_fs_comparer.run()

    mocked_save.assert_called_once_with(new_state=new_state)


def test_no_previous_state_without_send_on_missing(
    test_fs_comparer: FSComparer,
    mock_poller: Callable[[], str],
):
    test_fs_comparer.config.send_on_missing = False
    mocked_save = MagicMock()
    test_fs_comparer.save = mocked_save  # type: ignore
    new_state = mock_poller()

    test_fs_comparer.run()

    assert mocked_save.call_count == 0


def test_no_change(
    test_fs_comparer: FSComparer,
    mock_poller: Callable[[], str],
):
    mocked_save = MagicMock()
    test_fs_comparer.save = mocked_save  # type: ignore
    new_state = mock_poller()
    with open(test_fs_comparer.cache_path, "w") as f:
        f.write(new_state)

    test_fs_comparer.run()

    assert mocked_save.call_count == 0


def test_change(
    test_fs_comparer: FSComparer,
    mock_poller: Callable[[], str],
):
    mocked_save = MagicMock()
    test_fs_comparer.save = mocked_save  # type: ignore
    new_state = mock_poller()
    with open(test_fs_comparer.cache_path, "w") as f:
        f.write(f"not {new_state}")

    test_fs_comparer.run()

    mocked_save.assert_called_once_with(new_state=new_state)
