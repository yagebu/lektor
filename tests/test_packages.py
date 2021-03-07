from pathlib import Path
from textwrap import dedent

from lektor.packages import hash_directory
from lektor.packages import list_local_packages
from lektor.packages import load_manifest
from lektor.packages import write_manifest


def test_read_write_manifest(tmp_path: Path):
    manifest_path = tmp_path / "manifest"
    packages = {"@test": None, "pypi-package": "0.2"}
    write_manifest(manifest_path, packages)
    contents = manifest_path.read_text()
    assert contents == dedent(
        """\
        @test
        pypi-package=0.2
        """
    )
    loaded = load_manifest(manifest_path)
    assert loaded == packages


def test_list_local_packages(tmp_path: Path):
    (tmp_path / "nopackage").mkdir()
    (tmp_path / "package").mkdir()
    (tmp_path / "package" / "setup.py").touch()
    assert list_local_packages(tmp_path) == ["@package"]


def test_hash_directory(tmp_path: Path):
    before = hash_directory(tmp_path)
    assert before == "4cde429832ae7a7061dd66bb165a9df247d4bf30"
    (tmp_path / "dir").mkdir()
    with_dir = hash_directory(tmp_path)
    assert with_dir == "b652d7600e872548286a45da94e63446bb84b6da"
    (tmp_path / "dir").touch()
    assert hash_directory(tmp_path) == "b652d7600e872548286a45da94e63446bb84b6da"
