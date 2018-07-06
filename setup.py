import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

pkgs = setuptools.find_packages()
print('found these packages:', pkgs)

setuptools.setup(
    name="ml_ms4alg",
    version="0.0.1",
    author="Jeremy Magland",
    author_email="",
    description="Mountainsort v4 for MountainLab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/magland/ml_ms4alg",
    packages=pkgs,
    package_data={
        '': ['*.mp'], # Include all processor files
        'ml_ms4alg': ['mlscripts/*']
    },
    install_requires=
    [
        'pybind11',
        'isosplit5',
        'numpy',
        'mountainlab_pytools',
        'h5py'
    ],
    dependency_links=[
        'https://github.com/tjd2002/mltools/tarball/pypi-mountainlab_pytools#egg=mountainlab_pytools-0.1.2a',
        'https://github.com/tjd2002/isosplit5_python/tarball/pypi#egg=isosplit5-0.1.0'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
)
