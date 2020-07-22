from setuptools import setup


setup(
    name="pytex",
    version='1.0',
    description="Make LaTeX documents from Python code and from Pytest output",
    packages=["pytex"],
    #make pytest plugin available
    entry_points={"pytest11" : ["pytex_file = pytex.pytest_hook"]},
    classifiers=["Framework :: Pytest"],#for PyPI support
    )
