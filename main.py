#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data analysis project v 3.1
"""
import tkinter as tki
import tkinter.ttk as ttk
from tkinter import filedialog as fld
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import configparser


def read_from_text_file(file_name):
    """
    Функция читает базу данных из файла формата .csv или .xlsx
    Входные данные: имя файла (строка)
    Выходные данные: датафрейм с базой данных (pd.DataFrame())
    Автор:
    """
    if '.csv' in file_name:  # если файл .csv
        data_local = pd.read_csv(file_name)  # чтение из .csv
    else:  # если файл .xlsx или .xls
        data_local = pd.read_excel(file_name)  # чтение из .xlsx или .xls
    return data_local  # создание и возврат датафрейма


def read_from_bin_file(file_name):
    """
    Функция читает базу данных из двоичного файла
    Входные данные: имя файла
    Выходные данные: базa данных (массив, кортеж, словарь и т. д.)
    Автор:
    """
    data_local = np.load(file_name)  # загрузка базы данных из двоичного файла
    return data_local  # возвращение базы данных


def save_to_excel(data_local):
    """
    Функция сохраняет базу данных в файл .xlsx
    Входные данные: датафрейм с базой данных (pd.DataFrame())
    Выходные данные: нет
    Автор:
    """
    ftypes = [('Excel файлы', '*.xlsx')]
    dlg = fld.SaveAs(filetypes=ftypes)
    path = dlg.show() + '.xlsx'
    data_local.to_excel(path, index=False)  # сохранение базы данных в формате .xlsx


def save_to_excel_index(data_local):
    """
    Функция сохраняет базу данных в файл .xlsx, оставляя индекс
    Входные данные: датафрейм с базой данных (pd.DataFrame())
    Выходные данные: нет
    Автор:
    """
    ftypes = [('Excel файлы', '*.xlsx')]
    dlg = fld.SaveAs(filetypes=ftypes)
    path = dlg.show() + '.xlsx'
    data_local.to_excel(path)  # сохранение базы данных в формате .xlsx без индекса


def save_to_csv(file_name, data_local):
    """
    Функция сохраняет базу данных в файл .csv
    Входные данные: имя файла (строка), датафрейм с базой данных (pd.DataFrame())
    Выходные данные: нет
    Автор:
    """
    np.savetxt(file_name, data_local, fmt='%s', delimiter=';')  # сохранение базы данных в формате .csv


def save_to_bin_file(data_local, file_name):
    """
    Функция сохраняет базу данных в бинарный файл
    Входные данные: датафрейм с базой данных (pd.DataFrame()), имя файла (строка)
    Выходные данные: нет
    Автор:
    """
    np.save(file_name, data_local)  # сохранение базы данных в бинарном файле


def save_graphics(file_name):
    """
    Функция сохраняет построенный график в файл .png
    Входные данные: имя файла (строка)
    Выходные данные: нет
    Автор:
    """
    plt.savefig(file_name)  # сохранение графика в формате .png


def isNumeric(s):
    """
    Функция для проверки было ли введено число
    Входные данные: строка, которую нужно проверить(str)
    Выходные данные: True или False
    Автор:
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def plug(i):
    """
    Функция-"заглушка", чтобы при нажатии на строки treeview не срабатывали
    другие функции
    Входные данные: нет
    Выходные данные: нет
    Автор:
    """
    return i


def adding_entities(tree):
    """
    Функция добавляет строку со значениями, введёнными пользователем, в базу данных
    и таблицу treeview
    Входные данные: таблица (ttk.Treeview)
    Выходные данные: нет
    Автор:
    """

    def add_click():
        """
        Функция срабатывает при нажатии на кнопку подтверждения выбора значений
        для новой строки. Добавляет в базу данных новую строку с этими значениями,
        добавляет эту строку в Treeview
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """
        entities = []
        flag = 0
        for i in range(len(columns)):
            if columns[i] in string_columns:
                entities.append(combobox[i].get())
            elif columns[i] in int_columns:
                if isNumeric(spinbox[i].get()):
                    entities.append(np.int64(spinbox[i].get()))
                else:
                    flag = 1
            else:
                if isNumeric(spinbox[i].get()):
                    entities.append(np.float64(spinbox[i].get()))
                else:
                    flag = 1
        add_window.grab_release()
        add_window.destroy()
        if flag == 0:
            data.loc[len(data.index)] = entities
            tree.insert("", tki.END, values=entities, iid=len(data))
        else:
            tki.messagebox.showerror(title="Ошибка",
                                     message="Была введена качественная переменная для количественного столбца")

    config = configparser.ConfigParser()  # создание экземпляра ConfigParser
    config.read(
        'Analysing_demographic_data_of_customers_with_credit_history/config.ini')  # чтение конфигурационного файла
    add_window = tki.Toplevel()
    add_window.title("Добавление строки")
    add_window.geometry("350x525")
    add_window.resizable(False, False)
    combobox = 21 * [0]
    spinbox = 21 * [0]
    for i in range(len(columns)):
        add_label = tki.Label(add_window, text=columns[i],
                              font=(config['Adding_menu']['font'], int(config['Adding_menu']['font_size'])),
                              foreground=config['Adding_menu']['foreground'])
        add_label.grid(row=i, column=0)
    for i in range(len(columns)):
        if columns[i] in string_columns:
            characteristics = []
            pd_characteristics = pd.unique(data[columns[i]])
            for j in range(len(pd_characteristics)):
                characteristics.append(pd_characteristics[j])
            combobox[i] = ttk.Combobox(add_window, values=characteristics)
            combobox[i].current(0)
            combobox[i].grid(row=i, column=1)
        if columns[i] in int_columns or columns[i] in float_columns:
            characteristics = pd.unique(data[columns[i]])
            spinbox[i] = tki.Spinbox(add_window, from_=min(characteristics),
                                     to=max(characteristics))
            spinbox[i].grid(row=i, column=1)
    add_button = ttk.Button(add_window, text="Добавить", command=add_click)
    add_button.grid(row=21, column=1, sticky="we")


def deleting_entities(tree):
    """
    Функция удаляет выбранную пользователем строку из базы данных и из таблицы 
    Treeview
    Входные данные: таблица(ttk.Treeview)
    Выходные данные: нет
    Автор:
    """

    def del_select(event):
        """
        Функция срабатывает при нажатии на строку Treeview. Вызывает окно 
        подтверждения удаления выбранной строки
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """
        if not tree.selection():
            return
        check_window = tki.Toplevel()
        check_window.title("Подтверждение")
        check_window.geometry('200x100')
        check_window.resizable(False, False)
        label = ttk.Label(check_window, text="Удалить выделенную строку?",
                          font=(config['Deleting_menu']['font'], int(config['Deleting_menu']['font_size'])),
                          foreground=config['Deleting_menu']['foreground'])
        label.pack(anchor="c")
        button_yes = ttk.Button(check_window, text="Да", command=lambda: click_yes(check_window))
        button_yes.pack(side="left", padx=5)
        button_no = ttk.Button(check_window, text="Нет", command=lambda: click_no(check_window))
        button_no.pack(side="right", padx=5)

    def click_yes(check_window):
        """
        Функция срабатывает при нажатии на кнопку подтверждения удаления. 
        Удаляет выбранную пользователем строку из базы данных и из таблицы 
        Treeview
        Входные данные: окно подтверждения(tki.Toplevel)
        Выходные данные: нет
        Автор:
        """
        drop_index = int(tree.selection()[0])
        check_window.grab_release()
        check_window.destroy()
        global data
        data.drop(index=drop_index, inplace=True)
        data = data.reset_index(drop=True)
        tree.delete(*tree.get_children())
        for i in range(len(data)):
            values = []
            for j in range(len(columns)):
                values.append(data.iloc[i, j])
            tree.insert("", tki.END, values=values, iid=i)
        tree.bind('<<TreeviewSelect>>', plug)

    def click_no(check_window):
        """
        Функция срабатывает при нажатии на кнопку отмены удаления. Закрывает 
        окно подтверждения
        Входные данные: окно подтверждения(tki.Toplevel)
        Выходные данные: нет
        Автор:
        """
        check_window.grab_release()
        check_window.destroy()
        tree.bind('<<TreeviewSelect>>', plug)

    config = configparser.ConfigParser()  # создание экземпляра ConfigParser
    config.read(
        'Analysing_demographic_data_of_customers_with_credit_history/config.ini')  # чтение конфигурационного файла
    tki.messagebox.showinfo(title="Информация", message="Выберите строку для удаления")
    tree.bind('<<TreeviewSelect>>', del_select)


