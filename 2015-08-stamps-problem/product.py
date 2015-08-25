"""vector-product-based solver for stamps problem.
"""
from itertools import product

STAMP_SIZES = (50, 22, 10)

def product_solve(value, stamp_sizes=STAMP_SIZES):
    iterators = [range((value/s)+1) for s in stamp_sizes]
    best_result = None
    for p in product(*iterators):
        # Each p is an array with the length equal to len(stamp_sizes), where
        # p[i] is the count to be used for stamp_sizes[i]
        total = 0
        result_len = 0
        for (i, cnt) in enumerate(p):
            stamp_value = cnt * stamp_sizes[i]
            total += stamp_value
            result_len += cnt
            if total>value:
                break
        if total==value:
            # we have a solution
            if best_result is None or result_len<len(best_result):
                # new best result - build up the array
                best_result = []
                for (i, cnt) in enumerate(p):
                    best_result.extend([stamp_sizes[i],]*cnt)
    return best_result

if __name__=="__main__":
    import sys
    value = int(sys.argv[1])
    print "solution for %s is %s" % (value, product_solve(value, STAMP_SIZES))

