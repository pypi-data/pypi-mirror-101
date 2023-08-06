import setuptools

# read the contents of your README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ofpubsub",
    version="0.7",
    author="Mejik",
    author_email="mejik.dev@gmail.com",
    description="OnlyFunction PubSub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mejik/ofpubsub",
    install_requires=['requests'],
    packages=['ofpubsub'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
     python_requires='>=3.5',
)