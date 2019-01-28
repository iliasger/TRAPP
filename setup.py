from setuptools import setup, find_packages

# this is a python install script
# call it with >setup.py install
# to install all dependencies

setup(
    name='TRAPP',
    version='0.1',
    long_description="Traffic Reconfiguration and Adaptive Planning Framework",
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'msgpack-python',
        'colorama',
        'Dijkstar',
        'numpy'
    ]
)
