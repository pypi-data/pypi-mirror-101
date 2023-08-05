from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


test_requirements = [
    'pytest',
    'pytest-cov',
]


setup(
    name='circum-hc-sr04',
    version_format='{tag}',
    author="Lane Haury",
    author_email="lane@lumineerlabs.com",
    description="HC-SR04 sensor plugin for circum.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/LumineerLabs/circum-hc-sr04",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        'circum',
        'click',
    ],
    setup_requires=[
        'setuptools',
        'setuptools-git-version',
    ],
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'calibrate-hc-sr04=circum_hc_sr04.calibrate:cli',
        ],
        'circum.sensors': [
            'hc-sr04=circum_hc_sr04.hc_sr04:hc_sr04'
        ]
    },
    extras_require={
        'lint': [
            'flake8',
            'flake8-import-order',
            'flake8-builtins',
            'flake8-comprehensions',
            'flake8-bandit',
            'flake8-bugbear',
        ],
        'linux': [
            'RPi.GPIO2'
        ],
        'rpi': [
            'RPi.GPIO'
        ],
        'test': test_requirements,
    },
    python_requires=">=3.7",
)
