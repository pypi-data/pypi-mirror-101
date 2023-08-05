import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="segm8",
    version="1.0.0",
    description="Raspberry Pi library for interaction with a chain of a "
    "particular SegM8 7-segment indicator modules.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/amperka/SegM8Pi/",
    author="Amperka LLC",
    author_email="dev@amperka.com",
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["segm8"],
    install_requires=["spidev"],
)
