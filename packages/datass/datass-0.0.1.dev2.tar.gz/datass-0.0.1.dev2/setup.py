import re
import setuptools


with open('datass/__init__.py', 'r') as version:
    version = re.search('(\d\.\d\.[\d\w\.]+)', version.readline()).group()

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

run_requirements = [
    'numpy',
    'nltk',
    'pandas',
    'seaborn',
    'matplotlib',
    'plotly'
]

setuptools.setup(
    name='datass',
    version=version,
    author='Henrique Brandão',
    author_email='brandao.t.henrique@gmail.com',
    license='MIT',
    zip_safe=False,
    install_requirements=run_requirements,
    description='Data Science Shortcuts. Package for lazy, or overwhelmed, data scientists',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/htbrandao/datass',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
