from setuptools import setup, find_packages

VERSION = '0.1.1.2' 
DESCRIPTION = 'A python module using Veerer for drawing flat structures of triangulations in Jupyter Notebook'
#LONG_DESCRIPTION = 'My first Python package with a slightly longer description'
def readme():
    with open('README.txt') as f:
        return f.read()
# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name='displayFlips', 
        version=VERSION,
        authors="Van Khanh Ho, Matthieu Ralison, Sarah Besnard, Hugo Bergon, Laurent Lahely",
#       author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description=readme(),
        packages=['displayFlips'],
        package_data={
            "": ["JS/*.js"]
        },
        include_package_data=True
#        install_requires=['veerer', 'surface_dynamics', 'sage'],
        
        # keywords=['python', 'first package'],
        # classifiers= [
        #     "Development Status :: 3 - Alpha",
        #     "Intended Audience :: Education",
        #     "Programming Language :: Python :: 2",
        #     "Programming Language :: Python :: 3",
        #     "Operating System :: MacOS :: MacOS X",
        #     "Operating System :: Microsoft :: Windows",
        # ]
)