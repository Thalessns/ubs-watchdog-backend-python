from setuptools import setup, find_packages

setup(
    name='UBS-Watchdog',
    version="0.2.0",
    packages=find_packages(where='watchdog'),
    python_requires='>=3.12',
    install_requires=[],
)