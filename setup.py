from setuptools import setup, find_packages
setup(
    name = 'wuhan-stats',
    author='vipervit',
    author_email='vitolg1@gmail.com',
    license='Apache',
    description='Simple desktop alert for Wuhan virus statistics updates',
    packages = find_packages(),
    package_data={'': ['requirements.txt']},
    include_package_data=True,
    version='1.15.07'
)
