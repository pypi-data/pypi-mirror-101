import pathlib
import io
import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command
import version

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(version.version))
        os.system('git push --tags')

        sys.exit()


setup(name='archfx_cloud',
    version=version.version,
    description='Python client for https://archfx.io',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/iotile/python_archfx_cloud',
    author='Arch Systems Inc.',
    author_email="info@archsys.io",
    license='MIT',
    packages=find_packages(exclude=("tests",)),
    entry_points={
        'pytest11': ['mock_cloud = archfx_cloud.utils.mock_cloud']
    },
    python_requires=">=3.7,<4",
    install_requires=[
        'requests>=2.21.0',
        'python-dateutil'
    ],
    keywords=["iotile", "archfx", "arch", "iiot", "automation"],
    classifiers=[
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    zip_safe=False,
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
