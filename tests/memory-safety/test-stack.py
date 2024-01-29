import subprocess

from testsupport import run_project_executable, subtest, assert_contains


def main() -> None:
    # First make sure in bounds still works
    with subtest("run in bounds 1"):
        run_project_executable("memory-safety/build/stack-san.out", args=["1"])

    with subtest("run in bounds 2"):
        run_project_executable("memory-safety/build/stack-san.out", args=["31"])

    # out of bounds should fail
    with subtest("run out of bounds"):
        result = run_project_executable("memory-safety/build/stack-san.out", args=["32"], stderr=subprocess.PIPE,
                                        check=False)
        if result.returncode == 0:
            raise Exception("Expected program to exit with exit code != 0")
        assert_contains(result.stderr, "Illegal memory access")

    with subtest("run out of bounds negative"):
        result = run_project_executable("memory-safety/build/stack-san.out", args=["-1"], stderr=subprocess.PIPE,
                                        check=False)
        if result.returncode == 0:
            raise Exception("Expected program to exit with exit code != 0")
        assert_contains(result.stderr, "Illegal memory access")


if __name__ == "__main__":
    main()
