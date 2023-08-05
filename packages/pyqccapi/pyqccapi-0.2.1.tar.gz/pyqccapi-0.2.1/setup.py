import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyqccapi",
    version="0.2.1",
    author="roventine",
    author_email="ukyotachibana@yeah.net",
    description="simple api task for qcc",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/roventine/pyqccapi",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['requests', 'PyYAML','pywildcard','Logbook'],
)