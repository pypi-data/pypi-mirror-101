from setuptools import setup

setup(name="polyhedra",
    version="0.3",
    description="Various tools for manipulating 3D polyhedra and converting them to STL files.",
    author="Franklin Pezzuti Dyer",
    author_email="franklin+polyhedra@dyer.me",
    packages=["polyhedra"],
    install_requires=[
        "numpy",
        "os"
    ],
    zip_safe=False)
