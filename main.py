#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data analysis project v 2.0
"""
import tkinter as tki
import tkinter.ttk as ttk
from tkinter import filedialog as fld
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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
    Фукнция сохраняет построенный график в файл .png
    Входные данные: имя файла (строка)
    Выходные данные: нет
    Автор:
    """
    plt.savefig(file_name)


def adding_entities(data_local):
    """
    Функция добавляет строку со значениями, введёнными пользователем, в базу данных
    Входные данные: исходная база данных (pd.DataFrame())
    Выходные данные: новая база данных (pd.DataFrame())
    Автор:
    """
    temp = []
    columns = list(data_local)
    for i in range(len(columns)):
        if columns[i] in int_columns:
            temp.append(int(input()))
        elif columns[i] in float_columns:
            temp.append(float(input()))
        else:
            temp.append(input())
    data_local.loc[len(data_local.index)] = temp
    return data_local


def deleting_entities(data_local, drop_index):
    """
    Функция удаляет выбранную пользователем строку из базы данных
    Входные данные: исходная база данных (pd.DataFrame()), номер удаляемой строки (целое число)
    Выходные данные: новая база данных (pd.DataFrame())
    Автор:
    """
    return data_local.drop(index=drop_index)


def manual_modification(data_local, row_num, x):
    """
    Функция осуществляет ручную модификацию выбранного значения в базе данных
    Входные данные: исходная база данных (pd.DataFrame()), номер строки (целое число), название столбца (строка)
    Выходные данные: новая база данных (pd.DataFrame())
    Автор:
    """
    temp = input()
    if x in int_columns:
        data_local[x][row_num] = int(temp)
    elif x in float_columns:
        data_local[x][row_num] = float(temp)
    else:
        data_local[x][row_num] = temp
    return data_local


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
                spinbox[i] = tki.Spinbox(window, from_=min(characteristics), to=max(characteristics))
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
        sel = True
        for i in range(len(checkbutton)):
            if checkbutton_var[i].get() == 1:
                flag = 1
                if columns[i] in string_columns:
                    condition = combobox[i].get()
                elif columns[i] in int_columns:
                    condition = np.int64(spinbox[i].get())
                else:
                    condition = np.float64(spinbox[i].get())
                sel = sel & (data[columns[i]] == condition)
        if flag == 0:
            tki.messagebox.showwarning(title="Предупреждение", message="Не выбраны значения")
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
            btn2 = ttk.Button(window, text="Отфильтровать", command=lambda: click2(sel))
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
            else:
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
        statistics = data_local[var_list].describe()
        return statistics
    else:
        statistics = pd.crosstab(index=data_local[var_list[0]], columns='frequency')
        parts = pd.crosstab(index=data_local[var_list[0]], columns='percentage')
        parts = parts / parts.sum()
        statistics = pd.concat([statistics, parts], axis=1)
        return statistics


def pivot_table(data_local, x, y, z, v, func):
    """
    Создание сводной таблицы по паре выбранных качественных перменных
    Входные данные: база данных (pd.DataFrame()), первая качественная переменная (строка), вторая качественна переменная
    (строка), качественная переменная для агрегации (строка), количественная переменная для агрегации (строка), метод
    агрегации (строка)
    Выходные данные: сводная таблица (pd.DataFrame())
    Автор:
    """
    return pd.pivot_table(data_local, index=[x, y], columns=z, values=v,
                          aggfunc=func)


def clustered_bar_chart(data_local, x_local, y):
    """
    Создание кластеризованной столбчатой диаграммы для пары качественных переменных
    Входные данные: база данных (pd.DataFrame()), первая качественная переменная (строка), вторая качественная
    переменная и её значение (массив, кортеж, словарь и т. д.)
    Выходные данные: нет
    Автор:
    """
    x_list = pd.unique(data_local[x_local])
    y_list = [sum(data_local[data_local[y[0]] == y[1]]
                  [x_local] == x) for x in x_list]
    color = list('rbgmcyk')
    plt.grid()
    plt.bar(x_list, y_list, color=color)
    plt.show()


