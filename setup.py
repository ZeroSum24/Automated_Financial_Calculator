import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zerosum24",
    version="1.0.0",
    author="Stephen Waddell",
    author_email="stephen_waddell@hotmail.co.uk",
    description="A package to convert spreadsheets into a usable database where custom SQL queries are run to output financial calculations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZeroSum24/Automated_Financial_Calculator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
