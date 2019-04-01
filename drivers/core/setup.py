from distutils.core import setup, Extension

module2 = Extension('regV',
                    sources=['main.cpp', 'enc.cpp', 'motor.cpp', 'pid.cpp'],
                    libraries=['pigpio'],)

setup(name='regV',
      version='1.0',
      description='regV robot control',
      ext_modules=[module2])

