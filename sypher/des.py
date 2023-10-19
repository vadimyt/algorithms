import os
import multiprocessing
import time
import sys
import math
begin_replace_table = (
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17,  9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
)
end_replace_table = (
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
)
key_replace_table = (
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
)
key_select_table = (
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
)
extend_table = (
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
)
s_box_table = (
    (
        (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
        (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
        (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
        (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13),
    ),
    (
        (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
        (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
        (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
        (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),
    ),
    (
        (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
        (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
        (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
        (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),
    ),
    (
        (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
        (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
        (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
        (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),
    ),
    (
        (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
        (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
        (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
        (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),
    ),
    (
        (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
        (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
        (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
        (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),
    ),
    (
        (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
        (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
        (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
        (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),
    ),
    (
        (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
        (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
        (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
        (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),
    )
)
p_box_replace_table = (
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25,
)
spin_table = (1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28)
def crypt(mode, data_in_, number_of_blocks, kkey, queues):
    line_good = ''
    counter = 0
    for g in range(number_of_blocks):
        line_in_bad = ''
        #получение 64-битных блоков
        for elem in data_in_[g*8:(g+1)*8]:
            byte = bin(elem)[2:]
            while len(byte)<8:
                byte = '0'+byte
            line_in_bad += byte
        line_in_good = ''
        #начальная перестановка
        for i in range(64):
            line_in_good += line_in_bad[begin_replace_table[i]-1]
        if mode == 2:
            r_next = line_in_good[:32]
            l_next = line_in_good[32:]
        else:
            l_next = line_in_good[:32]
            r_next = line_in_good[32:]
        #16 раундов сети Фейстеля
        for i in range(1,17):
            r_after_f = ''
            r_ext = ''
            l_current = l_next
            l_next = r_next
            #функция f
            r_next = bin(int(l_current,2)^int(f(r_next,kkey[i]),2))[2:]
            while len(r_next)<32:
                r_next = '0'+r_next
        if mode == 2:
            line_out = r_next+l_next
        else:
            line_out = l_next+r_next
        #конечная перестановка
        for i in range(64):
            line_good += line_out[end_replace_table[i]-1]
        if g == number_of_blocks - 1 or g % 125 == 0 and g > 0:
            queues[counter].put(line_good)
            counter += 1
            line_good = ''
def f(data_in, _key):
        b = ['']*8
        data_out = ''
        #расширение 32-битной половины блока до 48 бит
        for i in range(48):
            data_out += data_in[extend_table[i]-1]
        #XOR данных и ключа
        data_in = bin(int(data_out,2)^int(_key,2))[2:]
        while len(data_in)<48:
            data_in = '0'+data_in
        #разбиение 48-битной последовательности на 8 частей по 6 бит
        for i in range(8):
            b[i] = data_in[i*6:(i+1)*6]
        data_in = ''
        #применене S-преобразования
        for i in range(8):
            data_out = bin(s_box_table[i][int(b[i][0]+b[i][5],2)][int((b[i][1:5]),2)])[2:]
            while len(data_out)<6:
                data_out = '0'+data_out
            data_in += data_out
        # P-перестановка
        data_out = ''
        for i in range(32):
            data_out += data_in[p_box_replace_table[i]-1]
        return data_out
k = ['']*17
c = ['']*17
d = ['']*17
cd = ['']*17
byte = ''
mode = 0
cpu_count = os.cpu_count()
processes = []
queues = []
if __name__ == '__main__':
    start_time = time.time()
    try:
        key = sys.argv[1]
        mode = int(sys.argv[2])
        file_size = os.stat(sys.argv[3]).st_size
        f1 = open(sys.argv[3],'rb')
        f2 = open(sys.argv[4],'wb')
    except IndexError:
        key = '1234567'
        mode = 1
        if mode == 1:
            file_size = os.stat('sypher/1.txt').st_size
            f1 = open('sypher/1.txt','rb')
            f2 = open('sypher/2.txt','wb')  
        else:
            file_size = os.stat('sypher/2.txt').st_size
            f1 = open('sypher/2.txt','rb')
            f2 = open('sypher/3.txt','wb')  
    #получение 56-битного ключа
    for i in range(7):
        byte = bin(ord(key[i]))[2:]
        while len(byte)<8:
            byte = '0'+byte
        k[0] += byte
    #расширение ключа до 64 бит
    for i in range(8):
        count = 0
        for j in range(7):
            if k[0][j+8*i] == '1':
                count += 1
        if count % 2 == 1:
            k[0] = k[0][:7+8*i] + '0' + k[0][7+i*8:]
        else:
            k[0] = k[0][:7+8*i] + '1' + k[0][7+i*8:]
    #получение c и d блоков из 64-битного ключа
    for i in range(28):
        c[0] += k[0][key_replace_table[i] - 1]
        d[0] += k[0][key_replace_table[i + 28] - 1]
    #получение 16-ти c и d вариаций
    for i in range(16):
        c[i + 1] = c[0][spin_table[i]:] + c[0][:spin_table[i]]
        d[i + 1] = d[0][spin_table[i]:] + d[0][:spin_table[i]]
    #получение 16-ти 48-битных подключей
    for i in range(1,17):
        cd[i] = c[i] + d[i]
        for j in range(48):
            k[i] += cd[i][key_select_table[j]-1]
    if mode == 2:
        k[1],k[2],k[3],k[4],k[5],k[6],k[7],k[8],k[9],k[10],k[11],k[12],k[13],k[14],k[15],k[16] = (
        k[16],k[15],k[14],k[13],k[12],k[11],k[10],k[9],k[8],k[7],k[6],k[5],k[4],k[3],k[2],k[1])
    blocks_count = math.ceil(file_size / 8)
    blocks_count_per_process = (blocks_count - 1) // cpu_count
    print('blocks_count =',blocks_count,'\nblocks_count_per_process =',blocks_count_per_process)
    if blocks_count_per_process > 0:
        for i in range(cpu_count):
            queues.append([multiprocessing.Queue() for s in range(math.ceil(blocks_count_per_process / 125))])
            processes.append(multiprocessing.Process(target=crypt, args=(mode, f1.read(8*blocks_count_per_process), blocks_count_per_process, k.copy(), queues[i])))
            processes[i].start()
            print('process '+str(i)+' started')
    #работа с последними блоками
    blocks_left = blocks_count - blocks_count_per_process * cpu_count
    line_for_input = f1.read()
    for i in range(8 - len(line_for_input) % 8):
        line_for_input = line_for_input[:len(line_for_input)//8*8]+bytes(chr(0b10100).encode('charmap'))+line_for_input[len(line_for_input)//8*8:]
    if blocks_count_per_process > 0:
        for i in range(cpu_count):
            processes[i].join()
            print('process '+str(i)+' ended')
    queues.append([multiprocessing.Queue() for s in range(math.ceil(blocks_left / 125))])
    crypt(mode, line_for_input, blocks_left, k, queues[-1])
    cyphers = ['']*(cpu_count+1 if blocks_count_per_process > 0 else 1)
    for i in range(cpu_count+1 if blocks_count_per_process > 0 else 1):
        for j in range(len(queues[i])):
            for x in range(queues[i][j].qsize()):
                cyphers[i] += queues[i][j].get()
    cypher = ''.join(cyphers[:-1])
    ctr = 0
    if mode == 2:
        while cyphers[-1][ctr*8-64:][:8] == '00010100':
            cyphers[-1] = cyphers[-1][:8*ctr-64]+cyphers[-1][ctr*8-56:]
            ctr += 1
    cypher += cyphers[-1]
    for i in range(8*blocks_count):
        try:
            f2.write(chr(int(cypher[8*i:8*(i+1)],2)).encode('charmap'))
        except ValueError:
            break
    print('Elapsed time: ', time.time() - start_time)