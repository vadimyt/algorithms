import time
import multiprocessing

def CreateUnsorted(n=100):
    import random
    array = [random.randint(0, 100) for i in range(n)]
    unsorted_file = open(r'sorting\UnSorted.txt', "w", encoding='utf-8')
    for i in range(len(array)):        
        unsorted_file.write(str(array[i])+'\n')
    unsorted_file.close()
    pass

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

def BubleSort(array):    
    n=len(array)
    sorted=array[:]
    print('1')    
    start_time = time.time()
    for i in range(n-1):
        for j in range(n-i-1):
            if int(sorted[j]) > int(sorted[j+1]):
                tmp = sorted[j]
                sorted[j] = sorted[j+1]
                sorted[j+1] = tmp
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Время выполнения пузырьковой сортировки: ', elapsed_time)
    sorted_file = open(r'sorting\BubleSorted.txt', "w", encoding='utf-8')
    for i in range(n):        
        sorted_file.write(str(sorted[i]))
    sorted_file.close()    
    pass

def ShakerSort(array):
    n=len(array)
    sorted=array[:]
    print('2')
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
    print('Время выполнения сортировки шейкера: ', elapsed_time)
    sorted_file = open(r'sorting\ShakerSorted.txt', "w", encoding='utf-8')
    for i in range(n):        
        sorted_file.write(str(sorted[i]))
    sorted_file.close()
    pass

if __name__ == '__main__':
    CreateUnsorted(5000)
    array=ReadFromUnsorted()
    p1=multiprocessing.Process(target=BubleSort,args=(array,))
    p2=multiprocessing.Process(target=ShakerSort,args=(array,))
    p2.start()
    p1.start()
    
    p1.join()
    p2.join()
    BubleSort(array)
    ShakerSort(array)