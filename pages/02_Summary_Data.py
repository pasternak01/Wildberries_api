import pandas as pd
import streamlit as st
import os


session_id = st.session_state['session_id']

# загрузка в DataFrame файлов
fin_file_path = f"uploaded_files/fin_data_file_{session_id}.xlsx"
if os.path.exists(fin_file_path):
    fin_df = pd.read_excel(fin_file_path)
    st.dataframe(fin_df.head(2)) #TODO Удалить?
else:
    st.warning("Файл файл финансового отчета не найден. Пожалуйста, загрузите файл на соответствующей странице.")

cost_file_path = f"uploaded_files/cost_data_file_{session_id}.xlsx"
if os.path.exists(cost_file_path):
    cost_df = pd.read_excel(cost_file_path)
else:
    st.warning("Файл себестоимости не найден. Пожалуйста, загрузите файл на соответствующей странице.")

st.markdown("## Сводные данные")
st.divider()
st.markdown("""## TODO LIST:
* [ ] Сделать обработку файлов
""")

st.divider()

st.markdown("### Круговые таблицы")



