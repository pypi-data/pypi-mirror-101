import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cocaddy",
    version="0.0.1a1",
    author="MisakiCoca",
    author_email="misakicoca@gmail.com",
    description="cotton candy instance python version",
    long_description="inside test",
    long_description_content_type="text/markdown",
    url="https://github.com/misakicoca/cotton-instance",
    project_urls={
        "Bug Tracker": "https://github.com/misakicoca/cotton-instance/issues",
    },
    classifiers=["Programming Language :: Python :: 3"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
