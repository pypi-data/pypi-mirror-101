import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="s3dxrd",
    version="0.0.2",
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
    install_requires=[  "ImageD11>=1.9.7", 
                        "numpy", 
                        "numba>=0.53.1", 
                        "Shapely>=1.70", 
                        "scipy",
                        "torch>=1.6.0"
                        "pickle",
                        "xfab>=0.0.4",
                        "fabio>=0.10.2",
                        "h5py" ]
)

# fastcache==1.1.0
# gmpy2==2.0.8
# idna @ file:///home/conda/feedstock_root/build_artifacts/idna_1593328102638/work
# ImageD11==1.9.7
# imageio==2.9.0
# imagesize==1.2.0
# ipython @ file:///tmp/build/80754af9/ipython_1598883821407/work
# ipython-genutils==0.2.0
# jedi @ file:///tmp/build/80754af9/jedi_1598371611696/work
# Jinja2 @ file:///home/conda/feedstock_root/build_artifacts/jinja2_1612119311452/work
# kiwisolver==1.2.0
# llvmlite==0.36.0
# MarkupSafe @ file:///home/conda/feedstock_root/build_artifacts/markupsafe_1602267312178/work
# matplotlib @ file:///tmp/build/80754af9/matplotlib-base_1597876319132/work
# mkl-fft==1.1.0
# mkl-random==1.1.1
# mkl-service==2.3.0
# mpmath==1.1.0
# networkx==2.5
# numba==0.53.1
# numpy @ file:///tmp/build/80754af9/numpy_and_numpy_base_1596233721170/work
# olefile==0.46
# packaging @ file:///home/conda/feedstock_root/build_artifacts/packaging_1612459636436/work
# parso==0.7.0
# pep517==0.10.0
# pexpect==4.8.0
# pickleshare==0.7.5
# Pillow @ file:///tmp/build/80754af9/pillow_1594307295532/work
# prompt-toolkit @ file:///tmp/build/80754af9/prompt-toolkit_1598885458782/work
# ptyprocess==0.6.0
# pycparser @ file:///home/conda/feedstock_root/build_artifacts/pycparser_1593275161868/work
# pyevtk==1.1.2
# Pygments==2.6.1
# PyOpenGL==3.1.5
# pyopengltk==0.0.3
# pyOpenSSL==19.1.0
# pyparsing==2.4.7
# PySocks @ file:///home/conda/feedstock_root/build_artifacts/pysocks_1610291447907/work
# python-dateutil==2.8.1
# pytz @ file:///home/conda/feedstock_root/build_artifacts/pytz_1612179539967/work
# PyWavelets==1.1.1
# rasterio==1.1.6
# requests @ file:///home/conda/feedstock_root/build_artifacts/requests_1608156231189/work
# # Editable install with no version control (s3dxrd==0.0.1)
# -e /home/axel/.local/lib/python3.8/site-packages
# scikit-image==0.17.2
# scipy @ file:///tmp/build/80754af9/scipy_1597686649129/work
# Shapely==1.7.0
# sip==4.19.13
# six==1.15.0
# snowballstemmer @ file:///home/conda/feedstock_root/build_artifacts/snowballstemmer_1611270869511/work
# snuggs==1.4.7
# Sphinx @ file:///home/conda/feedstock_root/build_artifacts/sphinx_1616256380770/work
# sphinx-rtd-theme @ file:///home/conda/feedstock_root/build_artifacts/sphinx_rtd_theme_1609854399947/work
# sphinxcontrib-applehelp==1.0.2
# sphinxcontrib-devhelp==1.0.2
# sphinxcontrib-htmlhelp==1.0.3
# sphinxcontrib-jsmath==1.0.1
# sphinxcontrib-qthelp==1.0.3
# sphinxcontrib-serializinghtml==1.1.4
# sympy @ file:///tmp/build/80754af9/sympy_1598376323917/work
# tifffile==2020.9.3
# toml==0.10.2
# torchvision==0.7.0
# tornado==6.0.4
# traitlets==4.3.3
# urllib3 @ file:///home/conda/feedstock_root/build_artifacts/urllib3_1615828766818/work
# wcwidth @ file:///tmp/build/80754af9/wcwidth_1593447189090/work
# xfab==0.0.4
