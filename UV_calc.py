from tkinter import *


# Функция для заполнения полей длины и ширины печатного листа типовыми размерами.
def set_format(f):
    global length_sheet
    global width_sheet
    global dic_formats
    length_sheet = dic_formats[f][1]
    width_sheet = dic_formats[f][0]
    entry_length.delete(0, END)
    entry_width.delete(0, END)
    entry_length.insert(0, length_sheet)
    entry_width.insert(0, width_sheet)


# Словарь со всеми невычисляемыми составляющими стоимости лакировки.
dic_all_prices = {"electricity": [2.8, 2.8], "dryer": [8.5, 10.5], "drum": [220, 300], "film": [35, 70],
                  "salary": [25, 25], "printing": [0.14, 0.2], "speed": [250, 200], "adjustment": [85, 95]}

# Словарь для типов лакировки. Ключ - тип лакировки. Элементы словаря - стоимость  1кг лака, расход лака на 1м.кв.
dic_type_lack = {"УФ-лак": [255, 0.012], "УФ-лак с поднятием": [800, 0.012], "Глиттер + УФ-лак (1:5)": [310, 0.165],
                 "Глиттер + УФ-лак с поднятием (1:5)": [660, 0.165]}

# Словарь типов клиентов. Ключ - название категории клиента. Элемент ключа - итоговая наценка к баховой стоимости.
dic_type_client = {"премиум": 1, "хорошо": 1.1, "стандарт": 1.2}

# Словарь типичных форматов печатного листа. Ключ - название формата. Элементы - ширина и длина листа в мм.
dic_formats = {"A4": [225, 320], "B4": [250, 350], "A3": [320, 450], "B3": [350, 500], """1/6 A1""": [300, 320],
               """1/6 B1""": [333, 350], "A2": [450, 640], "B2": [500, 700]}

root = Tk()
root.geometry("820x500")
root.iconbitmap("logo_timpack_200px_qhT_icon.ico")
root.title("Расчёт стоимости УФ-лакировки")

frame_1 = Frame(root, width=200)
frame_2 = Frame(root, width=500)
frame_3 = Frame(root, width=500)
frame_1.grid(row=0, column=0, padx=10, pady=10)
frame_2.grid(row=0, column=1, padx=10, pady=10)
frame_3.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

type_lack = StringVar()  # Раскрывающийся список для выбора типа лакировки
type_lack.set("УФ-лак")
button_type_lack = OptionMenu(frame_1, type_lack, *dic_type_lack)
button_type_lack.grid(row=0, column=0, columnspan=2, padx=5, pady=5, ipadx=50)

type_client = StringVar()  # Раскрывающийся спсисок для выбора типа клиента
type_client.set("преимиум")
button_type_client = OptionMenu(frame_1, type_client, *dic_type_client)  # Кнопка для выбора типа клиента
button_type_client.grid(row=1, column=1)

text_type_client = Label(frame_1, text="Тип Клиента:", justify=RIGHT)
text_amount = Label(frame_1, text="Тираж, листов:", justify=RIGHT)
text_percents = Label(frame_1, text="% заполнения", justify=RIGHT)
text_format = Label(frame_2, text="Формат печатного листа")
text_length = Label(frame_2, text="Длина, мм:", justify=RIGHT)
text_width = Label(frame_2, text="Ширина, мм:", justify=RIGHT)
text_cost_all_amount = Label(frame_3, text="Стоимость лакировки всего тиража, грн:", justify=RIGHT)
text_cost_one_sheet = Label(frame_3, text="Стоимость лакировки одного листа, грн:", justify=RIGHT)
text_result_cost_all_amount = Label(frame_3, text="Здесь будет переменная_1", relief=GROOVE)
text_result_cost_one_sheet = Label(frame_3, text="Здесь будет переменная_2", relief=RIDGE)

text_type_client.grid(row=1, column=0, sticky=E)
text_amount.grid(row=2, column=0, sticky=E)
text_percents.grid(row=3, column=0, sticky=E)
text_format.grid(row=0, column=0, columnspan=2)
text_length.grid(row=1, column=0, sticky=E)
text_width.grid(row=2, column=0, sticky=E)
text_cost_all_amount.grid(row=0, column=1)
text_cost_one_sheet.grid(row=1, column=1)
text_result_cost_all_amount.grid(row=0, column=2, sticky=E)
text_result_cost_one_sheet.grid(row=1, column=2, sticky=E)

entry_amount = Entry(frame_1, text="Какой тираж?")
entry_percents = Entry(frame_1)
entry_length = Entry(frame_2)
entry_width = Entry(frame_2)

entry_amount.grid(row=2, column=1)
entry_percents.grid(row=3, column=1)
entry_length.grid(row=1, column=1)
entry_width.grid(row=2, column=1)

button_A4 = Button(frame_2, text="A4", command=lambda: set_format("A4"))
button_B4 = Button(frame_2, text="B4", command=lambda: set_format("B4"))
button_A3 = Button(frame_2, text="A3", command=lambda: set_format("A3"))
button_B3 = Button(frame_2, text="B3", command=lambda: set_format("B3"))
button_sixthA1 = Button(frame_2, text="""1/6 A1""", command=lambda: set_format("""1/6 A1"""))
button_sixthB1 = Button(frame_2, text="""1/6 B1""", command=lambda: set_format("""1/6 B1"""))
button_A2 = Button(frame_2, text="A2", command=lambda: set_format("A2"))
button_B2 = Button(frame_2, text="B2", command=lambda: set_format("B2"))
button_calculate = Button(frame_3, text="Рассчитать")

button_A4.grid(row=3, column=0)
button_B4.grid(row=4, column=0)
button_A3.grid(row=3, column=1)
button_B3.grid(row=4, column=1)
button_sixthA1.grid(row=3, column=2)
button_sixthB1.grid(row=4, column=2)
button_A2.grid(row=3, column=3)
button_B2.grid(row=4, column=3)
button_calculate.grid(row=0, column=0)

root.mainloop()
