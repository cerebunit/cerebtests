# ~/cerebtests/setup.py
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
        name="cerebtests",
        version="0.0.1",
        author="Lungsi",
        author_email="lungsi.sharma@unic.cnrs-gif.fr",
        #packages=find_packages(),
        packages=["cerebtests",
                  #"cerebtests.file_manager",
                  #"cerebtests.test_manager",
                  # capabilities 
                  "cerebtests.capabilities",
                  "cerebtests.capabilities.cells",
                  # validation_tests
                  "cerebtests.validation_tests",
                  "cerebtests.validation_tests.cells",
                  #"cerebtests.validation_tests.cells.general",
                  "cerebtests.validation_tests.cells.Purkinje",
                  "cerebtests.validation_tests.cells.Granule",
                  #"cerebtests.validation_tests.cells.GolgiCell"
                  ],
        url="https://github.com/cerebunit/cerebtests",
        download_url = "https://github.com/cerebunit/cerebtests/archive/v0.0.1.tar.gz",
        keywords = ["VALIDATION", "CEREBELLUM", "NEUROSCIENCE",
                    "MODELING", "SCIENTIFIC METHOD"],
        license="BSD Clause-3",
        description="Installable package 'cerebtests' for cerebunit",
        long_description="Package for running validation test on cerebellum models. Three components of CerebUnit: CerebModels, CerebData, CerebStats (install) and CerebTests (install).",
        install_requires=[
            "sciunit",
            "quantities",
            "scipy",
            "numpy",
            "cerebstats",
            ],
        classifiers = [
            # "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as current state of package
            "Development Status :: 4 - Beta",
            # Define audience
            "Intended Audience :: Developers",
            # License
            "License :: OSI Approved :: BSD License",
            # Specify supported python versions
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            ],
)
