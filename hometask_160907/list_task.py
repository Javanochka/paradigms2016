# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    return list(set(lst))
 
# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    res = []
    i2 = 0
    for el in lst1:
        while i2 < len(lst2) and lst2[i2] <= el:
            res += [lst2[i2]]
            i2 += 1
        res += [el]
    while i2 < len(lst2):
        res += [lst2[i2]]
        i2 += 1
    return res
