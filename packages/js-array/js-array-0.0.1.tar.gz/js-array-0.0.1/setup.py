import setuptools

with open("README.md", "r") as f:
    _description = f.read()

setuptools.setup(
    name="js-array",
    version="0.0.1",
    author="jay3332",
    description="A basic Python module that brings the attributes and methods of a Javascript array to Python.",
    long_description=_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jay3332/js-array",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
