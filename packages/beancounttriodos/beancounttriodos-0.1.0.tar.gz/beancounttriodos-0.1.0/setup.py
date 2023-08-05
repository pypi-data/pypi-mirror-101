import setuptools

from beancounttriodos import VERSION


with open('LICENSE', encoding='utf-8') as fd:
    licensetext = fd.read()


setuptools.setup(name='beancounttriodos',
      version=VERSION,
      description="CSV importer script from Triodos online banking for beancount",
      url="https://github.com/vonshednob/beancount-triodos-importer",
      author="R",
      author_email="devel+beancount-triodos-this-is-spam@kakaomilchkuh.de",
      license=licensetext,
      py_modules=['beancounttriodos'],
      data_files=[],
      requires=['beancount'],
      python_requires='>=3.5',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   ])
