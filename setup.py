from setuptools import setup, find_packages

setup(
    name="metronome_extractor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    description="A package to extract metronome tracks from .gp files",
    author="Your Name",
    author_email="your.email@example.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)