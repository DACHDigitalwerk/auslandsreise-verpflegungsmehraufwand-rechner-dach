# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="auslandsreise-dach",
    version="1.0.0",
    description="DACH Auslandstagegeld- & Reisekostenpauschalen-Rechner 2026",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="DACH Digitalwerk",
    author_email="dach.digitalwerk@gmail.com",
    url="https://github.com/DACHDigitalwerk/auslands-reisekosten-tagegeld-rechner-dach",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Accounting",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "dach-ausland=auslandsreise_dach.cli:main",
        ],
    },
)
