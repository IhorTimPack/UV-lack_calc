from tkinter import *
from tkinter import ttk


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


# Функция для очистки полей ввода и графиков перед очерендым просчётом
def clean():
    # global details_frame
    entry_width.delete(0, END)
    entry_length.delete(0, END)
    entry_amount.delete(0, END)
    entry_percents.delete(0, END)
    canvas_graph.delete("all")  # Очистка Canvas перед отрисовкой очередного графика
    canvas_graph_2.delete("all")  # Очистка Canvas перед отрисовкой очередного графика
    report_type_client_var.set("")
    report_type_lack_var.set("")
    report_film_var.set("")
    report_amount_var.set("")
    report_width_var.set("")
    report_length_var.set("")
    report_percents_var.set("")
    report_cost_all_amount_var.set("")
    report_cost_one_sheet_var.set("")
    button_show_details["text"] = "Показать детали"
    details_frame.config(height=1)  # сжимаем окно до 1 пикселя, что бы не отображалась подробная калькуляция
    entry_amount.focus()  # Устанавливаем курсор в поле ввода тиража


# Функция для проверки перед просчетом корректности заполнения всех необходисых полей.
def check_filling(*args):
    if entry_width.get().isdigit() and entry_length.get().isdigit() and entry_amount.get().isdigit() and \
            entry_percents.get().isdigit():
        if int(entry_width.get()) < 1 or int(entry_width.get()) > 1000:
            entry_width.config(bg="red")
            entry_width.after(300, lambda: entry_width.config(bg="white"))
        elif int(entry_length.get()) < 1 or int(entry_length.get()) > 1000:
            entry_length.config(bg="red")
            entry_length.after(300, lambda: entry_length.config(bg="white"))
        elif int(entry_amount.get()) < 1 or int(entry_amount.get()) > 10000000:
            entry_amount.config(bg="red")
            entry_amount.after(300, lambda: entry_amount.config(bg="white"))
        elif int(entry_percents.get()) < 1 or int(entry_percents.get()) > 100:
            entry_percents.config(bg="red")
            entry_percents.after(300, lambda: entry_percents.config(bg="white"))
        else:
            calculate()
    else:
        if entry_width.get().isdigit() == False:
            entry_width.config(bg="red")
            entry_width.after(300, lambda: entry_width.config(bg="white"))
        if entry_length.get().isdigit() == False:
            entry_length.config(bg="red")
            entry_length.after(300, lambda: entry_length.config(bg="white"))
        if entry_amount.get().isdigit() == False:
            entry_amount.config(bg="red")
            entry_amount.after(300, lambda: entry_amount.config(bg="white"))
        if entry_percents.get().isdigit() == False:
            entry_percents.config(bg="red")
            entry_percents.after(300, lambda: entry_percents.config(bg="white"))


# Функция для вычисления итоговой стоимости выполнения лакировки
def calculate_result(i, amount):
    answer = (float(dic_all_prices["adjustment_cost"][i]) + float(dic_all_prices["drum"][i]) + (
            float(entry_length.get()) * float(entry_width.get()) * float(entry_percents.get()) / 100000000 * float(
        dic_type_lack[type_lack.get()][1]) * float(dic_type_lack[type_lack.get()][0]) * float(
        amount) + (float(dic_all_prices["dryer"][i]) * float(dic_all_prices["electricity"][i]) + float(
        dic_all_prices["salary"][i])) * float(amount) / float(dic_all_prices["speed"][i]) + float(
        amount) * float(dic_all_prices["printing"][i]) + float(
        dic_all_prices["adjustment_time"][i]) * float(dic_all_prices["salary"][i])) + float(
        dic_all_prices["film"][i]) * float(dic_films_reused[film_reused.get()])) * float(
        dic_type_client[type_client.get()])
    return answer


