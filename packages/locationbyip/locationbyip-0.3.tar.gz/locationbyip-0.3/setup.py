from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name="locationbyip",version="0.3",description="By this package you can find location, coordinates, isp details to use in your application.",author="Awais khan",long_description=long_description,author_email="contact@awaiskhan.com.pk", packages=['LocationByIP'], install_requires=['requests'])
