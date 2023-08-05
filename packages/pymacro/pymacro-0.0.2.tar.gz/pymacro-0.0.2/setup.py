import setuptools

with open("README.md", "r") as f:
    _description = f.read()

setuptools.setup(
    name="pymacro",
    version="0.0.2",
    author="jay3332",
    description="PyMacro can automate your tasks inside of Python.",
    long_description=_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "pyautogui",
        "pytweening"
    ],
    url="https://github.com/jay3332/PyMacro",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)