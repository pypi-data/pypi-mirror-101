import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="fancyconsole",
    version="0.0.1",
    author="Alexander Pfefferle",
    author_email="alex@pfefferle.xyz",
    description="fancy console with colors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/fancyconsole/",
    packages=["fancyconsole"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
