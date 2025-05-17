import streamlit as st
import numpy as np
import pandas as pd

df = pd.read_excel('Temp/Docs/13-19.05.xlsx', index_col="№")
print(len(df))

columns_to_drop_by_WB_recommendation = [
    'Вайлдберриз реализовал Товар (Пр)',
    'Скидка постоянного Покупателя (СПП), %',
    'Размер снижения кВВ из-за рейтинга, %',
    'Размер снижения кВВ из-за акции, %',
    'Размер  кВВ без НДС, % Базовый',
    'Итоговый кВВ без НДС, %',
    'Вознаграждение с продаж до вычета услуг поверенного, без НДС',
    'Возмещение за выдачу и возврат товаров на ПВЗ',
    'Вознаграждение Вайлдберриз (ВВ), без НДС', 'НДС с Вознаграждения Вайлдберриз',
    'Возмещение издержек по перевозке/по складским операциям с товаром',
    'Наименование банка-эквайера',
    'Номер офиса',
    'Наименование офиса доставки',
    'ИНН партнера',
    'Партнер'
]

custom_columns_to_drop = [
    'Бренд',
    'Согласованный продуктовый дисконт, %',
    'Промокод %',
    'Итоговая согласованная скидка, %',
    'Цена розничная с учетом согласованной скидки',
    'Дата начала действия фиксации',
    'Дата конца действия фиксации',
    'Признак услуги платной доставки',
    'Стикер МП',
    'Номер таможенной декларации',
    'Номер сборочного задания',
    'Код маркировки',
    'Организатор перевозки',
    'Удержания',
    'Фиксированный коэффициент склада по поставке',
    'Признак продажи юридическому лицу',
    'Номер короба для платной приемки'
]
print(len(columns_to_drop_by_WB_recommendation+ custom_columns_to_drop))

df = df.drop(columns=columns_to_drop_by_WB_recommendation + custom_columns_to_drop)


english_columns = [
    "Supply_Number",                            # Номер_поставки
    "Item_type",                                # Предмет
    "Code",                                     # Код_номенклатуры
    "Supplier_Article",                         # Артикул_поставщика
    "Name",                                     # Название
    "Size",                                     # Размер
    "Barcode",                                  # Баркод
    "Document_Type",                            # Тип_документа
    "Payment_Justification",                    # Обоснование_для_оплаты
    "Buyer_Order_Date",                         # Дата_заказа_покупателем
    "Sale_Date",                                # Дата_продажи
    "Quantity",                                 # Кол-во
    "Retail_Price",                             # Цена_розничная
    "KVV_Percent",                              # Размер_кВВ,_%
    "Acquiring_Payment_Commission",             # Эквайринг/Комиссии_за_организацию_платежей
    "Acquiring_Payment_Commission_Percent",     # Размер_комиссии_за_эквайринг/Комиссии_за_организацию_платежей,_%
    "Acquiring_Payment_Type",                   # Тип_платежа_за_Эквайринг/Комиссии_за_организацию_платежей
    "Amount_To_Seller",                         # К_перечислению_Продавцу_за_реализованный_Товар
    "Number_of_Deliveries",                     # Количество_доставок
    "Number_of_Returns",                        # Количество_возврата
    "Delivery_Services",                        # Услуги_по_доставке_товара_покупателю
    "Total_Fines",                              # Общая_сумма_штрафов
    "Extra_Payments",                           # Доплаты
    "Types_of_Logistics_Fines_and_Extra_Payments",  # Виды_логистики,_штрафов_и_доплат
    "Warehouse",                                # Склад
    "Country",                                  # Страна
    "Box_Type",                                 # Тип_коробов
    "Scan_Code",                                # ШК
    "Srid",                                     # Srid
    "Storage",                                  # Хранение
    "Paid_Acceptance"                           # Платная_приемка
]

columns_dict = {}
for column_ru, column_eng in zip(df.columns, english_columns):
    print(f'{column_eng.lower()} - {column_ru}')
    df = df.rename(columns={column_ru : column_eng.lower()})
    columns_dict[column_eng] = column_ru

df['wb_commision_in_rub'] = (df.retail_price * (df.kvv_percent / 100)).round(2)

df1 = df[['payment_justification', 'sale_date', 'quantity', 'wb_commision_in_rub', 'retail_price', 'kvv_percent', 'acquiring_payment_commission', 'amount_to_seller', 'delivery_services']]


table_summary = df1.groupby(['quantity', "payment_justification"]).agg(qty_operations=('payment_justification', 'count'),total_price=('retail_price', 'sum'), wb_comission_rub=('wb_commision_in_rub', 'sum'),acquring_sum=('acquiring_payment_commission', 'sum'), delivery_sum=('delivery_services', 'sum'), seller_profit=("amount_to_seller" , 'sum'))


table_summary.loc['Итого'] = table_summary.sum(numeric_only=True)


# Преобразование DataFrame в HTML таблицу
html_table = table_summary.to_html()

# Вывод HTML таблицы в Streamlit (позволяет использовать HTML)
st.markdown(html_table, unsafe_allow_html=True)


# st.map(map_data)
st.write("Hello Woooorld!")