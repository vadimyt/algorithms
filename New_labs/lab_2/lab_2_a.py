from scipy import fft
from math import pi
import numpy as np
import matplotlib.pyplot as plt

A = 1
T = 300
fi = pi/12
k = np.arange(0,1024)

numpy_k = np.array(k)

s = (2*pi*k)/T
x1 = 4 + A * np.sin(s+fi)

numpy_func = np.array(x1)
set_func_by_data = np.polyfit(numpy_k,numpy_func,1)
func_line = np.poly1d(set_func_by_data)

y = fft.fft(x1)

numpy_fourier_forward = np.array(y)
set_fourier_by_data = np.polyfit(numpy_k,numpy_fourier_forward,1)
fourier_line = np.poly1d(set_fourier_by_data)

F = fft.ifft(y)

numpy_fourier_reverse = np.array(F)
set_fourier_reverse_by_data = np.polyfit(numpy_k,numpy_fourier_reverse,1)
fourier_reverse_line = np.poly1d(set_fourier_reverse_by_data)

f = np.arange(0, len(y))/ len(y)

plt.figure(figsize=(40,15))

plt.subplot(3,1,1)

plt.plot(numpy_k, numpy_func, label = 'data') # точечный график по x_numpy, y_numpy
plt.plot(numpy_k, func_line(numpy_k), linestyle='dashed', color="orange", label = 'linear trend') # линейный тренд
plt.grid(color="gainsboro") # Сетка
plt.legend(loc='upper right', fontsize=10) 
plt.title("Исходная функция: 4+sin((2Pi/300)*tk + Pi/12)")

plt.subplot(3,1,2)

plt.plot(numpy_k, numpy_fourier_forward, label = 'data') # точечный график по x_numpy, y_numpy
plt.plot(numpy_k, fourier_line(numpy_k), linestyle='dashed', color="orange", label = 'linear trend') # линейный тренд
plt.grid(color="gainsboro") # Сетка
plt.legend(loc='upper right', fontsize=10) 
plt.title("Фурье прямой")

plt.subplot(3,1,3)

plt.plot(numpy_k, numpy_fourier_reverse, label = 'data') # точечный график по x_numpy, y_numpy
plt.plot(numpy_k, fourier_reverse_line(numpy_k), linestyle='dashed', color="orange", label = 'linear trend') # линейный тренд
plt.grid(color="gainsboro") # Сетка
plt.legend(loc='upper right', fontsize=10) 
plt.title("Фурье обратный")

fig = plt.gcf() # Взять текущую фигуру
fig.set_size_inches(15, 15) # Задать размеры графика

# Покажем окно с нарисованным графиком
plt.show()