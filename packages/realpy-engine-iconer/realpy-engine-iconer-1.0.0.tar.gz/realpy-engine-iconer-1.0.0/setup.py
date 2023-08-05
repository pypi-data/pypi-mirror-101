import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="realpy-engine-iconer",  # Replace with your own username
    version="1.0.0",
    author="Iconerworks",
    author_email="yoyofa2@hotmail.com",
    description="2D game engine with pygame",
    license="LICENSE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RealPy-Engine/realpy-core",
    project_urls={
        "Bug Tracker": "https://github.com/RealPy-Engine/realpy-core/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
)
