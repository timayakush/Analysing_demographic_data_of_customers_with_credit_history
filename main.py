#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data analysis project v 1.0
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def parser(file_name):
    data_local = pd.read_csv(file_name)
    return data_local


def save_to_excel(data_local):
    path = './output/' + input() + '.xlsx'
    data_local.to_excel(path, index=False)


def adding_entities(data_local):
    temp = []
    for i in range(len(list(data_local))):
        temp.append(input())
    data_local.loc[len(data_local.index)] = temp
    return data_local


def deleting_entities(data_local, drop_index):
    return data_local.drop(index=drop_index)


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
    SEL = True
    report_columns = []
    while (num_of_cons <= 0 or num_of_cons > 21):
        print('Введите количество условий:')
        num_of_cons = int(input())
    for i in range(num_of_cons):
        print('Введите название столбца, в котором находится', i + 1, 'условие:')
        column = input()
        print('Введите название', i + 1, 'условия:')
        condition = input()
        if (column in int_columns):
            condition = np.int64(condition)
        if (column in float_columns):
            condition = np.float64(condition)
        SEL = SEL & (data_local[column] == condition)
    while (num_of_col <= 0 or num_of_col > 21):
        print('Введите количество столбцов, которые будут в отчёте:')
        num_of_col = int(input())
    for i in range(num_of_col):
        print('Введите название', i + 1, 'столбца, который будет в отчёте:')
        column_report = input()
        report_columns.append(column_report)
    print('Введите название отчёта: ')
    report = input()
    W1 = data_local.loc[SEL, report_columns]
    PTH1 = "./" + report + ".xlsx"
    W1.to_excel(PTH1, index=False)
    return W1


def statictic_report(data_local, var_list):
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
    input: x, y, z - qualitative; v - quantitative
    possible aggfunc values = 'count', 'mean'
    """
    return pd.pivot_table(data_local, index=[x, y], columns=z, values=v,
                          aggfunc=func)


def clustered_bar_chart(data_local, x_local, y):
    """
    Creates a clustered bar chart based on a user-entered metric and side
    condition

    input: dataframe (dataframe), metric (string), condition (list/numpy array/
                                                              dataframe/tuple)

    author: Timofey Yaksuhev
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
    Creates a categorized bar chart based on a user-entered metric and side
    condition

    input: dataframe (pd), metric (string), condition (list/numpy array/
                                                       dataframe/tuple)

    author: Timofey Yaksuhev
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
    Creates a box-and-whiskers chart based on a user-entered metrics and group factor

    input: dataframe (pd), metric (string), group factor (string)

    author: Polina Tatarinova
    """
    data_local.boxplot(x, by=y, vert=False)


def scatter_chart(data_local, x, y, z):
    """
    Creates a scatter chart based on two user-entered metrics and side condition

    input: dataframe (pd), metric_1 (string), metric_2 (string), condition
    (list/numpy array/dataframe/tuple)

    author: Polina Tatarinova
    """
    x_list = data_local[data_local[z[0]] == z[1]][x]
    y_list = data_local[data_local[z[0]] == z[1]][y]
    plt.xlabel(x)
    plt.ylabel(y)
    plt.scatter(x_list, y_list, s=1)
    plt.show()


file = 'BankChurners.csv'
data = parser(file)
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
