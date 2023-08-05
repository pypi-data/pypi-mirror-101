from setuptools import setup
import os


def read(fname):
    return open(fname).read()


setup(
    name='GMMchi',
    version='0.1',
    author='Jeff Liu',
    author_email='jeffliu6068@gmail.com',
    packages=['GMMchi'],
    url='http://pypi.python.org/pypi/GMMchi/',
    license='MIT',
    description='GMM with chi-square protocol',
    long_description_content_type='text/markdown',
    long_description=read('README.md'),
    install_requires=[
        'pandas',
        'scipy',
        'numpy',
        'matplotlib',
        'seaborn',
        'sklearn',
        'tqdm',
    ],
)