# Функция отрабатывает команду "Рассчитать"
def calculate():
    # Если один из размеров листа больше 500 мм, цены берем для второй категории заказа
    if int(entry_length.get()) > 500 or int(entry_width.get()) > 500:
        i = 1
    else:
        i = 0
    result = calculate_result(i, entry_amount.get())
    draw_graph_all_amount(i)  # Отрисовка графика ст-ти тиража к размеру тиража
    draw_graph_one_sheet(i)  # Отрисовка графика ст-ти одного листа при лакировке тиража

    # Внесение данных в переменные для отображения итогов расчёта
    report_type_client_var.set(type_client.get())
    report_type_lack_var.set(type_lack.get())
    report_film_var.set(film_reused.get())
    report_amount_var.set(entry_amount.get())
    report_width_var.set(entry_width.get())
    report_length_var.set(entry_length.get())
    report_percents_var.set(entry_percents.get())
    report_cost_all_amount_var.set(f"{result:.2f}")
    report_cost_one_sheet_var.set(f"{result / float(entry_amount.get()):.3f}")

    # Вычисление и внесение данных для отображения подробной калькуляции
    details_cost_lack_var.set(f"""{(float(entry_length.get()) * float(entry_width.get()) * float(
        entry_percents.get()) / 100000000 * float(dic_type_lack[type_lack.get()][1]) * float(
        dic_type_lack[type_lack.get()][0]) * float(entry_amount.get())):.2f}""")
    details_salary_employee_var.set(f"""{((float(dic_all_prices["salary"][i])) * float(
        entry_amount.get()) / float(dic_all_prices["speed"][i]) + float(
        dic_all_prices["adjustment_time"][i]) * float(dic_all_prices["salary"][i])):.2f}""")
    details_electricity_var.set(f"""{((float(dic_all_prices["dryer"][i]) * float(
        dic_all_prices["electricity"][i])) * float(entry_amount.get()) / float(dic_all_prices["speed"][i])):.2f}""")
    details_film_var.set(f"""{(float(dic_all_prices["film"][i]) * float(dic_films_reused[film_reused.get()])):.2f}""")
    details_drum_var.set(f"""{float(dic_all_prices["drum"][i]):.2f}""")
    details_profit_var.set(f"""{(result - float(details_cost_lack_var.get())  - float(
        details_salary_employee_var.get()) - float(details_electricity_var.get()) - float(
        details_film_var.get()) - float(details_drum_var.get())):.2f}""")
    details_time_var.set(f"""{(float(entry_amount.get()) / float(dic_all_prices["speed"][i]) + float(
        dic_all_prices["adjustment_time"][i])):.2f}""")


def draw_graph_all_amount(i):  # Отрисовка графика ст-ти тиража к размеру тиража
    x0 = 35  # Координата точки "х=0" в координатах Canvas
    y0 = 220  # Координата точки "у=0" в координатах Canvas
    x_max = 580  # Кол-во пикселей от точки ноль до максимальной точки графика по оси "х"
    y_max = 190  # Кол-во пикселей от точки ноль до максимальной точки графика по оси "у"
    x_begin = x0  # Начальная точка "х" отрезка, из которых строится итоговый график. Вычисляется каждую итерацию.
    y_begin = y0  # Начальная точка "у" отрезка, из которых строится итоговый график. Вычисляется каждую итерацию.
    scale_x_graph_amount = float(entry_amount.get()) * 2 / x_max  # Коэф. пересчёта масштаба для оси "х"
    scale_y = y_max / calculate_result(i, float(entry_amount.get()) * 2)  # Коэф. пересчёта масштаба для оси "у"
    graph_amount = scale_x_graph_amount  # Значение для оси "х" увеличивающееся для каждой итерации построения графика
    canvas_graph.delete("all")  # Очистка Canvas перед отрисовкой очередного графика
    canvas_graph.create_line(x0 - 10, y0, x0 + x_max + 20, y0, width=1, arrow=LAST)  # Ось "x" координатной оси
    canvas_graph.create_line(x0, y0 + 10, x0, y0 - y_max - 20, width=1, arrow=LAST)  # Ось "y" координатной оси
    canvas_graph.create_line(x0 + x_max / 2, y0, x0 + x_max / 2, y0 - calculate_result(i, entry_amount.get()) * scale_y,
                             width=1, dash=(4, 2), fill="grey")
    canvas_graph.create_line(x0 + x_max, y0, x0 + x_max,
                             y0 - calculate_result(i, float(entry_amount.get()) * 2) * scale_y, width=1, dash=(4, 2),
                             fill="grey")
    canvas_graph.create_line(x0, y0 - calculate_result(i, entry_amount.get()) * scale_y, x0 + x_max / 2,
                             y0 - calculate_result(i, entry_amount.get()) * scale_y, width=1, dash=(4, 2), fill="grey")
    canvas_graph.create_line(x0, y0 - calculate_result(i, float(entry_amount.get()) * 2) * scale_y, x0 + x_max,
                             y0 - calculate_result(i, float(entry_amount.get()) * 2) * scale_y, width=1, dash=(4, 2),
                             fill="grey")
    canvas_graph.create_text(x0 + x_max - 45, y0 - 10, text="Тираж, листов")
    canvas_graph.create_text(x0 + 38, y0 - y_max - 10, text="Ст-сть, грн")
    canvas_graph.create_text(x0 + 10, y0 + 10, text="0")  # Подпись на оси "х". Точна "0"
    canvas_graph.create_text(x0 + x_max / 2, y0 + 10,
                             text=entry_amount.get(), fill="red")  # Подпись на оси "х". Расcчитываемый тираж
    canvas_graph.create_text(x0 + x_max, y0 + 10,
                             text=int(entry_amount.get()) * 2)  # Подпись на оси "х". Расчитываемый тираж * 2
    canvas_graph.create_text(x0 - 3, y0 - calculate_result(i, 1) * scale_y, text=int(calculate_result(i, 1)),
                             anchor=E)  # Подпись на оси "у". Ст-ть при тираже 1 лист.
    canvas_graph.create_text(x0 - 3, y0 - calculate_result(i, entry_amount.get()) * scale_y,
                             text=int(calculate_result(i, entry_amount.get())),
                             anchor=E, fill="red")  # Подпись на оси "у". Ст-ть при исходном тираже листов
    canvas_graph.create_text(x0 - 3, y0 - calculate_result(i, float(entry_amount.get()) * 2) * scale_y,
                             text=int(calculate_result(i, float(entry_amount.get()) * 2)),
                             anchor=E)  # Подпись на оси "у". Ст-ть при удвоенном тираже листов
    for j in range(1, x_max + 1):
        result_graph = calculate_result(i, graph_amount)
        graph_amount += scale_x_graph_amount
        x_begin += 1
        y_begin = y0 - result_graph * scale_y
        canvas_graph.create_line(x_begin, y_begin, x_begin + 1, y0 - result_graph * scale_y, width=1)  # график


