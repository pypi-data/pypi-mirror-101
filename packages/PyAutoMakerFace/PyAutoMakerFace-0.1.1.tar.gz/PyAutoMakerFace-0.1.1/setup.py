import setuptools
import os
import sys
import site
from os.path import dirname
from glob import glob

with open("README.md", "rt") as fh:
    long_description = fh.read()

data_files_path = ""

if sys.platform == "nt":
    data_files_path = os.path.join("lib", "site-packages")

elif sys.platform == "linux":
    #이게 뭐였더라
    version = "python{}.{}".format(sys.version_info[0], sys.version_info[1])
    data_files_path = os.path.join(site.USER_BASE, "lib", "", "site-packages")

setuptools.setup(
    name="PyAutoMakerFace", # Replace with your own username
    version="0.1.1",
    author="WDW",
    author_email="boa3465@gmail.com",
    description="얼굴 인식을 위한 패키지",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://boa9448.tistory.com",
    project_urls={
        "Bug Tracker": "https://boa9448.tistory.com",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["PyAutoMakerFace"],
    #data_files=[("lib\\site-packages\\PyAutoMakerFace\\models", [file for file in glob("PyAutoMakerFace\\models\\*.*")])],
    data_files=[(os.path.sep.join([data_files_path, "PyAutoMakerFace", "models"])
                 , [file for file in glob("PyAutoMakerFace\\models\\*.*")])],
    install_requires = ["opencv-contrib-python==4.4.0.46", "numpy", "imutils"
                        , "scikit-learn", "waitress", "flask", "requests"],
    python_requires=">=3.6",
)