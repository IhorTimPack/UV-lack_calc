from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import json
import time
import os
import os.path
import cv2
import pdf2image


# Функция для заполнения полей длины и ширины печатного листа типовыми размерами из словаря.
def set_format(f):
    entry_width.delete(0, END)
    entry_length.delete(0, END)
    entry_width.insert(0, dic_formats[f][0])
    entry_length.insert(0, dic_formats[f][1])


# Функция для очистки полей ввода и графиков перед очерендым просчётом
def clean():
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


# Функция перед просчетом проверяет корректность заполнения всех необходимых полей.
# Если поле заполнено некорректно, оно меняет свой цвет на красный на 0,3 сек.
# Если всё заполнено корректно, запускается функция "calculate", которая проводит расчёт.
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
def calculate_result(i, amount):  # Аргументы: тип заказа по размеру листа (> или < В3), тираж.
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


# Функция отрабатывает команду "Рассчитать". Запускается функцией "check filling".
def calculate():
    # Если один из размеров листа больше 500 мм, цены берем для второй категории заказов "i=1"
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
    # В цикле рисуем график маленькими отрезками с шагом по оси "х" в один пиксель
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


# Функция перед сохранением профиля создает окно в котором запрашивает пароль
def confirm_saving():
    global password_entry
    global password_window
    password_window = Toplevel(root)
    password_window.title("Введите пароль")
    password_window.geometry("280x90+200+100")
    password_window.grab_set()  # Не позволяет работать с другим окном, пока это окно не закрыто
    password_entry = Entry(password_window, show="*", justify="center")
    password_entry.focus()  # Помещаем курсор в поле ввода пароля
    password_window.bind("<Return>", check_password)  # Можем подтвердить ввод пароля нажатием Enter
    password_button = Button(password_window, text="Подтвердить", command=check_password)
    password_entry.pack(padx=5, pady=10)
    password_button.pack()


# Проверка пароля для функции подтверждения сохранения. Если пароль правильный, запускается функция сохранения.
def check_password(*args):
    if password_entry.get() == str(55555):
        save_data()
        password_window.destroy()
    else:  # Если пароль неверный поле ввода меняет цвет на красный на 0,3 сек и ждём повторного ввода пароля.
        password_entry.config(bg="red")
        password_entry.after(300, lambda: password_entry.config(bg="white"))
        password_entry.delete(0, END)


# Функция создает окно для ввода имени создаваемого профиля. После ввода имени профиля после нажатия клавиши "Enter"
# или нажатия на кнопку "Сохранить профиль" запускается на выполнение функция "save_profile"
def create_profile():
    global create_profile_entry
    global create_profile_window
    create_profile_window = Toplevel(root)
    create_profile_window.title("Введите название профиля")
    create_profile_window.geometry("320x90+200+100")
    create_profile_window.grab_set()  # Не позволяет работать с другим окном, пока это окно не закрыто
    create_profile_entry = Entry(create_profile_window)
    create_profile_entry.focus()
    create_profile_window.bind("<Return>", save_profile)
    create_profile_button = Button(create_profile_window, text="Сохранить профиль", command=save_profile)
    create_profile_entry.pack(padx=5, pady=10)
    create_profile_button.pack()


# Функция добавляет в соответствующий словарь название файла в котором будут данные создаваемого профиля,
# записывает в переменную путь к этому файлу с данными и даёт команду на сохранения файла
def save_profile(*args):
    global path_data
    dic_name_file_profile[create_profile_entry.get()] = "UV_lack_calc_data_" + create_profile_entry.get() + ".json"
    path_data = path_folder + "\\" + dic_name_file_profile[create_profile_entry.get()]
    save_data()
    save_list_profiles()
    switch_profile()
    create_profile_window.destroy()


# Функция считывает выбранное из раскрывающегося списка название профиля, формирует переменную с указанием пути к
# файлу с профилем. Загружает данный профиль и обновляет данные окна разрушая и заново его создавая.
def switch_profile(*args):
    global path_data
    global selected_profile
    selected_profile = price_type_profile.get()  # Присваиваем значение выбранного профиля
    type_profile_var.set(selected_profile)  # В переменную записываем название выбранного профиля для отображения в главном окне
    path_data = path_folder + "\\" + dic_name_file_profile[selected_profile]  # Путь к выбранному профилю
    if os.path.isfile(path_data):
        load_data()  # Загружаем в программу данные расценок выбранного профиля
        check_filling()  # Пересчитываем расчет для выбранного профиля
        prices_pop_up.destroy()
        show_prices()
    else: # Программа не нашло файл данными для данного профиля, берем данные из "Основного" профиля.
        selected_profile = "Основной"
        check_filling()  # Пересчитываем расчет для выбранного профиля
        prices_pop_up.destroy()
        show_prices()


