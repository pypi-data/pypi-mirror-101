from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
  long_description = f.read()

setup(name='packrequest',  # 包名
      version='2.0.0',  # 版本号
      description='A small example package',
      long_description=long_description,
      author='sunny99sun',
      author_email='sunny99sun@foxmail.com',
      url='https://github.com/sunny99sun/pytest/',
      install_requires=[],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      #package_dir={"": "pt-test"},
      #packages=setuptools.find_packages(where="src"),
      )