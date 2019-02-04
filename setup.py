from distutils.core import setup
from Cython.Build import cythonize

setup(name='Space Invaders',
      ext_modules=cythonize("draw.pyx"))
