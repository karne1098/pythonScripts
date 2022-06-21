test1 = "2.4K Subscribers"
test2 = "1M subscribers"
import numpy as np

fc1 = test1.split(" ")[0]
print(fc1)

ls = []

ls.append(1)
ls.append(2)
ls.append(3)
ls.insert(0, "followers")

print(ls)

data_ex = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
x = np.array(data_ex)[:, :2]
print(x)
