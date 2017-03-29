from setuptools import setup, find_packages

setup(
    name='cortexutils3',
    version='1.0.0',
    description='A Python 3 library for including utility classes for Cortex analyzers - copy from cortexutils missing'
                'the ioc parser dependency and artifacts.',
    author='Nils Kuhnert',
    author_email='3c7@posteo.de',
    license='MIT',
    url='tba',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    py_modules=['cortexutils3.analyzer'],
    packages=find_packages()
)
