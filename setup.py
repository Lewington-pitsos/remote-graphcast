import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="remote-graphcast",
    version="0.0.7",
    author="Louka Ewington-Pitsos",
    author_email="lewingtonpitsos@gmail.com",
    description="Allows people without massive GPUs to easily run graphcast on remote runpod servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lewington-pitsos/remote-graphcast",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'boto3', 
        'runpod'
	],
    python_requires='>=3.8',
)