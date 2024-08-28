import subprocess
from subprocess import CalledProcessError

import pytest

from gityup_py.main import (
    check_exec_exists,
    get_git_branch_name,
    git_remote_exists,
    git_status_clean,
    git_sync,
    is_git,
    parse_args,
)


def test_check_exec_exists():
    assert check_exec_exists("python")


def test_check_exec_exists_fail():
    assert not check_exec_exists("flubber")


def test_parse_args():
    home_path = parse_args("~")
    assert home_path.is_absolute()


def test_parse_args_fail():
    with pytest.raises(ValueError, match="Given path '/does/not/exist' is not an existing directory."):
        parse_args("/does/not/exist")


def test_is_git_dir(tmp_path):
    subprocess.run("git init >/dev/null", cwd=tmp_path, shell=True, check=True)
    assert is_git(tmp_path)


def test_is_git_dir_fail(tmp_path):
    assert not is_git(tmp_path)


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
    assert git_status_clean(tmp_path)


def test_git_status_clean_fail(tmp_path):
    subprocess.run("git init >/dev/null; echo 'hello' > test.txt", cwd=tmp_path, shell=True, check=True)
    assert not git_status_clean(tmp_path)


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
    branch_name = get_git_branch_name(tmp_path)
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
    assert git_remote_exists(project_path, "master")


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
        git_sync(project_path)
    except CalledProcessError as e:
        pytest.fail("error running git_sync", e)
