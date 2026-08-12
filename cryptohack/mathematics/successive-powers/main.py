nums = [588,665,216,113,642,4,836,114,851,492,819,237]

'''
a^x = a0 (mod p)
-> forall 3 digits p: > 851,
a^x = 588

a^(x+1) = 655
...
a^(x+n) = 237
**insight:
a^x * (a^(-x-1)) = a^(-1) mod p ->
found a.
'''
from sage.all import *

for p in range(851, 999):
    try:
        invs = pow(nums[0], -1, p)
        a = pow(invs*nums[1], 1, p)
        for i in range(0, len(nums)-1):
            flag = True
            if pow(a*nums[i], 1, p) != nums[i+1]:
                flag = False
            else:
                print(nums[i+1])
        if flag == True:
            print(p)
            print("!")
            print(a)
            break
    except:
        continue
