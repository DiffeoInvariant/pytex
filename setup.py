from setuptools import setup


setup(
    name="pytex",
    packages=["pytex"],
    #make pytest plugin available
    entry_points={"pytest11" : ["pytex_file = pytex.pytest_hook"]},
    classifiers=["Framework :: Pytest"],#for PyPI support
    )
