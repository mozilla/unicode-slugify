import sys
import io
from setuptools import setup

with io.open('README.md', encoding='utf-8') as fh:
    description = fh.read()

setup(
    name='unicode-slugify',
    version='0.1.5',
    description='A slug generator that turns strings into unicode slugs.',
    long_description=description,
    author='Jeff Balogh, Dave Dash',
    author_email='jbalogh@mozilla.com, dd@mozilla.com',
    url='http://github.com/mozilla/unicode-slugify',
    license='BSD',
    packages=['slugify'],
    include_package_data=True,
    package_data={'': ['README.md']},
    zip_safe=False,
    install_requires=['six', 'unidecode'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: Mozilla',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)


