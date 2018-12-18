import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="sutoppu",
    version="1.2",
    description="A simple python implementation of Specification pattern.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/u8slvn/sutoppu",
    author="u8slvn",
    author_email="u8slvn@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
    ],
    keywords='specification DDD business-rules verification',
    packages=["sutoppu"],
    include_package_data=True,
)
