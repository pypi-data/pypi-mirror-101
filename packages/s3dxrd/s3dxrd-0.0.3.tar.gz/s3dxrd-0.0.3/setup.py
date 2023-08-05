import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="s3dxrd",
    version="0.0.3",
    author="Axel Henningsson",
    author_email="nilsaxelhenningsson@gmail.com",
    description="Tools for intragranular strain estimation with s3dxrd data.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://bitbucket.org/Axiomel/gp-xrd/src/multigrain/",
    project_urls={
        "Documentation": "https://bitbucket.org/Axiomel/gp-xrd/src/multigrain/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[  "numpy",
                        "scipy",
                        "scikit-image>=0.17.2",
                        "torch>=1.6.0",
                        "pickle",
                        "h5py",
                        "matplotlib",
                        "numba>=0.53.1",
                        "rasterio>=1.1.6",
                        "Shapely>=1.7.0",
                        "ImageD11>=1.9.7",
                        "xfab>=0.0.4",
                        "fabio>=0.10.2",
                        "pyevtk>=1.1.2" ]
)