def manual_modification(tree):
    """
    Функция осуществляет модификацию выбранной ячейки в базе данных и таблице
    Treeview
    Входные данные: таблица(ttk.Treeview)
    Выходные данные: нет
    Автор:
    """

    def edit_select(event):
        """
        Функция срабатывает при нажатии на строку Treeview. Вызывает окно 
        редактирования выбранной строки
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """
        if not tree.selection():
            return
        row_num = int(tree.selection()[0])
        edit_window = tki.Toplevel()
        edit_window.title("Редактирование")
        edit_window.geometry('350x100')
        edit_window.resizable(False, False)
        edit_combobox = ttk.Combobox(edit_window, values=columns)
        edit_combobox.current(0)
        edit_combobox.grid(column=0, row=0, padx=10, pady=10)
        edit_button1 = ttk.Button(edit_window, text="Выбрать столбец", command=lambda: edit_click1(edit_combobox.get(),
                                                                                                   edit_window,
                                                                                                   row_num))
        edit_button1.grid(column=0, row=1, padx=10, sticky="we")

    def edit_click1(edit_column, edit_window, row_num):
        """
        Функция срабатывает при нажатии на кнопку подтверждения выбора столбца,
        в котором нужно отредактировать ячейку. Вызывает поле для ввода нового
        значения ячейки
        Входные данные: выбранный столбец(str), окно редактирования(tki.Toplevel),
        номер строки, в которой происходит редактирование(int)
        Выходные данные: нет
        Автор:
        """
        if edit_column in string_columns:
            characteristics = []
            pd_characteristics = pd.unique(data[edit_column])
            for i in range(len(pd_characteristics)):
                characteristics.append(pd_characteristics[i])
            value = ttk.Combobox(edit_window, values=characteristics)
            value.current(0)
            value.grid(column=1, row=0, padx=10, pady=10)
        else:
            characteristics = pd.unique(data[edit_column])
            value = tki.Spinbox(edit_window, from_=min(characteristics),
                                to=max(characteristics))
            value.grid(column=1, row=0, padx=10, pady=10)
        edit_button2 = ttk.Button(edit_window, text="Редактировать", command=lambda: edit_click2(value.get(),
                                                                                                 edit_column, row_num,
                                                                                                 edit_window))
        edit_button2.grid(column=1, row=1, padx=10, sticky="we")

    def edit_click2(value, edit_column, row_num, edit_window):
        """
        Функция срабатывает при нажатии на кнопку подтверждения редактирования 
        после введения нового значения ячейки. Осуществляет модификацию 
        выбранной ячейки в базе данных и таблице Treeview
        Входные данные: новое значение ячейки(str), выбранный столбец(str),
        номер строки, в которой происходит редактирование(int),окно 
        редактирования(tki.Toplevel)
        Выходные данные: нет
        Автор:
        """
        flag = 0
        if edit_column in string_columns:
            new_value = value
        elif edit_column in int_columns:
            if isNumeric(value):
                new_value = np.int64(value)
            else:
                flag = 1
                tki.messagebox.showerror(title="Ошибка",
                                         message="Была введена качественная переменная для количественного столбца")
        else:
            if isNumeric(value):
                new_value = np.float64(value)
            else:
                flag = 1
                tki.messagebox.showerror(title="Ошибка",
                                         message="Была введена качественная переменная для количественного столбца")
        edit_window.grab_release()
        edit_window.destroy()
        tree.bind('<<TreeviewSelect>>', plug)
        if flag == 0:
            pd.options.mode.chained_assignment = None
            data[edit_column][row_num] = new_value
            tree.delete(*tree.get_children())
            for i in range(len(data)):
                values = []
                for j in range(len(columns)):
                    values.append(data.iloc[i, j])
                tree.insert("", tki.END, values=values, iid=i)

    config = configparser.ConfigParser()  # создание экземпляра ConfigParser
    config.read(
        'Analysing_demographic_data_of_customers_with_credit_history/config.ini')  # чтение конфигурационного файла
    tki.messagebox.showinfo(title="Информация", message="Выберите строку для редактирования")
    tree.bind('<<TreeviewSelect>>', edit_select)


