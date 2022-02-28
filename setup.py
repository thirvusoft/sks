from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sks/__init__.py
from sks import __version__ as version

setup(
	name="sks",
	version=version,
	description="sks",
	author="sks",
	author_email="sks@gamil.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
