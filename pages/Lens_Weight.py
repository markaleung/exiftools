import streamlit as st, pandas as pd

class LensWeight:
    def __init__(self):
        self.aperture = 5.6
        self.crop = 1.0
        self.intercept = 170.93
        self.slope = 56.247
    def _calculate_weight(self):
        self.aperture_crop = self.aperture * self.crop
        self.value = (10 / self.aperture_crop) ** 2
        self.weight = self.intercept + self.value * self.slope
    def main(self, intercept, slope):
        self.intercept = intercept
        self.slope = slope
        self._calculate_weight()

class MultiLens:
    def __init__(self):
        self.df = pd.read_csv('pages/Lens_Weight.csv')
        self.lens_weight = LensWeight()
        self.lens_weight.crop = 1
    def _calculate_weight(self):
        self.lens_weight.main(intercept = self.row['intercept'], slope = self.row['slope'])
        st.write(f'A {self.row["name"]} lens will weigh {round(self.lens_weight.weight)} grams')
    def main(self, type_):
        for self.row in self.df.query('type == @type_').to_dict(orient = 'records'):
            self._calculate_weight()

multi_lens = MultiLens()

sensors = dict(pd.read_csv('pages/Sensor_Sizes.csv').values)
sensor = st.selectbox('Sensor Size', list(sensors.keys()))
multi_lens.lens_weight.crop = sensors['Full Frame'] / sensors[sensor]

multi_lens.lens_weight.aperture = st.number_input(f'Aperture Zoom', min_value = 2.8, max_value=8.0, value = 5.6)
multi_lens.main(type_ = 'Zoom')
multi_lens.lens_weight.aperture = st.number_input(f'Aperture Prime', min_value = 1.2, max_value=2.8, value = 1.7)
multi_lens.main(type_ = 'Prime')