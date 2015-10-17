===========
File Walker
===========

This is a collection of simple test programs which walk a filesystem hierarchy.
The same specification is implemented in multiple languages (currently Go,
Java, Ocaml, and Python) to facilitate comparison between the languages. A few
language properties of interest:

* Code organization (classes, functions, interfaces)
* Iteration (loops, recursion, generators)
* Error handling
* POSIX interfaces (in this case, the filesystem)

Building
========
This has only been tested on Ubuntu.

Prerequisites
-------------
To compile everything, you will need to install the Java 7 JDK, the Go compiler,
and the OCaml compiler.

The OCaml version of the walker will also need the ocaml-findlib package and the
OCaml fileutils library available at
https://forge.ocamlcore.org/projects/ocaml-fileutils/. Follow the instructions
in the INSTALL.txt file to build and install it. I tested with version 0.5.0.

When all the dependencies have been installed, you can run ``make all`` to compile
the code. To test run everything against your home directory, run ``make test``.


Specification
=============

Walker Function
---------------
There should be a primary walker function which takes as parameters an
absolute *root* path from where the traversal starts and a set of three callbacks.

This function walks the directory tree and calls the associated callback for each
directory, file, or error. It returns the count of directories encountered
(including the root), a count of files encountered (including any softlinks and
special files), and a count of errors encountered. It passes file ``stat``
information to each callback (see below), but should not make any necessary
``lstat()`` calls (one per object is all that should be needed).

Softlinks should not be followed -- the file stat information should be for the
link itself and the walker should not walk into links to directories.

To handle especially deep file trees, the file hierarchy should not be stored
on the program stack. This means that languages that do not do a tail recursion
optimization (TCO) must not use recursion.

Callbacks
~~~~~~~~~
The ``directory_attributes`` callback is to be called for each directory
encountered, the ``file_attributes`` callback called for each file encountered,
and the ``error`` callback should be called for each error. The first two
callbacks take two parameters: the path of the object and the file attributes.
The file attributes must include all the attributes of the POSIX ``lstat()``
system call, including permissions, user id, group id, timestamps, and flags.
The ``error`` callback takes two parameters: the path of the object and the
exception or error message.

Main Program
------------
The main program should take a required parameter, the root directory, and an
optional second parameter, the number of iterations. The root directory can
be a relative path, which should be converted to an absolute path before passing
it to the walker function. The walker is called the specified number of iterations
and then the results for the last interation are printed.

The main program must pass a set of callbaks to the walker function. We will just
pass in a set of callbacks that do nothing.

Errors
------
If the root path is not a directory, inaccessible, or an error occurs obtaining
its file attributes, then the program should exit with an error.

All other errors should be passed to the error callback. Errors may occur when:

* Reading the file listing of a directory (e.g. via ``readdir()``)
* Running ``stat`` on individual files
* Path manipulation (e.g. Python has problems with this if the path contains
  invalid characters for UTF-8).


Test Cases
==========
To test the program, the directory tree should have the following
files/directories:

1. Multiple sub-directories with files
2. Softlinks to files (counted as files)
3. Softlinks to directories (counted as files, should not follow the link)
4. Directories with no access (counted as errors)
5. Files with bad unicode characters (should at least not fail on them)


Performance
===========
I ran two sets of tests, one walking the local filesystem of a VM on my
laptop and one walking an NFS server over the network. The NFS requests
should take more time, so one would expect those tests to be more
I/O bound.

I ran the Go tests with both the Go 1.4 and the Go 1.5 compilers, just
because I had the 1.4 compiler handy at the time. As you will see, there
was a non-trivial peformance improvement from 1.4 to 1.5.


Local Tests
-----------
The local tests were run in an Ubuntu 14.04 Virtual Machine with 2 virtual
cores that was running on a Macbook pro with a 2 GHz Intel Core i7 processor
and all-flash storage. The entire root filesystem on the VM was walked.
There were approximately 74k directories, 604k files, and 1 error (the
results would vary slightly for each run). Since the scans complete quickly,
I ran the walkers with an *interation* parameter of 10. I ran each walker 
three times (for a total of 30 walks per walker). I then took the mean and
standard deviation of the three runs for each walker.

+------------+------------+------------+------------+----------+---------+
| Language   | Time 1 (s) | Time 2 (s) | Time 3 (s) | Mean (s) | Std Dev |
+============+============+============+============+==========+=========+
| Python 2.7 |     35.603 |     35.171 |     33.786 |     34.9 |    0.78 |
+------------+------------+------------+------------+----------+---------+
| Java 7     |     16.376 |     14.525 |     14.388 |     15.1 |    0.91 |
+------------+------------+------------+------------+----------+---------+
| Go 1.4     |     25.219 |     25.114 |     24.905 |     25.1 |    0.13 |
+------------+------------+------------+------------+----------+---------+
| Go 1.5     |     18.393 |     18.291 |     18.241 |     18.3 |    0.06 |
+------------+------------+------------+------------+----------+---------+
| OCaml 4.01 |     11.244 |     11.040 |     11.161 |     11.1 |    0.08 |
+------------+------------+------------+------------+----------+---------+


NFS Tests
---------
The NFS tests were run in an Ubuntu 14.04 Virtual Machine with 2 virtual cores
that was running on a 2.67Ghz, 6 core Intel Xeon X5650 processor. The storage,
accessed over a network, uses spinning drives in a RAID 7 configuration.
The directory tree walked included 10k directories, 5 million files, and no
errors.

I ran the walkers with an *iteration* parameter of 1. I ran each walker 3
times, and then took the mean and standard deviation.

+------------+----------+----------+----------+----------+----------+
| Language   |   Time 1 |   Time 2 |   Time 3 |     Mean |  Std Dev |
+============+==========+==========+==========+==========+==========+
| Python 2.7 |  44m 09s |  43m 56s |  42m 59s |  43m 41s |   0m 30s |
+------------+----------+----------+----------+----------+----------+
| Java 7     |  41m 12s |  42m 26s |  42m 50s |  42m 09s |   0m 42s |
+------------+----------+----------+----------+----------+----------+
| Go 1.4     |  40m 10s |  40m 33s |  39m 48s |  40m 10s |   0m 18s |
+------------+----------+----------+----------+----------+----------+
| Go 1.5     |  42m 03s |  41m 39s |  41m 18s |  41m 40s |   0m 18s |
+------------+----------+----------+----------+----------+----------+
| OCaml 4.01 |  41m 29s |  40m 51s |  40m 56s |  41m 05s |   0m 17s |
+------------+----------+----------+----------+----------+----------+

