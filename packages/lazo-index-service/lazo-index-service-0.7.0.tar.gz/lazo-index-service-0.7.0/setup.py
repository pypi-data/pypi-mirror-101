import os
from setuptools import setup


os.chdir(os.path.abspath(os.path.dirname(__file__)))


req = [
    'grpcio>=1.21,<2',
    'protobuf>=3.8'
]
setup(name='lazo-index-service',
      version='0.7.0',
      packages=['lazo_index_service'],
      install_requires=req,
      description="API for accessing the Lazo index.",
      author="Fernando Chirigati",
      author_email='fchirigati@nyu.edu',
      maintainer="Remi Rampin",
      maintainer_email='remi.rampin@nyu.edu',
      url='https://gitlab.com/ViDA-NYU/auctus/lazo-index-service',
      project_urls={
          'Homepage': 'https://gitlab.com/ViDA-NYU/auctus/'
                      + 'lazo-index-service',
          'Source': 'https://gitlab.com/ViDA-NYU/auctus/'
                    + 'lazo-index-service',
          'Tracker': 'https://gitlab.com/ViDA-NYU/auctus/'
                     + 'auctus/-/issues',
      },
      long_description="API for accessing the Lazo index.",
      license='Apache-2.0',
      keywords=['lazo'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Database :: Front-Ends',
          'Topic :: Scientific/Engineering :: Information Analysis'])
