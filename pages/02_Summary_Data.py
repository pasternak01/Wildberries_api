import pandas as pd
import streamlit as st
import os
from src.processing import *
from matplotlib import pyplot as plt

session_id = st.session_state['session_id']

# загрузка в DataFrame файлов
# Фин отчет
fin_file_path = f"uploaded_files/fin_data_file_{session_id}.xlsx"
if os.path.exists(fin_file_path):
    fin_df = pd.read_excel(fin_file_path, index_col="№")
    fin_df = columns_del_and_rename(fin_df)
    st.dataframe(fin_df.head(2))  # TODO Удалить?
    st.markdown(f'{fin_df.columns}\n {len(fin_df.columns)}')
else:
    st.warning("Файл файл финансового отчета не найден. Пожалуйста, загрузите файл на соответствующей странице.")
# файл с ценами
cost_file_path = f"uploaded_files/cost_data_file_{session_id}.xlsx"
if os.path.exists(cost_file_path):
    cost_df = pd.read_excel(cost_file_path)
else:
    st.warning("Файл себестоимости не найден. Пожалуйста, загрузите файл на соответствующей странице.")
# ========================= Сводные данные ============================
# =====================================================================================================================

st.markdown("## Сводные данные")
st.markdown("""## TODO LIST:
* [ ] График продаж по дням
* [ ] Выручка по дням
""")
st.divider()
# =====================================================================================================================
st.markdown("""## TODO LIST:
* [ ] Сделать обработку файлов
""")

st.divider()
# =====================================================================================================================
st.markdown("### Круговые таблицы")

st.divider()
# ======================== ВОЗВРАТЫ ================================
# =====================================================================================================================
st.markdown("### Возвраты")

try:

    st.markdown(f"Количество возвратов за период: **{fin_df[fin_df["number_of_returns"] > 0].shape[0]}**")

    df = fin_df[fin_df["number_of_returns"] > 0].groupby(["item_type"])[["number_of_returns"]].sum()
except Exception as e:
    st.error(e)

# ==========ВОЗВРАТЫ ============ 2 КОЛОНКИ С ГРАФИКАМИ ======================================
col1, col2 = st.columns(2)
# |---------- КОЛОНКА 1 ---------------/
with col1:
    st.markdown('Колонка 1')
    try:
        # Для графика нужны метки и значения
        labels = [f"{idx}" for idx in df.index]

        # # #
        fig, ax = plt.subplots(figsize=(3, 3))
        wedges, texts, autotexts = ax.pie(
            df["number_of_returns"],
            labels=None,
            autopct='%1.1f%%',
            startangle=-45,
            wedgeprops=dict(width=0.4),  # для donut-эффекта
        )
        ax.legend(wedges, labels, title="Тип товара", loc="center left", bbox_to_anchor=(1, 0.5))
        ax.set_title("Доля возвратов по группам")
        st.pyplot(fig)
    except Exception as e:
        st.error(e, icon="🚨")



# Размещаем дата фрейм с информацией о возвратах

# |---------- КОЛОНКА 2 ---------------/
with col2:
    st.markdown('Колонка 2')

try:
    st.dataframe(fin_df[fin_df["number_of_returns"] > 0].groupby(["item_type", "name"])[
                     ["number_of_returns", "delivery_services"]].sum().sort_values(by="number_of_returns",
                                                                                   ascending=False)
                 )
except Exception as e:
    st.error(e)
# =====================================================================================================================
