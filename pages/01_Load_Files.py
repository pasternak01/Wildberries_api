import pandas as pd
import streamlit as st
import os
from clean_up import cleanup_session_files


def get_ext(file_name: str):
    # получаем расширение загруженного файла для записи его
    _, ext = os.path.splitext(file_name)
    return ext.lstrip('.')


session_id = st.session_state['session_id']


st.header('Загрузка Файлов')
st.divider()
st.markdown("## TODO LIST:\n"
            "* [ ] сделать проверку загруженных файлов\n"
            "* [ ] указать то, что названия фалов должны содержать только латиницу\n"
            "* [ ] удалить TODO markdown блок")

st.divider()
# =====================================================================
# Удалить все файлы сессии
if st.button("Очистить файлы сессии"):
    cleanup_session_files(session_id)
    st.success("Файлы текущей сессии удалены.")

st.divider()
# =====================================================================
st.markdown("### 1. Финансовый отчет Wildberries")
st.markdown("**Загрузите файл с финансовым отчетом скачанным из личного кабинета Wildberries**")
#TODO Добавить справку как скачивать отчет
# Загрузка файла с фин отчетом
fin_data_file = st.file_uploader("Выберите файл для загрузки",
                                 type=["xlsx", "xls", "csv"],
                                 accept_multiple_files=False,
                                 key="fin_data_file")


# Папка для сохранения файлов
UPLOAD_DIR = os.path.join(os.getcwd(), "uploaded_files")
os.makedirs(UPLOAD_DIR, exist_ok=True)

fin_data_path = None
if fin_data_file is not None:
    ext = get_ext(fin_data_file.name)
    # Используем session_id в имени файла
    fin_data_path = os.path.join(UPLOAD_DIR, f'fin_data_file_{session_id}.{ext}')
    with open(fin_data_path, "wb") as f:
        f.write(fin_data_file.getbuffer())
    st.success(f"Файл '{fin_data_file.name}' успешно загружен и сохранён.")

    # Здесь можно добавить обработку файла
print(session_id)
if os.path.exists(os.path.join(UPLOAD_DIR, f'fin_data_file_{session_id}.xlsx')):
    st.success("✅ Файл текущей сессии загружен")
st.divider()
# =====================================================================

# Загрузка файла с себестоимостью
st.markdown("### 2. Загрузка файла с себестоимостью ")
st.markdown("**Загрузите файл с финансовым отчетом скачанным из личного кабинета Wildberries**")
st.markdown("Как должна выглядеть таблица:\n"
            "* в таблице должно быть 3 столбца\n"
            "* должна быть первая строка с названиями (могут быть любыми - называться по-разному)\n"
            "* столбцы должны располагаться **именно** в таком порядке")
#TODO Добавить справку как скачивать отчет

st.dataframe(pd.DataFrame({'Наименование': ['товар_1', 'товар_2'],
                       'Barcode': ["445646464654", "35644646464"],
                           "Цена" : [225.250, 500.00]}
                      ).reset_index(drop=True), hide_index=True )

cost_data_file = st.file_uploader("Выберите файл для загрузки",
                                  type=["xlsx", "xls", "csv"],
                                  accept_multiple_files=False,
                                  key="cost_data_file")

cost_data_path = None
if cost_data_file is not None:
    ext = get_ext(cost_data_file.name)
    # Используем session_id в имени файла
    cost_data_path = os.path.join(UPLOAD_DIR, f'cost_data_file_{session_id}.{ext}')
    
    with open(cost_data_path, "wb") as f:
        f.write(cost_data_file.getbuffer())
    st.success(f"Файл '{cost_data_file.name}' успешно загружен и сохранён.")

    # проверяем файл на Nan выдаем результат
    from src.session_utils import cost_detect
    cost_errors = cost_detect(pd.read_excel(cost_data_file))
    print(cost_errors[0])
    if cost_errors[0] > 0:
        st.warning(f'В таблице есть пропущеные значения! Количество: {cost_errors[0]}')
        st.dataframe(cost_errors[1])

if os.path.exists(os.path.join(UPLOAD_DIR, f'cost_data_file_{session_id}.xlsx')):
    st.success("✅ Файл текущей сессии загружен")

st.divider()
# =====================================================================

# Передаем данные по проекту
disable_data_processing = True
if fin_data_path is not None and cost_data_path is not None:
    disable_data_processing = False
    st.session_state['cost_data_file_path'] = cost_data_path
    st.session_state['fin_data_file_path'] = fin_data_path
# чтобы кнопки не были актины пока не загружены файлы
st.session_state['disable_data_processing'] = disable_data_processing
