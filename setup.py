from distutils.core import setup
from setuptools import find_packages

setup(
	name='bot',
	packages=find_packages('bot'),
	version='0.0.0',
	license='MIT',
	description='A simple discord bot',
	long_description="",
	long_description_content_type='text/markdown',
	author='Geoffrey Daniels',
	author_email='geoff@gpdaniels.com',
	url='https://gpdaniels.com',
	# List of packages to install with this one 
	install_requires=[
        "discord.py",
        "english-words",
    ],
)
