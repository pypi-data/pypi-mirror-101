from setuptools import setup
import pypandoc


def get_version(path):
    with open(path, "r") as fp:
        lines = fp.read()
    for line in lines.split("\n"):
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(name='lagmat',
      version=get_version("lagmat/__init__.py"),
      description=(
          "Lagmatrix. Create array with time-lagged copies of the features"),
      long_description=pypandoc.convert('README.md', 'rst'),
      url='http://github.com/ulf1/lagmat',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['lagmat'],
      install_requires=[
          'setuptools>=40.0.0',
          'numpy>=1.14.*,<2'],
      python_requires='>=3.6',
      zip_safe=True)
