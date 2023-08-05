from distutils.core import setup
import setuptools

setup(
    name='tool4keras',
    version='0.0.2',
    packages=setuptools.find_packages(),
    url='',
    license='MIT',
    author='samma',
    requires=['keras', 'google_drive_downloader', 'tensorflow', 'numpy', 'gensim', 'tqdm'],
    author_email='13336502700@163.com',
    description='collect common tool of keras'
)
