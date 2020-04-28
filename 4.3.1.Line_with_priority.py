n = int(input())  # Количество операций с деревом
lst = []  # Список дерева
ext_max_lst = []  # Список извлеченных максимальных значений
for j in range(n):
    command = input()  # Команда на добавление или извлечение элемента из дерева
    if command[0] == "I":  # Обработка команды добавления
        number = int(command[6::])  # Значение добавляемого элемента
        lst.append(number)
        i = len(lst)
        while True:
            if i // 2 < 1:
                break
            if lst[i-1] <= lst[(i // 2) - 1]:
                break
            lst[i-1], lst[(i // 2) - 1] = lst[(i // 2) - 1], lst[i-1]
            i = i // 2
    else:  # Обработка команды извлечения
        ext_max_lst.append(lst[0])  # Добавляем в список извлекаемый объект
        if len(lst) == 1:  # Если объект в списке один, просто удаляем его и идём за следующей командой
            lst.pop(0)
            continue
        lst[0] = lst.pop(len(lst) - 1)  # Последний элемент списка удаляем, а его значение записываем в первым
        i = len(lst)
        if lst[(2 * i) - 1] not in lst:
            continue
        else:
            print("ddd")
print(ext_max_lst)
