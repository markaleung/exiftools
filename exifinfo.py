import piexif, os, re, sys, numpy as np, subprocess

getFloat = lambda x: x[0]/x[1]
def printShort(dict_, filter_ = '.'):
	for k, v in dict_.items():
		if re.search(filter_, str(k)):
			if isinstance(v, dict):
				print(k)
				printShort(v)
			else:
				print(str(k)+'\t'+str(v)[0:50])
def getDate(file, exif):
	'''Find files where file has been modified'''
	takeDate, modDate = exif['0th'][306], exif['Exif'][36868]
	if str(takeDate) != str(modDate):
		print(file, takeDate, modDate)
		return True
def getExposureValue(file, exif):
	'''Find files with certain exposure value'''
	iso = exif['Exif'][34855]
	aperture, shutter, comp = [getFloat(exif['Exif'][n]) for n in [33437, 33434, 37380]]
	if isinstance(iso, int) and shutter > 0:
		ev = np.log2(aperture ** 2) - np.log2(shutter * iso * 0.01) + comp
		if 2 <= ev < 2.5:
			print(file, aperture, 1/shutter, iso, np.round(comp, 2), np.round(ev, 2))
			return True
def getFocal(file, exif):
	'''Find files with certain focal length'''
	length = getFloat(exif['Exif'][37386])
	if length >= 45:
		print(file, length)
		return True
def getIso(file, exif):
	'''Find files with certain ISO'''
	iso = exif['Exif'][34855]
	if isinstance(iso, int) and iso > 6400:
		print(file, iso)
		return True
def getLatitude(file, exif):
	'''Find files with Latitude Info'''
	if 6 in exif['GPS']:
		print(file, exif['GPS'][5], getFloat(exif['GPS'][6]))
		return True
def getNoGps(file, exif):
	'''Find files without GPS Info'''
	if 2 not in exif['GPS']:
		print(file, 'No GPS')
		return True
def getPanorama(file, exif):
	if exif['Exif'][40963] == 1920:
		print(file, exif['Exif'][40962])
		return True
def getTeleConv(file, exif):
	'''Find files where extra tele conversion has been used'''
	length35, length = exif['Exif'][41989], getFloat(exif['Exif'][37386])
	if 2.5 < length35 / length < 3:
		print(file, length35, length)
		return True
def getWhiteBalance(file, exif):
	wb = exif['Exif'][41987]
	if wb != 0:
		print(file, wb)
		return True
def oneFile(path):
	exif = piexif.load(path)
	for function in (
		# getDate, 
		# getExposureValue, 
		# getFocal, 
		# getIso, 
		# getLatitude, 
		# getNoGps, 
		# getPanorama, 
		getTeleConv, 
		# getWhiteBalance, 
	):
		try:
			if function(path, exif):
				return path
		except KeyError:
			pass
def multiFile(topFolder):
	os.chdir(topFolder)
	paths = [(folder, file) for folder, _, files in os.walk('.') for file in files]
	paths = sorted(paths, key = lambda x: x[1])
	paths = [oneFile(folder+separator+file) for folder, file in paths if file.lower()[-3:] == 'jpg']
	# On mac, opens all files that match the filter
	paths = [topFolder+re.sub(r"([ '])", r'\\\1', p[1:]) for p in paths if p]
	if paths and sys.platform == 'darwin':
		subprocess.call('open %s' % ' '.join(paths), shell=True)

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
