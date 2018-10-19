from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.1'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='etconfig',
    version=__version__,
    description='config library based on ElementTree api',
    long_description=long_description,
    url='https://github.com/yherve/etconfig',
    download_url='https://github.com/yherve/etconfig/tarball/' + __version__,
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    packages=find_packages(exclude=['examples', 'docs', 'tests*']),
    include_package_data=True,
    author='Yann Hervé',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email=''
)
