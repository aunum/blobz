![logo](./static/logo.png)

A lazy Python utility to store arbitrary artifacts in any docker image repository

# Install

```sh
pip install blobz
```

## Prerequisites
* Working authentication to your image registry of choice e.g. `~/.docker/config.json`

# Quick Start

Push some files to a docker repository and add labels to the artifact
```python
import blobz

blobz.push("myrepo/foo:v1", file="./tests/data/test.yaml", labels={"qux": "baz"})
```

Pull them back out
```python
blobz.pull("myrepo/foo:v1", "./out/")
```
---

Push an arbitrary python object to a repository
```python
bar_obj = Bar("bar", 1, {"qux": "baz"})

blobz.push("myrepo/bar:v1", obj=bar_obj)
```

Pull the object back out and load it

```python
import jsonpickle 

str_dict = blobz.pull_str("myrepo/bar:v1")
bar_obj = jsonpickle.decode(str_dict["BarObj.json"])
```

---
Push an object in pickle format with a designated filename
```python
blobz.push(
    "myrepo/bar:v2",
    obj_map={"my_obj.pkl": bar_obj},
    obj_encoder=blobz.ObjEncoderType.PICKLE,
)
```

Pull it back out as bytes and load it with pickle
```python
import pickle

byte_dict = blobz.pull_bytes("myrepo/bar:v2")
bar_obj = pickle.loads(byte_dict["my_obj.pkl"])
```

More complete examples can be found in the [tests](./tests/test_api.py)

# FAQ

__What about OCI artifacts?__

OCI artifacts are amazing and will be the future, but many registries don't support them yet, this tool will work with any docker registry. 


