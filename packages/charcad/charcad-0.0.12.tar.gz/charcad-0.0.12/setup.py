from setuptools import setup, find_packages
from charcad.version import __version__

#exec(open('charcad/version.py', 'r').read())

VERSION = __version__

requirements = open('requirements.txt', 'r').read().splitlines()

setup(
    name='charcad',
    packages=find_packages(),
    version=VERSION,
    license='MIT',
    description='Character-based drawing tool',
    author='Victor Zoni',
    author_email='vczoni@gmail.com',
    url='https://github.com/vczoni/charcad',
    download_url=VERSION.join(
        ['https://github.com/vczoni/charcad/archive/v', '.tar.gz']),
    keywords=['CHARACTER', 'DRAWING', 'BASIC'],
    install_requires=requirements,
    python_requires='>=3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
