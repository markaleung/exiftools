import piexif, datetime
from dateutil.relativedelta import relativedelta

class GPS():
	def _make_dms(self, number):
		number = abs(number)
		degrees = int(number)
		minutes = int((number - degrees) * 60)
		seconds = (number - degrees - minutes/60) * 3600 * MULTIPLIER_DMS
		seconds = int(round(seconds, 0))
		return ((degrees, 1), (minutes, 1), (seconds, MULTIPLIER_DMS))
	def load_gps(self, lat, lon, elevation):
		self.lat = lat
		self.lon = lon
		self.elevation = elevation
	def load_file(self, folder, file):
		self.folder = folder
		self.file = file
		self.exif = piexif.load(self.folder+'/'+self.file)
	def get_utc(self, hours, minutes):
		try:
			time = self.exif['Exif'][36867].decode('utf-8')
			time = datetime.datetime.strptime(time, '%Y:%m:%d %H:%M:%S')
			self.utc = time - relativedelta(hours = int(hours), minutes = int(minutes))
		# KeyError: Date is missing. TypeError: hours or minutes is None
		except (KeyError, TypeError):
			self.utc = float('nan')
	def _make_dict(self):
		main = [
			[1, b'N' if self.lat >= 0 else b'S'], 
			[2, self._make_dms(self.lat)], 
			[3, b'E' if self.lon >= 0 else b'W'], 
			[4, self._make_dms(self.lon)], 
		]
		elevation = [
			[5, 0 if self.elevation >= 0 else 1], 
			[6, (int(abs(self.elevation) * MULTIPLIER_ELEV), MULTIPLIER_ELEV)], 
		] if self.elevation == self.elevation else []
		utc = [
			[7, ((self.utc.hour, 1), (self.utc.minute, 1), (self.utc.second, 1))], 
			[29, self.utc.strftime('%Y:%m:%d').encode('utf-8')], 
		] if self.utc == self.utc else []
		self.exif['GPS'] = dict(main + elevation + utc)
		# Modify File
		piexif.insert(piexif.dump(self.exif), self.folder+'/'+self.file)
	def main(self):
		if 2 not in self.exif['GPS'] or True:
			self._make_dict()
			print(self.file, round(self.lat, 6), round(self.lon, 6))

def gps(folder, file, latitude, longitude, elevation, hours, minutes):
	my_gps = GPS()
	my_gps.load_file(folder, file)
	my_gps.load_gps(latitude, longitude, elevation)
	my_gps.get_utc(hours, minutes)
	my_gps.main()

# Multipliers
MULTIPLIER_DMS = 10000
MULTIPLIER_ELEV = 100

if __name__=='__main__':
    gps('/path/to/', 'image.jpg', 40.01105, 116.386242, 0, 8, 0)