# Функция отображения всех расценок
def show_prices():
    global prices_pop_up
    prices_pop_up = Toplevel(root)
    prices_pop_up.title("Расценки, нормы расхода")
    prices_pop_up.geometry("1200x680+100+35")
    prices_pop_up.grab_set()  # Не позволяет работать с другим окном, пока это окно не закрыто
    prices_window = Frame(prices_pop_up)
    prices_window.grid(row=0, column=0, padx=20, pady=20)

    price_button_save = Button(prices_window, text="Сохранить изменения в текущем профиле", command=confirm_saving)
    price_button_save_another = Button(prices_window, text="Создать новый профиль и сохранить изменения", command=create_profile)
    price_button_save.grid(row=20, column=0, columnspan=2, padx=5, pady=10, sticky=EW)
    price_button_save_another.grid(row=21, column=0, columnspan=2, padx=5, sticky=EW)

    # Выбор профиля из раскрывающекося списка и загрузка его в программу.
    global price_type_profile
    price_type_profile = StringVar()
    price_type_profile.set(selected_profile)
    price_text_select = Label(prices_window, text="Сменить профиль:")
    price_text_title = Label(prices_window, text="Профиль: " + price_type_profile.get(), font="TkDefaultFont 9 bold italic")
    price_text_select.grid(row=20, column=2, columnspan=2)
    price_text_title.grid(row=0, column=0)
    price_button_type_profile = OptionMenu(prices_window, price_type_profile, *dic_name_file_profile, command=switch_profile)
    price_button_type_profile.grid(row=21, column=2, columnspan=2, padx=5, sticky=EW)

    price_text_column = Label(prices_window, text="Формат печатного листа", font="TkDefaultFont 8 bold")
    price_text_column_less_b3 = Label(prices_window, text="< В-3", font="TkDefaultFont 8 bold")
    price_text_column_more_b3 = Label(prices_window, text="> В-3", font="TkDefaultFont 8 bold")
    price_text_electricity = Label(prices_window, text="Стоимость электричества")
    price_text_electricity_measure = Label(prices_window, text="грн/кВт.")
    price_text_drum = Label(prices_window, text="Стоимость изготовления рамки")
    price_text_drum_measure = Label(prices_window, text="грн/шт.")
    price_text_film = Label(prices_window, text="Стоимость плёнки")
    price_text_film_measure = Label(prices_window, text="грн/шт.")
    price_text_dryer = Label(prices_window, text="Мощность потребляемой электроэнергии")
    price_text_dryer_measure = Label(prices_window, text="кВт.")
    price_text_salary = Label(prices_window, text="Зарплата лакировщика")
    price_text_salary_measure = Label(prices_window, text="грн/час.")
    price_text_printing = Label(prices_window, text="Стоимость лакировки")
    price_text_printing_measure = Label(prices_window, text="грн/проход")
    price_text_speed = Label(prices_window, text="Скорость лакировки")
    price_text_speed_measure = Label(prices_window, text="лист/час.")
    price_text_adjustment_cost = Label(prices_window, text="Стоимость приладки")
    price_text_adjustment_cost_measure = Label(prices_window, text="грн.")
    price_text_adjustment_time = Label(prices_window, text="Время приладки")
    price_text_adjustment_time_measure = Label(prices_window, text="час.")
    price_text_UV_lack_column_1 = Label(prices_window, text="Ст-ть, грн/кг.", font="TkDefaultFont 8 bold")
    price_text_UV_lack_column_2 = Label(prices_window, text="Расход, кг/м.кв.", font="TkDefaultFont 8 bold")
    price_text_UV_lack_1 = Label(prices_window, text="УФ-лак")
    price_text_UV_lack_2 = Label(prices_window, text="УФ-лак с поднятием")
    price_text_UV_lack_3 = Label(prices_window, text="Глиттер + УФ-лак (1:5)")
    price_text_UV_lack_4 = Label(prices_window, text="Глиттер + УФ-лак с поднятием (1:5)")
    price_text_client = Label(prices_window, text="Тип клиента", font="TkDefaultFont 8 bold")
    price_text_client_ineterest = Label(prices_window, text="Коэф. наценки", font="TkDefaultFont 8 bold")
    price_text_client_premium = Label(prices_window, text="Премиум")
    price_text_client_well = Label(prices_window, text="Хорошо")
    price_text_client_standart = Label(prices_window, text="Стандарт")

    price_text_column.grid(row=0, column=2, columnspan=2, sticky=EW)
    price_text_column_less_b3.grid(row=1, column=2)
    price_text_column_more_b3.grid(row=1, column=3)
    price_text_electricity.grid(row=2, column=0, sticky=W)
    price_text_electricity_measure.grid(row=2, column=1)
    price_text_drum.grid(row=3, column=0, sticky=W)
    price_text_drum_measure.grid(row=3, column=1)
    price_text_film.grid(row=4, column=0, sticky=W)
    price_text_film_measure.grid(row=4, column=1)
    price_text_dryer.grid(row=5, column=0, sticky=W)
    price_text_dryer_measure.grid(row=5, column=1)
    price_text_salary.grid(row=6, column=0, sticky=W)
    price_text_salary_measure.grid(row=6, column=1)
    price_text_printing.grid(row=7, column=0, sticky=W)
    price_text_printing_measure.grid(row=7, column=1)
    price_text_speed.grid(row=8, column=0, sticky=W)
    price_text_speed_measure.grid(row=8, column=1)
    price_text_adjustment_cost.grid(row=9, column=0, sticky=W)
    price_text_adjustment_cost_measure.grid(row=9, column=1)
    price_text_adjustment_time.grid(row=10, column=0, sticky=W)
    price_text_adjustment_time_measure.grid(row=10, column=1)
    price_text_UV_lack_column_1.grid(row=11, column=2, pady=3, sticky=S)
    price_text_UV_lack_column_2.grid(row=11, column=3, pady=3, sticky=S)
    price_text_UV_lack_1.grid(row=12, column=0, sticky=W)
    price_text_UV_lack_2.grid(row=13, column=0, sticky=W)
    price_text_UV_lack_3.grid(row=14, column=0, sticky=W)
    price_text_UV_lack_4.grid(row=15, column=0, sticky=W)
    price_text_client.grid(row=16, column=0, pady=3, sticky=W)
    price_text_client_ineterest.grid(row=16, column=2, pady=3, sticky=S)
    price_text_client_premium.grid(row=17, column=0, sticky=W)
    price_text_client_well.grid(row=18, column=0, sticky=W)
    price_text_client_standart.grid(row=19, column=0, sticky=W)

    global price_entry_electricity
    global price_entry_drum_less_b3
    global price_entry_drum_more_b3
    global price_entry_film_less_b3
    global price_entry_film_more_b3
    global price_entry_dryer_less_b3
    global price_entry_dryer_more_b3
    global price_entry_salary_less_b3
    global price_entry_salary_more_b3
    global price_entry_printing_less_b3
    global price_entry_printing_more_b3
    global price_entry_speed_less_b3
    global price_entry_speed_more_b3
    global price_entry_adjustment_cost_less_b3
    global price_entry_adjustment_cost_more_b3
    global price_entry_adjustment_time_less_b3
    global price_entry_adjustment_time_more_b3
    global price_entry_UV_lack_1_cost
    global price_entry_UV_lack_1_outgo
    global price_entry_UV_lack_2_cost
    global price_entry_UV_lack_2_outgo
    global price_entry_UV_lack_3_cost
    global price_entry_UV_lack_3_outgo
    global price_entry_UV_lack_4_cost
    global price_entry_UV_lack_4_outgo
    global price_entry_client_premium
    global price_entry_client_well
    global price_entry_client_standart

    price_entry_electricity = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_drum_less_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_drum_more_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_film_less_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_film_more_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_dryer_less_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_dryer_more_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_salary_less_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_salary_more_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_printing_less_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_printing_more_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_speed_less_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_speed_more_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_adjustment_cost_less_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_adjustment_cost_more_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_adjustment_time_less_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_adjustment_time_more_b3 = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_UV_lack_1_cost = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_UV_lack_1_outgo = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_UV_lack_2_cost = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_UV_lack_2_outgo = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_UV_lack_3_cost = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_UV_lack_3_outgo = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_UV_lack_4_cost = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_UV_lack_4_outgo = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_client_premium = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_client_well = Entry(prices_window, width=10, justify=RIGHT)
    price_entry_client_standart = Entry(prices_window, width=10, justify=RIGHT)

    price_entry_electricity.grid(row=2, column=2, columnspan=2)
    price_entry_drum_less_b3.grid(row=3, column=2)
    price_entry_drum_more_b3.grid(row=3, column=3)
    price_entry_film_less_b3.grid(row=4, column=2)
    price_entry_film_more_b3.grid(row=4, column=3)
    price_entry_dryer_less_b3.grid(row=5, column=2)
    price_entry_dryer_more_b3.grid(row=5, column=3)
    price_entry_salary_less_b3.grid(row=6, column=2)
    price_entry_salary_more_b3.grid(row=6, column=3)
    price_entry_printing_less_b3.grid(row=7, column=2)
    price_entry_printing_more_b3.grid(row=7, column=3)
    price_entry_speed_less_b3.grid(row=8, column=2)
    price_entry_speed_more_b3.grid(row=8, column=3)
    price_entry_adjustment_cost_less_b3.grid(row=9, column=2)
    price_entry_adjustment_cost_more_b3.grid(row=9, column=3)
    price_entry_adjustment_time_less_b3.grid(row=10, column=2)
    price_entry_adjustment_time_more_b3.grid(row=10, column=3)
    price_entry_UV_lack_1_cost.grid(row=12, column=2)
    price_entry_UV_lack_1_outgo.grid(row=12, column=3)
    price_entry_UV_lack_2_cost.grid(row=13, column=2)
    price_entry_UV_lack_2_outgo.grid(row=13, column=3)
    price_entry_UV_lack_3_cost.grid(row=14, column=2)
    price_entry_UV_lack_3_outgo.grid(row=14, column=3)
    price_entry_UV_lack_4_cost.grid(row=15, column=2)
    price_entry_UV_lack_4_outgo.grid(row=15, column=3)
    price_entry_client_premium.grid(row=17, column=2)
    price_entry_client_well.grid(row=18, column=2)
    price_entry_client_standart.grid(row=19, column=2)

    price_entry_electricity.insert(0, dic_all_prices["electricity"][0])
    price_entry_drum_less_b3.insert(0, dic_all_prices["drum"][0])
    price_entry_drum_more_b3.insert(0, dic_all_prices["drum"][1])
    price_entry_film_less_b3.insert(0, dic_all_prices["film"][0])
    price_entry_film_more_b3.insert(0, dic_all_prices["film"][1])
    price_entry_dryer_less_b3.insert(0, dic_all_prices["dryer"][0])
    price_entry_dryer_more_b3.insert(0, dic_all_prices["dryer"][1])
    price_entry_salary_less_b3.insert(0, dic_all_prices["salary"][0])
    price_entry_salary_more_b3.insert(0, dic_all_prices["salary"][1])
    price_entry_printing_less_b3.insert(0, dic_all_prices["printing"][0])
    price_entry_printing_more_b3.insert(0, dic_all_prices["printing"][1])
    price_entry_speed_less_b3.insert(0, dic_all_prices["speed"][0])
    price_entry_speed_more_b3.insert(0, dic_all_prices["speed"][1])
    price_entry_adjustment_cost_less_b3.insert(0, dic_all_prices["adjustment_cost"][0])
    price_entry_adjustment_cost_more_b3.insert(0, dic_all_prices["adjustment_cost"][1])
    price_entry_adjustment_time_less_b3.insert(0, dic_all_prices["adjustment_time"][0])
    price_entry_adjustment_time_more_b3.insert(0, dic_all_prices["adjustment_time"][1])
    price_entry_UV_lack_1_cost.insert(0, dic_type_lack["УФ-лак"][0])
    price_entry_UV_lack_1_outgo.insert(0, dic_type_lack["УФ-лак"][1])
    price_entry_UV_lack_2_cost.insert(0, dic_type_lack["УФ-лак с поднятием"][0])
    price_entry_UV_lack_2_outgo.insert(0, dic_type_lack["УФ-лак с поднятием"][1])
    price_entry_UV_lack_3_cost.insert(0, dic_type_lack["Глиттер + УФ-лак (1:5)"][0])
    price_entry_UV_lack_3_outgo.insert(0, dic_type_lack["Глиттер + УФ-лак (1:5)"][1])
    price_entry_UV_lack_4_cost.insert(0, dic_type_lack["Глиттер + УФ-лак с поднятием (1:5)"][0])
    price_entry_UV_lack_4_outgo.insert(0, dic_type_lack["Глиттер + УФ-лак с поднятием (1:5)"][1])
    price_entry_client_premium.insert(0, dic_type_client["премиум"])
    price_entry_client_well.insert(0, dic_type_client["хорошо"])
    price_entry_client_standart.insert(0, dic_type_client["стандарт"])

    separator_line_2 = ttk.Separator(prices_window, orient=VERTICAL)
    separator_line_3 = ttk.Separator(prices_window, orient=HORIZONTAL)
    separator_line_2.place(x=312, y=432, height=90)
    separator_line_3.place(x=0, y=432, width=500)


