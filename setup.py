import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

pkgs = setuptools.find_packages()
print('found these packages:', pkgs)

d = {}
exec(open("ml_ms4alg/version.py").read(), None, d)
version = d['version']

pkg_name="ml_ms4alg"

setuptools.setup(
    name=pkg_name,
    version=version,
    author="Jeremy Magland",
    author_email="",
    description="Mountainsort v4 for MountainLab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/magland/ml_ms4alg",
    packages=pkgs,
    package_data={
        '': ['*.mp'], # Include all processor files
    },
    install_requires=
    [
    	'dask',
        'pybind11',
        'isosplit5',
        'numpy>=1.19.4',
        'mountainlab_pytools',
        'h5py',
        'sklearn',
        'spikeextractors>=0.4.1'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    )
)
