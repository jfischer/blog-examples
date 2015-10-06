import logging
import sys
import os
from os.path import exists, abspath, expanduser,isdir,join
from stat import S_ISDIR, S_ISLNK
from collections import deque

class SimpleCallbacks(object):
    def file_attributes(self, path, attrs):
        pass
    def directory_attributes(self, path, attrs):
        pass
    def error(self, path, exc):
        pass
        #sys.stderr.write("Error on file %s: '%s'\n" % (path, exc))


def get_files_and_stats_for_dir(dpath):
    """Generator that returns a sequence of pairs.
    Each pair is a file path and the associated stats. If there
    is an error, it instead yields a pair of the path and the exception.
    """
    try:
        names = os.listdir(dpath)
    except Exception, e:
        yield (dpath, e)
        return # done with the sequence
    for name in names:
        try:
            #p = join(dpath, unicode(name, 'utf-8', errors='replace'))
            p = join(dpath, unicode(name))
        except Exception, e:
            yield (dpath, e)
            continue
        try:
            stats = os.lstat(p)
        except Exception, e:
            yield (p, e)
        else:
            yield (p, stats)

    
def walk(root, callbacks):
    try:
        root_stats = os.lstat(root)
    except Exception, e:
        callbacks.error(root, e)
        return (0, 0, 1)
    callbacks.directory_attributes(root, root_stats)
    dirs = 1
    files = 0
    errors = 0
    work_q = deque([root,])
    while len(work_q)>0:
        d = work_q.popleft()
        for (p, s) in get_files_and_stats_for_dir(d):
            if isinstance(s, Exception):
                callbacks.error(p, s)
                errors += 1
            elif S_ISDIR(s.st_mode) and not S_ISLNK(s.st_mode):
                callbacks.directory_attributes(p, s)
                dirs += 1
                work_q.append(p)
            else:
                callbacks.file_attributes(p, s)
                files += 1
    return (dirs, files, errors)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    if len(sys.argv)!=2 and len(sys.argv)!=3:
        sys.stderr.write("%s ROOT_DIRECTORY [REPEAT_COUNT]\n" % sys.argv[0])
        sys.exit(1)
    root_dir = unicode(abspath(expanduser(sys.argv[1])))
    if len(sys.argv)==3:
        repeat_count = int(sys.argv[2])
    else:
        repeat_count = 1
    if not isdir(root_dir):
        sys.stderr.write("Root directory %s is invalid\n" % root_dir)
        sys.exit(1)
    print "starting at %s" % root_dir
    for i in range(repeat_count):
        print "Iteration %d..." % (i+1)
        (dirs, files, errors) = walk(root_dir, SimpleCallbacks())
    print "directories = %d, files = %d, errors = %d" % \
        (dirs, files, errors)
    sys.exit(0)
