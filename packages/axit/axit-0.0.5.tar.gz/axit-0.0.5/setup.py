import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="axit", 
    version="0.0.5",
    author="kyshel",
    author_email="kyshel@example.com",
    description="Axit is a package for ax things.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kyshel/axit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)