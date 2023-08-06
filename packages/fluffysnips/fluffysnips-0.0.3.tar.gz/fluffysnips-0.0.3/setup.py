import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fluffysnips",
    version="0.0.3",
    author="Jack Adamson",
    author_email="jack@mrfluffybunny.com",
    license="MIT",
    description="Various useful CLI tools",
    packages=setuptools.find_packages(),
    install_requires=["typer"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackadamson/fluffysnips",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "mvscreenshot=fluffysnips.mvscreenshot:app",
            "tablefix=fluffysnips.tablefix:app",
        ]
    },
)
