from setuptools import setup, find_packages

with open("CHANGELOG.md", "r") as fh:
    changelog = fh.read()
    latest = changelog.split("####")[1].split("\n", 1)[1].rstrip()

with open("README.md", "r") as fh:
    long_description = fh.read().format(latest_change=latest, changelog=changelog)

setup(
    name='create-machine-utils',
    version='1.3.5',
    packages=find_packages(),
    url='https://github.com/Minion3665/MiniUtils',
    license='GNU General Public License V3',
    author='Minion3665',
    author_email='nathan@clicksminuteper.net',
    description='The MiniUtils module to make making discord bots easier',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
