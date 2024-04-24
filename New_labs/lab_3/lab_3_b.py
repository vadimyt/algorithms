import random
import simpy

from lab_3_a import *

RANDOM_SEED = 0  # не установлено
NUM_SERVERS = 10  # Количество серверов
TIME_CONSUMING = 45  # Обслуживание 1 клиента
TIME_INTERVAL = 1/0.9  # Время между 2-мя заявками
SIM_TIME = 10000  # Общее время моделирования
CLIENT_NUMBER = 0  # Изначально уже занято количество машин


class Server(object):
    """
    Объект, обслуживающий клиентов
    """

    def __init__(self, env, num_servers, consuming_time):
        self.env = env
        self.machine = simpy.Resource(env, num_servers)
        self.consuming_time = consuming_time
        self.allClient = 0
        self.accomplishClient = 0

    def serve(self, client):
        yield self.env.timeout(self.consuming_time)
        self.allClient += 1
        per = random.randint(50, 99)
        # print("% s выполнение задачи:% d %%." % (client, per))
        if per > 80:
            self.accomplishClient += 1
            print("Количество клиентов, обслуживаемых рабочими станциями:% d. "
                  "Уровень соответствия службы рабочей станции:% .2f." % (self.allClient, float(self.accomplishClient) / float(self.allClient)))

        yield env.timeout(random.triangular(0.6, 1.5, 0.9))


def Client(env, name, cw):
    # print('% s обратился с запросом ​​в% .2f.' % (name, env.now))
    with cw.machine.request() as request:
        yield request
        # print('% s делает запрос в% .2f.' % (name, env.now))
        yield env.process(cw.serve(name))
        # print('% s завершает работу в% .2f.' % (name, env.now))


def setup(env, num_servers, consuming_time, t_inter, clientNumber):
    workstation = Server(env, num_servers, consuming_time)

    i = 0
    while (i < clientNumber):
        env.process(Client(env, 'Client_%d' % i, workstation))
        i += 1

    while True:
        yield env.timeout(t_inter)
        i += 1
        env.process(Client(env, 'Client_%d' % i, workstation))


# Инициализировать и запустить задачу симуляции
print("Начать симуляцию")

# Инициализировать начальное число, результат основателя может быть воспроизведен, когда указано значение
random.seed()

# Создайте среду и запустите симуляцию
env = simpy.Environment()
env.process(setup(env, NUM_SERVERS, TIME_CONSUMING,
            TIME_INTERVAL, CLIENT_NUMBER))

# Начать исполнение!
env.run(until=SIM_TIME)

# Расчёт характеристик СМО
handler = SMO(1/TIME_INTERVAL, 1/TIME_CONSUMING)
handler.MultiChannelWithQueueWithoutLen(NUM_SERVERS)
handler.print()
