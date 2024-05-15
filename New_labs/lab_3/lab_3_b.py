import random
import simpy

from lab_3_a import *

import random
import simpy

RANDOM_SEED = 0  # не установлено
NUM_SERVERS = 2  # Количество серверов
TIME_CONSUMING = 2  # Обслуживание 1 клиента
TIME_INTERVAL = 3  # Время между 2-мя заявками
SIM_TIME = 1000  # Общее время моделирования
QUEUEUE_LENGTH = 5
CLIENT_NUMBER = 0  # Изначально уже занято количество машин

queueue_lenth_mid = []
time_medium = []

class Server(object):
    def __init__(self, env, num_servers, consuming_time, queue_length):
        self.cancel_counter = 0
        self.all_clients = 0
        self.env = env
        self.machine = simpy.Resource(env, num_servers)
        self.consuming_time = consuming_time
        self.allClient = 0
        self.accomplishClient = 0
        self.queue_length = queue_length
        self.current_queue_length = 0
        self.available = True

    def serve(self, client):
        #print(self.current_queue_length)            
        yield self.env.timeout(self.consuming_time)
        self.allClient += 1
        self.accomplishClient += 1
        #print("Количество клиентов, обслуживаемых рабочими станциями:% d. "
        #      % (self.allClient))
        t = env.timeout(random.triangular(0.6, 1.5, 0.9))
        time_medium.append(t)
        yield t

def Client(env, name, cw):
    print('% s обратился с запросом ​​в% .2f.' % (name, env.now))
    with cw.machine.request() as request:
        #print(request)
        yield request
        print('% s делает запрос в% .2f.' % (name, env.now))
        yield env.process(cw.serve(name))
        cw.current_queue_length -= 1
        print('% s завершает работу в% .2f.' % (name, env.now))


def setup(env, workstation, t_inter, clientNumber):
    i = 0
    while (i < clientNumber):
        env.process(Client(env, 'Client_%d' % i, workstation))
        i += 1

    while True:
        queueue_lenth_mid.append(workstation.current_queue_length)
        yield env.timeout(t_inter)
        if(workstation.current_queue_length > workstation.queue_length):
            workstation.available = False
        else:
            workstation.available = True
            
        workstation.all_clients += 1
        if workstation.available:
            i += 1
            workstation.current_queue_length += 1
            env.process(Client(env, 'Client_%d' % i, workstation))
        else:
            print("Отказ")
            workstation.cancel_counter += 1        

# Инициализировать и запустить задачу симуляции
print("Начать симуляцию")

# Инициализировать начальное число, результат основателя может быть воспроизведен, когда указано значение
random.seed()

# Создайте среду и запустите симуляцию
env = simpy.Environment()
workstation = Server(env, NUM_SERVERS, TIME_CONSUMING,QUEUEUE_LENGTH)
env.process(setup(env, workstation,TIME_INTERVAL, CLIENT_NUMBER, ))

# Начать исполнение!
env.run(until=SIM_TIME)
print("Конец симуляции")
print("Результаты симуляции. Процент отказов:")
print(workstation.cancel_counter / workstation.all_clients)
i=0
for queue in queueue_lenth_mid:
    i+=queue
print("Средняя длинна очереди: " + str(i/len(queueue_lenth_mid)))
i=0
for time in time_medium:
    i+=time._delay
print("Среднеевремя ожидания в СМО: " + str(i/len(time_medium)))


# Расчёт характеристик СМО
handler = SMO(TIME_CONSUMING,1/TIME_INTERVAL)
handler.MultiChannelWithQueue(NUM_SERVERS,QUEUEUE_LENGTH)
handler.print()