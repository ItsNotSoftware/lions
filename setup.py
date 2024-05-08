from setuptools import setup, find_packages

setup(
    name="lions",
    version="1.0.0",
    author="Diogo Ferreira",
    author_email="itsnotsoftware@gmail.com",
    description="LIONS (Lightweight IoT Network Specification) is a communication protocol designed for IoT mesh/ad hoc networks. It facilitates seamless communication between devices and includes code generation based on message files (yaml), streamlining development and implementation processes.",
    packages=find_packages(),
    install_requires=["pydantic", "pyyaml", "jinja2", "pytest", "colorama"],
    entry_points={
        "console_scripts": [
            "lions = lions.main:main",
        ],
    },
)
