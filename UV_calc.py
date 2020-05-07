from tkinter import *


# Функция для заполнения полей длины и ширины печатного листа типовыми размерами.
def set_format(f):
    global width_sheet
    global length_sheet
    width_sheet = dic_formats[f][0]
    length_sheet = dic_formats[f][1]
    entry_width.delete(0, END)
    entry_length.delete(0, END)
    entry_width.insert(0, width_sheet)
    entry_length.insert(0, length_sheet)


def calculate():
    if int(entry_length.get()) > 500 or int(entry_width.get()) > 500:
        i = 1
    else:
        i = 0
    result = (float(dic_all_prices["adjustment_cost"][i]) + float(dic_all_prices["drum"][i]) + (
            float(entry_length.get()) * float(entry_width.get()) * float(entry_percents.get()) / 100000000 * float(
        dic_type_lack[type_lack.get()][1]) * float(dic_type_lack[type_lack.get()][0]) * float(
        entry_amount.get()) + (float(dic_all_prices["dryer"][i]) * float(dic_all_prices["electricity"][i]) + float(
        dic_all_prices["salary"][i])) * float(entry_amount.get()) / float(dic_all_prices["speed"][i]) + float(
        entry_amount.get()) * float(dic_all_prices["printing"][i]) + float(
        dic_all_prices["adjustment_time"][i]) * float(dic_all_prices["salary"][i])) + float(
        dic_all_prices["film"][i]) * float(dic_films_reused[film_reused.get()])) * float(
        dic_type_client[type_client.get()])
    # entry_result_cost_all_amount.delete(0, END)
    # entry_result_cost_one_sheet.delete(0, END)
    # entry_result_cost_all_amount.insert(0, f"{result:.2f}")  # Cт-ть лакировки с фиксацией двух знаков после запятой
    # entry_result_cost_one_sheet.insert(0, f"{result / float(entry_amount.get()):.2f}")

    # report = f"""Категория заказчика: '{type_client.get()}'. (+{int(float(dic_type_client[type_client.get()]) * 100 -
    #     100)}% к минимльной цене)\nТип лака: '{type_lack.get()}'\nТираж: {int(entry_amount.get()
    #     )} лист.\nШирина листа: {int(entry_width.get())} мм.\nДлина листа:\t{int(entry_length.get())
    #     } мм.\nЗаполнение лаком печатного листа: {int(entry_percents.get())} %\nСтоимость лакировки тиража: {
    #     f"{result:.2f}"} грн.\nСтоимость лакировки одного листа: {f"{result / float(entry_amount.get()):.2f}"} грн."""
    report_type_client_var.set(type_client.get())
    report_type_lack_var.set(type_lack.get())
    report_film_var.set(film_reused.get())
    report_amount_var.set(entry_amount.get())
    report_width_var.set(entry_width.get())
    report_length_var.set(entry_length.get())
    report_percents_var.set(entry_percents.get())
    report_cost_all_amount_var.set(f"{result:.2f}")
    report_cost_one_sheet_var.set(f"{result / float(entry_amount.get()):.3f}")
    # text_summary_result.delete(0.0, END)
    # text_summary_result.insert(END, report)


# Словарь со всеми невычисляемыми составляющими стоимости лакировки.
dic_all_prices = {"electricity": [2.8, 2.8], "dryer": [10.5, 10.5], "drum": [220, 300], "film": [35, 70],
                  "salary": [25, 25], "printing": [0.14, 0.2], "speed": [250, 200], "adjustment_cost": [85, 95],
                  "adjustment_time": [0.75, 0.75]}

# Словарь для типов лакировки. Ключ - тип лакировки. Элементы словаря - стоимость  1кг лака, расход лака на 1м.кв.
dic_type_lack = {"УФ-лак": [255, 0.012], "УФ-лак с поднятием": [800, 0.012], "Глиттер + УФ-лак (1:5)": [310, 0.165],
                 "Глиттер + УФ-лак с поднятием (1:5)": [660, 0.165]}

# Словарь типов клиентов. Ключ - название категории клиента. Элемент ключа - итоговая наценка к баховой стоимости.
dic_type_client = {"премиум": 1, "хорошо": 1.1, "стандарт": 1.2}

# Словарь типичных форматов печатного листа. Ключ - название формата. Элементы - ширина и длина листа в мм.
dic_formats = {"A4": [225, 320], "B4": [250, 350], "A3": [320, 450], "B3": [350, 500], """1/6 A1""": [300, 320],
               """1/6 B1""": [333, 350], "A2": [450, 640], "B2": [500, 700]}

# Словарь. Считать или нет стоимость вывода пленок.
dic_films_reused = {"новая": 1, "повторная или заказчика": 0}

