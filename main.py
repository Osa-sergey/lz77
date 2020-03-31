import struct
''' попытка записи в бин файл не работает с русским языком и не обрабатывает  буфер более 256'''
def encode(s, name):
    file = open(name, "wb")
    i_prev = 0
    i = 0 #номер символа в тексте
    buf_l = '~' * buf_size
    while i < len(s):
        buf_l += s[i_prev:i]
        buf_l = buf_l[-buf_size:]
        l = 1  # количество символов для поиска вхождения
        prev_incl = buf_size
        while True:
            buf_r = s[i:i + l]
            incl = str.find(buf_l + buf_r, buf_r)
            if incl < buf_size and i+l <= len(s):
                l += 1  # увеличиваем кол-во символов для поиска
                prev_incl = incl
                continue
            offset = buf_size - prev_incl if prev_incl < buf_size else 0
            shifted_offset = offset << 6
            char = bytes(s[i + l - 1], "utf-8")
            length = l-1
            offset_and_length = shifted_offset + length
            ol_bytes = struct.pack(">Hs", offset_and_length, char)
            file.write(ol_bytes)
            i_prev = i
            i += l
            break
    file.close()
    return


def decode(name):
    file = open(name, "rb")
    input = file.read()
    file.close()
    ret = ""
    i = 0
    items = []
    while i < len(input):
        (offset_and_length, char) = struct.unpack(">Hs", input[i:i + 3])
        offset = offset_and_length >> 6
        length = offset_and_length - (offset << 6)
        char = char.decode("utf-8")
        i = i + 3
        items.append([offset, length, char])
    for el in items:
        if el[0] == el[1] == 0:

            ret += el[2]
        else:
            ret += ret[-el[0]:]*(el[1]//el[0]) + ret[-el[0]:-el[0]+(el[1] % el[0])] + el[2]
    return ret

buf_size = 256
f = open('text.txt', 'r', encoding= "utf-8")
s = f.read()

f.close()
s += '\0'
encode(s, "compressed.bin")

s2 = decode("compressed.bin")
print(s2)
print('Fine' if s2 == s else 'Something has gone awry')
