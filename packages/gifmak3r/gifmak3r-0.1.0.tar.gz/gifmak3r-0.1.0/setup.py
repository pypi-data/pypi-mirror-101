# pylint: skip-file
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gifmak3r",
    version="0.1.0",
    author="Fahim Hussain",
    author_email="fahimhussain21@gmail.com",
    description="A gif generator in Python that creates gifs in user-specified formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frykher/gif-mak3r",
    project_urls={
        "Bug Tracker": "https://github.com/frykher/gif-mak3r/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], 
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["Pillow"]
)