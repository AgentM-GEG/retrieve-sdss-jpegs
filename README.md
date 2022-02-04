# retrieve-sdss-jpegs
A simple script to use SDSS SciServer frontend to retrieve JPEGs of galaxies across different data releases.

# Prerequistes

Install the SciServer module by unpacking the zip file provided in the repo. 

1. cd SciServer/py3
2. python3 setup.py install

Note: I made a small change to the getJpegCutout script that now pings an additional (old) server that hosts <DR12 JPEGs. 
If you download the current module from https://github.com/sciserver/SciScript-Python, it will fail e.g., DR7.
 
Look at the python file, change the JPEG save paths, and execute it!