root = Tk()
root.geometry("640x480")
root.iconbitmap("TimPack.ico")
root.title("Расчёт стоимости УФ-лакировки")

frame_1 = Frame(root, width=320, bg="#EEEEAE")
frame_2 = Frame(root, width=320, bg="#EEAEEE")
frame_3 = Frame(root, width=320, bg="#AEEEEE")
# frame_4 = Frame(root, width=320)
frame_5 = Frame(root, width=320, bg="#EEEEAE")
frame_1.grid(row=0, column=0)
frame_2.grid(row=0, column=1)
frame_3.grid(row=1, column=0, columnspan=2)
# frame_4.grid(row=2, column=0, columnspan=2)
# frame_5.grid_propagate(0)
frame_5.grid(row=3, column=0, columnspan=2)

type_lack = StringVar()  # Раскрывающийся список для выбора типа лакировки
type_lack.set("УФ-лак")
button_type_lack = OptionMenu(frame_1, type_lack, *dic_type_lack)
button_type_lack.config(width=32)
button_type_lack.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky="WE")

type_client = StringVar()  # Раскрывающийся спсисок для выбора типа клиента
type_client.set("премиум")
button_type_client = OptionMenu(frame_1, type_client, *dic_type_client)  # Кнопка для выбора типа клиента
button_type_client.grid(row=1, column=1, padx=2, pady=2, sticky="WE")

film_reused = StringVar()  # Раскрывающийся спсисок для выбора типа клиента
film_reused.set("новая")
button_film_reused = OptionMenu(frame_2, film_reused, *dic_films_reused)  # Кнопка для выбора типа клиента
button_film_reused.grid(row=3, column=1, padx=2, pady=2, sticky="WE")

text_type_client = Label(frame_1, text="Тип клиента:")
text_amount = Label(frame_1, text="Тираж, листов:")
text_percents = Label(frame_1, text="% заполнения:")
text_format = Label(frame_2, text="Формат печатного листа", width=23)
text_width = Label(frame_2, text="Ширина, мм:")
text_length = Label(frame_2, text="Длина, мм:")
text_film = Label(frame_2, text="Плёнка:")
# text_cost_all_amount = Label(frame_3, text="Стоимость лакировки всего тиража, грн:", justify=RIGHT)
# text_cost_one_sheet = Label(frame_3, text="Стоимость лакировки одного листа, грн:", justify=RIGHT)
# text_summary_result = Text(frame_4, height=8, width=60, bg="#EEEEEE")

text_type_client.grid(row=1, column=0, padx=5, pady=5, sticky=W)
text_amount.grid(row=2, column=0, padx=5, pady=5, sticky=W)
text_percents.grid(row=3, column=0, padx=5, pady=5, sticky=W)
text_format.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
text_width.grid(row=1, column=0, padx=5, pady=5, sticky=W)
text_length.grid(row=2, column=0, padx=5, pady=5, sticky=W)
text_film.grid(row=3, column=0, padx=5, pady=5, sticky=W)
# text_cost_all_amount.grid(row=0, column=1, padx=5, pady=5)
# text_cost_one_sheet.grid(row=1, column=1, padx=5, pady=5)
# text_summary_result.grid(row=0, column=0, padx=5, pady=5)

report_type_client_name = Label(frame_5, text="Тип клиента:", justify=LEFT)
report_type_client_var = StringVar()
report_type_client = Label(frame_5, textvariable=report_type_client_var, font=16)
report_type_client_measure = Label(frame_5)
report_type_lack_name = Label(frame_5, text="Тип лака:")
report_type_lack_var = StringVar()
report_type_lack = Label(frame_5, textvariable=report_type_lack_var, font=16)
report_film_name = Label(frame_5, text="Плёнка:")
report_film_var = StringVar()
report_film = Label(frame_5, textvariable=report_film_var, font=16)
report_amount_name = Label(frame_5, text="Тираж:")
report_amount_var = StringVar()
report_amount = Label(frame_5, textvariable=report_amount_var, font=16)
report_amount_measure = Label(frame_5, text="лист.")
report_width_name = Label(frame_5, text="Ширина листа:")
report_width_var = StringVar()
report_width = Label(frame_5, textvariable=report_width_var, font=16)
report_width_measure = Label(frame_5, text="мм.")
report_length_name = Label(frame_5, text="Длина листа:")
report_length_var = StringVar()
report_length = Label(frame_5, textvariable=report_length_var, font=16)
report_length_measure = Label(frame_5, text="мм.")
report_percents_name = Label(frame_5, text="Процент заполнения листа:")
report_percents_var = StringVar()
report_percents = Label(frame_5, textvariable=report_percents_var, font=16)
report_percents_measure = Label(frame_5, text="%")
report_cost_all_amount_name = Label(frame_5, text="Стоимость лакировки тиража:")
report_cost_all_amount_var = StringVar()
report_cost_all_amount = Label(frame_5, textvariable=report_cost_all_amount_var, font=16)
report_cost_all_amount_measure = Label(frame_5, text="грн.")
report_cost_one_sheet_name = Label(frame_5, text="Стоимость лакировки одного листа:")
report_cost_one_sheet_var = StringVar()
report_cost_one_sheet = Label(frame_5, textvariable=report_cost_one_sheet_var, font=16)
report_cost_one_sheet_measure = Label(frame_5, text="грн.")

