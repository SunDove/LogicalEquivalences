import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

def removeOutliers(arr):
    arr = np.array(arr)
    up = np.percentile(arr, 75)
    lo = np.percentile(arr, 25)
    iqr = up-lo
    up += iqr*1.5
    lo -= iqr*1.5
    ret = []
    for n in arr:
        if n<=up and n>=lo:
            ret.append(n)
    return ret


def main():

    with open('depthlimit.json', 'r') as file:
        data = json.loads(file.read())
    avgs = []
    for i in range(5, 26):
        a = data[str(i)]
        #a = removeOutliers(a)
        avgs.append(np.median(a))
    df = pd.DataFrame(data)
    print(avgs)
    plt.plot(avgs)
    plt.xticks(range(21), range(5, 26))
    plt.xlabel('Depth Limit')
    plt.ylabel('Average Runtime (seconds)')
    plt.title('Results Of Depth Limit Search')
    plt.show()


    with open('mL_res.json', 'r') as file:
        data = json.loads(file.read())
    avgs = []
    for i in range(20):
        a = data[str(i)]
        a = removeOutliers(a)
        avgs.append(np.mean(a))
    plt.plot(avgs)
    plt.xticks(range(20), range(1, 21))
    plt.xlabel('Generation')
    plt.ylabel('Average Runtime (seconds)')
    plt.title('Results Of Learning Heuristic Weights')
    plt.show()

    '''
    for i in range(len(data.keys())):
        d = list(data.keys())[i]
        df.hist(column=d)
        plt.show()
    '''

if __name__ == '__main__':
    main()