def draw_graph_one_sheet(i):  # Отрисовка графика ст-ти одного листа при лакировке тиража
    x0 = 35  # Координата точки "х=0" в координатах Canvas
    y0 = 220  # Координата точки "у=0" в координатах Canvas
    x_max = 580  # Кол-во пикселей от точки ноль до максимальной точки графика по оси "х"
    y_max = 190  # Кол-во пикселей от точки ноль до максимальной точки графика по оси "у"
    x_begin = x0  # Начальная точка "х" отрезка, из которых строится итоговый график
    # y_begin = y0  # Начальная точка "у" отрезка, из которых строится итоговый график
    scale_x_graph_amount = float(entry_amount.get()) * 2 / x_max  # Коэф. пересчёта масштаба для оси "х"
    # Коэф. пересчёта масштаба для оси "у"
    scale_y = y_max / (calculate_result(i, float(entry_amount.get()) / 2) / (float(entry_amount.get()) / 2))
    graph_amount = scale_x_graph_amount  # Значение для оси "х" увеличивающееся для каждой итерации построения графика
    canvas_graph_2.delete("all")  # Очистка Canvas перед отрисовкой очередного графика
    canvas_graph_2.create_line(x0 - 10, y0, x0 + x_max + 20, y0, width=1, arrow=LAST)  # Ось "x" координатной оси
    canvas_graph_2.create_line(x0, y0 + 10, x0, y0 - y_max - 20, width=1, arrow=LAST)  # Ось "y" координатной оси
    canvas_graph_2.create_line(x0 + x_max / 2, y0, x0 + x_max / 2,
                               y0 - (calculate_result(i, entry_amount.get()) / float(entry_amount.get())) * scale_y,
                               width=1, dash=(4, 2), fill="grey")  # Пунктир на ось "х" в точку тиража
    canvas_graph_2.create_line(x0 + x_max, y0, x0 + x_max, y0 - (
                calculate_result(i, float(entry_amount.get()) * 2) / (float(entry_amount.get()) * 2)) * scale_y,
                               width=1, dash=(4, 2), fill="grey")  # Пунктир на ось "х" в точку удвоенного тиража
    canvas_graph_2.create_line(x0, y0 - (calculate_result(i, entry_amount.get()) / float(entry_amount.get())) * scale_y,
                               x0 + x_max / 2,
                               y0 - (calculate_result(i, entry_amount.get()) / float(entry_amount.get())) * scale_y,
                               width=1, dash=(4, 2), fill="grey")  # Пунктир на ось "у" в точку стоимости тиража
    canvas_graph_2.create_line(x0, y0 - (
                calculate_result(i, float(entry_amount.get()) * 2) / (float(entry_amount.get()) * 2)) * scale_y,
                               x0 + x_max, y0 - (calculate_result(i, float(entry_amount.get()) * 2) / (
                    float(entry_amount.get()) * 2)) * scale_y, width=1, dash=(4, 2),
                               fill="grey")  # Пунктир на ось "у" в точку стоимости удвоенного тиража
    canvas_graph_2.create_line(x0, y0 - (calculate_result(i, 1000000) / 1000000) * scale_y, x0 + x_max + 10,
                               y0 - (calculate_result(i, 1000000) / 1000000) * scale_y, width=1, dash=(4, 2),
                               fill="grey")  # Пунктир на ось "у" в точку стоимости максимально возможного тиража
    canvas_graph_2.create_text(x0 + x_max - 45, y0 - 10, text="Тираж, листов")
    canvas_graph_2.create_text(x0 + 60, y0 - y_max - 10, text="Ст-сть за лист, грн")
    canvas_graph_2.create_text(x0 + 10, y0 + 10, text="0")  # Подпись на оси "х". Точна "0"
    canvas_graph_2.create_text(x0 + x_max / 2, y0 + 10, text=entry_amount.get(),
                               fill="red")  # Подпись на оси "х". Расчитываемый тираж
    canvas_graph_2.create_text(x0 + x_max, y0 + 10,
                               text=int(entry_amount.get()) * 2)  # Подпись на оси "х". Расчитываемый тираж * 2
    canvas_graph_2.create_text(x0 - 3,
                               y0 - (calculate_result(i, entry_amount.get()) / float(entry_amount.get())) * scale_y,
                               text=f"{(float((calculate_result(i, entry_amount.get()) / float(entry_amount.get())))):.3f}",
                               anchor=E, fill="red")  # Подпись на оси "у". Ст-ть при исходном тираже листов
    canvas_graph_2.create_text(x0 - 3, y0 - (
                calculate_result(i, float(entry_amount.get()) * 2) / (float(entry_amount.get()) * 2)) * scale_y,
                               text=f"{float((calculate_result(i, float(entry_amount.get()) * 2) / (float(entry_amount.get()) * 2))):.3f}",
                               anchor=E)  # Подпись на оси "у". Ст-ть при удвоенном тираже листов
    canvas_graph_2.create_text(x0 - 3, y0 - (calculate_result(i, 1000000) / 1000000) * scale_y,
                               text=f"{float((calculate_result(i, 1000000) / 1000000)):.3f}",
                               anchor=E)  # Подпись на оси "у". Ст-ть при максимально возможном тираже

    for j in range(1, x_max + 1):
        result_graph = calculate_result(i, graph_amount) / graph_amount
        graph_amount += scale_x_graph_amount
        x_begin += 1
        y_begin = y0 - result_graph * scale_y
        canvas_graph_2.create_line(x_begin, y_begin, x_begin + 1, y0 - result_graph * scale_y, width=1)


