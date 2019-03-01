from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="cpsm",
    version="0.0.0",  # Matches __init__.py
    author="Bryon Tjanaka",
    author_email="bryon.tjanaka@gmail.com",
    description=("Competitive Programming Solutions Manager"),
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=[
        "Jinja2==2.10",
    ],
    extras_require={},
    license="MIT",
    keywords="chemistry molecules forcefield",
    packages=["cpsm"],
    scripts=["bin/cpsm"],
)
