import subprocess
import statistics

from testsupport import run, subtest, run_project_executable, assert_contains
from time import time

# The instrumented binary should have an overhead of at most 4
MAX_SCALING_FACTOR = 4


def run_perf_test(name: str, n: int, m: int) -> float:
    start = time()
    run_project_executable(name, args=[str(n), str(m)], stdout=subprocess.PIPE)
    end = time()
    return end - start


def main() -> None:
    with subtest("check in bounds"):
        result = run_project_executable("memory-safety/build/performance-san.out", args=["100", "1000", "1"],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        check=False)
        if result.returncode == 0:
            raise Exception("Expected program to exit with exit code != 0")
        assert_contains(result.stderr, "Illegal memory access")

    with subtest("check performance"):
        durations_1 = []
        for i in range(20):
            duration_baseline = run_perf_test("memory-safety/build/performance.out", 1000, 100000)
            duration_san = run_perf_test("memory-safety/build/performance-san.out", 1000, 100000)
            durations_1.append(duration_san / duration_baseline)

        durations_2 = []
        for i in range(20):
            duration_baseline = run_perf_test("memory-safety/build/performance.out", 10000, 10000)
            duration_san = run_perf_test("memory-safety/build/performance-san.out", 10000, 10000)
            durations_2.append(duration_san / duration_baseline)

        scaling_factor = statistics.median(durations_1)
        print(f"Scaling factor: {scaling_factor}")
        if scaling_factor > MAX_SCALING_FACTOR:
            raise Exception(f"Performance test failed: {scaling_factor} < {MAX_SCALING_FACTOR}")

        scaling_factor = statistics.median(durations_2)
        print(f"Scaling factor: {scaling_factor}")
        if scaling_factor > MAX_SCALING_FACTOR:
            raise Exception(f"Performance test failed: {scaling_factor} < {MAX_SCALING_FACTOR}")


if __name__ == "__main__":
    main()
