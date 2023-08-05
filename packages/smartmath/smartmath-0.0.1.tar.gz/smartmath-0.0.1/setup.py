import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smartmath", # Replace with your own username
    version="0.0.1",
    author="Sneha Bhutada",
    author_email="snehabhutada2015@gmail.com",
    description="A small mathematics test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snehabhutada2015/smartmath",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)