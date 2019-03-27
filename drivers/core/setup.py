from distutils.core import setup, Extension

module1 = Extension('regV',
                    sources=['robotcontrol.cpp', 'motor.cpp', 'pid.cpp'],
                    libraries=['pigpio'],)

setup(name='regV',
      version='1.0',
      description='regV robot control',
      ext_modules=[module1])

