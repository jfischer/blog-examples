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
optional second parameter, the number of iterations.


Test Cases
==========
To test the program, the directory tree should have the following
files/directories:

1. Multiple sub-directories with files
2. Softlinks to files (counted as files)
3. Softlinks to directories (counted as files, should not follow the link)
4. Directories with no access (counted as errors)
5. Files with bad unicode characters (should be counted as errors, but aren't!)