# Функция для включения и выключения отображения подробной калькуляции расчитывемого заказа.
def details():
    if button_show_details["text"] == "Показать детали":
        details_frame.config(height=200)  # Увеличиваем размер окна, что бы отображалась подробная калькуляция
        button_show_details["text"] = "Скрыть детали"
    else:
        button_show_details["text"] = "Показать детали"
        details_frame.config(height=1)  # сжимаем окно до 1 пикселя, что бы не отображалась подробная калькуляция


# Функция отображения всех расценок
def show_prices():
    prices_window = Toplevel(root)
    prices_window.geometry("1200x680+100+35")
    prices_text_column_less_b3 = Label(prices_window, text="Печатный лист меньше В-3")
    prices_text_column_more_b3 = Label(prices_window, text="Печатный лист больше В-3")
    prices_text_electricity = Label(prices_window, text="Стоимость электричества")
    prices_text_electricity_measure = Label(prices_window, text="грн/кВт.")
    prices_text_drum = Label(prices_window, text="Стоимость изготовления рамки")
    prices_text_drum_measure = Label(prices_window, text="грн/шт.")
    price_text_film = Label(prices_window, text="Стоимость плёнки")
    price_text_film_measure = Label(prices_window, text="грн/шт.")
    price_text_dryer = Label(prices_window, text="Мощность потребляемой электроэнергии")
    price_text_dryer_measure = Label(prices_window, text="кВт.")
    price_text_salary = Label(prices_window, text="Зарплата лакировщика")
    price_text_salary_measure = Label(prices_window, text="грн/час.")
    price_text_printing = Label(prices_window, text="Стоиомсть лакировки")
    price_text_printing_measure = Label(prices_window, text="грн/проход")
    price_text_speed = Label(prices_window, text="Скорость лакировки")
    price_text_speed_measure = Label(prices_window, text="лист/час.")
    price_text_adjustment_cost = Label(prices_window, text="Стоимость приладки")
    price_text_adjustment_cost_measure = Label(prices_window, text="грн.")
    price_text_adjustment_time = Label(prices_window, text="Время приладки")
    price_text_adjustment_time_measure = Label(prices_window, text="часю")

    prices_text_column_less_b3.grid(row=0, column=2)
    prices_text_column_more_b3.grid(row=0, column=3)
    prices_text_electricity.grid(row=1, column=0)
    prices_text_electricity_measure.grid(row=1, column=1)
    prices_text_drum.grid(row=2, column=0)
    prices_text_drum_measure.grid(row=2, column=1)
    price_text_film.grid(row=3, column=0)
    price_text_film_measure.grid(row=3, column=1)
    price_text_dryer.grid(row=4, column=0)
    price_text_dryer_measure.grid(row=4, column=1)
    price_text_salary.grid(row=5, column=0)
    price_text_salary_measure.grid(row=5, column=1)
    price_text_printing.grid(row=6, column=0)
    price_text_printing_measure.grid(row=6, column=1)
    price_text_speed.grid(row=7, column=0)
    price_text_speed_measure.grid(row=7, column=1)
    price_text_adjustment_cost.grid(row=8, column=0)
    price_text_adjustment_cost_measure.grid(row=8, column=1)
    price_text_adjustment_time.grid(row=9, column=0)
    price_text_adjustment_time_measure.grid(row=9, column=1)


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
root.geometry("1200x680+100+35")
root.iconbitmap("TimPack.ico")
root.title("Расчёт стоимости УФ-лакировки")
root.option_add('*tearOff', FALSE)