report_type_client_name.grid(row=0, column=0, sticky="sw")
report_type_client.grid(row=0, column=1, sticky=E)
report_type_client_measure.grid(row=0, column=2, sticky="sw")
report_type_lack_name.grid(row=1, column=0, sticky="sw")
report_type_lack.grid(row=1, column=1, sticky=E)
report_film_name.grid(row=2, column=0, sticky="sw")
report_film.grid(row=2, column=1, sticky=E)
report_amount_name.grid(row=3, column=0, sticky="sw")
report_amount.grid(row=3, column=1, sticky=E)
report_amount_measure.grid(row=3, column=2, sticky="sw")
report_width_name.grid(row=4, column=0, sticky="sw")
report_width.grid(row=4, column=1, sticky=E)
report_width_measure.grid(row=4, column=2, sticky="sw")
report_length_name.grid(row=5, column=0, sticky="sw")
report_length.grid(row=5, column=1, sticky=E)
report_length_measure.grid(row=5, column=2, sticky="sw")
report_percents_name.grid(row=6, column=0, sticky="sw")
report_percents.grid(row=6, column=1, sticky=E)
report_percents_measure.grid(row=6, column=2, sticky="sw")
report_cost_all_amount_name.grid(row=7, column=0, sticky="sw")
report_cost_all_amount.grid(row=7, column=1, sticky=E)
report_cost_all_amount_measure.grid(row=7, column=2, sticky="sw")
report_cost_one_sheet_name.grid(row=8, column=0, sticky="sw")
report_cost_one_sheet.grid(row=8, column=1, sticky=E)
report_cost_one_sheet_measure.grid(row=8, column=2, sticky="sw")

entry_amount = Entry(frame_1, width=10, justify=RIGHT)
entry_percents = Entry(frame_1, width=10, justify=RIGHT)
entry_width = Entry(frame_2, width=10, justify=RIGHT)
entry_length = Entry(frame_2, width=10, justify=RIGHT)
# entry_result_cost_all_amount = Entry(frame_3, width=10, justify=RIGHT)
# entry_result_cost_one_sheet = Entry(frame_3, width=10, justify=RIGHT)

entry_amount.grid(row=2, column=1, padx=5, pady=5, sticky=E)
entry_percents.grid(row=3, column=1, padx=5, pady=5, sticky=E)
entry_width.grid(row=1, column=1, padx=5, pady=5, sticky=E)
entry_length.grid(row=2, column=1, padx=5, pady=5, sticky=E)
# entry_result_cost_all_amount.grid(row=0, column=2, padx=5, pady=5)
# entry_result_cost_one_sheet.grid(row=1, column=2, padx=5, pady=5)

button_A4 = Button(frame_2, text="A4", command=lambda: set_format("A4"), width=5)
button_B4 = Button(frame_2, text="B4", command=lambda: set_format("B4"), width=5)
button_A3 = Button(frame_2, text="A3", command=lambda: set_format("A3"), width=5)
button_B3 = Button(frame_2, text="B3", command=lambda: set_format("B3"), width=5)
button_sixthA1 = Button(frame_2, text="""1/6 A1""", command=lambda: set_format("""1/6 A1"""), width=5)
button_sixthB1 = Button(frame_2, text="""1/6 B1""", command=lambda: set_format("""1/6 B1"""), width=5)
button_A2 = Button(frame_2, text="A2", command=lambda: set_format("A2"), width=5)
button_B2 = Button(frame_2, text="B2", command=lambda: set_format("B2"), width=5)
button_calculate = Button(frame_3, text="Рассчитать", command=calculate, width=40)

button_A4.grid(row=0, column=2, padx=5, pady=5)
button_B4.grid(row=0, column=3, padx=5, pady=5)
button_A3.grid(row=1, column=2, padx=5, pady=5)
button_B3.grid(row=1, column=3, padx=5, pady=5)
button_sixthA1.grid(row=2, column=2, padx=5, pady=5)
button_sixthB1.grid(row=2, column=3, padx=5, pady=5)
button_A2.grid(row=3, column=2, padx=5, pady=5)
button_B2.grid(row=3, column=3, padx=5, pady=5)
button_calculate.grid(row=0, column=0, padx=5, pady=5)

root.mainloop()