def load_picture_calculate_filling():
    load_picture_pop_up = Toplevel(root)
    load_picture_pop_up.title("Определение процента заполнения лаком печатного листа")
    load_picture_pop_up.geometry("1200x680+100+35")
    load_picture_pop_up.grab_set()  # Не позволяет работать с другим окном, пока это окно не закрыто

    load_picture_window = Frame(load_picture_pop_up)
    load_picture_window.grid(row=0, column=0, padx=20, pady=20)

    def askopenfile():
        # global path_open_picture_file
        path_open_picture_file = filedialog.askopenfilename()
        # path_open_picture_file = path_open_picture_file.encode("utf-8")
        print("path_open_picture_file: ", path_open_picture_file)
        print("""path_open_picture_file.encode("utf-8"): """, path_open_picture_file.encode("utf-8"))

        print(type(path_open_picture_file))
        print(type(path_open_picture_file.encode("utf-8")))
        l = len(path_open_picture_file)
        print("l: ", l)
        extension = path_open_picture_file[l-3:l+1].lower()
        print("extension: ", extension)

        if extension == "pdf":
            images = pdf2image.convert_from_bytes(open(path_open_picture_file, 'rb').read())
            images[0].save(path_folder + "\\" + "UV_lack_calc_image.jpg", 'JPEG')
            image = cv2.imread(path_folder + "\\" + "UV_lack_calc_image.jpg", cv2.IMREAD_GRAYSCALE)  # Загружаем изображения как grayscale

        elif extension == "jpg":
            image = cv2.imread(path_open_picture_file, cv2.IMREAD_GRAYSCALE)  # Загружаем изображения как grayscale
            print(image)
        width = 500  # Задаём ширину изображения в пикселях.
        height = int(image.shape[0] * float(width) / image.shape[1])  # Пропорционально пересчитанная высота изображения
        dim = (width, height)
        median = 100  # Граничное среднее значение цвета для перовода изображения цветовую систему black and white
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)  # Пересчитываем изображение в нужные нам размеры
        ret, resized_b_and_w = cv2.threshold(resized, median, 255,
                                             cv2.THRESH_BINARY)  # Пересчитываем изображение в black and white
        window_gray = u"Image converted to grayscale"
        window_black = u"Image converted to black-and-white"
        cv2.namedWindow(window_gray)
        cv2.namedWindow(window_black)
        cv2.moveWindow(window_gray, 120, 150)
        cv2.moveWindow(window_black, 625, 150)
        cv2.imshow(window_gray, resized)  # Выводим на монитор исходное grayscale изображение
        cv2.imshow(window_black, resized_b_and_w)  # Выводим на монитор получившееся black and white изображение
        non_zero_pixels = cv2.countNonZero(resized_b_and_w)  # Подсчитываем количество белых пикселей
        black_pixels_percent = round(100 - (non_zero_pixels * 100 / (width * height)))
        print("Процент заполнения листа печатными элементами:", black_pixels_percent, "%")
        answer = str(" Процент заполнения листа печатными элементами: " + str(black_pixels_percent) + "%")
        load_picture_text_result_var = StringVar()
        load_picture_text_result_var.set(answer)
        load_picture_text_result = Label(load_picture_window, textvariable=load_picture_text_result_var)
        load_picture_text_result.grid(row=0, column=1)

        cv2.waitKey(0)


    load_picture_button_open_file = Button(load_picture_window, text="Открыть файл", command=askopenfile)
    load_picture_button_open_file.grid(row=0, column=0)








