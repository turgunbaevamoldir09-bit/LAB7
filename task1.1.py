import pandas as pd
import numpy as np

# Файлды оқу
df = pd.read_csv("2023-05-12_2023-06-12_client_login.csv", sep=';')

# Әр жол – жеке клиент
df['customer_id'] = df.index + 1

# amount (LAB1-де шығыс минус болуы тиіс)
df['amount'] = -df['Расход (руб.)'].astype(str).str.replace(',', '.').astype(float)

# tr_datetime = Дата
df['tr_datetime'] = df['Дата']

# tr_type = Тип устройства
df['tr_type'] = df['Тип устройства']

# mcc_code = Регион таргетинга (код болмағандықтан, hash)
df['mcc_code'] = df['Регион таргетинга'].astype(str).apply(lambda x: abs(hash(x)) % 10000)

# term_id = Кампания (код)
df['term_id'] = df['Кампания'].astype(str).apply(lambda x: abs(hash(x)) % 100000)

# gender түрлендіру (мужской = 1, женский = 0, не определен = -1)
df['gender'] = df['Пол'].map({
    'мужской': 1,
    'женский': 0,
    'не определен': -1
})

df.head()
