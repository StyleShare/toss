import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="toss",
    version="0.0.4",
    author="Styleshare",
    author_email="dev@styleshare.kr",
    description="Toss payment client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/styleshare/toss",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'inflection>=0.3.1',
        'pytz>=2018.7',
        'requests>=2.20.1'
    ]
)
