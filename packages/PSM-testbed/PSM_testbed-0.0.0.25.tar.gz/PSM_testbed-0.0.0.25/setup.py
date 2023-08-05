from setuptools import setup
from setuptools import find_packages


setup(name='PSM_testbed',
      version='0.0.0.25',
      description='A testbed package for Phillip Maire',
      packages=find_packages(),
      author_email='phillip.maire@gmail.com',
      zip_safe=False,
      install_requires=[
       # "pyicu",
       "natsort==7.1.1"])
#      packages=['PSM_testbed'],
