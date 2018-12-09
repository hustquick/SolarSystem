from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    licenses = f.read()

setup(
    name='solar_system',
    version='1.0',
    description='Packages for solar thermal power system',
    long_description=readme,
    author='Zhang Cheng',
    author_email='hustquick@hust.edu.cn',
    url='https://github.com/hustquick/PythonCascadeSystem',
    license=licenses,
    packages=find_packages(exclude=('tests', 'docs'))
)