# Создание меню
menubar = Menu(root)
root["menu"] = menubar
menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='Файл')
menubar.add_cascade(menu=menu_edit, label='Настройки')
menu_file.add_command(label='New', command=clean)
menu_file.add_command(label='Open...', command=clean)
menu_file.add_command(label='Close', command=clean)
menu_edit.add_command(label='Посмотреть расцени', command=show_prices)

details_frame = Frame(root, width=400, height=1)
details_frame.place(x=70, y=400)

type_lack = StringVar()  # Раскрывающийся список для выбора типа лакировки
type_lack.set("УФ-лак")
button_type_lack = OptionMenu(root, type_lack, *dic_type_lack)
button_type_lack.config(width=32)
button_type_lack.place(x=30, y=10)

type_client = StringVar()  # Раскрывающийся спсисок для выбора типа клиента
type_client.set("премиум")
button_type_client = OptionMenu(root, type_client, *dic_type_client)  # Кнопка для выбора типа клиента
button_type_client.place(x=170, y=42)

film_reused = StringVar()
film_reused.set("новая")
checkbutton_film_reused = Checkbutton(root, variable=film_reused, onvalue="новая",
                                      offvalue="повторная или заказчика")
checkbutton_film_reused.place(x=412, y=108)

separator_line_1 = ttk.Separator(root, orient=VERTICAL)
separator_line_1.place(x=279, y=10, height=120)

text_type_client = Label(root, text="Тип клиента:")
text_amount = Label(root, text="Тираж, листов:")
text_percents = Label(root, text="% заполнения:")
text_format = Label(root, text="Формат печатного листа", width=23)
text_width = Label(root, text="Ширина, мм:")
text_length = Label(root, text="Длина, мм:")
text_film = Label(root, text="Плёнка:")

text_type_client.place(x=30, y=50)
text_amount.place(x=30, y=80)
text_percents.place(x=30, y=110)
text_format.place(x=280, y=20)
text_width.place(x=290, y=50)
text_length.place(x=290, y=80)
text_film.place(x=290, y=110)

