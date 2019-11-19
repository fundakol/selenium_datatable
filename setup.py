import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='items-list',
    version='0.1.0',
    author='Łukasz Fundakowski',
    author_email='fundakol@yahoo.com',
    description="A small library for simplifying a table object in selenium",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fundakol/items-list-pattern',
    packages=['items_list'],
    install_requires=['selenium'],
    keywords='selenium table'
)

classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
]
