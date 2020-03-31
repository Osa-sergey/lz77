import time

''' Сам код алгоритма, отлажен, работает на любых окнах'''
def encode(s):
    struct = []
    i_prev = 0
    i = 0 #номер символа в тексте
    buf_l = '~' * buf_size #начальное заполнение буфера 
    while i < len(s):
        buf_l += s[i_prev:i] # двигаем скользящие окно 
        buf_l = buf_l[-buf_size:]
        l = 1  # количество символов для поиска вхождения
        prev_incl = buf_size #равно длине буфера что говорит о том, что нет совпадений 
        while True:
            buf_r = s[i:i + l]
            incl = str.find(buf_l + buf_r, buf_r)#поиск правой части буфера в объединении левой и правой
            if incl < buf_size and i+l <= len(s): #нам нужно начало совпадения в левой части буфера
                l += 1  # увеличиваем кол-во символов для поиска
                prev_incl = incl
                continue
            offset = buf_size - prev_incl if prev_incl < buf_size else 0 #если prev_incl больше длины буфера, то значит не был найден элемент
            struct.append([offset, l-1, s[i+l-1]])
            i_prev = i
            i += l
            break
    return struct


def decode(struct):
    ret = ""
    for el in struct:
        if el[0] == el[1] == 0: # 0 0 символ тогда просто добавляем его 
            ret += el[2]
        else:
            ret += ret[-el[0]:]*(el[1]//el[0]) + ret[-el[0]:-el[0]+(el[1] % el[0])] + el[2] 
            # откатываем курсор на offset назад и первым слагаемым повторяем этот кусок полное количество раз, влезающее в длину 
            # прибавляем остаток 
    return ret


buf_size = 1024
f = open('text.txt', 'r', encoding= "utf-8")
s = f.read()
f.close()

s += '\0' # для корректного обрабатывания конца файла

s1 = encode(s)
s2 = decode(s1)
print('Fine' if s2 == s else 'Something has gone awry')
