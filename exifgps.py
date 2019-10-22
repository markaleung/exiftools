import piexif, datetime, sys
from dateutil.relativedelta import relativedelta

# Helper Functions
multiplierDMS = 10000
multiplierElev = 100
def makeDMS(number):
	number = abs(number)
	degrees = int(number)
	minutes = int((number - degrees) * 60)
	seconds = (number - degrees - minutes/60) * 3600 * multiplierDMS
	seconds = int(round(seconds, 0))
	return ((degrees, 1), (minutes, 1), (seconds, multiplierDMS))
unDMS = lambda dms: round(dms[0][0] + dms[1][0] / 60 + dms[2][0] / 3600 / dms[2][1], 5)
def makeDict(lat, lon, elevation, utc):
	main = [
		[1, b'N' if lat >= 0 else b'S'], 
		[2, makeDMS(lat)], 
		[3, b'E' if lon >= 0 else b'W'], 
		[4, makeDMS(lon)], 
	]
	elevation = [
		[5, 0 if elevation >= 0 else 1], 
		[6, (int(abs(elevation) * multiplierElev), multiplierElev)]
	] if elevation == elevation else []
	utc = [
		[7, ((utc.hour, 1), (utc.minute, 1), (utc.second, 1))], 
		[29, utc.strftime('%Y:%m:%d').encode('utf-8')], 
	] if utc == utc else []
	return dict(main+elevation+utc)
def getUTC(folder, file, hours, minutes):
	exif = piexif.load(folder+'/'+file)
	try:
		time = exif['Exif'][36867].decode('utf-8')
		time = datetime.datetime.strptime(time, '%Y:%m:%d %H:%M:%S')
		utc = time - relativedelta(hours = int(hours), minutes = int(minutes))
	except KeyError:
		utc = float('nan')
	return exif, utc

# Main Function
def gps(folder, file, lat, lon, elevation, hours, minutes):
	exif, utc = getUTC(folder, file, hours, minutes)
	if 2 not in exif['GPS']:
		exif['GPS'] = makeDict(lat, lon, elevation, utc)
		# Modify File
		piexif.insert(piexif.dump(exif), folder+'/'+file)
		print(file, unDMS(exif['GPS'][2]), unDMS(exif['GPS'][4]))

if __name__=='__main__':
	gps('/path/to/photo', 'image.jpg', 100, 20, 20, 1, 0)
