from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="interactions_dynamic_help",
    version="1.0.3",
    description="Unofficial Dynamic Help Command for interactions.py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pilot1782/interactions-dynamic-help",
    author="Pilot1782",
    author_email="",
    license="GNU",
    packages=["interactions.ext.dynhelp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["discord-py-interactions", "docstring-parser"],
)
