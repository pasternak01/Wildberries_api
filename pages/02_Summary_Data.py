import pandas as pd
import streamlit as st
import os

from IPython.core.pylabtools import figsize
from matplotlib.pyplot import title

from src.processing import *
from matplotlib import pyplot as plt

session_id = st.session_state['session_id']

df = ["no df"]
# загрузка в DataFrame файлов
# Фин отчет
fin_file_path = f"uploaded_files/fin_data_file_{session_id}.xlsx"
if os.path.exists(fin_file_path):
    fin_df = pd.read_excel(fin_file_path, index_col="№")
    fin_df = columns_del_and_rename(fin_df)
    fin_df[['buyer_order_date', 'sale_date']] = fin_df[['buyer_order_date', 'sale_date']].apply(pd.to_datetime)
else:
    st.warning("Файл файл финансового отчета не найден. Пожалуйста, загрузите файл на соответствующей странице.")
# файл с ценами
cost_file_path = f"uploaded_files/cost_data_file_{session_id}.xlsx"
if os.path.exists(cost_file_path):
    cost_df = pd.read_excel(cost_file_path)
    cost_df.columns = ['item', 'barcode', 'item_cost']
else:
    st.warning("Файл себестоимости не найден. Пожалуйста, загрузите файл на соответствующей странице.")

# Объединение по столбцу 'Barcode'
try:
    df = pd.merge(fin_df, cost_df[['barcode', 'item_cost']], on='barcode', how='left')

except Exception as e:

    st.warning("Что-то не так с файлами")
    st.error(e)

# Освобождаем память
del fin_df
del cost_df

# ========================= Сводные данные ============================
min_date = df.loc[df['payment_justification'] == "Хранение", "sale_date"].min().strftime("%d %b %Y")
max_date = df.loc[df['payment_justification'] == "Хранение", "sale_date"].max().strftime("%d %b %Y")
st.markdown(f'''## Отчёт за период: {min_date} - {max_date}''')
st.divider()

col1, col2, col3 = st.columns(3)
#|---Col1---|
with col1:
    logistics = f"{df['delivery_services'].sum().round(2):,.2f}".replace(',', ' ')
    storage = f"{df['storage'].sum().round(2):,.2f}".replace(',', ' ')
    fines = f"{df['total_fines'].sum().round(2):,.2f}".replace(",", ' ')
    st.markdown("## Расходы")
    st.markdown(f"#### Логистика:\n"
                f"#### {logistics} руб.")
    st.markdown(f"#### Хранение: {storage} руб.")
    st.markdown(f"#### Штрафы: {fines} руб.")

#|---Col2---|
with col2:
    st.markdown("#### COL2")
#|---Col3---|
with col3:
    st.markdown("#### COL3")

# =====================================================================================================================
