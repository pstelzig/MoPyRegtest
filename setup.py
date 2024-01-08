import setuptools
import re

with open("README.md") as fh:
    long_description = fh.read()
    md_links_re = re.compile(r"\[(.+)\]\(/([^\)]*)\)")
    long_description = md_links_re.sub(r"[\1](https://github.com/pstelzig/MoPyRegtest/tree/master/\2)", long_description)

setuptools.setup(
    name="MoPyRegtest",
    version="0.5.0-rc.1",
    author="Philipp Emanuel Stelzig",
    description="A Python enabled simple regression testing framework for Modelica models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pstelzig/mopyregtest",
    packages=setuptools.find_packages(),
    package_data={"mopyregtest": ["templates/omc/model_import.mos.template",
                                  "templates/omc/model_simulate.mos.template"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3.8',
    install_requires=[
        "numpy",
        "pandas"
    ],
    entry_points={
        'console_scripts': [
            'mopyregtest = mopyregtest.cli:main',
        ]
    }
)
