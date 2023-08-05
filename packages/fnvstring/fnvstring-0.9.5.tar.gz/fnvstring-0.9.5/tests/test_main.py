import sys

from pytest import fixture

from fnvstring.__main__ import main


def test_no_argument(monkeypatch, *arg, **args):
    assert main() == 0


@fixture(autouse=True)
def test_to_many_arguments(monkeypatch, *arg, **args):
    monkeypatch.setattr(sys, "argv", ["fvnhash"])
    assert main() == -1

    monkeypatch.setattr(
        sys, "argv", ["fvnhash", "mystring", "mysalt", "extraincorrectargument"]
    )
    assert main() == -1


@fixture(autouse=True)
def test_valid_arguments(monkeypatch, *arg, **args):
    monkeypatch.setattr(sys, "argv", ["fvnhash", "-h"])
    assert main() == 0

    monkeypatch.setattr(sys, "argv", ["fvnhash", "mystring"])
    assert main() == 0

    monkeypatch.setattr(sys, "argv", ["fvnhash", "mystring", "mysalt"])
    assert main() == 0
