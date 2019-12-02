import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='selenium_datatable',
    version='0.2.0',
    author='Łukasz Fundakowski',
    author_email='fundakol@yahoo.com',
    description="A small library for simplifying a table object in selenium",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fundakol/selenium_datatable',
    packages=['selenium_datatable'],
    install_requires=['selenium'],
    keywords='selenium table'
)

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
]
