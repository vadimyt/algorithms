from math import factorial

class SMO:

    '''
        #Интeнсивность (вызов в минуту, Лямбда)
        Intensity #Проверка на 0

        #Время обслуживания 1 заявки
        ServiceTime #Проверка на 0

        #Интенсивность обслуживания заявок (мю)
        IntensityService  #Проверка на 0

        #Вероятность обслуживания заявки
        ProbabilityService

        #Время простоя
        DownTime

        #Вероятность отказа
        ProbabilityFault

        #Абсолютная пропускная способность (А)
        Bandwidth

        #Интенсивность потока заявок
        MultIntensity

        #Среднее число занятых каналов
        AverageChannel

        #Относительная пропускная способность
        RelativeBandwidth

        #Время ожидания в очереди
        WaitTime

        #Среднее число заявок в СМО
        Lsmo

        #Средняя длина очереди
        QueueLength

        #Вероятность образования очереди
        ProbabilityQueue

        #Среднее время нахождения в СМО
        SMOTime
        
        #Статична ли СМО. False - если очередь будет стремиться в бесконечность
        IsStatic
    '''

    def __init__(self,serviceTime, intensity):
        self.Intensity=intensity
        self.ServiceTime=serviceTime
        self.IntensityService=1/self.ServiceTime

    def SingleChannelWithFail(self):
       #Вероятность обслуживания заявки
        self.ProbabilityService=self.IntensityService/(self.Intensity+self.IntensityService)
        #Время простоя
        self.DownTime=1/self.Intensity
        #Вероятность отказа в обслуживании
        self.ProbabilityFault=1-self.ProbabilityService
        #Пропускная способность
        self.Bandwidth=self.Intensity*self.ProbabilityService
        
    def SingleChannelWithQueue(self, len):
        p=self.Intensity/self.IntensityService
        
        if p==1:
            p_0=1/(len+2)
        else:
            p_0=(1-p)/(1-(p**(len+2)))
       #Вероятность обслуживания заявки
        self.ProbabilityService=self.Intensity/(self.Intensity+self.IntensityService)
        self.ProbabilityFault=p**(len+1)*p_0
        self.RelativeBandwidth=1-self.ProbabilityFault
        self.AverageChannel=self.RelativeBandwidth*self.Intensity
        if p==1:
                self.QueueLength=(len*(len+1))/(2*(len+2))
        else:
             self.QueueLength=(p**2)*(1-(p**len)*(len-len*p+1))/((1-p)**2)
        self.WaitTime=self.QueueLength/self.Intensity
        self.Lsmo=1+self.QueueLength
        if p!=1:
            self.SMOTime=self.Lsmo/self.Intensity
        else:
            self.SMOTime=(len+1)/(2*self.IntensityService)
            
    def SingleChannelWithQueueWhithoutLen(self):
        p=self.Intensity/self.IntensityService
        if p<1:
            self.IsStatic=True
         
            self.QueueLength=(p**2)/(1-p)
            self.WaitTime=self.QueueLength/self.Intensity
            self.Lsmo=(p)/(1-p)
            self.SMOTime=self.Lsmo/self.Intensity
        else:
            self.IsStatic=False
            
    def MultiChannelWithFail(self, ChannelCount):
        #Вероятность обслуживания заявки
        self.MultIntensity=self.Intensity/self.IntensityService
        p_0=0
        for n in range(0, ChannelCount):
            p_0+=(self.MultIntensity**n)/SMO.factorial(n)
        p_0=p_0**(-1)
        self.ProbabilityService=self.Intensity/(self.Intensity+self.IntensityService)
        self.RelativeBandwidth=self.ProbabilityService
        self.ProbabilityFault=p_0*((self.MultIntensity**ChannelCount)/SMO.factorial(ChannelCount))
        self.Bandwidth=self.Intensity*self.RelativeBandwidth
        self.AverageChannel=self.Bandwidth/self.IntensityService
        
    def MultiChannelWithQueue(self, count,len):
        p=self.Intensity/self.IntensityService
        
        if (p/count)==1:
            p_0=0
            for n in range(0, count):
                p_0+=(p**n)/SMO.factorial(n)
            p_0+=(len*(p**(count+1)))/(SMO.factorial(count)*count)
            p_0=p_0**(-1)
        else:
            p_0=0
            for n in range(0, count):
                p_0+=(p**n)/SMO.factorial(n)
            p_0+=(((p**(count+1))/(SMO.factorial(count)*(count-p)))*(1-((p/count)**len)))
            p_0=p_0**(-1)
        self.ProbabilityFault=((p**(count+len))/((count**len)*SMO.factorial(count)))*p_0
       
        if (p/n)==1:
                self.QueueLength=((p*(count+1))/(count*SMO.factorial(count)))*((len*(len+1))/2)*p_0
        else:
             self.QueueLength=((p*(count+1))/(count*SMO.factorial(count)))*((1-(((p/count)**len)*(len+1-(len*p/count))))/((1-(p/count))**2))*p_0
        self.WaitTime=self.QueueLength/self.Intensity
        self.ProbabilityFault=(p**(count+len))*((p_0)/((count**len)*SMO.factorial(count)))
        self.SMOTime=self.WaitTime+((1-self.ProbabilityFault)/(self.IntensityService))
        self.AverageChannel=(self.Intensity/self.IntensityService)*(1-self.ProbabilityFault)
        
    def MultiChannelWithQueueWithoutLen(self, count):
        p=self.Intensity/self.IntensityService
        if (p/count)<1:
            self.IsStatic=True
            p_0=0
            for n in range(0, count):
                p_0+=(p**n)/SMO.factorial(n)
            p_0+=(p**(count+1))/(SMO.factorial(count)*(count-p))
            p_0=p_0**(-1)
            self.ProbabilityQueue=((p**(count+1))/((count-p)*SMO.factorial(count)))*p_0
            self.QueueLength=(count/(count-p))*p_0
            self.WaitTime=self.QueueLength/self.Intensity
            self.AverageChannel=p
            self.Lsmo=self.QueueLength+self.AverageChannel
            self.SMOTime=self.WaitTime+1/self.IntensityService
        else:
            self.IsStatic=False

    def print(self):
        print("Интeнсивность "+str(self.Intensity))
        print("Время обслуживания 1 заявки "+str(self.ServiceTime))
        print("---------------------------------------------")
        print("Характеристики СМО")
        try:
            if(self.IntensityService!=None):
                print("Интенсивность обслуживания заявок: "+str(self.IntensityService))            
        except:
            pass
        try:
            if(self.ProbabilityService!=None):
                print("Вероятность обслуживания заявки: "+str(self.ProbabilityService))            
        except:
            pass
        try:
            if(self.DownTime!=None):
                print("Время простоя: "+str(self.DownTime))        
        except:
            pass 
        try:   
            if(self.ProbabilityFault!=None):
                print("Вероятность отказа: "+str(self.ProbabilityFault))      
        except:
            pass  
        try:    
            if(self.Bandwidth!=None):
                print("Абсолютная пропускная способность: "+str(self.Bandwidth))     
        except:
            pass     
        try:  
            if(self.MultIntensity!=None):
                print("Интенсивность потока заявок: "+str(self.MultIntensity))    
        except:
            pass        
        try:
            if(self.AverageChannel!=None):
                print("Среднее число занятых каналов: "+str(self.AverageChannel))   
        except:
            pass      
        try:   
            if(self.RelativeBandwidth!=None):
                print("Относительная пропускная способность: "+str(self.RelativeBandwidth))  
        except:
            pass  
        try:        
            if(self.WaitTime!=None):
                print("Время ожидания в очереди: "+str(self.WaitTime))     
        except:
            pass      
        try: 
            if(self.Lsmo!=None):
                print("Среднее число заявок в СМО: "+str(self.Lsmo))   
        except:
            pass      
        try:   
            if(self.QueueLength!=None):
                print("Средняя длина очереди: "+str(self.QueueLength))   
        except:
            pass      
        try:   
            if(self.ProbabilityQueue!=None):
                print("Вероятность образования очереди: "+str(self.ProbabilityQueue))  
        except:
            pass          
        try:
            if(self.SMOTime!=None):
                print("Среднее время нахождения в СМО: "+str(self.SMOTime))    
        except:
            pass        
        try:
            if(self.IsStatic!=None):
                print("Статична ли СМО. False - если очередь будет стремиться в бесконечность: "+str(self.IsStatic)) 
        except:
            pass           
    
    def factorial(n):
        return factorial(n)
    
