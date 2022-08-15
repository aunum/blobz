import os
import stat
import platform
import sys
import urllib.request
from setuptools import find_packages
from setuptools import setup

REPO = "old-ocean-creature/carvel-imgpkg"
VERSION = "v0.29.3-arc"
BIN_PATH = "./blobz/bin"


def download():
    """Download imgpkg"""

    build = platform.platform()
    os_name = sys.platform
    print(f"downloading imgpkg for '{os_name}' '{build}'")

    asset_url = f"https://github.com/{REPO}/releases/download/{VERSION}"

    if os_name == "darwin":
        if "x86_64" in build:
            asset_url = f"{asset_url}/imgpkg-darwin-amd64"
        if "arm64" in build:
            asset_url = f"{asset_url}/imgpkg-darwin-arm64"
    elif os_name == "linux":
        if "x86_64" in build:
            asset_url = f"{asset_url}/imgpkg-linux-amd64"
        if "arm64" in build:
            asset_url = f"{asset_url}/imgpkg-linux-arm64"
    else:
        raise ValueError(f"os name not supported '{os_name}'")

    # download the url contents in binary format
    headers = {"Accept": "application/octet-stream"}
    print("asset_url: ", asset_url)
    req = urllib.request.Request(asset_url, headers=headers)
    r = urllib.request.urlopen(req)

    if not os.path.exists(BIN_PATH):
        os.mkdir(BIN_PATH)

    file_path = os.path.join(BIN_PATH, "imgpkg")
    with open(file_path, "wb") as code:
        code.write(r.read())

    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IEXEC)


download()

setup(
    name="blobz",
    version="0.0.13",
    url="https://github.com/aunum/blobz",
    project_urls={
        "Documentation": "https://github.com/aunum/blobz",
        "Code": "https://github.com/aunum/blobz",
        "Issue tracker": "https://github.com/aunum/blobz",
    },
    maintainer="Patrick Barker",
    description="Artifact storage using OCI registries",
    python_requires=">=3.6",
    install_requires=["jsonpickle"],
    packages=find_packages(include=("blobz", "blobz.*")),
    package_data={"blobz": ["bin/*"]},
)
