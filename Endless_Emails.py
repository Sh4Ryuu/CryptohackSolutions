#!/usr/bin/env python3
import gmpy2
from Crypto.Util import number
from itertools import combinations


def load_output():
    ret = {'n':[], 'c':[]}
    with open("output.txt", 'rb') as fd:
        while True:
            line = fd.readline()
            if not line: break
            line = line.strip().decode()
            if not line: continue

            k, v = line.split('=')
            k = k.strip()
            if k == 'e':
                continue
            ret[k].append(int(v))

    return ret

def decrypt(grps, e):
    for grp in combinations(zip(grps['n'], grps['c']), e):
        N = 1
        for x in grp: N *= x[0]

        M = 0
        for x in grp:
            M += x[1]*number.inverse(N//x[0], x[0])*(N//x[0])
        M %= N

        m, exact = gmpy2.iroot(M, e)
        if exact:
            decrypted_message = number.long_to_bytes(m)
            # Slice to print only the portion starting with "crypto{"
            flag_start = decrypted_message.find(b'crypto{')
            if flag_start != -1:
                print(decrypted_message[flag_start:].decode())

grps = load_output()
decrypt(grps, 3)

