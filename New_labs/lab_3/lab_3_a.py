import time
import numpy as np
import math
import matplotlib.pyplot as plt

class MultiSMO_otk:
      def __init__(self, n, _lambda, mu):
        MultiSMO_limited.n = n
        MultiSMO_limited._lambda = _lambda
        MultiSMO_limited.mu = mu
        MultiSMO_limited.p = MultiSMO_limited._lambda/MultiSMO_limited.mu
        #характеристики        
        MultiSMO_limited.p_0 = MultiSMO_limited.func_p_0(self)
        MultiSMO_limited.p_otk = MultiSMO_limited.func_p_otk(self)
        MultiSMO_limited.L_och = MultiSMO_limited.func_L_och(self)
        MultiSMO_limited.T_och = MultiSMO_limited.func_T_och(self)
        MultiSMO_limited.T_SMO = MultiSMO_limited.func_T_SMO(self)
        MultiSMO_limited.k_zan = MultiSMO_limited.func_k_zan(self)  
        MultiSMO_limited.k_sr = MultiSMO_limited.func_k_sr(self)  

        def func_p_otk(self):
            return

class MultiSMO_limited:   
    def __init__(self, n, m, _lambda, mu):
        MultiSMO_limited.n = n
        MultiSMO_limited.m = m
        MultiSMO_limited._lambda = _lambda
        MultiSMO_limited.mu = mu
        MultiSMO_limited.p = MultiSMO_limited._lambda/MultiSMO_limited.mu
        MultiSMO_limited.pn = MultiSMO_limited.p/MultiSMO_limited.n
        #характеристики        
        MultiSMO_limited.p_0 = MultiSMO_limited.func_p_0(self)
        MultiSMO_limited.p_otk = MultiSMO_limited.func_p_otk(self)
        MultiSMO_limited.L_och = MultiSMO_limited.func_L_och(self)
        MultiSMO_limited.T_och = MultiSMO_limited.func_T_och(self)
        MultiSMO_limited.T_SMO = MultiSMO_limited.func_T_SMO(self)
        MultiSMO_limited.k_zan = MultiSMO_limited.func_k_zan(self)  
        MultiSMO_limited.k_sr = MultiSMO_limited.func_k_sr(self)     
    
    def func_p_0(self):        
        sum=0        
        for k in range(MultiSMO_limited.n+1):
            sum+=(MultiSMO_limited.p**k/math.factorial(k))
        if(MultiSMO_limited.pn == 1):
            return (sum+MultiSMO_limited.m*MultiSMO_limited.p**(MultiSMO_limited.n+1)/(math.factorial(MultiSMO_limited.n)*MultiSMO_limited.n))**-1
        else:
            return (sum+MultiSMO_limited.p**(MultiSMO_limited.n+1)/(math.factorial(MultiSMO_limited.n)*(MultiSMO_limited.n-MultiSMO_limited.p))*(1-MultiSMO_limited.pn**MultiSMO_limited.m))**-1
   
    def func_p_otk(self):
        return MultiSMO_limited.p**(MultiSMO_limited.n+MultiSMO_limited.m)/(math.factorial(MultiSMO_limited.n)*(MultiSMO_limited.n**MultiSMO_limited.m))*MultiSMO_limited.p_0
    
    def func_L_och(self):
        if(MultiSMO_limited.pn == 1):
            return (MultiSMO_limited.p**(MultiSMO_limited.n+1)/(MultiSMO_limited.n*math.factorial(MultiSMO_limited.n)))*(MultiSMO_limited.m*(MultiSMO_limited.m+1)/2)*MultiSMO_limited.p_0
        else:
            return (MultiSMO_limited.p**(MultiSMO_limited.n+1)/(MultiSMO_limited.n*math.factorial(MultiSMO_limited.n)))*((1-MultiSMO_limited.pn**MultiSMO_limited.m*(MultiSMO_limited.m+1-MultiSMO_limited.m*MultiSMO_limited.pn))/((1*MultiSMO_limited.pn)**2))
    
    def func_T_och(self):
        return MultiSMO_limited.L_och/MultiSMO_limited._lambda   
    
    def func_T_SMO(self):
        return MultiSMO_limited.T_och+(1-MultiSMO_limited.p_otk)/MultiSMO_limited.mu   
    
    def func_k_zan(self):
        return (MultiSMO_limited._lambda/MultiSMO_limited.mu)*(1-MultiSMO_limited.p_otk)
    
    def func_k_sr(self):
        return (MultiSMO_limited.k_zan/MultiSMO_limited.n)
    
    def print_all_char(self):
        print("p_0=")
        print(str(MultiSMO_limited.p_0)+"\n")
        print("вер.отк.=")
        print(str(MultiSMO_limited.p_otk)+"\n")
        print("ср.дл.оч.=")
        print(str(MultiSMO_limited.L_och)+"\n")
        print("ср.вр.ож.оч.=")
        print(str(MultiSMO_limited.T_och)+"\n")
        print("ср.вр.преб.в смо.=")
        print(str(MultiSMO_limited.T_SMO)+"\n")          
        print("ср.зн.зан.кан.=")
        print(str(MultiSMO_limited.k_zan)+"\n")             
        print("коэфф.зан=")
        print(str(MultiSMO_limited.k_sr)+"\n") 

