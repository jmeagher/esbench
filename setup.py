# from distutils.core import setup
from setuptools import setup

setup(
    name='esbench',
    version='0.01-dev',
    description="Testing ElasticSearch",
    author="John Meagher",
    author_email="",
    license="",
    classifiers=[
      "Programming Language :: Python :: 3",
      "Intended Audience :: Developers",
    ],
    install_requires=[
        'locustio==0.8.1',
        'Faker==0.9.0',
    ],
)