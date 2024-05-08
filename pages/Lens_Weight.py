import streamlit as st

crops = {
    'Full Frame': 43.27, 
    'APS-C': 28.29, 
    'Canon': 26.82, 
    'M43': 21.64, 
    '1"': 15.86, 
}
crops = {name: crops['Full Frame'] / value for name, value in crops.items()}
class LensWeight:
    def __init__(self):
        self.crop = CROP
    def _set_subclass_variables(self):
        pass
    def _calculate_weight(self):
        self.aperture_crop = self.aperture * crops[self.crop]
        self.slope = (10 / self.aperture_crop) ** 2
        self.weight = self.intercept + self.slope * self.coefficient
    def main(self):
        self._set_subclass_variables()
        self._calculate_weight()
        return self.weight
class Zoom(LensWeight):
    def _set_subclass_variables(self):
        self.aperture = APERTURE_ZOOM
class Z_15_30(Zoom):
    def _set_subclass_variables(self):
        super()._set_subclass_variables()
        self.intercept = 213.76
        self.coefficient = 42.846
class Z_24_70(Zoom):
    def _set_subclass_variables(self):
        super()._set_subclass_variables()
        self.intercept = 170.93
        self.coefficient = 56.247
class Z_70_300(Zoom):
    def _set_subclass_variables(self):
        super()._set_subclass_variables()
        self.intercept = 33.674
        self.coefficient = 212.92
class Prime(LensWeight):
    def _set_subclass_variables(self):
        self.aperture = APERTURE_PRIME
class P_35(Prime):
    def _set_subclass_variables(self):
        super()._set_subclass_variables()
        self.intercept = 36.746
        self.coefficient = 11.571
class P_50(Prime):
    def _set_subclass_variables(self):
        super()._set_subclass_variables()
        self.intercept = 29.106
        self.coefficient = 8.6293

CROP = st.selectbox('Crop Factor', list(crops.keys()))
APERTURE_ZOOM = st.number_input('Aperture Zoom', min_value = 2.8, max_value=8.0, value = 5.6)
for class_ in Z_15_30, Z_24_70, Z_70_300:
    object_ = class_()
    st.write(round(object_.main()))
APERTURE_PRIME = st.number_input('Aperture Prime', min_value = 1.2, max_value=2.8, value = 1.7)
for class_ in P_35, P_50:
    object_ = class_()
    st.write(round(object_.main()))
