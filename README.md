# ECOOP 2016 Artifact

## Building

Ensure you have the `base-devel` group installed and the `multilib` repository
enabled. Afterwards you can build the package in the standard Arch Linux
fashion:

    cd ~/abs
    makepkg -s

## Testing

There are 16 small test cases you run to ensure the tool works correctly.
Navigate to the test directory if you wish to see these tests:

    cd ~/abs/src/llvm-csan-0.0.1/projects/compiler-rt/test/csan

The expected test results are embedded within the source files themselves. Any
lines with `CHECK` are expected to occur on `stderr` when the source file is
compiled and run with our tool enabled. Any lines beginning with `CHECK-NOT`
should not occur when our tool is used. To run all the tests do the following:

    cd ~/abs/src/llvm-csan-0.0.1/build
    make check-csan

## Results

Our results are in the `results` directory, organized by project name. These
files represent our findings organized by manually categorizing the violations
and putting them all under the same heading. The remaining results show the
number of violations at each source location. These violations are annotated
with source locations.
