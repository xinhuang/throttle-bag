try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import throttle_bag

with open("README.rst") as readme_file:
    readme_string = readme_file.read()

setup(
    name="throttle-bag",
    version=throttle_bag.__version__,
    description="",
    author="Xin Huang",
    author_email="xinhuang.abc@gmail.com",
    url="https://github.com/xinhuang/throttle-bag",
    py_modules=['throttle_bag'],
    packages=['tests'],
    license="License :: OSI Approved :: MIT License",
    long_description=readme_string,
)
