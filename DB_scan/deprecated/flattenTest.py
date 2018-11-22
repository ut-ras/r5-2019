import numpy as np
import sys

def search_ref(objID, startID, eq_list):
    if eq_list[objID-1] == objID:
        eq_list[startID-1] = objID
    else:
        objID = eq_list[objID-1]
        search_ref(objID, startID, eq_list)
    return eq_list

def flatten_list(eq_list):
    for elem in range(1, len(eq_list)+1):
        print("Flattening: {elem}".format(elem=elem))
        search_ref(elem, elem, eq_list)
    return eq_list

idx_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
test_list = [1, 2, 2, 1, 3, 4, 7, 5, 8]
end_list = [1, 2, 2, 1, 2, 1, 7, 2, 2]

print(test_list)
output = flatten_list(test_list)
print(end_list)
print(output)
