==========================
File Walker
=========================

This is a collection of simple test programs which walk a filesystem hierarchy.
The same specification is implemented in multiple languages (currently Go,
Java, Ocaml, and Python) to facilitate comparison between the languages. A few
language properties of interest:

* Code organization (classes, functions, interfaces)
* Iteration (loops, recursion, generators)
* Error handling
* POSIX interfaces (in this case, the filesystem)


Specification
=============

Walker Function
---------------
There should be a primary walker function which takes as parameters an
absolute *root* path from where the traversal starts and a set of three callbacks.

This function walks the directory tree and calls the associated callback for each
directory, file, or error. It returns the count of directories encountered
(including the root), a count of files encountered (including any softlinks and
special files), and a count of errors encountered. It passes file `stat`
information to each callback (see below), but should not make any necessary
`lstat()` calls (one per object is all that should be needed).

Softlinks should not be followed -- the file stat information should be for the
link itself and the walker should not walk into links to directories.

To handle especially deep file trees, the file hierarchy should not be stored
on the program stack. This means that languages that do not do a tail recursion
optimization (TCO) must not use recursion.

Callbacks
~~~~~~~~~
The `directory_attributes` callback is to be called for each directory encountered,
the `file_attributes` callback called for each file encountered, and the `error`
callback should be called for each error. The first two callbacks take two parameters:
the path of the object and the file attributes. The file attributes must include
all the attributes of the POSIX `lstat()` system call, including permissions,
user id, group id, timestamps, and flags. The `error` callback takes two parameters:
the path of the object and the exception or error message.

Main Program
------------
The main program should take a required parameter, the root directory, and an
optional second parameter, the number of iterations. The root directory can
be a relative path, which should be converted to an absolute path before passing
it to the walker function. The walker is called the specified number of iterations
and then the results for the last interation are printed.

Errors
------
If the root path is not a directory, inaccessible, or an error occurs obtaining
its file attributes, then the program should exit with an error.

All other errors should be passed to the error callback. Errors may occur when:

* Reading the file listing of a directory (e.g. via `listdir()`)
* Running `stat` on individual files
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
