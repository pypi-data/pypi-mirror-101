from setuptools import setup

setup(
    name='DEA',
    version='0.1',
    author='Jeff Liu',
    author_email='jeffliu6068@gmail.com',
    packages=['DEA'],
    url='https://github.com/jeffliu6068/DEA',
    license='LICENSE.txt',
    description='A simple library for differential expression analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pandas',
        'scipy',
        'numpy',
        'matplotlib',
        'sklearn',
        'tqdm'
    ],
)
