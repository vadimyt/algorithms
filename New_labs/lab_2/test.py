import time
import numpy as np
import matplotlib.pyplot as plt

class Random:   
    def __init__(self, a = 16807, k=31, x0=10):
        Random.a = a        
        Random.m = 2**k
        Random.x = x0

    def nextRandom(self):
        Random.x  = (Random.a * Random.x) % Random.m
        return (Random.x/Random.m)

random = Random()

values = []

for i in range(10):
    values.append(random.nextRandom())

print(values)