def data_filter():
    """
    Фильтрация базы данных по выбранным условиям, сохранение отфильтрованной базы данных
    Входные данные: нет
    Выходные данные: нет
    Автор:
    """

    def checkbutton_changed(i):
        """
        Функция добавляет поле для выбора условия фильтрации
        Входные данные: номер столбца (int)
        Выходные данные: нет
        Автор:
        """
        if checkbutton_var[i].get() == 1:
            label3 = ttk.Label(window, text="Введите значения, по которым",
                               font=(config['Filter_menu']['font'], int(config['Filter_menu']['font_size'])),
                               foreground=config['Filter_menu']['foreground'])
            label3.grid(row=0, column=1)
            label4 = ttk.Label(window, text="нужно отсортировать данные",
                               font=(config['Filter_menu']['font'], int(config['Filter_menu']['font_size'])),
                               foreground=config['Filter_menu']['foreground'])
            label4.grid(row=1, column=1)
            if columns[i] in string_columns:
                characteristics = []
                pd_characteristics = pd.unique(data[columns[i]])
                for j in range(len(pd_characteristics)):
                    characteristics.append(pd_characteristics[j])
                combobox[i] = ttk.Combobox(window, values=characteristics)
                combobox[i].current(0)
                combobox[i].grid(row=i + 2, column=1)
            if columns[i] in int_columns or columns[i] in float_columns:
                characteristics = pd.unique(data[columns[i]])
                spinbox[i] = tki.Spinbox(window, from_=min(characteristics),
                                         to=max(characteristics))
                spinbox[i].grid(row=i + 2, column=1)

    def click1():
        """
        Функция проверяет, заданы ли условия для фильтрации. Если да, то 
        выводит список столбцов для выбора тех, которые останутся в
        отфильтрованной базе данных
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """
        flag1 = 0
        flag2 = 0
        SEL = True
        for i in range(len(checkbutton)):
            if checkbutton_var[i].get() == 1:
                flag1 = 1
                if columns[i] in string_columns:
                    condition = combobox[i].get()
                elif columns[i] in int_columns:
                    if isNumeric(spinbox[i].get()):
                        condition = np.int64(spinbox[i].get())
                    else:
                        flag2 = 1
                else:
                    if isNumeric(spinbox[i].get()):
                        condition = np.float64(spinbox[i].get())
                    else:
                        flag2 = 1
                if flag2 == 0:
                    SEL = SEL & (data[columns[i]] == condition)
        if flag1 == 0:
            tki.messagebox.showwarning(title="Предупреждение",
                                       message="Не выбраны значения")
        elif flag2 == 0:
            label1 = ttk.Label(window, text="Выберите столбцы,",
                               font=(config['Filter_menu']['font'], int(config['Filter_menu']['font_size'])),
                               foreground=config['Filter_menu']['foreground'])
            label1.grid(row=0, column=2)
            label2 = ttk.Label(window, text="которые нужно оставить",
                               font=(config['Filter_menu']['font'], int(config['Filter_menu']['font_size'])),
                               foreground=config['Filter_menu']['foreground'])
            label2.grid(row=1, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[0], variable=checkbutton_var1[0]))
            checkbutton1[0].grid(row=2, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[1], variable=checkbutton_var1[1]))
            checkbutton1[1].grid(row=3, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[2], variable=checkbutton_var1[2]))
            checkbutton1[2].grid(row=4, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[3], variable=checkbutton_var1[3]))
            checkbutton1[3].grid(row=5, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[4], variable=checkbutton_var1[4]))
            checkbutton1[4].grid(row=6, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[5], variable=checkbutton_var1[5]))
            checkbutton1[5].grid(row=7, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[6], variable=checkbutton_var1[6]))
            checkbutton1[6].grid(row=8, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[7], variable=checkbutton_var1[7]))
            checkbutton1[7].grid(row=9, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[8], variable=checkbutton_var1[8]))
            checkbutton1[8].grid(row=10, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[9], variable=checkbutton_var1[9]))
            checkbutton1[9].grid(row=11, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[10], variable=checkbutton_var1[10]))
            checkbutton1[10].grid(row=12, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[11], variable=checkbutton_var1[11]))
            checkbutton1[11].grid(row=13, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[12], variable=checkbutton_var1[12]))
            checkbutton1[12].grid(row=14, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[13], variable=checkbutton_var1[13]))
            checkbutton1[13].grid(row=15, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[14], variable=checkbutton_var1[14]))
            checkbutton1[14].grid(row=16, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[15], variable=checkbutton_var1[15]))
            checkbutton1[15].grid(row=17, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[16], variable=checkbutton_var1[16]))
            checkbutton1[16].grid(row=18, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[17], variable=checkbutton_var1[17]))
            checkbutton1[17].grid(row=19, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[18], variable=checkbutton_var1[18]))
            checkbutton1[18].grid(row=20, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[19], variable=checkbutton_var1[19]))
            checkbutton1[19].grid(row=21, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[20], variable=checkbutton_var1[20]))
            checkbutton1[20].grid(row=22, column=2)
            btn2 = ttk.Button(window, text="Отфильтровать", command=lambda: click2(SEL))
            btn2.grid(row=23, column=1)
        elif flag2 == 1:
            tki.messagebox.showerror(title="Ошибка",
                                     message="Была введена качественная переменная для количественного столбца")

    def click2(SEL):
        """
        Функция проверяет, заданы ли условия для фильтрации. Если да, то 
        выводит список столбцов для выбора тех, которые останутся в
        отфильтрованной базе данных
        Входные данные: условие фильтрации(pd.Series())
        Выходные данные: нет
        Автор:
        """
        flag = 0
        report_columns = []
        for i in range(len(checkbutton1)):
            if checkbutton_var1[i].get() == 1:
                flag = 1
                report_columns.append(columns[i])
        if flag == 1:
            data_filter = data.loc[SEL, report_columns]
            if data_filter.empty:
                tki.messagebox.showinfo(title="Информация",
                                        message="Выбранным параметрам не соответствует ни одна строка")
                window.grab_release()
                window.destroy()
            else:
                window.grab_release()
                window.destroy()
                window1 = tki.Toplevel()
                window1.title("Отфильтрованная база данных")
                window1.geometry('600x250')
                menu1 = tki.Menu(window1)
                menu1.add_command(label="Сохранить", command=lambda: save_to_excel(data_filter))
                window1.config(menu=menu1)
                tree1 = ttk.Treeview(window1, columns=report_columns, show="headings")
                for i in range(len(report_columns)):
                    tree1.heading(report_columns[i], text=report_columns[i])
                for i in range(len(data_filter)):
                    values = []
                    for j in range(len(report_columns)):
                        values.append(data_filter.iloc[i, j])
                    tree1.insert("", tki.END, values=values)
                scrollbar11 = ttk.Scrollbar(window1, orient="horizontal", command=tree1.xview)
                scrollbar11.pack(fill="x", side="bottom")
                tree1["xscrollcommand"] = scrollbar11.set
                scrollbar21 = ttk.Scrollbar(window1, orient="vertical", command=tree1.yview, )
                scrollbar21.pack(side="right", fill="y")
                tree1["yscrollcommand"] = scrollbar21.set
                tree1.pack(fill="both", expand=1)
        else:
            tki.messagebox.showwarning(title="Предупреждение", message="Не выбраны значения")

    config = configparser.ConfigParser()  # создание экземпляра ConfigParser
    config.read(
        'Analysing_demographic_data_of_customers_with_credit_history/config.ini')  # чтение конфигурационного файла
    window = tki.Toplevel()
    window.title("Фильтр")
    window.geometry("550x575")
    window.resizable(False, False)
    label1 = ttk.Label(window, text="Выберите столбцы, по которым",
                       font=(config['Filter_menu']['font'], int(config['Filter_menu']['font_size'])),
                       foreground=config['Filter_menu']['foreground'])
    label1.grid(row=0, column=0)
    label2 = ttk.Label(window, text="нужно отсортировать данные",
                       font=(config['Filter_menu']['font'], int(config['Filter_menu']['font_size'])),
                       foreground=config['Filter_menu']['foreground'])
    label2.grid(row=1, column=0)
    checkbutton_var = []
    checkbutton = []
    checkbutton_var1 = []
    checkbutton1 = []
    spinbox = 21 * [0]
    combobox = 21 * [0]
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[0], variable=checkbutton_var[0], command=lambda: checkbutton_changed(0)))
    checkbutton[0].grid(row=2, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[1], variable=checkbutton_var[1], command=lambda: checkbutton_changed(1)))
    checkbutton[1].grid(row=3, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[2], variable=checkbutton_var[2], command=lambda: checkbutton_changed(2)))
    checkbutton[2].grid(row=4, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[3], variable=checkbutton_var[3], command=lambda: checkbutton_changed(3)))
    checkbutton[3].grid(row=5, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[4], variable=checkbutton_var[4], command=lambda: checkbutton_changed(4)))
    checkbutton[4].grid(row=6, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[5], variable=checkbutton_var[5], command=lambda: checkbutton_changed(5)))
    checkbutton[5].grid(row=7, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[6], variable=checkbutton_var[6], command=lambda: checkbutton_changed(6)))
    checkbutton[6].grid(row=8, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[7], variable=checkbutton_var[7], command=lambda: checkbutton_changed(7)))
    checkbutton[7].grid(row=9, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[8], variable=checkbutton_var[8], command=lambda: checkbutton_changed(8)))
    checkbutton[8].grid(row=10, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[9], variable=checkbutton_var[9], command=lambda: checkbutton_changed(9)))
    checkbutton[9].grid(row=11, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[10], variable=checkbutton_var[10],
                                       command=lambda: checkbutton_changed(10)))
    checkbutton[10].grid(row=12, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[11], variable=checkbutton_var[11],
                                       command=lambda: checkbutton_changed(11)))
    checkbutton[11].grid(row=13, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[12], variable=checkbutton_var[12],
                                       command=lambda: checkbutton_changed(12)))
    checkbutton[12].grid(row=14, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[13], variable=checkbutton_var[13],
                                       command=lambda: checkbutton_changed(13)))
    checkbutton[13].grid(row=15, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[14], variable=checkbutton_var[14],
                                       command=lambda: checkbutton_changed(14)))
    checkbutton[14].grid(row=16, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[15], variable=checkbutton_var[15],
                                       command=lambda: checkbutton_changed(15)))
    checkbutton[15].grid(row=17, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[16], variable=checkbutton_var[16],
                                       command=lambda: checkbutton_changed(16)))
    checkbutton[16].grid(row=18, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[17], variable=checkbutton_var[17],
                                       command=lambda: checkbutton_changed(17)))
    checkbutton[17].grid(row=19, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[18], variable=checkbutton_var[18],
                                       command=lambda: checkbutton_changed(18)))
    checkbutton[18].grid(row=20, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[19], variable=checkbutton_var[19],
                                       command=lambda: checkbutton_changed(19)))
    checkbutton[19].grid(row=21, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[20], variable=checkbutton_var[20],
                                       command=lambda: checkbutton_changed(20)))
    checkbutton[20].grid(row=22, column=0)
    btn1 = ttk.Button(window, text="Закончить выбор", command=click1)
    btn1.grid(row=23, column=1)


