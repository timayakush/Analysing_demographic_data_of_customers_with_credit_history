"""
Data analysis project v 1.0
"""
import pandas as pd
import matplotlib.pyplot as plt


def gender_to_churn_rate(data_local):
    """
    bar graph gender->churn rate
    """
    x_list = pd.unique(data_local['Gender'])
    y_list = [sum(data_local[data_local["Attrition_Flag"] == "Attrited Customer"]
                  ['Gender'] == x) for x in x_list]
    plt.bar(x_list, y_list)
    plt.show()


def marital_status_to_churn_rate(data_local):
    """
    bar graph marital status->churn rate
    """
    x_list = pd.unique(data_local['Marital_Status'])
    y_list = [sum(data_local[data_local["Attrition_Flag"] == "Attrited Customer"]
                  ['Marital_Status'] == x) for x in x_list]
    plt.bar(x_list, y_list)
    plt.show()


def income_category_to_churn_rate(data_local):
    """
    bar graph income category->churn rate
    """
    x_list = pd.unique(data_local['Income_Category'])
    y_list = [sum(data_local[data_local["Attrition_Flag"] == "Attrited Customer"]
                  ['Income_Category'] == x) for x in x_list]
    plt.figure(figsize=(15, 10))
    plt.bar(x_list, y_list)
    plt.show()


def education_level_to_churn_rate(data_local):
    """
    bar graph education level->churn rate
    """
    x_list = pd.unique(data_local['Education_Level'])
    y_list = [sum(data_local[data_local["Attrition_Flag"] == "Attrited Customer"]
                  ['Education_Level'] == x) for x in x_list]
    plt.figure(figsize=(15, 10))
    plt.bar(x_list, y_list)
    plt.show()


data = pd.read_csv("BankChurners.csv")
gender_to_churn_rate(data)
marital_status_to_churn_rate(data)
income_category_to_churn_rate(data)
education_level_to_churn_rate(data)
