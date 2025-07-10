import subprocess
from subprocess import CalledProcessError

import pytest

from gityup_py import main as app


def test_check_exec_exists():
    assert app.check_exec_exists("python")


def test_check_exec_exists_fail():
    assert not app.check_exec_exists("flubber")


def test_parse_args():
    home_path = app.parse_args("~")
    assert home_path.is_absolute()


def test_parse_args_fail():
    with pytest.raises(ValueError, match="Given path '/does/not/exist' is not an existing directory."):
        app.parse_args("/does/not/exist")


def test_is_git_dir(tmp_path):
    subprocess.run("git init >/dev/null", cwd=tmp_path, shell=True, check=True)
    assert app.is_git(tmp_path)


def test_is_git_dir_fail(tmp_path):
    assert not app.is_git(tmp_path)


def test_git_status_clean(tmp_path):
    try:
        subprocess.run(
            "git init >/dev/null; echo 'hello' > test.txt; git add .; git commit -m 'test' >/dev/null",
            cwd=tmp_path,
            shell=True,
            check=True,
        )
    except CalledProcessError as e:
        pytest.fail("failed to initialize git repo with single commit", e)
    assert app.git_status_clean(tmp_path)


def test_git_status_clean_fail(tmp_path):
    subprocess.run("git init >/dev/null; echo 'hello' > test.txt", cwd=tmp_path, shell=True, check=True)
    assert not app.git_status_clean(tmp_path)


def test_get_git_branch_name(tmp_path):
    try:
        subprocess.run(
            "git init >/dev/null; echo 'hello' > test.txt; git add .; git commit -m 'test' >/dev/null",
            cwd=tmp_path,
            shell=True,
            check=True,
        )
    except CalledProcessError as e:
        pytest.fail("failed to initialize git repo with single commit", e)
    branch_name = app.get_git_branch_name(tmp_path)
    assert branch_name == "main"


def test_git_remote_exists(tmp_path):
    try:
        subprocess.run(
            ["git", "clone", "https://github.com/kevwil/git-smart.git"],
            cwd=tmp_path,
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
    except CalledProcessError as e:
        pytest.fail("failed to clone git repo", e)
    project_path = tmp_path / "git-smart"
    assert app.git_remote_exists(project_path, "master")


def test_git_sync(tmp_path):
    try:
        subprocess.run(
            ["git", "clone", "https://github.com/kevwil/git-smart.git"],
            cwd=tmp_path,
            check=True,
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
        )
    except CalledProcessError as e:
        pytest.fail("failed to clone git repo", e)

    project_path = tmp_path / "git-smart"
    try:
        app.git_sync(project_path)
    except CalledProcessError as e:
        pytest.fail("error running git_sync", e)