def statistic_report():
    """
    Статистический отчёт по выбранным количественным или качественным переменным
    Входные данные: нет
    Выходные данные: нет
    Автор:
    """

    def click_1():
        """
        Вызывается при нажатии кнопки подтверждения выбора типа переменной, 
        даёт возможность пользователю выбрать столбцы для создания отчёта
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """
        button_1.config(state='disabled')
        if combobox_1.get() == "Качественная":
            label2 = ttk.Label(statistic_window, text="Выберите столбец",
                               font=(config['Statistic_menu']['font'], int(config['Statistic_menu']['font_size'])),
                               foreground=config['Statistic_menu']['foreground'])
            label2.grid(row=0, column=1)
            combobox_2 = ttk.Combobox(statistic_window, values=qualitative_variables)
            combobox_2.current(0)
            combobox_2.grid(row=1, column=1)
            button_2 = ttk.Button(statistic_window, text="Закончить выбор", command=lambda: click_2(combobox_2.get()))
            button_2.grid(row=2, column=1)
        else:
            label2 = ttk.Label(statistic_window, text="Выберите столбцы",
                               font=(config['Statistic_menu']['font'], int(config['Statistic_menu']['font_size'])),
                               foreground=config['Statistic_menu']['foreground'])
            label2.grid(row=0, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[0], variable=checkbutton_var[0]))
            checkbutton[0].grid(row=1, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[1], variable=checkbutton_var[1]))
            checkbutton[1].grid(row=2, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[2], variable=checkbutton_var[2]))
            checkbutton[2].grid(row=3, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[3], variable=checkbutton_var[3]))
            checkbutton[3].grid(row=4, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[4], variable=checkbutton_var[4]))
            checkbutton[4].grid(row=5, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[5], variable=checkbutton_var[5]))
            checkbutton[5].grid(row=6, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[6], variable=checkbutton_var[6]))
            checkbutton[6].grid(row=7, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[7], variable=checkbutton_var[7]))
            checkbutton[7].grid(row=8, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[8], variable=checkbutton_var[8]))
            checkbutton[8].grid(row=9, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[9], variable=checkbutton_var[9]))
            checkbutton[9].grid(row=10, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[10], variable=checkbutton_var[10]))
            checkbutton[10].grid(row=11, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[11], variable=checkbutton_var[11]))
            checkbutton[11].grid(row=12, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[12], variable=checkbutton_var[12]))
            checkbutton[12].grid(row=13, column=1)
            checkbutton_var.append(tki.IntVar())
            checkbutton.append(
                ttk.Checkbutton(statistic_window, text=quantitative_variables[13], variable=checkbutton_var[13]))
            checkbutton[13].grid(row=14, column=1)
            button_3 = ttk.Button(statistic_window, text="Закончить выбор", command=click_3)
            button_3.grid(row=15, column=1)

    def click_2(var):
        """
        Вызывается, если пользователь создаёт отчёт по качественной переменной.
        Формирует статистический отчёт, выводит его в отдельное окно с 
        возможностью сохранения
        Входные данные: название переменной(str)
        Выходные данные: нет
        Автор:
        """
        statistic_window.grab_release()
        statistic_window.destroy()
        statistics = pd.crosstab(index=data[var], columns='Frequency')
        parts = pd.crosstab(index=data[var], columns='Percentage')
        parts = parts / parts.sum()
        statistics = pd.concat([statistics, parts], axis=1)
        statistics_columns = statistics.columns
        statistics_rows = statistics.index.tolist()
        col = []
        col.append(var)
        for i in range(len(statistics_columns)):
            col.append(statistics_columns[i])
        statistic_window1 = tki.Toplevel()
        statistic_window1.title("Статистический отчёт")
        statistic_window1.geometry(config['Statistic_menu']['a'] + 'x' + config['Statistic_menu']['b'])
        menu1 = tki.Menu(statistic_window1)
        menu1.add_command(label="Сохранить", command=lambda: save_to_excel_index(statistics))
        statistic_window1.config(menu=menu1)
        tree1 = ttk.Treeview(statistic_window1, columns=col, show="headings")
        for i in range(len(col)):
            tree1.heading(col[i], text=col[i])
        for i in range(len(statistics)):
            values = []
            values.append(statistics_rows[i])
            for j in range(len(col) - 1):
                values.append(statistics.iloc[i, j])
            tree1.insert("", tki.END, values=values)
        tree1.pack(fill="both", expand=1)

    def click_3():
        """
        Вызывается, если пользователь создаёт отчёт по количественным переменным.
        Формирует статистический отчёт, выводит его в отдельное окно с 
        возможностью сохранения
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """
        statistic_window.grab_release()
        statistic_window.destroy()
        var_list = []
        flag = 0
        for i in range(len(checkbutton)):
            if checkbutton_var[i].get() == 1:
                flag = 1
                var_list.append(quantitative_variables[i])
        if flag == 0:
            tki.messagebox.showwarning(title="Предупреждение", message="Не выбраны значения")
        else:
            statistics = pd.DataFrame({'': var_list, 'max': [data[i].max() for i in var_list],
                                       'min': [data[i].min() for i in var_list],
                                       'mean': [data[i].mean() for i in var_list],
                                       'sample_variance': [data[i].var() for i in var_list],
                                       'standard_deviation': [data[i].std() for i in var_list]})
            statistics_columns = statistics.columns
            col = []
            for i in range(len(statistics_columns)):
                col.append(statistics_columns[i])
            statistic_window1 = tki.Toplevel()
            statistic_window1.title("Статистический отчёт")
            statistic_window1.geometry(config['Statistic_menu']['a'] + 'x' + config['Statistic_menu']['b'])
            menu1 = tki.Menu(statistic_window1)
            menu1.add_command(label="Сохранить", command=lambda: save_to_excel(statistics))
            statistic_window1.config(menu=menu1)
            tree1 = ttk.Treeview(statistic_window1, columns=col, show="headings")
            for i in range(len(col)):
                tree1.heading(col[i], text=col[i])
            for i in range(len(statistics)):
                values = []
                for j in range(len(col)):
                    values.append(statistics.iloc[i, j])
                tree1.insert("", tki.END, values=values)
            tree1.pack(fill="both", expand=1)

    config = configparser.ConfigParser()  # создание экземпляра ConfigParser
    config.read(
        'Analysing_demographic_data_of_customers_with_credit_history/config.ini')  # чтение конфигурационного файла
    statistic_window = tki.Toplevel()
    statistic_window.title("Статистический отчет")
    statistic_window.geometry(config['Statistic_menu']['x'] + 'x' + config['Statistic_menu']['y'])
    statistic_window.resizable(False, False)
    label1 = ttk.Label(statistic_window, text="Выберите тип переменных",
                       font=(config['Statistic_menu']['font'], int(config['Statistic_menu']['font_size'])),
                       foreground=config['Statistic_menu']['foreground'])
    label1.grid(row=0, column=0)
    col = ["Количественные", "Качественная"]
    combobox_1 = ttk.Combobox(statistic_window, values=col)
    combobox_1.current(0)
    combobox_1.grid(row=1, column=0)
    button_1 = ttk.Button(statistic_window, text="Подтвердить", command=click_1)
    button_1.grid(row=2, column=0)
    checkbutton_var = []
    checkbutton = []


