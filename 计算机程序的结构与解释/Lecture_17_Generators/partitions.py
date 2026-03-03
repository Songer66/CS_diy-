def count_partitions(n,m):
    if n == 0:
        return 1
    if n < 0:
        return 0
    if m == 0:
        return 0
    else:
        with_at_least_m = count_partitions(n-m,m)
        without_m = count_partitions(n,m-1)
        return with_at_least_m + without_m
    
def list_partitions(n,m):
    if n < 0 or m == 0:
        return []
    else:
        exact_match = []
        if n == m:
            exact_match = [[m]]
        with_m = [p + [m] for p in list_partitions(n-m,m)]
        without_m = list_partitions(n,m-1)
        return exact_match + with_m + without_m
    
def string_partitions(n,m):
    if n < 0 or m == 0:
        return []
    else:
        exact_match = []
        if n == m:
            exact_match = [str(m)]
        with_m = [p + ' + ' + str(m) for p in string_partitions(n-m,m)]
        without_m = string_partitions(n,m-1)
        return exact_match + with_m + without_m

def yield_partitions(n,m):
    if n > 0 and m > 0:
        if n == m:
            yield str(m)
        for p in yield_partitions(n-m,m):
            yield str(m) + ' + ' + p
        yield from yield_partitions(n,m-1)

t = yield_partitions(5,3)
for _ in range(4):
    print(next(t))