
def encode_map(m):
    ret = ''
    for r in m:
        ret = ret + ''.join([str(c) for c in r])
    return ret

def decode_map(s, size):
    ret = []
    for j in range(size):
        row = []
        for i in range(size):
            row.append(s[j*size + i])
        ret.append(row)
    return ret

def print_map(m):
    for row in m:
        print(row)