def pivot_table():
    """
    Создание сводной таблицы по паре выбранных качественных переменных
    Входные данные: нет
    Выходные данные: нет
    Автор:
    """

    def click_1():
        """
        Создание сводной таблицы по паре выбранных качественных переменных после
        проверки на различие выбранных переменных, вывод таблицы в отдельное 
        окно с возможностью сохранения
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """
        if combobox_5 == 'Cумма':
            method = 'count'
        else:
            method = 'mean'
        if combobox_1.get() == combobox_2.get() or combobox_1.get() == combobox_3.get() or combobox_2.get() == \
                combobox_3.get():
            tki.messagebox.showwarning(title="Предупреждение", message="Были выбраны одинаковые значения")
        else:
            pivot_table = pd.pivot_table(data, index=[combobox_1.get(), combobox_2.get()], columns=combobox_3.get(),
                                         values=combobox_4.get(), aggfunc=method)
            pivot_columns = pivot_table.columns
            col = []
            col.append(combobox_1.get())
            col.append(combobox_2.get())
            rows = pivot_table.index.tolist()
            for i in range(len(pivot_columns)):
                col.append(pivot_columns[i])
            pivot_window1 = tki.Toplevel()
            pivot_window1.title("Сводная таблица")
            pivot_window1.geometry(config['Pivot_menu']['a'] + 'x' + config['Pivot_menu']['b'])
            menu1 = tki.Menu(pivot_window1)
            menu1.add_command(label="Сохранить", command=lambda: save_to_excel_index(pivot_table))
            pivot_window1.config(menu=menu1)
            tree1 = ttk.Treeview(pivot_window1, columns=col, show="headings")
            for i in range(len(col)):
                tree1.heading(col[i], text=col[i])
            for i in range(len(pivot_table)):
                values = []
                values.append(rows[i][0])
                values.append(rows[i][1])
                for j in range(len(col) - 2):
                    values.append(pivot_table.iloc[i, j])
                tree1.insert("", tki.END, values=values)
            scrollbar1 = ttk.Scrollbar(pivot_window1, orient="horizontal", command=tree1.xview)
            scrollbar1.pack(fill="x", side="bottom")
            tree1["xscrollcommand"] = scrollbar1.set
            tree1.pack(fill="both", expand=1)
            pivot_window.grab_release()
            pivot_window.destroy()

    config = configparser.ConfigParser()  # создание экземпляра ConfigParser
    config.read(
        'Analysing_demographic_data_of_customers_with_credit_history/config.ini')  # чтение конфигурационного файла
    pivot_window = tki.Toplevel()
    pivot_window.title("Сводная таблица")
    pivot_window.geometry(config['Pivot_menu']['x'] + 'x' + config['Pivot_menu']['y'])
    pivot_window.resizable(False, False)
    methods = ['Сумма', 'Среднее']
    label_1 = ttk.Label(pivot_window, text="Выберите качественные переменные",
                        font=(config['Pivot_menu']['font'], int(config['Pivot_menu']['font_size'])),
                        foreground=config['Pivot_menu']['foreground'])
    label_1.grid(row=0, column=1)
    combobox_1 = ttk.Combobox(pivot_window, values=qualitative_variables)
    combobox_1.current(0)
    combobox_1.grid(row=1, column=0)
    combobox_2 = ttk.Combobox(pivot_window, values=qualitative_variables)
    combobox_2.current(1)
    combobox_2.grid(row=1, column=1)
    combobox_3 = ttk.Combobox(pivot_window, values=qualitative_variables)
    combobox_3.current(2)
    combobox_3.grid(row=1, column=2)
    label_2 = ttk.Label(pivot_window, text="Выберите количественную переменную",
                        font=(config['Pivot_menu']['font'], int(config['Pivot_menu']['font_size'])),
                        foreground=config['Pivot_menu']['foreground'])
    label_2.grid(row=2, column=1)
    combobox_4 = ttk.Combobox(pivot_window, values=quantitative_variables)
    combobox_4.current(0)
    combobox_4.grid(row=3, column=1)
    label_3 = ttk.Label(pivot_window, text="Выберите метод агрегации",
                        font=(config['Pivot_menu']['font'], int(config['Pivot_menu']['font_size'])),
                        foreground=config['Pivot_menu']['foreground'])
    label_3.grid(row=4, column=1)
    combobox_5 = ttk.Combobox(pivot_window, values=methods)
    combobox_5.current(0)
    combobox_5.grid(row=5, column=1)
    button_1 = ttk.Button(pivot_window, text="Создать таблицу", command=click_1)
    button_1.grid(row=6, column=1)


def clustered_bar_chart():
    """
    Создание кластеризованной столбчатой диаграммы для пары 'качественная - качественная' переменных
    Входные данные: нет
    Выходные данные: нет
    Автор:
    """

    def selected_1(event):
        """
        Создание выпадающего списка
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """

        def selected_2(event):
            """
            Создание выпадающего списка
            Входные данные: нет
            Выходные данные: нет
            Автор:
            """

            def selected_3(event):
                """
                Создание и вывод графика на экран
                Входные данные: нет
                Выходные данные: нет
                Автор:
                """

                def selected_4():
                    """
                    Сохранение графика в файл .png
                    Входные данные: нет
                    Выходные данные: нет
                    Автор:
                    """
                    fig.savefig('/Users/tima/desktop/to.png')  # сохранение в формате .png

                fig = Figure(figsize=(15, 7), dpi=100)  # создание экземпляра Figure для графиков
                ax = fig.add_subplot(111)  # создание поля для графика
                x_list = pd.unique(data[combobox_1.get()])  # инициализация датафрейма из уровней первой переменной
                y_list = [sum(data[data[combobox_2.get()] == combobox_3.get()]
                              [combobox_1.get()] == x) for x in x_list]  # создание списка частот для каждого уровня
                color = list('rbgmcyk')  # инициализация списка цветов для диаграммы
                ax.grid()  # добавление сетки на график
                ax.bar(x_list, y_list, color=color)  # построение диаграммы
                canvas_1 = FigureCanvasTkAgg(fig, master=window)  # создание поля для двумерных изображений
                canvas_1.draw()  # перерисовывание текущей фигуры
                canvas_1.get_tk_widget().pack(side=tki.TOP, fill=tki.NONE, expand=0)  # расположение графика на виджете
                btn = tki.Button(window, text='Сохранить', command=selected_4)  # создание кнопки для сохранения
                btn.pack(anchor=tki.S)  # расположение кнопки
                window.after(200, None)  # продолжение в фоновом режиме

            label_3 = ttk.Label(window, text='Выберите значение второй переменной',
                                font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                                foreground=config['Graphic_menu']['foreground'])  # создание надписи
            label_3.place(x=20, y=110)  # расположение надписи
            selection = combobox_2.get()  # получение текущего выбранного значения из второго списка
            a = list(data[selection].unique())  # инициализация списка из уровней выбранной переменной
            combobox_3 = ttk.Combobox(window, values=a, state='readonly')  # создание третьего выпадающего списка
            combobox_3.place(x=20, y=130)  # расположение выпадающего списка
            combobox_3.bind('<<ComboboxSelected>>', selected_3)  # отслеживание статуса списка

        label_2 = ttk.Label(window, text='Выберите 2-ю качественную переменную',
                            font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                            foreground=config['Graphic_menu']['foreground'])  # создание надписи
        label_2.place(x=20, y=70)  # расположение надписи
        drop = combobox_1.get()  # сохранение индекса использованной до этого переменной
        combobox_2 = ttk.Combobox(window, values=[x for x in qualitative_variables if x != drop], state='readonly')  #
        # создание второго выпадающего списка из оставшихся переменных
        combobox_2.place(x=20, y=90)  # расположение выпадающего списка
        combobox_2.bind('<<ComboboxSelected>>', selected_2)  # отслеживание статуса списка

    config = configparser.ConfigParser()  # создание экземпляра ConfigParser
    config.read(
        'Analysing_demographic_data_of_customers_with_credit_history/config.ini')  # чтение конфигурационного файла
    window = tki.Toplevel()  # открывает новое диалоговое окно
    window.title("Кластеризованная столбчатая диаграмма")  # название окна
    window.geometry(config['Graphic_menu']['x'] + 'x' + config['Graphic_menu']['y'])  # размер окна
    label_1 = ttk.Label(window, text='Выберите 1-ю качественную переменную',
                        font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                        foreground=config['Graphic_menu']['foreground'])  # создание надписи
    label_1.place(x=20, y=30)  # расположение надписи
    combobox_1 = ttk.Combobox(window, values=qualitative_variables, state='readonly')  # создание первого выпадающего
    # списка
    combobox_1.place(x=20, y=50)  # расположение выпадающего списка
    combobox_1.bind('<<ComboboxSelected>>', selected_1)  # отслеживание статуса списка


