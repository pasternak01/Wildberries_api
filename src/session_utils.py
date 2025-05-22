import pandas as pd
from pandas import DataFrame


### Upload Data


# == Загрузка файла с ценами


def cost_detect(df:pd.DataFrame):
    cost_df_none_count = df.isnull().sum().sum()
    missing_rows = df[df.isnull().any(axis=1)]
    return cost_df_none_count, missing_rows
# проверка датафрейма на NaN