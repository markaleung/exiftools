import streamlit as st, pandas as pd

sensors = dict(pd.read_csv('pages/Sensor_Sizes.csv').values)
f2 = st.number_input('Real life distance from object (mm)', value = 4035.0)
o2 = st.number_input('Real life object size (mm)', value = 815.0)
o3 = st.number_input('Photo object size (mm)', value = 34.0)
d3 = st.number_input('Photo image diagonal (mm)', value = 298.0)
sensor = st.selectbox('Sensor Size', list(sensors.keys()))
d1 = sensors[sensor]

f1 = (d1 * f2 * o3) / (o2 * d3)
st.write(f'Your lens has a focal length of {round(f1, 2)}mm')