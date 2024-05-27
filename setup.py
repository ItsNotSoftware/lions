from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lions",
    version="1.4.5",
    author="Diogo Ferreira",
    author_email="itsnotsoftware@gmail.com",
    description="LIONS (Lightweight IoT Network Specification) is a communication protocol designed for IoT mesh/ad hoc networks. It facilitates seamless communication between devices and includes code generation based on message files (yaml), streamlining development and implementation processes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"lions": ["cpp_gen/templates/*.jinja"]},
    url="https://github.com/ItsNotSoftware/lions",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=["pydantic", "pyyaml", "jinja2", "pytest", "colorama"],
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "lions = lions.main:main",
        ],
    },
)
