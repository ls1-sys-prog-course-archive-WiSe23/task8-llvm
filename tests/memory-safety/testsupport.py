import string
import sys

if sys.version_info < (3, 7):
    print("This module assumes at least python 3.7", file=sys.stderr)
    raise Exception("python too old")

import io
import os
import subprocess
from pathlib import Path
from shlex import quote
from tempfile import NamedTemporaryFile
from typing import (
    IO,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Text,
    Union,
    Iterator,
    NoReturn,
)
from inspect import getframeinfo, stack
from contextlib import contextmanager
from urllib.request import urlopen  # Python 3

TEST_ROOT = Path(__file__).parent.resolve()
PROJECT_ROOT = TEST_ROOT.parent
HAS_TTY = sys.stderr.isatty()


def test_root() -> Path:
    """
    Path to test directory
    """
    return TEST_ROOT


def project_root() -> Path:
    """
    Path to project directory
    """
    return PROJECT_ROOT


def fail(msg: str) -> NoReturn:
    """
    Fail test with given error message
    """
    warn(msg)
    sys.exit(1)
    raise Exception("BUG! should not happen")


def assert_executable(executable: str, msg: str, path: Optional[str] = None) -> None:
    """
    exits if program does not exists
    """
    if not find_executable(executable, path):
        fail(msg)


def ensure_library(name: str, msg: Optional[str] = None) -> Path:
    p = find_library(name)
    if not p:
        if msg is None:
            fail(f"Cannot find library {name}")
        else:
            fail(msg)
    return p


def color_text(code: int, file: IO[Any] = sys.stdout) -> Callable[[str], None]:
    """
    Print with color if stderr is a tty
    """

    def wrapper(text: str) -> None:
        if HAS_TTY:
            print(f"\x1b[{code}m{text}\x1b[0m", file=file)
        else:
            print(text, file=file)

    return wrapper


warn = color_text(91, file=sys.stderr)
info = color_text(92, file=sys.stderr)


def find_executable(executable: str, path: Optional[str] = None) -> Optional[str]:
    """Find if 'executable' can be run. Looks for it in 'path'
    (string that lists directories separated by 'os.pathsep';
    defaults to os.environ['PATH']). Checks for all executable
    extensions. Returns full path or None if no command is found.
    """
    if path is None:
        path = os.environ["PATH"]
    paths = path.split(os.pathsep)
    extlist = [""]
    if os.name == "os2":
        (base, ext) = os.path.splitext(executable)
        # executable files on OS/2 can have an arbitrary extension, but
        # .exe is automatically appended if no dot is present in the name
        if not ext:
            executable = executable + ".exe"
    elif sys.platform == "win32":
        pathext = os.environ["PATHEXT"].lower().split(os.pathsep)
        (base, ext) = os.path.splitext(executable)
        if ext.lower() not in pathext:
            extlist = pathext
        # Windows looks for binaries in current dir first
        paths.insert(0, "")

    for ext in extlist:
        execname = executable + ext
        for p in paths:
            f = os.path.join(p, execname)
            if os.path.isfile(f):
                return f
    else:
        return None


def project_dirs() -> List[Path]:
    dirs = [
        # Add project root to PATH
        PROJECT_ROOT,
        # add Rust release directory
        PROJECT_ROOT.joinpath("target", "release"),
        # add Rust debug directory
        PROJECT_ROOT.joinpath("target", "debug"),
    ]
    return dirs


def find_library(name: str, dirs: List[Path] = project_dirs()) -> Optional[Path]:
    for dir in dirs:
        libpath = dir.joinpath(name)
        if libpath.exists():
            return libpath
    return None


def project_path() -> str:
    dirs = project_dirs()
    return os.pathsep.join(map(str, dirs))


_FILE = Union[None, int, IO[Any]]


def find_project_executable(exe: str) -> str:
    path = project_path()
    fullpath = find_executable(exe, path)
    if fullpath is not None:
        return fullpath
    paths = path.split(os.pathsep)
    locations = "\n  ".join(os.path.join(path, exe) for path in paths)

    raise OSError(
        f"executable '{exe}' not found. The following locations where considered:\n  {locations}"
    )


def run_project_executable(
        exe: str,
        args: List[str] = [],
        extra_env: Dict[str, str] = {},
        stdin: _FILE = None,
        stdout: _FILE = None,
        stderr: _FILE = None,
        input: Optional[str] = None,
        timeout: Optional[int] = None,
        check: bool = True,
) -> "subprocess.CompletedProcess[Text]":
    return run(
        [find_project_executable(exe)] + args,
        extra_env,
        stdin,
        stdout,
        stderr,
        input=input,
        check=check,
        timeout=timeout,
    )


def run(
        cmd: List[str],
        extra_env: Dict[str, str] = {},
        stdin: _FILE = None,
        stdout: _FILE = None,
        stderr: _FILE = None,
        input: Optional[str] = None,
        timeout: Optional[int] = None,
        check: bool = True,
        shell: bool = False,
) -> "subprocess.CompletedProcess[Text]":
    """
    Run a program while also pretty print the command that it runs
    """
    env = os.environ.copy()
    env.update(extra_env)
    env_string = []
    for k, v in extra_env.items():
        env_string.append(f"{k}={v}")
    pretty_cmd = "$ "
    if input is not None:
        pretty_cmd += f"echo {quote(input)} | "
    if len(extra_env) > 0:
        pretty_cmd += " ".join(env_string) + " "
    if shell:
        pretty_cmd += "sh -c "
    pretty_cmd += " ".join(map(quote, cmd))
    if isinstance(stdin, io.IOBase):
        pretty_cmd += f" < {stdin.name}"
    if isinstance(stdout, io.IOBase):
        pretty_cmd += f" > {stdout.name}"
    if isinstance(stderr, io.IOBase):
        pretty_cmd += f" 2> {stderr.name}"
    info(pretty_cmd)
    return subprocess.run(
        cmd[0] if shell else cmd,
        cwd=PROJECT_ROOT,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        timeout=timeout,
        check=check,
        env=env,
        text=True,
        input=input,
        shell=shell,
    )


def ensure_download(url: str, dest: Path) -> None:
    """
    Download `url` to `dest` if dest does not exists yet
    """
    if dest.exists():
        return
    download(url, dest)


def assert_contains(haystack: str, needle: str) -> None:
    if not haystack.__contains__(needle):
        raise Exception(f"Could not find '{needle}' in program output")


@contextmanager
def subtest(msg: str) -> Iterator[None]:
    """
    Run a subtest, if it fails it will exit the program while printing the error
    """
    caller = getframeinfo(stack()[2][0])
    info(msg + "...")
    try:
        yield
    except Exception as e:
        fail(f"`{msg}` at {caller.filename}:{caller.lineno} failed with: {e}")


def download(url: str, dest: Path) -> None:
    """
    Download `url` to `dest`
    """
    info(f"download {url} to {dest}...")
    response = urlopen(url)
    temp = NamedTemporaryFile(dir=dest.parent, delete=False)
    try:
        while True:
            chunk = response.read(16 * 1024)
            if not chunk:
                break
            temp.write(chunk)
        os.rename(temp.name, dest)
    finally:
        if os.path.exists(temp.name):
            os.unlink(temp.name)
