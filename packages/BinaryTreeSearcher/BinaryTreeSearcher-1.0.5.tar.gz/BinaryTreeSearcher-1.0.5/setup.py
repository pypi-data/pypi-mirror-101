import setuptools

with open("README.md", "r") as rd:
    long_description = rd.read()

setuptools.setup(
    name="BinaryTreeSearcher",
    version="1.0.5",
    author="Solomon Ndifereke Aniefiok",
    author_email="solomonndi96@gmail.com",
    description="A simple binary tree search library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DR-FREKE/BinaryTreeSearch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
)
