from pulp import LpVariable, LpProblem, LpMaximize, value
import time

start = time.time()
x1 = LpVariable("x1", lowBound=10, upBound=20)
x2 = LpVariable("x2", lowBound=20, upBound=40)
x3 = LpVariable("x3", lowBound=25, upBound=100)
problem = LpProblem('0', LpMaximize)
problem += 10*x1 + 15*x2 + 20*x3, "Функция цели"
problem += 2*x1 + 4* x3 <= 200, "1"
problem += 4*x1 + 3*x2 + x3 <= 500, "2"
problem += 10*x1 + 15*x2 + 20*x3 <= 1495, "3"
problem += 30*x1 + 20*x2 + 25*x3 <= 4500, "4"
problem.solve()
print("Результат:")
for variable in problem.variables():
    print (variable.name, "=", variable.varValue)
print("Прибыль:")
print(value(problem.objective))
stop = time.time()
print ("Время :")
print(stop - start)