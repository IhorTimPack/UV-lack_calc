lst = list(input())  # Исходная строка символов до кодировки
all_symbols = list(set(lst))  # Список всех символов
all_symbols.sort()
frieq_symbol = {}  # Словарь всех символов с их частотой в исходной строке
code_symbol = {}  # Словарь с кодом всех символов
for i in all_symbols:
    frieq_symbol[i] = lst.count(i)
    code_symbol[i] = None
if len(all_symbols) > 1:
    while len(frieq_symbol) > 0:
        min_1 = len(lst)
        min_1_symb = ""
        min_2 = len(lst)
        min_2_symb = ""
        for i in frieq_symbol:  # Определяем первый символ с минимальным повторением в строке
            if frieq_symbol[i] < min_1:
                min_1_symb = i
                min_1 = frieq_symbol[i]
        for i in frieq_symbol:  # Оперделяем второй символ с минимальным посторением в строке
            if frieq_symbol[i] < min_2 and i != min_1_symb:
                min_2_symb = i
                min_2 = frieq_symbol[i]
        frieq_symbol[min_1_symb + min_2_symb] = min_1 + min_2  # Внесли в словарь частотности новый узел с именем двух детей и суммой их значений
        for i in list(min_1_symb):
            if code_symbol[i] == None:
                code_symbol[i] = "0"
            else:
                code_symbol[i] = code_symbol[i] + "0"
        for i in list(min_2_symb):
            if code_symbol[i] == None:
                code_symbol[i] = "1"
            else:
                code_symbol[i] = code_symbol[i] + "1"
        frieq_symbol.pop(min_1_symb)
        frieq_symbol.pop(min_2_symb)
        if len(frieq_symbol) == 1:
            break
if len(all_symbols) > 1:
    for i in code_symbol:
        code_symbol[i] = code_symbol[i][::-1]
    code = ""
    for i in lst:
        code += code_symbol[i]
    print(len(all_symbols), len(code))
    for i in all_symbols:
        print(i + ":", code_symbol[i])
    print(code)
else:
    print("1", len(lst))
    print(all_symbols[0] + ": 0")
    print("0" * len(lst))