def categorized_bar_chart(data_local, x, y):
    """
    Создание категоризированной гистограммы для пары 'количественная - качественная' переменных
    Входные данные: база данных (pd.DataFrame()), количественная переменная (строка), качественная переменная и её
    значение (массив, кортеж, словарь и т. д.)
    Выходные данные: нет
    Автор:
    """
    column_size = len(data_local[data_local[y[0]] == y[1]][x])
    s_dev = np.std(data_local[data_local[y[0]] == y[1]][x])
    iqr = np.subtract(*np.percentile(data_local[data_local[y[0]] == y[1]][x], [75, 25]))
    min_max = max(data_local[data_local[y[0]] == y[1]][x]) - min(data_local[data_local[y[0]] == y[1]][x])
    sturges = 1 + 3.322 * np.log10(column_size)
    scott = min_max * np.power(column_size, 1 / 3) / (3.5 * s_dev)
    freedman = min_max * np.power(column_size, 1 / 3) / (2 * iqr)
    labels = ['Sturges', 'Scott', 'Freedman-Diaconis', 'Categories']
    colors = ['#3e1ca8', '#ff3442', '#00e277', '#ffe4e1']
    n_bins = list(map(round, [sturges, scott, freedman])) + [10]
    _, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 15))
    for i in range(4):
        ax = axes[i // 2, i % 2]
        ax.hist(data_local[data_local[y[0]] == y[1]][x], bins=n_bins[i], color=colors[i])
        ax.set_title(labels[i])
        ax.axvline(np.mean(data_local[data_local[y[0]] == y[1]][x]), linestyle='dashed', color='black')
    plt.show()


def box_and_whiskers_chart(data_local, x, y):
    """
    Создание категоризированной диаграммы Бокса-Вискера для пары 'количественная - качественная' переменных
    Входные данные: база данных (pd.DataFrame()), количественная переменная (строка), качественная переменная и её
    значение (массив, кортеж, словарь и т. д.)
    Выходные данные: нет
    Автор:
    """
    data_local.boxplot(x, by=y, vert=False)


def scatter_chart(data_local, x, y, z):
    """
    Создание категоризированной диаграммы рассеивания для пары количественных переменных и одной качественной переменной
    Входные данные: база данных (pd.DataFrame()), первая количественная переменная (строка), вторая количественная
    переменная (строка), качественная переменная и её значение (массив, кортеж, словарь и т. д.)
    Выходные данные: нет
    Автор:
    """
    x_list = data_local[data_local[z[0]] == z[1]][x]
    y_list = data_local[data_local[z[0]] == z[1]][y]
    plt.xlabel(x)
    plt.ylabel(y)
    plt.scatter(x_list, y_list, s=1)
    plt.show()


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
    menu.add_command(label="Файл")
    menu.add_command(label="Отчёт", command=data_filter)
    root.config(menu=menu)
    tree = ttk.Treeview(columns=columns, show="headings", height=500)
    for i in range(len(columns)):
        tree.heading(columns[i], text=columns[i])
    for i in range(len(data)):
        values = []
        for j in range(len(columns)):
            values.append(data.iloc[i, j])
        tree.insert("", tki.END, values=values)
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
qualitative_variables = ['Attrition_Flag', 'Gender', 'Education_Level',
                         'Marital_Status', 'Income_Category', 'Card_Category']
quantitative_variables = ['Customer_Age', 'Dependent_count', 'Months_on_book',
                          'Total_Relationship_Count', 'Months_Inactive_12_mon',
                          'Contacts_Count_12_mon', 'Credit_Limit',
                          'Total_Revolving_Bal', 'Avg_Open_To_Buy',
                          'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt',
                          'Total_Trans_Ct', 'Total_Ct_Chng_Q4_Q1',
                          'Avg_Utilization_Ratio']
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
interface()
