import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="world-class",
    version="0.0.8",
    description="A mixture of ISO 3166-1 Alpha-2 Country codes and ISO 639-1 Language codes.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/lvm/world-class",
    author="Mauro Lizaur",
    author_email="mauro@sdf.org",
    license="BSD 3-Clause License",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["world_class"],
    include_package_data=True,
    install_requires=[],
    entry_points={},
)
