import streamlit as st, pandas as pd


sensors = dict(pd.read_csv('pages/Sensor_Sizes.csv').values)
focal_length = st.number_input('Focal Length', value = 50)
aperture = st.number_input('Aperture', value = 2.0)
iso = st.number_input('ISO', value = 100)
sensor = st.selectbox('Sensor Size', list(sensors.keys()))
image_diagonal = sensors[sensor]

selected = pd.DataFrame([{'Focal Length': focal_length, 'Aperture': aperture, 'ISO': iso}]).T
df = pd.DataFrame()
for sensor_temp, diagonal in sensors.items():
    df[sensor_temp] = selected * (diagonal / image_diagonal)
st.dataframe(df.round(1).T)