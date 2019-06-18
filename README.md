# exiftools
A collection of programs for processing digital photos' EXIF data
These programs require installing piexif: pip install piexif. 

# exifinfo
Useful functions to filter for photos with certain exif properties

# exifrename
Rename photos based on their exif date

This program has two functions
## rename(topFolder, expressions)
- This adds date and time to all photos in all subdirectories in topFolder
- The date time format is '20190101_010101_' + original file name
- You must specify a list of regular expressions to match filenames e.g. [r'img_\d{4}.jpg', r'p\d{7}.jpg']
## unrename(topFolder)
- This removes date and time from all photos in all subdirectories in topFolder
- It only removes date and time in the format '20190101_010101_'

# exifgps
Add GPS Information to your photos

- This program contains one main function: gps(folder, file, latitude, longitude, elevation, hours, minutes). 
- Latitude and longitude should be specified in decimal degrees. 
- Elevation is specified in metres. If elevation is unavailable, put float('nan'). 
- You can specify hours and minutes of the time zone where the photos were taken. 
