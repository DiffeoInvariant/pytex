from setuptools import setup


setup(
    name="pytex",
    version="0.1.0",
    packages=["pytex"],
    #make pytest plugin available
    entry_points={"pytest11" : ["pytex_file = pytex.pytest_hook"]},
    classifiers=["Framework :: Pytest"],#for PyPI support
    )
