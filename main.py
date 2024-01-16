import exifread as ef
import glob
import csv
import os

# Written by Richard Blanchette 090419
# "barrowed" from https://stackoverflow.com/questions/19804768/interpreting-gps-info-of-exif-data-from-photo-in-python
# who "barrowed" from
# https://gist.github.com/snakeye/fdc372dbf11370fe29eb


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


def getGPS(filepath):
    '''
    returns gps data if present other wise returns empty dictionary
    '''
    with open(filepath, 'rb') as f:
        tags = ef.process_file(f)

        if tags == {}:
            print ('Bad File: ', filepath)
            DateTime = "None"
            latitude = "None"
            longitude = "None"
            print("Processed a total of" , count , "pictures")
            input("Press Enter to Close....")
            quit()

        DateTime = tags.get('EXIF DateTimeOriginal')
        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')
        if latitude:
            lat_value = _convert_to_degress(latitude)
            if latitude_ref.values != 'N':
                lat_value = -lat_value
        else:
            return {}
        if longitude:
            lon_value = _convert_to_degress(longitude)
            if longitude_ref.values != 'E':
                lon_value = -lon_value
        else:
            return {}
        return DateTime, lat_value, lon_value
    return {}

# This is to build the CSV and assign Headers
with open('imagelog.csv', mode='w', newline='') as imagelog:
    fieldnames = ['Filepath', 'DateTimeOriginal',
                  'GPSLatitude', 'GPSLongitude']
    imagelog = csv.DictWriter(imagelog, fieldnames=fieldnames)

    imagelog.writeheader()

#Reset Counter
count = 0

print("Folder Name?")
FolderName = input()

if (os.path.isdir(FolderName)):
    print("Directory exist")
else:
    print("Directory does not exist")
    input("Press Enter to Close....")
    quit()

# Initialize counters
file_count = 0
file_types = {}

# Iterate over files in the directory
for file_path in glob.glob(FolderName + '/*'):
    # Increment file count
    file_count += 1

    # Get file extension
    file_extension = os.path.splitext(file_path)[1]

    # Update file types dictionary
    if file_extension in file_types:
        file_types[file_extension] += 1
    else:
        file_types[file_extension] = 1

# Print the results
print("Number of files:", file_count)
print("File types:")
for file_extension, count in file_types.items():
    print(file_extension, ":", count)

path = glob.glob(os.path.join(FolderName, '*.jpg')) or glob.glob(os.path.join(FolderName, '*.JPG'))

# Reset Counter
processed_count = 0
for filepath in path:
    print(filepath)

    Time, Lat, Long = getGPS(filepath)
    print(Time)
    print(Lat)
    print(Long)

    with open('imagelog.csv', mode='a', newline='') as imagelog:
        fieldnames = ['Filepath', 'DateTimeOriginal', 'GPSLatitude', 'GPSLongitude']
        imagelog = csv.DictWriter(imagelog, fieldnames=fieldnames)
        imagelog.writerow({'Filepath': filepath, 'DateTimeOriginal': Time, 'GPSLatitude': Lat, 'GPSLongitude': Long})
        processed_count += 1

print(f"Processed: {processed_count}")
input("Press Enter to Close....")
quit()