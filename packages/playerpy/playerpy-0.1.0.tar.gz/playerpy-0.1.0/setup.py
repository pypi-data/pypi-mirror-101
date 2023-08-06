from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys
import os

# Read the version but avoid importing the __init__.py since
# we might not have all dependencies installed
with open(os.path.join(os.path.dirname(__file__), "playerpy", "version.py")) as fp:
    exec(fp.read())

class PyTestCommand(TestCommand):
    user_options = []

    def finalize_options(self):
        pass

    def run_tests(self):
        import pytest
        errno = pytest.main()
        sys.exit(errno)

setup(
    name='playerpy',
    description='Video player in python',
    long_description='''
A simple video player with quick key-bindings for play, reverse,
goto frame number etc. Class is easily extendible for other
projects, e.g. data annotation tools.
    ''',
    version=__version__,
    packages=['playerpy'],
    url='https://github.com/daniel-falk/playerpy',
    download_url='https://github.com/daniel-falk/playerpy/archive/refs/tags/v%s.tar.gz' % __version__,
    author='Daniel Falk',
    author_email='daniel.falk.1@fixedit.ai',
    license='MIT',
    cmdclass={'test': PyTestCommand},
    tests_require=['pytest'],
    install_requires=[
        "vi3o",
        "pyglet",
        "pathlib",
        "pillow",
        "imageio",
        "imageio-ffmpeg",
    ],
    entry_points = {
        'console_scripts': ['playerpy=playerpy:play_cmd'],
    }
)
