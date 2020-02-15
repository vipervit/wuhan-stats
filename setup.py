from setuptools import setup, find_packages
from wuhan_stats import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = 'wuhan_stats',
    author='vipervit',
    author_email='vitolg1@gmail.com',
    license='Apache',
    description='Simple desktop alert for Wuhan virus statistics updates',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = find_packages(),
    version=__version__,
    url='https://github.com/vipervit/wuhan_stats',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: MacOS :: MacOS X",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop"
    ],
    install_requires=[
   'beautifulsoup4',
   'plyer',
   'requests'
    ]
)
