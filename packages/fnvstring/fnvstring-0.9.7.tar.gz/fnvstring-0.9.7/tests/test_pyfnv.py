from fnvstring import Fvn64SaltedHasher, Hash


def test_ok():
    assert Hash.works_ok() is True


def test_Salted():
    salted = Fvn64SaltedHasher("mysalt")
    assert salted.salt == "mysalt"
    assert salted.hash("A") == Hash.from_string("A", "mysalt")
    assert salted.hash("A") != Hash.from_string("A")
