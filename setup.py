import os
import glob
from setuptools import setup
from setuptools import find_packages
from distutils.core import setup
from Cython.Build import cythonize

# python setup.py build_ext --inplace
# python setup.py sdist bdist_wheel
# twine upload dist/measurement_stats-0.2.2*

my_directory = os.path.realpath(os.path.dirname(__file__))

cython_glob_path = os.path.join(my_directory, '**', '*.pyx')
cython_files = cythonize(
    [p for p in glob.iglob(cython_glob_path, recursive=True)]
)


def read_me():
    with open('README.rst') as f:
        return f.read()

setup(
    name='measurement_stats',
    version='0.2.2',
    description=
            'Measurement statistics with uncertainties and error propagation',
    long_description=read_me(),
    url='https://github.com/sernst/Measurement_Statistics',
    author='Scott Ernst',
    author_email='swernst@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',

        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    ext_modules=cython_files,
    install_requires=[
        'pandas',
        'numpy',
        'six',
        'scipy'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    keywords='measurements statistics error propagation',
)
