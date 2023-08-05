import setuptools

REQUIRED_PACKAGES = [
    'python-dateutil',
    'pytz>=2021.1',
    'requests',
    'pathlib',
    'pandas>=0.25.1',
    'regex',
    'xarray==0.17.0',
    'netCDF4',
    'pyarrow',
    'nlqweer==0.0.1'
    ]

PACKAGE_NAME = 'nlqweer'
PACKAGE_VERSION = '0.0.1'

setuptools.setup(
    name = 'nlqweer',
    version = '0.0.1',  # Ideally should be same as your GitHub release tag varsion
    description = 'weather data platform',
    author = 'minh',
    author_email = 'minh@novalinq.com',
    url = 'https://github.com/novalinq/nlqweer/',
    keywords = ['knmi', 'Actuele10mindataKNMIstations', 'nederlands'],
    classifiers = [],
    packages = setuptools.find_packages(),
)
