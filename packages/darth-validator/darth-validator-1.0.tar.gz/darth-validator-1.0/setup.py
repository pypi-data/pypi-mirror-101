import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="darth-validator",
    version="1.0",
    author="Angel Davila",
    author_email="adavila0703@gmail.com",
    description="Automatically validates correlation between two workbooks."
                "darth-validator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adavila0703/darth-validator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
