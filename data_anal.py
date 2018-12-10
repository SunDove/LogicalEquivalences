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
    for i in range(25, 35):
        a = data[str(i)]
        #a = removeOutliers(a)
        avgs.append(np.median(a))
    df = pd.DataFrame(data)
    print(avgs)
    plt.plot(avgs)
    plt.show()

    '''
    for i in range(len(data.keys())):
        d = list(data.keys())[i]
        df.hist(column=d)
        plt.show()
    '''

if __name__ == '__main__':
    main()
