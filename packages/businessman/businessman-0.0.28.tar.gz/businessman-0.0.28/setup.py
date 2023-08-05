import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="businessman",
    version="0.0.28",
    license='MIT',
    author="Ahmad Sharif",
    author_email="ahmad.sharif.abc@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['API', "CRUD", "restx"],
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Topic :: Software Development :: Build Tools',
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
