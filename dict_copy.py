import copy

my_dict = {1:2, 2:3}

copy_dict = copy.deepcopy(my_dict)

my_dict = {9:0}

print(copy_dict)