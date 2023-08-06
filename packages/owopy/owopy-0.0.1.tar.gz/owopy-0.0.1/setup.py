from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Other Audience',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9'
]

setup(
    name = 'owopy',
    version = '0.0.1',
    description = 'This module OwOifies your sentences (turns your sentences into japanese "furry" baby babblespeak :>)',
    long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url = 'https://github.com/Nimboss2411/OwOpy',
    author = 'Nimit Grover',
    author_email = 'nimbossthegreat@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = 'text',
    packages = find_packages(),
    install_requires = ['']
)