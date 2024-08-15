from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mobile_app/__init__.py
from mobile_app import __version__ as version

setup(
	name="mobile_app",
	version=version,
	description="mobile_app",
	author="rehan",
	author_email="rehan@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
