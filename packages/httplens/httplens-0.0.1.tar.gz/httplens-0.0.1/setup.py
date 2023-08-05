from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A Collection of http debugging and testing tools"
LONG_DESCRIPTION = open("README.md").read()


# Setting up
setup(
    name="httplens",
    version=VERSION,
    author="quiktea",
    author_email="wishymovies@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["aiohttp"],
    keywords=["python", "http", "debug", "testing"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)