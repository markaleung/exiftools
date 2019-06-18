import os, re, piexif, sys

def checkRE(file):
	for r in [
		r'^img_\d{4}(\D.*)?.jpg', 
		r'^p\d{7}(\D.*)?.jpg', 
	]:
		if re.search(r, file.lower()):
			return True
	return False

def rename(folder, file):
	if checkRE(file.lower()):
		old = folder+separator+file

		exif = piexif.load(old)
		try:
			time = exif['Exif'][36867].decode('utf-8')
			time = time.replace(':', '').replace(' ', '_')
			
			new = folder+separator+time+'_'+file
			print(new)
			os.rename(old, new)
		except KeyError:
			pass

def unrename(folder, file):
	if re.match(r'\d{8}_\d{6}_.*.jpg', file.lower()):
		new = folder+separator+re.sub(r'^\d{8}_\d{6}_(.*)$', r'\1', file)
		print(new)
		os.rename(folder+separator+file, new)

def main(topFolder, function):
	os.chdir(topFolder)
	paths = [(folder, file) for folder, _, files in os.walk('.') for file in files]
	paths = sorted(paths, key = lambda x: x[1])
	[function(folder, file) for folder, file in paths]

if __name__ == '__main__':
	if sys.platform == 'win32':
		separator = '\\'
    topFolder = 'C:\\Photos'
	else:
		separator = '/'
    topFolders = ["/Pictures/"
  main(topFolder, rename)
