from setuptools import setup, find_packages
from setuptools.command.egg_info import egg_info


class egg_info_ex(egg_info):
    """ Includes license file into `.egg-info` folder.

    :ref: https://stackoverflow.com/a/66443941
    """

    def run(self):
        # don't duplicate license into `.egg-info` when building a distribution
        if not self.distribution.have_run.get('install', True):
            # `install` command is in progress, copy license
            self.mkpath(self.egg_info)
            self.copy_file('LICENSE', self.egg_info)

        egg_info.run(self)


setup(
    name='loggz',
    version='0.1.0',
    author='Deepnox',
    author_email='opensource@deepnox.io',
    packages=find_packages(include=['loggz']),
    url='http://pypi.python.org/pypi/loggz/',
    license='MIT',
    cmdclass = {'egg_info': egg_info_ex},
    license_files=('LICENSE',),
    description='A helper to implement simple but standard and jsonified strategies for logging.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Logging',
    ],
    test_suite='tests',
)
