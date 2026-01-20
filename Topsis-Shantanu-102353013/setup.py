from setuptools import setup, find_packages

setup(
    name="Topsis-Shantanu-102353013",
    version="1.0.0",
    author="Shantanu Singhal",
    author_email="example@email.com", 
    description="A Python package for implementing TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)",
    long_description=open("README.md").read() if open("README.md").read() else "",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis_shantanu_102353013.topsis:main",
        ],
    },
)
