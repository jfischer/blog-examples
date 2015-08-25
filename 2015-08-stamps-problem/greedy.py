"""Greedy implementation for stamps.
"""

STAMP_SIZES = (50, 22, 10)

def greedy_solve(value, stamp_sizes=STAMP_SIZES):
    """Find the minimal list of stamps which add up the value, where
    stamps may have face values taken from stamp sizes.
    """
    stamp_sizes = sorted(stamp_sizes, reverse=True) # want to check in descending order
    stamps = []
    total = 0
    for face_value in stamp_sizes:
        # Compute the most stamps of the value whose total
        # is below the amount left
        cnt = (value-total)/face_value
        if cnt==0:
            continue
        stamps.extend([face_value]*cnt) # repeat the current value cnt times
        total += (cnt*face_value)
        if total==value:
            return stamps

if __name__=="__main__":
    import sys
    value = int(sys.argv[1])
    print "solution for %s is %s" % (value, greedy_solve(value, STAMP_SIZES))