report_type_client_name = Label(root, text="Тип клиента:", justify=LEFT)
report_type_client_var = StringVar()
report_type_client = Label(root, textvariable=report_type_client_var, font="TkDefaultFont 11 bold italic")
report_type_lack_name = Label(root, text="Тип лака:")
report_type_lack_var = StringVar()
report_type_lack = Label(root, textvariable=report_type_lack_var, font="TkDefaultFont 11 bold italic")
report_film_name = Label(root, text="Плёнка:")
report_film_var = StringVar()
report_film = Label(root, textvariable=report_film_var, font="TkDefaultFont 11 bold italic")
report_amount_name = Label(root, text="Тираж:")
report_amount_var = StringVar()
report_amount = Label(root, textvariable=report_amount_var, font="TkDefaultFont 11 bold italic")
report_amount_measure = Label(root, text="лист.")
report_width_name = Label(root, text="Ширина листа:")
report_width_var = StringVar()
report_width = Label(root, textvariable=report_width_var, font="TkDefaultFont 11 bold italic")
report_width_measure = Label(root, text="мм.")
report_length_name = Label(root, text="Длина листа:")
report_length_var = StringVar()
report_length = Label(root, textvariable=report_length_var, font="TkDefaultFont 11 bold italic")
report_length_measure = Label(root, text="мм.")
report_percents_name = Label(root, text="Процент заполнения листа:")
report_percents_var = StringVar()
report_percents = Label(root, textvariable=report_percents_var, font="TkDefaultFont 11 bold italic")
report_percents_measure = Label(root, text="%")
report_cost_all_amount_name = Label(root, text="Стоимость лакировки тиража:")
report_cost_all_amount_var = StringVar()
report_cost_all_amount = Label(root, textvariable=report_cost_all_amount_var, font="TkDefaultFont 11 bold italic", fg="red")
report_cost_all_amount_measure = Label(root, text="грн.")
report_cost_one_sheet_name = Label(root, text="Стоимость лакировки одного листа:")
report_cost_one_sheet_var = StringVar()
report_cost_one_sheet = Label(root, textvariable=report_cost_one_sheet_var, font="TkDefaultFont 11 bold italic", fg="red")
report_cost_one_sheet_measure = Label(root, text="грн.")

report_type_client_name.place(x=80, y=170)
report_type_client.place(x=420, y=192, anchor="se")
report_type_lack_name.place(x=80, y=195)
report_type_lack.place(x=420, y=217, anchor="se")
report_film_name.place(x=80, y=220)
report_film.place(x=420, y=242, anchor="se")
report_amount_name.place(x=80, y=245)
report_amount.place(x=420, y=267, anchor="se")
report_amount_measure.place(x=425, y=245)
report_width_name.place(x=80, y=270)
report_width.place(x=420, y=292, anchor="se")
report_width_measure.place(x=425, y=270)
report_length_name.place(x=80, y=295)
report_length.place(x=420, y=317, anchor="se")
report_length_measure.place(x=425, y=295)
report_percents_name.place(x=80, y=320)
report_percents.place(x=420, y=342, anchor="se")
report_percents_measure.place(x=425, y=320)
report_cost_all_amount_name.place(x=80, y=345)
report_cost_all_amount.place(x=420, y=367, anchor="se")
report_cost_all_amount_measure.place(x=425, y=345)
report_cost_one_sheet_name.place(x=80, y=370)
report_cost_one_sheet.place(x=420, y=392, anchor="se")
report_cost_one_sheet_measure.place(x=425, y=370)

details_cost_lack_name = Label(details_frame, text="Стоимость УФ-лака:")
details_cost_lack_var = StringVar()
details_cost_lack = Label(details_frame, textvariable=details_cost_lack_var, font="TkDefaultFont 11 bold italic")
details_cost_lack_measure = Label(details_frame, text="грн.")
details_salary_employee_name = Label(details_frame, text="Зарплата печатника:")
details_salary_employee_var = StringVar()
details_salary_employee = Label(details_frame, textvariable=details_salary_employee_var, font="TkDefaultFont 11 bold italic")
details_salary_employee_measure = Label(details_frame, text="грн.")
details_electricity_name = Label(details_frame, text="Стоимость электричества:")
details_electricity_var = StringVar()
details_electricity = Label(details_frame, textvariable=details_electricity_var, font="TkDefaultFont 11 bold italic")
details_electricity_measure = Label(details_frame, text="грн.")
details_film_name = Label(details_frame, text="Стоимость пленки")
details_film_var = StringVar()
details_film = Label(details_frame, textvariable=details_film_var, font="TkDefaultFont 11 bold italic")
details_film_measure = Label(details_frame, text="грн.")
details_drum_name = Label(details_frame, text="Стоимость рамки:")
details_drum_var = StringVar()
details_drum = Label(details_frame, textvariable=details_drum_var, font="TkDefaultFont 11 bold italic")
details_drum_measure = Label(details_frame, text="грн.")
details_profit_name = Label(details_frame, text="Заработок:")
details_profit_var = StringVar()
details_profit = Label(details_frame, textvariable=details_profit_var, font="TkDefaultFont 11 bold italic")
details_profit_measure = Label(details_frame, text="грн.")
details_time_name = Label(details_frame, text="Время лакировки:")
details_time_var = StringVar()
details_time = Label(details_frame, textvariable=details_time_var, font="TkDefaultFont 11 bold italic")
details_time_measure = Label(details_frame, text="ч.")

