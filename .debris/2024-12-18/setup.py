from setuptools import setup

# Uvozimo sadržaj requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='your_package_name',
    version='0.1',
    packages=['your_package'],
    install_requires=requirements,  # Dodajemo liste zavisnosti iz requirements.txt
)
