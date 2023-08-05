from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Class/Attribute Model Generator'
LONG_DESCRIPTION = 'Class/Attribute models generated from YAML'

setup(
       # the name must match the folder name 'verysimplemodule'
        name="clamg", 
        version=VERSION,
        author="Spencer Rak",
        author_email="<spencer.rak@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'PyYAML'
        ],
        keywords=['yaml', 'class'],
        classifiers= []
)
