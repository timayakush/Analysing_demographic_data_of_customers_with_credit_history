#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data analysis project v 2.7.1
"""
import tkinter as tki
import tkinter.ttk as ttk
from tkinter import filedialog as fld
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def read_from_text_file(file_name):
    """
    Функция читает базу данных из файла формата .csv или .xlsx
    Входные данные: имя файла (строка)
    Выходные данные: датафрейм с базой данных (pd.DataFrame())
    Автор:
    """
    if '.csv' in file_name:
        data_local = pd.read_csv(file_name)
    else:
        data_local = pd.read_excel(file_name)
    return data_local


def read_from_bin_file(file_name):
    """
    Функция читает базу данных из двоичного файла
    Входные данные: имя файла
    Выходные данные: базa данных (массив, кортеж, словарь и т. д.)
    Автор:
    """
    data_local = np.load(file_name)
    return data_local


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
    data_local.to_excel(path, index=False)


def save_to_csv(file_name, data_local):
    """
    Функция сохраняет базу данных в файл .csv
    Входные данные: имя файла (строка), датафрейм с базой данных (pd.DataFrame())
    Выходные данные: нет
    Автор:
    """
    np.savetxt(file_name, data_local, fmt='%s', delimiter=';')


def save_to_bin_file(data_local, file_name):
    """
    Функция сохраняет базу данных в бинарный файл
    Входные данные: датафрейм с базой данных (pd.DataFrame()), имя файла (строка)
    Выходные данные: нет
    Автор:
    """
    np.save(file_name, data_local)


def save_graphics(file_name):
    """
    Функция сохраняет построенный график в файл .png
    Входные данные: имя файла (строка)
    Выходные данные: нет
    Автор:
    """
    plt.savefig(file_name)


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
        for i in range(len(columns)):
            if columns[i] in string_columns:
                entities.append(combobox[i].get())
            elif columns[i] in int_columns:
                entities.append(np.int64(spinbox[i].get()))
            else:
                entities.append(np.float64(spinbox[i].get()))
        data.loc[len(data.index)] = entities
        add_window.grab_release()
        add_window.destroy()
        tree.insert("", tki.END, values=entities, iid=len(data))
    add_window = tki.Toplevel()
    add_window.title("Добавление строки")
    add_window.geometry("350x525")
    add_window.resizable(False, False)
    combobox = 23 * [0]
    spinbox = 23 * [0]
    for i in range(len(columns) - 2):
        add_label = tki.Label(add_window, text=columns[i])
        add_label.grid(row=i, column=0)
    add_label = tki.Label(add_window, text="Naive_Bayes_Classifier_mon1")
    add_label.grid(row=21, column=0)
    add_label = tki.Label(add_window, text="Naive_Bayes_Classifier_mon2")
    add_label.grid(row=22, column=0)
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
    add_button = tki.Button(add_window, text="Добавить", command=add_click)
    add_button.grid(row=23, column=1, sticky="we")


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
        label = ttk.Label(check_window, text="Удалить выделенную строку?")
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
        print(data)
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
        edit_button2 = ttk.Button(edit_window, text="Редактировать",
                                  command=lambda: edit_click2(value.get(), edit_column, row_num, edit_window))
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
        if edit_column in string_columns:
            new_value = value
        elif edit_column in int_columns:
            new_value = np.int64(value)
        else:
            new_value = np.float64(value)
        pd.options.mode.chained_assignment = None
        data[edit_column][row_num] = new_value
        print(data)
        edit_window.grab_release()
        edit_window.destroy()
        tree.delete(*tree.get_children())
        for i in range(len(data)):
            values = []
            for j in range(len(columns)):
                values.append(data.iloc[i, j])
            tree.insert("", tki.END, values=values, iid=i)
        tree.bind('<<TreeviewSelect>>', plug)

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
            if columns[i] in string_columns:
                characteristics = []
                pd_characteristics = pd.unique(data[columns[i]])
                for j in range(len(pd_characteristics)):
                    characteristics.append(pd_characteristics[j])
                combobox[i] = ttk.Combobox(window, values=characteristics)
                combobox[i].current(0)
                combobox[i].grid(row=i, column=1)
            if columns[i] in int_columns or columns[i] in float_columns:
                characteristics = pd.unique(data[columns[i]])
                spinbox[i] = tki.Spinbox(window, from_=min(characteristics),
                                         to=max(characteristics))
                spinbox[i].grid(row=i, column=1)

    def click1():
        """
        Функция проверяет, заданы ли условия для фильтрации. Если да, то 
        выводит список столбцов для выбора тех, которые останутся в
        отфильтрованной базе данных
        Входные данные: нет
        Выходные данные: нет
        Автор:
        """
        flag = 0
        SEL = True
        for i in range(len(checkbutton)):
            if checkbutton_var[i].get() == 1:
                flag = 1
                if columns[i] in string_columns:
                    condition = combobox[i].get()
                elif columns[i] in int_columns:
                    condition = np.int64(spinbox[i].get())
                else:
                    condition = np.float64(spinbox[i].get())
                SEL = SEL & (data[columns[i]] == condition)
        if flag == 0:
            tki.messagebox.showwarning(title="Предупреждение",
                                       message="Не выбраны значения")
        else:
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[0], variable=checkbutton_var1[0]))
            checkbutton1[0].grid(row=0, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[1], variable=checkbutton_var1[1]))
            checkbutton1[1].grid(row=1, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[2], variable=checkbutton_var1[2]))
            checkbutton1[2].grid(row=2, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[3], variable=checkbutton_var1[3]))
            checkbutton1[3].grid(row=3, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[4], variable=checkbutton_var1[4]))
            checkbutton1[4].grid(row=4, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[5], variable=checkbutton_var1[5]))
            checkbutton1[5].grid(row=5, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[6], variable=checkbutton_var1[6]))
            checkbutton1[6].grid(row=6, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[7], variable=checkbutton_var1[7]))
            checkbutton1[7].grid(row=7, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[8], variable=checkbutton_var1[8]))
            checkbutton1[8].grid(row=8, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[9], variable=checkbutton_var1[9]))
            checkbutton1[9].grid(row=9, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[10], variable=checkbutton_var1[10]))
            checkbutton1[10].grid(row=10, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[11], variable=checkbutton_var1[11]))
            checkbutton1[11].grid(row=11, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[12], variable=checkbutton_var1[12]))
            checkbutton1[12].grid(row=12, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[13], variable=checkbutton_var1[13]))
            checkbutton1[13].grid(row=13, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[14], variable=checkbutton_var1[14]))
            checkbutton1[14].grid(row=14, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[15], variable=checkbutton_var1[15]))
            checkbutton1[15].grid(row=15, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[16], variable=checkbutton_var1[16]))
            checkbutton1[16].grid(row=16, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[17], variable=checkbutton_var1[17]))
            checkbutton1[17].grid(row=17, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[18], variable=checkbutton_var1[18]))
            checkbutton1[18].grid(row=18, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[19], variable=checkbutton_var1[19]))
            checkbutton1[19].grid(row=19, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(ttk.Checkbutton(window, text=columns[20], variable=checkbutton_var1[20]))
            checkbutton1[20].grid(row=20, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(
                ttk.Checkbutton(window, text="Naive_Bayes_Classifier_mon1", variable=checkbutton_var1[21]))
            checkbutton1[21].grid(row=21, column=2)
            checkbutton_var1.append(tki.IntVar())
            checkbutton1.append(
                ttk.Checkbutton(window, text="Naive_Bayes_Classifier_mon2", variable=checkbutton_var1[22]))
            checkbutton1[22].grid(row=22, column=2)
            btn2 = ttk.Button(window, text="Отфильтровать", command=lambda: click2(SEL))
            btn2.grid(row=24, column=1)

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

    window = tki.Toplevel()
    window.title("Фильтр")
    window.geometry("500x550")
    window.resizable(False, False)
    checkbutton_var = []
    checkbutton = []
    checkbutton_var1 = []
    checkbutton1 = []
    spinbox = 23 * [0]
    combobox = 23 * [0]
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[0], variable=checkbutton_var[0], command=lambda: checkbutton_changed(0)))
    checkbutton[0].grid(row=0, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[1], variable=checkbutton_var[1], command=lambda: checkbutton_changed(1)))
    checkbutton[1].grid(row=1, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[2], variable=checkbutton_var[2], command=lambda: checkbutton_changed(2)))
    checkbutton[2].grid(row=2, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[3], variable=checkbutton_var[3], command=lambda: checkbutton_changed(3)))
    checkbutton[3].grid(row=3, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[4], variable=checkbutton_var[4], command=lambda: checkbutton_changed(4)))
    checkbutton[4].grid(row=4, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[5], variable=checkbutton_var[5], command=lambda: checkbutton_changed(5)))
    checkbutton[5].grid(row=5, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[6], variable=checkbutton_var[6], command=lambda: checkbutton_changed(6)))
    checkbutton[6].grid(row=6, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[7], variable=checkbutton_var[7], command=lambda: checkbutton_changed(7)))
    checkbutton[7].grid(row=7, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[8], variable=checkbutton_var[8], command=lambda: checkbutton_changed(8)))
    checkbutton[8].grid(row=8, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(
        ttk.Checkbutton(window, text=columns[9], variable=checkbutton_var[9], command=lambda: checkbutton_changed(9)))
    checkbutton[9].grid(row=9, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[10], variable=checkbutton_var[10],
                                       command=lambda: checkbutton_changed(10)))
    checkbutton[10].grid(row=10, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[11], variable=checkbutton_var[11],
                                       command=lambda: checkbutton_changed(11)))
    checkbutton[11].grid(row=11, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[12], variable=checkbutton_var[12],
                                       command=lambda: checkbutton_changed(12)))
    checkbutton[12].grid(row=12, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[13], variable=checkbutton_var[13],
                                       command=lambda: checkbutton_changed(13)))
    checkbutton[13].grid(row=13, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[14], variable=checkbutton_var[14],
                                       command=lambda: checkbutton_changed(14)))
    checkbutton[14].grid(row=14, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[15], variable=checkbutton_var[15],
                                       command=lambda: checkbutton_changed(15)))
    checkbutton[15].grid(row=15, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[16], variable=checkbutton_var[16],
                                       command=lambda: checkbutton_changed(16)))
    checkbutton[16].grid(row=16, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[17], variable=checkbutton_var[17],
                                       command=lambda: checkbutton_changed(17)))
    checkbutton[17].grid(row=17, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[18], variable=checkbutton_var[18],
                                       command=lambda: checkbutton_changed(18)))
    checkbutton[18].grid(row=18, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[19], variable=checkbutton_var[19],
                                       command=lambda: checkbutton_changed(19)))
    checkbutton[19].grid(row=19, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text=columns[20], variable=checkbutton_var[20],
                                       command=lambda: checkbutton_changed(20)))
    checkbutton[20].grid(row=20, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text="Naive_Bayes_Classifier_mon1", variable=checkbutton_var[21],
                                       command=lambda: checkbutton_changed(21)))
    checkbutton[21].grid(row=21, column=0)
    checkbutton_var.append(tki.IntVar())
    checkbutton.append(ttk.Checkbutton(window, text="Naive_Bayes_Classifier_mon2", variable=checkbutton_var[22],
                                       command=lambda: checkbutton_changed(22)))
    checkbutton[22].grid(row=22, column=0, sticky="nswe")
    btn1 = ttk.Button(window, text="Закончить выбор", command=click1)
    btn1.grid(row=23, column=1)


def statistic_report(data_local, var_list):
    """
    Статистический отчёт по выбранным количественным или качественным переменным
    Входные данные: база данных (pd.DataFrame()), список переменных (массив, кортеж, датафрейм и т. д.)
    Выходные данные: статистический отчёт (pd.DataFrame())
    Автор:
    """
    if var_list[0] in quantitative_variables:
        statistics = pd.DataFrame({'var_list': var_list, 'max': [data_local[i].max() for i in var_list],
                                   'min': [data_local[i].min() for i in var_list],
                                   'mean': [data_local[i].mean() for i in var_list],
                                   'sample_variance': [data_local[i].var() for i in var_list],
                                   'standard_deviation': [data_local[i].std() for i in var_list]})
        return statistics
    else:
        statistics = pd.crosstab(index=data_local[var_list[0]], columns='frequency')
        parts = pd.crosstab(index=data_local[var_list[0]], columns='percentage')
        parts = parts / parts.sum()
        statistics = pd.concat([statistics, parts], axis=1)
        return statistics


def pivot_table(data_local, x, y, z, v, func):
    """
    Создание сводной таблицы по паре выбранных качественных переменных
    Входные данные: база данных (pd.DataFrame()), первая качественная переменная (строка), вторая качественна переменная
    (строка), качественная переменная для агрегации (строка), количественная переменная для агрегации (строка), метод
    агрегации (строка)
    Выходные данные: сводная таблица (pd.DataFrame())
    Автор:
    """
    return pd.pivot_table(data_local, index=[x, y], columns=z, values=v,
                          aggfunc=func)


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
                    fig.savefig('/Users/tima/desktop/to.png')

                fig = Figure(figsize=(10, 4), dpi=100)
                ax = fig.add_subplot(111)
                x_list = pd.unique(data[combobox_1.get()])
                y_list = [sum(data[data[combobox_2.get()] == combobox_3.get()]
                              [combobox_1.get()] == x) for x in x_list]
                color = list('rbgmcyk')
                ax.grid()
                ax.bar(x_list, y_list, color=color)
                canvas_1 = FigureCanvasTkAgg(fig, master=window)
                canvas_1.draw()
                canvas_1.get_tk_widget().pack(side=tki.TOP, fill=tki.NONE, expand=0)
                btn = tki.Button(window, text='Сохранить', command=selected_4)
                btn.pack(anchor=tki.S)
                window.after(200, None)

            selection = combobox_2.get()
            a = list(data[selection].unique())
            combobox_3 = ttk.Combobox(window, values=a, state='readonly')
            combobox_3.place(x=250, y=60)
            combobox_3.bind('<<ComboboxSelected>>', selected_3)

        drop = combobox_1.get()
        combobox_2 = ttk.Combobox(window, values=[x for x in qualitative_variables if x != drop], state='readonly')
        combobox_2.place(x=20, y=60)
        combobox_2.bind('<<ComboboxSelected>>', selected_2)

    window = tki.Toplevel()
    window.title("Кластеризованная столбчатая диаграмма")
    window.geometry("500x550")
    window.resizable(False, False)
    combobox_1 = ttk.Combobox(window, values=qualitative_variables, state='readonly')
    combobox_1.place(x=20, y=30)
    combobox_1.bind('<<ComboboxSelected>>', selected_1)


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
                    fig.savefig('/Users/tima/desktop/to.png')

                fig = Figure(figsize=(10, 4), dpi=100)
                column_size = len(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()])
                s_dev = np.std(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()])
                iqr = np.subtract(*np.percentile(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()],
                                                 [75, 25]))
                min_max = max(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()]) -\
                    min(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()])
                sturges = 1 + 3.322 * np.log10(column_size)
                scott = min_max * np.power(column_size, 1 / 3) / (3.5 * s_dev)
                freedman = min_max * np.power(column_size, 1 / 3) / (2 * iqr)
                labels = ['Sturges', 'Scott', 'Freedman-Diaconis', 'Categories']
                colors = ['#3e1ca8', '#ff3442', '#00e277', '#ffe4e1']
                n_bins = list(map(round, [sturges, scott, freedman])) + [10]
                for i in range(4):
                    ax = fig.add_subplot(int('22' + str(i + 1)))
                    ax.hist(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()], bins=n_bins[i],
                            color=colors[i])
                    ax.set_title(labels[i])
                    ax.axvline(np.mean(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()]),
                               linestyle='dashed', color='black')
                canvas_1 = FigureCanvasTkAgg(fig, master=window)
                canvas_1.draw()
                canvas_1.get_tk_widget().pack(side=tki.TOP, fill=tki.NONE, expand=0)
                btn = tki.Button(window, text='Сохранить', command=selected_4)
                btn.pack(anchor=tki.S)
                window.after(200, None)

            selection = combobox_2.get()
            a = list(data[selection].unique())
            combobox_3 = ttk.Combobox(window, values=a, state='readonly')
            combobox_3.place(x=250, y=60)
            combobox_3.bind('<<ComboboxSelected>>', selected_3)

        combobox_2 = ttk.Combobox(window, values=qualitative_variables, state='readonly')
        combobox_2.place(x=20, y=60)
        combobox_2.bind('<<ComboboxSelected>>', selected_2)

    window = tki.Toplevel()
    window.title("Категоризированная гистограмма")
    window.geometry("500x550")
    window.resizable(False, False)
    combobox_1 = ttk.Combobox(window, values=quantitative_variables, state='readonly')
    combobox_1.place(x=20, y=30)
    combobox_1.bind('<<ComboboxSelected>>', selected_1)


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
                    fig.savefig('/Users/tima/desktop/to.png')

                fig = Figure(figsize=(10, 4), dpi=100)
                ax = fig.add_subplot(111)
                ax.boxplot(data[data[combobox_2.get()] == combobox_3.get()][combobox_1.get()], vert=False)
                canvas_1 = FigureCanvasTkAgg(fig, master=window)
                canvas_1.draw()
                canvas_1.get_tk_widget().pack(side=tki.TOP, fill=tki.NONE, expand=0)
                btn = tki.Button(window, text='Сохранить', command=selected_4)
                btn.pack(anchor=tki.S)
                window.after(200, None)

            selection = combobox_2.get()
            a = list(data[selection].unique())
            combobox_3 = ttk.Combobox(window, values=a, state='readonly')
            combobox_3.place(x=250, y=60)
            combobox_3.bind('<<ComboboxSelected>>', selected_3)

        combobox_2 = ttk.Combobox(window, values=qualitative_variables, state='readonly')
        combobox_2.place(x=20, y=60)
        combobox_2.bind('<<ComboboxSelected>>', selected_2)

    window = tki.Toplevel()
    window.title("Категоризированная диаграмма Бокса-Вискера")
    window.geometry("500x550")
    window.resizable(False, False)
    combobox_1 = ttk.Combobox(window, values=quantitative_variables, state='readonly')
    combobox_1.place(x=20, y=30)
    combobox_1.bind('<<ComboboxSelected>>', selected_1)


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
                        fig.savefig('/Users/tima/desktop/to.png')

                    fig = Figure(figsize=(10, 4), dpi=100)
                    ax = fig.add_subplot(111)
                    x_list = data[data[combobox_3.get()] == combobox_4.get()][combobox_1.get()]
                    y_list = data[data[combobox_3.get()] == combobox_4.get()][combobox_2.get()]
                    ax.scatter(x_list, y_list, s=1)
                    canvas_1 = FigureCanvasTkAgg(fig, master=window)
                    canvas_1.draw()
                    canvas_1.get_tk_widget().pack(side=tki.TOP, fill=tki.NONE, expand=0)
                    btn = tki.Button(window, text='Сохранить', command=selected_5)
                    btn.pack(anchor=tki.S)
                    window.after(200, None)

                selection = combobox_3.get()
                a = list(data[selection].unique())
                combobox_4 = ttk.Combobox(window, values=a, state='readonly')
                combobox_4.place(x=250, y=90)
                combobox_4.bind('<<ComboboxSelected>>', selected_4)

            combobox_3 = ttk.Combobox(window, values=qualitative_variables, state='readonly')
            combobox_3.place(x=20, y=90)
            combobox_3.bind('<<ComboboxSelected>>', selected_3)

        drop = combobox_1.get()
        combobox_2 = ttk.Combobox(window, values=[x for x in quantitative_variables if x != drop], state='readonly')
        combobox_2.place(x=20, y=60)
        combobox_2.bind('<<ComboboxSelected>>', selected_2)

    window = tki.Toplevel()
    window.title("Категоризированная диаграмма рассеивания")
    window.geometry("500x550")
    window.resizable(False, False)
    combobox_1 = ttk.Combobox(window, values=quantitative_variables, state='readonly')
    combobox_1.place(x=20, y=30)
    combobox_1.bind('<<ComboboxSelected>>', selected_1)


def interface():
    """
    Интерфейс программы
    Входные данные: нет
    Выходные данные: нет
    Автор:
    """
    root = tki.Tk()
    root.title('Приложение для анализа данных кредитных историй заёмщиков')
    root.geometry('600x250')
    root.minsize(300, 200)
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
    graphic_menu = tki.Menu(tearoff=0)
    graphic_menu.add_command(label='Кластеризованная столбчатая диаграмма', command=clustered_bar_chart)
    graphic_menu.add_command(label='Категоризированная гистограмма', command=categorized_bar_chart)
    graphic_menu.add_command(label='Категоризированная диаграмма Бокса-Вискера', command=box_and_whiskers_chart)
    graphic_menu.add_command(label='Категоризированная диаграмма рассеивания', command=scatter_chart)
    menu.add_cascade(label="Файл", menu=file_menu)
    menu.add_cascade(label="Отчёт", menu=report_menu)
    menu.add_cascade(label="Графические отчёты", menu=graphic_menu)
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


file = 'Analysing_demographic_data_of_customers_with_credit_history/BankChurners.csv'
data = read_from_text_file(file)
data_columns = data.columns
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
                         'Marital_Status', 'Income_Category', 'Card_Category']
quantitative_variables = ['Customer_Age', 'Dependent_count', 'Months_on_book',
                          'Total_Relationship_Count', 'Months_Inactive_12_mon',
                          'Contacts_Count_12_mon', 'Credit_Limit',
                          'Total_Revolving_Bal', 'Avg_Open_To_Buy',
                          'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt',
                          'Total_Trans_Ct', 'Total_Ct_Chng_Q4_Q1',
                          'Avg_Utilization_Ratio']

interface()
