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

## Usage

To use the tool, use `clang++` as you normally would except add the flags
`-fsanitize=const -g`. Note that it is also helpful to disable optimizations
and include the frame pointer with `-O0 -fno-omit-frame-pointer`. To run the
example given in Listing 1 of the paper, do the following:

    cd ~/examples
    clang++ -std=c++11 -fsanitize=const -g listing-1.cpp

Then you can run the resulting executable with `./a.out` and you should see a
warning. To write to an external log file, use the `log_path` option. For
example, to log the results to a file called `listing-1.log` do the following:

    CSAN_OPTIONS=log_path=listing-1.log ./a.out

After running the program again, there should be no extra output on `stderr`
and there should be a `listing-1.log.XXXXX` file in the current directory where
`XXXXX` are random numbers.

## Experiments

All experiments are located in the `experiments` directory. To instrument a
package, for example `ninja`, do the following:

    cd ~/experiements
    python build.py ninja

Any violations that occur during build time are located in the `experiments`
directory in a file named `PACKAGE-build.log`. To create the groupings for
manually inspection run `python group.py ninja`. The `group.py` script collects
all results from log files with the specified project name.

## Results

Our results are in the `results` directory, organized by project name. These
files represent our findings organized by manually categorizing the violations
and putting them all under the same heading. The remaining results show the
number of violations at each source location. These violations are annotated
with source locations.
