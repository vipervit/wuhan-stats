from setuptools import setup, find_packages
from wuhan_stats import __version__
setup(
    name = 'wuhan_stats',
    author='vipervit',
    author_email='vitolg1@gmail.com',
    license='Apache',
    description='Simple desktop alert for Wuhan virus statistics updates',
    packages = find_packages(),
    package_data={'': ['requirements.txt']},
    include_package_data=True,
    version=__version__
)
