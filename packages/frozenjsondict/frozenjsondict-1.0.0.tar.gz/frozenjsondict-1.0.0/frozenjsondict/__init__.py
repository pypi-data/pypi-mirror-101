from collections.abc import Mapping
import json


class FrozenJsonDict(Mapping):
    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)
        self._id = json.dumps(self._dict, sort_keys=True, separators=(",", ":"))
        self._hash = hash(self._id)

    def __getitem__(self, item):
        return self._dict[item]

    def __getattr__(self, item):
        return self._dict[item]

    def __contains__(self, item):
        return item in self._dict

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self._id}>"
