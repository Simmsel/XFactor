from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="XFactor",
    version="1.0.0",
    python_requires=">=3.8",
    install_requires=requirements,
    packages=find_packages(),
)