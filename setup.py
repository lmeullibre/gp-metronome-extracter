from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="metronome_extractor",
    version="0.1.6",  
    author="Sergi Martinez",
    author_email="sergimartinezrodriguez@gmail.com",
    description="A package to generate metronome tracks from Guitar Pro files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lmeullibre/gp-metronome-extractor",
    packages=find_packages(),
    tests_require=["pytest"],
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)