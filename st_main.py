import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import time
import uuid
from clean_up import  cleanup_all_temp_data
import os

# st.markdown(
#     """
#     <style>
#     /* Скрыть сам сайдбар */
#     [data-testid="stSidebar"] {display: none !important;}
#     /* Скрыть кнопку открытия сайдбара */
#     [data-testid="stSidebarCollapseControl"] {display: none !important;}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Генерируем уникальный идентификатор для сессии (один раз)
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())

#TODO ВРЕМЕННОЕ ХРАНЕНИЕ Seeion id - DELETE
with open('session_id.txt', 'w') as f:
    f.write(st.session_state['session_id'])

session_id = st.session_state['session_id']
# Для отладки — выводим session_state
st.success(session_id)



st.markdown("## Main page")


disable_data_processing = st.session_state.get('disable_data_processing', True)
disable_data_processing = False # TODO Удалить в финальной версии
            # (Разрешает без загрузки таблиц открывать Сводные данные (02_Summary_Data.py)


st.page_link("st_main.py", label="Home", icon="🏠")
st.page_link("pages/01_Load_Files.py", label="Загрузка файлов", icon="1️⃣")
st.page_link("pages/02_Summary_Data.py", label="Сводные данные", icon="2️⃣", disabled=disable_data_processing)
st.page_link("http://www.google.com", label="Google", icon="🌎")

sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

print(selected)

left, right = st.columns(2)

if left.button("Do it!✅", use_container_width=True):
    print(1)
    left.markdown("### Value button")

if right.button("Not do it!❌", use_container_width=True):
    print("remove all data")
    cleanup_all_temp_data()
    right.success("All files been removed ❌")

st.divider()



