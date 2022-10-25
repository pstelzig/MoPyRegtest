import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MoPyRegtest",
    version="0.1.0",
    author="Philipp Emanuel Stelzig",
    description="A Python enabled simple regression testing framework for Modelica models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/pstelzig/mopyregtest",
    packages=setuptools.find_packages(),
    package_data={"mopyregtest": ["templates/omc/model_import.mos.template",
                                  "templates/omc/model_simulate.mos.template"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3.8'
)
