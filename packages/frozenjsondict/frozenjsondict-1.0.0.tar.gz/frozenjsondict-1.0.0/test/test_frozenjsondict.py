from frozenjsondict import FrozenJsonDict


fjd_1 = FrozenJsonDict({"a": [1, 2, 3]})
fjd_2 = FrozenJsonDict({"b": [3, 4], "c": [6]})
fjd_3 = FrozenJsonDict({"c": [6], "b": [3, 4]})


def test_get_item():
    assert fjd_1["a"] == [1, 2, 3]


def test_get_attr():
    assert fjd_1.a == [1, 2, 3]


def test_contains():
    assert "a" in fjd_1


def test_iter():
    assert FrozenJsonDict({key: value for key, value in fjd_2.items()}) == fjd_2


def test_len():
    assert len(fjd_2) == 2


def test_hash():
    assert hash(fjd_2) == hash(fjd_3)


def test_eq():
    assert fjd_2 == fjd_3


def test_repr():
    assert str(fjd_1) == '<FrozenJsonDict {"a":[1,2,3]}>'
