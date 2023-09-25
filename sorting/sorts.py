def CreateUnsorted():
    import random
    array = [random.randint(0, 100) for i in range(100)]
    # print(array)
    unsorted_file = open(r'sorting\unsorted.txt', "w", encoding='utf-8')
    unsorted_file.write(str(array))
    unsorted_file.close()
    pass

CreateUnsorted()