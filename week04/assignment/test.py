import random
test = [20,13,4,8,3,11,16,19,24]


target_number = 54

count = 0

test1 = test.copy()
bag = []

while sum(bag) != target_number:
    if sum(bag) < target_number:
        rm = random.choice(test1)
        test1.remove(rm)
        bag.append(rm)
    elif sum(bag) > target_number:
        rm = random.choice(bag)
        bag.remove(rm)
        test1.append(rm)
        # test1.append(bag.remove(random.choice(bag)))
    print(sum(bag))
    count += 1
print(count)
print(bag)


# test.sort()
# while sum(bag) != target_number:
    
    
    
    
#     if sum(bag) < target_number:
#         rm = random.choice(test1)
#         test.remove(rm)
#         bag.append(rm)
#     elif sum(bag) > target_number:
#         rm = random.choice(bag)
#         bag.remove(rm)
#         test.append(rm)
#         # test1.append(bag.remove(random.choice(bag)))
#     print(sum(bag))
#     count += 1


# # def recurson_test(bag, list_left):
# #     if sum(bag) == 64:
# #         return bag, len(bag)
# #     elif sum(bag) > 64:
# #         return False
# #     else:
# #         bag
