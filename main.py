#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data analysis project v 1.4
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tki
import tkinter.ttk as ttk


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


def save_to_excel(data_local, file_name):
    """
    Функция сохраняет базу данных в файл .xlsx
    Входные данные: датафрейм с базой данных (pd.DataFrame()), имя файла (строка)
    Выходные данные: нет
    Автор:
    """
    path = './output/' + file_name + '.xlsx'
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


def report_generation(data_local):
    """
    Создание отчета на основе базы данных

    Входные параметры:
    база данных data_local

    Внутри функции происходит ввод следующих переменных:
    num_of_cons (количество условий)
    column (название столбца, в котором находится условие)
    condition (название условия)
    num_of_col (количество столбцов, которые будут в отчёте)
    column_report (название столбца, который будет в отчёте)
    report (название отчёта)

    Возвращает:
    W1 (новая база данных, содержащая num_of_cons столбцов, отсортированных по условиям)
    Сохраняет файл с названием, которое задаёт пользователь, в формате .xlsx в папку, где находится программа
    """
    num_of_cons = 0
    num_of_col = 0
    sel = True
    report_columns = []
    while num_of_cons <= 0 or num_of_cons > 21:
        print('Введите количество условий:')
        num_of_cons = int(input())
    for i in range(num_of_cons):
        print('Введите название столбца, в котором находится', i + 1, 'условие:')
        column = input()
        print('Введите название', i + 1, 'условия:')
        condition = input()
        if column in int_columns:
            condition = np.int64(condition)
        if column in float_columns:
            condition = np.float64(condition)
        sel = sel & (data_local[column] == condition)
    while num_of_col <= 0 or num_of_col > 21:
        print('Введите количество столбцов, которые будут в отчёте:')
        num_of_col = int(input())
    for i in range(num_of_col):
        print('Введите название', i + 1, 'столбца, который будет в отчёте:')
        column_report = input()
        report_columns.append(column_report)
    print('Введите название отчёта: ')
    report = input()
    w1 = data_local.loc[sel, report_columns]
    save_to_excel(w1, report)
    return w1


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
columns = data.columns
int_columns = []
string_columns = []
float_columns = []
for i in range(len(columns)):
    if isinstance(data.iloc[1, i], str):
        string_columns.append(columns[i])
    elif isinstance(data.iloc[1, i], np.float64):
        float_columns.append(columns[i])
    else:
        int_columns.append(columns[i])
