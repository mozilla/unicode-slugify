from setuptools import setup

setup(
    name='unicode-slugify',
    version='0.1.1',
    description='A slug generator that turns strings into unicode slugs.',
    long_description=open('README.md').read(),
    author='Jeff Balogh, Dave Dash',
    author_email='jbalogh@mozilla.com, dd@mozilla.com',
    url='http://github.com/mozilla/unicode-slugify',
    license='BSD',
    packages=['slugify'],
    include_package_data=True,
    package_data = { '': ['README.md'] },
    zip_safe=False,
    install_requires=['django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: Mozilla',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)


