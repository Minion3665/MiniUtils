from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='create-machine-utils',
    version='1.2.6',
    packages=find_packages(),
    url='https://github.com/Minion3665/MiniUtils',
    license='GNU General Public License V3',
    author='Minion3665',
    author_email='nathan@clicksminuteper.net',
    description='The MiniUtils module to make making discord bots easier',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
