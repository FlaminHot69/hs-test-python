from setuptools import find_namespace_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="hs-test-python",
    version="3.0.0",
    author="Vladimir Turov",
    author_email="vladimir.turov@stepik.org",
    description="A small framework that simplifies testing educational projects for https://hyperskill.org/.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/hyperskill/hs-test-python",
    packages=find_namespace_packages(exclude=['tests']),
    python_requires=">=3.6",
    install_requires=[
        "psutil==5.8.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6"
    ],
)
