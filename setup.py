import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FitGaze-CodeHeist", 
    version="0.0.1",
    author="CodeHeist",
    author_email="marvelvarghese18@gmail.com",
    description="An gaze tracking package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/codeheist/2020_CSB05_EYETRACKING.git",
    packages=['FitGaze'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)