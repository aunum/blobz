"""Test blobz API"""

from datetime import datetime
import sys
import pickle
from typing import Any, Dict

import jsonpickle

sys.path.append("../")
import blobz

curr_dt = datetime.now()
timestamp = int(round(curr_dt.timestamp()))

# test file
blobz.push(
    f"oldoceancreature/blobz-test:file-{timestamp}",
    file="./tests/data/test.yaml",
    labels={"this": "that"},
    refs={"related_artifact": "oldoceancreature/blobz-test:other"},
)
blobz.pull(f"oldoceancreature/blobz-test:file-{timestamp}", "./tests/out/")


class Foo:
    """A test obj"""

    a: str
    b: int
    c: Dict[str, Any]

    def __init__(self, a: str, b: int, c: Dict[str, Any]):
        self.a = a
        self.b = b
        self.c = c


class Bar:
    """A test obj"""

    d: str
    e: int
    f: Dict[str, Any]

    def __init__(self, d: str, e: int, f: Dict[str, Any]):
        self.d = d
        self.e = e
        self.f = f


foo_obj = Foo("foo", 1, {"bar": "baz"})
bar_obj = Bar("bar", 2, {"qux": "qoz"})

# single obj str
blobz.push(f"oldoceancreature/blobz-test:obj-single-{timestamp}", obj=foo_obj)
str_dict = blobz.pull_str(f"oldoceancreature/blobz-test:obj-single-{timestamp}")
assert jsonpickle.decode(str_dict["Foo.json"]).__dict__ == foo_obj.__dict__

# list obj str
blobz.push(f"oldoceancreature/blobz-test:obj-multi-{timestamp}", obj=[foo_obj, bar_obj])
str_dict = blobz.pull_str(f"oldoceancreature/blobz-test:obj-multi-{timestamp}")
assert jsonpickle.decode(str_dict["Foo.json"]).__dict__ == foo_obj.__dict__

# list obj dups
blobz.push(f"oldoceancreature/blobz-test:obj-multi-{timestamp}", obj=[foo_obj, foo_obj])
str_dict = blobz.pull_str(f"oldoceancreature/blobz-test:obj-multi-{timestamp}")
assert jsonpickle.decode(str_dict["Foo.json"]).__dict__ == foo_obj.__dict__
assert jsonpickle.decode(str_dict["Foo-1.json"]).__dict__ == foo_obj.__dict__

# obj map str
blobz.push(f"oldoceancreature/blobz-test:obj-str-{timestamp}", obj_map={"test_obj.json": foo_obj})
str_dict = blobz.pull_str(f"oldoceancreature/blobz-test:obj-str-{timestamp}")
assert jsonpickle.decode(str_dict["test_obj.json"]).__dict__ == foo_obj.__dict__

# obj map bytes
blobz.push(
    f"oldoceancreature/blobz-test:obj-bytes-{timestamp}",
    obj_map={"test_obj.pkl": foo_obj},
    obj_encoder=blobz.ObjEncoderType.PICKLE,
)
byte_dict = blobz.pull_bytes(f"oldoceancreature/blobz-test:obj-bytes-{timestamp}")
assert pickle.loads(byte_dict["test_obj.pkl"]).__dict__ == foo_obj.__dict__
