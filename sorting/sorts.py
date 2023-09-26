import time
from multiprocessing import Process, Queue
import random
import matplotlib.pyplot as plt

def CreateUnsorted(n=100):
    array = [random.randint(0, 100) for i in range(n)]
    unsorted_file = open(r'sorting\UnSorted.txt', "w", encoding='utf-8')
    for i in range(len(array)):        
        unsorted_file.write(str(array[i])+'\n')
    unsorted_file.close()

def ReadFromUnsorted():
    try:
        unsorted_file = open(r'sorting\UnSorted.txt', "r", encoding='utf-8')
    except FileNotFoundError:
        CreateUnsorted()
        unsorted_file = open(r'sorting\UnSorted.txt', "r", encoding='utf-8')
    array=unsorted_file.readlines()
    unsorted_file.close()
    # if I want to erase \n while reading
    # array=list(map(lambda x:x.strip(),array))
    return array

def BubleSort(array,q):    
    n=len(array)
    sorted=array[:]
    start_time = time.time()
    for i in range(n-1):
        for j in range(n-i-1):
            if int(sorted[j]) > int(sorted[j+1]):
                tmp = sorted[j]
                sorted[j] = sorted[j+1]
                sorted[j+1] = tmp
    end_time = time.time()
    elapsed_time = end_time - start_time
    if q!=None:
        q.put(elapsed_time)
    #print('Время выполнения пузырьковой сортировки: ', elapsed_time, '\n')
    sorted_file = open(r'sorting\BubleSorted.txt', "w", encoding='utf-8')
    for i in range(n):        
        sorted_file.write(str(sorted[i]))
    sorted_file.close()

def ShakerSort(array,q):
    n=len(array)
    sorted=array[:]
    start_time=time.time()
    left=0
    right=n-1
    while left <= right:
        for i in range(left, right, 1):
            if int(sorted[i]) > int(sorted[i+1]):
                tmp=sorted[i]
                sorted[i]=sorted[i+1]
                sorted[i+1]=tmp
        right -= 1
        for i in range(right, left, -1):
            if int(sorted[i-1]) > int(sorted[i]):
                tmp=sorted[i]
                sorted[i]=sorted[i-1]
                sorted[i-1]=tmp
        left += 1
    end_time=time.time()
    elapsed_time=end_time-start_time
    if q!=None:
        q.put(elapsed_time)
    #print('Время выполнения сортировки шейкера: ', elapsed_time, '\n')
    sorted_file = open(r'sorting\ShakerSorted.txt', "w", encoding='utf-8')
    for i in range(n):        
        sorted_file.write(str(sorted[i]))
    sorted_file.close()

def InsertionSort(array,q):
    n=len(array)
    sorted=array[:]
    start_time=time.time()
    for i in range(n):
        key=int(sorted[i])
        j=i-1
        while j>=0 and key < int(sorted[j]):
            sorted[j+1]=sorted[j]
            j-=1
        sorted[j+1]=key
    end_time=time.time()
    elapsed_time=end_time-start_time
    if q!=None:
        q.put(elapsed_time)
    #print('Время выполнения сортировки вставками: ', elapsed_time, '\n')
    sorted_file = open(r'sorting\InsertionSorted.txt', "w", encoding='utf-8')
    for i in range(n):        
        sorted_file.write(str(sorted[i])+'\n')
    sorted_file.close()

def QuickSort(array,q):
    n=len(array)
    sorted=array[:]
    start_time=time.time()
    recQuickSort(sorted,0,n-1)
    end_time=time.time()
    elapsed_time=end_time-start_time
    if q!=None:
        q.put(elapsed_time)
    #print('Время выполнения быстрой сортировки: ', elapsed_time, '\n')
    sorted_file = open(r'sorting\QuickSorted.txt', "w", encoding='utf-8')
    for i in range(n):        
        sorted_file.write(str(sorted[i]))
    sorted_file.close()

def recQuickSort(array,low,high):
    if low<high:
        pivot=partition(array,low,high)
        recQuickSort(array,low,pivot-1)
        recQuickSort(array,pivot+1,high)

def partition(array,low,high):
    pivot=int(array[high])
    i=low-1
    for j in range(low,high):
        if int(array[j]) <= pivot:
            i=i+1
            tmp=array[i]
            array[i]=array[j]
            array[j]=tmp
    tmp=array[i+1]
    array[i+1]=array[high]
    array[high]=tmp
    return i+1

def TestSorts():
    CreateUnsorted(10000)
    array=ReadFromUnsorted()
    p1=Process(target=BubleSort,args=(array,None))
    p2=Process(target=ShakerSort,args=(array,None))    
    p3=Process(target=InsertionSort,args=(array,None))  
    p4=Process(target=QuickSort,args=(array,None))  
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()

def TestGraph():
    x = [1, 2, 3, 4, 5]
    y = [25, 32, 34, 20, 25]
    a = [10, 11, 12, 13, 14] 
    b = [10, 11, 12, 13, 14] 
    plt.plot(x,y, color="g",label='xy')
    plt.plot(a,b, color="r",label='ab')
    plt.legend()
    plt.show()

def SortsComparison():
    n=10
    m=15
    ABS=[]
    ASS=[]
    AIS=[]
    AQS=[]
    Y=[]
    QBS=Queue()
    QSS=Queue()
    QIS=Queue()
    QQS=Queue()
    for i in range(m):
        #l=pow(n,i+1)
        l=n*(i+1)*5
        Y.append(l)
        CreateUnsorted(l)
        array=ReadFromUnsorted()
        p1=Process(target=BubleSort,args=(array,QBS))
        p2=Process(target=ShakerSort,args=(array,QSS))    
        p3=Process(target=InsertionSort,args=(array,QIS))  
        p4=Process(target=QuickSort,args=(array,QQS))  
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        ABS.append(QBS.get())
        ASS.append(QSS.get())
        AIS.append(QIS.get())
        AQS.append(QQS.get())
        print("Итерация номер:" + str(i))
    QBS.close()
    QBS.join_thread()
    QSS.close()
    QSS.join_thread()
    QIS.close()
    QIS.join_thread()
    QQS.close()
    QQS.join_thread()
    plt.plot(ABS,Y, color="r",label='пузырьковая сортировка')
    plt.plot(ASS,Y, color="g",label='сортировка шейкера')
    plt.plot(AIS,Y, color="b",label='сортировка вставками')
    plt.plot(AQS,Y, color="y",label='быстрая сортировка')
    plt.legend()
    plt.show()

        
def main():
    TestSorts()
    #TestGraph()
    #SortsComparison()

if __name__ == '__main__':
    main()