# Функция формирует окно, в котором можно увидеть путь к файлам профилей, увидеть список всех профилей, дату
# последнего редактирования каждого профиля, статус (доступность) файла с настройками для каждого профиля ии удалить
# ненужные профили.
def manage_profiles():
    manage_profiles_pop_up = Toplevel(root)
    manage_profiles_pop_up.title("Управление профилями")
    manage_profiles_pop_up.geometry("1200x680+100+35")
    manage_profiles_pop_up.grab_set()  # Не позволяет работать с другим окном, пока это окно не закрыто

    manage_profiles_window = Frame(manage_profiles_pop_up)
    manage_profiles_window.grid(row=0, column=0, padx=20, pady=20)

    # Вложенная функция удаляет профиль выбранный из списка профилей и удаляет с диска файл этого профиля
    def delete_profile(*args):  # аргументом функции является название удаляемого профайла
        if manage_type_profile.get() != "Основной":
            path_temp = path_folder + "\\" + dic_name_file_profile[manage_type_profile.get()]
            dic_name_file_profile.pop(manage_type_profile.get())
            save_list_profiles()
            if os.path.isfile(path_temp):
                os.remove(path_temp)
            manage_profiles_pop_up.destroy()
            manage_profiles()

    manage_text_path_name = Label(manage_profiles_window, text="Путь, по которому раcположены конфигурационные файлы:")
    manage_text_path = Label(manage_profiles_window, text=path_folder)
    manage_text_title_name = Label(manage_profiles_window, text="Название профиля", font="TkDefaultFont 8 bold")
    manage_text_title_status = Label(manage_profiles_window, text="Состояние файла профиля", font="TkDefaultFont 8 bold")
    manage_text_title_date = Label(manage_profiles_window, text="Дата изменения профиля", font="TkDefaultFont 8 bold")
    manage_text_path_name.grid(row=0, column=0, columnspan=2)
    manage_text_path.grid(row=0, column=2)
    manage_text_title_name.grid(row=1, column=0)
    manage_text_title_status.grid(row=1, column=1)
    manage_text_title_date.grid(row=1, column=2)

    j = 1
    for i in dic_name_file_profile:
        path_temp = path_folder + "\\" + dic_name_file_profile[i]
        manage_text_file = Label(manage_profiles_window, text=i)
        manage_text_file.grid(row=j + 1, column=0)
        if os.path.isfile(path_temp):
            manage_text_date = Label(manage_profiles_window, text=time.strftime('%d-%m-%Y  %H:%M', time.localtime(os.path.getmtime(path_temp))))
            manage_text_date.grid(row=j + 1, column=2)
            manage_text_status = Label(manage_profiles_window, text="Ок")
        else:
            manage_text_status = Label(manage_profiles_window, text="Файл не найден")
        manage_text_status.grid(row=j + 1, column=1)
        j += 1
    manage_type_profile = StringVar()
    manage_type_profile.set("Выберите профиль для удаления")
    # manage_type_profile.set(selected_profile)
    manage_button_type_profile = OptionMenu(manage_profiles_window, manage_type_profile, *dic_name_file_profile, command=delete_profile)
    manage_button_type_profile.grid(row=j+1, column=0)


