import setuptools


setuptools.setup(
    name='seal-sorcery',
    version='1.0.0',
    author='RimoChan',
    author_email='the@librian.net',
    description='seal-sorcery',
    long_description=open('readme.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RimoChan/seal-sorcery',
    packages=[
        'seal_sorcery',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'numpy>=1.24.3',
        'opencv-python>=4.8.0.76',
        'numpy-stl>=3.0.1',
    ],
)
