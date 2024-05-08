import streamlit as st
import numpy as np

aperture = st.number_input('Aperture', min_value = 1.0, max_value = 22.0, value = 2.0)
shutter = 1/st.number_input('1/Shutter Speed', min_value = 0.1, max_value = 16000.0, value = 60.0)
iso = st.number_input('ISO', min_value=50, max_value=1000000, value = 200)
exposure = np.log2(aperture ** 2) - np.log2(shutter * iso * 0.01)
st.write(f'Exposure = {exposure.round(3)}')