class MultiSMO_unlimited:   
    def __init__(self, n, _lambda, mu):
        MultiSMO_unlimited.n = n
        MultiSMO_unlimited._lambda = _lambda
        MultiSMO_unlimited.mu = mu
        MultiSMO_unlimited.p = MultiSMO_unlimited._lambda/MultiSMO_unlimited.mu
        MultiSMO_unlimited.pn = MultiSMO_unlimited.p/MultiSMO_unlimited.n
        #характеристики        
        MultiSMO_unlimited.p_0 = MultiSMO_unlimited.func_p_0(self)
        MultiSMO_unlimited.p_och = MultiSMO_unlimited.func_p_och(self)
        MultiSMO_unlimited.L_och = MultiSMO_unlimited.func_L_och(self)
        MultiSMO_unlimited.T_och = MultiSMO_unlimited.func_T_och(self)
        MultiSMO_unlimited.T_SMO = MultiSMO_unlimited.func_T_SMO(self)
        MultiSMO_unlimited.k_sr = MultiSMO_unlimited.func_k_sr(self)
        MultiSMO_unlimited.k_zan = MultiSMO_unlimited.func_k_zan(self)        
        MultiSMO_unlimited.L_SMO = MultiSMO_unlimited.func_L_SMO(self)
    
    def func_p_0(self):
        sum=0
        for k in range(MultiSMO_unlimited.n+1):
            sum+=(MultiSMO_unlimited.p**k/math.factorial(k))
        return (sum+MultiSMO_unlimited.p**(MultiSMO_unlimited.n+1)/(math.factorial(MultiSMO_unlimited.n)*(MultiSMO_unlimited.n-MultiSMO_unlimited.p)))**-1
    
    def func_p_och(self):
        return MultiSMO_unlimited.p**(MultiSMO_unlimited.n+1)/(math.factorial(MultiSMO_unlimited.n)*(MultiSMO_unlimited.n-MultiSMO_unlimited.p))*MultiSMO_unlimited.p_0
    
    def func_L_och(self):
        return (MultiSMO_unlimited.n/(MultiSMO_unlimited.n-MultiSMO_unlimited.p))*MultiSMO_unlimited.p_och
    
    def func_T_och(self):
        return MultiSMO_unlimited.L_och/MultiSMO_unlimited._lambda   
    
    def func_T_SMO(self):
        return MultiSMO_unlimited.T_och+1/MultiSMO_unlimited.mu
    
    def func_k_sr(self):
        return MultiSMO_unlimited.p
    
    def func_k_zan(self):
        return MultiSMO_unlimited.k_sr/MultiSMO_unlimited.n

    def func_L_SMO(self):
        return MultiSMO_unlimited.L_och + MultiSMO_unlimited.k_sr
    
    def print_all_char(self):
        print("p_0=")
        print(str(MultiSMO_unlimited.p_0)+"\n")
        print("вер.оч.=")
        print(str(MultiSMO_unlimited.p_och)+"\n")
        print("ср.дл.оч.=")
        print(str(MultiSMO_unlimited.L_och)+"\n")
        print("ср.вр.ож.оч.=")
        print(str(MultiSMO_unlimited.T_och)+"\n")
        print("ср.вр.преб.в смо.=")
        print(str(MultiSMO_unlimited.T_SMO)+"\n")
        print("ср.ч.зан.кан.=")
        print(str(MultiSMO_unlimited.k_sr)+"\n")
        print("коэфф.зан=")
        print(str(MultiSMO_unlimited.k_zan)+"\n")
        print("ср.ч.заяв.в смо.=")
        print(str(MultiSMO_unlimited.L_SMO)+"\n")

tmp=MultiSMO_limited(n=3,m=5,_lambda=6,mu=2)
tmp.print_all_char()