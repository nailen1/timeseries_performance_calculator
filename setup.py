from setuptools import setup, find_packages

setup(
    name="timeseries_performance_calculator",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        req.strip() for req in open("requirements.txt", encoding="utf-8")
        if req.strip() and not req.strip().startswith("#")
    ],
    author="June Young Park",
    author_email="juneyoungpaak@gmail.com",
    description="A Python package for calculating and analyzing time series performance metrics",
    long_description=open("README.md", encoding="utf-8").read() if open("README.md", encoding="utf-8", errors='ignore') else "",
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Office/Business :: Financial",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
    ],
)
