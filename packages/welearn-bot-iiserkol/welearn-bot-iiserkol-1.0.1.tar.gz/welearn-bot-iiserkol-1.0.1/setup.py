from setuptools import setup

requirements = []
with open("requirements.txt", "r") as fh:
    for line in fh:
        requirements.append(line.strip())

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name = "welearn-bot-iiserkol",
    description = "A command line client for WeLearn, in the IISER Kolkata domain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = "Parth Bibekar",
    author_email = "bibekarparth24@gmail.com",
    url = "https://github.com/ParthBibekar/Welearn-bot",
    version = "1.0.1",
    license = "MIT",
    scripts = ["welearn_bot"],
    install_requires = requirements
)
