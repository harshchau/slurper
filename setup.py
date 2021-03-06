import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slurper", # Replace with your own username
    version="0.0.5.23",
    author="Harsh Chaudhary",
    author_email="chaudhary.harsh@gmail.com",
    description="A package to scrape public data sources",
    long_description="A package to scrape public data sources",
    long_description_content_type="text/markdown",
    url="https://github.com/harshchau/slurper",
    packages=setuptools.find_packages(exclude=('tests')),
    install_requires = [
        'beautifulsoup4',
        'bs4',
        'cachetools',
        'certifi',
        'chardet',
        'docutils',
        'html2text',
        'idna',
        'jmespath',
        'python-dateutil',
        'reppy',
        'requests',
        'requests-file',
        'selenium',
        'six',
        'soupsieve',
        'tldextract',
        'urllib3',
        'validator_collection'
# boto3
# botocore
# s3transfer        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)