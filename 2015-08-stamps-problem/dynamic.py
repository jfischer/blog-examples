"""Dynamic programming solver for stamps problem.
    1. Break the problem into smaller subproblems
    2. Remember the results of the subproblems to avoid recalculation
    
    We exploit symmetry in the optimal solutions due to the associative
    probpery of addition. If [S_a1, ..., S_an] and [S_b1, ..., S_bn] are
    both optimal solutions to V1 and [S_a1, ..., S_an, V2-V1] is an
    optimal solution to V2, then [S_b1, ..., S_bn, V2-V1] is also an optimal
    solution to V2. In other words, optimal solutions to subproblems are
    interchangable.
"""

STAMP_SIZES = (50, 22, 10)

def dynamic_solve(value, stamp_sizes=STAMP_SIZES):
    """Dynamic programming solution to stamps problem:
    """
    # map from value to best solution so far for that value
    best_so_far = {s:[s,] for s in stamp_sizes}
    # base case
    if value in best_so_far:
        return [value,]
    new_cases_added = True
    # We start with the base cases and keep increasing the length of the
    # solutions by one. If we increase the length and find no new optimal
    # solutions below the value, then no solution exists.
    while new_cases_added:
        new_cases_added = False
        for s in stamp_sizes:
            for v in best_so_far.keys():
                subtotal = v+s
                if subtotal==value:
                    return best_so_far[v] + [s,]
                elif subtotal<value and (subtotal not in best_so_far):
                    best_so_far[subtotal] = best_so_far[v] + [s,]
                    new_cases_added = True
    return None # no solution found


if __name__=="__main__":
    import sys
    value = int(sys.argv[1])
    print "solution for %s is %s" % (value, dynamic_solve(value, STAMP_SIZES))

            
