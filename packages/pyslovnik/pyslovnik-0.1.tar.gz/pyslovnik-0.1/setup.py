from setuptools import find_packages, setup

setup(
    name="pyslovnik",
    packages=find_packages(include=["PySlovnik"]),
    version="0.1",
    description="Python wrapper pro Internetovou jazykovou příručku od Ústavu pro jazyk český Akademie věd České republiky",
    url='http://github.com/CrumblyLiquid/PySlovnik',
    author="CrumblyLiquid",
    author_email="crumblyliquid@gmail.com",
    download_url="https://github.com/CrumblyLiquid/PySlovnik/archive/refs/tags/0.1.tar.gz",
    license="GNU GPLv3",
    keywords=["czech", "dictionary"],
    install_requires=["requests", "bs4"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)