def categorized_bar_chart():
    """
    Создание категоризированной гистограммы для пары 'количественная - качественная' переменных
    Входные данные: нет
    Выходные данные: нет
    Автор:
    """

    def selected_1(event):
        """
        Создание выпадающего списка
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """

        def selected_2(event):
            """
            Создание выпадающего списка
            Входные данные: нет
            Выходные данные: нет
            Автор:
            """

            def selected_3(event):
                """
                Создание и вывод графика на экран
                Входные данные: нет
                Выходные данные: нет
                Автор:
                """

                def selected_4():
                    """
                    Сохранение графика в файл .png
                    Входные данные: нет
                    Выходные данные: нет
                    Автор:
                    """
                    fig.savefig('/Users/tima/desktop/to.png')  # сохранение в формате .png

                fig = Figure(figsize=(15, 7), dpi=100)  # создание экземпляра Figure для графиков
                column_size = len(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()])  # нахождение
                # размера выборки
                s_dev = np.std(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()])  # нахождение
                # среднего отклонения
                iqr = np.subtract(*np.percentile(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()],
                                                 [75, 25]))  # нахождение межквартильного размаха
                min_max = max(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()]) - \
                    min(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()])  # нахождение размаха
                # выборки
                sturges = 1 + 3.322 * np.log10(column_size)  # Sturges' formula
                scott = min_max * np.power(column_size, 1 / 3) / (3.5 * s_dev)  # Scott's rule
                freedman = min_max * np.power(column_size, 1 / 3) / (2 * iqr)  # Freedman–Diaconis' choice
                labels = ['Sturges', 'Scott', 'Freedman-Diaconis', 'Categories']  # инициализация списка названий для
                # гистограмм
                colors = ['#3e1ca8', '#ff3442', '#00e277', '#ffe4e1']  # инициализация списка цветов для гистограммы
                n_bins = list(map(round, [sturges, scott, freedman])) + [10]  # список из количества интервалов на
                # графиках
                for i in range(4):
                    ax = fig.add_subplot(int('22' + str(i + 1)))  # создание поля для графика
                    ax.hist(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()], bins=n_bins[i],
                            color=colors[i])  # построение диаграммы
                    ax.set_title(labels[i])  # добавление названия
                    ax.axvline(np.mean(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()]),
                               linestyle='dashed', color='black')  # построение линии через среднее значение
                canvas_1 = FigureCanvasTkAgg(fig, master=window)  # создание поля для двумерных изображений
                canvas_1.draw()  # перерисовывание текущей фигуры
                canvas_1.get_tk_widget().pack(side=tki.TOP, fill=tki.NONE, expand=0)  # расположение графиков на виджете
                btn = tki.Button(window, text='Сохранить', command=selected_4)  # создание кнопки сохранения
                btn.pack(anchor=tki.S)  # расположение кнопки
                window.after(200, None)  # продолжение в фоновом режиме

            label_3 = ttk.Label(window, text='Выберите значение качественной переменной',
                                font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                                foreground=config['Graphic_menu']['foreground'])  # создание надписи
            label_3.place(x=20, y=110)  # расположение надписи
            selection = combobox_2.get()  # получение выбранного значения из второго списка
            a = list(data[selection].unique())  # инициализация списка из уровней выбранной переменной
            combobox_3 = ttk.Combobox(window, values=a, state='readonly')  # создание третьего выпадающего списка
            combobox_3.place(x=20, y=130)  # расположение списка
            combobox_3.bind('<<ComboboxSelected>>', selected_3)  # отслеживание статуса списка

        label_2 = ttk.Label(window, text='Выберите качественную переменную',
                            font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                            foreground=config['Graphic_menu']['foreground'])  # создание надписи
        label_2.place(x=20, y=70)  # расположение надписи
        combobox_2 = ttk.Combobox(window, values=qualitative_variables, state='readonly')  # создание второго списка
        combobox_2.place(x=20, y=90)  # расположение списка
        combobox_2.bind('<<ComboboxSelected>>', selected_2)  # отслеживание статуса списка

    config = configparser.ConfigParser()  # создание экземпляра ConfigParser
    config.read(
        'Analysing_demographic_data_of_customers_with_credit_history/config.ini')  # чтение конфигурационного файла
    window = tki.Toplevel()  # создание диалогового окна
    window.title("Категоризированная гистограмма")  # название окна
    window.geometry(config['Graphic_menu']['x'] + 'x' + config['Graphic_menu']['y'])  # размер окна
    label_1 = ttk.Label(window, text='Выберите количественную переменную',
                        font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                        foreground=config['Graphic_menu']['foreground'])  # создание надписи
    label_1.place(x=20, y=30)  # расположение надписи
    combobox_1 = ttk.Combobox(window, values=quantitative_variables, state='readonly')  # создание первого выпадающего
    # списка
    combobox_1.place(x=20, y=50)  # расположение списка
    combobox_1.bind('<<ComboboxSelected>>', selected_1)  # отслеживание статуса списка


def box_and_whiskers_chart():
    """
    Создание категоризированной диаграммы Бокса-Вискера для пары 'количественная - качественная' переменных
    Входные данные: нет
    Выходные данные: нет
    Автор:
    """

    def selected_1(event):
        """
        Создание выпадающего списка
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """

        def selected_2(event):
            """
            Создание выпадающего списка
            Входные данные: нет
            Выходные данные: нет
            Автор:
            """

            def selected_3(event):
                """
                Создание и вывод графика на экран
                Входные данные: нет
                Выходные данные: нет
                Автор:
                """

                def selected_4():
                    """
                    Сохранение графика в файл .png
                    Входные данные: нет
                    Выходные данные: нет
                    Автор:
                    """
                    fig.savefig('/Users/tima/desktop/to.png')  # сохранение в формате .png

                fig = Figure(figsize=(15, 7), dpi=100)  # создание экземпляра Figure для графиков
                ax = fig.add_subplot(111)  # создание поля для графика
                ax.boxplot(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()], vert=False)  # построение
                # диаграммы
                canvas_1 = FigureCanvasTkAgg(fig, master=window)  # создание поля для двумерных изображений
                canvas_1.draw()  # перерисовывание текущей фигуры
                canvas_1.get_tk_widget().pack(side=tki.TOP, fill=tki.NONE, expand=0)  # расположение графика на виджете
                btn = tki.Button(window, text='Сохранить', command=selected_4)  # создание кнопки сохранения
                btn.pack(anchor=tki.S)  # расположение кнопки
                window.after(200, None)  # продолжение в фоновом режиме

            label_3 = ttk.Label(window, text='Выберите значение качественной переменной',
                                font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                                foreground=config['Graphic_menu']['foreground'])  # создание надписи
            label_3.place(x=20, y=110)  # расположение надписи
            selection = combobox_2.get()  # получение выбранного значения
            a = list(data[selection].unique())  # инициализация списка из уровней выбранной переменной
            combobox_3 = ttk.Combobox(window, values=a, state='readonly')  # создание выпадающего списка
            combobox_3.place(x=20, y=130)  # расположение списка
            combobox_3.bind('<<ComboboxSelected>>', selected_3)  # отслеживание статуса списка

        label_2 = ttk.Label(window, text='Выберите качественную переменную',
                            font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                            foreground=config['Graphic_menu']['foreground'])  # создание надписи
        label_2.place(x=20, y=70)  # расположение надписи
        combobox_2 = ttk.Combobox(window, values=qualitative_variables, state='readonly')  # создание выпадающего списка
        combobox_2.place(x=20, y=90)  # расположение списка
        combobox_2.bind('<<ComboboxSelected>>', selected_2)  # отслеживание списка

    config = configparser.ConfigParser()  # создание экземпляра ConfigParser
    config.read(
        'Analysing_demographic_data_of_customers_with_credit_history/config.ini')  # чтение конфигурационного файла
    window = tki.Toplevel()  # создание диалогового окна
    window.title("Категоризированная диаграмма Бокса-Вискера")  # название окна
    window.geometry(config['Graphic_menu']['x'] + 'x' + config['Graphic_menu']['y'])  # размер окна
    label_1 = ttk.Label(window, text='Выберите количественную переменную',
                        font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                        foreground=config['Graphic_menu']['foreground'])  # создание надписи
    label_1.place(x=20, y=30)  # расположение надписи
    combobox_1 = ttk.Combobox(window, values=quantitative_variables, state='readonly')  # создание выпадающего списка
    combobox_1.place(x=20, y=50)  # расположение списка
    combobox_1.bind('<<ComboboxSelected>>', selected_1)  # отслеживание статуса списка


