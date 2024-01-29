import subprocess

from testsupport import run_project_executable, subtest, assert_contains


def main() -> None:
    # First make sure in bounds still works
    with subtest("run in bounds"):
        run_project_executable("memory-safety/build/use-after-free-san.out", args=[])

    with subtest("run out of bounds"):
        result = run_project_executable("memory-safety/build/use-after-free-san.out", args=[""], stderr=subprocess.PIPE,
                                        check=False)
        if result.returncode == 0:
            raise Exception("Expected program to exit with exit code != 0")
        assert_contains(result.stderr, "Illegal memory access")


if __name__ == "__main__":
    main()
