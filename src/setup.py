from setuptools import setup, find_packages

from codecs import open
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with open(os.path.join(here, '..', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stard',

    version='0.0.1',

    description='Service manager',
    long_description=long_description,

    url='https://github.com/DexterLB/stard',

    author='Angel Angelov',
    author_email='hextwoa@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='startup services init',

    packages=find_packages(),

    install_requires=[],

    extras_require={
        'dev': [],
        'test': ['nose'],
    },

    package_data={
    },

    data_files = [
        ('/etc/stard', ['etc/init.py'])
    ],

    entry_points={
        'console_scripts': [
            'stard=stard.stard:main',
            'rc.init=stard.stard:init',
        ],
    },
)
