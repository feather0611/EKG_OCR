## Information
This repository provides three functions. The first is transfer dicom image format into PNG format. Second is doing OCR process with EKG data that in specfic format, and it will crop the part contains raw image data.
### Develop Environment
Python 3.9.7
### Required Modules
1. [Numpy](https://github.com/numpy/numpy)
2. [Pandas](https://github.com/pandas-dev/pandas)
3. [Pytesseract](https://github.com/madmaze/pytesseract)
4. [pydicom](https://github.com/pydicom/pydicom)
5. [Pillow](https://github.com/python-pillow/Pillow)
6. [OpenCV](https://github.com/opencv/opencv)

## Usage
1. Create an empty directory on the path you want.
2. Make sure `Virtualenv` is already installed. If your Python environment not install `Virtualenv` yet. You can install it with pip.
<pre>
pip3 install virtualenv
</pre>
3. Open Terminal or Command line tools. Change working directory to the new one. Then use `Virtualenv` to create a new venv. 
#### Windows
<pre>
dir your/path
virtualenv --python=/path/to/your/python venv
</pre>
#### macOS/Linux
<pre>
cd your/path
virtualenv --python=/path/to/your/python venv
</pre>
4. Enter the virtual environment mode.
#### Windows
<pre>
.\venv\Scripts\activate.bat
</pre>
#### macOS/Linux
<pre>
source ./venv/bin/activate
</pre>
If enter the virtual environment successfully. you will see your command line changed like below.
#### Windows
<pre>
(venv) C:\>
</pre>
#### macOS/Linux
<pre>
(venv) $
</pre>
5. clone this repository into the directory.
<pre>
git clone https://github.com/feather0611/EKG_OCR.git
</pre>
6. Use `pip` to install all the required modules with `requirements.txt`
<pre>
pip install -r requirements.txt
</pre>
7. `transer.py` will automatically rename EKG dicom file that provided by VGHTC(臺中榮總) and take out to specific directory. And also it will make a png copy in the path you want. Please edit line 18-21 of this file to assign the path of source, files that take out, and files that transfer into PNG. For example:
<pre>
# path to dicom source
source = './300EKG/0001/'
# path to output destination
dist = './prod300/dist/'     # Path to store dicom files
origin = './prod300/origin/' # Path to store PNG files.
</pre>
8. Then run it.
<pre>
python transfer.py
</pre>

You don't need to clean up separate directory into one directory. You can just change the source path and run several times, and the result will be added in the destination path.    
9. Now we got PNG files that needed in OCR works. So you can change the path on line 26-27 of `main.py` into the directory path you just store PNG format image and the path to store the raw EKG information part. For example:
<pre>
img_path = './prod300/dist/'
raw_path = './prod300/raw/'
</pre>
10. Then run this script.
<pre>
python main.py
</pre>
11. If everything is OK, you will get two files and all the PNG files contain raw EKG data, `out.csv` and `err.csv`. The records on `out.csv` are basically correct. But maybe some little problem will still happen. The records on `err.csv` are records have problems obviously.
