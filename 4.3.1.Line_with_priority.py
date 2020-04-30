n = int(input())  # Количество операций с деревом
lst = []  # Список дерева
ext_max_lst = []  # Список извлеченных максимальных значений
for j in range(n):
    command = input()  # Команда на добавление или извлечение элемента из дерева
    if command[0] == "I":  # Обработка команды добавления
        number = int(command[6::])  # Значение добавляемого элемента
        lst.append(number)
        i = len(lst)
        while True: # В цикле "поднимаем" элемент, пока над ним есть меньшие элементы
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
        lst[0] = lst.pop(len(lst) - 1)  # Последний элемент списка удаляем, а его значение записываем первым
        i = len(lst)
        index_el = 0  # Индекс перемещаемого элемента в дереве
        while True:  # В цикле "топим" элемент пока под ним есть большие элементы
            if (index_el + 1) > (len(lst) // 2):  # Если условие верно, значит у элемента нет потомков. Идём за следующей командой
                break
            if (index_el + 1) * 2 + 1 > len(lst):  # Если условие верно, значит у элемента есть только один потомок
                index_comp_el = index_el * 2 + 1
            else:  # Определяем большего из двух потомков элемента
                if lst[index_el * 2 + 1] > lst[index_el * 2 + 2]:
                    index_comp_el = index_el * 2 + 1
                else:
                    index_comp_el = index_el * 2 + 2
            if lst[index_el] >= lst[index_comp_el]: # Если элемент больше или равен потомку, идём за следующей командой
                break
            else: # Если потомок больше родителя, меняем их местами ("топим" родителя)
                lst[index_el], lst[index_comp_el] = lst[index_comp_el], lst[index_el]
                index_el = index_comp_el
for i in ext_max_lst:
    print(i)