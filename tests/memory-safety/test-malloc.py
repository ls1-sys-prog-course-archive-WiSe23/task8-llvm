import subprocess
import pathlib

from testsupport import run_project_executable, subtest, assert_contains


def main() -> None:
    # First make sure in bounds still works
    with subtest("run in bounds"):
        with open(pathlib.Path(__file__).parent.resolve().joinpath("input-1.txt")) as stdin:
            result = run_project_executable("memory-safety/build/malloc-san.out", stdin=stdin, stdout=subprocess.PIPE)
            assert_contains(result.stdout, "Hello normal user Max Mustermann")

    with subtest("run out of bounds"):
        with open(pathlib.Path(__file__).parent.resolve().joinpath("input-2.txt")) as stdin:
            result = run_project_executable("memory-safety/build/malloc-san.out", stdin=stdin, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, check=False)
            if result.returncode == 0:
                raise Exception("Expected program to exit with exit code != 0")
            assert_contains(result.stderr, "Illegal memory access")


if __name__ == "__main__":
    main()