#  Функция для сохранения в файле *.json данных о всех расценках. Если программа открылась, не нашла файл *.json
#  с расценками и загрузились расценки по умолчанию, прописанные в словарях в теле программы, спросить пользователя
#  хочет ли он, что бы текущие расценки сохранялись и в дальнейшем они использовались для расчетов.
def save_data():
    global succcessful_load
    if succcessful_load == False:
        decide = messagebox.askyesno(message="""Обратите внимание. При открытии программы не
    загрузились расценки. Программа использует расценки\nпо умолчанию. После сохранения программа будет
    использовать эти расценки. Все прошлые данные будут\nпотеряны. Убедитесь, что Вы сохраняете актуальные\nрасценки."""
                                     , title="Сохранение расценок")
        # Пользователь отказался записывать текущие расценки в файл *.json. Продолжаем работать с текущими расценками
        # до момента закрытия текущей программы
        if decide == False:
            return
    succcessful_load = True
    # Переписываем все расценки из полей ввода в соответствующие словари
    dic_all_prices["electricity"][0] = price_entry_electricity.get()
    dic_all_prices["electricity"][1] = price_entry_electricity.get()
    dic_all_prices["drum"][0] = price_entry_drum_less_b3.get()
    dic_all_prices["drum"][1] = price_entry_drum_more_b3.get()
    dic_all_prices["film"][0] = price_entry_film_less_b3.get()
    dic_all_prices["film"][1] = price_entry_film_more_b3.get()
    dic_all_prices["dryer"][0] = price_entry_dryer_less_b3.get()
    dic_all_prices["dryer"][1] = price_entry_dryer_more_b3.get()
    dic_all_prices["salary"][0] = price_entry_salary_less_b3.get()
    dic_all_prices["salary"][1] = price_entry_salary_more_b3.get()
    dic_all_prices["printing"][0] = price_entry_printing_less_b3.get()
    dic_all_prices["printing"][1] = price_entry_printing_more_b3.get()
    dic_all_prices["speed"][0] = price_entry_speed_less_b3.get()
    dic_all_prices["speed"][1] = price_entry_speed_more_b3.get()
    dic_all_prices["adjustment_cost"][0] = price_entry_adjustment_cost_less_b3.get()
    dic_all_prices["adjustment_cost"][1] = price_entry_adjustment_cost_more_b3.get()
    dic_all_prices["adjustment_time"][0] = price_entry_adjustment_time_less_b3.get()
    dic_all_prices["adjustment_time"][1] = price_entry_adjustment_time_more_b3.get()
    dic_type_lack["УФ-лак"][0] = price_entry_UV_lack_1_cost.get()
    dic_type_lack["УФ-лак"][1] = price_entry_UV_lack_1_outgo.get()
    dic_type_lack["УФ-лак с поднятием"][0] = price_entry_UV_lack_2_cost.get()
    dic_type_lack["УФ-лак с поднятием"][1] = price_entry_UV_lack_2_outgo.get()
    dic_type_lack["Глиттер + УФ-лак (1:5)"][0] = price_entry_UV_lack_3_cost.get()
    dic_type_lack["Глиттер + УФ-лак (1:5)"][1] = price_entry_UV_lack_3_outgo.get()
    dic_type_lack["Глиттер + УФ-лак с поднятием (1:5)"][0] = price_entry_UV_lack_4_cost.get()
    dic_type_lack["Глиттер + УФ-лак с поднятием (1:5)"][1] = price_entry_UV_lack_4_outgo.get()
    dic_type_client["премиум"] = price_entry_client_premium.get()
    dic_type_client["хорошо"] = price_entry_client_well.get()
    dic_type_client["стандарт"] = price_entry_client_standart.get()

    with open(path_data, "w", encoding="utf-8") as write_data:
        dic_s = {}
        dic_s.update(dic_all_prices)
        dic_s.update(dic_type_lack)
        dic_s.update(dic_type_client)
        json.dump(dic_s, write_data, ensure_ascii=False)
    prices_pop_up.destroy()  # Закрываем окно после сохранения данных в файл.


