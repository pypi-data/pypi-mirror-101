# !/usr/bin/env python
__version__ = "1.2.2"

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='api_jwt',
    version=__version__,
    description='Library for JWT encoding/decoding specifically adapted to use in APIs',
    long_description_content_type="text/markdown",
    long_description=readme(),
    author='Greger Wedel',
    author_email='greger@greger.io',
    license='Apache2',
    url='https://github.com/gregertw/api_jwt',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    py_modules=['api_jwt', ],
    install_requires=[
        'pyjwt>=1.6.1',
        'cryptography',
    ],
    include_package_data=True
)
