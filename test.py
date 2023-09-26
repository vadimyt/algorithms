import time
import multiprocessing
from multiprocessing import Process
from multiprocessing import Pool

def test(n):
    time.sleep(2)
    print("hru"+n)  
    pass  

def test2(n):
    time.sleep(1)
    print("qwa"+n)
    pass

if __name__ == '__main__':
    p= multiprocessing.Process(target=test, args=("hru",))
    p.start()
    p2= multiprocessing.Process(target=test2, args=("hru2",))
    p2.start()
    p3= multiprocessing.Process(target=test, args=("hru3",))
    p3.start()

    p.join()
    p2.join()
    p3.join()