# Функция для сохранения списка доступных профилей в файл.
def save_list_profiles():
    with open(path_profile, "w", encoding="utf-8") as write_data:
        dic_list = {}
        dic_list.update(dic_name_file_profile)
        json.dump(dic_list, write_data, ensure_ascii=False)


# Функция для обновления всех расценок данными из файла *.json
def load_data():
    if succcessful_load == True:
        global path_data
        with open(path_data, "r", encoding="utf-8") as load_all_data:
            dic_l = json.load(load_all_data)
            for i in dic_l:
                if i in dic_all_prices:
                    dic_all_prices[i] = dic_l[i]
                elif i in dic_type_lack:
                    dic_type_lack[i] = dic_l[i]
                elif i in dic_type_client:
                    dic_type_client[i] = dic_l[i]


# Функция для обновления списка профилей
def load_profile():
    global dic_name_file_profile
    if succcessful_load == True:
        with open(path_profile, "r", encoding="utf-8") as load_profile_list:
            dic_name_file_profile = json.load(load_profile_list)


# Словарь со всеми постоянными составляющими стоимости лакировки.
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

# Словарь для перечисления назвний всех сохраненных профилей и названий соответствующих файлов
dic_name_file_profile = {"Основной": "UV_lack_calc_data.json"}

root = Tk()
root.geometry("1200x680+100+35")
root.iconbitmap(r"D:\Python\UV_calc\TimPack.ico")
root.title("Расчёт стоимости УФ-лакировки")
root.option_add('*tearOff', FALSE)  # Делаем раскрывающиеся меню "неотрывными" от основного окна

