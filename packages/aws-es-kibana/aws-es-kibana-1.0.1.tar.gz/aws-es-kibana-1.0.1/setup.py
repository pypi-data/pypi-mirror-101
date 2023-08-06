"""Setup for the aws-es-kibana package."""

import setuptools
import os


setuptools.setup(
    author="Ajay Kulal",
    author_email="hackerhero@wearehackerone.com",
    name='aws-es-kibana',
    license="MIT",
    description='aws-es-kibana is a amazing package for data handling',
    version='v1.0.1',
    long_description="no long decsription given",
    url='https://github.com/bountyrecon/',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
