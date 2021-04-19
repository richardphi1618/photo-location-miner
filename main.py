import exifread as ef
import glob
import csv
import os
import re

# Written by Richard Blanchette 090419
# "barrowed" from https://stackoverflow.com/questions/19804768/interpreting-gps-info-of-exif-data-from-photo-in-python
# who "barrowed" from
# https://gist.github.com/snakeye/fdc372dbf11370fe29eb

#test

def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


def getGPS(filepath):
    '''
    returns gps data if present otherwise returns empty dictionary
    '''
    with open(filepath, 'rb') as f:
        tags = ef.process_file(f)

        if tags == {}:
            print('Bad File: ', filepath)
            DateTime = "None"
            latitude = "None"
            longitude = "None"
            print("Processed a total of", count, "pictures")
            input("Press Enter to Close....")
            quit()

        DateTime = tags.get('EXIF DateTimeOriginal')
        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')
        UserComment = tags.get('EXIF UserComment')

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
        return DateTime, lat_value, lon_value, UserComment
    return {}

# This is to build the CSV and assign Headers
with open('imagelog.csv', mode='w', newline='') as imagelog:
    fieldnames = ['Filepath', 'DateTimeOriginal',
                  'GPSLatitude', 'GPSLongitude', 'UserComment']
    imagelog = csv.DictWriter(imagelog, fieldnames=fieldnames)

    imagelog.writeheader()

# Reset Counter
count = 0

print("Folder Name?")
FolderName = input()


#check if folder exists
if (os.path.isdir(FolderName)):
    print("Directory exist")
else:
    print("Directory does not exist")
    input("Press Enter to Close....")
    quit()


for filepath in glob.iglob(FolderName+'/*.jpg'):
    Time, Lat, Long, UserComm = getGPS(filepath)
    '''
    print(Time)
    print(Lat)
    print(Long)
    '''

    # snip text from user comment
    print(filepath)
    UserComm_str = str(UserComm)
    UserComm_Desc = re.search('DESCRIPTION: (.*) WATERMARK:', UserComm_str)
    # print(UserComm_Desc.group(1))

    # store data in spreadsheet

    with open('imagelog.csv', mode='a', newline='') as imagelog:
        fieldnames = ['Filepath', 'DateTimeOriginal',
                      'GPSLatitude', 'GPSLongitude', 'UserComment']
        imagelog = csv.DictWriter(imagelog, fieldnames=fieldnames)
        imagelog.writerow({'Filepath': filepath, 'DateTimeOriginal': Time,
                           'GPSLatitude': Lat, 'GPSLongitude': Long, 'UserComment': UserComm_Desc.group(1)})

    # count number of files
        count += 1

print("Processed ", count, " of pictures")
input("Press Enter to Close....")