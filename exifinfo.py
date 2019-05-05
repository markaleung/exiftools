import piexif, os, re, sys, numpy as np

getFloat = lambda x: x[0]/x[1]
def printShort(dict_, filter_ = '.'):
	for k, v in dict_.items():
		if filter_ and re.search(filter_, str(k)):
			if isinstance(v, dict):
				print(k)
				printShort(v)
			else:
				print(str(k)+'\t'+str(v)[0:50])
def getNoGps(file, exif):
	'''Find files without GPS Info'''
	if 2 not in exif['GPS']:
		print(file, 'No GPS')
def getLatitude(file, exif):
	'''Find files with Latitude Info'''
	if 6 in exif['GPS']:
		print(file, exif['GPS'][5], getFloat(exif['GPS'][6]))
def getDate(file, exif):
	'''Find files where file has been modified'''
	takeDate, modDate = exif['0th'][306], exif['Exif'][36868]
	if str(takeDate) != str(modDate):
		print(file, takeDate, modDate)
def getTeleConv(file, exif):
	'''Find files where extra tele conversion has been used'''
	length35, length = exif['Exif'][41989], getFloat(exif['Exif'][37386])
	if 2.5 < length35 / length < 3:
		print(file, length35, length)
def getFocal(file, exif):
	'''Find files with certain focal length'''
	length = getFloat(exif['Exif'][37386])
	if length >= 45:
		print(file, length)
def getIso(file, exif):
	'''Find files with certain ISO'''
	iso = exif['Exif'][34855]
	if isinstance(iso, int) and iso > 6400:
		print(file, iso)
def getEv(file, exif):
	'''Find files with certain exposure value'''
	iso = exif['Exif'][34855]
	aperture, shutter, comp = [getFloat(exif['Exif'][n]) for n in [33437, 33434, 37380]]
	if isinstance(iso, int) and shutter > 0:
		ev = np.log2(aperture ** 2) - np.log2(shutter * iso * 0.01) + comp
		if ev > 13.5 or ev < 1.5:
			print(file, aperture, 1/shutter, iso, np.round(comp, 2), np.round(ev, 2))
def oneFile(path):
	exif = piexif.load(path)
	for function in (
		# getNoGps, 
		# getLatitude, 
		# getDate, 
		# getTeleConv, 
		# getFocal, 
		# getIso, 
		# getEv, 
	):
		try:
			function(path, exif)
		except KeyError:
			pass
def multiFile(folder):
	os.chdir(folder)
	paths = [(folder, file) for folder, _, files in os.walk('.') for file in files]
	paths = sorted(paths, key = lambda x: x[1])
	[oneFile(folder+separator+file) for folder, file in paths if file.lower()[-3:] == 'jpg']
if __name__=='__main__':
	if sys.platform == 'win32':
		separator = '\\'
		folder = 'C:\\Path to\\Photos'
	else:
		separator = '/'
		folder = "/Path to/Pictures/"
	multiFile(folder)
	# Get full info for one image
	exif = piexif.load('/Path to/Picture.jpg')
	printShort(exif)
