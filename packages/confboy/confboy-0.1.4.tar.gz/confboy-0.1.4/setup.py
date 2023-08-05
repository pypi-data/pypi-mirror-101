import setuptools


VERSION = '0.1.4'


setuptools.setup(
    name='confboy',
    packages=setuptools.find_packages(),
    version=VERSION,
    description='Better configs with TOML support',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Euromance/confboy',
    author='Euromancer',
    author_email='kysput@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    project_urls={
        'Repository': 'https://github.com/Euromance/confboy',
    },
    python_requires='>=3.7,<4.0',
    install_requires=[
        'toml==0.10.2',
    ],
    extras_require={
        'dev': [
            'flake8==3.9.0',
        ],
        'test': [
            'pytest-cov==2.11.1',
            'pytest==6.2.2',
        ],
    },
)
