
import pandas as pd
import streamlit as st
from datetime import datetime

def parse_date(date_str):
    if len(date_str.split('/')) == 2:  # mm/yyyy format
        return datetime.strptime(f"01/{date_str}", "%d/%m/%Y")
    else:  # dd/mm/yyyy format
        return datetime.strptime(date_str, "%d/%m/%Y")

def calculate_man_months(start_date, end_date):
    delta = end_date - start_date
    return round(delta.days / 30, 1)

def merge_periods(periods):
    merged = []
    for start, end in sorted(periods):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

def process_excel(file):
    df = pd.read_excel(file, engine='openpyxl')
    man_months = []
    for index, row in df.iterrows():
        periods = row.dropna()
        period_list = []
        for period in periods:
            start_date, end_date = period.split('-')
            start_date = parse_date(start_date.strip())
            end_date = parse_date(end_date.strip())
            period_list.append([start_date, end_date])
        merged_periods = merge_periods(period_list)
        total_man_months = sum(calculate_man_months(start, end) for start, end in merged_periods)
        man_months.append(total_man_months)
    df['Ανθρωπομήνες'] = man_months
    df.loc['Σύνολο'] = df.sum(numeric_only=True)
    return df

st.title('Υπολογισμός Ανθρωπομηνών από Excel')
uploaded_file = st.file_uploader("Ανέβασε αρχείο Excel", type=["xlsx"])

if uploaded_file is not None:
    processed_df = process_excel(uploaded_file)
    st.write(processed_df)
    processed_df.to_excel("processed_file.xlsx", index=False)
    st.download_button(label="Κατέβασε το νέο αρχείο", data=open("processed_file.xlsx", "rb"), file_name="processed_file.xlsx")
