import shutil
import subprocess
from pathlib import Path
from subprocess import CalledProcessError

import typer


def git_remote_exists(project: Path, branch: str):
    working_dir = project.expanduser().resolve()
    remote_config = f"branch.{branch}.remote"
    try:
        subprocess.run(
            ["git", "config", remote_config],
            cwd=working_dir,
            capture_output=True,
            check=True,
        )
        return True
    except CalledProcessError:
        return False


def git_sync(project: Path):
    working_dir = project.expanduser().resolve()
    r1 = subprocess.run(["git", "smart-pull"], cwd=working_dir)
    r1.check_returncode()
    r2 = subprocess.run(["git", "remote", "update", "origin", "--prune"], cwd=working_dir)
    r2.check_returncode()


def get_git_branch_name(project: Path):
    working_dir = project.expanduser().resolve()
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=working_dir,
        capture_output=True,
        text=True,
    )
    result.check_returncode()
    return result.stdout.strip()


def git_status_clean(project: Path):
    working_dir = project.expanduser().resolve()
    try:
        subprocess.run("git status | grep 'nothing to commit' >/dev/null", cwd=working_dir, check=True, shell=True)
        return True
    except CalledProcessError:
        return False


def is_git(a_dir: Path):
    x = a_dir.expanduser().resolve() / ".git"
    return x.exists() and x.is_dir()


def update_projects(root_path: Path):
    for child in root_path.iterdir():
        if child.is_dir() and is_git(child):
            if not git_status_clean(child):
                print(f"local changes detected, skipping {child}")
            else:
                branch = get_git_branch_name(child)
                if len(branch) == 0:
                    print("#### detached HEAD state, skipping ####")
                else:
                    if not git_remote_exists(child, branch):
                        print(f"no remote to pull from, skipping {child}")
                    else:
                        print(f"#### pulling {child} ####")
                        git_sync(child)
                        print("")


def check_exec_exists(binary: str):
    e = shutil.which(binary)
    return e is not None


def parse_args(root: str):
    p = Path(root).expanduser().resolve()
    if p.exists() and p.is_dir():
        return p.absolute()
    else:
        msg = f"Given path '{root}' is not an existing directory."
        raise ValueError(msg)


def main(root_dir: str):
    the_path = parse_args(root_dir)
    check_exec_exists("git")
    check_exec_exists("git-smart-pull")
    update_projects(the_path)


if __name__ == "__main__":
    typer.run(main)
