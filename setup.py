from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="cpsm",
    version="1.0.0",  # Matches __init__.py
    author="Bryon Tjanaka",
    author_email="bryon.tjanaka@gmail.com",
    description="Competitive Programming Solutions Manager",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/btjanaka/cpsm",
    install_requires=[
        "Jinja2==2.10",
    ],
    extras_require={},
    license="MIT",
    keywords="competitive-programming solutions kattis leetcode hackerrank uva",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    include_package_data=True,
    packages=["cpsm"],
    scripts=["bin/cpsm"],
)
