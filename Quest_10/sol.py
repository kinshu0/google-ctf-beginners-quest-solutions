import numpy as np
from matplotlib import pyplot as plt


# for i in range(1, 8):
#     # numpy read csv file

#     data = np.genfromtxt(f'{i}.csv', delimiter=',').transpose()

#     for arr_idx in range(1, len(data)):
#         data[arr_idx] =  data[arr_idx] + -min(data[arr_idx])
#         data[arr_idx] =  (data[arr_idx] * 255/max(data[arr_idx])).astype(int)


#     # fig, axs = plt.subplots(4, sharex=True, figsize=(18,14))

#     # for i in range(1, len(data)):
#     #     axs[i-1].scatter(np.arange(len(data[i])), data[i])

#     # plt.show()

#     for arr_idx in range(1, len(data)):
#         with open(f'{i}_c{arr_idx}.data', 'wb') as f:
#             f.write(data[arr_idx].tobytes())

#     break


for i in range(1, 8):
    with open(f'{i}.csv') as f:
        lines = f.read().split('\n')
    
    c0 = []
    c1 = []
    c2 = []
    c3 = []
    c4 = []

    for line in lines:
        d = line.split(',')
        c0.append(float(d[0]))
        c1.append(float(d[1]))
        c2.append(float(d[2]))
        c3.append(float(d[3]))
        c4.append(float(d[4]))


    for arr in [c1, c2, c3, c4]:
        k = min(arr)
        p = max(arr) + -k
        for z in range(len(arr)):
            arr[z] += -k
            arr[z] *= 255/p

    with open(f'{i}_c1.data', 'wb') as f:
        f.write(bytes([int(x) for x in c1]))
        
    with open(f'{i}_c2.data', 'wb') as f:
        f.write(bytes([int(x) for x in c2]))
        
    with open(f'{i}_c3.data', 'wb') as f:
        f.write(bytes([int(x) for x in c3]))
        
    with open(f'{i}_c4.data', 'wb') as f:
        f.write(bytes([int(x) for x in c4]))
        
    