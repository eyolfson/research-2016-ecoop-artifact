# ECOOP 2016 Artifact

There is an example virtual machine located at
`http://laforge.cs.uwaterloo.ca/ecoop-2016.qcow2` already setup. The username
and password to this VM are both `ecoop-2016`. To run the VM, for example with
QEMU, do the following:

    qemu-system-x86_64 -enable-kvm -m 2048 -drive file=ecoop-2016.qcow2,format=qcow2

The login information you'll always want to use is:

    Username: ecoop-2016
    Password: ecoop-2016

This VM should have all the requirements needed to run all of the experiments.
If you want to SSH into the VM from your host, use the following:

    qemu-system-x86_64 -enable-kvm -m 2048 -drive file=ecoop-2016.qcow2,format=qcow2 -net user,hostfwd=tcp::10022-:22 -net nic

Then from your host machine do:

    ssh ecoop-2016@localhost -p10022

## Building (Optional)

If you are using the VM image that we've distributed, the `clang`
executable on that VM points to a prebuilt version of our
tool. However, we've included the sources and you can build your own
`clang` from scratch as follows.

Ensure you have the `base-devel` group installed and the `multilib` repository
enabled. Afterwards you can build the package in the standard Arch Linux
fashion:

    cd ~/abs
    makepkg -s

After building the tool, you can use our set of 16 small test cases
you run to ensure the tool works correctly. Navigate to the test
directory to see these tests:

    cd ~/abs/src/llvm-csan-0.0.1/projects/compiler-rt/test/csan

Note: if you haven't built the tool, this directory will not exist, do the
following first:

    cd ~/abs
    makepkg -o

The expected test results are embedded within the source files themselves. Any
lines with `CHECK` are expected to occur on `stderr` when the source file is
compiled and run with our tool enabled. Any lines beginning with `CHECK-NOT`
should not occur when our tool is used. To run all the tests do the following:

    cd ~/abs/src/llvm-csan-0.0.1/build
    make check-csan

Note that you must have built the tool in order to run `make check-csan`!

### Manually Running Tests

Instead of automatically running the tests with `make check-csan` (and not getting much feedback,
due to the LLVM testing framework), you can also manually run the tests. You do need to
`cd ~/abs; makepkg -o` as described above, though.

To manually run them yourself do the following:

    cd ~
    clang -fsanitize=const -g ~/abs/src/llvm-csan-0.0.1/projects/compiler-rt/test/csan/const-object.cc -o const-object
    ./const-object

You may explore all the other tests by exploring
`~/abs/src/llvm-csan-0.0.1/projects/compiler-rt/test/csan` and running them in
a similar manner.

## Usage

To use the tool, use `clang++` as you normally would, but add the
flags `-fsanitize=const -g`. You should get more precise results if
you disable optimizations and include the frame pointer with `-O0
-fno-omit-frame-pointer`. To run the example given in Listing 1 of the
paper, do the following:

    cd ~/examples
    clang++ -std=c++11 -fsanitize=const -g listing-1.cpp

You can run the resulting executable as `./a.out` and you should see a
warning. To write to an external log file, use the `log_path` option. For
example, to log the results to a file called `listing-1.log` do the following:

    CSAN_OPTIONS=log_path=listing-1.log ./a.out

After running the program again, there should be no extra output on `stderr`
and there should be a `listing-1.log.XXXXX` file in the current directory where
`XXXXX` are random numbers. Feel free to try it out!

## Experiments

All experiments are located in the `experiments` directory. To instrument a
package, for example Ninja, do the following:

    cd ~/experiments
    python build.py ninja

Any violations that occur during build time are located in the `experiments`
directory in a file named `PACKAGE-build.log`. To create the groupings for
manual inspection run `python group.py ninja`. The `group.py` script collects
all results from log files with the specified project name. Some projects run
tests as part of their build process (like Ninja) and the results are already
available to go over.

The next subsections give examples of how we obtained our results in the paper.

### Ninja

In this case, as part of the build process, the tests are run. Therefore the
`ninja-build.log.XXXXX` show what violations occur as part of the test suite.
If you open this file and observe it, the first non-standard library portion of
the stack trace should be in `src/disk_interface_test.cc:226:3` matching the
results of the paper. There should be 4 unique source locations, starting in
the standard libary, for all violations. To determine them, which is done for
all other experiements, do the following:

    cd ~/experiments
    python group.py ninja-build

This should group the raw results into unique locations and also give the
dynamic violation count.

### Fish

    cd ~/experiments
    python build.py fish
    CSAN_OPTIONS=log_path=fish.log fish/pkg/fish/usr/bin/fish

Then press control-D to exit. Afterwards you can do the same as with Ninja:

    python group.py fish

These results should correspond to the paper.

### Mosh

    cd ~/experiments
    python build.py mosh
    CSAN_OPTIONS=log_path=mosh.log mosh/pkg/mosh/usr/bin/mosh-server
    pkill mosh-server

Again, similar to the last case, use the group script:

    python group.py mosh

These results should correspond to the paper.

### LLVM

Similar to before, LLVM compiles `llvm-tblgen` and executes it as part of its
build process. Therefore after running the build script the results should be
accessible with:

    cd ~/experiments
    python group.py llvm-build

### Wayland / Weston

First build Wayland and install the package:

    cd ~/experiments
    python build.py wayland
    sudo pacman -U wayland/wayland-1.9.0-1-x86_64.pkg.tar.xz

Then you can build weston:

    python build.py weston

Again, run the produced executable:

    CSAN_OPTIONS=log_path=weston.log weston/pkg/weston/usr/bin/weston

### Tesseract

Similar to Fish, you may need to also include `LD_LIBRARY_PATH` like so:

    CSAN_OPTIONS=log_path=tesseract.log LD_LIBRARY_PATH=pkg/tesseract/usr/lib pkg/tesseract/usr/bin/tesseract

### LevelDB

Similar to LLVM, tests are run as part of the build process.

### Protobuf

Similar to LLVM, tests are run as part of the build process.

## Timing

To collect the timing results, for example for Protobuf, do the following:

    cd ~/experiments
    python time.py protobuf

Note that you'll have to clear all the build files between each run. Do that
with the following command (you need to `cd` into the project directory first).

    cd ~/experiments/protobuf
    rm -rf src pkg *.pkg.tar.xz

The resulting files will be in `/tmp/time-protobuf-build` and
`/tmp/time-protobuf-check`. The last 3 lines of the first file indicate how
long it took to build with the tool enabled. The last 3 lines of the second
file indicate how long it took to run the tests with the tool enabled. After
recording these numbers you can do the same procedure with the tool disabled.
To collect the timing (after cleaning) results do:

    cd ~/experiments
    python time-disable-csan.py protobuf

## Results

Our results are in the `results` directory, organized by project name. These
files represent our findings organized by manually categorizing the violations
and putting them all under the same heading. The remaining results show the
number of violations at each source location. These violations are annotated
with source locations.
