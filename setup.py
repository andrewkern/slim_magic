from codecs import open as codecs_open
from setuptools import setup, find_packages
from warnings import warn
import os


# Get the long description from the relevant file
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# After exec'ing this file we have tskit_version defined.
tskit_version = None  # Keep PEP8 happy.
version_file = os.path.join("slim_magic", "_version.py")
with open(version_file) as f:
    exec(f.read())

setup(name='slim_magic',
      version=slim_magic_version,
      description=u"ipython magic for SLiM.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[],
      keywords=['tree sequences', 'tskit', 'slim', 'ipython', 'magic'],
      author=u"Andrew Kern",
      author_email='adkern@uoregon.edu',
      url='https://github.com/andrewkern/slim_magic',
      license='MIT',
      packages=['slim_magic'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'msprime>=1.0.1',
          'tskit',
          'kastore',
          'numpy',
          'pandas',
          'jupyter',
          'matplotlib'],
      extras_require={
          'dev': [],
      },

      setup_requires=[],
      project_urls={
          'Bug Reports': 'https://github.com/andrewkern/slim_magic/issues',
          'Source': 'https://github.com/andrewkern/slim_magic/pyslim',
      },
      )
