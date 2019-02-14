from setuptools import setup
from Cython.Build import cythonize

setup(name='Space Invaders',
      description='A Space Invaders (Intel 8080) emulator ',
      url='https://github.com/Andrix44/Space-Invaders',
      install_requires=[
            'Cython', 'pygame'
      ],
      ext_modules=cythonize('hotcode.pyx'))
