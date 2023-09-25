def CreateUnsorted():
    import random
    array = [random.randint(0, 100) for i in range(100)]
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
    for i in range(n-1):
        for j in range(n-i-1):
            if int(sorted[j]) > int(sorted[j+1]):
                tmp = sorted[j]
                sorted[j] = sorted[j+1]
                sorted[j+1] = tmp
    sorted_file = open(r'sorting\BubleSorted.txt', "w", encoding='utf-8')
    for i in range(n):        
        sorted_file.write(str(sorted[i]))
    sorted_file.close()
    pass

BubleSort(ReadFromUnsorted())