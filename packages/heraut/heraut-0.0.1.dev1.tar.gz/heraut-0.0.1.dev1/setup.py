import setuptools

with open("ReadMe.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="heraut",
    version="0.0.1dev1",
    author="Michael Kupperman",
    author_email="kupperma@uw.edu",
    description="The herald of python message passing between threads and processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkupperman/heraut",
    project_urls={
        "Bug Tracker": "https://github.com/mkupperman/heraut/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=['watchdog>=2.0.0'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
