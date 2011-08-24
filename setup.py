from setuptools import setup

from version import get_git_version


setup(name='deterministic-dingus',
      version=get_git_version(),
      description='A handy extension of the dingus record and assert library',
      long_description=file('README.rst').read(),
      author='Allan Caffee',
      author_email='allan.caffee@gmail.com',
      install_requires=['dingus'],
      py_modules=['deterministic_dingus'],
      license='BSD',
      url='https://github.com/allancaffee/deterministic-dingus',
      keywords='testing test mocking mock double stub fake record assert',
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Testing",
                   ],
     )
