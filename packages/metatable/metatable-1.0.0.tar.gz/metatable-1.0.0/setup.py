from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="metatable",
    version="1.0.0",
    packages=["metatable",],
    install_requires=["symbolism",],
    license="MIT",
    url="https://github.com/reity/metatable",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Extensible table data structure that supports concise "+\
                "workflow descriptions via user-defined combinators.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
