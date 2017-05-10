from setuptools import setup

setup(name='weirdpad',
      version='0.1',
      description='Class for applying wordpad effect to digital images',
      url='https://github.com/marcushaddon/weirdpad.git',
      author='Marcus Haddon',
      author_email='haddon.marcus@gmail.com',
      license='MIT',
      packages=['weirdpad'],
      install_requires=[
          'os',
          'PIL',
          'random',
          'appdirs',
          'olefile',
          'packaging',
          'Pillow',
          'pyparsing',
          'six'
      ],
      include_package_data=True,
      zip_safe=False)