def scatter_chart():

    """
    Создание категоризированной диаграммы рассеивания для пары количественных переменных и одной качественной переменной
    Входные данные: нет
    Выходные данные: нет
    Автор:
    """

    def selected_1(event):
        """
        Создание выпадающего списка
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """

        def selected_2(event):
            """
            Создание выпадающего списка
            Входные данные: нет
            Выходные данные: нет
            Автор:
            """

            def selected_3(event):
                """
                Создание выпадающего списка
                Входные данные: нет
                Выходные данные: нет
                Автор:
                """

                def selected_4(event):
                    """
                    Создание и вывод графика на экран
                    Входные данные: нет
                    Выходные данные: нет
                    Автор:
                    """

                    def selected_5():
                        """
                        Сохранение графика в файл .png
                        Входные данные: нет
                        Выходные данные: нет
                        Автор:
                        """
                        fig.savefig('/Users/tima/desktop/to.png')  # сохранение в формате .png

                    fig = Figure(figsize=(15, 7), dpi=100)  # создание экземпляра Figure для графиков
                    ax = fig.add_subplot(111)  # создание поля для графика
                    x_list = data[data[combobox_3.get()] == combobox_4.get()][combobox_1.get()]  # создание датафрейма
                    # для первой переменной
                    y_list = data[data[combobox_3.get()] == combobox_4.get()][combobox_2.get()]  # создание датафрейма
                    # для второй переменной
                    ax.scatter(x_list, y_list, s=1)  # создание графика
                    canvas_1 = FigureCanvasTkAgg(fig, master=window)  # создание поля для двумерных изображений
                    canvas_1.draw()  # перерисовывание текущей фигуры
                    canvas_1.get_tk_widget().pack(side=tki.TOP, fill=tki.NONE, expand=0)  # расположение графика на
                    # виджете
                    btn = tki.Button(window, text='Сохранить', command=selected_5)  # создание кнопки сохранения
                    btn.pack(anchor=tki.S)  # расположение кнопки
                    window.after(200, None)  # продолжение в фоновом режиме

                label_4 = ttk.Label(window, text='Выберите значение качественной переменной',
                                    font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                                    foreground=config['Graphic_menu']['foreground'])  # создание надписи
                label_4.place(x=20, y=150)  # расположение надписи
                selection = combobox_3.get()  # получение выбранного значения
                a = list(data[selection].unique())  # инициализация списка из уровней выбранной переменной
                combobox_4 = ttk.Combobox(window, values=a, state='readonly')  # создание выпадающего списка
                combobox_4.place(x=20, y=170)  # расположение списка
                combobox_4.bind('<<ComboboxSelected>>', selected_4)  # отслеживание статуса списка

            label_3 = ttk.Label(window, text='Выберите качественную переменную',
                                font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                                foreground=config['Graphic_menu']['foreground'])  # создание надписи
            label_3.place(x=20, y=110)  # расположение надписи
            combobox_3 = ttk.Combobox(window, values=qualitative_variables, state='readonly')  # создание выпадающего
            # списка
            combobox_3.place(x=20, y=130)  # расположение списка
            combobox_3.bind('<<ComboboxSelected>>', selected_3)  # отслеживание статуса списка

        label_2 = ttk.Label(window, text='Выберите 2-ю количественную переменную',
                            font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                            foreground=config['Graphic_menu']['foreground'])  # создание надписи
        label_2.place(x=20, y=70)  # расположение надписи
        drop = combobox_1.get()  # сохранения индекса выбранной переменной
        combobox_2 = ttk.Combobox(window, values=[x for x in quantitative_variables if x != drop], state='readonly')  #
        # создание выпадающего списка
        combobox_2.place(x=20, y=90)  # расположение списка
        combobox_2.bind('<<ComboboxSelected>>', selected_2)  # отслеживание статуса списка

    config = configparser.ConfigParser()  # создание экземпляра ConfigParser
    config.read(
        'Analysing_demographic_data_of_customers_with_credit_history/config.ini')  # чтение конфигурационного файла
    window = tki.Toplevel()  # создание диалогового окна
    window.title("Категоризированная диаграмма рассеивания")  # название окна
    window.geometry(config['Graphic_menu']['x'] + 'x' + config['Graphic_menu']['y'])  # размер окна
    label_1 = ttk.Label(window, text='Выберите 1-ю количественную переменную',
                        font=(config['Graphic_menu']['font'], int(config['Graphic_menu']['font_size'])),
                        foreground=config['Graphic_menu']['foreground'])  # создание надписи
    label_1.place(x=20, y=30)  # расположение надписи
    combobox_1 = ttk.Combobox(window, values=quantitative_variables, state='readonly')  # создание выпадающего списка
    combobox_1.place(x=20, y=50)  # расположение списка
    combobox_1.bind('<<ComboboxSelected>>', selected_1)  # отслеживание статуса списка


