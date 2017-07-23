from itertools import combinations

numbers = [1,2,3,4]
for item in combinations(numbers, 3):
    print sorted(item)