def Tasks():
    print("Task1")  
    Task1 =  SMO(serviceTime=1,intensity=0.95)
    Task1.SingleChannelWithFail()
    Task1.print()
    print("\n")

    print("Task2")
    Task2 =  SMO(serviceTime=1.25,intensity=0.7)
    Task2.SingleChannelWithQueue(len=3)
    Task2.print()
    print("\n")

    print("Task3")  
    Task3 =  SMO(serviceTime=1,intensity=0.8)
    Task3.MultiChannelWithQueueWithoutLen(count=3)
    Task3.print()
    print("\n")

    print("Task4")
    Task4 =  SMO(serviceTime=1.2,intensity=0.5)
    Task4.SingleChannelWithFail()
    Task4.print()
    print("\n")

    print("Task5")  
    Task5 =  SMO(serviceTime=3,intensity=1)
    Task5.MultiChannelWithQueueWithoutLen(count=3)
    Task5.print()
    print("\n")

    print("Task6")
    Task6 =  SMO(serviceTime=2,intensity=1/3)
    Task6.MultiChannelWithQueue(count=2,len=5)
    Task6.print()
    print("\n")

def UserInput():
    try:
        serviceTime=float(input("Время обслуживания: "))
        if (serviceTime == None or serviceTime < 0):
            return 0
        intensity=float(input("Интенсивность: "))
        if (intensity == None or intensity < 0):
            return 0
        len=int(input("Максимальная длинна очереди: "))
        if (len == None or len < 0):
            return 0
        count=int(input("Кол-во каналов: "))
        if (count == None or count < 0):
            return 0
        fail = bool(input("СМО с отказом (true/false): "))
        if (fail == None or fail != (True or False)):
            return 0
        else:
            smo = SMO(serviceTime,intensity)
            if (len != 0):
                if (count > 1):
                    if(fail == True):
                        smo.MultiChannelWithQueue(count,len)
                    else:                
                        smo.MultiChannelWithQueueWithoutLen(count)
                else:
                    if(fail == True):
                        smo.SingleChannelWithQueue(len)
                    else:                
                        smo.SingleChannelWithQueueWhithoutLen()
            else:
                if (count > 1):
                    smo.MultiChannelWithFail()
                else:
                    smo.SingleChannelWithFail()
            smo.print()
            return 1
    except:
        return 0

if __name__ == '__main__':
    Tasks()
    #res = UserInput()
    #if (res == 0):
        #print("Неверный ввод")
