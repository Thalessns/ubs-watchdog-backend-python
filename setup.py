from setuptools import setup, find_packages

setup(
    name='UBS-Watchdog',
    version='0.0.1',
    packages=find_packages(where='watchdog'),
    python_requires='>=3.13',
    install_requires=[],
)