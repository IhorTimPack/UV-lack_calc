numbers = input().split()
code_symbols = {}
for i in range(int(numbers[0])):
    symb = input().split()
    code_symbols[symb[1]] = symb[0][0:1:]
lst = list(input())
piece_symb = ""
encode_txt = ""
count = 0
while len(lst) > 0:
    piece_symb = piece_symb + lst[count]
    lst.pop(0)
    if piece_symb in code_symbols:
        encode_txt += code_symbols[piece_symb]
        count = 0
        piece_symb = ""
print(piece_symb)