import numpy as np
import pydicom
from PIL import Image
import os
import platform
from shutil import copyfile


def load_dir(src_dir):
    files = os.listdir(src_dir)
    # for MacOS
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    return files


# path to dicom source
source = './300EKG/0004/'
# path to output destination
dist = './prod300/dist/'
origin = './prod300/origin/'

patients = load_dir(source)

# filter the EKG files
for p in patients:
    dirs = load_dir(source + p + '/')
    if 'EKG' in dirs:
        files = load_dir(source+p+'/EKG/')
        if (len(files) != 0):
            try:
                os.rename(source + p + '/EKG/IMG0001', source + p + '/EKG/' + p + '.dcm')
            except:
                pass
            copyfile(source + p + '/EKG/' + p + '.dcm', origin + p + '.dcm')
            im = pydicom.dcmread(source + p + '/EKG/' + p + '.dcm')
            im = im.pixel_array.astype(float)
            rescaled_image = (np.maximum(im, 0) / im.max()) * 255
            final_image = np.uint8(rescaled_image)
            final_image = Image.fromarray(final_image)
            # final_image.show()
            final_image.save(dist + p + '.png')