# Формирование пути к файлу *.json с расценкам. При включении программы по умолчанию загружаем профиль "Основной".
selected_profile = "Основной"
path_folder = r"D:\Python\UV_calc"  # Путь к папке, в которой храняться все файлы *.json с настройками
path_data = path_folder + "\\" + dic_name_file_profile[selected_profile]  # Путь к файлу *.json с расценками
path_profile = path_folder + "\\" + "UV_lack_calc_list_profiles.json"  # Путь к файлу *.json с перечнем профилей


# При старте программы загружаем и меняем заданные в словарях в коде программы расценки, на расценки из *.json
try:  # Проверяем, удалось ли нам загрузить расценки из фала *.json
    succcessful_load = True  # Переменная показывает, что файл загрузился, расценки обновлены.
    load_data()
except:  # Загрузка данных не удалась.
    succcessful_load = False  # Переменная показывает, что файл не загрузился, расценки не обновлены.
    decide = messagebox.askyesno(message="""При открытии программы не удалось загрузить расценки.
Будут использоваться расценки по умолчанию. Сохранить\nрасценки по умолчанию для дальнейшего использования,
или Вы попробуете найти файл с настройками и вернуться\nк ним при следующей загрузке""", title="Проблемы с загрузкой данных.")
    if decide == True:  # Пользователь согласился перезаписать и использовать расценки по умолчанию.
        succcessful_load = True
        show_prices()
        save_data()  # Создаём новый файл *.json, в котором будут расценки по умолчанию.
        prices_pop_up.destroy()

# При старте программы загружаем и меняем заданные по умолчанию в словаре названия профилей.
try:
    load_profile()
except:
    if succcessful_load == True:
        save_list_profiles()

# Создание меню
menubar = Menu(root)
root["menu"] = menubar
menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menubar.add_cascade(menu=menu_edit, label='Меню')
menu_edit.add_command(label='Расценки', command=show_prices)
menu_edit.add_command(label='Управлениями профилями', command=manage_profiles)
menu_edit.add_command(label='Определение % заполнения', command=load_picture_calculate_filling)


# Фрейм для размещения виджетов отчета расчета калькуляции
report_frame = Frame(root, width=400, height=240)
report_frame.place(x=70, y=190)

# Фрейм для размещения виджетов детальной калькуляции
details_frame = Frame(root, width=400, height=1)
details_frame.place(x=70, y=430)

# Раскрывающийся список для выбора типа лакировки
type_lack = StringVar()
type_lack.set("УФ-лак")
button_type_lack = OptionMenu(root, type_lack, *dic_type_lack)
button_type_lack.config(width=32)
button_type_lack.place(x=30, y=10)

# Раскрывающийся спсисок для выбора типа клиента
type_client = StringVar()
type_client.set("премиум")
button_type_client = OptionMenu(root, type_client, *dic_type_client)  # Кнопка для выбора типа клиента
button_type_client.config(width=8)
button_type_client.place(x=174, y=42)

