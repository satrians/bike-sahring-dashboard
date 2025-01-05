import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import streamlit.components.v1 as components
sns.set(style='dark')

data = pd.read_csv('D:\portfolio\Proyek Analisis Data\Dashboard\data.csv')

# Menambahkan kolom latitude dan longitude sintetis
np.random.seed(42)  # Seed untuk konsistensi
data['latitude'] = np.random.uniform(low=37.77, high=37.78, size=len(data))
data['longitude'] = np.random.uniform(low=-122.42, high=-122.41, size=len(data))

st.title('Bike Sharing Data Analysis Dashboard')

# menampilkan informasi dataset
st.subheader('Data Information')
st.write(data.head())

# Grafik Penyewaan Sepeda per Bulan
st.subheader("Penyewaan Sepeda per Bulan")
monthly_rentals = data.groupby('hr')['cnt_hour'].sum()
st.bar_chart(monthly_rentals)

# Grafik Penyewaan Sepeda Berdasarkan Cuaca
st.subheader("Penyewaan Sepeda Berdasarkan Cuaca")
weather_rentals = data.groupby('weather_labels')['cnt_day'].mean()
st.bar_chart(weather_rentals)

# Menampilkan peta (jika ada data geospasial)
import folium
from folium.plugins import HeatMap
import streamlit_folium as st_folium

# Interactive filter for holiday
holiday_filter = st.selectbox("Pilih Hari Libur", options=data['holiday_day'].unique(), format_func=lambda x: "Libur" if x == 1 else "Tidak Libur")

# Filter data based on holiday
filtered_data = data[data['holiday_day'] == holiday_filter]

# Display filtered data
st.write(f"Data untuk {'Libur' if holiday_filter == 1 else 'Tidak Libur'}")
st.write(filtered_data)

# Bar plot for rentals based on holiday
st.subheader('Rata-rata Sewaan Berdasarkan Hari Libur Nasional')
average_holiday = data.groupby('holiday_day')['cnt_day'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='holiday_day', y='cnt_day', data=average_holiday, palette='Set2', dodge=False, ax=ax)
ax.set_title('Rata-rata Sewaan Berdasarkan Hari Libur Nasional')
ax.set_xlabel('Hari Libur')
ax.set_ylabel('Rata-rata Sewaan')
ax.set_xticklabels(['Tidak Libur', 'Libur'])
st.pyplot(fig)

# Interactive filter for month
month_filter = st.selectbox("Pilih Bulan", options=data['mnth_hour'].unique(), format_func=lambda x: f"Bulan {x}")

# Filter data based on month
filtered_data = data[data['mnth_hour'] == month_filter]

# Display filtered data
st.write(f"Data untuk Bulan {month_filter}")
st.write(filtered_data)

# Map visualization for rental distribution
st.subheader("Distribusi Penyewaan Sepeda")
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)
HeatMap(filtered_data[['latitude', 'longitude', 'cnt_day']].dropna()).add_to(m)
st.write(m)

# jalankan Folium map to HTML dan menampilkan visual di streamlit
map_html = m._repr_html_()
components.html(map_html, height=600)