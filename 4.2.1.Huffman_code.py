lst = list(input())  # Исходная строка символов до кодировки
all_symbols = set(lst)  # Список всех символов
frieq_symbol = {}  # Словарь всех символов с их частотой в исходной строке
code_symbol = {}  # Словарь с кодом всех символов
for i in all_symbols:
    frieq_symbol[i] = lst.count(i)
    code_symbol[i] = None
min_1 = len(lst)
min_2 = len(lst)
print(frieq_symbol)
print(code_symbol)
while len(frieq_symbol) > 0:
    for i in frieq_symbol:  # Определяем два символа с минимальными повторениями в строке
        if frieq_symbol[i] < min_1:
            min_1_symb = i
            min_1 = frieq_symbol[i]
        elif frieq_symbol[i] < min_2:
            min_2_symb = i
            min_2 = frieq_symbol[i]
    frieq_symbol[min_1_symb + min_2_symb] = min_1 + min_2  # Внесли в словарь частотности новый узел с именем двух детей и суммой их значений
    if code_symbol[min_1_symb] == None:
        code_symbol[min_1_symb] = "0"
    else:
        code_symbol[min_1_symb] = code_symbol[min_1_symb] + "0"
    if code_symbol[min_2_symb] == None:
        code_symbol[min_2_symb] = "1"
    else:
        code_symbol[min_2_symb] = code_symbol[min_2_symb] + "1"
    frieq_symbol.pop(min_1_symb)
    frieq_symbol.pop(min_2_symb)
    print(frieq_symbol)
    print(code_symbol)