# Размещение виджетов описания подробной калькуляции в координатах "details_frame"
details_cost_lack_name.place(x=10, y=10)
details_cost_lack.place(x=350, y=31, anchor="se")
details_cost_lack_measure.place(x=355, y=10)
details_salary_employee_name.place(x=10, y=35)
details_salary_employee.place(x=350, y=56, anchor="se")
details_salary_employee_measure.place(x=355, y=35)
details_electricity_name.place(x=10, y=60)
details_electricity.place(x=350, y=81, anchor="se")
details_electricity_measure.place(x=355, y=60)
details_film_name.place(x=10, y=85)
details_film.place(x=350, y=106, anchor="se")
details_film_measure.place(x=355, y=85)
details_drum_name.place(x=10, y=110)
details_drum.place(x=350, y=131, anchor="se")
details_drum_measure.place(x=355, y=110)
details_profit_name.place(x=10, y=135)
details_profit.place(x=350, y=156, anchor="se")
details_profit_measure.place(x=355, y=135)
details_time_name.place(x=10, y=160)
details_time.place(x=350, y=181, anchor="se")
details_time_measure.place(x=355, y=160)

entry_amount = Entry(root, width=10, justify=RIGHT)
entry_percents = Entry(root, width=10, justify=RIGHT)
entry_width = Entry(root, width=10, justify=RIGHT)
entry_length = Entry(root, width=10, justify=RIGHT)

entry_amount.place(x=200, y=80)
entry_percents.place(x=200, y=110)
entry_width.place(x=370, y=50)
entry_length.place(x=370, y=80)

button_A4 = Button(root, text="A4", command=lambda: set_format("A4"), width=5)
button_B4 = Button(root, text="B4", command=lambda: set_format("B4"), width=5)
button_A3 = Button(root, text="A3", command=lambda: set_format("A3"), width=5)
button_B3 = Button(root, text="B3", command=lambda: set_format("B3"), width=5)
button_sixthA1 = Button(root, text="""1/6 A1""", command=lambda: set_format("""1/6 A1"""), width=5)
button_sixthB1 = Button(root, text="""1/6 B1""", command=lambda: set_format("""1/6 B1"""), width=5)
button_A2 = Button(root, text="A2", command=lambda: set_format("A2"), width=5)
button_B2 = Button(root, text="B2", command=lambda: set_format("B2"), width=5)
button_calculate = Button(root, text="Рассчитать", command=check_filling, width=23)
button_clean = Button(root, text="Очистить", command=clean, width=23)
button_show_details = Button(root, text="Показать детали", command=details, width=23)

button_A4.place(x=445, y=15)
button_B4.place(x=495, y=15)
button_A3.place(x=445, y=45)
button_B3.place(x=495, y=45)
button_sixthA1.place(x=445, y=75)
button_sixthB1.place(x=495, y=75)
button_A2.place(x=445, y=105)
button_B2.place(x=495, y=105)
button_calculate.place(x=10, y=140)
button_clean.place(x=190, y=140)
button_show_details.place(x=370, y=140)

canvas_graph = Canvas(root, width=637, height=250)
canvas_graph.place(x=560, y=2)
canvas_graph_2 = Canvas(root, width=637, height=250)
canvas_graph_2.place(x=560, y=300)

root.bind("<Return>", check_filling)  # Выполнить расчет по нажатию клавиши Enter/Return
entry_amount.focus()  # Устанавливаем курсор в поле ввода тиража
root.mainloop()
