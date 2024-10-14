from setuptools import setup, find_packages

setup(
    name="ferpy",
    version="0.1.0",
    author="Jon Gabirondo-López",
    author_email="jon.gabirondol@ehu.eus",
    description="A Python implementation of the FER data structure.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jongablop/ferpy",
    license="GPL-3.0",
    packages=find_packages(),  # Automatically find packages in the fer_py directory
    install_requires=[],       # List any dependencies here, e.g., ["numpy", "pandas"]
    python_requires=">=3.6",   # Specify the Python versions supported
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
