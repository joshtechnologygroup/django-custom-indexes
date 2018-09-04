import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-custom-indexes',
    url='https://github.com/joshtechnologygroup/django-custom-indexes/',
    packages=find_packages(),
    version='0.1.4',
    description='PostgreSQL custom indexes for Django models',
    long_description=README,
    author='Anshul Chhangani',
    author_email='anshul.chhangani@gmail.com',
    license='BSD',
    install_requires=[],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
