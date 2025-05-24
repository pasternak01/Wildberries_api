import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

from src.config import columns_eng_ru_dict


def columns_eng_to_rus(eng_cols : list):
    """
    Для красоты отображения в таблицах приложения,
     меняем англ. названия колонок на русский
    :param eng_cols: Колонки датафрейма df.columns
    :return: Заменяем на Русские названия и меняем _ на пробел
    """
    return [columns_eng_ru_dict[col].replace("_", " ") for col in eng_cols]

def columns_del_and_rename(df:pd.DataFrame):
    """
    ТОЛЬКО ДЛЯ ФИН ОТЧЕТА ВАЙЛДБЕРРИЗ
    Функция удаляет из входящего датафрейма с финотчетом WB лишние колонки
    и переименовывает их на английский язык для удобства работы с Датафреймом
    Словарь с названиями колонок находится в src/config.py
    :param df: fin.df  - Финансовый датафрейм Wildberries
    :return: готовый к обработке датафорейм
    """
# Удаление лишних колонок из Фин отчета датасета
    df.columns = [i.replace(" ", "_") for i in df.columns] #заменяем пробелы на _ как в config.py
    eng_dict = columns_eng_ru_dict #Согласованые колонки которые решили оставить
    col_to_drop_list = []
    for n, i in enumerate(df.columns):
        if i not in eng_dict.values():
            print(f"❌ {n}. {i.replace("_", " ")}")
            col_to_drop_list.append(i) # составляется список колонок к удалению не согласованых в config.py
        else:
            print(f"✅ {n}. {i.replace("_", " ")}")
    print(col_to_drop_list)
    df = df.drop(columns=col_to_drop_list)
    df.columns = eng_dict.keys()
    return df




def return_goods_data(df: pd.DataFrame):
    """принимает датафрейм отдает датафрейм по возвратам
    JUPITER - 2.3.1"""
    df = df[df["number_of_returns"] > 0].groupby(["item_type", "name"])[
        ["number_of_returns", "delivery_services"]
    ].sum().sort_values(by="number_of_returns",ascending=False).reset_index()
    return df