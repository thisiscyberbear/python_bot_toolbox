import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
	
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="python-bot-toolbox-cyberbear",
    version="0.0.1",
	install_requires=requirements,
    author="Marc-André Bär",
    author_email="thisiscyberbear@gmail.com",
    description="A bot toolbox which contains several tools to create python bot scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thisiscyberbear/python_bot_toolbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)