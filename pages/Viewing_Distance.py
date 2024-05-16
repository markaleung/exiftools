import streamlit as st, numpy as np, pandas as pd

sensors = dict(pd.read_csv('pages/Sensor_Sizes.csv').values)
class DistanceCalculator:
    def __init__(self):
        self.viewing_distance = 1.3
        self.image_diagonal = 1.0
        self.pixels_per_degree = 60
        self.sensor = 'Micro Four Thirds'
    def _calculate_viewing_ratio(self):
        self.viewing_ratio = self.viewing_distance / self.image_diagonal
        self.viewing_ratio_reverse = 1 / self.viewing_ratio
    def _calculate_megapixels(self):
        self.degrees_diagonal = 2 * np.degrees(np.arctan(self.viewing_ratio_reverse/2))
        self.pixel_diagonal = self.degrees_diagonal * self.pixels_per_degree
        self.pixel_horizontal = self.pixel_diagonal * 4/5
        self.pixel_vertical = self.pixel_diagonal * 3/5
        self.megapixels = self.pixel_horizontal * self.pixel_vertical / 1000000.0
    def _calculate_for_sensor(self):
        self.sensor_diagonal = sensors[self.sensor]
        self.focal_length = self.sensor_diagonal * self.viewing_ratio
        self.pixel_size = self.sensor_diagonal * 1000 / self.pixel_diagonal
        self.min_aperture = self.pixel_size / 0.61
    def main(self):
        self._calculate_viewing_ratio()
        self._calculate_megapixels()
        self._calculate_for_sensor()

dc = DistanceCalculator()
dc.viewing_distance = st.number_input('Viewing Distance', min_value = 0.4, max_value = 130.0, value = 1.3)
dc.image_diagonal = st.number_input('Image Diagonal', min_value = 0.3, max_value=100.0, value = 1.0)
dc.main()
st.write(
f'''
- This viewing distance equals a field of view of {int(dc.degrees_diagonal)} degrees  
- For visual acuity of {dc.pixels_per_degree} pixels per degree  
- {int(dc.pixel_horizontal)} x {int(dc.pixel_vertical)} pixels, 
or {round(dc.megapixels, 2)} megapixels, are required  
'''.strip()
)

dc.sensor = st.selectbox('Sensor Size', list(sensors.keys()))
dc.main()
st.write(
f'''
On a {dc.sensor} sensor:  
- This viewing distance equals a {round(dc.focal_length, 1)} mm lens  
- And a pixel size of {round(dc.pixel_size, 2)} microns  
- This limits the narrowest aperture to {round(dc.min_aperture, 2)}  
'''.strip()
)