def settings_editing():
    """
    Пользовательская настройка интерфейса
    Входные данные: нет
    Выходные данные: нет
    Автор:
    """
    config = configparser.ConfigParser()  # создание экземпляра ConfigParser
    config.read(
        'Analysing_demographic_data_of_customers_with_credit_history/config.ini')  # чтение конфигурационного файла

    def selected_1(event):
        """
        Создание списка доступных для изменения настроек
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """
        def selected_2(event):
            """
            Создание списка доступных значений для изменения настройки
            Входные данные: нет
            Выходные данные: нет
            Автор:
            """
            def selected_font(event):
                """
                Изменение шрифта
                Входные данные: нет
                Выходные данные: нет
                Автор:
                """
                config = configparser.RawConfigParser()
                config.optionxform = str
                config.read('Analysing_demographic_data_of_customers_with_credit_history/config.ini')
                config.set(dict_1[combobox_1.get()], 'font', combobox_3.get())
                with open('Analysing_demographic_data_of_customers_with_credit_history/config.ini', 'w') as configfile:
                    config.write(configfile)

            def selected_color(event):
                """
                Изменение цвета
                Входные данные: нет
                Выходные данные: нет
                Автор:
                """
                config = configparser.RawConfigParser()
                config.optionxform = str
                config.read('Analysing_demographic_data_of_customers_with_credit_history/config.ini')
                config.set(dict_1[combobox_1.get()], 'foreground', dict_3[combobox_3.get()])
                with open('Analysing_demographic_data_of_customers_with_credit_history/config.ini', 'w') as configfile:
                    config.write(configfile)

            def selected_number():
                """
                Изменение размера окон
                Входные данные: нет
                Выходные данные: нет
                Автор:
                """
                config = configparser.RawConfigParser()
                config.optionxform = str
                config.read('Analysing_demographic_data_of_customers_with_credit_history/config.ini')
                config.set(dict_1[combobox_1.get()], dict_2[combobox_2.get()], str(spinbox.get()))
                with open('Analysing_demographic_data_of_customers_with_credit_history/config.ini', 'w') as configfile:
                    config.write(configfile)

            selection_2 = combobox_2.get()
            if selection_2 == 'Шрифт':
                combobox_3 = ttk.Combobox(window, values=['TkDefaultFont', 'TkTextFont', 'TkFixedFont', 'TkMenuFont',
                                                          'TkHeadingFont', 'TkCaptionFont', 'TkSmallCaptionFont',
                                                          'TkIconFont', 'TkTooltipFont'])
                combobox_3.place(x=250, y=100)
                combobox_3.bind('<<ComboboxSelected>>', selected_font)
            elif selection_2 == 'Цвет текста':
                dict_3 = {'Чёрный': '#000000', 'Красный': '#FF0000', 'Синий': '#0000FF', 'Зелёный': '#008000',
                          'Жёлтый': '#FFFF00', 'Фиолетовый': '#8B00FF', 'Оранжевый': '#FFA500'}
                combobox_3 = ttk.Combobox(window, values=['Чёрный', 'Красный', 'Синий', 'Зелёный', 'Жёлтый',
                                                          'Фиолетовый', 'Оранжевый'])
                combobox_3.place(x=250, y=100)
                combobox_3.bind('<<ComboboxSelected>>', selected_color)
            else:
                spinbox = ttk.Spinbox(window, from_=100, to=900, state='readonly')
                btn = ttk.Button(window, text='Сохранить', command=selected_number)
                btn.pack(anchor=tki.S)

        selection_1 = combobox_1.get()
        label_2 = ttk.Label(window, text='Выберите настройку, который вы хотите изменить',
                            font=(config['Settings_menu']['font'], int(config['Settings_menu']['font_size'])),
                            foreground=config['Settings_menu']['foreground'])  # создание надписи
        label_2.place(x=20, y=70)  # расположение надписи
        dict_2 = {'Длина окна': 'x', 'Ширина окна': 'y', 'Минимальная длина': 'x_min', 'Минимальная ширина': 'y_min',
                  'Размер шрифта': 'font_size', 'Длина доп. окна': 'a', 'Ширина доп. окна': 'b'}
        if selection_1 == 'Основное меню':
            a = ['Длина окна', 'Ширина окна', 'Минимальная длина', 'Минимальная ширина']
        elif selection_1 == 'Меню модификации':
            a = ['Длина окна', 'Ширина окна']
        elif selection_1 in ('Статистический отчёт', 'Сводная таблица'):
            a = ['Длина окна', 'Ширина окна', 'Длина доп. окна', 'Ширина доп. окна', 'Шрифт', 'Размер шрифта',
                 'Цвет текста']
        else:
            a = ['Длина окна', 'Ширина окна', 'Шрифт', 'Размер шрифта', 'Цвет текста']
        combobox_2 = ttk.Combobox(window, values=a, state='readonly')
        combobox_2.place(x=20, y=100)
        combobox_2.bind('<<ComboboxSelected>>', selected_2)

    window = tki.Toplevel()  # создание диалогового окна
    window.title('Настройки приложения')  # название окна
    window.geometry(config['Settings_menu']['x'] + 'x' + config['Settings_menu']['y'])  # размер окна
    label_1 = ttk.Label(window, text='Выберите раздел настроек, который вы хотите изменить',
                        font=(config['Settings_menu']['font'], int(config['Settings_menu']['font_size'])),
                        foreground=config['Settings_menu']['foreground'])  # создание надписи
    label_1.place(x=20, y=30)  # расположение надписи
    dict_1 = {'Основное меню': 'Main_menu', 'Графические отчёты': 'Graphic_menu', 'Меню добавления': 'Adding_menu',
              'Меню удаления': 'Deleting_menu', 'Меню модификации': 'Modification_menu', 'Фильтр': 'Filter_menu',
              'Статистический отчёт': 'Statistic_menu', 'Сводная таблица': 'Pivot_menu',
              'Меню настроек': 'Settings_menu'}
    combobox_1 = ttk.Combobox(window, values=['Основное меню', 'Графические отчёты', 'Меню добавления', 'Меню удаления',
                                              'Меню модификации', 'Фильтр', 'Статистический отчёт', 'Сводная таблица',
                                              'Меню настроек'], state='readonly')  #
    # создание выпадающего списка
    combobox_1.place(x=20, y=50)  # расположение списка
    combobox_1.bind('<<ComboboxSelected>>', selected_1)  # отслеживание статуса списка


def interface():
    """
    Интерфейс программы
    Входные данные: нет
    Выходные данные: нет
    Автор:
    """
    config = configparser.ConfigParser()  # создание экземпляра ConfigParser
    config.read(
        'Analysing_demographic_data_of_customers_with_credit_history/config.ini')  # чтение конфигурационного файла
    root = tki.Tk()
    root.title('Приложение для анализа данных кредитных историй заёмщиков')
    root.geometry(config['Main_menu']['x'] + 'x' + config['Main_menu']['y'])
    root.minsize(int(config['Main_menu']['x_min']), int(config['Main_menu']['y_min']))
    menu = tki.Menu(root)
    edit_menu = tki.Menu(tearoff=0)
    edit_menu.add_command(label="Редактировать ячейку", command=lambda: manual_modification(tree))
    edit_menu.add_command(label="Удалить строку", command=lambda: deleting_entities(tree))
    edit_menu.add_command(label="Добавить строку", command=lambda: adding_entities(tree))
    file_menu = tki.Menu(tearoff=0)
    file_menu.add_cascade(label="Редактировать", menu=edit_menu)
    file_menu.add_command(label="Сохранить", command=lambda: save_to_excel(data))
    report_menu = tki.Menu(tearoff=0)
    report_menu.add_command(label="Фильтр", command=data_filter)
    report_menu.add_command(label="Статистический отчёт", command=statistic_report)
    report_menu.add_command(label="Сводная таблица", command=pivot_table)
    graphic_menu = tki.Menu(tearoff=0)
    graphic_menu.add_command(label='Кластеризованная столбчатая диаграмма', command=clustered_bar_chart)
    graphic_menu.add_command(label='Категоризированная гистограмма', command=categorized_bar_chart)
    graphic_menu.add_command(label='Категоризированная диаграмма Бокса-Вискера', command=box_and_whiskers_chart)
    graphic_menu.add_command(label='Категоризированная диаграмма рассеивания', command=scatter_chart)
    settings_menu = tki.Menu(tearoff=0)
    settings_menu.add_command(label='Настройки', command=settings_editing)
    menu.add_cascade(label="Файл", menu=file_menu)
    menu.add_cascade(label="Текстовые отчёты", menu=report_menu)
    menu.add_cascade(label="Графические отчёты", menu=graphic_menu)
    menu.add_cascade(label='Настройки', menu=settings_menu)
    root.config(menu=menu)
    tree = ttk.Treeview(columns=columns, show="headings", height=500)
    for i in range(len(columns)):
        tree.heading(columns[i], text=columns[i])
    for i in range(len(data)):
        values = []
        for j in range(len(columns)):
            values.append(data.iloc[i, j])
        tree.insert("", tki.END, values=values, iid=i)
    scrollbar1 = ttk.Scrollbar(orient="horizontal", command=tree.xview)
    scrollbar1.pack(fill="x", side="bottom")
    tree["xscrollcommand"] = scrollbar1.set
    scrollbar2 = ttk.Scrollbar(orient="vertical", command=tree.yview, )
    scrollbar2.pack(side="right", fill="y")
    tree["yscrollcommand"] = scrollbar2.set
    tree.pack()
    root.mainloop()


file = 'Analysing_demographic_data_of_customers_with_credit_history/Base_edited.xlsx'  # файл с исходной базой данных
data = read_from_text_file(file)  # чтение файла
data_columns = data.columns  # создание списка из столбцов
columns = []
int_columns = []
string_columns = []
float_columns = []
for i in range(len(data_columns)):
    columns.append(data_columns[i])
    if isinstance(data.iloc[1, i], str):
        string_columns.append(data_columns[i])
    elif isinstance(data.iloc[1, i], np.float64):
        float_columns.append(data_columns[i])
    else:
        int_columns.append(data_columns[i])
qualitative_variables = ['Attrition_Flag', 'Gender', 'Education_Level',
                         'Marital_Status', 'Income_Category', 'Card_Category']  # список качественных переменных
quantitative_variables = ['Customer_Age', 'Dependent_count', 'Months_on_book',
                          'Total_Relationship_Count', 'Months_Inactive_12_mon',
                          'Contacts_Count_12_mon', 'Credit_Limit',
                          'Total_Revolving_Bal', 'Avg_Open_To_Buy',
                          'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt',
                          'Total_Trans_Ct', 'Total_Ct_Chng_Q4_Q1',
                          'Avg_Utilization_Ratio']  # список количественных переменных
interface()  # вызов и запуск интерфейса