# Поле флажок, для выбора, считать ли в заказе пленку, или она повторная/заказчика
film_reused = StringVar()
film_reused.set("новая")
checkbutton_film_reused = Checkbutton(root, variable=film_reused, onvalue="новая",
                                      offvalue="повторная или заказчика")
checkbutton_film_reused.place(x=412, y=108)

# Виджет разделяющая линия
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

type_profile_name = Label(root, text="Тип профиля:", justify=LEFT)
type_profile_var = StringVar()
type_profile_var.set(selected_profile)
type_profile = Label(root, textvariable=type_profile_var, font="TkDefaultFont 11 bold italic")
type_profile_name.place(x=80, y=175)
type_profile.place(x=420, y=197, anchor="se")

report_type_client_name = Label(report_frame, text="Тип клиента:", justify=LEFT)
report_type_client_var = StringVar()
report_type_client = Label(report_frame, textvariable=report_type_client_var, font="TkDefaultFont 11 bold italic")
report_type_lack_name = Label(report_frame, text="Тип лака:")
report_type_lack_var = StringVar()
report_type_lack = Label(report_frame, textvariable=report_type_lack_var, font="TkDefaultFont 11 bold italic")
report_film_name = Label(report_frame, text="Плёнка:")
report_film_var = StringVar()
report_film = Label(report_frame, textvariable=report_film_var, font="TkDefaultFont 11 bold italic")
report_amount_name = Label(report_frame, text="Тираж:")
report_amount_var = StringVar()
report_amount = Label(report_frame, textvariable=report_amount_var, font="TkDefaultFont 11 bold italic")
report_amount_measure = Label(report_frame, text="лист.")
report_width_name = Label(report_frame, text="Ширина листа:")
report_width_var = StringVar()
report_width = Label(report_frame, textvariable=report_width_var, font="TkDefaultFont 11 bold italic")
report_width_measure = Label(report_frame, text="мм.")
report_length_name = Label(report_frame, text="Длина листа:")
report_length_var = StringVar()
report_length = Label(report_frame, textvariable=report_length_var, font="TkDefaultFont 11 bold italic")
report_length_measure = Label(report_frame, text="мм.")
report_percents_name = Label(report_frame, text="Процент заполнения листа:")
report_percents_var = StringVar()
report_percents = Label(report_frame, textvariable=report_percents_var, font="TkDefaultFont 11 bold italic")
report_percents_measure = Label(report_frame, text="%")
report_cost_all_amount_name = Label(report_frame, text="Стоимость лакировки тиража:")
report_cost_all_amount_var = StringVar()
report_cost_all_amount = Label(report_frame, textvariable=report_cost_all_amount_var, font="TkDefaultFont 11 bold italic", fg="red")
report_cost_all_amount_measure = Label(report_frame, text="грн.")
report_cost_one_sheet_name = Label(report_frame, text="Стоимость лакировки одного листа:")
report_cost_one_sheet_var = StringVar()
report_cost_one_sheet = Label(report_frame, textvariable=report_cost_one_sheet_var, font="TkDefaultFont 11 bold italic", fg="red")
report_cost_one_sheet_measure = Label(report_frame, text="грн.")

# Размещение виджетов описания отчетов расчета калькуляции в координатах "report_frame"
report_type_client_name.place(x=10, y=10)
report_type_client.place(x=350, y=32, anchor="se")
report_type_lack_name.place(x=10, y=35)
report_type_lack.place(x=350, y=57, anchor="se")
report_film_name.place(x=10, y=60)
report_film.place(x=350, y=82, anchor="se")
report_amount_name.place(x=10, y=85)
report_amount.place(x=350, y=107, anchor="se")
report_amount_measure.place(x=355, y=85)
report_width_name.place(x=10, y=110)
report_width.place(x=350, y=132, anchor="se")
report_width_measure.place(x=355, y=110)
report_length_name.place(x=10, y=135)
report_length.place(x=350, y=157, anchor="se")
report_length_measure.place(x=355, y=135)
report_percents_name.place(x=10, y=160)
report_percents.place(x=350, y=182, anchor="se")
report_percents_measure.place(x=355, y=160)
report_cost_all_amount_name.place(x=10, y=185)
report_cost_all_amount.place(x=350, y=207, anchor="se")
report_cost_all_amount_measure.place(x=355, y=185)
report_cost_one_sheet_name.place(x=10, y=210)
report_cost_one_sheet.place(x=350, y=232, anchor="se")
report_cost_one_sheet_measure.place(x=355, y=210)

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
canvas_graph.place(x=560, y=20)
canvas_graph_2 = Canvas(root, width=637, height=250)
canvas_graph_2.place(x=560, y=300)

root.bind("<Return>", check_filling)  # Выполнить расчет по нажатию клавиши Enter/Return
entry_amount.focus()  # Устанавливаем курсор в поле ввода тиража
root.mainloop()
