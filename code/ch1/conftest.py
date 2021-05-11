from pathlib import Path
from _pytest.nodes import Item
from _pytest.runner import CallInfo
import pytest

FAILURES_FILE = Path() / "failures.txt"


def pytest_configure(config):
    config.addinivalue_line("markers", "cool_marker: this one is for cool tests.")
    config.addinivalue_line(
        "markers", "mark_with(arg, arg2): this marker takes arguments."
    )


@pytest.hookimpl()
def pytest_sessionstart(session):
    if FAILURES_FILE.exists():
        # We want to delete the file if it already exists
        # so we don't carry over failures form last run
        FAILURES_FILE.unlink()
    FAILURES_FILE.touch()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    # All code prior to yield statement would be ran prior
    # to any other of the same fixtures defined

    outcome = yield  # Run all other pytest_runtest_makereport non wrapped hooks
    result = outcome.get_result()
    if result.when == "call" and result.failed:
        try:  # Just to not crash py.test reporting
            with open(str(FAILURES_FILE), "a") as f:
                f.write(result.nodeid + "\n" + result.longreprtext)
        except Exception as e:
            print("ERROR", e)
            pass
