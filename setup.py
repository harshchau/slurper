import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slurper", # Replace with your own username
    version="0.0.5.5",
    author="Harsh Chaudhary",
    author_email="chaudhary.harsh@gmail.com",
    description="A package to scrape public data sources",
    long_description="A package to scrape public data sources",
    long_description_content_type="text/markdown",
    url="https://github.com/harshchau/slurper",
    packages=setuptools.find_packages(exclude=('tests')),
    install_requires = [
        'requests',
        'html2text',
        'bs4',
        'argparse'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)